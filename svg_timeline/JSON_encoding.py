from dataclasses import is_dataclass
from datetime import datetime
from json import dumps, JSONEncoder
from pathlib import Path

from svg_timeline.time_calculations import TimeSpacing
from svg_timeline.timeline import TimelinePlot
from svg_timeline.timeline_geometry import TimeLineGeometry


def save_json(timeline: TimelinePlot, file_path: Path):
    """ Save a JSON representing the timeline under the given file path """
    with open(file_path, 'w') as json_file:
        json_file.write(dumps(timeline, cls=TimeLineEncoder, indent='  '))


class TimeLineEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TimelinePlot):
            return {
                "type": obj.__class__.__name__,
                "layers": obj.layers,
                "geometry": obj.geometry,
            }
        if isinstance(obj, TimeLineGeometry):
            return {
                "type": obj.__class__.__name__,
                "first": obj.first,
                "last": obj.last,
                "style": obj.style,
            }
        if isinstance(obj, TimeSpacing):
            return {
                "type": obj.__class__.__name__,
                "start_date": obj.start_date,
                "end_date": obj.end_date,
            }
        if is_dataclass(obj):
            return {
                "type": obj.__class__.__name__,
                **{k: v for k, v in obj.__dict__.items()},
            }
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Path):
            return {
                "type": obj.__class__.__name__,
                "path": str(obj),
            }
        # Let the base class default method raise the TypeError
        return super().default(obj)