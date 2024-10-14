""" test cases for the classes defined in the geometry module """
from timeliner.geometry import Canvas, CanvasPoint, CanvasVector


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
