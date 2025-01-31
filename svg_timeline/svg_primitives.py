""" classes for defining different kinds of elements that can be drawn in an SVG """
import math
from mimetypes import guess_type
from base64 import b64encode
from html import escape
from pathlib import Path

from svg_timeline.geometry import Vector
from svg_timeline.svg import SvgElement
from svg_timeline.svg_style import SvgTextStyle, SvgPathStyle


class Line(SvgElement):
    """ straight line from one point to another """
    def __init__(self, source: Vector, target: Vector, style: SvgPathStyle):
        super().__init__(tag='path')
        self.source = source
        self.target = target
        self.path_style = style

    @property
    def attributes(self) -> dict[str, str]:
        attr = {
            'd': f'M{self.source.x},{self.source.y} L{self.target.x},{self.target.y}'
        }
        attr |= self.path_style.as_attributes
        return attr


class Text(SvgElement):
    """ text at a fixed position on the canvas """
    def __init__(self, coord: Vector, style: SvgTextStyle, text: str):
        super().__init__(tag='text', content=escape(text))
        self.coord = coord
        self.text_style = style

    @property
    def attributes(self) -> dict[str, str]:
        attr = {'x': str(self.coord.x), 'y': str(self.coord.y)}
        attr |= self.text_style.as_attributes
        return attr


class Rectangle(SvgElement):
    """ rectangle filled with the given color """
    def __init__(self, corner1: Vector, corner2: Vector, color: str):
        super().__init__(tag='rect')
        self.corner1 = corner1
        self.corner2 = corner2
        self.color = color

    @property
    def attributes(self) -> dict[str, str]:
        return {
            'x': str(min(self.corner1.x, self.corner2.x)),
            'y': str(min(self.corner1.y, self.corner2.y)),
            'width': str(math.fabs(self.corner1.x - self.corner2.x)),
            'height': str(math.fabs(self.corner1.y - self.corner2.y)),
            'fill': self.color,
        }


class Circle(SvgElement):
    """ circle filled with the given color """
    def __init__(self, center: Vector, radius: float, color: str):
        super().__init__(tag='circle')
        self.center = center
        self.radius = radius
        self.color = color

    @property
    def attributes(self) -> dict[str, str]:
        return {
            'cx': str(self.center.x),
            'cy': str(self.center.y),
            'r': str(self.radius),
            'fill': self.color,
        }


class Image(SvgElement):
    """ SVG embedding of the image found at the given file path """
    def __init__(self, top_left: Vector, width: float, height: float,
                 file: Path):
        super().__init__(tag='image')
        self.top_left = top_left
        self.width = width
        self.height = height
        self.file = file

    @property
    def attributes(self) -> dict[str, str]:
        mimetype, encoding = guess_type(self.file)
        with open(self.file, 'rb', encoding=encoding) as image_file:
            image_data = b64encode(image_file.read())
        return {
            'x': str(self.top_left.x),
            'y': str(self.top_left.y),
            'width': str(self.width),
            'height': str(self.height),
            'xlink:href': f'data:{mimetype};base64,{image_data.decode()}',
        }
