import uuid
import time
import logging

from collections import namedtuple

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy import Column
from server.redis_cache.poolmanager import PoolManager
from server.logging import try_call, make_logger

logger = make_logger(__name__)


class RedisORMMeta(DefaultMeta):
    _REDIS_POOL = None

    @classmethod
    def create_cc_class(cls):
        class CacheFunc:
            def __init__(self, key, columns, redis_type="HASH"):
                self.key = key
                self.columns = columns
                self.redis_type

    def __new__(cls, name, bases, d):

        sup_return = super(cls, RedisORMMeta).__new__(cls, name, bases, d)
        print(cls)

        return sup_return

    def __init__(cls, name, bases, d):
        col_dict = {name: col for name, col in d.items() if isinstance(col, Column)}
        super(RedisORMMeta, cls).__init__(name, bases, d)

    def _make_redis_funcs(cls, debug=False):
        """
        Adds redis methods to class. Debug mode tries to define all functions.
        This should be called after super().__new__ in __new__. 

        """
        if not debug:
            cls._add_dict_to_r()
            cls._add_r_to_dict()
            cls._add_from_r()
            cls._add_to_r()
        else:
            logger.info(f"Adding redis functions in debug for {cls.__name__}")

            results = map(
                lambda f: try_call(f, debug_logger=logger),
                [
                    cls._add_dict_to_r(),
                    cls._add_r_to_dict(),
                    cls._add_from_r(),
                    cls._add_to_r(),
                ],
            )

            if all(x[1] for x in results):
                logger.info("Added all redis functions successfully")
            else:
                logger.info(
                    f"Redis functions added: {list(filter(lambda x: x[1], results))}"
                )
                logger.info(
                    f"Redis functions not added {list(filter(lambda x: not x[1], results))}"
                )

    @classmethod
    def keyname(cls, cachekey, extra_namespaces=None, prepend_extra=False):
        if extra_namespaces is None:
            return f"{cls.__name__}:{cachekey}"
        else:
            if prepend_extra:
                namespaces = extra_namespaces + [cls.__name__]
            else:
                namespaces = [cls.__name__] + extra_namespaces

            return f'{":".join(namespaces)}:{cachekey}'

    def _add_default_expiration_method(cls):
        try:
            expire_method, dt = cls.CACHE_EXPIRATION
        except AttributeError:
            expire_method, dt = "NORMAL", 3600

        if expire_method == "NORMAL":
            default_expire = lambda rconn, keyname: rconn.expire(keyname, dt)
        elif expire_method == "EXPIRE_AT":
            default_expire = lambda rconn, keyname: rconn.expireat(
                keyname, time.time() + dt
            )
        else:
            default_expire = None
        cls.default_expire = default_expire

    def _conn_method(cls, conn_type):
        try:
            default_conn_method = cls.CACHE_CONN_METHOD
        except AttributeError:
            pass

    def _add_dict_to_r(cls):
        if cls.CACHED and cls.CACHE_KEY:

            @classmethod
            def dict_to_r(cls, d, key=None):
                data_dict = {k: v for k, v in d if v in cls.CACHE_MODEL.columns}
                if key is None:
                    key = d[cls.CACHE_MODEL.key]

                extra_namespaces = kwargs.get("extra_namepaces", None)
                try:
                    cls._REDIS_POOL.conn.hmset(
                        cls.keyname(key, extra_namespaces), data_dict
                    )
                except Exception as e:
                    print(e)
                    print(type(e))

        else:

            @classmethod
            def dict_to_r(cls, *args, **kwargs):
                raise NotImplementedError(
                    f"Model class {cls.__name__} does not have CACHE settings defined"
                )

        cls.dict_to_r = dict_to_r

    def _add_r_to_dict(cls):
        if cls.CACHED and cls.CACHE_KEY:

            @classmethod
            def r_to_dict(cls, key, extra_namepaces=None, safe=False):
                data_dict = cls._REDIS_POOL.conn.hgetall(
                    cls.keyname(key, extra_namepaces)
                )
                if safe:
                    for name, _ in cls.CACHED:
                        if name not in data_dict:
                            raise ValueError("Redis record is incomplete")
                return data_dict

        else:

            @classmethod
            def r_to_dict(cls, *args, **kwargs):
                raise NotImplementedError(
                    f"Model class {cls.__name__} does not have CACHE settings defined"
                )

        cls.r_to_dict = r_to_dict

    def _add_to_r(cls):
        if cls.CACHED and cls.CACHE_KEY:

            def to_r(self, extra_namepaces=None):
                model_dict = self.__dict__
                try:
                    data_dict = {name: model_dict[name] for name, _ in cls.CACHED}
                    key = model_dict[cls.CACHE_KEY]
                    cls._REDIS_POOL.conn.hmset(
                        cls.keyname(key, extra_namepaces), data_dict
                    )
                except Exception as e:
                    print(e)
                    print(type(e))

        else:

            def to_r(self, *args, **kwargs):
                raise NotImplementedError(
                    f"Model class {cls.__name__} does not have CACHE settings defined"
                )

        cls.to_r = to_r

    def _add_from_r(cls):
        if cls.CACHED and cls.CACHE_KEY:

            @classmethod
            def from_r(cls, key, extra_namespaces=None):
                data_dict = cls._REDIS_POOL.conn.hgetall(
                    cls.keyname(key, extra_namespaces)
                )
                if data_dict:
                    try:
                        #! Use the column to coerce type if it becines a problem
                        data_dict[cls.CACHE_KEY[0]] = key
                        return cls(**data_dict)
                    except Exception as e:
                        print(e)
                        print(type(e))
                else:
                    return None

        else:

            @classmethod
            def from_r(cls, *args, **kwargs):
                raise NotImplementedError(
                    f"Model class {cls.__name__} does not have CACHE settings defined"
                )

        cls.from_r = from_r

    @classmethod
    def _set_redis_pool(cls, redis_pool):
        if isinstance(redis_pool, PoolManager):
            RedisORMMeta._REDIS_POOL = redis_pool

        else:
            raise TypeError("Redis pool is not a PoolManager")


RedisORMMeta.create_cc_class()
