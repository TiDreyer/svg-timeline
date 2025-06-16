""" test cases for the classes defined in the svg module """
from textwrap import dedent

from svg_timeline.svg import SvgFile, SvgElement


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
    svg = SvgFile(width=800, height=600)
    header = dedent('''\
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
         width="800" height="600" viewBox="0 0 800 600">
    ''')
    assert svg.header == header


def test_svg_defs_section():
    definitions = [
        SvgElement('a', {'a1': 'hello', 'a2': 'world'}, 'asdf'),
        SvgElement('b', {'b1': 'hello', 'b2': 'world'}),
    ]
    svg_with = SvgFile(width=800, height=600, definitions=definitions)
    svg_without = SvgFile(width=800, height=600)
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
    svg_with = SvgFile(width=800, height=600, elements=elements)
    svg_without = SvgFile(width=800, height=600)
    element_section = dedent('''\
    <a a1="hello" a2="world">asdf</a>
    <b b1="hello" b2="world" />
    ''')
    assert svg_with.element_section == element_section
    assert svg_without.element_section == ''


def test_svg_footer():
    svg = SvgFile(width=800, height=600)
    footer = dedent('''\
    </svg>
    ''')
    assert svg.footer == dedent(footer)
