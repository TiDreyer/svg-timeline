""" test cases for the classes defined in the time_calculation module """
from datetime import datetime

from svg_timeline.time_calculations import TimeGradient
from svg_timeline.time_calculations import _normalize_month, _normalize_date, _normalize_time
from svg_timeline.time_calculations import TimeSpacingPerMillennia, TimeSpacingPerCentury, TimeSpacingPerDecade
from svg_timeline.time_calculations import TimeSpacingPerYear, TimeSpacingPerMonth, TimeSpacingPerWeek, TimeSpacingPerDay
from svg_timeline.time_calculations import TimeSpacingPerHour
from svg_timeline.geometry import Vector

__DATE_MINUS_ONE = datetime.fromisoformat('2000-01-01T00:00:00')
__DATE_START = datetime.fromisoformat('2000-01-01T10:00:00')
__DATE_HALF = datetime.fromisoformat('2000-01-01T15:00:00')
__DATE_END = datetime.fromisoformat('2000-01-01T20:00:00')
__DATE_PLUS_POINT_TWO = datetime.fromisoformat('2000-01-01T22:00:00')

__COORD_MINUS_ONE = Vector(-100, 0)
__COORD_START = Vector(0, 100)
__COORD_HALF = Vector(50, 150)
__COORD_END = Vector(100, 200)
__COORD_PLUS_POINT_TWO = Vector(120, 220)

__GRADIENT = TimeGradient(source=__COORD_START, target=__COORD_END, start_date=__DATE_START, end_date=__DATE_END)


def test_timegradient_init():
    assert __GRADIENT.start_date == __DATE_START
    assert __GRADIENT.end_date == __DATE_END
    assert __GRADIENT.source == __COORD_START
    assert __GRADIENT.target == __COORD_END


def test_timegradient_date_to_coord():
    assert __GRADIENT.date_to_coord(__DATE_MINUS_ONE) == __COORD_MINUS_ONE
    assert __GRADIENT.date_to_coord(__DATE_START) == __COORD_START
    assert __GRADIENT.date_to_coord(__DATE_HALF) == __COORD_HALF
    assert __GRADIENT.date_to_coord(__DATE_END) == __COORD_END
    assert __GRADIENT.date_to_coord(__DATE_PLUS_POINT_TWO) == __COORD_PLUS_POINT_TWO


def test_timegradient_date_to_relative():
    assert __GRADIENT.date_to_relative(__DATE_MINUS_ONE) == -1
    assert __GRADIENT.date_to_relative(__DATE_START) == 0
    assert __GRADIENT.date_to_relative(__DATE_HALF) == 0.5
    assert __GRADIENT.date_to_relative(__DATE_END) == 1
    assert __GRADIENT.date_to_relative(__DATE_PLUS_POINT_TWO) == 1.2


def test_timegradient_coord_to_date():
    assert __GRADIENT.coord_to_date(__COORD_MINUS_ONE) == __DATE_MINUS_ONE
    assert __GRADIENT.coord_to_date(__COORD_START) == __DATE_START
    assert __GRADIENT.coord_to_date(__COORD_HALF) == __DATE_HALF
    assert __GRADIENT.coord_to_date(__COORD_END) == __DATE_END
    assert __GRADIENT.coord_to_date(__COORD_PLUS_POINT_TWO) == __DATE_PLUS_POINT_TWO


def test_timegradient_coord_to_relative():
    assert __GRADIENT.coord_to_relative(__COORD_MINUS_ONE) == -1
    assert __GRADIENT.coord_to_relative(__COORD_START) == 0
    assert __GRADIENT.coord_to_relative(__COORD_HALF) == 0.5
    assert __GRADIENT.coord_to_relative(__COORD_END) == 1
    assert __GRADIENT.coord_to_relative(__COORD_PLUS_POINT_TWO) == 1.2
    # points that are not directly on the timeline
    assert __GRADIENT.coord_to_relative(Vector(0, 200)) == 0.5
    assert __GRADIENT.coord_to_relative(Vector(100, 100)) == 0.5
    assert __GRADIENT.coord_to_relative(Vector(-50, 150)) == 0
    assert __GRADIENT.coord_to_relative(Vector(50, 250)) == 1


def test_timegradient_relative_to_coord():
    assert __GRADIENT.relative_to_coord(-1) == __COORD_MINUS_ONE
    assert __GRADIENT.relative_to_coord(0) == __COORD_START
    assert __GRADIENT.relative_to_coord(0.5) == __COORD_HALF
    assert __GRADIENT.relative_to_coord(1) == __COORD_END
    assert __GRADIENT.relative_to_coord(1.2) == __COORD_PLUS_POINT_TWO


