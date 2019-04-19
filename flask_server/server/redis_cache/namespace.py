from server.redis_cache.redisobject import (
    RedisObject,
    NoRedisConnection,
    ExpirationPolicy,
)


class Namespace(RedisObject):
    def __getattr__(self, name):
        try:
            if name in self.__dict__["children"]:
                return self.children[name]
        except KeyError:
            pass

    def __setattr__(self, name, value):
        try:
            if name in self.__dict__["children"]:
                self.remove_child(name)
                self.add_child(value)
            else:
                return super().__setattr__(name, value)

        except KeyError:
            return super().__setattr__(name, value)


class BaseNamespace(Namespace):
    def __init__(self, pool_manager, expiration_policy=None):
        self._pool_manager = pool_manager
        super().__init__("", parent=None, children=None)
        self._r = self._pool_manager.conn
        if expiration_policy is None:
            self.expiration_policy = ExpirationPolicy()

    @property
    def pool_manager(self):
        return self._pool_manager

    @pool_manager.setter
    def pool_manager(self, pool_manager):
        if self.pool_manager is not None:
            self.pool_manager.close_pool()
        self._pool_manager = pool_manager
        self.r = self.pool_manager.conn

    def set_parent(self, parent):
        raise NotImplementedError("BaseNamespace cannot have a parent")

