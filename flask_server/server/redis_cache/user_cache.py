import logging

from flask import g, jsonify
from redis.exceptions import DataError

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


@return_signature(USER_SIG)
@global_poolman
def get_user_by_id(r, user_id):
    try:
        user_id = int(user_id)
        if r.exists(f"user:{user_id}"):
            return r.hgetall(f"user:{user_id}")
        else:
            logger.error(f'User {user_id} does not exist')
            return {}
    except Exception as e:
        logger.error("Error thrown in `get_user_by_id`")
        logger.error(e)
        raise type(e)


@global_poolman
def user_is_online(r, user_id):
    return r.sismember("user:online", user_id)


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
    for thread_id in user.threads:
        pipe.sadd(f"user:{user.id}:threads", thread_id)
    pipe.expire(f"user:{user.id}:threads", exp)
    pipe.execute()
    logger.info(pipe.hgetall(f"user:{user.id}").execute())
    logger.info(f"user:{user.id}")


@global_pipe
def extend_user_data(pipe, user_id, exp=DEFAULT_USER_EXPIRE):
    pipe.expire(f"user:{user_id}", exp)
    pipe.expire(f"user:{user_id}:threads", exp)
    pipe.execute()


@global_poolman
def get_user_threads(r, user_id):
    threads = r.smembers(f"user:{user_id}:threads")
    if threads:
        return list(map(lambda th: int(th.decode("utf-8")), threads))
    else:
        return []


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


@global_poolman
def user_from_sid(r, user_sid):
    return int(r.get(f"user:sid:{user_sid}"))


@global_poolman
def set_user_sid(r, user_id, user_sid):
    if r.exists(f"user:sid:{user_sid}") or r.hget(f"user:{user_id}", "sid"):
        logger.debug(r.hget(f"user:{user_id}", "sid").decode('utf-8') == NO_SID)
        logger.debug(NO_SID)
        if r.hget(f"user:{user_id}", "sid").decode('utf-8') != NO_SID: 
            raise DataError("User SID already set")
        
    r.set(f"user:sid:{user_sid}", user_id)
    r.hset(f"user:{user_id}", "sid", user_sid)
    logger.info(f'user:{user_id} sid set to {user_sid}')