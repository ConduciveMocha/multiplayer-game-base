import logging

from server.redis_cache.poolmanager import global_poolman, global_pipe
import redis
from redis.exceptions import LockError

DEFAULT_MESSAGE_EXPIRE = 900


@global_pipe
def new_message(pipe, message):
    try:

        with pipe.lock("message:last_id", timeout=2):
            last_id = pipe.get("message:last_id")
            pipe.execute()

        last_id += 1

        pipe.hmset(f"message:{last_id}", message)
        pipe.expire(f"messasge:{last_id}", DEFAULT_MESSAGE_EXPIRE)
        pipe.ladd(f"thread:{message.thread_id}:messages", last_id)
        pipe.incr("message:last_id")
        pipe.execute()

    except LockError:
        logging.error("lock:message:last_id wasnt acquired")


@global_poolman
def get_messages(r, message_ids):
    return [(m, r.hgetall(f"message:{m}")) for m in message_ids]


@global_poolman
def message_by_id(pipe, message_id):
    return pipe.hgetall(f"message:{message_id}")

