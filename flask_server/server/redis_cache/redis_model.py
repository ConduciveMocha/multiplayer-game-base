import redis


class RedisObject:
    REDIS = None

    @classmethod
    def init_redis(cls, *args, **kwargs):
        cls.REDIS = redis.Redis(*args, **kwargs)


class RedisModel(RedisObject):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


class RedisType(RedisObject):
    REDIS = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_entry(self):
        pass

    def set_entry(self):
        pass

    def clean(self):
        pass

    def make_entry(self):
        pass

    def delete_entry(self):
        pass
