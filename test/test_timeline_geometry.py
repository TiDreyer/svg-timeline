""" test cases for the classes defined in the timeline_geometry module """
from datetime import datetime

from pytest import fixture

from svg_timeline.vectors import Vector
from svg_timeline.timeline_geometry import TimeGradient, TimeLineGeometry

__DATESTR_MINUS_ONE = '2000'
__DATESTR_START = '2000-01-01T10'
__DATESTR_HALF = '2000-01-01T15'
__DATESTR_END = '2000-01-01T20'
__DATESTR_PLUS_POINT_TWO = '2000-01-01T22'

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


@fixture(scope='module')
def gradient() -> TimeGradient:
    return TimeGradient(
        source=__COORD_START,
        target=__COORD_END,
        start_date=__DATE_START,
        end_date=__DATE_END,
    )


@fixture(scope='module')
def str_gradient() -> TimeGradient:
    return TimeGradient(
        source=__COORD_START,
        target=__COORD_END,
        start_date=__DATESTR_START,
        end_date=__DATESTR_END,
    )


def test_timegradient_init(gradient):
    assert gradient.start_date == __DATE_START
    assert gradient.end_date == __DATE_END
    assert gradient.source == __COORD_START
    assert gradient.target == __COORD_END


def test_timegradient_init_from_str(gradient, str_gradient):
    assert gradient.start_date == str_gradient.start_date
    assert gradient.end_date == str_gradient.end_date
    assert gradient.source == str_gradient.source
    assert gradient.target == str_gradient.target


def test_timegradient_date_to_coord(gradient):
    assert gradient.date_to_coord(__DATE_MINUS_ONE) == __COORD_MINUS_ONE
    assert gradient.date_to_coord(__DATE_START) == __COORD_START
    assert gradient.date_to_coord(__DATE_HALF) == __COORD_HALF
    assert gradient.date_to_coord(__DATE_END) == __COORD_END
    assert gradient.date_to_coord(__DATE_PLUS_POINT_TWO) == __COORD_PLUS_POINT_TWO


def test_timegradient_date_to_coord_from_str(gradient):
    assert gradient.date_to_coord(__DATESTR_MINUS_ONE) == __COORD_MINUS_ONE
    assert gradient.date_to_coord(__DATESTR_START) == __COORD_START
    assert gradient.date_to_coord(__DATESTR_HALF) == __COORD_HALF
    assert gradient.date_to_coord(__DATESTR_END) == __COORD_END
    assert gradient.date_to_coord(__DATESTR_PLUS_POINT_TWO) == __COORD_PLUS_POINT_TWO


def test_timegradient_date_to_relative(gradient):
    assert gradient.date_to_relative(__DATE_MINUS_ONE) == -1
    assert gradient.date_to_relative(__DATE_START) == 0
    assert gradient.date_to_relative(__DATE_HALF) == 0.5
    assert gradient.date_to_relative(__DATE_END) == 1
    assert gradient.date_to_relative(__DATE_PLUS_POINT_TWO) == 1.2


def test_timegradient_date_to_relative_from_str(gradient):
    assert gradient.date_to_relative(__DATESTR_MINUS_ONE) == -1
    assert gradient.date_to_relative(__DATESTR_START) == 0
    assert gradient.date_to_relative(__DATESTR_HALF) == 0.5
    assert gradient.date_to_relative(__DATESTR_END) == 1
    assert gradient.date_to_relative(__DATESTR_PLUS_POINT_TWO) == 1.2


def test_timegradient_coord_to_date(gradient):
    assert gradient.coord_to_date(__COORD_MINUS_ONE) == __DATE_MINUS_ONE
    assert gradient.coord_to_date(__COORD_START) == __DATE_START
    assert gradient.coord_to_date(__COORD_HALF) == __DATE_HALF
    assert gradient.coord_to_date(__COORD_END) == __DATE_END
    assert gradient.coord_to_date(__COORD_PLUS_POINT_TWO) == __DATE_PLUS_POINT_TWO


def test_timegradient_coord_to_relative(gradient):
    assert gradient.coord_to_relative(__COORD_MINUS_ONE) == -1
    assert gradient.coord_to_relative(__COORD_START) == 0
    assert gradient.coord_to_relative(__COORD_HALF) == 0.5
    assert gradient.coord_to_relative(__COORD_END) == 1
    assert gradient.coord_to_relative(__COORD_PLUS_POINT_TWO) == 1.2
    # points that are not directly on the timeline
    assert gradient.coord_to_relative(Vector(0, 200)) == 0.5
    assert gradient.coord_to_relative(Vector(100, 100)) == 0.5
    assert gradient.coord_to_relative(Vector(-50, 150)) == 0
    assert gradient.coord_to_relative(Vector(50, 250)) == 1


def test_timegradient_relative_to_coord(gradient):
    assert gradient.relative_to_coord(-1) == __COORD_MINUS_ONE
    assert gradient.relative_to_coord(0) == __COORD_START
    assert gradient.relative_to_coord(0.5) == __COORD_HALF
    assert gradient.relative_to_coord(1) == __COORD_END
    assert gradient.relative_to_coord(1.2) == __COORD_PLUS_POINT_TWO


def test_timegradient_relative_to_date(gradient):
    assert gradient.relative_to_date(-1) == __DATE_MINUS_ONE
    assert gradient.relative_to_date(0) == __DATE_START
    assert gradient.relative_to_date(0.5) == __DATE_HALF
    assert gradient.relative_to_date(1) == __DATE_END
    assert gradient.relative_to_date(1.2) == __DATE_PLUS_POINT_TWO


def test_init_timelinegeometry_from_string():
    from_date = TimeLineGeometry(__DATE_START, __DATE_END)
    from_str = TimeLineGeometry(__DATESTR_START, __DATESTR_END)
    assert from_date.first == from_str.first
    assert from_date.last == from_str.last
    assert from_date.as_coord(__DATE_HALF) == from_str.as_coord(__DATESTR_HALF)
    assert from_date.as_coord(__DATESTR_HALF) == from_str.as_coord(__DATE_HALF)
