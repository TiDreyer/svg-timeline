""" basic geometry classes to describe canvas points """

class Canvas:
    """ representation of a rectangular drawing area
    with the origin (0,0) in the top left corner """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
