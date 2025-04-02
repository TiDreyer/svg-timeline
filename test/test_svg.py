""" test cases for the classes defined in the svg module """
from textwrap import dedent

from svg_timeline.svg import SVG, SvgElement

def test_svg_element_getters():
    empty = SvgElement(tag='empty')
    assert empty.tag == 'empty'
    assert isinstance(empty.attributes, dict)
    assert len(empty.attributes) == 0
    assert empty.content is None
    assert empty.classes == []

    full_attr = {'a': 'asdf', 'b': 'av;eiojoia', 'class': 'a b c'}
    classes = ['1', 'b', '3']
    full_content = ";alsdkjf;lasjdf;lksajdf;lkjas;dflja;sldf;lasdjf"
    full = SvgElement(tag='full', attributes=full_attr, content=full_content, classes=classes)
    expected_attr = {'a': 'asdf', 'b': 'av;eiojoia', 'class': 'a b c 1 3'}
    assert full.tag == 'full'
    assert isinstance(full.attributes, dict)
    assert len(full.attributes) == len(expected_attr)
    assert full.attributes == expected_attr
    assert full.classes == ['a', 'b', 'c', '1', '3']
    assert full.content == full_content


def test_svg_element_str():
    with_content = SvgElement('asdf', {'a1': 'hello', 'a2': 'world'}, 'Hello World!')
    without_content = SvgElement('asdf', {'a1': 'hello', 'a2': 'world'})
    assert str(with_content) == '<asdf a1="hello" a2="world">Hello World!</asdf>'
    assert str(without_content) == '<asdf a1="hello" a2="world" />'


def test_svg_header():
    svg = SVG(width=800, height=600)
    header = dedent('''\
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
         width="800" height="600" viewBox="0 0 800 600">
    ''')
    assert svg.header == header


def test_svg_style_section():
    style = {
        'svg': {'background': 'white'},
        'text': {
            'font-family': 'Liberation Sans',
            'font-size': '12pt',
            'fill': 'black',
            'dominant-baseline': 'central',
            'text-anchor': 'middle',
        },
    }
    svg = SVG(width=800, height=600, style=style)
    style_section = dedent('''\
    <style>
    svg {
      background: white;
    }
    text {
      font-family: Liberation Sans;
      font-size: 12pt;
      fill: black;
      dominant-baseline: central;
      text-anchor: middle;
    }
    </style>
    ''')
    assert svg.style_section == style_section


def test_svg_defs_section():
    definitions = [
        SvgElement('a', {'a1': 'hello', 'a2': 'world'}, 'asdf'),
        SvgElement('b', {'b1': 'hello', 'b2': 'world'}),
    ]
    svg_with = SVG(width=800, height=600, definitions=definitions)
    svg_without = SVG(width=800, height=600)
    defs_section = dedent('''\
    <defs>
      <a a1="hello" a2="world">asdf</a>
      <b b1="hello" b2="world" />
    </defs>
    ''')
    assert svg_with.defs_section == defs_section
    assert svg_without.defs_section == ''


def test_svg_element_section():
    elements = [
        SvgElement('a', {'a1': 'hello', 'a2': 'world'}, 'asdf'),
        SvgElement('b', {'b1': 'hello', 'b2': 'world'}),
    ]
    svg_with = SVG(width=800, height=600, elements=elements)
    svg_without = SVG(width=800, height=600)
    element_section = dedent('''\
    <a a1="hello" a2="world">asdf</a>
    <b b1="hello" b2="world" />
    ''')
    assert svg_with.element_section == element_section
    assert svg_without.element_section == ''


def test_svg_footer():
    svg = SVG(width=800, height=600)
    footer = dedent('''\
    </svg>
    ''')
    assert svg.footer == dedent(footer)


def test_svg_full():
    style = {
        'svg': {'background': 'white'},
        'text': {
            'font-family': 'Liberation Sans',
            'font-size': '12pt',
            'fill': 'black',
            'dominant-baseline': 'central',
            'text-anchor': 'middle',
        },
    }
    definitions = [
        SvgElement('x', {'x1': 'hello', 'x2': 'world'}, 'asdf'),
        SvgElement('y', {'y1': 'hello', 'y2': 'world'}),
    ]
    elements = [
        SvgElement('a', {'a1': 'hello', 'a2': 'world'}, 'asdf'),
        SvgElement('b', {'b1': 'hello', 'b2': 'world'}),
    ]
    svg = SVG(width=800, height=600, style=style, elements=elements, definitions=definitions)
    full = dedent('''\
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
         width="800" height="600" viewBox="0 0 800 600">
    <style>
    svg {
      background: white;
    }
    text {
      font-family: Liberation Sans;
      font-size: 12pt;
      fill: black;
      dominant-baseline: central;
      text-anchor: middle;
    }
    </style>
    <defs>
      <x x1="hello" x2="world">asdf</x>
      <y y1="hello" y2="world" />
    </defs>
    <a a1="hello" a2="world">asdf</a>
    <b b1="hello" b2="world" />
    </svg>
    ''')
    assert svg.full == full
