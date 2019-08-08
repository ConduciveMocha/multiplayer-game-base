import pytest
from math import hypot
from server.game.geometric_types.vector import Vector
from server.logging import make_test_logger, log_test

logger = make_test_logger(__name__)


@log_test(logger)
def test_vector_properties():
    test_x, test_y = 5, 6
    v = Vector(test_x, test_y)

    assert v.x == test_x
    assert v.y == test_y
    assert v.mag == hypot(test_x, test_y)

    v0 = Vector(1, 0)
    assert v0.mag == 1
    assert v0.theta == 0


@log_test(logger)
def test_vector_eq():
    test_x, test_y = 5, 6
    v1 = Vector(test_x, test_y)
    assert v1 == Vector(test_x, test_y)
    assert v1 != Vector(test_x, -1)


@log_test(logger)
def test_vector_arith():
    test_x1, test_y1 = 2, 3
    test_x2, test_y2 = 5, 6
    v1, v2 = Vector(test_x1, test_y1), Vector(test_x2, test_y2)

    # Addition test vectors
    v1pv2 = v1 + v2
    v2pv1 = v2 + v1

    # Asserts addition returns vectors
    assert isinstance(v1pv2, Vector)
    assert isinstance(v2pv1, Vector)

    # Assert addition acts component-wise
    assert v1pv2.x == test_x1 + test_x2
    assert v1pv2.y == test_y1 + test_y2

    # Asserts that addition is commutative
    assert v1pv2 == v2pv1

    # Subtraction test vector
    v1mv2 = v1 - v2

    # Asserts subtraction returns vectors
    assert isinstance(v1mv2, Vector)

    # Assert subtraction acts component-wise
    assert v1mv2.x == test_x1 - test_x2
    assert v1mv2.y == test_y1 - test_y2

    # Multiplication test vectors
    v1t10 = v1 * 10
    tentv1 = 10 * v1

    # Asserts multiplication returns a Vector
    assert isinstance(v1t10, Vector)
    assert isinstance(tentv1, Vector)

    # Asserts multiplication is applied component-wise
    assert v1t10.x == test_x1 * 10
    assert v1t10.y == test_y1 * 10

    # Asserts scalar multiplication is communative
    assert v1t10 == tentv1
