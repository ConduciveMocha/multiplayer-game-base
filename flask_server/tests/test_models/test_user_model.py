import pytest

from werkzeug.security import check_password_hash

from server.db.models import User, Email
from server.logging import make_test_logger, log_test

logger = make_test_logger(__name__)


@pytest.mark.parametrize(
    "username,password,email",
    [("testuser12345", "password123456", "testemail@email.com")],
)
@log_test(logger)
def test_user_model(username, password, email):
    user = User(username, password, email)

    assert user.username == username
    assert user.email.email == email
    assert user.password_hash is not None
    assert user.password_salt is not None
    assert user.check_login(username, password) == True


@log_test(logger)
def test_check_login(with_app):
    username, password, email = (
        "testuser12345",
        "password123456",
        "testemail@email.com",
    )
    user = User(username, password, email)

    assert user.check_login(username, password) == True
    assert user.check_login("wrong_user", password) == False
    assert user.check_login(username, "wrongpassword") == False
    assert user.check_login("wrong_user", "wrongpassword") == False


@log_test(logger)
def test_password_prop(with_app):
    username, password, email = (
        "testuser12345",
        "password123456",
        "testemail@email.com",
    )
    user = User(username, password, email)
    assert "$" in user.password
    assert user.password.startswith("pbkdf2:sha256")
    assert check_password_hash(user.password, password)
    assert user.check_login(username, password)

    old_salt, old_hash = user.password_salt, user.password_hash
    new_pass = "pass_word1234"
    user.password = new_pass

    assert "$" in user.password
    assert user.password.startswith("pbkdf2:sha256")
    assert old_salt != user.password_salt
    assert old_hash != user.password_hash

    assert check_password_hash(user.password, password) == False
    assert check_password_hash(user.password, new_pass)
    assert user.check_login(username, new_pass)


@pytest.mark.parametrize(
    "username,expected",
    [
        ("username123456", True),
        ("username_use2", True),
        ("USERNAME___", True),
        ("", False),
        ("\n\n\n\n\n\n\n", False),
        ("123456789", False),
        ("_________", False),
        ("thisusernameiswaytoolong", False),
        ("<>[]\\@#$%^&&#", False),
    ],
)
@log_test(logger)
def test_username_validation(with_app, username, expected):
    password, email = "password123456", "testemail@email.com"
    if expected == True:
        user = User(username, password, email)
        assert user.username == username
    else:
        try:
            user = User(username, password, email)
            assert False
        except AssertionError:
            assert True
