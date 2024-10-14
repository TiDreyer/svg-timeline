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


def test_vector_equal():
    p_0_0 = CanvasPoint(0, 0)
    p_1_1 = CanvasPoint(1, 1)
    assert CanvasVector(p_0_0, p_1_1) == CanvasVector(p_0_0, p_1_1)
    assert CanvasVector(p_1_1, p_0_0) == CanvasVector(p_1_1, p_0_0)
    assert CanvasVector(p_1_1, p_1_1) == CanvasVector(p_1_1, p_1_1)
    assert CanvasVector(p_0_0, p_0_0) != CanvasVector(p_1_1, p_1_1)
    assert CanvasVector(p_0_0, p_1_1) != CanvasVector(p_1_1, p_0_0)


def test_vector_in_canvas():
    canvas = Canvas(100, 100)
    in_point_a = CanvasPoint(30, 30)
    in_point_b = CanvasPoint(50, 50)
    out_point_a = CanvasPoint(-33, 50)
    out_point_b = CanvasPoint(33, 120)
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
    p_0_0 = CanvasPoint(0, 0)
    p_0_1 = CanvasPoint(0, 1)
    p_1_0 = CanvasPoint(1, 0)
    p_0_m1 = CanvasPoint(0, -1)
    p_m1_0 = CanvasPoint(-1, 0)
    p_1_2 = CanvasPoint(1, 2)
    p_2_4 = CanvasPoint(2, 4)
    p_3_6 = CanvasPoint(3, 6)
    p_m3_m6 = CanvasPoint(-3, -6)
    # normal scaling
    assert CanvasVector(p_0_0, p_1_2) * 2 == CanvasVector(p_0_0, p_2_4)
    assert CanvasVector(p_0_0, p_1_2) * 3 == CanvasVector(p_0_0, p_3_6)
    assert CanvasVector(p_0_0, p_2_4) * 0.5 == CanvasVector(p_0_0, p_1_2)
    assert CanvasVector(p_0_0, p_3_6) / 3 == CanvasVector(p_0_0, p_1_2)
    assert CanvasVector(p_0_0, p_m3_m6) / -3 == CanvasVector(p_0_0, p_1_2)
    # wrong type
    with pytest.raises(TypeError):
        _ = CanvasVector(p_0_0, p_0_0) * '7'
    # float and integer
    assert CanvasVector(p_0_0, p_3_6) * 7 == CanvasVector(p_0_0, p_3_6) * 7.0
    assert CanvasVector(p_3_6, p_0_0) * 7 == CanvasVector(p_3_6, p_0_0) * 7.0
    # magnitude zero vectors
    assert CanvasVector(p_0_0, p_0_0) * 7 == CanvasVector(p_0_0, p_0_0)
    assert CanvasVector(p_3_6, p_3_6) * 7 == CanvasVector(p_3_6, p_3_6)
    assert CanvasVector(p_0_0, p_0_0) * 7 != CanvasVector(p_3_6, p_3_6)
    # left and right multiplicity
    assert CanvasVector(p_0_0, p_3_6) * 7 == 7 * CanvasVector(p_0_0, p_3_6)
    assert CanvasVector(p_3_6, p_0_0) * 7 == 7 * CanvasVector(p_3_6, p_0_0)
    assert CanvasVector(p_0_0, p_3_6) * -7 == -7 * CanvasVector(p_0_0, p_3_6)
    assert CanvasVector(p_3_6, p_0_0) * -7 == -7 * CanvasVector(p_3_6, p_0_0)
    # inversion
    assert CanvasVector(p_0_0, p_0_1) * -1 == CanvasVector(p_0_0, p_0_m1)
    assert CanvasVector(p_0_0, p_1_0) * -1 == CanvasVector(p_0_0, p_m1_0)
    assert CanvasVector(p_0_0, p_3_6) * -1 == CanvasVector(p_0_0, p_m3_m6)



