import pytest
from redis import Redis
from server.logging import make_logger, log_test
from server.utils.data_generators import FlexDict
from server.redis_cache.poolmanager import map_dict_signature
from server.redis_cache.user_cache import user_is_online,set_user_online,user_from_sid,get_online_users,extend_user_data,set_user_offline
logger = make_logger(__name__)
TEST_USER_EXPIRE = 15

@pytest.fixture(scope='function')
def r_inst():
    logger.info('Creating redis instance')
    r = Redis()
    yield r
    logger.info('Returning from test.')

def test_get_online_users(r_inst):
    user = FlexDict()
    user.id = 5
    user.username = 'test'
    user_sid = str(21341235)
    user.message_threads = [1,2,3,4]

    dict_signature = {'username':str, 'online':int,'id':int,'sid':str}

    set_user_online(user,user_sid)
    online_users = get_online_users()
    assert isinstance(online_users[user.id], dict)
    u = online_users[user.id]
    assert u['id'] == user.id
    assert u['username'] == user.username
    assert u['online'] == 1

def test_user_is_online(r_inst):
    in_set = [x ** 2 for x in range(10,20)]
    out_set = [x+102 for x in range(10)]
    for mem_id in in_set:
        r_inst.sadd('user:online', mem_id)
    
    for mem_id in in_set:
        assert user_is_online(mem_id) == True
    for mem_id in out_set:
        assert user_is_online(mem_id) == False
    for mem_id in in_set:
        r_inst.srem('user:onlilne', mem_id)


def test_set_user_online(r_inst):
    user = FlexDict()
    user.id = 5
    user.username = 'test'
    user_sid = str(21341235)
    user.message_threads = [1,2,3,4]

    dict_signature = {'username':str, 'online':int,'id':int,'sid':str}

    set_user_online(user,user_sid,exp=TEST_USER_EXPIRE)
    assert r_inst.sismember("user:online",user.id)

    # Gets user:<id> from redis and then decodes it using the map_signature function
    user_entry = map_dict_signature(r_inst.hgetall(f"user:{user.id}"),dict_signature)
    assert user_entry['username'] == user.username
    assert user_entry['online'] == 1
    assert user_entry['id'] == user.id
    assert user_entry['sid'] == user_sid
    assert int(r_inst.get(f'user:sid:{user_sid}')) == user.id
    assert r_inst.ttl(f'user:{user.id}') <= TEST_USER_EXPIRE
    assert r_inst.ttl(f'user:{user.id}:threads') <= TEST_USER_EXPIRE
    for th_id in user.message_threads:
        assert r_inst.sismember(f"user:{user.id}:threads",th_id) == True

def test_extend_user_data(r_inst):
    user = FlexDict()
    user.id = 5
    user.username = 'test'
    user_sid = str(21341235)
    user.message_threads = [1,2,3,4]

    dict_signature = {'username':str, 'online':int,'id':int,'sid':str}
    set_user_online(user,user_sid,exp=TEST_USER_EXPIRE)
    
    extend_user_data(user.id, exp=2*TEST_USER_EXPIRE)

    assert TEST_USER_EXPIRE < r_inst.ttl(f'user:{user.id}') <= 2*TEST_USER_EXPIRE
    assert TEST_USER_EXPIRE < r_inst.ttl(f'user:{user.id}:threads') <= 2*TEST_USER_EXPIRE
    

def test_set_user_offline(r_inst):
    user = FlexDict()
    user.id = 5
    user.username = 'test'
    user_sid = str(21341235)
    user.message_threads = [1,2,3,4]

    dict_signature = {'username':str, 'online':int,'id':int,'sid':str}
    set_user_online(user,user_sid,exp=TEST_USER_EXPIRE)

    returned_user_id = set_user_offline(user_sid)
    assert returned_user_id == user.id
    assert r_inst.sismember('user:online', user.id) == False
    assert r_inst.get(f'user:sid:{user_sid}') == None
    returned_user_object = map_dict_signature(r_inst.hgetall(f'user:{user.id}'), dict_signature)
    assert returned_user_object['online'] == 0
    assert returned_user_object['username']== user.username
    assert returned_user_object['id'] == user.id
    assert returned_user_object['sid'] == 'NONE'


def test_user_from_sid(r_inst):
    user = FlexDict()
    user.id = 5
    user.username = 'test'
    user_sid = str(21341235)
    user.message_threads = [1,2,3,4]
    set_user_online(user,user_sid)

    assert user_from_sid(user_sid) == user.id