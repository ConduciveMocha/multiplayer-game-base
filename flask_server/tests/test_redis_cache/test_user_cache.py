import pytest
from redis import Redis
from server.logging import make_logger, log_test
from server.utils.data_generators import FlexDict
from server.redis_cache.poolmanager import map_dict_signature
from server.redis_cache.user_cache import (
    user_is_online,
    set_user_online,
    user_from_sid,
    get_online_users,
    extend_user_data,
    set_user_offline,
    set_user_sid,
    USER_SIG,
    NO_SID,
)

logger = make_logger(__name__)
TEST_USER_EXPIRE = 15


@pytest.fixture(scope="function")
def mock_user(r_inst):
    user = FlexDict()
    user.id = 5
    user.username = "test"
    user_sid = str(21341235)
    user.threads = [1, 2, 3, 4]

    set_user_online(user, user_sid)
    yield user, user_sid

    r_inst.delete(f"user:{user.id}")
    r_inst.delete(f"user:sid:{user_sid}")
    r_inst.delete(f"user:{user.id}:threads")
    r_inst.srem(f"user:online", user.id)


def test_get_online_users(r_inst, mock_user):
    user, user_sid = mock_user
    online_users = get_online_users()
    assert isinstance(online_users[user.id], dict)
    u = online_users[user.id]
    assert u["id"] == user.id
    assert u["username"] == user.username
    assert u["online"] == 1


def test_user_is_online(r_inst):
    in_set = [x ** 2 for x in range(10, 20)]
    out_set = [x + 102 for x in range(10)]
    for mem_id in in_set:
        r_inst.sadd("user:online", mem_id)

    for mem_id in in_set:
        assert user_is_online(mem_id) == True
    for mem_id in out_set:
        assert user_is_online(mem_id) == False
    for mem_id in in_set:
        r_inst.srem("user:online", mem_id)


def test_set_user_online(r_inst, mock_user):
    user, user_sid = mock_user

    set_user_online(user, user_sid, exp=TEST_USER_EXPIRE)
    assert r_inst.sismember("user:online", user.id)

    # Gets user:<id> from redis and then decodes it using the map_signature function
    user_entry = map_dict_signature(r_inst.hgetall(f"user:{user.id}"), USER_SIG)
    assert user_entry["username"] == user.username
    assert user_entry["online"] == 1
    assert user_entry["id"] == user.id
    assert user_entry["sid"] == user_sid
    assert int(r_inst.get(f"user:sid:{user_sid}")) == user.id
    assert r_inst.ttl(f"user:{user.id}") <= TEST_USER_EXPIRE
    assert r_inst.ttl(f"user:{user.id}:threads") <= TEST_USER_EXPIRE
    for th_id in user.threads:
        assert r_inst.sismember(f"user:{user.id}:threads", th_id) == True


def test_extend_user_data(r_inst):
    user = FlexDict()
    user.id = 5
    user.username = "test"
    user_sid = str(21341235)
    user.threads = [1, 2, 3, 4]

    set_user_online(user, user_sid, exp=TEST_USER_EXPIRE)

    extend_user_data(user.id, exp=2 * TEST_USER_EXPIRE)

    assert TEST_USER_EXPIRE < r_inst.ttl(f"user:{user.id}") <= 2 * TEST_USER_EXPIRE
    assert (
        TEST_USER_EXPIRE < r_inst.ttl(f"user:{user.id}:threads") <= 2 * TEST_USER_EXPIRE
    )


def test_set_user_offline(r_inst, mock_user):
    user, user_sid = mock_user

    set_user_online(user, user_sid, exp=TEST_USER_EXPIRE)

    returned_user_id = set_user_offline(user_sid)
    assert returned_user_id == user.id
    assert r_inst.sismember("user:online", user.id) == False
    assert r_inst.get(f"user:sid:{user_sid}") == None
    returned_user_object = map_dict_signature(
        r_inst.hgetall(f"user:{user.id}"), USER_SIG
    )
    assert returned_user_object["online"] == 0
    assert returned_user_object["username"] == user.username
    assert returned_user_object["id"] == user.id
    assert returned_user_object["sid"] == NO_SID


def test_user_from_sid(r_inst, mock_user):
    user, user_sid = mock_user
    assert user_from_sid(user_sid) == user.id


def test_add_user_sid(r_inst):
    user_sid = 123412345
    user_id = 1234
    set_user_sid(user_id, user_sid)
    assert user_from_sid(user_sid) == user_id
    assert int(r_inst.hget(f"user:{user_id}", "sid")) == user_sid
    r_inst.delete(f"user:sid:{user_sid}")
    r_inst.hdel(f"user:{user_id}", "sid")

