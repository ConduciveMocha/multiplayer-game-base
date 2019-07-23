import logging

from server.redis_cache.poolmanager import global_poolman, global_pipe
import redis
from redis.exceptions import LockError
from server.logging import make_logger
DEFAULT_MESSAGE_EXPIRE = 7200

"""
Messaging Structures:
thread:next-id -- (int) Next id to be created
thread:<id:int> -- (hash) meta data of thread
thread:<id:int>:members -- (set) list of ids of members in the thread
thread:<id:int>:messages -- (list) list of ids of messages sent in the thread
message:next-id -- (int) Next id to be created
message:<id:int> -- (hash) message data


"""
THREAD_START = "START"

logger = make_logger(__name__)

@global_pipe
def create_message(pipe,message_dict):
    message_id = message_dict['id']
    pipe.hmset(f'message:{message_id}',message_dict)
    pipe.lpush(f"thread:{message_dict['thread']}:messages", message_id)
    pipe.execute()


@global_poolman
def get_next_id(r):
    message_id = int(r.get('message:next-id'))
    r.incr('message:next-id')
    return message_id

@global_poolman
def get_message_by_id(r,message_id):
    try:
        return r.hgetall(f"message:{message_id}")
    except Exception as e:
        logger.error(e)
        raise type(e)


# Ugly. Ugly, ugly, ugly.
# Function only works if no race condition created when 
# creating threads with the same members...
@global_poolman
def check_if_thread_exists(r,members):
    mutual_threads = r.sinter(map(lambda mem: f"user:{mem}:threads", members))
    for th in mutual_threads:
        if len(members) == r.llen(f"thread:{th}:members"):
            return th
    return None

@global_pipe
def create_thread(pipe,thread_dict,members,messages=[]):
    thread_id = pipe.get('thread:next-id')
    
    existing_thread = check_if_thread_exists(members)
    if existing_thread:
        return existing_thread


    pipe.incr('thread:next-id')
    pipe.hmset(f'thread:{thread_id}',thread_dict)
    # add members to set
    for member in members:
        pipe.sadd(f'thread:{thread_id}:members', member)
        pipe.sadd(f'user:{member}:threads', thread_id)

    # Push messages into list
    for message in messages:
        pipe.lpush(f'thread:{thread_id}:messages', message)

    pipe.lpush(f'thread:{thread_id}:messages', THREAD_START)
    pipe.execute()
    return thread_id

def create_message_dict(content,sender,thread):
    return {'content':content,'sender':sender, 'thread':thread,'id':get_next_id()}
