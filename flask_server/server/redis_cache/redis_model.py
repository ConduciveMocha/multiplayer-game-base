import redis


class RedisEntry:
    _R = redis.Redis()
    _loaded_objects = {}
    def __init__(self, prefix=""):
        self.has_been_read = False
        self.prefix = prefix
        self.dirty = None
    def _save_loaded_object(self,obj_id):
        self._loaded_objects[str(self.__class__)][obj_id] = self
        

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


class LazyList:
    def __int__(self,load_function, initial_list=None):
        self._list = initial_list if initial_list is not None else []
        self.load_function = load_function
    def __len__(self):
        return self._list
    def __getitem__(self,key):
        return self.load_function(self._list[key])
    def __setitem__(self,key,value):
        self._list[key] = value

    def __delitem__(self,key):
        del self._list[key]

    @property
    def keys(self):
        return self._list

    def __iter__(self):
        for val in self._list:
            yield self.load_function(val)
        