""" high level timeline API classes """
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from timeliner.geometry import Vector
from timeliner.svg import SVG
from timeliner.svg_primitives import Rectangle, Line, Text, Circle, Image
from timeliner.svg_style import SvgPathStyle, SvgTextStyle
from timeliner.time_calculations import TimeGradient, TimeSpacing


@dataclass
class Event:
    date: datetime
    text: str


@dataclass
class DatedImage:
    date: datetime
    file_path: Path


@dataclass
class TimeSpan:
    start_date: datetime
    end_date: datetime
    text: str


class TimelinePlot:
    def __init__(self, start_date: datetime, end_date: datetime,
                 time_spacing: TimeSpacing, minor_tics: Optional[TimeSpacing] = None,
                 size: tuple[int, int] = (800, 600)):
        self._width, self._height = size
        self._svg = SVG(self._width, self._height)
        self._add_background()

        y = 0.8 * self._height
        x1, x2 = 0.05 * self._width,  0.95 * self._width
        self._time = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                  start_date=start_date, end_date=end_date)
        self._tics = time_spacing
        self._tics_minor = minor_tics
        self._add_timeline()

    def _add_background(self):
        background = Rectangle(
            Vector(0, 0), Vector(self._width, self._height),
            'white',
        )
        self._svg.elements.append(background)

    def _add_timeline(self):
        style_arrow = SvgPathStyle(stroke_width=3)
        style_major = SvgPathStyle(stroke_width=2)
        style_minor = SvgPathStyle(stroke_width=1)
        text_style = SvgTextStyle()
        line = Line(self._time.source, self._time.target, style=style_arrow)
        self._svg.elements.append(line)
        timeline_delta = self._time.target - self._time.source
        tic_delta = 10 * timeline_delta.orthogonal()
        for date, label in zip(self._tics.dates, self._tics.labels):
            tic_base = self._time.date_to_coord(date)
            tic_end = tic_base + tic_delta
            text_start = tic_base + 1.5 * tic_delta
            self._svg.elements.append(Line(source=tic_base, target=tic_end, style=style_major))
            self._svg.elements.append(Text(text_start, text_style, label))
        if self._tics_minor is None:
            return
        for date in self._tics_minor.dates:
            tic_base = self._time.date_to_coord(date)
            tic_end = tic_base + 0.5 * tic_delta
            self._svg.elements.append(Line(source=tic_base, target=tic_end, style=style_minor))

    def add_event(self, event: Event, lane: int = 1, color: str = 'red'):
        line_style = SvgPathStyle(stroke_width=2, color=color)
        text_style = SvgTextStyle()
        event_base = self._time.date_to_coord(event.date)
        event_end = self.__to_lane_point(event.date, lane=lane)
        text_coord = self.__to_lane_point(event.date, lane=(lane+0.5))
        self._svg.elements += [
            Line(source=event_base, target=event_end, style=line_style),
            Circle(center=event_end, radius=3, color=color),
            Text(text_coord, text_style, event.text),
        ]

    def add_image(self, image: DatedImage, height: float, width: float, lane: int = 1, color: str = 'black'):
        line_style = SvgPathStyle(stroke_width=2, color=color)
        event_base = self._time.date_to_coord(image.date)
        event_end = self.__to_lane_point(image.date, lane=lane)
        image_top_left = event_end + height * self.lane_normal + width/2 * self.lane_normal.orthogonal(ccw=True)
        self._svg.elements += [
            Line(source=event_base, target=event_end, style=line_style),
            Image(top_left=image_top_left, file=image.file_path, height=height, width=width),
        ]

    def add_timespan(self, timespan: TimeSpan, lane: int = 1, color: str = 'red', width: float = 13):
        text_style = SvgTextStyle(font_size=0.8*width)
        start_corner = self.__to_lane_point(timespan.start_date, lane=lane) + width/2 * self.lane_normal
        end_corner = self.__to_lane_point(timespan.end_date, lane=lane) - width/2 * self.lane_normal
        middle_date = timespan.start_date + (timespan.end_date - timespan.start_date) / 2
        text_coord = self.__to_lane_point(middle_date, lane=lane)
        self._svg.elements += [
            Rectangle(start_corner, end_corner, color=color),
            Text(text_coord, text_style, timespan.text),
        ]

    @property
    def lane_normal(self) -> Vector:
        return (self._time.target - self._time.source).orthogonal(ccw=True)

    def __to_lane_point(self, date: datetime, lane: float = 1, lane_height: int = 20) -> Vector:
        date_coord = self._time.date_to_coord(date)
        lane_point = date_coord + lane * lane_height * self.lane_normal
        return lane_point

    def save(self, file_path: Path):
        self._svg.save_as(file_path=file_path)
