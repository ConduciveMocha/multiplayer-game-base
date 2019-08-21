from redis import Redis

from server.logging import make_logger
from server.redis_cache.user_cache import set_user_online
from server.redis_cache.message_cache import (
    create_message,
    create_message_dict,
    create_thread,
    create_thread_dict,
)
from server.utils.data_generators import FlexDict

logger = make_logger(__name__)

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
        "members": [1, 2,0],
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
    mock_user_setup()
    mock_threads_setup()
    mock_message_setup()

