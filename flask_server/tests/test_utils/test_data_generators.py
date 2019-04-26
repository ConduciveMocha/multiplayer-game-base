import pytest
from server.db.models import User,Email
from server.utils.data_generators import generate_random_username,generate_random_password,generate_random_email


def test_generate_username():
    for i in range(100):
        username = generate_random_username()
        assert User.validate_username(username) == True

def test_generate_email():
    for i in range(100):
        email = generate_random_email()
        assert Email.validate_email(email) == True

def test_generate_password():
    for i in range(100):
        password = generate_random_password()
            
        
        assert User.validate_password(password) == True