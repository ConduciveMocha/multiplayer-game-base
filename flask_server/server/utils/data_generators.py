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
        self.func = func
        self.name = name if name else func.__name__
        self._unique = unique
        self.existing = existing if existing else []
        self._generated = set(self.existing)
        self.stop_after = stop_after if stop_after else -1
        self.satisfies = satisfies if satisfies else lambda *args, **kwargs: True
        self.args = ()
        self.kwargs = {}

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

        def composedFunction(*args, **kwargs):
            return FlexDict(
                {
                    generator.name: generator(*args, **kwargs)
                    for generator in value_generators
                }
            )

        if name is None:
            name = f'Composed({",".join(generator.name for generator in value_generators)})'

        return cls(
            composedFunction, name=name, unique=False, satisfies=None, stop_after=1
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
    return "".join(random.choices(USERNAME_CHARS, k=random.randint(8, 16)))


@value_generator(name="password", unique=False)
def generate_password():
    return "".join(random.choices(PASSWORD_CHARS, k=random.randint(8, 16)))


@value_generator(name="email", satisfies=Email.validate_email, stop_after=50)
def generate_email():
    local = "".join(random.choices(EMAIL_LOCAL_CHARS, k=random.randint(1, 45)))
    domain = "".join(random.choices(EMAIL_DOMAIN_CHARS, k=random.randint(1, 10)))
    tld = "".join(random.choices(EMAIL_DOMAIN_CHARS, k=random.randint(2, 3)))
    email = f"{local}@{domain}.{tld}"
    return email


@value_generator(name="user_sid", unique=True, stop_after=100)
def generate_user_sid():
    sid = ["S", str(random.randint(0, 9))] + [
        str(random.randint(1, 10000000000)) for _ in range(random.randint(1, 15))
    ]
    return "-".join(sid)


generate_online = ValueGenerator(
    lambda: round(random.random()), name="online", unique=False
)
generate_user_id = ValueGenerator(
    lambda: random.randint(1, 10000), name="user_id", stop_after=100
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
for _ in range(20):
    print(generate_user())
for user in generate_user.getn(20):
    print(user)
