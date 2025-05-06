""" functionality for (de-)serializing a timeline as JSON """
from dataclasses import is_dataclass
from datetime import datetime
from enum import Enum
from json import dumps, loads, JSONEncoder, JSONDecoder
from pathlib import Path

from svg_timeline import __version__
from svg_timeline.time_calculations import TimeSpacing
from svg_timeline.timeline import TimelinePlot
from svg_timeline.timeline_geometry import TimeLineGeometry
import svg_timeline.timeline_elements as ele
import svg_timeline.timeline_geometry as geo
import svg_timeline.time_calculations as tls


def save_json(timeline: TimelinePlot, file_path: Path):
    """ Save a JSON representing the timeline under the given file path """
    with_meta = {
        'meta': {
            'created': datetime.now(),
            'version': __version__,
        },
        'data': timeline,
    }
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(dumps(with_meta, cls=TimeLineEncoder, indent='  '))


def load_json(file_path: Path) -> TimelinePlot:
    """ Load a JSON representing the timeline from the given file path """
    with open(file_path, 'r', encoding='utf-8') as json_file:
        with_meta = loads(json_file.read(), cls=TimeLineDecoder)
    return with_meta['data']


class KnownClasses(Enum):
    """ registry of classes that can be (de-)serialized """
    # pylint: disable=invalid-name
    # (the enum names need to be the class names to allow for easier de-serialization)
    TimelinePlot = TimelinePlot
    TimeLineGeometry = TimeLineGeometry
    GeometrySettings = geo.GeometrySettings
    Title = ele.Title
    TimeArrow = ele.TimeArrow
    Event = ele.Event
    ConnectedEvents = ele.ConnectedEvents
    DatedImage = ele.DatedImage
    TimeSpan = ele.TimeSpan
    TimeSpacingPerMillennia = tls.TimeSpacingPerMillennia
    TimeSpacingPerCentury = tls.TimeSpacingPerCentury
    TimeSpacingPerDecade = tls.TimeSpacingPerDecade
    TimeSpacingPerYear = tls.TimeSpacingPerYear
    TimeSpacingPerMonth = tls.TimeSpacingPerMonth
    TimeSpacingPerWeek = tls.TimeSpacingPerWeek
    TimeSpacingPerDay = tls.TimeSpacingPerDay
    TimeSpacingPerHour = tls.TimeSpacingPerHour
    TimeSpacingPerMinute = tls.TimeSpacingPerMinute
    TimeSpacingPerSecond = tls.TimeSpacingPerSecond
    Path = Path


class TimeLineEncoder(JSONEncoder):
    """ JSON encoder to serialize timeline specific classes
    that the default JSONEncoder can't handle """
    def default(self, o):
        if isinstance(o, TimelinePlot):
            return {
                "type": KnownClasses(o.__class__).name,
                "layers": o.layers,
                "geometry": o.geometry,
            }
        if isinstance(o, TimeLineGeometry):
            return {
                "type": KnownClasses(o.__class__).name,
                "start_date": o.first,
                "end_date": o.last,
                "style": o.style,
            }
        if isinstance(o, TimeSpacing):
            return {
                "type": KnownClasses(o.__class__).name,
                "start_date": o.start_date,
                "end_date": o.end_date,
            }
        if is_dataclass(o):
            return {
                "type": KnownClasses(o.__class__).name,
                **o.__dict__,
            }
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Path):
            return {
                "type": KnownClasses.Path.name,
                "path": str(o),
            }
        # Let the base class default method raise the TypeError
        return super().default(o)


class TimeLineDecoder(JSONDecoder):
    """ JSON decoder to de-serialize timeline specific classes
    that the default JSONDecoder can't handle """
    def decode(self, s, **kwargs) -> TimelinePlot:
        pure_json = super().decode(s, **kwargs)
        return recursive_decode(pure_json)


def recursive_decode(json_object: any) -> any:
    """ recursively transform the object returned by the
    default JSONDecoder into our custom classes """
    # depth-first: decode sub-objects before using them to decode this object
    if isinstance(json_object, dict):
        for key, value in json_object.items():
            json_object[key] = recursive_decode(value)
    if isinstance(json_object, list):
        for i, value in enumerate(json_object):
            json_object[i] = recursive_decode(value)
    # special cases, that can be decoded:
    if isinstance(json_object, str):
        try:
            return datetime.fromisoformat(json_object)
        except ValueError:
            pass
    if isinstance(json_object, dict) and json_object.get('type', '') == KnownClasses.Path.name:
        return Path(json_object['path'])
    if isinstance(json_object, dict) and 'type' in json_object:
        cls = KnownClasses[json_object.pop('type')].value
        return cls(**json_object)
    # if it is no special case, return the current representation:
    return json_object
