import redis
from functools import wraps, partial
from enum import Enum
from server.redis_cache.redisobject import RedisObject, NoRedisConnection


class RedisTypeEnum(Enum):
    ANY = (
        "delete",
        "exists",
        "expire",
        "expireat",
        "persist",
        "pexpire",
        "pexpireat",
        "pttl",
        "rename",
        "renamenx",
        "touch",
        "ttl",
        "pexpire",
    )
    KEY = (
        *ANY,
        "append",
        "bitcount",
        "bitfield",
        "bitop",
        "bitpos",
        "decr",
        "decrby",
        "get",
        "getbit",
        "getrange",
        "getset",
        "incr",
        "incrby",
        "incrbyfloat",
        "mget",
        "mset",
        "msetnx",
        "psetex",
        "set",
        "setbit",
        "setex",
        "setnx",
        "setrange",
        "strlen",
        "scan",
    )
    LIST = (
        *ANY,
        "blpop",
        "brpop",
        "brpoplpush",
        "lindex",
        "linsert",
        "llen",
        "lpop",
        "lpush",
        "lpushx",
        "lrange",
        "lrem",
        "lset",
        "ltrim",
        "rpop",
        "rpoplpush",
        "rpush",
        "rpushx",
    )
    HASH = (
        *ANY,
        "hdel",
        "hexists",
        "hget",
        "hgetall",
        "hincrby",
        "hincrbyfloat",
        "hkeys",
        "hlen",
        "hmget",
        "hmset",
        "hset",
        "hsetnx",
        "hstrlen",
        "hvals",
        "hscan",
    )
    SET = (
        *ANY,
        "sadd",
        "scard",
        "sdiff",
        "sdiffstore",
        "sinter",
        "sinterstore",
        "sismember",
        "smembers",
        "smove",
        "spop",
        "srandmember",
        "srem",
        "sunion",
        "sunionstore",
        "sscan",
    )
    ZET = (
        *ANY,
        "zadd",
        "zcard",
        "zcount",
        "zincrby",
        "zinterstore",
        "zlexcount",
        "zpopmax",
        "zpopmin",
        "zrange",
        "zrangebylex",
        "zreverangebylex",
        "zrangebyscore",
        "zrank",
        "zrem",
        "zremrangebylex",
        "zremrangebyrank",
        "zremrangebyscore",
        "zrevrange",
        "zreverangebyscore",
        "zrevrank",
        "zscore",
        "zunionstore",
        "zscan",
    )
    HYPERLOGLOG = (*ANY, "pfadd", "pfcount", "pfmerge")
    HASHFIELD = (
        "hdel",
        "hexists",
        "hget",
        "hincrby",
        "hincrbyfloat",
        "hset",
        "hsetnx",
        "hstrlen",
    )


