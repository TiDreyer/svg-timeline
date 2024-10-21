""" classes and functions for easier calculations on datetimes and coordinates """
from datetime import datetime

from timeliner.geometry import CanvasVector, CanvasPoint


class TimeGradient:
    """ class for the transfer of dates to canvas coordinates and back """
    def __init__(self, timeline: CanvasVector, start_date: datetime, end_date: datetime):
        """
        :param timeline: the vector on the canvas that correspond to the given times
        :param start_date: the datetime that corresponds to the start of the canvas_vector
        :param end_date: the datetime that corresponds to the end of the canvas_vector
        """
        self._timeline = timeline
        self._start_date = start_date
        self._end_date = end_date

    @property
    def timeline(self) -> CanvasVector:
        """ the vector on the canvas that correspond to the given times """
        return self._timeline

    @property
    def start_date(self) -> datetime:
        """ the datetime that corresponds to the start of the canvas_vector """
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """ the datetime that corresponds to the end of the canvas_vector """
        return self._end_date

    def coord_to_date(self, coord: CanvasPoint) -> datetime:
        """ transform an absolute position on the canvas into a date """
        return self.relative_to_date(self.coord_to_relative(coord=coord))

    def coord_to_relative(self, coord: CanvasPoint) -> float:
        """ transform an absolute position on the canvas
        into a relative position on the timeline
        """
        # Transform coordinates so that the timeline start is at (0, 0).
        # (simplifies the following calculations)
        coord_x = coord.x - self._timeline.initial_point.x
        coord_y = coord.y - self._timeline.initial_point.y
        end_x = self._timeline.terminal_point.x - self._timeline.initial_point.x
        end_y = self._timeline.terminal_point.y - self._timeline.initial_point.y
        # Given a scalar factor 'a', minimize the length of vector 'coord - a * end'.
        # 'a' then describes the relative position on this timeline with the
        # shortest distance to the given coordinates.
        # Solved analytically, this gives:
        numerator = coord_x * end_x + coord_y * end_y
        denominator = end_x**2 + end_y**2
        a = numerator / denominator
        return a

    def date_to_coord(self, date: datetime) -> CanvasPoint:
        """ transform a date into a position on the canvas """
        return self.relative_to_coord(self.date_to_relative(date=date))

    def date_to_relative(self, date: datetime) -> float:
        """ transform a date into a relative position on the timeline """
        self_delta = self._end_date - self._start_date
        date_delta = date - self.start_date
        return date_delta / self_delta

    def relative_to_coord(self, relative_position: float) -> CanvasPoint:
        """ transform a relative position on the timeline
        into an absolute position on the canvas
        """
        scaled_vector = relative_position * self._timeline
        return scaled_vector.terminal_point

    def relative_to_date(self, relative_position: float) -> datetime:
        """ transform a relative position on the timeline into a date """
        delta = self._end_date - self._start_date
        return self._start_date + relative_position * delta


class TimeSpacing:
    """ base class for semantic datetime spacing within a given range """
    def __init__(self, start_date: datetime, end_date: datetime):
        if not start_date < end_date:
            raise ValueError("start date needs to be smaller than end date")
        self._start_date = start_date
        self._end_date = end_date

    @property
    def start_date(self) -> datetime:
        """ the datetime that corresponds to the start of the time range """
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """ the datetime that corresponds to the end of the time range """
        return self._end_date

    @property
    def labels(self) -> list[str]:
        """ Tic labels
        :return list of tic labels as strings
        """
        raise NotImplementedError

    @property
    def dates(self) -> list[datetime]:
        """ Positions of the tics
        :return list of tic positions as datetime objects
        """
        raise NotImplementedError
