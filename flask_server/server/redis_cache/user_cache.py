import logging

from flask import g, jsonify
from redis.exceptions import DataError

from server.redis_cache.poolmanager import global_poolman, global_pipe,map_dict_signature
from server.logging import make_logger

uc_logger = make_logger(__name__)

DEFAULT_USER_EXPIRE = 60 * 60 * 2

user_sig = {'id':int,'username':str,'online':int,'sid':str}
@global_poolman
def get_online_users(r):
    try:
        user_list = {
            int(user_id.decode('ascii')): map_dict_signature(r.hgetall(f"user:{user_id.decode('ascii')}"), user_sig)
            for user_id in r.sscan_iter("user:online")
        }
        return user_list
    except Exception as e:
        uc_logger.error(e)
        raise type(e)


@global_poolman
def get_user_by_id(r, user_id):
    try:
        
        if r.exists(f"user:{user_id}"):
            return r.hget(f"user:{user_id}", "username")
        else:
            return None
    except Exception as e:
        uc_logger.error(e)
        raise type(e)


@global_poolman
def user_is_online(r, user_id):
    return r.sismember("user:online", user_id)


@global_pipe
def set_user_online(pipe, user, user_sid,exp=DEFAULT_USER_EXPIRE):
    pipe.sadd("user:online", user.id)
    pipe.hmset(f"user:{user.id}", {"username": user.username, "online": 1,"id":user.id, "sid":user_sid})
    pipe.set(f"user:sid:{user_sid}", user.id)
    pipe.expire(f"user:{user.id}", exp)
    for thread_id in user.message_threads:
        pipe.sadd(f"user:{user.id}:threads",  thread_id)
    pipe.expire(f"user:{user.id}:threads", exp)
    pipe.execute()


@global_pipe
def extend_user_data(pipe, user_id, exp=DEFAULT_USER_EXPIRE):
    pipe.expire(f"user:{user_id}", exp)
    pipe.expire(f"user:{user_id}:threads", exp)
    pipe.execute()


@global_pipe
def set_user_offline(pipe, user_sid):
    pipe.get(f"user:sid:{user_sid}")
    user_id = int(pipe.execute()[0])
    if user_id is None:
        uc_logger.warning(f"Data missing from user:sid")
        raise DataError(f"User with sid {user_sid} was not in user:sid")
    elif  not isinstance(user_id,int):
        uc_logger.critical(f'Pipe returning incorrect type for user_id  (Function: set_user_offline returned {type(user_id)})')
        raise DataError(f'Pipe returning incorrect type for user_id  (Function: set_user_offline returned {type(user_id)})')
    else:
        pipe.delete(f"user:sid:{user_sid}")
        pipe.srem("user:online", user_id)
        pipe.hset(f"user:{user_id}", "online", 0)
        pipe.hset(f'user:{user_id}', 'sid', 'NONE')
        pipe.execute()
        return user_id


@global_poolman
def user_from_sid(r, user_sid):
    return int(r.get(f"user:sid:{user_sid}"))

