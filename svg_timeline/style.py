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
    title = 'title'
    time_axis = 'time_axis'
    minor_tick = 'minor_tick'
    major_tick = 'major_tick'
    event = 'event'
    timespan = 'timespan'
    image = 'image'
    white_text = 'white_text'
    cat_a = 'category_a'
    cat_b = 'category_b'
    cat_c = 'category_c'
    cat_d = 'category_d'
    cat_e = 'category_e'


DEFAULT_CSS = {
    ':root': {
        '--color_a': '#003f5c',
        '--color_b': '#58508d',
        '--color_c': '#bc5090',
        '--color_d': '#ff6361',
        '--color_e': '#ffa600',
    },
    f'path.{ClassNames.cat_a}': {'stroke': 'var(--color_a)'},
    f'path.{ClassNames.cat_b}': {'stroke': 'var(--color_b)'},
    f'path.{ClassNames.cat_c}': {'stroke': 'var(--color_c)'},
    f'path.{ClassNames.cat_d}': {'stroke': 'var(--color_d)'},
    f'path.{ClassNames.cat_e}': {'stroke': 'var(--color_e)'},
    f'rect.{ClassNames.cat_a}, circle.{ClassNames.cat_a}': {'fill': 'var(--color_a)'},
    f'rect.{ClassNames.cat_b}, circle.{ClassNames.cat_b}': {'fill': 'var(--color_b)'},
    f'rect.{ClassNames.cat_c}, circle.{ClassNames.cat_c}': {'fill': 'var(--color_c)'},
    f'rect.{ClassNames.cat_d}, circle.{ClassNames.cat_d}': {'fill': 'var(--color_d)'},
    f'rect.{ClassNames.cat_e}, circle.{ClassNames.cat_e}': {'fill': 'var(--color_e)'},
    'svg': {
        'background': 'white',
    },
    'path': {
        'stroke': 'black',
        'stroke-width': '2pt',
        'fill': 'none',
    },
    'text': {
        'font-size': '12pt',
        'font-family': 'Liberation Sans',
        'fill': 'black',
        'text-anchor': 'middle',
        'dominant-baseline': 'center',
    },
    'circle, rect': {
        'fill': 'black',
    },
    f'text.{ClassNames.title}': {
        'font-size': '20pt',
    },
    f'path.{ClassNames.time_axis}': {
        'stroke-width': '3pt',
    },
    f'path.{ClassNames.major_tick}': {
        'stroke-width': '2pt',
    },
    f'path.{ClassNames.minor_tick}': {
        'stroke-width': '1pt',
    },
    f'path.{ClassNames.event}': {
        'stroke-width': '2pt',
    },
    f'circle.{ClassNames.event}': {
        'radius': '3pt',
    },
    f'path.{ClassNames.timespan}': {
        'stroke-width': '1pt',
    },
    f'text.{ClassNames.timespan}': {
        'font-size': '11pt',
    },
    f'path.{ClassNames.image}': {
        'stroke-width': '2pt',
    },
    f'text.{ClassNames.white_text}': {
        'fill': 'white',
    },
}
