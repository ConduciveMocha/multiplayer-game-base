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

logger = make_logger(__name__)


class ThreadEntry(RedisEntry):
    THREAD_SIG = {"id": int, "name": str}
    THREAD_START = "-1"

    def __init__(
        self,
        thread_id: int,
        thread_name: str = None,
        users: list = None,
        messages: list = None,
    ):
        self._messages = messages
        self.thread_id = thread_id
        self._users = users
        self.room_name = f"thread-{thread_id}"
        super().__init__(thread_id)

    def add_loaded_object(self, obj_id, obj):

        self.__class__._loaded_objects[obj_id] = obj

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
        member_ids = self._R.smembers(f"thread:{self.thread_id}:members")
        self._users = [
            UserEntry.from_user_id(int(member_id)) for member_id in member_ids
        ]
        return self._users

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
        if cls._object_is_saved(thread_id):
            return cls._get_saved_object(thread_id)

        try:
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
        try:

            return {
                "id": self.thread_id,
                "users": [member.user_id for member in self.users],
                "messages": [message.message_id for message in self.messages],
            }
        except Exception as e:
            logger.debug(f"Thrown in thread.to_dict: ({type(e)}) {e}")


class MessageEntry(RedisEntry):
    MESSAGE_SIG = {"thread": int, "sender": int, "content": str, "id": int}

    def __init__(self, message_id: int, thread_id: int, sender_id: int, content: str):
        self.message_id = message_id
        self.thread_id = thread_id
        self._thread = None
        self.sender_id = sender_id
        self._sender = None
        self.content = content
        super().__init__(message_id)

    @property
    def thread(self):
        if self._thread is None:
            self._thread = ThreadEntry.from_id(self.thread_id)
        return self._thread

    @thread.setter
    def thread(self, thread):
        self._thread = thread
        self.commit()

    @property
    def sender(self):
        if self._sender is None:
            logger.debug(f"self.sender_id: {self.sender_id}")
            self._sender = UserEntry.from_user_id(self.sender_id)
        return self._sender

    @sender.setter
    def sender(self, sender):
        self._sender = sender
        self.commit()

    @classmethod
    def from_id(cls, message_id: int, thread=None):
        if cls._object_is_saved(message_id):
            return cls._get_saved_object(message_id)
        try:
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
        if incr:
            cls._R.incr("message:next-id")
        return message_id

    def commit(self):
        # Add Message

        with self._R.pipeline() as pipe:
            pipe.hmset(
                f"message:{self.message_id}",
                {
                    "content": self.content,
                    "sender": self.sender.user_id,
                    "thread": self.thread_id,
                    "id": self.message_id,
                },
            )
            pipe.zadd(
                f"thread:{self.thread_id}:messages",
                {str(len(self.thread)): self.message_id},
            )
            pipe.execute()

    def to_dict(self):
        return {
            "content": self.content,
            "sender": self.sender.user_id,
            "thread": self.thread_id,
            "id": self.message_id,
        }

