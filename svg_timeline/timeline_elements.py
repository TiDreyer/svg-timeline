from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from svg_timeline.style import Defaults, ClassNames
from svg_timeline.svg import SvgGroup
from svg_timeline.svg_primitives import Text, Circle, Line


class TimeLineElement:
    """ base class for describing an element that can be plotted within a timeline """
    def svg_group(self) -> SvgGroup:
        pass


@dataclass
class Event(TimeLineElement):
    date: datetime
    text: str
    classes: Optional[list[Optional[list[str]]]] = None
    lane: int = 1

    def svg_group(self) -> SvgGroup:
        classes = self.classes or []
        classes += [ClassNames.EVENT]
        event_base = self._time.date_to_coord(self.date)
        event_end = self.__to_lane_point(self.date, lane=self.lane)
        text_coord = self.__to_lane_point(self.date, lane=(self.lane+0.5 if self.lane >= 0 else self.lane-0.5))
        event = SvgGroup([
            Line(source=event_base, target=event_end, classes=classes),
            Circle(center=event_end, radius=Defaults.event_dot_radius, classes=classes),
            Text(text_coord, text, classes=classes),
        ], id_base='event')
        return event
