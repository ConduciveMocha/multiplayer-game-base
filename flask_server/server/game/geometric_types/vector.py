from math import cos, sin, hypot, sqrt, atan


class Vector:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __composite_values__(self):
        return self._x, self._y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def mag(self):
        return hypot(self.x, self.y)

    @mag.setter
    def mag(self, mag):
        mag = self.mag
        self._x = cos(self.theta) * mag
        self._y = sin(self.theta) * mag

    @property
    def theta(self):
        return atan(self.y / self.x)

    @theta.setter
    def theta(self, rads):
        mag = self.mag
        self._x = mag * cos(rads)
        self._y = mag * sin(rads)

    def x_vect(self):
        return Vector(self.x, 0)

    def y_vect(self):
        return Vector(0, self.y)

    def __add__(self, other):
        return Vector(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        return Vector(self._x - other.x, self._y - other.y)

    def __iadd__(self, other):
        return Vector(self._x + other.x, self._y + other.y)

    def __isub__(self, other):
        return Vector(self._x - other.x, self._y - other.y)

    def __mul__(self, mag):
        return Vector(self._x * mag, self._y * mag)

    def __rmul__(self, mag):
        return self.__mul__(mag)

    def __imul__(self, mag):
        return mag * self

    def __str__(self):
        return f"<{self.x},{self.y}>"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False

        return other.x == self.x and other.y == self.y

    def __ne__(self, other):
        return not self.__eq__(other)

