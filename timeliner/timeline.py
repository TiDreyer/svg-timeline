""" high level timeline API classes """
from datetime import datetime
from pathlib import Path
from typing import Optional

from timeliner.geometry import Vector
from timeliner.style import TimelineStyle
from timeliner.svg import SVG
from timeliner.svg_primitives import Rectangle, Line, Text, Circle, Image
from timeliner.svg_style import SvgPathStyle, SvgTextStyle
from timeliner.time_calculations import TimeGradient, TimeSpacing


class TimelinePlot:
    def __init__(self, start_date: datetime, end_date: datetime,
                 time_spacing: TimeSpacing, minor_tics: Optional[TimeSpacing] = None,
                 size: tuple[int, int] = (800, 600)):
        self._width, self._height = size
        self._svg = SVG(self._width, self._height)
        self._add_background()

        y = TimelineStyle.arrow_y_position * self._height
        x1 = TimelineStyle.arrow_x_padding * self._width
        x2 = (1 - TimelineStyle.arrow_x_padding) * self._width
        self._time = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                  start_date=start_date, end_date=end_date)
        self._tics = time_spacing
        self._tics_minor = minor_tics
        self._add_timeline()

    def _add_background(self):
        background = Rectangle(
            Vector(0, 0), Vector(self._width, self._height),
            TimelineStyle.bg_clor,
        )
        self._svg.elements.append(background)

    def _add_timeline(self):
        style_arrow = SvgPathStyle(stroke_width=TimelineStyle.arrow_stroke_width)
        style_major = SvgPathStyle(stroke_width=TimelineStyle.major_stroke_width)
        style_minor = SvgPathStyle(stroke_width=TimelineStyle.minor_stroke_width)
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

    def add_event(self, date: datetime, text: str,
                  lane: int = 1, color: Optional[str] = None):
        color = color or TimelineStyle.event_color
        line_style = SvgPathStyle(stroke_width=TimelineStyle.event_stroke_width, color=color)
        text_style = SvgTextStyle()
        event_base = self._time.date_to_coord(date)
        event_end = self.__to_lane_point(date, lane=lane)
        text_coord = self.__to_lane_point(date, lane=(lane+0.5))
        self._svg.elements += [
            Line(source=event_base, target=event_end, style=line_style),
            Circle(center=event_end, radius=TimelineStyle.event_dot_radius, color=color),
            Text(text_coord, text_style, text),
        ]

    def add_image(self, date: datetime, image_path: Path, height: float, width: float,
                  lane: int = 1, color: Optional[str] = None):
        line_style = SvgPathStyle(stroke_width=TimelineStyle.image_stroke_width,
                                  color=color or TimelineStyle.image_color)
        event_base = self._time.date_to_coord(date)
        event_end = self.__to_lane_point(date, lane=lane)
        image_top_left = event_end + height * self.lane_normal + width/2 * self.lane_normal.orthogonal(ccw=True)
        self._svg.elements += [
            Line(source=event_base, target=event_end, style=line_style),
            Image(top_left=image_top_left, file=image_path, height=height, width=width),
        ]

    def add_timespan(self, start_date: datetime, end_date: datetime, text: str,
                     lane: int = 1, color: Optional[str] = None,
                     text_color: Optional[str] = None, width: Optional[int] = None):
        width = width or TimelineStyle.timespan_width
        text_style = SvgTextStyle(text_color=text_color or TimelineStyle.timespan_text_color,
                                  font_size=TimelineStyle.timespan_text_size_factor * width)
        start_corner = self.__to_lane_point(start_date, lane=lane) + width/2 * self.lane_normal
        end_corner = self.__to_lane_point(end_date, lane=lane) - width/2 * self.lane_normal
        middle_date = start_date + (end_date - start_date) / 2
        text_coord = self.__to_lane_point(middle_date, lane=lane)
        self._svg.elements += [
            Rectangle(start_corner, end_corner, color=color or TimelineStyle.timespan_bg_color),
            Text(text_coord, text_style, text),
        ]

    def add_title(self, title: str):
        text_style = SvgTextStyle(
            text_color=TimelineStyle.title_text_color,
            font_size=int(self._height*TimelineStyle.title_size_factor),
        )
        text_coord = Vector(x=int(self._width * TimelineStyle.title_x_position),
                            y=int(self._height * TimelineStyle.title_y_position))
        self._svg.elements += [Text(text_coord, text_style, title)]

    @property
    def lane_normal(self) -> Vector:
        return (self._time.target - self._time.source).orthogonal(ccw=True)

    def __to_lane_point(self, date: datetime, lane: float = 1) -> Vector:
        date_coord = self._time.date_to_coord(date)
        lane_point = date_coord + lane * TimelineStyle.lane_width * self.lane_normal
        return lane_point

    def save(self, file_path: Path):
        self._svg.save_as(file_path=file_path)
