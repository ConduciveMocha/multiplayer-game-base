import pytest
from server.game.geometric_types.vector import Vector
from server.game.geometric_types.rectangle import Rectangle
from server.logging import make_logger, log_test

logger = make_logger(__name__)


@log_test(logger)
def test_rectangle_eq():
    r1 = Rectangle.from_components(1, 2, 3, 4)
    r2 = Rectangle(Vector(1, 2), Vector(3, 4))
    r3 = Rectangle(Vector(0, 0), Vector(0, 0))
    assert r1 == r2
    assert r1 != r3


@log_test(logger)
def test_rectangle_area():
    test_dim_x, test_dim_y = 3, 4
    test_area = test_dim_x * test_dim_y
    dim = Vector(3, 4)
    pos1 = Vector(1, 2)
    pos2 = Vector(6, 4)

    r1 = Rectangle(pos1, Vector(test_dim_x, test_dim_y))
    r2 = Rectangle(pos2, Vector(test_dim_x, test_dim_y))

    assert r1.area() == r2.area()
    assert r1.area() == test_area
    assert r2.area() == test_area


@log_test(logger)
def test_rectangle_collides():
    r1 = Rectangle.from_components(10, 10, 5, 5)
    r2 = Rectangle.from_components(12, 12, 4, 4)
    r3 = Rectangle.from_components(12, 10, 2, 10)
    r4 = Rectangle.from_components(6, 10, 4, 20)
    assert r1.collides(r2)
    assert r2.collides(r1)
    assert r3.collides(r1)
    assert r1.collides(r1)
    assert r1.collides(r4)
