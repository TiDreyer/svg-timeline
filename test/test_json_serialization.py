from datetime import datetime
from json import dumps, loads
from pathlib import Path

import svg_timeline.json_serialize as serialize
from svg_timeline.svg_primitives import SvgGroup
from svg_timeline.timeline import Event


def test_datetime_encoding():
    now = datetime.now()
    encoded = dumps(now, cls=serialize.TimeLineEncoder)
    decoded = loads(encoded, cls=serialize.TimeLineDecoder)
    assert now == decoded


def test_path_encoding():
    this_file = Path(__file__)
    encoded = dumps(this_file, cls=serialize.TimeLineEncoder)
    decoded = loads(encoded, cls=serialize.TimeLineDecoder)
    assert this_file == decoded


def test_event_encoding():
    current_event = Event(datetime.now(), 'test')
    encoded = dumps(current_event, cls=serialize.TimeLineEncoder)
    decoded = loads(encoded, cls=serialize.TimeLineDecoder)
    assert current_event.date == decoded.date
    assert current_event.text == decoded.text
    assert current_event.lane == decoded.lane
    assert current_event.classes == decoded.classes


def test_serialization_invariance():
    """ loading and saving a JSON serialization should only change the date """
    json_path = Path(__file__).parent.joinpath('files/emmy_noether.json')
    with open(json_path, 'r', encoding='utf-8') as json_file:
        direct_read = json_file.read()
    decoded = serialize.decode_serialisation(direct_read)
    encoded = serialize.encode_serialisation(decoded)
    # compare line by line
    direct_read_lines = direct_read.split('\n')
    encoded_lines = encoded.split('\n')
    assert len(direct_read_lines) == len(encoded_lines)
    for direct_line, encoded_line in zip(direct_read_lines, encoded_lines):
        if '"created":' in encoded_line:
            continue
        assert encoded_line == direct_line


def test_compilation_invariance():
    """ loading a JSON serialization should result in the same SVG """
    json_path = Path(__file__).parent.joinpath('files/emmy_noether.json')
    with open(json_path, 'r', encoding='utf-8') as json_file:
        direct_read = json_file.read()
    decoded = serialize.decode_serialisation(direct_read)
    encoded = serialize.encode_serialisation(decoded)
    decoded_2 = serialize.decode_serialisation(encoded)
    # compare SVGs line by line
    svg_1_lines = decoded.svg.full.split('\n')
    SvgGroup.id_counters = {}  # reset id-counters
    svg_2_lines = decoded_2.svg.full.split('\n')
    assert len(svg_1_lines) == len(svg_2_lines)
    for svg_1_line, svg_2_line in zip(svg_1_lines, svg_2_lines):
        assert svg_2_line == svg_1_line