def test_timegradient_relative_to_date():
    assert __GRADIENT.relative_to_date(-1) == __DATE_MINUS_ONE
    assert __GRADIENT.relative_to_date(0) == __DATE_START
    assert __GRADIENT.relative_to_date(0.5) == __DATE_HALF
    assert __GRADIENT.relative_to_date(1) == __DATE_END
    assert __GRADIENT.relative_to_date(1.2) == __DATE_PLUS_POINT_TWO


def test_normalize_month():
    # month too low
    assert _normalize_month(year=2020, month=-20) == (2018, 4, 30)
    assert _normalize_month(year=2020, month=-12) == (2018, 12, 31)
    assert _normalize_month(year=2020, month=-11) == (2019, 1, 31)
    assert _normalize_month(year=2020, month=-2) == (2019, 10, 31)
    assert _normalize_month(year=2020, month=0) == (2019, 12, 31)
    # month ok
    assert _normalize_month(year=2020, month=1) == (2020, 1, 31)
    assert _normalize_month(year=2020, month=12) == (2020, 12, 31)
    # month too high
    assert _normalize_month(year=2020, month=13) == (2021, 1, 31)
    assert _normalize_month(year=2020, month=15) == (2021, 3, 31)
    assert _normalize_month(year=2020, month=30) == (2022, 6, 30)


def test_normalize_date():
    # non-leap year
    assert _normalize_date(year=2021, month=2, day=29) == (2021, 3, 1)
    assert _normalize_date(year=2021, month=1, day=182) == (2021, 7, 1)
    # leap year
    assert _normalize_date(year=2020, month=2, day=29) == (2020, 2, 29)
    assert _normalize_date(year=2020, month=1, day=182) == (2020, 6, 30)
    # negative days
    assert _normalize_date(year=2020, month=1, day=0) == (2019, 12, 31)
    assert _normalize_date(year=2020, month=1, day=-31) == (2019, 11, 30)
    # combination of days and months
    assert _normalize_date(year=2020, month=13, day=32) == (2021, 2, 1)
    assert _normalize_date(year=2020, month=0, day=0) == (2019, 11, 30)


def test_normalize_time():
    # unchanged time
    assert _normalize_time(hour=2, minute=34, second=56) == (0, 2, 34, 56)
    # single overflow
    assert _normalize_time(hour=0, minute=0, second=0) == (0, 0, 0, 0)
    assert _normalize_time(hour=0, minute=0, second=60) == (0, 0, 1, 0)
    assert _normalize_time(hour=0, minute=60, second=0) == (0, 1, 0, 0)
    assert _normalize_time(hour=24, minute=0, second=0) == (1, 0, 0, 0)
    # multiple overflows
    assert _normalize_time(hour=24, minute=60, second=60) == (1, 1, 1, 0)
    assert _normalize_time(hour=100, minute=123, second=123) == (4, 6, 5, 3)
    # negative overflows
    assert _normalize_time(hour=0, minute=0, second=-1) == (-1, 23, 59, 59)
    assert _normalize_time(hour=-100, minute=-123, second=-123) == (-5, 17, 54, 57)


def test_time_spacing_per_millennia():
    spacing = TimeSpacingPerMillennia(
        datetime.fromisoformat('0030-01-02'),
        datetime.fromisoformat('4005-01-02'),
    )
    assert spacing.labels == ['1000', '2000', '3000', '4000']
    assert spacing.dates == [
        datetime.fromisoformat('1000-01-01T00:00:00'),
        datetime.fromisoformat('2000-01-01T00:00:00'),
        datetime.fromisoformat('3000-01-01T00:00:00'),
        datetime.fromisoformat('4000-01-01T00:00:00'),
    ]


def test_time_spacing_per_century():
    spacing = TimeSpacingPerCentury(
        datetime.fromisoformat('1523-01-02'),
        datetime.fromisoformat('2105-01-02'),
    )
    assert spacing.labels == ['1600', '1700', '1800', '1900', '2000', '2100']
    assert spacing.dates == [
        datetime.fromisoformat('1600-01-01T00:00:00'),
        datetime.fromisoformat('1700-01-01T00:00:00'),
        datetime.fromisoformat('1800-01-01T00:00:00'),
        datetime.fromisoformat('1900-01-01T00:00:00'),
        datetime.fromisoformat('2000-01-01T00:00:00'),
        datetime.fromisoformat('2100-01-01T00:00:00'),
    ]


