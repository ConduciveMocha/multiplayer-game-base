import logging
import time
from redis.exceptions import WatchError

from server.redis_cache.poolmanager import global_pipe, global_poolman

# ? Should this run indefinitely if the watch keeps getting interupted?
@global_pipe
def get_thread_id(pipe, thread_hash):
    while True:
        try:
            # Get current newestid
            pipe.watch("thread:newestid")
            current = pipe.get("thread:newestid")
            next_id = int(current) + 1

            # Increment newestid in redis
            pipe.multi()
            pipe.incr("thread:newestid")
            pipe.execute()

            return next_id
        except WatchError:
            continue


@global_pipe
def new_thread(pipe, thread_hash, thread):
    pipe.multi()
    pipe.key(f"thread:hash:{thread_hash}", thread.id)
    pipe.hmset(f"thread:{thread.id}", thread)
    pipe.zadd(f"thread:{thread.id}:messages", time.time(), "THREAD_START")
    pipe.execute()
    for m_id in thread["members"]:
        pipe.ladd(f"user:{m_id}:threads", thread.thread_hash)
    if thread.messages:
        # ? Lock this so user cant try to acquire messages while adding messages?
        pipe.multi()
        for mess_id, mess_created in map(lambda x: (x.created, x.id), thread.messages):
            pipe.zadd(f"thread:{thread.id}:messages", mess_created, mess_id)
        pipe.execute()


@global_poolman
def check_for_thread(r, thread_hash):
    return r.exists(f"thread:hash:{thread_hash}")

