from server.redis_cache.poolmanager import global_poolman, global_pipe, return_signature
import redis
from redis.exceptions import LockError
from server.logging import make_logger
from server.redis_cache.redis_model import RedisEntry
from server.redis_cache.user_cache import UserEntry

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

# TODO: See if this can be changed to something useful
THREAD_START = "-1"
THREAD_SIG = {"id": int, "name": str}
MESSAGE_SIG = {"thread": int, "sender": int, "content": str, "id": int}

logger = make_logger(__name__)


class ThreadEntry(RedisEntry):
    THREAD_SIG = {"id": int, "name": str}

    def __init__(self, thread_id, thread_name=None, users=None, messages=None):
        self._messages = messages
        self.thread_id = thread_id
        self._users = users
        self.room_name = f"thread-{thread_id}"
        super().__init__(self)

    # This class variable needs a setter to prevent recursively calling itself
    # when getting messages (which themselves will try to get this thread by id).
    @property
    def messages(self):
        if self._messages is None:

            self._messages = self._read_messages_from_cache()

        return self._messages

    @messages.setter
    def messages(self, messages):
        self._messages = messages
        self.commit()

    @property
    def users(self):
        if self._users is None:
            self._users = self._read_users_from_cache()
        return self._users

    @users.setter
    def users(self, users):
        self._users = users
        self.dirty = True

    def _read_users_from_cache(self):
        member_ids = self._R.smembers(f"thread:{thread_id}:members")
        self._users = [
            UserEntry.from_user_id(int(member_id)) for member_id in member_ids
        ]

    def _read_messages_from_cache(self):
        id_list = map(
            lambda zmem: int(zmem[1]),
            self._R.zscan(f"thread:{self.thread_id}:messages")[1],
        )
        id_list = filter(lambda x: x != -1, id_list)

        self._messages = [
            MessageEntry.from_id(message_id, thread=self) for message_id in id_list
        ]
        return self._messages

    @classmethod
    def from_id(cls, thread_id):
        try:
            logger.info(f"Getting thread:{thread_id}")
            raw_thread_data = cls._R.hgetall(f"thread:{thread_id}")
            thread_data = cls.fix_thread_signature(raw_thread_data)
            
            thread_obj = cls(thread_data["id"])

            return thread_obj

        except Exception as e:
            logger.error(f"Error thrown in ThreadEntry.from_id: {e}")
            return None

    @classmethod
    def fix_thread_signature(cls, returned_thread):
        return cls.fix_hash_signature(returned_thread, cls.THREAD_SIG)

    def get_thread_length(self):
        if len(self.messages):
            return len(self.messages)
        else:
            raise redis.DataError

    def __len__(self):
        return self.get_thread_length()

    def create_default_thread_name(self):
        usernames = [user.username for user in self.users]
        return ", ".join(usernames[:-1]) + " and " + usernames[-1]

    def is_user_in_thread(self, user):
        if isinstance(user, str) or isinstance(user, int):
            user = UserEntry.from_user_id(user)
        for member in self.users:
            if member == user:
                return True
        return False

    @classmethod
    def check_if_thread_exists(cls, members):
        mutual_threads = cls._R.sinter(
            map(lambda mem: f"user:{mem.user_id}:threads", members)
        )
        for th in mutual_threads:
            logger.info(f"thread: {th}")
            th = int(th.decode("utf-8"))
            if len(members) == cls._R.scard(f"thread:{th}:members"):
                return cls.from_id(th)

        return None

    @classmethod
    def next_id(cls, incr=False):
        thread_id = int(cls._R.get("thread:next-id"))
        logger.info(f"Next available thread id: {thread_id}")
        if incr:
            cls._R.incr("thread:next-id")
        logger.info(f"thread:next-id Incremented")
        return thread_id

    def commit(self):
        with self._R.pipeline() as pipe:
            pipe.hmset(
                f"threaget_user_d:{self.thread_id}",
                {"id": self.thread_id, "name": self.thread_name},
            )
            for user in self.users:
                pipe.sadd(f"thread:{self.thread_id}:members", user.id)
                pipe.sadd(f"user:{user.id}.threads", self.thread_id)
            pipe.zadd(f"thread:{thread_id}:messages", {0: -1})
            pipe.execute()

    def to_dict(self):
        logger.info("In tget_user_o dict")
        try:
            logger.info(f"{self.messages}")
        except:
            pass
        return {
            "id": self.thread_id,
            "users": [member.user_id for member in self.users],
            "messages": [message.message_id for message in self.messages],
        }

