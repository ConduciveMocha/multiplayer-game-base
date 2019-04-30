import pytest
import redis

from flask import request

from server.logging import make_logger, log_test
from server.utils.redisutils import decode_dict
from app import poolman
from server.redis_cache.user_cache import (
    get_online_users,
    get_user,
    user_online,
    set_user_online,
    set_user_offline,
    extend_user_data,
    user_from_sid,
    echo,
    decode_dict,
    DEFAULT_USER_EXPIRE,
)

logger = make_logger(__name__)


def test_echo(poolman_app):
    app, poolman = poolman_app
    with app.test_request_context("/"):
        x = echo()
        assert x.decode("utf-8") == "Test"


def test_get_online_users(poolman_app, populate_users):

    cached_users = get_online_users()

    for mock_user in populate_users:
        logger.debug(f"{mock_user.online}")
        if mock_user.online:
            cache_data = cached_users[mock_user.user_id]
            assert mock_user.user_id in cached_users
            assert int(cache_data["user_id"]) == mock_user.user_id
            assert cache_data["username"] == mock_user.username
            assert int(cache_data["online"]) == mock_user.online
        else:
            assert mock_user.user_id not in cached_users


def test_user_online(poolman_app, populate_users):
    app, poolman = poolman_app

    for mock_user in populate_users:
        if mock_user.online == 1:
            assert user_online(mock_user.user_id)
        else:
            assert user_online(mock_user.user_id) == False
    logger.info(f"{user_online(-100)}")
    assert user_online(-100) == False
    assert user_online("apple") == False


def test_get_user(poolman_app, populate_users):
    app, poolman = poolman_app
    for mock_user in populate_users:

        cache_data = get_user(mock_user.user_id)
        assert cache_data is not None
        assert int(cache_data["user_id"]) == mock_user.user_id
        assert cache_data["username"] == mock_user.username
        assert int(cache_data["online"]) == mock_user.online

    assert get_user(-1500) is None
    assert get_user("asdf") is None


def test_set_user_online(poolman_app, populate_users):
    offline_users = filter(lambda x: not bool(x.online), populate_users)
    for mock_user in offline_users:
        mock_user.id = mock_user.user_id
        assert mock_user.online == 0
        assert user_online(mock_user.user_id) == False

        user_id = set_user_online(mock_user, mock_user.user_sid)

        assert user_id in get_online_users()
        assert user_online(user_id)

        cache_data = get_user(user_id)

        assert cache_data is not None
        assert int(cache_data["user_id"]) == user_id
        assert cache_data["username"] == mock_user.username
        assert int(cache_data["online"]) == mock_user.online
        assert cache_data["user_sid"] == mock_user.user_sid

        assert user_from_sid(mock_user.sid) == user_id
