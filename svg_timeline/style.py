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
        'font-size': '12pt',
        'font-family': 'Liberation Sans',
        'fill': 'black',
        'text-anchor': 'middle',
        'dominant-baseline': 'center',
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
        'fill': 'black',
        'stroke-width': '2pt',
    },
    f'circle.{ClassNames.event}': {
        'fill': 'black',
        'radius': '3pt',
    },
    f'rect.{ClassNames.timespan}': {
        'fill': 'black',
    },
    f'path.{ClassNames.timespan}': {
        'fill': 'black',
        'stroke-width': '1pt',
    },
    f'text.{ClassNames.timespan}': {
        'font-size': '11pt',
        'fill': 'white',
    },
    f'path.{ClassNames.image}': {
        'fill': 'black',
        'stroke-width': '2pt',
    },
}
