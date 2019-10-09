import logging

from flask import g, jsonify
from redis.exceptions import DataError
import redis
from server.redis_cache.redis_model import RedisEntry


from server.redis_cache.poolmanager import (
    global_poolman,
    global_pipe,
    map_dict_signature,
    return_signature,
)
from server.logging import make_logger

logger = make_logger(__name__)
DEFAULT_USER_EXPIRE = 60 * 60 * 2

NO_SID = "NO_SID"

USER_SIG = {"id": int, "username": str, "online": int, "sid": str}


class UserEntry(RedisEntry):
    USER_SIG = {"id": int, "username": str, "online": int, "sid": str}
    NO_SID = "NO_SID"
    DEFAULT_USER_EXPIRE = 60 * 60 * 2

    def __init__(self, user_id, username, online, sid=None, threads=None):
        from server.redis_cache.message_cache import ThreadEntry

        logger.debug(f"Creating UserEntry-{user_id}")
        self.user_id = user_id
        self.username = username
        self.online = online
        if isinstance(threads, ThreadEntry):
            self._threads = [threads]
        else:
            self._threads = None
        self.sid = sid if sid else NO_SID

        super().__init__(user_id)

    @property
    def threads(self):
        if self._threads is None:
            self.get_threads()
        return self._threads

    @threads.setter
    def threads(self, threads):
        self._threads = threads
        threads.commit()

    def get_threads(self):
        from server.redis_cache.message_cache import ThreadEntry

        logger.debug("Inside get_threads")
        raw_thread_ids = self._R.smembers(f"user:{self.user_id}:threads")
        if raw_thread_ids:

            thread_ids = list(map(lambda th: int(th.decode("utf-8")), raw_thread_ids))
            logger.debug(f"thread_ids: {thread_ids}")
            self._threads = [ThreadEntry.from_id(thread_id) for thread_id in thread_ids]
        else:
            self._threads = []

    @classmethod
    def from_user_id(cls, user_id, thread=None):
        if cls._object_is_saved(user_id):
            return cls._get_saved_object(user_id)
        try:
            user_id = int(user_id)
            if cls._R.exists(f"user:{user_id}"):
                raw_user_data = cls._R.hgetall(f"user:{user_id}")
                user_data = cls.fix_hash_signature(raw_user_data, cls.USER_SIG)
                username, online, sid = (
                    user_data["username"],
                    user_data["online"],
                    user_data["sid"],
                )
                return cls(user_id, username, online, sid, threads=thread)

            else:
                logger.error(f"User {user_id} does not exist")
                return {}
        except Exception as e:
            logger.error("Error thrown in `from_user_id`")
            logger.error(e)
            raise type(e)

    @classmethod
    def from_sid(cls, sid):
        user_id = int(cls._R.get(f"user:sid:{sid}"))
        return cls.from_user_id(user_id)

    @classmethod
    def get_online_users(cls):
        try:
            raw_user_ids = [
                int(user_id.decode("utf-8"))
                for user_id in cls._R.sscan_iter("user:online")
            ]
            user_list = {
                user_id: cls.fix_hash_signature(
                    cls._R.hgetall(f"user:{user_id}"), cls.USER_SIG
                )
                for user_id in raw_user_ids
            }
            return user_list
        except Exception as e:
            logger.error(e)
            raise type(e)

    @classmethod
    def user_is_online(cls, user_id):
        return cls._R.sismember("user:online", user_id)

    def _set_user_offline(self):
        if self.sid is None:
            raise DataError

        with self._R.pipeline() as pipe:
            pipe.get(f"user:sid:{self.sid}")
            pipe.delete(f"user:sid:{self.sid}")
            pipe.srem("user:online", self.user_id)
            pipe.hset(f"user:{self.user_id}", "online", 0)
            pipe.hset(f"user:{self.user_id}", "sid", NO_SID)
            pipe.execute()

    def _set_user_online(self):
        with self._R.pipeline() as pipe:

            logger.info(f"Setting user online: {self.user_id}")
            pipe.sadd("user:online", self.user_id)
            pipe.hmset(
                f"user:{self.user_id}",
                {
                    "username": self.username,
                    "online": 1,
                    "id": self.user_id,
                    "sid": self.sid,
                },
            )
            pipe.set(f"user:sid:{self.sid}", self.user_id)
            pipe.expire(f"user:{self.user_id}", self.DEFAULT_USER_EXPIRE)
            try:
                for thread in self.threads:
                    pipe.sadd(f"user:{self.user_id}:threads", thread.thread_id)
                pipe.expire(f"user:{self.user_id}:threads", self.DEFAULT_USER_EXPIRE)
            except AttributeError:
                logger.error(f"No threads attached to user object: {self.user_id}")

            pipe.execute()
            logger.info(pipe.hgetall(f"user:{self.user_id}").execute())
            logger.info(f"user:{self.user_id}")

    #! UNFINISHED
    def commit(self):
        # Set user sid
        if self._R.exists(f"user:sid:{self.sid}") or self._R.hget(
            f"user:{self.user_id}", "sid"
        ):

            if (
                self._R.hget(f"user:{self.user_id}", "sid").decode("utf-8")
                != self.NO_SID
            ):
                raise DataError("User SID already set")

        self._R.set(f"user:sid:{self.sid}", self.user_id)
        self._R.hset(f"user:{self.user_id}", "sid", self.sid)
        logger.info(f"user:{self.user_id} sid set to {self.sid}")

        #! VV Not true VV. Must catch exception
        # Everything commited, so session is no longer dirty
        self.dirty = False

    def extend_data(self):
        with self._R.pipeline() as pipe:
            pipe.expire(f"user:{self.user_id}", self.DEFAULT_USER_EXPIRE)
            pipe.expire(f"user:{user_id}:threads", SELF.DEFAULT_USER_EXPIRE)
            pipe.execute()

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __ne__(self, other):
        return not self.__eq__(other)

