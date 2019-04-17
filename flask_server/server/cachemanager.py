import logging
import redis
from contextlib import contextmanager
from functools import wraps


def make_redis_url(host, port, db):
    return f'redis://{host}:{port}/{db}'


cm_logger = logging.getLogger(name=__name__)


class PoolManager():
    _POOLS = {}  # Object for saving connection pools

    # wrappers for properties that change the pool object
    def alters_pool(func):
        @wraps(func)
        def wrapper(self, val):
            old_key = self._key

            if old_key in PoolManager._POOLS and PoolManager._POOLS[old_key]['n'] is 1:
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

    def __init__(self, host=None, port=None, db=None, logger=None):
        self._key = (host, port, db)
        self._host = host
        self._port = port
        self._db = db
        self.logger = logger if logger else cm_logger
        self._pool = None
        self.r = None
        self.init_pool()

    def init_pool(self):
        """ Initializes a connection pool or sets the pool
            member variable to a connection pool already opened
            by another object.

        """

        if None not in self._key:

            if self._key in PoolManager._POOLS:
                if self._pool is not PoolManager._POOLS[self._key]['pool']:
                    PoolManager._POOLS[self._key]['n'] += 1
                    self._pool = PoolManager._POOLS[self._key]['pool']
                    self.logger.info(
                        'Pool already instantiated. Setting pool to existing object')
                    self.logger.debug(PoolManager._POOLS)
                else:
                    self.logger.debug('Pool already instantiated')

            else:
                PoolManager._POOLS[self._key] = {}
                PoolManager._POOLS[self._key]['pool'] = redis.ConnectionPool(
                    host=self.host, port=self.port, db=self.db)
                PoolManager._POOLS[self._key]['n'] = 1
                self._pool = PoolManager._POOLS[self._key]['pool']
                self.logger.debug('New connection pool created')

        else:
            self.logger.warn('Unable to create pool. Missing arguments.')
            self._pool = None

    def __enter__(self):
        return self.conn()

    def __exit__(self, type, value, traceback):
        self.close()

    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, p):
        raise NotImplementedError('Pool cannot be set directly')

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

    def conn(self):
        if self._pool is None:
            self.logger.error('Unable to create client. No connection Pool')
            raise ValueError('No pool open in `PoolManager`')
        elif self.r is None:
            self.logger.debug('New redis client instantiated')
            self.r = redis.Redis(connection_pool=self._pool)
        return self.r

    def close(self):

        if self.r:
            del self.r
            self.r = None
            self.logger.debug('Redis client removed')
        else:
            self.logger.warn('No redis client open')

    @contextmanager
    def pipe(self, remove_client=True, execute_pipe=False):

        with self.conn().pipeline() as pipe:
            self.logger.debug('Pipeline opened')
            yield pipe
            if execute_pipe:
                self.logger.debug('Executing redis commands')
                pipe.execute()
        self.logger.debug('Pipeline closed')
        if remove_client:
            self.close()

    @alters_pool
    def init_app(self, app):
        self._host = app.config.get('REDIS_HOST', 'localhost')
        self._port = app.config.get('REDIS_PORT', 6379)
        self._db = app.config.get('REDIS_DB', 0)
        self._key = (self._host, self._port, self._db)

    def close_pool(self,  force_conn=False, force=False):
        """Closes the connection pool (if one exists).


        """
        if self._pool is not None:
            if self.r is not None:
                if force_conn or force:
                    del self.r
                else:
                    self.logger.error(
                        'Pool in use by another object. Pool was not closed')
                    return

            if PoolManager._POOLS[self._key]['n'] == 1 or force:
                PoolManager._POOLS[self._key]['pool'].disconnect()
                self._pool = None
                del PoolManager._POOLS[self._key]
                self.logger.debug('Pool closed')
            else:
                PoolManager._POOLS[self._key]['n'] -= 1
                self._pool = None
                self.logger.debug(
                    f'Pool remains open. Pool open in {PoolManager._POOLS[self._key]["n"]} other object(s)')

        else:
            self.logger.warn('No pool instantiated')

    def use(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self as r:
                ret = func(r, *args, **kwargs)
            return ret
        return wrapper


poolman = PoolManager()
