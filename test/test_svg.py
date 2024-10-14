""" test cases for the classes defined in the svg module """
from timeliner.svg import SvgElement

def test_svg_element_getters():
    empty = SvgElement(tag='empty')
    assert empty.tag == 'empty'
    assert isinstance(empty.attributes, dict)
    assert len(empty.attributes) == 0
    assert empty.content is None

    full_attr = {'a': 'asdf', 'b': 'av;eiojoia'}
    full_content = ";alsdkjf;lasjdf;lksajdf;lkjas;dflja;sldf;lasdjf"
    full = SvgElement(tag='full', attributes=full_attr, content=full_content)
    assert full.tag == 'full'
    assert isinstance(full.attributes, dict)
    assert len(full.attributes) == len(full_attr)
    assert full.attributes == full_attr
    assert full.content == full_content


def test_svg_element_str():
    with_content = SvgElement('asdf', {'a1': 'hello', 'a2': 'world'}, 'Hello World!')
    without_content = SvgElement('asdf', {'a1': 'hello', 'a2': 'world'})
    assert str(with_content) == '<asdf a1="hello" a2="world">Hello World!</asdf>'
    assert str(without_content) == '<asdf a1="hello" a2="world" />'
