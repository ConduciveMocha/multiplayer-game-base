import pytest
import os

import serverconfig

""" Fixture that creates a function to set environment 
dict. Environment dict is reset back during cleanup.
"""
@pytest.fixture
def set_env():
    old_env_args = os.environ
    def _set_env(env_dict):
        for k,v in env_dict.items():
            os.environ[k] = v
    yield _set_env
    os.environ = old_env_args

""" Fixture that generates a secret key and a jwt 
key. Returns a tuple
"""
@pytest.fixture
def with_keys():
    return os.urandom(24).hex(), os.urandom(24).hex()

# Helper functuion that checks if config class matches
# the serverconfig.Config class
def config_is_base(config_base):
    __tracebackhide__ = True
    if not config_base.DEBUG == False:
        pytest.fail('DEBUG is not False ')
    if not config_base.TESTING == False:
        pytest.fail('TESTING is not False')
    if not isinstance(config_base.SECRET_KEY,str):
        pytest.fail('SECRET_KEY not a string')
    if not isinstance(config_base.JWT_KEY,str):
        pytest.fail('JWT_KEY is not a string')
    if not isinstance(config_base.DATABASE_URI,str):
        pytest.fail('DATABASE_URI is not a string')

# Helper functuion that checks if config class matches
# the serverconfig.DevelopmentConfig class
def config_is_dev(config_dev):
    __tracebackhide__ = True
    if not config_dev.DEBUG == True:
        pytest.fail('DEBUG is not True')
    if not config_dev.TESTING == False:
        pytest.fail('TESTING is not False')
    if not isinstance(config_dev.SECRET_KEY,str):
        pytest.fail('SECRET_KEY not a string')
    if not isinstance(config_dev.JWT_KEY,str):
        pytest.fail('JWT_KEY is not a string')
    if not isinstance(config_dev.DATABASE_URI,str):
        pytest.fail('DATABASE_URI is not a string')

# Helper functuion that checks if config class matches
# the serverconfig.TestingConfig class
def config_is_test(config_test):
    __tracebackhide__ = True
    if not config_test.DEBUG == False:
        pytest.fail('DEBUG is not False ')
    if not config_test.TESTING == True:
        pytest.fail('TESTING is not True')
    if not isinstance(config_test.SECRET_KEY,str):
        pytest.fail('SECRET_KEY not a string')
    if not isinstance(config_test.JWT_KEY,str):
        pytest.fail('JWT_KEY is not a string')
    if not isinstance(config_test.DATABASE_URI,str):
        pytest.fail('DATABASE_URI is not a string')

# Tests properties of Config
def test_config_class():
    config_base = serverconfig.Config
    config_is_base(config_base)

# Tests properties of DevelopmentConfig
def test_developmentconfig_class():
    config_dev = serverconfig.DevelopmentConfig
    config_is_dev(config_dev)

# Tests properties of TestingConfig
def test_testingconfig_class():
    config_test = serverconfig.TestingConfig
    config_is_test(config_test)

# Tests -p flag
def test_prod_flag():
    config_base = serverconfig.get_config(['-p'])
    config_is_base(config_base)

# Tests -d
def test_debug_flag():
    config_dev = serverconfig.get_config(['-d'])
    config_is_dev(config_dev)

# Tests -t flag
def test_testing_flag():
    config_test = serverconfig.get_config(['-t'])
    config_is_test(config_test)

# Tests setting environment variables DEBUG and TESTING 
# to False
def test_prod_env(set_env):
    set_env(env_dict={'DEBUG':'FALSE', 'TESTING':'FALSE'})
    config_base = serverconfig.get_config([])
    config_is_base(config_base)

# Tests setting DEBUG to True
def test_debug_env(set_env):
    set_env(env_dict={'DEBUG':'TRUE', 'TESTING':'FALSE'})
    config_dev = serverconfig.get_config([])
    config_is_dev(config_dev)

# Tests setting TESTING to True
def test_testing_env(set_env):
    set_env(env_dict={'DEBUG':'FALSE', 'TESTING':'TRUE'})
    config_test = serverconfig.get_config([])
    config_is_test(config_test)

# Tests -sk flag
def test_serverkey_flag(with_keys):
    key,_ = with_keys
    config_short = serverconfig.get_config(['-sk',key])
    config_long = serverconfig.get_config([f'--serverkey={key}'])
    
    assert config_short.SECRET_KEY == key # Check SECRET_KEY
    config_is_base(config_short)
    
    assert config_long.SECRET_KEY == key # Check SECRET_KEY
    config_is_base(config_long)

# Tests -jk flag
def test_jwtkey_flag(with_keys):
    _,jwt = with_keys
    config_short = serverconfig.get_config(['-jk',jwt])
    config_long = serverconfig.get_config([f'--jwtkey={jwt}'])
    
    assert config_short.JWT_KEY == jwt # Check JWT_KEY
    config_is_base(config_short)
    
    assert config_long.JWT_KEY == jwt  # Check JWT_KEY
    config_is_base(config_long)

# Tests -k flag
def test_keys_flag(with_keys):
    key,jwt = with_keys
    config_short = serverconfig.get_config(['-k',key,jwt])
    config_long = serverconfig.get_config(['--keys',key,jwt])
    
    assert config_short.SECRET_KEY == key # Check SECRET_KEY
    assert config_short.JWT_KEY == jwt    # Check JWT_KEY
    config_is_base(config_short)
    
    assert config_long.SECRET_KEY == key  # Check SECRET_KEY
    assert config_long.JWT_KEY == jwt     # Check JWT_KEY
    config_is_base(config_long)

# Tests setting keys and DATABASE_URI in env
def test_keydb_env(set_env,with_keys):
    key,jwt = with_keys
    db_uri = 'dburi'
    set_env(env_dict={'SECRET_KEY':key, 'JWT_KEY':jwt, 'DATABASE_URI':db_uri})
    config = serverconfig.get_config([])
    assert config.SECRET_KEY == key # Check SECRET_KEY
    assert config.JWT_KEY == jwt    # Check JWT_KEY
    assert config.DATABASE_URI == db_uri # Check DATABASE_URI


