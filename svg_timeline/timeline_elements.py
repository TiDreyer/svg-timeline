from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from svg_timeline.geometry import Vector
from svg_timeline.style import Defaults, ClassNames
from svg_timeline.svg import SvgGroup
from svg_timeline.svg_primitives import Line, Text, Circle
from svg_timeline.time_calculations import TimeGradient, TimeSpacing


Classes = Optional[list[str]]


class TimeLineCoordinates:
    """ class for the transfer of dates and lanes to canvas coordinates """
    def __init__(self,
                 start_date: datetime,
                 end_date: datetime,
                 canvas_size: tuple[int, int],
                 major_tics: TimeSpacing,
                 minor_tics: Optional[TimeSpacing] = None,
                 ):
        """
        :param start_date: the lower boundary of the timeline
        :param end_date: the upper boundary of the timeline
        :param canvas_size: the width and height of the canvas in pixel
        :param major_tics: the spacing of the major tics drawn on the time arrow
        :param minor_tics: [optional] the spacing of the minor tics drawn on the time arrow
        """
        width, height = canvas_size
        y = Defaults.arrow_y_position * height
        x1 = Defaults.arrow_x_padding * width
        x2 = (1 - Defaults.arrow_x_padding) * width
        self._gradient = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                      start_date=start_date, end_date=end_date)
        self._tics_major = major_tics
        self._tics_minor = minor_tics

    @property
    def lane_normal(self) -> Vector:
        """ Normal vector orthogonal to the timeline direction
        This vector is used to calculate the positions of the different lanes.
        """
        return (self._gradient.target - self._gradient.source).orthogonal(ccw=True)

    def as_coord(self, date: datetime, lane: float = 0) -> Vector:
        """ return the coordinates responding to this date on a given lane
        (default: on the time arrow)
        """
        date_coord = self._gradient.date_to_coord(date)
        lane_point = date_coord + lane * Defaults.lane_width * self.lane_normal
        return lane_point

    @property
    def time_arrow(self) -> SvgGroup:
        """ the svg representation of the time arrow and its tics """
        timeline = SvgGroup(id_base='timeline')
        line = Line(self._gradient.source, self._gradient.target, classes=[ClassNames.TIMEAXIS])
        timeline.append(line)
        timeline_delta = self._gradient.target - self._gradient.source
        tic_delta = 10 * timeline_delta.orthogonal()
        major_tics = SvgGroup(id_base='tics')
        for date, label in zip(self._tics_major.dates, self._tics_major.labels):
            tic_base = self._gradient.date_to_coord(date)
            tic_end = tic_base + tic_delta
            text_start = tic_base + 1.5 * tic_delta
            major_tics.append(Line(source=tic_base, target=tic_end, classes=[ClassNames.MAJOR_TICK]))
            major_tics.append(Text(text_start, label, classes=[ClassNames.MAJOR_TICK]))
        timeline.append(major_tics)
        if self._tics_minor is None:
            return timeline
        minor_tics = SvgGroup(id_base='tics')
        for date in self._tics_minor.dates:
            tic_base = self._gradient.date_to_coord(date)
            tic_end = tic_base + 0.5 * tic_delta
            minor_tics.append(Line(source=tic_base, target=tic_end, classes=[ClassNames.MINOR_TICK]))
        timeline.append(minor_tics)
        return timeline


class TimeLineElement(ABC):
    """ interface definition for timeline elements """
    def svg(self, coord: TimeLineCoordinates) -> SvgGroup:
        raise NotImplementedError


@dataclass
class Event(TimeLineElement):
    """ an event that happened at a single point in time """
    date: datetime
    text: str
    lane: float = 1
    classes: Classes = None

    def svg(self, coord: TimeLineCoordinates) -> SvgGroup:
        classes = self.classes or []
        classes += [ClassNames.EVENT]
        event_base = coord.as_coord(self.date)
        event_end = coord.as_coord(self.date, lane=self.lane)
        text_coord = coord.as_coord(self.date, lane=(self.lane + 0.5 if self.lane >= 0 else self.lane - 0.5))
        event = SvgGroup([
            Line(source=event_base, target=event_end, classes=classes),
            Circle(center=event_end, radius=Defaults.event_dot_radius, classes=classes),
            Text(text_coord, self.text, classes=classes),
        ], id_base='event')
        return event
