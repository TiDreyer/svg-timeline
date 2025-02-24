""" Singleton to store styling defaults """
from dataclasses import dataclass


@dataclass
class __TimelineStyle:
    title_x_position: float = 1/2
    title_y_position: float = 1/17
    title_size_factor: float = 1/15
    title_text_color: str = 'black'
    title_font_family: str = 'Liberation Sans'

    lane_width: float = 30
    bg_clor: str = 'white'

    arrow_stroke_width: float = 3
    arrow_y_position: float = 0.9
    arrow_x_padding: float = 0.03

    major_stroke_width: float = 2
    minor_stroke_width: float = 1

    event_stroke_width: float = 2
    event_dot_radius: float = 3
    event_color: str = 'black'

    image_stroke_width: float = 2
    image_color: str = 'black'

    timespan_width: float = 18
    timespan_bg_color: str = 'blue'
    timespan_use_start_stilt: bool = False
    timespan_use_end_stilt: bool = False
    timespan_stilt_stroke_width: float = 1
    timespan_stilt_color: str = 'lightgrey'
    timespan_text_color: str = 'black'
    timespan_text_size_factor: float = 0.7


Defaults = __TimelineStyle()

DEFAULT_CSS = {
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
    }
}
