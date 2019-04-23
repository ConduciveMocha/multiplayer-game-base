import logging
from server.redis_cache.poolmanager import global_pipe, global_poolman


@global_pipe
def new_thread(p, thread_hash, thread):
    pipe.hmset(f"thread:{thread_hash}", thread)
    pipe.ladd(f"thread:{thread_hash}:messages", "THREAD_START")
    for m_id in thread["members"]:
        pipe.ladd(f"user:{m_id}:threads", thread_hash)

