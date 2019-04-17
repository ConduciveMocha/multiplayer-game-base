class Singleton(type):
    """
    An metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """
    _instances = {}
    call_counts = 0

    def __new__(cls, clsname, superclasses, attributedict):
        print('__new__')
        print("clsname: ", clsname)
        print("superclasses: ", superclasses)
        print("attributedict: ", attributedict)
        print()
        return type.__new__(cls, clsname, superclasses, attributedict)

    def __call__(cls, *args, **kwargs):
        cls.call_counts += 1
        print('calls: ', cls.call_counts)
        print('__call__')
        key = (args, tuple(sorted(kwargs.items())))
        print('key', key)
        print('cls', cls)
        if cls not in cls._instances:
            print('cls not in cls._instances')
            cls._instances[cls] = {}
        if key not in cls._instances[cls]:
            print('key not in cls._instances[cls]')
            cls._instances[cls][key] = super(
                Singleton, cls).__call__(*args, **kwargs)
        print('instances', cls._instances)
        print()
        return cls._instances[cls][key]

    def __init__(cls, clsname, superclasses, attributedict):
        print('__init__')
        print("clsname: ", clsname)
        print("superclasses: ", superclasses)
        print("attributedict: ", attributedict)
        print()


class Test(metaclass=Singleton):
    def __init__(self, val=None):
        self.val = val if val else 0
        self.name = self.__class__.call_counts

    def modify(self, val):
        self = self.__class__(val)

    def print_name(self):
        print('calling', self.name)


x = Test()
x.print_name()
y = Test()
y.print_name()
z = Test(5)
z.print_name()
a = Test(5)
a.print_name()
a.modify(6)

print(a.val)
print(a == z)
