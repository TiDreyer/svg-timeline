""" base classes for handling CSS """
from enum import StrEnum


class CascadeStyleSheet(dict):
    """ basic representation of a CSS """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_validate()

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
        css_section = ""
        for selector, props in self.items():
            css_section += f'{selector} {{{line_break}'
            for name, value in props.items():
                css_section += f'{indent}{name}: {value};{line_break}'
            css_section += f'}}{line_break}'
        return css_section


class ClassNames(StrEnum):
    """ string constants for all the class names that are commonly used for styling via CSS """
    TITLE = 'title'
    TIMEAXIS = 'time_axis'
    MINOR_TICK = 'minor_tic'
    MAJOR_TICK = 'major_tic'
    EVENT = 'event'
    TIMESPAN = 'timespan'
    IMAGE = 'image'


class Colors(StrEnum):
    """ string constants for all the colors that are pre-defined as class names """
    WHITE = '#ffffff'
    BLACK = '#000000'
    COLOR_A = '#003f5c'
    COLOR_B = '#58508d'
    COLOR_C = '#bc5090'
    COLOR_D = '#ff6361'
    COLOR_E = '#ffa600'


DEFAULT_CSS = CascadeStyleSheet({
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
    f'path.{ClassNames.TIMEAXIS}': {
        'stroke-width': '3pt',
    },
    f'path.{ClassNames.MAJOR_TICK}': {
        'stroke-width': '2pt',
    },
    f'path.{ClassNames.MINOR_TICK}': {
        'stroke-width': '1pt',
    },
    f'path.{ClassNames.EVENT}': {
        'stroke-width': '2pt',
    },
    f'circle.{ClassNames.EVENT}': {
        'radius': '3pt',
    },
    f'path.{ClassNames.TIMESPAN}': {
        'stroke-width': '1pt',
    },
    f'text.{ClassNames.TIMESPAN}': {
        'font-size': '9pt',
    },
    f'path.{ClassNames.IMAGE}': {
        'stroke-width': '2pt',
    },
})

for __COLOR in Colors:
    __SELECTOR = f'path.{__COLOR.name.lower()}, rect.{__COLOR.name.lower()}, circle.{__COLOR.name.lower()}'
    DEFAULT_CSS[__SELECTOR] = {
        'stroke': str(__COLOR),
        'fill': str(__COLOR),
    }
    __SELECTOR = f'text.{__COLOR.name.lower()}_text'
    DEFAULT_CSS[__SELECTOR] = {
        'fill': str(__COLOR),
    }
