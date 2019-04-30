import pytest
from server.db.models import User, Email
from server.utils.data_generators import (
    generate_username,
    generate_email,
    generate_password,
    generate_online,
    generate_user_id,
    generate_user_sid,
    generate_user,
)


def test_generate_username():
    for i in range(100):
        username = generate_username()
        assert User.validate_username(username) == True


def test_generate_email():
    for i in range(100):
        email = generate_email()
        assert Email.validate_email(email) == True


def test_generate_password():
    for i in range(100):
        password = generate_password()
        assert User.validate_password(password) == True
