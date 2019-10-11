import redis
from server.logging import make_logger

logger = make_logger(__name__)


class RedisEntry:

    _R = redis.Redis()
    _loaded_objects = {}

    def __init__(self, obj_id, prefix=""):
        self.has_been_read = False
        self.prefix = prefix
        self.dirty = None
        self._obj_id = obj_id
        self._save_object()

    def _save_object(self):
        if str(self.__class__) not in self._loaded_objects:
            self._loaded_objects[str(self.__class__)] = {}
        self._loaded_objects[str(self.__class__)][self._obj_id] = self

    @classmethod
    def _object_is_saved(cls, obj_id):
        cls_dict = cls._loaded_objects.get(str(cls), None)
        logger.debug(f"obj_id: {obj_id}")
        logger.debug(f"class dict: {cls_dict}\n\n")
        if cls_dict:
            return obj_id in cls_dict
        else:
            return False

    @classmethod
    def _get_saved_object(cls, obj_id):
        return cls._loaded_objects[str(cls)][obj_id]

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
    def __int__(self, load_function, initial_list=None):
        self._list = initial_list if initial_list is not None else []
        self.load_function = load_function

    def __len__(self):
        return self._list

    def __getitem__(self, key):
        return self.load_function(self._list[key])

    def __setitem__(self, key, value):
        self._list[key] = value

    def __delitem__(self, key):
        del self._list[key]

    @property
    def keys(self):
        return self._list

    def __iter__(self):
        for val in self._list:
            yield self.load_function(val)

