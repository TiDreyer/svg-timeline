""" classes that define the geometry of the timeline plot """
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from svg_timeline.geometry import Vector
from svg_timeline.time_calculations import TimeGradient


@dataclass
class CanvasGeometry:
    """ geometry settings related to the canvas """
    height: int = 800
    width: int = 1000
    x_padding: float = 0.03


@dataclass
class LaneGeometry:
    """ geometry settings related to the lane definitions """
    lane_zero_y: float = 0.9
    width: float = 30


@dataclass
class TitleGeometry:
    """ geometry settings related to the title elements """
    x_position: float = 1/2
    y_position: float = 1/17
    size_factor: float = 1/15


@dataclass
class EventGeometry:
    """ geometry settings related to the event elements """
    dot_radius: float = 3


@dataclass
class TimespanGeometry:
    """ geometry settings related to the timespan elements """
    width: float = 18


@dataclass
class GeometrySettings:
    canvas: CanvasGeometry = field(default_factory=CanvasGeometry)
    title: TitleGeometry = field(default_factory=TitleGeometry)
    lane: LaneGeometry = field(default_factory=LaneGeometry)
    event: EventGeometry = field(default_factory=EventGeometry)
    timespan: TimespanGeometry = field(default_factory=TimespanGeometry)


class TimeLineGeometry:
    """ class for the transfer of dates and lanes to canvas coordinates """
    def __init__(self,
                 start_date: datetime,
                 end_date: datetime,
                 style: Optional[GeometrySettings] = None,
                 ):
        """
        :param start_date: the lower boundary of the timeline
        :param end_date: the upper boundary of the timeline
        """
        self._style = style or GeometrySettings()
        self._first = start_date
        self._last = end_date
        y = self._style.lane.lane_zero_y * self._style.canvas.height
        x1 = self._style.canvas.x_padding * self._style.canvas.width
        x2 = (1 - self._style.canvas.x_padding) * self._style.canvas.width
        self._gradient = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                      start_date=start_date, end_date=end_date)

    @property
    def style(self) -> GeometrySettings:
        """ styling information for the timeline """
        return self._style

    @property
    def first(self) -> datetime:
        """ first date of the timeline """
        return self._first

    @property
    def last(self) -> datetime:
        """ last date of the timeline """
        return self._last

    @property
    def width(self) -> int:
        """ full width of the canvas """
        return self._style.canvas.width

    @property
    def height(self) -> int:
        """ full height of the canvas """
        return self._style.canvas.height

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
        lane_point = date_coord + lane * self._style.lane.width * self.lane_normal
        return lane_point
