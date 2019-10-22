import logging

from flask import g, jsonify
from redis.exceptions import DataError
import socketio
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


class UserEntry(RedisEntry):
    """
    REDIS STRUCTURE
    
        user:<user_id> -> {id, username, online, sid}
        user:sid:<sid> -> user_id
    """

    # CLASS VARIABLES

    USER_SIG = {"id": int, "username": str, "online": int, "sid": str}
    NO_SID = "NO_SID"
    DEFAULT_USER_EXPIRE = 60 * 60 * 2

    # CONSTRUCTORS

    def __init__(
        self,
        user_id: int,
        username: str,
        online: bool,
        sid: str = None,
        threads: list = None,
    ):
        from server.redis_cache.message_cache import ThreadEntry

        self.user_id = user_id
        self.username = username
        self.online = online
        if isinstance(threads, ThreadEntry):
            self._threads = [threads]
        else:
            self._threads = None
        self.sid = sid if sid else NO_SID

        super().__init__(user_id)

    @classmethod
    def from_user_id(cls, user_id):
        logger.debug(f"Loading user from user_id: {user_id}")
        user_id = int(user_id)

        # Get cached object
        if cls._object_is_saved(user_id):
            return cls._get_saved_object(user_id)

        try:

            raw_user_data = cls._R.hgetall(f"user:{user_id}")

        # Catches user not existing
        except Exception as e:
            logger.error("Error thrown in `from_user_id`\nUser does not exist")

            logger.error(e)
            raise type(e)

        user_data = cls.fix_hash_signature(raw_user_data, cls.USER_SIG)
        username, online, sid = (
            user_data["username"],
            user_data["online"],
            user_data["sid"],
        )
        return cls(user_id, username, online, sid)

    @classmethod
    def from_sid(cls, sid):
        logger.debug(f"Loading user from sid: {sid}")
        user_id = int(cls._R.get(f"user:sid:{sid}"))
        return cls.from_user_id(user_id)

    # MAGIC METHODS

    def __str__(self):
        return f"<UserEntry| user_id: {self.user_id} username: {self.username} online: {self.online}>"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __ne__(self, other):
        return not self.__eq__(other)

    # PROPERTIES

    """
        Lazy loads threads. Prevents loading threads from cache 
        for no reason. Might be unnecessary after adding in-class 
        caching.
    """

    @property
    def threads(self):
        if self._threads is None:
            self._get_threads()
            try:
                for thread in self._threads:
                    logger.debug("CALLING JOIN ROOM")
                    socketio.join_room(room=thread.room_name, sid=self.sid)
                    logger.debug(
                        f"User ({self.user_id}) joined room {thread.room_name} "
                    )
            except Exception as e:
                logger.error(f"Error joining thread rooms: {e}")
                logger.error(f"{type(e)}")
        return self._threads

    @threads.setter
    def threads(self, threads):
        self._threads = threads
        threads.commit()

    # STATIC CLASS METHODS

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
            logger.error(f"Error retrieving online users: {e}")
            raise type(e)

    @classmethod
    def user_is_online(cls, user_id):
        return cls._R.sismember("user:online", user_id)

    # HELPER METHODS

    # TODO Make sure this isnt called outside of the class
    # Helper function that loads threads into `threads` instance variable
    def _get_threads(self):
        from server.redis_cache.message_cache import ThreadEntry

        raw_thread_ids = self._R.smembers(f"user:{self.user_id}:threads")
        # If redis loads something, fix the response and set threads
        if raw_thread_ids:
            thread_ids = list(map(lambda th: int(th.decode("utf-8")), raw_thread_ids))
            self._threads = [ThreadEntry.from_id(thread_id) for thread_id in thread_ids]
        # Else return empty list
        else:
            self._threads = []

    # Sets the user offline. Duh. Raises a DataError if the user isnt
    # found in redis.
    def _set_user_offline(self):
        if self.sid is None:
            raise DataError

        with self._R.pipeline() as pipe:

            pipe.delete(f"user:sid:{self.sid}")
            pipe.srem("user:online", self.user_id)
            pipe.hset(f"user:{self.user_id}", "online", 0)
            pipe.hset(f"user:{self.user_id}", "sid", NO_SID)
            pipe.execute()

    # ? Could be 'public'?
    # Sets user to online in redis
    def _set_user_online(self):
        with self._R.pipeline() as pipe:

            # Setting user:<userid>
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

            # setting user:sid:<sid>
            pipe.set(f"user:sid:{self.sid}", self.user_id)
            pipe.expire(f"user:{self.user_id}", self.DEFAULT_USER_EXPIRE)

            # ? Probably could be safely removed/removed with little issue
            # Catches the thread objects not loading a user
            try:
                # Adds all associated threads to redis
                for thread in self.threads:
                    pipe.sadd(f"user:{self.user_id}:threads", thread.thread_id)
                pipe.expire(f"user:{self.user_id}:threads", self.DEFAULT_USER_EXPIRE)
            except AttributeError:
                logger.error(f"No threads attached to user object: {self.user_id}")

            pipe.execute()

    # ? UNFINISHED
    def commit(self):
        # TODO: If fails check for user:sid:<sid> but accepts user:<user_id> update user:sid:<sid>
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

        #! VV Not true VV. Must catch exception
        # Everything commited, so session is no longer dirty
        self.dirty = False

    def extend_data(self):
        with self._R.pipeline() as pipe:
            pipe.expire(f"user:{self.user_id}", self.DEFAULT_USER_EXPIRE)
            pipe.expire(f"user:{self.user_id}:threads", self.DEFAULT_USER_EXPIRE)
            pipe.execute()

