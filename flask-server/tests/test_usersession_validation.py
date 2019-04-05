import pytest
from server.db.usersession import UserSession

test_usernames = [
    ('username12345', True),                  # Valid
    ('UserName12345', True),                  # Valid
    ('usernameusernads', True),               # Valid
    ('Username_undre', True),                 # Valid
    ('a', False),                             # Too Short
    ('asdfbasdfasdfsdfsdfasdfasdfas', False), # Too Long
    ('12345678', False),                      # Only numbers
    ('username-', False),                     # Special Character
    ('User<>useruser', False),                # Special Character
    ('username12345\n', False),               # Newline Character
    ('username\t\t\t\t', False),              # Tab
    ('username Username', False),             # Space
    ('User😀suserus', False),                 # Unicode Character
]

test_emails = [
    ('test@test.com', True),               # Valid
    ('TEST@test.Com', True),               # Valid
    ('example@example', False),            # No TLD
    ('example.Example',  False),           # No Domain      
    ('@t.com', False),                     # No local
    ('lorem ipsum valid@email.com', False) # Match not at start of string
]

test_passwords = [
    ('AbCdEFgH', True),                    # Valid
    ('a', False),                          # Too Short
    ('1assdfsdfsdfsdfsdfsd',False),        # Too Long
    ('\n\n\n\n\n\n\n\n\n\n', False)        # Whitespace Characters
]



@pytest.mark.parametrize("test_un, expected", test_usernames)
def test_valid_username(test_un, expected):
    assert UserSession.valid_username(test_un) == expected

@pytest.mark.parametrize("test_email, expected", test_emails)
def test_valid_email(test_email,expected):
    assert UserSession.valid_email(test_email) == expected

@pytest.mark.parametrize("test_pw, expected", test_passwords)
def test_valid_password(test_pw,expected):
    assert UserSession.valid_password(test_pw) == expected
