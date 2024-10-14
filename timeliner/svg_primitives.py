""" classes for defining different kinds of elements that can be drawn in an SVG """
import math
from mimetypes import guess_type
from base64 import b64encode
from pathlib import Path

from timeliner.geometry import CanvasVector, CanvasPoint
from timeliner.svg import SvgElement
from timeliner.svg_style import SvgTextStyle, SvgPathStyle


class Line(SvgElement):
    """ straight line from one point to another """
    def __init__(self, coord: CanvasVector, style: SvgPathStyle):
        super().__init__(tag='path')
        self.coord = coord
        self.path_style = style

    @property
    def attributes(self) -> dict[str, str]:
        a, b = self.coord.initial_point, self.coord.terminal_point
        attr = {'d': f'M{a.x},{a.y} L{b.x},{b.y}'}
        attr |= self.path_style.as_attributes
        return attr


class Text(SvgElement):
    """ text at a fixed position on the canvas """
    def __init__(self, coord: CanvasPoint, style: SvgTextStyle, text: str):
        super().__init__(tag='text', content=text)
        self.coord = coord
        self.text_style = style

    @property
    def attributes(self) -> dict[str, str]:
        attr = {'x': str(self.coord.x), 'y': str(self.coord.y)}
        attr |= self.text_style.as_attributes
        return attr


class Rectangle(SvgElement):
    """ rectangle filled with the given color """
    def __init__(self, coord: CanvasVector, color: str):
        super().__init__(tag='rect')
        self.coord = coord
        self.color = color

    @property
    def attributes(self) -> dict[str, str]:
        a, b = self.coord.initial_point, self.coord.terminal_point
        return {
            'x': str(min(a.x, b.x)),
            'y': str(min(a.y, b.y)),
            'width': str(math.fabs(a.x - b.x)),
            'height': str(math.fabs(a.y - b.y)),
            'fill': self.color,
        }


class Circle(SvgElement):
    """ circle filled with the given color """
    def __init__(self, center: CanvasPoint, radius: float, color: str):
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
    def __init__(self, position: CanvasPoint, width: float, height: float,
                 file: Path):
        super().__init__(tag='image')
        self.position = position
        self.width = width
        self.height = height
        self.file = file

    @property
    def attributes(self) -> dict[str, str]:
        mimetype, encoding = guess_type(self.file)
        with open(self.file, 'rb', encoding=encoding) as image_file:
            image_data = b64encode(image_file.read())
        return {
            'x': str(self.position.x),
            'y': str(self.position.y),
            'width': str(self.width),
            'height': str(self.height),
            'xlink:href': f'data:{mimetype};base64,{image_data.decode()}',
        }
