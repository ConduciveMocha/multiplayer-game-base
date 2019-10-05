import redis


class RedisEntry:
    _R = redis.Redis()

    def __init__(self, prefix=""):
        self.has_been_read = False
        self.prefix = prefix
        self.dirty = None

    @staticmethod
    def fix_hash_signature(d, sig):
        return {
            key.decode("utf-8"): sig[key.decode("utf-8")](val.decode("utf-8"))
            for key, val in d.items()
        }

    def make_key(self, *args):
        return ":".join([prefix] + args)

    def commit(self):
        raise NotImplementedError