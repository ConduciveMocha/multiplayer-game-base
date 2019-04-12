import pytest

from werkzeug.security import check_password_hash

from server.db import db_session
from server.models import User,Email




@pytest.mark.parametrize("username,password,email", [
("testuser12345", "password123456","testemail@email.com")
])
def test_user_model(username,password,email):
    user = User(username,password,email)
    
    assert user.username == username
    assert user.email.email == email
    assert user.password_hash is not None
    assert user.password_salt is not None
    assert user.check_login(username,password) == True


def test_check_login():
    username, password, email = (
        "testuser12345", "password123456", "testemail@email.com")
    user = User(username,password,email)

    assert user.check_login(username,password) == True
    assert user.check_login('wrong_user', password) == False
    assert user.check_login(username, 'wrongpassword') == False
    assert user.check_login('wrong_user', 'wrongpassword') == False    

def test_password_prop():
    username, password, email = (
        "testuser12345", "password123456", "testemail@email.com")
    user = User(username, password, email)
    assert '$' in user.password
    assert user.password.startswith('pbkdf2:sha256')
    assert check_password_hash(user.password,password)
    assert user.check_login(username,password)

    old_salt, old_hash = user.password_salt,user.password_hash
    new_pass = 'pass_word1234'
    user.password = new_pass
    
    assert '$' in user.password
    assert user.password.startswith('pbkdf2:sha256')
    assert old_salt != user.password_salt
    assert old_hash != user.password_hash

    assert check_password_hash(user.password,password) == False
    assert check_password_hash(user.password,new_pass)
    assert user.check_login(username, new_pass)


@pytest.mark.parametrize("username,expected",[
    ("username123456", True),
    ("username_use2",True),
    ("USERNAME___",True),
    ("", False),
    ("\n\n\n\n\n\n\n", False),
    ('123456789', False),
    ('_________', False),
    ('thisusernameiswaytoolong', False),
    ("<>[]\\@#$%^&&#", False)
])
def test_username_validation(username, expected):
    password, email = "password123456", "testemail@email.com"
    if expected == True:
        user = User(username,password,email)
        assert user.username == username
    else:
        try:
            user = User(username,password,email)
            assert False
        except AssertionError:
            assert True
        
    
@pytest.mark.parametrize("address,expected",[
    ('email.email@email.com', True),
    ('email@wisc.edu',True),
    ('email@government.gov', True),
    ('this is definitely not an email', False),
    ('@fails.com',False),
    ('email@email', False)
])
def test_email_validation(address,expected):
    if expected:
        email = Email(address)
        assert email.email == address
        assert email.verified == False

    else:
        try:
            email = Email(address)
            assert False
        except AssertionError:
            assert True
