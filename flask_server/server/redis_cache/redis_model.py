import redis


class RedisModel:
    REDIS = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
