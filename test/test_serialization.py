from datetime import datetime
from json import dumps, loads
from pathlib import Path

from svg_timeline.JSON_encoding import TimeLineEncoder, TimeLineDecoder
from svg_timeline.timeline_elements import Event


def test_datetime_encoding():
    now = datetime.now()
    encoded = dumps(now, cls=TimeLineEncoder)
    decoded = loads(encoded, cls=TimeLineDecoder)
    assert now == decoded


def test_path_encoding():
    this_file = Path(__file__)
    encoded = dumps(this_file, cls=TimeLineEncoder)
    decoded = loads(encoded, cls=TimeLineDecoder)
    assert this_file == decoded


def test_event_encoding():
    current_event = Event(datetime.now(), 'test')
    encoded = dumps(current_event, cls=TimeLineEncoder)
    decoded = loads(encoded, cls=TimeLineDecoder)
    assert current_event.date == decoded.date
    assert current_event.text == decoded.text
    assert current_event.lane == decoded.lane
    assert current_event.classes == decoded.classes
