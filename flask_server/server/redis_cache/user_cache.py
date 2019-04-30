import logging

from flask import g, jsonify
from redis.exceptions import DataError

import server.redis_cache.namespace as ns

from server.redis_cache.poolmanager import global_poolman, global_pipe
from server.logging import make_logger
from server.utils.redisutils import decode_dict


logger = make_logger(__name__)

DEFAULT_USER_EXPIRE = 60 * 60 * 2


@global_poolman
def echo(r):
    x = r.echo("Test")
    logger.debug(f"{x}")
    return x


@global_poolman
def get_online_users(r):
    try:
        user_dict = {}
        for user_id in r.sscan_iter(ns.user_online):

            user_id = int(user_id.decode("utf-8"))
            user_dict[user_id] = decode_dict(r.hgetall(ns.user(user_id)))
        return user_dict
    except Exception as e:
        logger.exception(e)
        raise Exception


@global_poolman
def get_user(r, user_id):
    try:
        exists = r.exists(ns.user(user_id))
        if exists:
            return decode_dict(r.hgetall(ns.user(user_id)))
        else:
            return None
    except Exception as e:
        logger.error(e)
        raise type(e)


@global_poolman
def user_online(r, user_id):
    return r.sismember(ns.user_online, user_id)


@global_pipe
def set_user_online(pipe, user, user_sid):
    pipe.sadd(ns.user_online, user.id)
    pipe.hmset(
        ns.user(user.id),
        {
            "user_id": user.id,
            "username": user.username,
            "online": True,
            "user_sid": user_sid,
        },
    )
    pipe.set(ns.user_sid(user_sid), user.id)
    pipe.expire(ns.user(user.id), DEFAULT_USER_EXPIRE)
    for thread in user.message_threads:
        pipe.zadd(ns.user_threads(user.id), thread.created, thread.id)
    pipe.expire(ns.user_threads(user.id), DEFAULT_USER_EXPIRE)
    pipe.execute()


@global_pipe
def set_user_offline(pipe, user_sid):
    user_id = pipe.get(ns.user_sid(user_sid)).decode("utf-8")
    pipe.execute()
    if user_id is None:
        logger.warn(f"Data missing from user:sid")
        raise DataError(f"User with sid {user_sid} was not in user:sid")
    pipe.delete(ns.user_sid(user_sid))
    pipe.srem(ns.ns.user_online, user_id)
    pipe.hset(ns.user, "online", False)
    pipe.execute()
    return int(user_id.decode("utf-8"))


@global_pipe
def extend_user_data(pipe, user_id, exp=DEFAULT_USER_EXPIRE):
    pipe.expire(ns.user(user_id), exp)
    pipe.expire(ns.user_threads(user_id), exp)
    pipe.execute()


@global_poolman
def user_from_sid(r, user_sid):
    return r.get(ns.user_sid(user_sid)).decode("utf-8")


@global_poolman
def get_user_ttl(r, user_id):
    return int(r.ttl(ns.user(user_id)))

