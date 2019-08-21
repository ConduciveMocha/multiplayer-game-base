import logging
import copy
import redis
from redis.lock import Lock
from contextlib import contextmanager
from functools import wraps

from flask import g, _app_ctx_stack, current_app

from server.logging import make_logger


def make_redis_url(host, port, db):
    return f"redis://{host}:{port}/{db}"


cm_logger = make_logger(name=__name__)


class PoolManager:
    _POOLS = {}  # Object for saving connection pools

    # wrappers for properties that change the pool object
    def alters_pool(func):
        @wraps(func)
        def wrapper(self, val):
            old_key = self._key

            if old_key in PoolManager._POOLS and PoolManager._POOLS[old_key]["n"] is 1:
                self.close_pool(force=True)

            func(self, val)

            self._key = (self.host, self.port, self.db)
            if old_key == self._key:
                return
            elif None in self._key:
                self._pool = None
            else:
                self.init_pool()

        return wrapper

    def __init__(self, host=None, port=None, db=None):
        self._key = (host, port, db)
        self._host = host
        self._port = port
        self._db = db
        self.logger = make_logger("poolmanager:instance")
        self._pool = None
        self.init_pool()

    def init_pool(self):
        """ Initializes a connection pool or sets the pool
            member variable to a connection pool already opened
            by another object.

        """

        if None not in self._key:

            if self._key in PoolManager._POOLS:
                if self._pool is not PoolManager._POOLS[self._key]["pool"]:
                    PoolManager._POOLS[self._key]["n"] += 1
                    self._pool = PoolManager._POOLS[self._key]["pool"]
                    self.logger.info(
                        "Pool already instantiated. Setting pool to existing object"
                    )
                    self.logger.debug(PoolManager._POOLS)
                else:
                    self.logger.debug("Pool already instantiated")

            else:
                PoolManager._POOLS[self._key] = {}
                PoolManager._POOLS[self._key]["pool"] = redis.ConnectionPool(
                    host=self.host, port=self.port, db=self.db
                )

                PoolManager._POOLS[self._key]["n"] = 1
                self._pool = PoolManager._POOLS[self._key]["pool"]
                self.logger.debug("New connection pool created")

        else:
            self.logger.warning("Unable to create pool. Missing arguments.")
            self.logger.debug(f"Key: {self._key}")
            self._pool = None

    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        pass

    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, p):
        raise NotImplementedError("Pool cannot be set directly")

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def db(self):
        return self._db

    @host.setter
    @alters_pool
    def host(self, host):
        self._host = host

    @port.setter
    @alters_pool
    def port(self, port):
        self._port = port

    @db.setter
    @alters_pool
    def db(self, db):
        self._db = db

    @property
    def conn(self):
        if self._pool is None:
            self.logger.error("Unable to create client. No connection Pool")
            raise ValueError("No pool open in `PoolManager`")

        else:
            return redis.Redis(connection_pool=self.pool)

    @contextmanager
    def pipe(self, remove_client=True, execute_pipe=False):

        with self.conn.pipeline() as pipe:
            self.logger.debug("Pipeline opened")
            yield pipe
            if execute_pipe:
                self.logger.debug("Executing redis commands")
                pipe.execute()
        self.logger.debug("Pipeline closed")
        if remove_client:
            self._r = None

    def init_app(self, app):
        self.app = app
        self._host = app.config.get("REDIS_HOST", "localhost")
        self._port = app.config.get("REDIS_PORT", 6379)
        self._db = app.config.get("REDIS_DB", 0)
        self._key = (self._host, self._port, self._db)
        self.logger.debug(f"KEY: {self._key}")
        self.init_pool()

    def close_pool(self, force_conn=False, force=False):
        """Closes the connection pool (if one exists).


        """

        if self._pool is not None:
            try:
                if self.r is not None:
                    if force_conn or force:
                        del self.r

                    else:
                        self.logger.error(
                            "Pool in use by connection. Pool was not closed"
                        )
                        self.logger.debug(f"Connections Left: {PoolManager._POOLS}")
                        return False
            except AttributeError:
                pass

            if PoolManager._POOLS[self._key]["n"] == 1 or force:
                PoolManager._POOLS[self._key]["pool"].disconnect()
                self._pool = None
                del PoolManager._POOLS[self._key]
                self.logger.debug("Pool closed")
                try:
                    self.logger.debug(
                        f"Connections Left After Deletion: {PoolManager._POOLS[self._key]['n']}"
                    )

                except KeyError:
                    pass
                return True
            else:
                PoolManager._POOLS[self._key]["n"] -= 1
                self._pool = None
                self.logger.debug(
                    f'Pool remains open. Pool open in {PoolManager._POOLS[self._key]["n"]} other object(s)'
                )
                try:
                    self.logger.debug(
                        f"Connections Left After Removal: {PoolManager._POOLS[self._key]['n']}"
                    )
                except KeyError:
                    self.logger.debug("All connections closed")
                return False

        else:
            self.logger.warning("No pool instantiated")
            return False

    def copy(self):
        self._POOLS[self._key]["n"] += 1
        return copy.copy(self)

    @contextmanager
    def with_lock(self, key, pipe=False, timeout=None, sleep=0.1, blocking_timeout=5):
        r = self.conn
        lock = r.lock(key)
        lock.acquire
        yield r
        lock.release()





def global_poolman(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            poolman = g.poolman
        # Attribute error catches g not having poolman attribute
        # Runtime error catches g not existing (when tests are running)
        except (AttributeError,RuntimeError):
            poolman = PoolManager(host='localhost',port=6379, db=0)
        with poolman as r:
            return func(r, *args, **kwargs)
        poolman.close_pool()
    return wrapper


def global_pipe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            poolman = g.poolman
        # Attribute error catches g not having poolman attribute
        # Runtime error catches g not existing (when tests are running)
        except (AttributeError,RuntimeError):
            poolman = PoolManager(host='localhost',port=6379, db=0)

        with poolman.pipe() as pipe:
            return func(pipe, *args, **kwargs)
        poolman.close_pool()

    return wrapper

# Used to return the correct types when pulling a dictionary from redis
def map_dict_signature(d,signature):
    # 'beautiful' one liner. Maybe change to lambda to make it even more unreadable
    cm_logger.info(f'Dictionary {d} mapped by {signature}')
    return {key.decode('utf-8'):signature[key.decode('utf-8')](val.decode('utf-8')) for key,val in d.items()}


def return_signature(signature):
    def _return_signature(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            ret = func(*args,**kwargs)
            if isinstance(ret,dict):
                return map_dict_signature(ret,signature)
            else:
                raise TypeError('Function did not return dictionary')
        return wrapper
    return _return_signature