class RedisType(RedisObject):
    _REDIS_TYPE = RedisTypeEnum.ANY

    def __init__(self, name, parent=None):

        super().__init__(name, parent=parent, children=None)

    @staticmethod
    def redis_method(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            obj, *args = args
            if obj.r is None:
                raise AttributeError

            else:
                return func(*args, **kwargs)

    def typed_redis_method(arg_type, n=1):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                obj, *args = args
                if n - 1 is 0:
                    if isinstance(args[0], arg_type):
                        return func(*args, **kwargs)
                    else:
                        raise TypeError
                else:
                    if all(isinstance(arg, arg_type) for arg in args.islice(n - 1)):
                        func(*args, **kwargs)
                    else:
                        raise TypeError

            return wrapper

        return decorator

    def make_functions(self):
        if self._r is None:
            for f in self._REDIS_TYPE.value:
                self.__dict__[f] = None
        else:
            for f in self._REDIS_TYPE.value:
                self.__dict__[f] = partial(self._r.__getattribute__(f), self.key)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        if self.r is not r:
            self._r = r
            self.make_functions()
            if self.children:
                for c in self.children:
                    c.r = r

    @property
    def ttl(self):
        return self.ttl()

    @property
    def pttl(self):
        return self.pttl()


class RedisHashField(RedisType):
    _REDIS_TYPE = RedisTypeEnum.HASHFIELD

    def make_functions(self):
        if self.r is None:
            for f in self._REDIS_TYPE.value:
                self.__dict__[f] = None
        else:
            for f in self._REDIS_TYPE.value:
                self.__dict__[f] = partial(
                    self.r.__getattribute__(f), self.key, self.name
                )

    def __init__(self, name, parent):
        if parent is None:
            raise TypeError
        super().__init__(name, parent=parent)
        self._name = name
        self._key = self.parent.key
        self._r = self.parent.r
        self.make_functions()

    @property
    def name(self):
        return self._name

    @property
    def key(self):
        return self._key

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        if r is self.parent.r and self.r is not r:
            self._r = r
            self.make_functions()


class RedisHash(RedisType):
    _REDIS_TYPE = RedisTypeEnum.HASH

    def __init__(self, name, fields, parent=None):

        super().__init__(name, parent=parent)
        if all(
            [
                field not in self.__class__.__dict__
                and field not in redis.Redis.__dict__
                for field in fields
            ]
        ):
            self.fields = map(lambda field: RedisHashField(field), fields)
        else:
            raise AttributeError

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self.set_parent(parent)

    @RedisType.redis_method
    def __len__(self):
        return self.hlen()

    @RedisType.redis_method
    def __getitem__(self, field):
        if field not in fields:
            raise KeyError
        else:
            return self.hget(field)

    @RedisType.redis_method
    def __setitem__(self, field, value):
        self.r.hset(self.key, field, value)
        if field not in fields:
            self.fields.append(field)

    @RedisType.redis_method
    def __delitem__(self, field):
        if field in self.fields:
            self.fields.remove(field)
            self.hdel(field)

    def __contains__(self, item):
        return item in fields

    @RedisType.redis_method
    def get(self, names=None):
        if names:
            return self.hget(*names)
        else:
            return self.hgetall()

    @RedisType.redis_method
    def set(self, vals):

        if isinstance(vals, dict):
            old_fields = self.fields
            old_val = self.hgetall()
            try:
                self.delete()
                self.hmset(vals)
                self.fields = list(vals.keys())
            except Exception:
                try:
                    self.fields = old_fields
                    self.delete()
                    self.hmset(old_val)
                except Exception:
                    self.fields = None

        elif isinstance(vals, list):
            if len(vals) is not len(self.fields):
                raise ValueError
            else:
                self.delete()
                self.hmset({f: v for f, v in zip(self.fields, vals)})
        else:
            raise ValueError


class RedisKey(RedisType):
    _REDIS_TYPE = RedisTypeEnum.KEY

    def __init__(self, name, parent):
        super().__init__(name, parent=parent)

    @RedisType.redis_method
    def set(self, value):
        self.set(value)

    @RedisType.redis_method
    def get(self):
        return self.get()

    @RedisType.redis_method
    def __len__(self):
        return self.strlen()

    @RedisType.redis_method
    def append(self, val):
        self.append(val)


class RedisList(RedisType):
    _REDIS_TYPE = RedisTypeEnum.LIST

    @RedisType.redis_method
    def __len__(self):
        return self.llen()

    @RedisType.redis_method(int)
    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.step is None:
                return self.lrange(index.start, index.stop)
            else:
                return self.lrange(index.start, index.stop)[:: index.step]
        elif isinstance(index, int):
            self.lindex(index)
        else:
            raise TypeError

    @RedisType.typed_redis_method(int)
    def __setitem__(self, index, value):
        self.lset(index, value)

    @RedisType.redis_method
    def push(self, *values):
        for value in values:
            self.rpush(value)

    @RedisType.redis_method
    def pop(self):
        return self.rpop()

    @RedisType.redis_method
    def insert_before(self, pivot, val):
        self.linsert("BEFORE", pivot, val)

    @RedisType.redis_method
    def insert_after(self, pivot, val):
        self.linsert("AFTER", pivot, val)

    @RedisType.redis_method
    def enqueue(self, *values):
        for value in values:
            self.lpush(value)

    @RedisType.redis_method
    def dequeue(self):
        self.lpop()

    @RedisType.redis_method
    def lpeek(self):
        return self.lindex(0)

    @RedisType.redis_method
    def rpeek(self):
        return self.lindex(-1)


class RedisSet(RedisType):
    _REDIS_TYPE = RedisTypeEnum.SET

    @RedisType.redis_method
    def __len__(self):
        return self.scard()

    @RedisType.redis_method
    def rand(self):
        return self.srandmember()

    @RedisType.redis_method
    def get(self):
        return self.smembers()

    @RedisType.redis_method
    def set(self, new_set):
        try:
            new_set = set(new_set)
            self.delete()
            self.sadd(new_set)
        except Exception:
            print(e)
            print(type(e))
            print("RedisSet.set")

    @RedisType.redis_method
    def remove(self, *members):
        self.srem(*members)

    @RedisType.redis_method
    def __contains__(self, val):
        return self.sismember(val)

    @RedisType.typed_redis_method(RedisSet)
    def __and__(self, other):
        return self.union(other.key)

    @RedisType.typed_redis_method(RedisSet)
    def __iand__(self, other):
        self.sunionstore(other.key, self.key)


class RedisZet(RedisType):
    _REDIS_TYPE = RedisTypeEnum.ZET

    @RedisType.redis_method
    def __len__(self):
        return self.zcard()
