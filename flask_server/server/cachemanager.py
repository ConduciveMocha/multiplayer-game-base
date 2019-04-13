import logging
import redis

r = redis.Redis(host='localhost', port=6379, db=0)


class RedisNamespace:
    __NAMESPACE_NAME__ = ""
    CHILD_NAMESPACES = ["_DEBUG", "_PERSIST"]
    PARENT_NAMESPACE = None

    @classmethod
    def make_namespace(cls, namespace_name):
        cls.__NAMESPACE_NAME__ = namespace_name

        cls.__setattr__(namespace_name,)


def insert(namespace, elements, indices=None):
    with r.pipeline() as p:
        for el in elements:
            p.hmset(namespace, el)
            for index in indices:
                p.zadd(f'{namespace}:{index.name}', {el[index.name]: el[index.value]},
                       nx=index.nx, xx=index.xx, ch=index.ch, incr=index.incr)
        p.execute()


def persist(key):
    r.hset('_PERSIST', key, 1)


def remove(key):
    with r.pipeline as p:
        if not p.hget('_PERSIST', key):
            p.delete(key)
            r.hdel('_PERSIST', key)
        else:
            # Add callback task to queue
            pass


class CacheManager:
    REDIS_POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)

    def __init__(self):
        self.r = redis.Redis(connection_pool=CacheManager.REDIS_POOL)

    def __enter__(self):
        return self.r

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            # TODO add logging here
            pass

        CacheManager.REDIS_POOL.release(self.r)
        self.r = None
