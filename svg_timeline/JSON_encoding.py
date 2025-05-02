from dataclasses import is_dataclass
from datetime import datetime
from enum import Enum
from json import dumps, JSONEncoder
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
                "first": obj.first,
                "last": obj.last,
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