import logging

from flask import g, jsonify
from redis.exceptions import DataError

from server.redis_cache.poolmanager import global_poolman, global_pipe
from server.logging import make_logger

uc_logger = make_logger(__name__)

DEFAULT_USER_EXPIRE = 60 * 60 * 2


@global_poolman
def get_online_users(r):
    try:
        user_list = {
            user_id: r.hget(f"user:{user_id}", "username")
            for user_id in r.sscan_iter("user:online")
        }
        return user_list
    except Exception as e:
        uc_logger.error(e)
        raise type(e)


@global_poolman
def user_from_cache(r, user_id):
    try:
        
        if r.exists(f"user:{user_id}"):
            return r.hget(f"user:{user_id}", "username")
        else:
            return None
    except Exception as e:
        uc_logger.error(e)
        raise type(e)


@global_poolman
def user_online(r, user_id):
    return r.sismember("user:online", user_id)


@global_pipe
def set_user_online(pipe, user, user_sid):
    pipe.sadd("user:online", user.id)
    pipe.hmset(f"user:{user.id}", {"username": user.username, "online": 1})
    pipe.set(f"user:sid:{user_sid}", user.id)
    pipe.expire(f"user:{user.id}", DEFAULT_USER_EXPIRE)
    for thread in user.message_threads:
        pipe.zadd(f"user:{user.id}:threads", thread.created, thread.id)
    pipe.expire(f"user:{user.id}:threads", DEFAULT_USER_EXPIRE)
    pipe.execute()


@global_pipe
def extend_user_data(pipe, user_id, exp=DEFAULT_USER_EXPIRE):
    pipe.expire(f"user:{user_id}", exp)
    pipe.expire(f"user:{user_id}:threads", exp)
    pipe.execute()


@global_pipe
def set_user_offline(pipe, user_sid):
    user_id = pipe.get(f"user:sid:{user_sid}")
    pipe.execute()
    if user_id is None:
        uc_logger.warn(f"Data missing from user:sid")
        raise DataError(f"User with sid {user_sid} was not in user:sid")
    pipe.delete(f"user:sid:{user_sid}")
    pipe.srem("user:online", user_id)
    pipe.hset(f"user:{user_id}", "online", 0)
    pipe.execute()
    return user_id


@global_poolman
def user_from_sid(pipe, user_sid):
    return pipe.get(f"user:sid:{user_sid}")

