""" base classes for creating SVG files """
from html import escape
from typing import Optional


class SvgElement:
    """ general class for describing an element in an SVG and transforming it into
    its XML representation for saving it """
    def __init__(self, tag: str, attributes: Optional[dict[str, str]] = None,
                 content: Optional[str] = None):
        self._tag = tag
        self._attributes = attributes or {}
        self._content = content

    @property
    def tag(self) -> str:
        """ the element's tag as a string """
        return self._tag

    @property
    def attributes(self) -> dict[str, str]:
        """ dictionary of the element's attributes """
        return self._attributes

    @property
    def content(self) -> Optional[str]:
        """ the element's content as a string """
        return self._content

    def __str__(self) -> str:
        svg_element = f'<{self.tag}'
        for key, value in self.attributes.items():
            svg_element += f' {key}="{escape(value)}"'
        if self.content is not None:
            svg_element += f'>{self.content}</{self.tag}>'
        else:
            svg_element += ' />'
        return svg_element
