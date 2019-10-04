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

NO_SID = "NO_SID"

USER_SIG = {"id": int, "username": str, "online": int, "sid": str}


class UserEntry(RedisEntry):
    USER_SIG = {"id": int, "username": str, "online": int, "sid": str}
    NO_SID = "NO_SID"
    DEFAULT_USER_EXPIRE = 60 * 60 * 2

    def __init__(self, user_id, username, online, sid=None):
        self.user_id = user_id
        self.username = username
        self.online = online
        self.threads = []
        self.sid = sid

        super().__init__(self)

    @classmethod
    def from_user_id(cls, user_id):
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
                return cls(user_id, username, online, sid)

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
        with self._R.pipeline as pipe:

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
            logger.info(pipe.hgetall(f"user:{user.id}").execute())
            logger.info(f"user:{user.id}")

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


# Added
@global_poolman
def get_online_users(r):
    try:
        user_list = {
            int(user_id.decode("utf-8")): map_dict_signature(
                r.hgetall(f"user:{user_id.decode('utf-8')}"), USER_SIG
            )
            for user_id in r.sscan_iter("user:online")
        }
        return user_list
    except Exception as e:
        logger.error(e)
        raise type(e)


# Added
@return_signature0(USER_SIG)
@global_poolman
def get_user_by_id(r, user_id):
    try:
        user_id = int(user_id)
        if r.exists(f"user:{user_id}"):
            return r.hgetall(f"user:{user_id}")
        else:
            logger.error(f"User {user_id} does not exist")
            return {}
    except Exception as e:
        logger.error("Error thrown in `get_user_by_id`")
        logger.error(e)
        raise type(e)


# Added
@global_poolman
def user_is_online(r, user_id):
    return r.sismember("user:online", user_id)


# Added
@global_pipe
def set_user_online(pipe, user, user_sid=NO_SID, exp=DEFAULT_USER_EXPIRE):
    logger.info(f"Setting user online: {user}")
    pipe.sadd("user:online", user.id)
    pipe.hmset(
        f"user:{user.id}",
        {"username": user.username, "online": 1, "id": user.id, "sid": user_sid},
    )
    pipe.set(f"user:sid:{user_sid}", user.id)
    pipe.expire(f"user:{user.id}", exp)
    try:
        for thread_id in user.threads:
            pipe.sadd(f"user:{user.id}:threads", thread_id)
        pipe.expire(f"user:{user.id}:threads", exp)
    except AttributeError:
        logger.error(f"No threads attached to user object: {user}")

    pipe.execute()
    logger.info(pipe.hgetall(f"user:{user.id}").execute())
    logger.info(f"user:{user.id}")


# Added
@global_pipe
def extend_user_data(pipe, user_id, exp=DEFAULT_USER_EXPIRE):
    pipe.expire(f"user:{user_id}", exp)
    pipe.expire(f"user:{user_id}:threads", exp)
    pipe.execute()


# Implicit
@global_poolman
def get_user_threads(r, user_id):
    threads = r.smembers(f"user:{user_id}:threads")
    if threads:
        return list(map(lambda th: int(th.decode("utf-8")), threads))
    else:
        return []


# Added
@global_pipe
def set_user_offline(pipe, user_sid):
    pipe.get(f"user:sid:{user_sid}")
    user_id = int(pipe.execute()[0])
    if user_id is None:
        logger.warning(f"Data missing from user:sid")
        raise DataError(f"User with sid {user_sid} was not in user:sid")
    elif not isinstance(user_id, int):
        logger.critical(
            f"Pipe returning incorrect type for user_id  (Function: set_user_offline returned {type(user_id)})"
        )
        raise DataError(
            f"Pipe returning incorrect type for user_id  (Function: set_user_offline returned {type(user_id)})"
        )
    else:
        pipe.delete(f"user:sid:{user_sid}")
        pipe.srem("user:online", user_id)
        pipe.hset(f"user:{user_id}", "online", 0)
        pipe.hset(f"user:{user_id}", "sid", NO_SID)
        pipe.execute()
        return user_id


# added
@global_poolman
def user_from_sid(r, user_sid):
    return int(r.get(f"user:sid:{user_sid}"))


# Addded
@global_poolman
def set_user_sid(r, user_id, user_sid):
    if r.exists(f"user:sid:{user_sid}") or r.hget(f"user:{user_id}", "sid"):
        logger.debug(r.hget(f"user:{user_id}", "sid").decode("utf-8") == NO_SID)
        logger.debug(NO_SID)
        if r.hget(f"user:{user_id}", "sid").decode("utf-8") != NO_SID:
            raise DataError("User SID already set")

    r.set(f"user:sid:{user_sid}", user_id)
    r.hset(f"user:{user_id}", "sid", user_sid)
    logger.info(f"user:{user_id} sid set to {user_sid}")

