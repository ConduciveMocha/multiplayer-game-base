def make_namespace_function(prefixes=None, postfixes=None, name=None):
    if prefixes is None:
        prefix = ""
    else:
        prefixes = [prefixes] if isinstance(prefixes, str) else prefixes
        prefix = ":".join(prefixes) if prefixes else ""

    if postfixes is None:
        postfix = None
    else:
        postfixes = [postfixes] if isinstance(postfixes, str) else postfixes
        postfix = ":".join(postfixes)

    def namespace_function(val):
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        else:
            val = str(val)
        return f'{prefix + ":" if prefix else ""}{val}{":"+postfix if postfix else ""}'

    namespace_function.__name__ = (
        f'{name if name else prefix}{"" + postfix if postfix else ""}_namespace'
    )

    return namespace_function


user = make_namespace_function("user")
user_threads = make_namespace_function("user", "threads")
user_online = "user:online"
user_sid = make_namespace_function(["user", "sid"])