get_user_
class MessageEntry(RedisEntrget_user_y):
    MESSAGE_SIG = {"thread":get_user_ int, "sender": int, "content": str, "id": int}

    def __init__(self, message_id, thread, sender, content):
        self.message_id = message_id
        self.thread = thread
        self.sender = sender
        self.content = content
        super().__init__(self)

    @classmethod
    def from_id(cls, message_id, thread=None):
        try:
            logger.info(f"Getting message:{message_id}")
            raw_message_data = cls._R.hgetall(f"message:{message_id}")
            message_data = cls.fix_message_signature(raw_message_data)
            return cls(
                message_data["id"],
                ThreadEntry.from_id(message_data["thread"])
                if thread is None
                else thread,
                UserEntry.from_user_id(message_data["sender"]),
                message_data["content"],
            )
        except Exception as e:
            logger.error(e)
            raise type(e)

    @classmethod
    def fix_message_signature(cls, returned_message):
        return cls.fix_hash_signature(returned_message, cls.MESSAGE_SIG)

    @classmethod
    def next_id(cls, incr=False):
        message_id = int(cls._R.get("message:next-id"))
        logger.info(f"Next available message id: {message_id}")
        if incr:
            cls._R.incr("message:next-id")
        logger.info(f"message:next-id Incremented")
        return message_id

    def commit(self):
        # Add Message

        with self._R.pipeline() as pipe:
            pipe.hmset(
                f"message:{self.message_id}",
                {
                    "content": self.content,
                    "sender": self.sender.user_id,
                    "thread": self.thread.thread_id,
                    "id": self.message_id,
                },
            )
            pipe.zadd(
                f"thread:{self.thread.thread_id}:messages",
                {str(len(self.thread)): self.message_id},
            )
            pipe.execute()

    def to_dict(self):
        return {
            "content": self.content,
            "sender": self.sender.user_id,
            "thread": self.thread.thread_id,
            "id": self.message_id,
        }


# Added
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


# Added
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


# Added
# Gets next message-id and increments
@global_poolman
def get_next_message_id(r):
    message_id = int(r.get("message:next-id"))
    logger.info(f"Next available message id: {message_id}")
    r.incr("message:next-id")
    logger.info(f"message:next-id Incremented")
    return message_id


# Added
# Gets next thread-id and increments
@global_poolman
def get_next_thread_id(r):
    thread_id = int(r.get("thread:next-id"))
    logger.info(f"Next available thread id: {thread_id}")
    r.incr("thread:next-id")
    logger.info(f"thread:next-id Incremented")
    return thread_id


# Added
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


# Added
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


# Added
@global_poolman
def check_if_user_in_thread(r, thread_id, user_id):
    is_member = r.sismember(f"thread:{thread_id}:members", user_id)
    logger.info(f"Result of sismember for user {user_id} in {thread_id}: {is_member}")
    return is_member


# Added
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


# Added
@global_poolman
def get_thread_message_ids(r, thread_id):
    logger.info(f"Message ids for {thread_id}")
    logger.info(r.zscan(f"thread:{thread_id}:messages"))
    id_list = map(lambda zmem: int(zmem[1]), r.zscan(f"thread:{thread_id}:messages")[1])
    return list(filter(lambda x: x != -1, id_list))


# Added?
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


# Addeed?
def get_thread_by_id(thread_id):
    thread = _get_thread_by_id(thread_id)
    if thread:
        thread["messages"] = get_thread_message_ids(thread_id)
        return thread
    else:
        return None


# Implicit
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


# Unused
def create_message_dict(content, sender, thread, id=None):
    return {
        "content": str(content),
        "sender": int(sender),
        "thread": int(thread),
        "id": int(id) if id else get_next_message_id(),
    }


# TODO Rename members
# Unused
def create_thread_dict(sender, members, name, id=None):
    full_members_list = list(set([sender, *members]))
    return {
        "members": full_members_list,
        "name": str(name) if name else create_default_thread_name(full_members_list),
        "id": int(id) if id else get_next_thread_id(),
        "messages": [],
    }

