""" test cases for the classes defined in the geometry module """
from timeliner.geometry import Canvas, CanvasPoint


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
