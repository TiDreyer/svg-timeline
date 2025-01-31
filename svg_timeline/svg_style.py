""" data classes for defining the style of different SVG elements """
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class SvgTextStyle:
    """ data class containing style information for SVG text """
    font_size: int|float = 12
    font_family: str = 'Liberation Sans'
    text_color: str = 'black'
    text_align: Literal['left']|Literal['middle']|Literal['right']|Literal['justify'] = 'middle'
    anchor_vertical: Literal['top']|Literal['center']|Literal['bottom'] = 'center'

    @property
    def as_attributes(self) -> dict[str, str]:
        """ transform the content into the representation expected by SVG """
        match self.anchor_vertical:
            case 'top': dominant_baseline = 'hanging'
            case 'center': dominant_baseline = 'central'
            case 'bottom': dominant_baseline = 'text-top'
            case _: raise ValueError(f"Unknown value: {self.anchor_vertical}")
        return {
            'font-size': str(self.font_size),
            'font-family': self.font_family,
            'fill': self.text_color,
            'text-anchor': self.text_align,
            'dominant-baseline': dominant_baseline,
        }


@dataclass
class SvgPathStyle:
    """ data class containing style information for SVG paths """
    color: str = 'black'
    stroke_width: int|float = 2
    fill: Optional[str] = None

    @property
    def as_attributes(self) -> dict[str, str]:
        """ transform the content into the representation expected by SVG """
        return {
            'stroke': self.color,
            'stroke-width': str(self.stroke_width),
            'fill': 'none' if self.fill is None else self.fill,
        }
