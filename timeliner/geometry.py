""" basic geometry classes to describe canvas points """

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
        raise TypeError(f"__contains__ not defined for type '{type(item)}'")


class CanvasPoint:
    """ a point within a canvas """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
