""" classes for defining different kinds of elements that can be drawn in an SVG """
import math
from mimetypes import guess_type
from base64 import b64encode
from html import escape
from pathlib import Path
from textwrap import indent
from typing import Optional, Self

from svg_timeline.geometry import Vector
from svg_timeline.svg import SvgElement, _INDENT


class Line(SvgElement):
    """ straight line from one point to another """
    def __init__(self, source: Vector, target: Vector, classes: Optional[list[str]] = None):
        super().__init__(tag='path', classes=classes)
        self.source = source
        self.target = target
        self._update_attributes()

    def _update_attributes(self) -> None:
        self._attributes.update({
            'd': f'M{self.source.x},{self.source.y} L{self.target.x},{self.target.y}'
        })


class Text(SvgElement):
    """ text at a fixed position on the canvas """
    def __init__(self, coord: Vector, text: str, classes: Optional[list[str]] = None):
        super().__init__(tag='text', content=escape(text), classes=classes)
        self.coord = coord
        self._update_attributes()

    def _update_attributes(self) -> None:
        self._attributes.update({
            'x': str(self.coord.x),
            'y': str(self.coord.y),
        })


class Rectangle(SvgElement):
    """ rectangle filled with the given color """
    def __init__(self, corner1: Vector, corner2: Vector, classes: Optional[list[str]] = None):
        super().__init__(tag='rect', classes=classes)
        self.corner1 = corner1
        self.corner2 = corner2
        self._update_attributes()

    def _update_attributes(self) -> None:
        self._attributes.update({
            'x': str(min(self.corner1.x, self.corner2.x)),
            'y': str(min(self.corner1.y, self.corner2.y)),
            'width': str(math.fabs(self.corner1.x - self.corner2.x)),
            'height': str(math.fabs(self.corner1.y - self.corner2.y)),
        })


class Circle(SvgElement):
    """ circle filled with the given color """
    def __init__(self, center: Vector, radius: float, classes: Optional[list[str]] = None):
        super().__init__(tag='circle', classes=classes)
        self.center = center
        self.radius = radius
        self._update_attributes()

    def _update_attributes(self) -> None:
        self._attributes.update({
            'cx': str(self.center.x),
            'cy': str(self.center.y),
            'r': str(self.radius),
        })


class Image(SvgElement):
    """ SVG embedding of the image found at the given file path """
    def __init__(self, top_left: Vector, width: float, height: float,
                 xlink_href: str, classes: Optional[list[str]] = None):
        super().__init__(tag='image', classes=classes)
        self.top_left = top_left
        self.width = width
        self.height = height
        self.xlink_href = xlink_href
        self._update_attributes()

    def _update_attributes(self) -> None:
        self._attributes.update({
            'x': str(self.top_left.x),
            'y': str(self.top_left.y),
            'width': str(self.width),
            'height': str(self.height),
            'xlink:href': self.xlink_href,
        })

    @staticmethod
    def xlink_href_from_file_path(file: Path) -> str:
        """ determine the data representation of the image from its path """
        mimetype, encoding = guess_type(file)
        with open(file, 'rb', encoding=encoding) as image_file:
            image_data = b64encode(image_file.read())
        xlink_href = f'data:{mimetype};base64,{image_data.decode()}'
        return xlink_href

    @classmethod
    def from_path(cls, top_left: Vector, width: float, height: float,
                  file_path: Path, classes: Optional[list[str]] = None) -> Self:
        """ generate an instance from a file path instead of the data """
        xlink_href = cls.xlink_href_from_file_path(file_path)
        return cls(top_left, width, height, xlink_href, classes)


class SvgGroup(SvgElement):
    """ a group of SVG elements inside a g-container """
    id_counters = {}

    def __init__(self,
                 elements: Optional[list[SvgElement]] = None,
                 attributes: Optional[dict[str, str]] = None,
                 classes: Optional[list[str]] = None,
                 id_base: str = 'group',
                 exact_id: Optional[str] = None,
                 ):
        super().__init__(tag='g', attributes=attributes, classes=classes)
        self._elements = elements or []
        counter = SvgGroup.id_counters.setdefault(id_base, 1)
        if exact_id is not None:
            self._attributes['id'] = exact_id
        else:
            self._attributes['id'] = f'{id_base}_{counter:03}'
        SvgGroup.id_counters[id_base] += 1

    @property
    def content(self) -> Optional[str]:
        """ the contained elements """
        if len(self._elements) == 0:
            return None
        content_lines = [indent(str(element), _INDENT) for element in self._elements]
        return '\n' + '\n'.join(content_lines) + '\n'

    def append(self, element: SvgElement) -> None:
        """ add an element to this group """
        self._elements.append(element)
