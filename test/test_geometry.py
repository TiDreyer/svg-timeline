""" test cases for the classes defined in the geometry module """
import math

import pytest

from svg_timeline.vectors import Vector, COORD_TOLERANCE


def test_vector_equal():
    v_0_0 = Vector(0, 0)
    v_0_1 = Vector(0, 1)
    v_1_0 = Vector(1, 0)
    v_1_1 = Vector(1, 1)
    # obvious equal cases
    assert v_0_0 == v_0_0
    assert v_0_1 == v_0_1
    assert v_1_0 == v_1_0
    assert v_1_1 == v_1_1
    # obvious unequal cases
    assert v_0_0 != v_0_1
    assert v_0_0 != v_1_0
    assert v_0_0 != v_1_1
    assert v_0_1 != v_0_0
    assert v_1_0 != v_0_0
    assert v_1_1 != v_0_0
    # rounding errors
    one_ninth = 1 / 9
    one_tenth = 1 / 10
    assert Vector(0, 1 / 3) == Vector(0, one_ninth + one_ninth + one_ninth)
    assert Vector(0, 0.3) == Vector(0, one_tenth + one_tenth + one_tenth)
    # close cases
    below_tol = 0.99 * COORD_TOLERANCE
    above_tol = 1.01 * COORD_TOLERANCE
    assert v_0_0 == Vector(below_tol, below_tol)
    assert v_0_0 != Vector(below_tol, above_tol)
    assert v_0_0 != Vector(above_tol, below_tol)
    assert v_0_0 != Vector(above_tol, above_tol)


def test_vector_addition():
    assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)
    assert Vector(1, -2) + Vector(-3, 4) == Vector(-2, 2)


def test_vector_subtraction():
    assert Vector(1, 2) - Vector(3, 4) == Vector(-2, -2)
    assert Vector(1, -2) - Vector(-3, 4) == Vector(4, -6)


def test_vector_multiplication():
    # normal scaling
    assert Vector(1, 2) * 2 == Vector(2, 4)
    assert Vector(1, 2) * 3 == Vector(3, 6)
    assert Vector(2, 4) * 0.5 == Vector(1, 2)
    assert Vector(3, 6) / 3 == Vector(1, 2)
    assert Vector(-3, -6) / -3 == Vector(1, 2)
    # wrong type
    with pytest.raises(TypeError):
        _ = Vector(0, 0) * '7'
    # float and integer
    assert Vector(3, 6) * 7 == Vector(3, 6) * 7.0
    assert Vector(-3, -6) * 7 == Vector(-3, -6) * 7.0
    # magnitude zero vector
    assert Vector(0, 0) * 7 == Vector(0, 0)
    # left and right multiplicity
    assert Vector(3, 6) * 7 == 7 * Vector(3, 6)
    assert Vector(3, 6) * -7 == -7 * Vector(3, 6)
    # inversion
    assert Vector(0, 1) * -1 == Vector(0, -1)
    assert Vector(1, 0) * -1 == Vector(-1, 0)
    assert Vector(3, 6) * -1 == Vector(-3, -6)



def test_vector_magnitude():
    # zero length
    assert Vector(0, 0).mag == 0
    # one component
    assert Vector(0, 4).mag == 4
    assert Vector(0, -4).mag == 4
    assert Vector(3, 0).mag == 3
    assert Vector(-3, 0).mag == 3
    # 3^2 + 4^2 = 5^2
    assert Vector(3, 4).mag == 5
    assert Vector(-3, -4).mag == 5
    assert Vector(-4, 3).mag == 5


def test_vector_normalized():
    v_x_norm = Vector(1, 0)
    v_y_norm = Vector(0, 1)
    v_x_norm_neg = Vector(-1, 0)
    v_y_norm_neg = Vector(0, -1)
    # zero length
    with pytest.raises(ZeroDivisionError):
        _ = Vector(0, 0).normalized()
    # one component
    assert Vector(0, 4).normalized() == v_y_norm
    assert Vector(0, -4).normalized() == v_y_norm_neg
    assert Vector(0, 7).normalized() == v_y_norm
    assert Vector(0, -7).normalized() == v_y_norm_neg
    assert Vector(4, 0).normalized() == v_x_norm
    assert Vector(-4, 0).normalized() == v_x_norm_neg
    assert Vector(7, 0).normalized() == v_x_norm
    assert Vector(-7, 0).normalized() == v_x_norm_neg


def test_vector_orthogonal():
    v_up = Vector(0, -1)
    v_down = Vector(0, 1)
    v_left = Vector(-1, 0)
    v_right = Vector(1, 0)
    inv_sqrt2 = 1/math.sqrt(2)
    v_uv_left = Vector(-inv_sqrt2, -inv_sqrt2)
    v_uv_right = Vector(inv_sqrt2, -inv_sqrt2)
    v_down_left = Vector(-inv_sqrt2, inv_sqrt2)
    v_down_right = Vector(inv_sqrt2, inv_sqrt2)
    # clockwise
    assert v_up.orthogonal() == v_right
    assert v_right.orthogonal() == v_down
    assert v_down.orthogonal() == v_left
    assert v_left.orthogonal() == v_up
    assert v_uv_left.orthogonal() == v_uv_right
    assert v_uv_right.orthogonal() == v_down_right
    assert v_down_right.orthogonal() == v_down_left
    assert v_down_left.orthogonal() == v_uv_left
    # counterclockwise
    assert v_up.orthogonal(ccw=True) == v_left
    assert v_left.orthogonal(ccw=True) == v_down
    assert v_down.orthogonal(ccw=True) == v_right
    assert v_right.orthogonal(ccw=True) == v_up
    assert v_uv_right.orthogonal(ccw=True) == v_uv_left
    assert v_uv_left.orthogonal(ccw=True) == v_down_left
    assert v_down_left.orthogonal(ccw=True) == v_down_right
    assert v_down_right.orthogonal(ccw=True) == v_uv_right
