import random

from server.db.models import User, Email

ALPHA_UPPER = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
ALPHA_LOWER = [chr(i) for i in range(ord("a"), ord("z") + 1)]
NUM_CHARS = [str(i) for i in range(10)]
USERNAME_SPECIAL = ["_"]
PASSWORD_SPECIAL = list("!@#$%^&*()-_+={]}[\\|~`/?.>,<;:\"'")
EMAIL_LOCAL_SPECIAL = list(".-")
EMAIL_DOMAIN_SPECIAL = ["-"]

ALPHA_NUM = ALPHA_LOWER + ALPHA_UPPER + NUM_CHARS

USERNAME_CHARS = ALPHA_NUM + USERNAME_SPECIAL
PASSWORD_CHARS = ALPHA_NUM + PASSWORD_SPECIAL
EMAIL_LOCAL_CHARS = ALPHA_LOWER + NUM_CHARS + EMAIL_LOCAL_SPECIAL
EMAIL_DOMAIN_CHARS = ALPHA_LOWER + NUM_CHARS + EMAIL_DOMAIN_SPECIAL


def generate_random_username():
    for i in range(100):
        # ugly, UGLY list comp to get list of valid username characters
        username = "".join(random.choices(USERNAME_CHARS, k=random.randint(8, 16)))
        if User.validate_username(username):
            break
    else:
        raise Exception(
            "Called by conftest:random_username after failing to generate a valid username after 100 tries"
        )
    return username


def generate_random_password():
    password = "".join(random.choices(PASSWORD_CHARS, k=random.randint(8, 16)))
    return password


def generate_random_email():
    for i in range(100):
        local = "".join(random.choices(EMAIL_LOCAL_CHARS, k=random.randint(1, 45)))
        domain = "".join(random.choices(EMAIL_DOMAIN_CHARS, k=random.randint(1, 10)))
        tld = "".join(random.choices(EMAIL_DOMAIN_CHARS, k=random.randint(2, 3)))
        email = f"{local}@{domain}.{tld}"
        if Email.validate_email(email):
            break
    else:
        raise Exception(
            "Called by random email after failing to generate a valid email after 100 tries"
        )
    return email


def mock_user_list(n=100):
    return [
        (
            generate_random_username(),
            generate_random_password(),
            generate_random_email(),
        )
        for _ in range(n)
    ]
