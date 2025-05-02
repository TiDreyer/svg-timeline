from dataclasses import is_dataclass
from datetime import datetime
from enum import Enum
from json import dumps, loads, JSONEncoder, JSONDecoder
from pathlib import Path

from svg_timeline.time_calculations import TimeSpacing
from svg_timeline.timeline import TimelinePlot
from svg_timeline.timeline_geometry import TimeLineGeometry
import svg_timeline.timeline_elements as ele
import svg_timeline.timeline_geometry as geo
import svg_timeline.time_calculations as tls


def save_json(timeline: TimelinePlot, file_path: Path):
    """ Save a JSON representing the timeline under the given file path """
    with open(file_path, 'w') as json_file:
        json_file.write(dumps(timeline, cls=TimeLineEncoder, indent='  '))


def load_json(file_path: Path) -> TimelinePlot:
    """ Load a JSON representing the timeline from the given file path """
    with open(file_path, 'r') as json_file:
        return loads(json_file.read(), cls=TimeLineDecoder)


class KnownClasses(Enum):
    TimelinePlot = TimelinePlot
    TimeLineGeometry = TimeLineGeometry
    GeometrySettings = geo.GeometrySettings
    CanvasGeometry = geo.CanvasGeometry
    TitleGeometry = geo.TitleGeometry
    LaneGeometry = geo.LaneGeometry
    EventGeometry = geo.EventGeometry
    TimespanGeometry = geo.TimespanGeometry
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
    def default(self, obj):
        if isinstance(obj, TimelinePlot):
            return {
                "type": KnownClasses(obj.__class__).name,
                "layers": obj.layers,
                "geometry": obj.geometry,
            }
        if isinstance(obj, TimeLineGeometry):
            return {
                "type": KnownClasses(obj.__class__).name,
                "start_date": obj.first,
                "end_date": obj.last,
                "style": obj.style,
            }
        if isinstance(obj, TimeSpacing):
            return {
                "type": KnownClasses(obj.__class__).name,
                "start_date": obj.start_date,
                "end_date": obj.end_date,
            }
        if is_dataclass(obj):
            return {
                "type": KnownClasses(obj.__class__).name,
                **{k: v for k, v in obj.__dict__.items()},
            }
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Path):
            return {
                "type": KnownClasses.Path.name,
                "path": str(obj),
            }
        # Let the base class default method raise the TypeError
        return super().default(obj)


class TimeLineDecoder(JSONDecoder):
    def decode(self, s, **kwargs) -> TimelinePlot:
        pure_json = super().decode(s, **kwargs)
        return recursive_decode(pure_json)


def recursive_decode(json_object: any) -> any:
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