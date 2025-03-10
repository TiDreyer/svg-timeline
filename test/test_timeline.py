from datetime import datetime

from pytest import raises

from svg_timeline.timeline import TimelinePlot
from svg_timeline.time_calculations import TimeSpacingPerYear


def test_connected_events_raises_on_length():
    """ the lists passed to add_connected_events need to have the same length
    otherwise the call should raise a RuntimeError """
    start_date = datetime.fromisoformat('2000-01-01')
    end_date = datetime.fromisoformat('2010-12-31')
    tlp = TimelinePlot(
        start_date=start_date,
        end_date=end_date,
        time_spacing=TimeSpacingPerYear(start_date, end_date),
    )
    # first correct usage examples:
    tlp.add_connected_events(dates=[start_date, end_date], labels=['adsf', 'asdfas'])
    tlp.add_connected_events(dates=[start_date, end_date], labels=['adsf', 'asdfas'], classes=[[], []])
    tlp.add_connected_events(dates=[start_date, end_date], labels=['adsf', 'asdfas'], classes=[['color_a', 'asdf'], ['color_e']])
    # mis-matched lengths:
    with raises(RuntimeError):
        tlp.add_connected_events(dates=[start_date], labels=[])
    with raises(RuntimeError):
        tlp.add_connected_events(dates=[start_date, end_date], labels=['adsf'])
    with raises(RuntimeError):
        tlp.add_connected_events(dates=[start_date], labels=['adsf', 'asdfas'])
    with raises(RuntimeError):
        tlp.add_connected_events(dates=[start_date, end_date], labels=['adsf', 'asdfas'], classes=[])
    with raises(RuntimeError):
        tlp.add_connected_events(dates=[start_date, end_date], labels=['adsf', 'asdfas'], classes=[['color_a']])
