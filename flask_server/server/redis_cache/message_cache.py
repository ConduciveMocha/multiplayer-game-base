from server.redis_cache.poolmanager import global_poolman, global_pipe, return_signature
import redis
from redis.exceptions import LockError
from server.logging import make_logger

DEFAULT_MESSAGE_EXPIRE = 7200

"""
Messaging Structures:
thread:next-id -- (int) Next id to be created
thread:<id:int> -- (hash) meta data of thread
thread:<id:int>:members -- (set) list of ids of members in the thread
thread:<id:int>:messages -- (zet) list of ids of messages sent in the thread
message:next-id -- (int) Next id to be created
message:<id:int> -- (hash) message data


"""

# CONSTANTS

# TODO: See if this can be changed to something userful
THREAD_START = "-1"
THREAD_SIG = {"id": int, "name": str}
MESSAGE_SIG = {"thread": int, "sender": int, "content": str, "id": int}

logger = make_logger(__name__)


class ThreadEntry:
    def __init__(self, thread_id, users, messages=[]):
        self.r = redis.Redis()
        self.has_been_read = False

    def get_thread_length(self):
        if len(self.messages):
            return len(self.messages)
        else:
            raise redis.DataError

    def __len__(self):
        return self.get_thread_length()

    def create_default_thread_name(self):
        pass


class MessageEntry:
    def __init__(self, message_id, thread_id, user_id, content):
        self.r = redis.Redis()


#! TODO: Added method that joins user names
@global_poolman
def create_default_thread_name(r, users):
    usernames = [r.hget(f"user:{user}", "username") for user in users]
    return ", ".join(usernames[:-1]) + " and " + usernames[-1]


# Added
@global_poolman
def thread_length(r, thread_id):
    try:
        return int(r.zcard(f"thread:{thread_id}:messages"))
    except TypeError:
        return 0


# Adds message to redis
@global_pipe
def create_message(pipe, message_dict):
    message_id = message_dict["id"]

    thread_len = thread_length(message_dict["thread"])
    logger.info(f'Thread Length for {message_dict["id"]} is: {thread_len}')
    pipe.hmset(f"message:{message_id}", message_dict)
    pipe.zadd(
        f"thread:{message_dict['thread']}:messages", {str(thread_len): message_id}
    )
    pipe.execute()


# Gets next message-id and increments
@global_poolman
def get_next_message_id(r):
    message_id = int(r.get("message:next-id"))
    logger.info(f"Next available message id: {message_id}")
    r.incr("message:next-id")
    logger.info(f"message:next-id Incremented")
    return message_id


# Gets next thread-id and increments
@global_poolman
def get_next_thread_id(r):
    thread_id = int(r.get("thread:next-id"))
    logger.info(f"Next available thread id: {thread_id}")
    r.incr("thread:next-id")
    logger.info(f"thread:next-id Incremented")
    return thread_id


# Gets the contents of the message:<id> key
#! TODO: Add auxilary keys (i.e. message:<id>:users) to return dict
@return_signature(MESSAGE_SIG)
@global_poolman
def get_message_by_id(r, message_id):
    try:
        logger.info(f"Getting message:{message_id}")
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
        logger.info(f"thread: {th}")
        th = int(th.decode("utf-8"))
        if len(members) == r.scard(f"thread:{th}:members"):

            return th

    return None


@global_poolman
def check_if_user_in_thread(r, thread_id, user_id):
    is_member = r.sismember(f"thread:{thread_id}:members", user_id)
    logger.info(f"Result of sismember for user {user_id} in {thread_id}: {is_member}")
    return is_member


# Adds the thread to redis
@global_pipe
def create_thread(pipe, thread_dict):
    members = thread_dict["members"]
    thread_id = thread_dict["id"]

    logger.info(f"Making thread object: thread:{thread_id}")
    pipe.hmset(f"thread:{thread_id}", {"id": thread_id, "name": thread_dict["name"]})

    logger.info(f"Adding users to thread:{thread_id}:members")
    for user in members:
        pipe.sadd(f"thread:{thread_id}:members", user)
        pipe.sadd(f"user:{user}:threads", thread_id)

    logger.info(f"Creating thread:{thread_id}:messages")
    pipe.zadd(f"thread:{thread_id}:messages", {0: -1})

    logger.info("Executing pipe in `create_thread`")
    pipe.execute()
    return thread_dict


@global_poolman
def get_thread_message_ids(r, thread_id):
    logger.info(f"Message ids for {thread_id}")
    logger.info(r.zscan(f"thread:{thread_id}:messages"))
    id_list = map(lambda zmem: int(zmem[1]), r.zscan(f"thread:{thread_id}:messages")[1])
    return list(filter(lambda x: x != -1, id_list))


# Allows the thread object to get signature mapped
@return_signature(THREAD_SIG)
@global_poolman
def _get_thread_by_id(r, thread_id):
    try:
        logger.info(f"Getting thread:{thread_id}")
        thread = r.hgetall(f"thread:{thread_id}")
        logger.info(f"thread:{thread_id} = {thread}")
        return thread
    except Exception as e:
        logger.error("Error thrown in _get_thread_by_id")
        return {}


def get_thread_by_id(thread_id):
    thread = _get_thread_by_id(thread_id)
    if thread:
        thread["messages"] = get_thread_message_ids(thread_id)
        return thread
    else:
        return None


@global_poolman
def get_thread_messages(r, thread_id):
    message_ids = r.zscan(f"thread:{thread_id}:messages")[1]
    logger.info(f"Message Ids: {message_ids}")
    thread_messages = {
        int(m_id[1]): get_message_by_id(int(m_id[1]))
        for m_id in message_ids
        if m_id[1] != -1
    }

    logger.info(f"Thread messages: {thread_messages}")
    return thread_messages


def create_message_dict(content, sender, thread, id=None):
    return {
        "content": str(content),
        "sender": int(sender),
        "thread": int(thread),
        "id": int(id) if id else get_next_message_id(),
    }


# TODO Rename members
def create_thread_dict(sender, members, name, id=None):
    full_members_list = list(set([sender, *members]))
    return {
        "members": full_members_list,
        "name": str(name) if name else create_default_thread_name(full_members_list),
        "id": int(id) if id else get_next_thread_id(),
        "messages": [],
    }

