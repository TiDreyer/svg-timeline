""" classes and functions for easier calculations on datetimes and coordinates """
import calendar
from calendar import weekday
from collections.abc import Iterable
from datetime import datetime

from svg_timeline.geometry import Vector


class TimeGradient:
    """ class for the transfer of dates to canvas coordinates and back """
    def __init__(self, source: Vector, target: Vector, start_date: datetime, end_date: datetime):
        """
        :param source: the point on the canvas that correspond to the start of the gradient
        :param target: the point on the canvas that correspond to the end of the gradient
        :param start_date: the datetime that corresponds to the start of the canvas_vector
        :param end_date: the datetime that corresponds to the end of the canvas_vector
        """
        self._source = source
        self._target = target
        self._start_date = start_date
        self._end_date = end_date

    @property
    def source(self) -> Vector:
        """ the point on the canvas that correspond to the start of the gradient """
        return self._source

    @property
    def target(self) -> Vector:
        """ the point on the canvas that correspond to the end of the gradient """
        return self._target

    @property
    def start_date(self) -> datetime:
        """ the datetime that corresponds to the start of the canvas_vector """
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """ the datetime that corresponds to the end of the canvas_vector """
        return self._end_date

    def coord_to_date(self, coord: Vector) -> datetime:
        """ transform an absolute position on the canvas into a date """
        return self.relative_to_date(self.coord_to_relative(coord=coord))

    def coord_to_relative(self, coord: Vector) -> float:
        """ transform an absolute position on the canvas
        into a relative position on the timeline
        """
        # Transform coordinates so that the timeline start is at (0, 0).
        # (simplifies the following calculations)
        coord_x = coord.x - self._source.x
        coord_y = coord.y - self._source.y
        end_x = self._target.x - self._source.x
        end_y = self._target.y - self._source.y
        # Given a scalar factor 'a', minimize the length of vector 'coord - a * end'.
        # 'a' then describes the relative position on this timeline with the
        # shortest distance to the given coordinates.
        # Solved analytically, this gives:
        numerator = coord_x * end_x + coord_y * end_y
        denominator = end_x**2 + end_y**2
        a = numerator / denominator
        return a

    def date_to_coord(self, date: datetime) -> Vector:
        """ transform a date into a position on the canvas """
        return self.relative_to_coord(self.date_to_relative(date=date))

    def date_to_relative(self, date: datetime) -> float:
        """ transform a date into a relative position on the timeline """
        self_delta = self._end_date - self._start_date
        date_delta = date - self.start_date
        return date_delta / self_delta

    def relative_to_coord(self, relative_position: float) -> Vector:
        """ transform a relative position on the timeline
        into an absolute position on the canvas
        """
        delta = self._target - self._source
        scaled_vector = self._source + (relative_position * delta)
        return scaled_vector

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


def _normalize_month(year: int, month: int = 1) -> (int, int, int):
    """ Helper function to normalize a date after the months have been manually counted up or down
    Note: Does NOT correct the day
    :returns (normalized year, normalized month, n_days in month)
    """
    year += (month - 1) // 12
    month = ((month - 1) % 12) + 1
    _, n_days = calendar.monthrange(year, month)
    return year, month, n_days


def _normalize_date(year: int, month: int = 1, day: int = 1) -> (int, int, int):
    """ Helper function to normalize a date after the days or months have been manually counted up or down
    :returns (normalized year, normalized month, normalized day)
    """
    year, month, n_days = _normalize_month(year=year, month=month)
    while day > n_days:
        month += 1
        day -= n_days
        year, month, n_days = _normalize_month(year=year, month=month)
    while day < 1:
        month -= 1
        year, month, n_days = _normalize_month(year=year, month=month)
        day += n_days
    return year, month, day


def _normalize_time(hour: int = 0, minute: int = 0, second: int = 0) -> (int, int, int, int):
    """ Helper function to normalize a time after the hours, minutes or seconds have been manually counted up or down
    Note: might lead to a day overflow that this function does not handle
    :returns (day overflow, normalized hour, normalized minute, normalized second)
    """
    # normalize seconds
    minute += second // 60
    second = second % 60
    # normalize minutes
    hour += minute // 60
    minute = minute % 60
    # normalize hours
    day_overflow = hour // 24
    hour = hour % 24
    return day_overflow, hour, minute, second