def test_vector_magnitude():
    p_0_0 = CanvasPoint(0, 0)
    p_3_0 = CanvasPoint(3, 0)
    p_0_4 = CanvasPoint(0, 4)
    p_3_4 = CanvasPoint(3, 4)
    p_6_7 = CanvasPoint(6, 7)
    p_10_10 = CanvasPoint(10, 10)
    # zero length
    assert CanvasVector(p_0_0, p_0_0).mag == 0
    assert CanvasVector(p_3_4, p_3_4).mag == 0
    # one component
    assert CanvasVector(p_0_0, p_0_4).mag == 4
    assert CanvasVector(p_0_4, p_0_0).mag == 4
    assert CanvasVector(p_0_0, p_3_0).mag == 3
    assert CanvasVector(p_3_0, p_0_0).mag == 3
    # 3^2 + 4^2 = 5^2
    assert CanvasVector(p_0_0, p_3_4).mag == 5
    assert CanvasVector(p_3_4, p_0_0).mag == 5
    assert CanvasVector(p_6_7, p_10_10).mag == 5
    assert CanvasVector(p_10_10, p_6_7).mag == 5


def test_vector_normalized():
    p_0_0 = CanvasPoint(0, 0)
    p_0_1 = CanvasPoint(0, 1)
    p_1_0 = CanvasPoint(1, 0)
    p_0_m1 = CanvasPoint(0, -1)
    p_m1_0 = CanvasPoint(-1, 0)
    p_0_4 = CanvasPoint(0, 4)
    p_0_7 = CanvasPoint(0, 7)
    p_4_0 = CanvasPoint(4, 0)
    p_7_0 = CanvasPoint(7, 0)
    p_3_4 = CanvasPoint(3, 4)
    v_x_norm = CanvasVector(p_0_0, p_1_0)
    v_y_norm = CanvasVector(p_0_0, p_0_1)
    v_x_norm_neg = CanvasVector(p_0_0, p_m1_0)
    v_y_norm_neg = CanvasVector(p_0_0, p_0_m1)
    # zero length
    with pytest.raises(ZeroDivisionError):
        _ = CanvasVector(p_0_0, p_0_0).normalized()
    with pytest.raises(ZeroDivisionError):
        _ = CanvasVector(p_3_4, p_3_4).normalized()
    # one component
    assert CanvasVector(p_0_0, p_0_4).normalized() == v_y_norm
    assert CanvasVector(p_0_4, p_0_0).normalized() == v_y_norm_neg
    assert CanvasVector(p_0_4, p_0_7).normalized() == v_y_norm
    assert CanvasVector(p_0_7, p_0_4).normalized() == v_y_norm_neg
    assert CanvasVector(p_0_0, p_4_0).normalized() == v_x_norm
    assert CanvasVector(p_4_0, p_0_0).normalized() == v_x_norm_neg
    assert CanvasVector(p_4_0, p_7_0).normalized() == v_x_norm
    assert CanvasVector(p_7_0, p_4_0).normalized() == v_x_norm_neg


def test_vector_orthogonal():
    p_0_0 = CanvasPoint(0, 0)
    v_up = CanvasVector(p_0_0, CanvasPoint(0, -1))
    v_down = CanvasVector(p_0_0, CanvasPoint(0, 1))
    v_left = CanvasVector(p_0_0, CanvasPoint(-1, 0))
    v_right = CanvasVector(p_0_0, CanvasPoint(1, 0))
    inv_sqrt2 = 1/math.sqrt(2)
    v_up_left = CanvasVector(p_0_0, CanvasPoint(-inv_sqrt2, -inv_sqrt2))
    v_up_right = CanvasVector(p_0_0, CanvasPoint(inv_sqrt2, -inv_sqrt2))
    v_down_left = CanvasVector(p_0_0, CanvasPoint(-inv_sqrt2, inv_sqrt2))
    v_down_right = CanvasVector(p_0_0, CanvasPoint(inv_sqrt2, inv_sqrt2))
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
