from flask_sqlalchemy.model import DefaultMeta

from sqlalchemy.inspection import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy import Column
from server.redis_cache.cachemanager import PoolManager

class RedisORMMeta(DefaultMeta):
    _REDIS_POOL = None
    def __new__(cls,name,bases,d):
        col_dict = {name:col for name,col in d.items() if isinstance(col, Column)}
        try:
            # Catches model parent classes
            if not col_dict:
                d['CACHED'] = None

            # Raise error if both defined since it will cause undetermined behavior
            elif 'CACHED' in d and 'NOT_CACHED' in d:
                raise AttributeError('Canot define `CACHED` and `NOT_CACHED`')
            
            elif 'CACHED' in d:
                # ensures cached is iterable
                if isinstance(d['CACHED'], list):
                    cached = d['CACHED']
                else:
                    cached = [d['CACHED']]
                
                d['CACHED'] = list(filter(lambda x: x[0] in cached or x[1] in cached, col_dict.items()))
                
                
            elif 'NOT_CACHED' in d:
                if isinstance(d['NOT_CACHED'], list):
                    ncached = d['NOT_CACHED']
                else:
                    ncached = [d['NOT_CACHED']]
                d['CACHED'] = list(filter(lambda x: x[0] not in ncached and x[1] not in ncached, col_dict.items()))
            else:
                d['CACHED'] = None

        except KeyError as e:
            print(e)
            raise AttributeError('Column not defined in model')

        # Column dict not defined
        if col_dict is None or d['CACHED'] is None:
            d['CACHED'] = None
            d['CACHE_KEY'] = None

        # d['CACHED] and CACHE_KEY defined
        elif 'CACHE_KEY' in d:
            if isinstance(d['CACHE_KEY'], str):
                try:
                    d['CACHE_KEY'] = (d['CACHE_KEY'],col_dict[d['CACHE_KEY']])
                except KeyError:
                    raise AttributeError('CACHE_KEY column not defined in model')
            
            elif isinstance(d['CACHE_KEY'],Column):
                try:
                    d['CACHE_KEY'] = next(filter(lambda x: x[1] is d['CACHE_KEY'], col_dict.items()))
                except IndexError:
                    raise AttributeError('CacheKey Column not defined in model')
            else:
                raise TypeError('CACHE_KEY must have type str or Column')

        # Automatically assing 'CACHE_KEY'
        else:
            try:
                d['CACHE_KEY'] = next(filter(lambda x: not x[1].primary_key, col_dict.items()))
            except (StopIteration, AttributeError) as e:
                raise AttributeError('Could not auto-assign CACHE_KEY. Define a CACHE_KEY in the model class')
        
        return super(cls,RedisORMMeta).__new__(cls,name,bases,d)

    s
    
    def __init__(cls,name,bases,d):
        super(RedisORMMeta,cls).__init__(name,bases,d)
        cls._make_redis_func()
    
    def _make_redis_func(cls):
        pass
        # try:
        #     inspect(cls)
        # except NoInspectionAvailable:
        #     def cache(self):
        #         raise NotImplementedError('Not implemented for this class')
        #     cls.cache = cache
        #     return    
        # def cache(self):
        #     try:
                
                
        #         redis_dict = {att:self.__dict__[att] for att in self.CACHED}
        #         # print(RedisORMMeta._REDIS_POOL)
        #         # print(cls.__name__,d['CACHE_KEY'])
        #         # print(f'{cls.__name__}:{d['CACHE_KEY']}')
        #         # print(d)
        #         RedisORMMeta._REDIS_POOL.conn.hmset(f'{cls.__name__}:{d['CACHE_KEY']}', redis_dict)
        #     except KeyError:
        #         raise AttributeError(f'Must define instance variables ({",".join(self.CACHED)}) to persist to redis')
        #     except AttributeError:
        #         raise AttributeError('Redis PoolManager not bound. Use `set_redis_pool(PoolManager)` to instantiate.')
        # cls.cache = cache
    
    @classmethod
    def _set_redis_pool(cls,redis_pool):
        if isinstance(redis_pool,PoolManager):
            RedisORMMeta._REDIS_POOL = redis_pool
            
        else:
            raise TypeError('Redis pool is not a PoolManager')