class YearBasedTimeSpacing(TimeSpacing):
    """ base class to return one entry per X years """
    _base = 1

    @property
    def _range(self) -> Iterable:
        first = (self._start_date.year // self._base + 1) * self._base
        last = (self._end_date.year // self._base) * self._base
        return range(first, last + self._base, self._base)

    @property
    def dates(self) -> list[datetime]:
        dates = [datetime(year=year, month=1, day=1)
                 for year in self._range]
        return dates

    @property
    def labels(self) -> list[str]:
        labels = [str(value) for value in self._range]
        return labels


class TimeSpacingPerMillennia(YearBasedTimeSpacing):
    """ return one entry per 1000 years
    Note: ISO 8601 only allows years between 0000 and 9999
    """
    _base = 1000


class TimeSpacingPerCentury(YearBasedTimeSpacing):
    """ return one entry per 100 years """
    _base = 100


class TimeSpacingPerDecade(YearBasedTimeSpacing):
    """ return one entry per 10 years """
    _base = 10


class TimeSpacingPerYear(YearBasedTimeSpacing):
    """ return one entry per year """
    _base = 1


class TimeSpacingPerMonth(TimeSpacing):
    """ return one entry per month """
    @property
    def dates(self) -> list[datetime]:
        year, month, _ = _normalize_month(year=self.start_date.year, month=self.start_date.month + 1)
        date = datetime(year=year, month=month, day=1)
        dates = []
        while date <= self.end_date:
            dates.append(date)
            year, month, _ = _normalize_month(year=year, month=month + 1)
            date = datetime(year=year, month=month, day=1)
        return dates

    @property
    def labels(self) -> list[str]:
        labels = [calendar.month_abbr[date.month] for date in self.dates]
        return labels


class TimeSpacingPerWeek(TimeSpacing):
    """ return one entry per week """
    @property
    def dates(self) -> list[datetime]:
        year, month, day = self.start_date.year, self.start_date.month, self.start_date.day
        year, month, day = _normalize_date(year=year, month=month, day=day + 1)
        while weekday(year, month, day) != 0:
            year, month, day = _normalize_date(year=year, month=month, day=day + 1)
        dates = []
        date = datetime(year=year, month=month, day=day)
        while date <= self.end_date:
            dates.append(date)
            year, month, day = _normalize_date(year=year, month=month, day=day + 7)
            date = datetime(year=year, month=month, day=day)
        return dates

    @property
    def labels(self) -> list[str]:
        labels = [f"{date.isocalendar().week:02}" for date in self.dates]
        return labels


class TimeSpacingPerDay(TimeSpacing):
    """ return one entry per day """
    @property
    def dates(self) -> list[datetime]:
        date_tuple = _normalize_date(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day + 1)
        date = datetime(*date_tuple)
        dates = []
        while date <= self.end_date:
            dates.append(date)
            date_tuple = _normalize_date(year=date.year, month=date.month, day=date.day + 1)
            date = datetime(*date_tuple)
        return dates

    @property
    def labels(self) -> list[str]:
        labels = [str(date.day) for date in self.dates]
        return labels


class TimeSpacingPerHour(TimeSpacing):
    """ return one entry per hour """
    @property
    def dates(self) -> list[datetime]:
        date_tuple = (self.start_date.year, self.start_date.month, self.start_date.day)
        _, hour, _, _ = _normalize_time(hour=self.start_date.hour + 1)
        date = datetime(*date_tuple, hour=hour)
        dates = []
        while date <= self.end_date:
            dates.append(date)
            day_overflow, hour, _, _ = _normalize_time(hour=date.hour + 1)
            date_tuple = _normalize_date(year=date.year, month=date.month, day=date.day + day_overflow)
            date = datetime(*date_tuple, hour=hour)
        return dates

    @property
    def labels(self) -> list[str]:
        labels = [f"{date.hour:02}:00" for date in self.dates]
        return labels
