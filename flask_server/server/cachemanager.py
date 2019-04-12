import logging
import redis


class RedisNamespace:
    CHILD_NAMESPACES = [""]
    PARENT_NAMESPACES = None


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
