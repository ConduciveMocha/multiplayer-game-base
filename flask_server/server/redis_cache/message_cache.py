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


@global_poolman
def create_default_thread_name(r, users):
    return "TEST"


@global_pipe
def create_message(pipe, message_dict):
    message_id = message_dict["id"]
    pipe.hmset(f"message:{message_id}", message_dict)
    pipe.lpush(f"thread:{message_dict['thread']}:messages", message_id)
    pipe.execute()


@global_poolman
def get_next_message_id(r):
    message_id = int(r.get("message:next-id"))
    logger.debug(f"Next available message id: {message_id}")
    r.incr("message:next-id")
    logger.debug(f"message:next-id Incremented")
    return message_id


@global_poolman
def get_next_thread_id(r):
    thread_id = int(r.get("thread:next-id"))
    logger.debug(f"Next available thread id: {thread_id}")
    r.incr("thread:next-id")
    logger.debug(f"thread:next-id Incremented")
    return thread_id


@global_poolman
def get_message_by_id(r, message_id):
    try:
        logger.debug(f"Getting message:{message_id}")
        return r.hgetall(f"message:{message_id}")
    except Exception as e:
        logger.error(e)
        raise type(e)


# Ugly. Ugly, ugly, ugly.
#! Function only works if no race condition created when creating threads with the same members...
@global_poolman
def check_if_thread_exists(r, members):
    mutual_threads = r.sinter(map(lambda mem: f"user:{mem}:threads", members))
    for th in mutual_threads:
        if len(members) == r.llen(f"thread:{th}:members"):
            return th
    return None


@global_pipe
def create_thread(pipe, thread_dict):
    users = thread_dict["users"]
    thread_id = thread_dict["id"]

    logger.info(f"Making thread object: thread:{thread_id}")
    pipe.hmset(f"thread:{thread_id}", {"id": thread_id, "name": thread_dict["name"]})

    logger.info(f"Adding users to thread:{thread_id}:members")
    pipe.sadd(f"thread:{thread_id}:members", *users)

    logger.info("Updating users' thread list")
    # Add thread to members' thread list
    for user in users:
        pipe.sadd(f"user:{user}:threads", thread_id)

    logger.info(f"Creating thread:{thread_id}:messages")
    pipe.lpush(f"thread:{thread_id}:messages", THREAD_START)

    # Push message into list
    if thread_dict["content"]:
        logger.info(f"Adding first message")
        pipe.lpush(f"thread:{thread_id}:messages", thread_dict["content"])

    logger.info("Executing pipe")
    pipe.execute()
    logger.info("Pipe executed. Returning")


def create_message_dict(content, sender, thread):
    return {
        "content": content,
        "sender": sender,
        "thread": thread,
        "id": get_next_message_id(),
    }


def create_thread_dict(content, sender, users, name):
    full_users = [sender, *users]
    existing_thread = check_if_thread_exists(full_users)
    if existing_thread:
        return existing_thread, True
    else:
        return (
            {
                "content": content,
                "users": full_users,
                "name": name if name else create_default_thread_name(full_users),
                "id": get_next_thread_id(),
            },
            False,
        )

