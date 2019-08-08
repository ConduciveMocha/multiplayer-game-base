#


from random import random, randint, choices, uniform
from math import floor

from server.db.models import User, Email


#   Constant definitions
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


# Gets words from a dictionary file
def get_wordlist(dictionary="./words.txt"):
    wordlist = []
    with open(dictionary, "r") as f:
        for word in f:
            word = word.rstrip()
            if not word:
                continue
            wordlist.append(word.rstrip())

    return wordlist


# Defines constant 'WORD_LIST'
try:
    WORD_LIST = get_wordlist()
except FileNotFoundError:
    import os

    print(os.getcwd())
    WORD_LIST = get_wordlist(
        dictionary="/home/nate/code/multiplayer-game-base/flask_server/server/utils/words.txt"
    )

# Dictionary that can be called like an object. Actually, more like
# an object that can be called like a dictionary! Keys must be strings
# to insure thjat they are able to be called with a '.'
class FlexDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        self[name] = value


class ValueGenerator:
    def __init__(
        self,
        func,
        name=None,
        existing=None,
        unique=True,
        stop_after=None,
        satisfies=None,
    ):
        self.func = (
            func
        )  # Function that creates a random value based on undefinded inputs
        self.name = name if name else func.__name__  # Name of value
        self._unique = (
            unique
        )  # If unique is true, each value is saved in memory and no new value can match it
        self.existing = (
            existing if existing else []
        )  # Allows values to be added at init
        self._generated = set(
            self.existing
        )  # Set of existing values. Only used if `self.unique` == true
        self.stop_after = (
            stop_after if stop_after else -1
        )  # Integer limit on number of times to run the value generator function.
        self.satisfies = (
            satisfies if satisfies else lambda *args, **kwargs: True
        )  # External function to check if the value generated is valid
        self.args = ()  # Memoized arguments to be passed to the function #! Make them tuples?
        self.kwargs = {}  # Memoized kwargs to be passed to the value generator

    def __call__(self, *args, **kwargs):

        i = self.stop_after
        while True:
            val = self.func(*args, **kwargs)
            try:
                if val not in self._generated and self.satisfies(val):
                    if self.unique:
                        self._generated.add(val)
                    return val
                else:
                    i -= 1
                    if i is 0:
                        raise Exception("Could not create value")
            except TypeError:
                return val

    def getn(self, n, *args, **kwargs):
        if not args and not kwargs:
            self.args = args
            self.kwargs = kwargs

        for _ in range(n):
            yield self.__call__(*self.args, **self.kwargs)

        self.args = ()
        self.kwargs = {}

        raise StopIteration

    def with_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    @property
    def unique(self):
        return self._unique

    @property
    def generated(self):
        return self._generated

    def add_value(self, val, to_generated=True, to_existing=False):
        if not self.unique:
            print("un")
        elif not to_generated and not to_existing:
            print(
                "to_generated and to_existing are false. No modification will be made"
            )
        if to_generated:
            self._generated.add(val)
        if to_existing:
            self.existing.append(val)

    def reset(self):
        self._generated(self.existing)

    @classmethod
    def compose(cls, *value_generators, name=None):

        if any(not isinstance(generator, cls) for generator in value_generators):
            # DEBUG STUFF
            print(cls)
            for generator in value_generators:
                print(type(generator))
            raise ValueError

        def composed_function(*args, **kwargs):
            return FlexDict(
                {
                    generator.name: generator(*args, **kwargs)
                    for generator in value_generators
                }
            )

        if name is None:
            name = f'Composed({",".join(generator.name for generator in value_generators)})'

        return cls(
            composed_function, name=name, unique=False, satisfies=None, stop_after=1
        )


def value_generator(func_arg=None, *args, **kwargs):
    if callable(func_arg):
        return ValueGenerator(func_arg, *args, **kwargs)
    else:

        def decorator(func):
            return ValueGenerator(func, *args, **kwargs)

        return decorator


@value_generator(name="username", satisfies=User.validate_username, stop_after=50)
def generate_username():
    return "".join(choices(USERNAME_CHARS, k=randint(8, 16)))


@value_generator(name="password", unique=False)
def generate_password():
    return "".join(choices(PASSWORD_CHARS, k=randint(8, 16)))


@value_generator(name="email", satisfies=Email.validate_email, stop_after=50)
def generate_email():
    local = "".join(choices(EMAIL_LOCAL_CHARS, k=randint(1, 45)))
    domain = "".join(choices(EMAIL_DOMAIN_CHARS, k=randint(1, 10)))
    tld = "".join(choices(EMAIL_DOMAIN_CHARS, k=randint(2, 3)))
    email = f"{local}@{domain}.{tld}"
    return email


@value_generator(name="user_sid", unique=True, stop_after=100)
def generate_user_sid():
    sid = ["S", str(randint(0, 9))] + [
        str(randint(1, 10000000000)) for _ in range(randint(1, 15))
    ]
    return "-".join(sid)


generate_online = ValueGenerator(lambda: round(random()), name="online", unique=False)
generate_user_id = ValueGenerator(
    lambda: randint(1, 10000), name="user_id", stop_after=100
)

generate_user = ValueGenerator.compose(
    generate_username,
    generate_password,
    generate_user_id,
    generate_email,
    generate_online,
    generate_user_sid,
    name="user",
)


def generate_random_message(num_words, wordlist=None):
    if wordlist is None or len(wordlist) == 0:
        wordlist = get_wordlist()
    word_array = choices(wordlist, k=num_words)
    word_array[0] = word_array[0].capitalize()
    return " ".join(word_array) + "."


def generate_message_element(min_len=5, max_len=50, sender=None, wordlist=None):
    if sender not in ["sent", "recieved"]:
        sender = ["sent", "recieved"][round(random())]

    wrapped = f"<div class='message'>\n\t<div class='{sender}'>\n\t\t<p class='{sender}-message'>\n\t\t{generate_random_message(floor(uniform(min_len,max_len)), wordlist=wordlist)}\n\t\t</p>\n\t</div>\n</div>"
    return wrapped


for _ in range(15):
    print(generate_message_element(wordlist=WORD_LIST))


# generate_message = ValueGenerator()
mock_user_list = []
