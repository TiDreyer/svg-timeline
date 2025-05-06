""" classes that define the geometry of the timeline plot """
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from svg_timeline.geometry import Vector
from svg_timeline.time_calculations import TimeGradient


@dataclass
class GeometrySettings:
    """ geometry settings related to the canvas """
    canvas_height: int = 800
    canvas_width: int = 1000
    canvas_x_padding: float = 0.03
    lane_zero_rel_y_position: float = 0.9
    lane_height: float = 30


class TimeLineGeometry:
    """ class for the transfer of dates and lanes to canvas coordinates """
    def __init__(self,
                 start_date: datetime,
                 end_date: datetime,
                 settings: Optional[GeometrySettings] = None,
                 ):
        """
        :param start_date: the lower boundary of the timeline
        :param end_date: the upper boundary of the timeline
        """
        self._settings = settings or GeometrySettings()
        self._first = start_date
        self._last = end_date
        y = self._settings.lane_zero_rel_y_position * self._settings.canvas_height
        x1 = self._settings.canvas_x_padding * self._settings.canvas_width
        x2 = (1 - self._settings.canvas_x_padding) * self._settings.canvas_width
        self._gradient = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                      start_date=start_date, end_date=end_date)

    @property
    def settings(self) -> GeometrySettings:
        """ styling information for the timeline """
        return self._settings

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
        return self._settings.canvas_width

    @property
    def height(self) -> int:
        """ full height of the canvas """
        return self._settings.canvas_height

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
        lane_point = date_coord + lane * self._settings.lane_height * self.lane_normal
        return lane_point
