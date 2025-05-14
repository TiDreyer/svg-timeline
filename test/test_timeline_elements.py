from datetime import datetime

from pytest import raises

from svg_timeline.timeline_elements import ConnectedEvents


def test_connected_events_raises_on_length():
    """ the lists passed to ConnectedEvents need to have the same length
    otherwise the call should raise a ValueError """
    date_1 = datetime.fromisoformat('2000-01-01')
    date_2 = datetime.fromisoformat('2010-12-31')
    # first correct usage examples:
    _ = ConnectedEvents(dates=[date_1, date_2], labels=['adsf', 'asdfas'])
    _ = ConnectedEvents(dates=[date_1, date_2], labels=['adsf', 'asdfas'], individual_classes=[[], []])
    _ = ConnectedEvents(dates=[date_1, date_2], labels=['adsf', 'asdfas'], individual_classes=[['color_a', 'asdf'], ['color_e']])
    # mis-matched lengths:
    with raises(ValueError):
        _ = ConnectedEvents(dates=[date_1], labels=[])
    with raises(ValueError):
        _ = ConnectedEvents(dates=[date_1, date_2], labels=['adsf'])
    with raises(ValueError):
        _ = ConnectedEvents(dates=[date_1], labels=['adsf', 'asdfas'])
    with raises(ValueError):
        _ = ConnectedEvents(dates=[date_1, date_2], labels=['adsf', 'asdfas'], individual_classes=[])
    with raises(ValueError):
        _ = ConnectedEvents(dates=[date_1, date_2], labels=['adsf', 'asdfas'], individual_classes=[['color_a']])
