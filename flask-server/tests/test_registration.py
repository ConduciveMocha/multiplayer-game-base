import pytest

from app import app
from server.serverconfig import TestingConfig
from server.db import db_session
from server.models import User, Email
mock_users_list = [
    ('testuser' + str(i), 'password1234', f'email{i}@email.com') for i in range(10)
]

@pytest.fixture
def client():
    app.config.from_object(TestingConfig)
    _client = app.test_client()
    yield client


@pytest.fixture
def mock_users():
    user_list = []
    for u in mock_users_list:
        username, password, email = u
        try:
            current_user = db_session.query(User).filter(User.username==username, email==email).one()
            user_list.append(current_user)
        except Exception as e:
            try:
                new_user = User(username,password,email)
            except AssertionError:
                continue
            db_session.add(new_user)
            db_session.commit()
            user_list.append(new_user)
    return user_list


def test_mock_users(mock_users):
    assert len(mock_users) > 0
    for i,u in enumerate(mock_users):
        print(f'{i+1}. {u.username} - {u.password} - {u.email} ')
        assert u.username is not None
        assert u.password is not None
        assert u.email is not None



