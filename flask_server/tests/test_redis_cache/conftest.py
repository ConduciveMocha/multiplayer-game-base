import pytest
import redis

from flask import g

from server.redis_cache.poolmanager import PoolManager
from server.utils.data_generators import generate_user
from server.logging import make_logger, log_test

logger = make_logger("test_redis_cache" + __name__)


@pytest.fixture(scope="session")
def poolman_app(app):
    with app.test_request_context("/"):
        poolman = PoolManager()
        poolman.init_app(app)
        g.poolman = poolman

        return app, poolman


@pytest.fixture(scope="session")
def populate_users(poolman_app):
    app, poolman = poolman_app
    user_list = list(generate_user.getn(100))
    # Add to redis
    with poolman as r:
        for mock_user in user_list:
            del mock_user["password"]
            del mock_user["email"]
            r.hmset(f"user:{mock_user['user_id']}", mock_user)
            if mock_user["online"] == 1:
                r.sadd("user:online", mock_user["user_id"])

    yield user_list

    # Remove from redis
    logger.info("Deleting users")
    with poolman as r:
        for mock_user in user_list:
            r.delete(f"user:{mock_user['user_id']}")
        r.delete("user:online")
