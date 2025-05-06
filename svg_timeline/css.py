""" base classes for handling CSS """
from enum import StrEnum
from typing import Optional

from svg_timeline.colors import ColorPalette, DEFAULT_COLORS


class CascadeStyleSheet(dict):
    """ basic representation of a CSS """
    def __init__(self, custom_entries: Optional[dict] = None):
        super().__init__(_DEFAULTS)
        if custom_entries is not None:
            self.update(custom_entries)
        self.full_validate()
        self._used_color_palette: Optional[ColorPalette] = None

    def full_validate(self):
        """ check that the object represents valid CSS """
        for key, value in self.items():
            self.__validate_one_entry(key, value)

    def __setitem__(self, key, value):
        self.__validate_one_entry(key, value)
        super().__setitem__(key, value)

    @staticmethod
    def __validate_one_entry(key, value):
        if not isinstance(key, str):
            raise TypeError(f"Invalid key {key}. All CSS keys must be strings.")
        if not isinstance(value, dict):
            raise TypeError(f"Invalid entry for key {key}. All CSS entries must be dicts.")
        for sub_key, sub_value in value.items():
            if not isinstance(sub_key, str):
                raise TypeError(f"Invalid subkey {sub_key} in entry {key}. All CSS keys must be strings.")
            if not isinstance(sub_value, str):
                raise TypeError(f"Invalid value for {sub_key} in entry {key}. All CSS values must be strings.")

    def compile(self, indent='', line_break='\n') -> str:
        """ compile the contained style definition into a css file """
        if self._used_color_palette is None:
            self.set_color_palette(DEFAULT_COLORS)
        css_section = f'{line_break or " "}'
        for selector, props in self.items():
            css_section += f'{selector} {{{line_break}'
            css_section += f'{line_break or " "}'.join(
                f'{indent}{name}: {value};' for name, value in props.items()
            )
            css_section += f'{line_break or " "}}}{line_break or " "}'
        return css_section

    def set_color_palette(self, palette: ColorPalette):
        if self._used_color_palette is not None:
            raise RuntimeError("Color palette was already set on this CascadeStyleSheet")
        for i, color in enumerate(palette):
            self[f'.colored.c{i:02}'] = {
                'stroke': color.color,
                'fill': color.color,
            }
            self[f'.top_text.c{i:02}'] = {
                'fill': color.top_text_color,
            }
        self._used_color_palette = palette


class ClassNames(StrEnum):
    """ string constants for all the class names that are commonly used for styling via CSS """
    # determining the timeline element:
    TITLE = 'title'
    TIME_ARROW = 'time_arrow'
    EVENT = 'event'
    TIMESPAN = 'timespan'
    CONNECTED_EVENTS = 'connected_events'
    IMAGE = 'image'
    # sub-elements
    TIME_ARROW_AXIS = 'time_axis'
    TIME_ARROW_MINOR_TIC = 'minor_tic'
    TIME_ARROW_MAJOR_TIC = 'major_tic'
    # for picking which color to use:
    COLORED = 'colored'
    TOP_TEXT = 'top_text'


_DEFAULTS = {
    'rect.background': {
        'fill': 'white',
    },
    'path': {
        'stroke': 'black',
        'stroke-width': '2pt',
        'fill': 'none',
    },
    'text': {
        'font-size': '10pt',
        'font-family': 'Liberation Sans',
        'fill': 'black',
        'text-anchor': 'middle',
        'dominant-baseline': 'central',
    },
    'circle, rect': {
        'fill': 'black',
    },
    f'text.{ClassNames.TITLE}': {
        'font-size': '20pt',
    },
    f'path.{ClassNames.TIME_ARROW_AXIS}': {
        'stroke-width': '3pt',
    },
    f'path.{ClassNames.TIME_ARROW_MAJOR_TIC}': {
        'stroke-width': '2pt',
    },
    f'path.{ClassNames.TIME_ARROW_MINOR_TIC}': {
        'stroke-width': '1pt',
    },
    f'path.{ClassNames.EVENT}': {
        'stroke-width': '2pt',
    },
    f'text.{ClassNames.TIMESPAN}': {
        'font-size': '9pt',
    },
    f'path.{ClassNames.IMAGE}': {
        'stroke-width': '2pt',
    },
}
