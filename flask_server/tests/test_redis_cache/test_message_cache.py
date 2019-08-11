import pytest
from redis import Redis
from server.logging import make_logger, log_test
from server.utils.data_generators import generate_random_message
from server.redis_cache.message_cache import create_default_thread_name,create_message_dict,create_thread_dict,get_next_thread_id,get_next_message_id
logger = make_logger(__name__)


@pytest.fixture(scope='module')
def r_inst():
    logger.info('Creating redis instance in r_inst pytest fixture')
    r = Redis()
    yield r
    logger.info('Returning from test to r_inst pytest fixture')

# @pytest.fixture(scope="function")
# def mock_messages():
#     m1 = create_message_dict("test1", 25,5,1000)
#     m2 = create_message_dict('test2',25,5,1001)

def test_get_next_thread_id(r_inst):
    logger.info('Running test')
    t_id = int(r_inst.get('thread:next-id'))
    assert t_id  == get_next_thread_id()
    assert int(r_inst.get('thread:next-id')) == t_id +1

def test_get_next_message_id(r_inst):
    logger.info('Running test')
    m_id = int(r_inst.get('message:next-id'))
    assert m_id  == get_next_message_id()
    assert int(r_inst.get('message:next-id')) == m_id +1


@pytest.mark.parametrize(["content","sender","thread","id"],[
(generate_random_message(25), 2,3,None),
(generate_random_message(46), '2','3', None),
(generate_random_message(50), 2,3,92)
])
def test_create_message_dict(content,sender,thread,id):
    if id is not None:
        message_dict = create_message_dict(content,sender,thread,id=id)
    else:
        message_dict = create_message_dict(content,sender,thread)
    
    assert str(content) == message_dict['content']
    assert int(sender) == message_dict['sender']
    assert int(thread) == message_dict['thread']
    if id:
        assert int(id) == message_dict['id']
    else:
        assert isinstance(message_dict['id'], int)

def test_create_default_thread_name():
    assert create_default_thread_name(['a']) == "TEST"

