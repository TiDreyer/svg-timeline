""" test cases for the classes defined in the time_calculation module """
from datetime import datetime

from timeliner.time_calculations import TimeGradient
from timeliner.geometry import CanvasPoint, CanvasVector

__DATE_MINUS_ONE = datetime.fromisoformat('2000-01-01T00:00:00')
__DATE_START = datetime.fromisoformat('2000-01-01T10:00:00')
__DATE_HALF = datetime.fromisoformat('2000-01-01T15:00:00')
__DATE_END = datetime.fromisoformat('2000-01-01T20:00:00')
__DATE_PLUS_POINT_TWO = datetime.fromisoformat('2000-01-01T22:00:00')

__COORD_MINUS_ONE = CanvasPoint(-100, 0)
__COORD_START = CanvasPoint(0, 100)
__COORD_HALF = CanvasPoint(50, 150)
__COORD_END = CanvasPoint(100, 200)
__COORD_PLUS_POINT_TWO = CanvasPoint(120, 220)

__TIMELINE = CanvasVector(__COORD_START, __COORD_END)
__GRADIENT = TimeGradient(timeline=__TIMELINE, start_date=__DATE_START, end_date=__DATE_END)


def test_timegradient_init():
    assert __GRADIENT.start_date == __DATE_START
    assert __GRADIENT.end_date == __DATE_END
    assert __GRADIENT.timeline == __TIMELINE


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
    assert __GRADIENT.coord_to_relative(CanvasPoint(0, 200)) == 0.5
    assert __GRADIENT.coord_to_relative(CanvasPoint(100, 100)) == 0.5
    assert __GRADIENT.coord_to_relative(CanvasPoint(-50, 150)) == 0
    assert __GRADIENT.coord_to_relative(CanvasPoint(50, 250)) == 1


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
