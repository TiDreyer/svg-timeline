""" classes for defining different kinds of elements that can be drawn in an SVG """
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

