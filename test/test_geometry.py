""" test cases for the classes defined in the geometry module """
import math

import pytest

from timeliner.geometry import Canvas, CanvasPoint, CanvasVector, COORD_TOLERANCE


def test_point_in_canvas():
    canvas = Canvas(100, 100)
    # corners
    assert CanvasPoint(0, 0) in canvas
    assert CanvasPoint(100, 100) in canvas
    assert CanvasPoint(100, 0) in canvas
    assert CanvasPoint(0, 100) in canvas
    # borders
    assert CanvasPoint(50, 0) in canvas
    assert CanvasPoint(50, 100) in canvas
    assert CanvasPoint(100, 50) in canvas
    assert CanvasPoint(0, 50) in canvas
    # inside
    assert CanvasPoint(30, 30) in canvas
    assert CanvasPoint(50, 50) in canvas
    assert CanvasPoint(99, 30) in canvas
    assert CanvasPoint(99.9999, 30) in canvas
    # outside
    assert CanvasPoint(-1, 50) not in canvas
    assert CanvasPoint(50, -30) not in canvas
    assert CanvasPoint(101, 50) not in canvas
    assert CanvasPoint(50, 130) not in canvas
    assert CanvasPoint(50, 100.0001) not in canvas


def test_point_equal():
    p_0_0 = CanvasPoint(0, 0)
    p_0_1 = CanvasPoint(0, 1)
    p_1_0 = CanvasPoint(1, 0)
    p_1_1 = CanvasPoint(1, 1)
    # obvious equal cases
    assert p_0_0 == p_0_0
    assert p_0_1 == p_0_1
    assert p_1_0 == p_1_0
    assert p_1_1 == p_1_1
    # obvious unequal cases
    assert p_0_0 != p_0_1
    assert p_0_0 != p_1_0
    assert p_0_0 != p_1_1
    assert p_0_1 != p_0_0
    assert p_1_0 != p_0_0
    assert p_1_1 != p_0_0
    # rounding errors
    one_ninth = 1 / 9
    one_tenth = 1 / 10
    assert CanvasPoint(0, 1/3) == CanvasPoint(0, one_ninth+one_ninth+one_ninth)
    assert CanvasPoint(0, 0.3) == CanvasPoint(0, one_tenth+one_tenth+one_tenth)
    # close cases
    below_tol = 0.99 * COORD_TOLERANCE
    above_tol = 1.01 * COORD_TOLERANCE
    assert p_0_0 == CanvasPoint(below_tol, below_tol)
    assert p_0_0 != CanvasPoint(below_tol, above_tol)
    assert p_0_0 != CanvasPoint(above_tol, below_tol)
    assert p_0_0 != CanvasPoint(above_tol, above_tol)


def test_vector_init():
    a_point = CanvasPoint(4, 6)
    a_tuple = (4, 6)
    b_point = CanvasPoint(-3.5, -7.89)
    b_tuple = (-3.5, -7.89)
    assert CanvasVector(a_point, b_point) == CanvasVector(a_tuple, b_tuple)
    assert CanvasVector(a_point, b_point) == CanvasVector(a_point, b_tuple)
    assert CanvasVector(a_point, b_point) == CanvasVector(a_tuple, b_point)


def test_vector_equal():
    assert CanvasVector((0, 0), (1, 1)) == CanvasVector((0, 0), (1, 1))
    assert CanvasVector((1, 1), (0, 0)) == CanvasVector((1, 1), (0, 0))
    assert CanvasVector((1, 1), (1, 1)) == CanvasVector((1, 1), (1, 1))
    assert CanvasVector((0, 0), (0, 0)) != CanvasVector((1, 1), (1, 1))
    assert CanvasVector((0, 0), (1, 1)) != CanvasVector((1, 1), (0, 0))


def test_vector_in_canvas():
    canvas = Canvas(100, 100)
    in_point_a = (30, 30)
    in_point_b = (50, 50)
    out_point_a = (-33, 50)
    out_point_b = (33, 120)
    # inside
    assert CanvasVector(in_point_a, in_point_a) in canvas
    assert CanvasVector(in_point_a, in_point_b) in canvas
    assert CanvasVector(in_point_b, in_point_a) in canvas
    assert CanvasVector(in_point_b, in_point_b) in canvas
    # outside
    assert CanvasVector(out_point_a, in_point_b) not in canvas
    assert CanvasVector(out_point_a, out_point_b) not in canvas
    assert CanvasVector(in_point_a, out_point_b) not in canvas
    assert CanvasVector(out_point_b, out_point_a) not in canvas


