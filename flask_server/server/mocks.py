from redis import Redis, DataError

from server.logging import make_logger
from server.redis_cache.user_cache import UserEntry
from server.redis_cache.message_cache import ThreadEntry, MessageEntry
from server.utils.data_generators import FlexDict
from server.db.models import InventoryObject
from app import db

logger = make_logger(__name__)

mock_threads = {0: ThreadEntry("0", "mockthread2")}


mock_users = {
    0: {"id": 0, "username": "testuser0", "threads": []},
    1: {"id": 1, "username": "testuser1", "threads": [0]},
    2: {"id": 2, "username": "testuser2", "threads": [0, 1]},
    3: {"id": 3, "username": "testuser3", "threads": [1]},
    4: {"id": 4, "username": "testuser4", "threads": [2]},
    5: {"id": 5, "username": "testuser5", "threads": [2]},
}

mock_threads = {
    0: {
        "id": 0,
        "name": "mockthread1",
        "members": [1, 2, 0],
        "messages": [1, 2, 3, 4, 12],
    },
    1: {"id": 1, "name": "mockthread2", "members": [2, 3], "messages": [5, 6, 7]},
    2: {"id": 2, "name": "mockthread3", "members": [4, 5], "messages": [8, 9, 10, 11]},
}

mock_messages = {
    1: {"id": 1, "sender": 1, "content": "Hey Babe", "thread": 0},
    2: {"id": 2, "sender": 2, "content": "How Ya Doin", "thread": 0},
    3: {"id": 3, "sender": 1, "content": "Good, You?", "thread": 0},
    4: {"id": 4, "sender": 2, "content": "test4", "thread": 0},
    5: {"id": 5, "sender": 3, "content": "test5", "thread": 1},
    6: {"id": 6, "sender": 2, "content": "test6", "thread": 1},
    7: {"id": 7, "sender": 3, "content": "test7", "thread": 1},
    8: {"id": 8, "sender": 4, "content": "test8", "thread": 2},
    9: {"id": 9, "sender": 5, "content": "test9", "thread": 2},
    10: {"id": 10, "sender": 5, "content": "test10", "thread": 2},
    11: {"id": 11, "sender": 4, "content": "test11", "thread": 2},
    12: {"id": 12, "sender": 1, "content": "test12", "thread": 0},
}

mock_inventory = {
    0: {"id": 0, "name": "Test Item 0", "quantity": 1},
    1: {"id": 1, "name": "Test Item 1", "quantity": 1},
    2: {"id": 2, "name": "Test Item 2", "quantity": 1},
    3: {"id": 3, "name": "Test Item 3", "quantity": 1},
    4: {"id": 4, "name": "Test Item 4", "quantity": 1},
    5: {"id": 5, "name": "Test Item 5", "quantity": 3},
    6: {"id": 6, "name": "Test Item 6", "quantity": 56},
    7: {"id": 7, "name": "Test Item 7", "quantity": 128},
}


DEFAULT_USER_EXPIRE = 60 * 60 * 2

NO_SID = "NO_SID"


def mock_inventory_setup():
    for item_id, item_dict in mock_inventory.items():
        item = InventoryObject(id=item_id, name=item_dict["name"])
        db.session.add(item)
    db.session.commit()


def set_user_online(user, user_sid=NO_SID, exp=DEFAULT_USER_EXPIRE):
    r = Redis()
    pipe = r.pipeline()

    logger.info(f"Setting user online: {user}")
    pipe.sadd("user:online", user.id)
    pipe.hmset(
        f"user:{user.id}",
        {"username": user.username, "online": 1, "id": user.id, "sid": user_sid},
    )
    pipe.set(f"user:sid:{user_sid}", user.id)
    pipe.expire(f"user:{user.id}", exp)
    try:
        for thread_id in user.threads:
            pipe.sadd(f"user:{user.id}:threads", thread_id)
        pipe.expire(f"user:{user.id}:threads", exp)
    except AttributeError:
        logger.error(f"No threads attached to user object: {user}")

    pipe.execute()
    logger.info(pipe.hgetall(f"user:{user.id}").execute())
    logger.info(f"user:{user.id}")


def thread_length(thread_id):
    r = Redis()
    try:
        return int(r.zcard(f"thread:{thread_id}:messages"))
    except TypeError:
        return 0


def set_user_offline(user_sid):
    pipe = Redis().pipeline()
    pipe.get(f"user:sid:{user_sid}")
    user_id = int(pipe.execute()[0])
    if user_id is None:
        logger.warning(f"Data missing from user:sid")
        raise DataError(f"User with sid {user_sid} was not in user:sid")
    elif not isinstance(user_id, int):
        logger.critical(
            f"Pipe returning incorrect type for user_id  (Function: set_user_offline returned {type(user_id)})"
        )
        raise DataError(
            f"Pipe returning incorrect type for user_id  (Function: set_user_offline returned {type(user_id)})"
        )
    else:
        pipe.delete(f"user:sid:{user_sid}")
        pipe.srem("user:online", user_id)
        pipe.hset(f"user:{user_id}", "online", 0)
        pipe.hset(f"user:{user_id}", "sid", NO_SID)
        pipe.execute()
        return user_id


def create_thread(thread_dict):
    r = Redis()
    pipe = r.pipeline()

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


def create_message(message_dict):
    r = Redis()
    pipe = r.pipeline()
    message_id = message_dict["id"]

    thread_len = thread_length(message_dict["thread"])
    logger.info(f'Thread Length for {message_dict["id"]} is: {thread_len}')
    pipe.hmset(f"message:{message_id}", message_dict)
    pipe.zadd(
        f"thread:{message_dict['thread']}:messages", {str(thread_len): message_id}
    )
    pipe.execute()


def mock_user_setup():
    logger.info("Adding Mock Users")
    for user in mock_users.values():
        set_user_online(FlexDict.from_dict(user))
    logger.info("Finished Adding Mock Users")


def mock_threads_setup():
    logger.info("Adding Mock Threads")
    for thread in mock_threads.values():
        create_thread(FlexDict.from_dict(thread))
    logger.info("Finished Adding Mock Threads")


def mock_message_setup():
    logger.info("Adding Mock Messages")
    for message in mock_messages.values():
        create_message(FlexDict.from_dict(message))
    logger.info("Finished Adding Mock Messages")


def setup_mocks():
    r = Redis()
    r.flushall()
    r.set("message:next-id", 13)
    r.set("thread:next-id", 3)
    mock_user_setup()
    mock_inventory_setup()
    mock_threads_setup()
    mock_message_setup()

