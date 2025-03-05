""" Singleton to store styling defaults """
from dataclasses import dataclass
from enum import StrEnum


@dataclass
class __TimelineStyle:
    title_x_position: float = 1/2
    title_y_position: float = 1/17
    title_size_factor: float = 1/15

    lane_width: float = 30

    arrow_y_position: float = 0.9
    arrow_x_padding: float = 0.03

    event_dot_radius: float = 3

    timespan_width: float = 18
    timespan_use_start_stilt: bool = False
    timespan_use_end_stilt: bool = False


Defaults = __TimelineStyle()


class ClassNames(StrEnum):
    """ string constants for all the class names that are commonly used for styling via CSS """
    TITLE = 'title'
    TIMEAXIS = 'time_axis'
    MINOR_TICK = 'minor_tic'
    MAJOR_TICK = 'major_tic'
    EVENT = 'event'
    TIMESPAN = 'timespan'
    IMAGE = 'image'
    WHITE_TEXT = 'white_text'


class Colors(StrEnum):
    """ string constants for all the colors that are pre-defined as class names """
    COLOR_A = '#003f5c'
    COLOR_B = '#58508d'
    COLOR_C = '#bc5090'
    COLOR_D = '#ff6361'
    COLOR_E = '#ffa600'


DEFAULT_CSS = {
    'svg': {
        'background': 'white',
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
    f'text.{ClassNames.WHITE_TEXT}': {
        'fill': 'white',
    },
}

for __COLOR in Colors:
    __SELECTOR = f'path.{__COLOR.name.lower()}, rect.{__COLOR.name.lower()}, circle.{__COLOR.name.lower()}'
    DEFAULT_CSS[__SELECTOR] = {
        'stroke': str(__COLOR),
        'fill': str(__COLOR),
    }
