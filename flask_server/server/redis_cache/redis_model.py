import redis
        

class RedisEntry:

    def __init__(self,prefix=""):
        self._r = redis.Redis()
        self.has_been_read = False
        self.prefix = prefix
    
    @staticmethod
    def fix_hash_signature(d,sig):
        return {key.decode('utf-8'):sig[key.decode('utf-8')](val.decode('utf-8')) for key,val in d.items()}

    def make_key(self,*args):
        return ":".join([prefix] + args)







