from math import sqrt, hypot, atan
from server.game.geometric_types.vector import Vector


class Rectangle:
    def __init__(self, pos, dim):
        self.pos = pos
        if dim.x >= 0 and dim.y >= 0:
            self._dim = dim
        else:
            raise ValueError("Rectangle Dimension cannot be negative")

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return self.pos == other.pos and self.dim == other.dim
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_components(cls, posx, posy, dimx, dimy):
        pos = Vector(posx, posy)
        dim = Vector(dimx, dimy)
        return cls(pos, dim)

    @property
    def dim(self):
        return self._dim

    @dim.setter
    def dim(self, dim):
        if dim.x >= 0 and dim.y >= 0:
            self._dim = dim
        else:
            raise ValueError("Rectangle Dimension Cannot Be Negative")

    def area(self):
        return self.dim.x * self.dim.y

    def contains_point(self, pt):
        return (self.pos.x <= pt.x <= self.pos.x + self.dim.x) and (
            self.pos.y <= pt.y <= self.pos.y + self.dim.y
        )

    def corner_points(self):
        return (
            self.pos,
            self.pos + self.dim.x_vect(),
            self.pos + self.dim,
            self.pos + self.dim.y_vect(),
        )

    # Helper function for collides method to avoid infinite recursion
    # called on `other`
    def _collides(self, other):
        for pt in self.corner_points():
            if other.contains_point(pt):
                return True
        if (
            other.pos.x <= self.pos.x <= other.dim.x + other.pos.x
            and self.pos.y <= other.pos.y
            and self.pos.y + self.dim.y >= other.pos.y + other.dim.y
        ):
            return True
        else:
            return False

    def collides(self, other):
        return self._collides(other) or other._collides(self)