def test_vector_multiplication():
    # normal scaling
    assert CanvasVector((0, 0), (1, 2)) * 2 == CanvasVector((0, 0), (2, 4))
    assert CanvasVector((0, 0), (1, 2)) * 3 == CanvasVector((0, 0), (3, 6))
    assert CanvasVector((0, 0), (2, 4)) * 0.5 == CanvasVector((0, 0), (1, 2))
    assert CanvasVector((0, 0), (3, 6)) / 3 == CanvasVector((0, 0), (1, 2))
    assert CanvasVector((0, 0), (-3, -6)) / -3 == CanvasVector((0, 0), (1, 2))
    # wrong type
    with pytest.raises(TypeError):
        _ = CanvasVector((0, 0), (0, 0)) * '7'
    # float and integer
    assert CanvasVector((0, 0), (3, 6)) * 7 == CanvasVector((0, 0), (3, 6)) * 7.0
    assert CanvasVector((3, 6), (0, 0)) * 7 == CanvasVector((3, 6), (0, 0)) * 7.0
    # magnitude zero vectors
    assert CanvasVector((0, 0), (0, 0)) * 7 == CanvasVector((0, 0), (0, 0))
    assert CanvasVector((3, 6), (3, 6)) * 7 == CanvasVector((3, 6), (3, 6))
    assert CanvasVector((0, 0), (0, 0)) * 7 != CanvasVector((3, 6), (3, 6))
    # left and right multiplicity
    assert CanvasVector((0, 0), (3, 6)) * 7 == 7 * CanvasVector((0, 0), (3, 6))
    assert CanvasVector((3, 6), (0, 0)) * 7 == 7 * CanvasVector((3, 6), (0, 0))
    assert CanvasVector((0, 0), (3, 6)) * -7 == -7 * CanvasVector((0, 0), (3, 6))
    assert CanvasVector((3, 6), (0, 0)) * -7 == -7 * CanvasVector((3, 6), (0, 0))
    # inversion
    assert CanvasVector((0, 0), (0, 1)) * -1 == CanvasVector((0, 0), (0, -1))
    assert CanvasVector((0, 0), (1, 0)) * -1 == CanvasVector((0, 0), (-1, 0))
    assert CanvasVector((0, 0), (3, 6)) * -1 == CanvasVector((0, 0), (-3, -6))



def test_vector_magnitude():
    # zero length
    assert CanvasVector((0, 0), (0, 0)).mag == 0
    assert CanvasVector((3, 4), (3, 4)).mag == 0
    # one component
    assert CanvasVector((0, 0), (0, 4)).mag == 4
    assert CanvasVector((0, 4), (0, 0)).mag == 4
    assert CanvasVector((0, 0), (3, 0)).mag == 3
    assert CanvasVector((3, 0), (0, 0)).mag == 3
    # 3^2 + 4^2 = 5^2
    assert CanvasVector((0, 0), (3, 4)).mag == 5
    assert CanvasVector((3, 4), (0, 0)).mag == 5
    assert CanvasVector((6, 7), (10, 10)).mag == 5
    assert CanvasVector((10, 10), (6, 7)).mag == 5


def test_vector_normalized():
    v_x_norm = CanvasVector((0, 0), (1, 0))
    v_y_norm = CanvasVector((0, 0), (0, 1))
    v_x_norm_neg = CanvasVector((0, 0), (-1, 0))
    v_y_norm_neg = CanvasVector((0, 0), (0, -1))
    # zero length
    with pytest.raises(ZeroDivisionError):
        _ = CanvasVector((0, 0), (0, 0)).normalized()
    with pytest.raises(ZeroDivisionError):
        _ = CanvasVector((3, 4), (3, 4)).normalized()
    # one component
    assert CanvasVector((0, 0), (0, 4)).normalized() == v_y_norm
    assert CanvasVector((0, 4), (0, 0)).normalized() == v_y_norm_neg
    assert CanvasVector((0, 4), (0, 7)).normalized() == v_y_norm
    assert CanvasVector((0, 7), (0, 4)).normalized() == v_y_norm_neg
    assert CanvasVector((0, 0), (4, 0)).normalized() == v_x_norm
    assert CanvasVector((4, 0), (0, 0)).normalized() == v_x_norm_neg
    assert CanvasVector((4, 0), (7, 0)).normalized() == v_x_norm
    assert CanvasVector((7, 0), (4, 0)).normalized() == v_x_norm_neg


def test_vector_orthogonal():
    v_up = CanvasVector((0, 0), (0, -1))
    v_down = CanvasVector((0, 0), (0, 1))
    v_left = CanvasVector((0, 0), (-1, 0))
    v_right = CanvasVector((0, 0), (1, 0))
    inv_sqrt2 = 1/math.sqrt(2)
    v_up_left = CanvasVector((0, 0), (-inv_sqrt2, -inv_sqrt2))
    v_up_right = CanvasVector((0, 0), (inv_sqrt2, -inv_sqrt2))
    v_down_left = CanvasVector((0, 0), (-inv_sqrt2, inv_sqrt2))
    v_down_right = CanvasVector((0, 0), (inv_sqrt2, inv_sqrt2))
    # clockwise
    assert v_up.orthogonal() == v_right
    assert v_right.orthogonal() == v_down
    assert v_down.orthogonal() == v_left
    assert v_left.orthogonal() == v_up
    assert v_up_left.orthogonal() == v_up_right
    assert v_up_right.orthogonal() == v_down_right
    assert v_down_right.orthogonal() == v_down_left
    assert v_down_left.orthogonal() == v_up_left
    # counterclockwise
    assert v_up.orthogonal(ccw=True) == v_left
    assert v_left.orthogonal(ccw=True) == v_down
    assert v_down.orthogonal(ccw=True) == v_right
    assert v_right.orthogonal(ccw=True) == v_up
    assert v_up_right.orthogonal(ccw=True) == v_up_left
    assert v_up_left.orthogonal(ccw=True) == v_down_left
    assert v_down_left.orthogonal(ccw=True) == v_down_right
    assert v_down_right.orthogonal(ccw=True) == v_up_right
