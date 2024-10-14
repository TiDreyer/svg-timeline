""" basic geometry classes to describe canvas points """
import math


# tolerance on coordinates within which two points are considered equal
COORD_TOLERANCE = 0.000_001


class Canvas:
    """ representation of a rectangular drawing area
    with the origin (0,0) in the top left corner """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __contains__(self, item) -> bool:
        """ check whether the item is contained within the canvas"""
        if isinstance(item, CanvasPoint):
            if item.x < 0 or item.y < 0:
                return False
            if item.x > self.width:
                return False
            if item.y > self.height:
                return False
            return True
        if isinstance(item, CanvasVector):
            # only True if the vector is **completely** contained inside the canvas
            if item.initial_point not in self:
                return False
            if item.terminal_point not in self:
                return False
            return True
        raise TypeError(f"__contains__ not defined for type '{type(item)}'")


class CanvasPoint:
    """ a point within a canvas """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        """ two points are equal, if their coordinates are equal within COORD_TOLERANCE """
        if not isinstance(other, CanvasPoint):
            raise TypeError("Can only compare with another CanvasPoint instance")
        return (math.fabs(self.x - other.x) < COORD_TOLERANCE and
                math.fabs(self.y - other.y) < COORD_TOLERANCE)


class CanvasVector:
    """ a vector between two points on a canvas """
    def __init__(self, initial_point: CanvasPoint, terminal_point: CanvasPoint):
        self.initial_point = initial_point
        self.terminal_point = terminal_point

    def __eq__(self, other) -> bool:
        """ two vectors are equal, if their two endpoints are equal within COORD_TOLERANCE """
        if not isinstance(other, CanvasVector):
            raise TypeError("Can only compare with another CanvasVector instance")
        return (self.initial_point == other.initial_point and
                self.terminal_point == other.terminal_point)

    @property
    def mag(self) -> float:
        """ the vector magnitude (length) according to the euclidian norm """
        delta_x_squared = (self.terminal_point.x - self.initial_point.x)**2
        delta_y_squared = (self.terminal_point.y - self.initial_point.y)**2
        norm = math.sqrt(delta_x_squared + delta_y_squared)
        return norm
