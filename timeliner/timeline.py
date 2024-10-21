""" high level timeline API classes """
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from timeliner.geometry import Vector
from timeliner.svg import SVG
from timeliner.svg_primitives import Rectangle, Line, Text, Circle
from timeliner.svg_style import SvgPathStyle, SvgTextStyle
from timeliner.time_calculations import TimeGradient, TimeSpacing

@dataclass
class Event:
    date: datetime
    text: str


class TimelinePlot:
    def __init__(self, start_date: datetime, end_date: datetime,
                 time_spacing: TimeSpacing,
                 size: tuple[int, int] = (800, 600)):
        self._width, self._height = size
        self._svg = SVG(self._width, self._height)
        self._add_background()

        y = 0.8 * self._height
        x1, x2 = 0.05 * self._width,  0.95 * self._width
        self._time = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                  start_date=start_date, end_date=end_date)
        self._tics = time_spacing
        self._add_timeline()

    def _add_background(self):
        background = Rectangle(
            Vector(0, 0), Vector(self._width, self._height),
            'white',
        )
        self._svg.elements.append(background)

    def _add_timeline(self):
        style_major = SvgPathStyle(stroke_width=3)
        style_minor = SvgPathStyle(stroke_width=2)
        text_style = SvgTextStyle()
        line = Line(self._time.source, self._time.target, style=style_major)
        self._svg.elements.append(line)
        timeline_delta = self._time.target - self._time.source
        tic_delta = 10 * timeline_delta.orthogonal()
        for date, label in zip(self._tics.dates, self._tics.labels):
            tic_base = self._time.date_to_coord(date)
            tic_end = tic_base + tic_delta
            self._svg.elements.append(Line(source=tic_base, target=tic_end, style=style_minor))
            self._svg.elements.append(Text(tic_end, text_style, label))

    def add_event(self, event: Event, lane: int = 1, color: str = 'red'):
        line_style = SvgPathStyle(stroke_width=2, color=color)
        text_style = SvgTextStyle()
        lane_shift = 30 * (self._time.target - self._time.source).orthogonal(ccw=True)
        event_base = self._time.date_to_coord(event.date)
        event_end = event_base + lane * lane_shift
        self._svg.elements += [
            Line(source=event_base, target=event_end, style=line_style),
            Circle(center=event_end, radius=3, color=color),
            Text(event_end + 0.5 * lane_shift, text_style, event.text),
        ]

    def save(self, file_path: Path):
        self._svg.save_as(file_path=file_path)