def test_time_spacing_per_decade():
    spacing = TimeSpacingPerDecade(
        datetime.fromisoformat('1964-01-02'),
        datetime.fromisoformat('2010-01-02'),
    )
    assert spacing.labels == ['1970', '1980', '1990', '2000', '2010']
    assert spacing.dates == [
        datetime.fromisoformat('1970-01-01T00:00:00'),
        datetime.fromisoformat('1980-01-01T00:00:00'),
        datetime.fromisoformat('1990-01-01T00:00:00'),
        datetime.fromisoformat('2000-01-01T00:00:00'),
        datetime.fromisoformat('2010-01-01T00:00:00'),
    ]


def test_time_spacing_per_year():
    spacing = TimeSpacingPerYear(
        datetime.fromisoformat('2000-01-02'),
        datetime.fromisoformat('2005-01-02'),
    )
    assert spacing.labels == ['2001', '2002', '2003', '2004', '2005']
    assert spacing.dates == [
        datetime.fromisoformat('2001-01-01T00:00:00'),
        datetime.fromisoformat('2002-01-01T00:00:00'),
        datetime.fromisoformat('2003-01-01T00:00:00'),
        datetime.fromisoformat('2004-01-01T00:00:00'),
        datetime.fromisoformat('2005-01-01T00:00:00'),
    ]


def test_time_spacing_per_month():
    spacing = TimeSpacingPerMonth(
        datetime.fromisoformat('1999-10-02'),
        datetime.fromisoformat('2000-03-02'),
    )
    assert spacing.labels == ['Nov', 'Dec', 'Jan', 'Feb', 'Mar']
    assert spacing.dates == [
        datetime.fromisoformat('1999-11-01T00:00:00'),
        datetime.fromisoformat('1999-12-01T00:00:00'),
        datetime.fromisoformat('2000-01-01T00:00:00'),
        datetime.fromisoformat('2000-02-01T00:00:00'),
        datetime.fromisoformat('2000-03-01T00:00:00'),
    ]


def test_time_spacing_per_week():
    spacing = TimeSpacingPerWeek(
        datetime.fromisoformat('2024-12-12'),
        datetime.fromisoformat('2025-01-22'),
    )
    assert spacing.labels == ['51', '52', '01', '02', '03', '04']
    assert spacing.dates == [
        datetime.fromisoformat('2024-12-16T00:00:00'),
        datetime.fromisoformat('2024-12-23T00:00:00'),
        datetime.fromisoformat('2024-12-30T00:00:00'),
        datetime.fromisoformat('2025-01-06T00:00:00'),
        datetime.fromisoformat('2025-01-13T00:00:00'),
        datetime.fromisoformat('2025-01-20T00:00:00'),
    ]


def test_time_spacing_per_day():
    spacing = TimeSpacingPerDay(
        datetime.fromisoformat('1999-12-29'),
        datetime.fromisoformat('2000-01-02'),
    )
    assert spacing.labels == ['30', '31', '1', '2']
    assert spacing.dates == [
        datetime.fromisoformat('1999-12-30T00:00:00'),
        datetime.fromisoformat('1999-12-31T00:00:00'),
        datetime.fromisoformat('2000-01-01T00:00:00'),
        datetime.fromisoformat('2000-01-02T00:00:00'),
    ]


def test_time_spacing_per_day_bug_01():
    """ With these dates, the properties dates and values threw an ValueError """
    spacing = TimeSpacingPerDay(
        datetime.fromisoformat('2024-12-31'),
        datetime.fromisoformat('2025-04-02'),
    )
    dates = spacing.dates
    labels = spacing.labels
    assert len(dates) == len(labels)


def test_time_spacing_per_hour():
    spacing = TimeSpacingPerHour(
        datetime.fromisoformat('1999-12-31T20:35:56'),
        datetime.fromisoformat('2000-01-01T03:35:56'),
    )
    assert spacing.labels == ['21:00', '22:00', '23:00', '00:00', '01:00', '02:00', '03:00']
    assert spacing.dates == [
        datetime.fromisoformat('1999-12-31T21:00:00'),
        datetime.fromisoformat('1999-12-31T22:00:00'),
        datetime.fromisoformat('1999-12-31T23:00:00'),
        datetime.fromisoformat('2000-01-01T00:00:00'),
        datetime.fromisoformat('2000-01-01T01:00:00'),
        datetime.fromisoformat('2000-01-01T02:00:00'),
        datetime.fromisoformat('2000-01-01T03:00:00'),
    ]
