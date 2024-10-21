""" basic geometry classes to describe canvas points """
import math
from typing import Self


# tolerance on coordinates within which two points are considered equal
COORD_TOLERANCE = 0.000_001


class Canvas:
    """ representation of a rectangular drawing area
    with the origin (0,0) in the top left corner """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"Canvas(width={self.width}, height={self.height})"

    def __contains__(self, item) -> bool:
        """ check whether the item is contained within the canvas"""
        if isinstance(item, CanvasPoint):
            if (item.x < 0 or item.x > self.width or
                item.y < 0 or item.y > self.height):
                return False
            return True
        if isinstance(item, CanvasVector):
            # only True if the vector is **completely** contained inside the canvas
            if item.initial_point not in self or item.terminal_point not in self:
                return False
            return True
        raise TypeError(f"__contains__ not defined for type '{type(item)}'")


class CanvasPoint:
    """ a point within a canvas """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"CanvasPoint({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        """ two points are equal, if their coordinates are equal within COORD_TOLERANCE """
        if not isinstance(other, CanvasPoint):
            raise TypeError("Can only compare with another CanvasPoint instance")
        return (math.fabs(self.x - other.x) < COORD_TOLERANCE and
                math.fabs(self.y - other.y) < COORD_TOLERANCE)


ORIGIN = CanvasPoint(0, 0)


class CanvasVector:
    """ a vector between two points on a canvas """
    def __init__(self, initial_point: CanvasPoint|tuple[float, float],
                 terminal_point: CanvasPoint|tuple[float, float]):
        if isinstance(initial_point, CanvasPoint):
            self.initial_point = initial_point
        elif isinstance(initial_point, tuple):
            self.initial_point = CanvasPoint(*initial_point)
        if isinstance(terminal_point, CanvasPoint):
            self.terminal_point = terminal_point
        elif isinstance(terminal_point, tuple):
            self.terminal_point = CanvasPoint(*terminal_point)

    def __repr__(self) -> str:
        return f"CanvasVector({self.initial_point}, {self.terminal_point})"

    def __eq__(self, other) -> bool:
        """ two vectors are equal, if their two endpoints are equal within COORD_TOLERANCE """
        if not isinstance(other, CanvasVector):
            raise TypeError("Can only compare with another CanvasVector instance")
        return (self.initial_point == other.initial_point and
                self.terminal_point == other.terminal_point)

    def __mul__(self, other) -> Self:
        """ scalar multiplication with an integer or float value
        which leaves the initial_point and direction as-is, and returns a vector
        which has a scaled magnitude
        """
        if not isinstance(other, (int, float)):
            return NotImplemented
        if self.mag == 0:
            return self
        direction = self.normalized().terminal_point
        new_magnitude = self.mag * other
        new_terminal_x = self.initial_point.x + new_magnitude * direction.x
        new_terminal_y = self.initial_point.y + new_magnitude * direction.y
        return CanvasVector(initial_point=self.initial_point,
                            terminal_point=CanvasPoint(new_terminal_x, new_terminal_y))

    def __rmul__(self, other) -> Self:
        """ (see __mul__)"""
        return self.__mul__(other=other)

    def __truediv__(self, other) -> Self:
        """ (see __mul__)"""
        factor = 1/other
        return self.__mul__(other=factor)

    def __rtruediv__(self, other) -> Self:
        """ dividing a value by a vector is not possible """
        return NotImplemented

    @property
    def mag(self) -> float:
        """ the vector magnitude (length) according to the euclidian norm """
        delta_x_squared = (self.terminal_point.x - self.initial_point.x)**2
        delta_y_squared = (self.terminal_point.y - self.initial_point.y)**2
        norm = math.sqrt(delta_x_squared + delta_y_squared)
        return norm

    def normalized(self) -> Self:
        """ return a normalized version of the vector
        the initial_point will be the origin (0, 0) and the magnitude will be 1
        :raises ZeroDivisionError if the vector has magnitude zero
        """
        if self.mag == 0:
            raise ZeroDivisionError("Can not normalize a vector of magnitude 0")
        norm_x = (self.terminal_point.x - self.initial_point.x) / self.mag
        norm_y = (self.terminal_point.y - self.initial_point.y) / self.mag
        norm_vec = CanvasVector(ORIGIN, CanvasPoint(norm_x, norm_y))
        return norm_vec

    def orthogonal(self, ccw: bool = False) -> Self:
        """ return a normalized vector that points in the (counter)clockwise
        orthogonal direction from this vector
        :argument ccw if True rotate counterclockwise, otherwise clockwise
        :raises ZeroDivisionError if the vector has magnitude zero
        """
        if self.mag == 0:
            raise ZeroDivisionError("Can not normalize a vector of magnitude 0")
        norm_x = (self.terminal_point.x - self.initial_point.x) / self.mag
        norm_y = (self.terminal_point.y - self.initial_point.y) / self.mag
        if ccw:
            vec_orthogonal = CanvasVector(ORIGIN, CanvasPoint(norm_y, -norm_x))
        else:
            vec_orthogonal = CanvasVector(ORIGIN, CanvasPoint(-norm_y, norm_x))
        return vec_orthogonal
