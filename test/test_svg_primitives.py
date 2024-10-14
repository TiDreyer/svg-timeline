""" test cases for the classes defined in the svg_primitives module """
from timeliner.geometry import CanvasVector, CanvasPoint
from timeliner.svg_primitives import Line, Text
from timeliner.svg_style import SvgPathStyle, SvgTextStyle


def test_line():
    style = SvgPathStyle()
    coord = CanvasVector(CanvasPoint(-100, -200), CanvasPoint(300, 400))
    line = Line(coord=coord, style=style)
    svg = '<path d="M-100,-200 L300,400" stroke="black" stroke-width="2" fill="none" />'
    assert str(line) == svg


def test_text():
    style = SvgTextStyle()
    coord = CanvasPoint(300, 400)
    text = Text(coord=coord, style=style, text='asdf\nasdf\nasdf')
    svg = ('<text x="300" y="400"'
           ' font-size="12" font-family="Liberation Sans"'
           ' text-anchor="middle" dominant-baseline="central">'
           'asdf\nasdf\nasdf'
           '</text>')
    assert str(text) == svg
