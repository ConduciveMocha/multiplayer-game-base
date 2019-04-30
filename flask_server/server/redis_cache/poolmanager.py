import logging
import copy
import redis
from redis.lock import Lock
from contextlib import contextmanager
from functools import wraps

from flask import g, _app_ctx_stack, current_app

from server.logging import make_logger


class PoolManager:

    _POOLS = {}  # Object for saving connection pools

    def __init__(self, host=None, port=None, db=None):
        self._key = (host, port, db)
        self._host = host
        self._port = port
        self._db = db
        self.logger = make_logger("poolmanager:instance")
        self._pool = None
        self.init_pool()

    # ---SETUP/TEARDOWN FUNCTIONS---

    # TODO: Add settings for default lock behavior
    def init_pool(self):
        """Initializes the connection pool with the specified host,port and db
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
            self.logger.warn("Unable to create pool. Missing arguments.")
            self.logger.debug(f"Key: {self._key}")
            self._pool = None

    def close_pool(self, force_conn=False, force=False):
        """Closes the connection pool (if open)
        
        Keyword Arguments:
            force_conn {bool} -- Forces close any open connections ( (default: {False})
            force {bool} -- Forces close the connection pool (default: {False})
        
        Returns:
            [bool] -- Returns True if the connection pool was closed
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

    def init_app(self, app):
        """Initializes the PoolManager object with settings from a flask app
        
        Arguments:
            app {Flask} -- A flask app
        """
        self.app = app
        self._host = app.config.get("REDIS_HOST", "localhost")
        self._port = app.config.get("REDIS_PORT", 6379)
        self._db = app.config.get("REDIS_DB", 0)
        self._key = (self._host, self._port, self._db)
        self.logger.debug(f"KEY: {self._key}")
        self.init_pool()

    # --------------------------------------------------------------------------------

    # ---PROPERTIES---
    def alters_pool(func):
        """Decorator for property setters that modify connection pool attributes. Before
            the wrapped function is called, the pool is closed (if it exists). Afterward,
            init_pool is called with the new settings 
        
        Arguments:
            func {function} -- Wrapped funtion (property setter)
        
        Returns:
            [function] -- Wrapped function
        """

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

    # =HOST=
    @property
    def host(self):
        return self._host

    @host.setter
    @alters_pool
    def host(self, host):
        self._host = host

    # =PORT=
    @property
    def port(self):
        return self._port

    @port.setter
    @alters_pool
    def port(self, port):
        self._port = port

    @property
    def db(self):
        return self._db

    @db.setter
    @alters_pool
    def db(self, db):
        self._db = db

    # =POOL=
    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, p):
        raise NotImplementedError("Pool cannot be set directly")

    # ? Refactor this?
    # =CONN=
    @property
    def conn(self):
        if self._pool is None:
            self.logger.error("Unable to create client. No connection Pool")
            raise ValueError("No pool open in `PoolManager`")

        else:
            return redis.Redis(connection_pool=self.pool, decode_responses=True)

    # --------------------------------------------------------------------------------

    # ---CONTEXT MANAGERS---
    # ? Refactor this out
    # Allows the object to be used as a context manager
    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        pass

    @contextmanager
    def pipe(self, remove_client=True, execute_pipe=False):
        """Context manager for using a pipe from the connection pool
        
        Keyword Arguments:
            remove_client {bool} -- If True, removes r from object after call (deprecated) (default: {True})
            execute_pipe {bool} -- If True, pipe.execute is called during cleanup (default: {False})
        """
        with self.conn.pipeline() as pipe:
            self.logger.debug("Pipeline opened")
            yield pipe
            if execute_pipe:
                self.logger.debug("Executing redis commands")
                pipe.execute()
        self.logger.debug("Pipeline closed")
        if remove_client:
            self._r = None

    @contextmanager
    def with_lock(self, key, pipe=False, timeout=None, sleep=0.1, blocking_timeout=5):
        """Context manager for acquiring a lock from the PoolManager
        
        Arguments:
            key {str} -- Name of key that will be locked
        
        Keyword Arguments:
            pipe {bool} -- If True, a pipe object will be returned  (default: {False})
            timeout {int} -- Timeout for acquiring the lock (default: {None})
            sleep {float} -- Duration of sleep between acquisition attemps (default: {0.1})
            blocking_timeout {int} -- Timeout for the redis client to be blocked (default: {5})
        """
        connection_method = self.pipe if pipe else self.conn

        with connection_method as r:
            lock = r.lock(
                key, timeout=timeout, sleep=sleep, blocking_timeout=blocking_timeout
            )
            lock.acquire()
            yield r
            lock.release()

    # --------------------------------------------------------------------------------


def global_poolman(func):
    """Decorator for passing a connection from the app global PoolManager to the wrapped function
    
    Arguments:
        func {function} -- Function that uses a redis connection
    
    Returns:
        [type] -- The return value of the wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        poolman = g.poolman
        with poolman as r:
            return func(r, *args, **kwargs)

    return wrapper


def global_pipe(func):
    """Decorator for passing a pipe from the app global PoolManager to the wrapped function
    
    Arguments:
        func {function} -- Function that uses a redis connection
    
    Returns:
        [type] -- The return value of the wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        poolman = g.poolman
        with poolman.pipe() as pipe:
            return func(pipe, *args, **kwargs)

    return wrapper

