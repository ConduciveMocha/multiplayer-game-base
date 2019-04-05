import pytest
from server.db.usersession import UserSession

@pytest.fixture
def user_sess():
    return UserSession()

def test_username_in_use(user_sess):
    assert user_sess.username_in_use('nate12345678') == True  # Valid - Base Case
    assert user_sess.username_in_use('notinuse123') == False  # Invalid - Base Case
    assert user_sess.username_in_use(' nate12345678') == True # Valid - Padded

def test_email_in_use(user_sess):
    assert user_sess.email_in_use('email.email@email.com') == True      # Valid - Base Case
    assert user_sess.email_in_use('email.notinuse@gmail.com') == False  # Invalid - Base Case
    assert user_sess.email_in_use('email.email@email.com ') == True     # Valid - Padded


def test_validate_failed_username(user_sess):
    valid_username = 'nate12345678'
    valid_password = 'password123'
    valid_email = 'example@email.com'

    invalid_username = 'invalidusernamecauseitslogn'