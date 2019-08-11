import pytest

import redis

from server.logging import make_test_logger, log_test
from server.redis_cache.poolmanager import PoolManager
from app import create_app
from app import poolman

logger = make_test_logger(__name__)


@pytest.fixture(scope="function")
def poolmanagers():
    PoolManager._POOLS = {}
    pm1 = PoolManager()

    app = create_app()
    app.config["REDIS_HOST"] = "localhost"
    app.config["REDIS_PORT"] = 6379
    app.config["REDIS_DB"] = 0
    pm2 = PoolManager()
    pm2.init_app(app)
    poolman.close_pool()
    pm3 = PoolManager(host="localhost", port=6379, db=0)
    logger.debug(f"Connections: {PoolManager._POOLS}")
    yield pm1, pm2, pm3
    pm2.close_pool()
    pm3.close_pool()




@log_test(logger)
def test_poolmam_attributes(poolmanagers):
    """
    Tests that attributes evaluate to correct values in each of the threa instantiation methods
    """
    pm1, pm2, pm3 = poolmanagers

    assert pm1.host is None
    assert pm1.port is None
    assert pm1.db is None
    assert pm1._key == (None, None, None)
    assert pm1.pool == None

    assert pm2.host == "localhost"
    assert pm2.port == 6379
    assert pm2.db == 0
    assert pm2._key == ("localhost", 6379, 0)
    assert pm2.pool != None

    assert pm3.host == "localhost"
    assert pm3.port == 6379
    assert pm3.db == 0
    assert pm3._key == ("localhost", 6379, 0)
    assert pm3.pool != None

    assert pm1._pool != pm2.pool
    assert pm1._key != pm2._key

    assert pm1._pool != pm3.pool
    assert pm1._key != pm3._key

    assert pm2._pool == pm3.pool

    assert pm1._key not in PoolManager._POOLS
    assert pm1._key not in pm1._POOLS

    assert pm2._key in PoolManager._POOLS
    assert pm2._key in pm2._POOLS

    assert pm3._key in PoolManager._POOLS
    assert pm3._key in pm3._POOLS


@log_test(logger)
def test_poolman_singleton(poolmanagers):
    """
    Tests that the class object PoolManager._POOLS is a singleton on the 
    instance variable _key
    """
    pm1, pm2, pm3 = poolmanagers

    assert pm1._key not in PoolManager._POOLS
    assert pm1._key not in pm1._POOLS
    assert pm1._key not in pm2._POOLS
    assert pm1._key not in pm3._POOLS

    assert pm1.pool not in map(lambda x: x["pool"], PoolManager._POOLS.values())
    assert pm1.pool not in map(lambda x: x["pool"], pm1._POOLS.values())
    assert pm1.pool not in map(lambda x: x["pool"], pm2._POOLS.values())
    assert pm1.pool not in map(lambda x: x["pool"], pm3._POOLS.values())

    assert pm2._key in PoolManager._POOLS
    assert pm2._key in pm1._POOLS
    assert pm2._key in pm2._POOLS
    assert pm2._key in pm3._POOLS
    assert pm2.pool in map(lambda x: x["pool"], PoolManager._POOLS.values())
    assert pm2.pool in map(lambda x: x["pool"], pm1._POOLS.values())
    assert pm2.pool in map(lambda x: x["pool"], pm2._POOLS.values())
    assert pm2.pool in map(lambda x: x["pool"], pm3._POOLS.values())

    assert pm3._key in PoolManager._POOLS
    assert pm3._key in pm1._POOLS
    assert pm3._key in pm2._POOLS
    assert pm3._key in pm3._POOLS
    assert pm3.pool in map(lambda x: x["pool"], PoolManager._POOLS.values())
    assert pm3.pool in map(lambda x: x["pool"], pm1._POOLS.values())
    assert pm3.pool in map(lambda x: x["pool"], pm2._POOLS.values())
    assert pm3.pool in map(lambda x: x["pool"], pm3._POOLS.values())


@log_test(logger)
def test_conn(poolmanagers):
    """
    Tests the connection property. Should return a redis instance if the pool
    is defined
    """
    pm1, pm2, pm3 = poolmanagers
    with pytest.raises(ValueError) as excinfo:
        pm1.conn
    assert "No pool open" in str(excinfo)

    assert isinstance(pm2.conn, redis.Redis)
    assert isinstance(pm3.conn, redis.Redis)


# TODO add check to ensure pipe executes
@log_test(logger)
def test_pipe(poolmanagers):
    """
    Tests the pipe context manager.
    """
    pm1, pm2, pm3 = poolmanagers

    with pytest.raises(ValueError) as excinfo:
        pm1.conn
    assert "No pool open" in str(excinfo)

    with pm2.pipe() as pipe:
        assert isinstance(pipe, redis.Redis)
    with pm2.pipe() as pipe:
        assert isinstance(pipe, redis.Redis)

    with pm3.pipe() as pipe:
        assert isinstance(pipe, redis.Redis)


# TODO: Add force close tests
@log_test(logger)
def test_close_pool(poolmanagers):
    """
    Tests closing the connection pool. Should only close the redis.ConnectionPool if no
    other objects are using the connection pool -- ConnectionPools are a singleton on _key
    """
    pm1, pm2, pm3 = poolmanagers
    logger.debug(f"_POOLS: {PoolManager._POOLS}")
    assert pm1.close_pool() == False
    logger.debug(f"_POOLS: {PoolManager._POOLS}")
    assert pm2.close_pool() == False
    logger.debug(f"_POOLS: {PoolManager._POOLS}")
    assert pm3.close_pool() == True
    logger.debug(f"_POOLS: {PoolManager._POOLS}")
    pm2 = PoolManager(host="localhost", port=6379, db=0)
    logger.debug(f"_POOLS: {PoolManager._POOLS}")
    assert pm3.close_pool() == False
    logger.debug(f"_POOLS: {PoolManager._POOLS}")
    assert pm2.close_pool() == True
