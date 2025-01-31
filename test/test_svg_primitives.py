""" test cases for the classes defined in the svg_primitives module """
from pathlib import Path

from svg_timeline.geometry import Vector
from svg_timeline.svg_primitives import Line, Text, Rectangle, Circle, Image
from svg_timeline.svg_style import SvgPathStyle, SvgTextStyle


def test_line():
    style = SvgPathStyle()
    source = Vector(-100, -200)
    target = Vector(300, 400)
    line = Line(source=source, target=target, style=style)
    svg = '<path d="M-100,-200 L300,400" stroke="black" stroke-width="2" fill="none" />'
    assert str(line) == svg


def test_text():
    style = SvgTextStyle()
    coord = Vector(300, 400)
    text = Text(coord=coord, style=style, text='asdf\nasdf\nasdf')
    svg = ('<text x="300" y="400"'
           ' font-size="12" font-family="Liberation Sans" fill="black"'
           ' text-anchor="middle" dominant-baseline="central">'
           'asdf\nasdf\nasdf'
           '</text>')
    assert str(text) == svg


def test_rectangle():
    corner1 = Vector(-100, -200)
    corner2 = Vector(300, 400)
    rect = Rectangle(corner1=corner1, corner2=corner2, color='red')
    svg = '<rect x="-100" y="-200" width="400.0" height="600.0" fill="red" />'
    assert str(rect) == svg


def test_circle():
    coord = Vector(300, 400)
    circle = Circle(center=coord, radius=30, color='green')
    svg = '<circle cx="300" cy="400" r="30" fill="green" />'
    assert str(circle) == svg


def test_image():
    center = Vector(300, 400)
    file_path = Path(__file__).parent.joinpath('files/single_pixel.png')
    image = Image(top_left=center, width=200, height=300, file=file_path)
    svg = ('<image x="300" y="400" width="200" height="300"'
           ' xlink:href="data:image/png;base64,'
           'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAA'
           'AADElEQVQI12P4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC'
           '" />')
    assert str(image) == svg
