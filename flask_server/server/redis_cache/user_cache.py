import logging

from flask import g, jsonify
from server.redis_cache.poolmanager import global_poolman, global_pipe

uc_logger = logging.getLogger(__name__)

DEFAULT_USER_EXPIRE = 60 * 60 * 2


@global_poolman
def get_online_users(r):
    try:
        user_list = {
            user_id: r.hget(f"user:{user_id}", "username")
            for user_id in r.sscan_iter("user:online")
        }
        return jsonify(**user_list)
    except Exception as e:
        uc_logger.error(e)
        return jsonify(error="Internal server error")


@global_poolman
def user_id_cached(r, user_id):
    try:
        exists = r.exists(f"user:{user_id}")
        if exists:
            return jsonify({user_id: r.hget(f"user:{user_id}", "username")})
        else:
            return None
    except Exception as e:
        uc_logger.error(e)
        return jsonify(error="Internal server errror")


@global_poolman
def user_online(r, user_id):
    return r.sismember("user:online", user_id)


@global_pipe
def set_user_online(pipe, user):
    pipe.sadd("user:online", user.id)
    pipe.hmset(f"user:{user.id}", {"username": user.username, "online": 1})
    pipe.expire(f"user:{user.id}", DEFAULT_USER_EXPIRE)
    for thread in user.message_threads:
        pipe.zadd(f"user:{user.id}:threads", thread.created, thread.id)
    pipe.expire(f"user:{user.id}:threads", DEFAULT_USER_EXPIRE)
    pipe.execute()


@global_pipe
def extend_user_data(pipe, user_id, exp=DEFAULT_USER_EXPIRE):
    pipe.expire(f"user:{user.id}", exp)
    pipe.expire(f"user:{user.id}:threads", exp)
    pipe.execute()


@global_pipe
def set_user_offline(pipe, user_id):
    pipe.srem("user:online", user_id)
    pipe.hset(f"user:{user_id}", "online", 0)
