class NoRedisConnection(BaseException):
    pass


class ExpirationPolicy:
    EXPIRE_FUNCS = {"TIMER": "expire", "INTERVAL": "expireat"}

    def __init__(self, name=None, expire_type=None, expire_interval=None):

        self.name = name
        self.expire_type = expire_type if expire_type else "TIMER"
        self.expire_interval = None
        self._r = None
        self._policy_owner = None

    def dispatch(self, key, *args, **kwargs):
        raise NotImplementedError

    def set_expiration(self, key):
        if self.r:
            if expire_interval:
                self.r.__getattribute__(EXPIRE_FUNCS[self.expire_type])(
                    key, self.expire_interval
                )
            self.dispatch(key)
        else:
            raise NoRedisConnection

    @property
    def policy_owner(self):
        return self._policy_owner

    @policy_owner.setter
    def policy_owner(self, policy_owner):
        if policy_owner.expiration_policy is not self:
            raise Exception
        else:
            self._policy_owner(policy_owner)
            self._r = self._policy_owner.r

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        if self.policy_owner is None:
            self.r = r
        elif hasattr(self.policy_owner, r) and self.policy_owner.r is r:
            self._r = r
        else:
            raise AttributeError

    def recurse(self, func):
        stack = [self.policy_owner]
        while len(stack) > 0:
            top = stack.pop()
            for c in top.children:
                if c.expiration_policy is None or c.expiration_policy is self:
                    stack.push(c)

            yield func(top)


class RedisObject:
    def __init__(self, name, parent=None, children=None, expiration_policy=None):
        self.children = children if children else {}
        self._parent = parent
        self._name = name
        self._key = name
        self._r = None
        self._expiration_policy = (
            expiration_policy if expiration_policy else ExpirationPolicy()
        )

    def add_child(self, child, force=False):
        current_child = self.children.get(child.name, None)
        if child.parent is None:
            child.set_parent(self)

        elif child.parent is not self:
            if force:
                child.parent.remove_child(self.children[child.name])
                child.set_parent(self)
            else:
                raise Exception
        if current_child is None:

            self.children.update({child.name: child})
        elif current_child is not child:
            if force:
                self.remove_child(child.name)
                self.children.update({child.name, child})
            else:
                raise Exception

    def remove_child(self, child, force=False):
        if force and not isinstance(child, str):
            child = child.name

        if isinstance(child, str):
            try:
                child_obj = self.children[child]
            except KeyError:
                raise Exception

            child_obj.parent = None
            del self.children[child_obj]
            return child_obj

        elif child.name not in self.children:
            raise Exception

        elif self.children[child.name] is not child:
            raise Exception

        else:
            child.parent = None
            del self.children[child.name]
            return child

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        if r is not None and self.r is not r:
            self._r = r
            if self.children:
                for ch in self.children.values():
                    ch.r = self._r

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self.parent is None:
            self._name = name
            self._key = name
        else:
            if name in self.parent.children:
                raise Exception
            else:
                self._name = name
                self._key = f"{self.parent.key}:{self.name}"

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        raise NotImplementedError("Cannot set key")

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self.set_parent(parent)

    def set_parent(self, parent):

        if parent is self.parent:
            return

        if self.parent:
            self.parent.remove_child(self)
            self.r = None
        self._parent = parent
        if self.parent is None:
            self._key = self.name
            self.r = None
        else:
            if self.name not in parent.children:
                self.parent.add_child(self)
            if self.parent.key is "":
                self._key = self.name
            else:
                self._key = f"{self._parent.key}:{self.name}"
            self.r = parent.r

    @property
    def expiration_policy(self):
        if self._expiration_policy:
            return self._expiration_policy
        else:
            return self.parent.expiration_policy

    @expiration_policy.setter
    def expiration_policy(self, expiration_policy):
        if self.expiration_policy.policy_owner is self:
            self._expiration_policy = expiration_policy
