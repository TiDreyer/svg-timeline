""" high level timeline API classes """
from datetime import datetime
from pathlib import Path
from typing import Optional

from svg_timeline.geometry import Vector
from svg_timeline.svg import SVG, SvgGroup
from svg_timeline.svg_primitives import Rectangle
from svg_timeline.time_calculations import TimeSpacing
from svg_timeline.timeline_elements import TimeLineElement, Title, TimeArrow
from svg_timeline.timeline_elements import Event, ConnectedEvents, DatedImage, TimeSpan
from svg_timeline.timeline_geometry import TimeLineGeometry
from svg_timeline._warnings import deprecated



class TimelinePlot:
    """ representation of a timeline plot
    dates, timespans etc. can be added to this timeline via method calls
    """
    def __init__(self, coordinates: TimeLineGeometry,
                 time_spacing: TimeSpacing, minor_tics: Optional[TimeSpacing] = None,
                 ):
        self._layer: dict[int, list[TimeLineElement]] = dict()
        self._coordinates = coordinates
        self.add_element(TimeArrow(major_tics=time_spacing, minor_tics=minor_tics), layer=0)

    def add_element(self, element: TimeLineElement, layer: int = 1) -> None:
        self._layer.setdefault(layer, []).append(element)

    @property
    def layers(self) -> dict[int, list[TimeLineElement]]:
        return self._layer

    @property
    def geometry(self) -> TimeLineGeometry:
        return self._coordinates

    @deprecated(msg="use add_element() instead")
    def add_event(self, date: datetime, text: str,
                  lane: int = 1, classes: Optional[list[str]] = None):
        """ Add an event to the timeline that happened at a single point in time """
        event = Event(date=date, text=text, lane=lane, classes=classes)
        self.add_element(event)

    @deprecated(msg="use add_element() instead")
    def add_connected_events(self, dates: list[datetime], labels: list[str],
                             classes: Optional[list[Optional[list[str]]]] = None,
                             lane: int = 1,
                             ) -> None:
        """ Add a series of events connected via lines """
        connected_events = ConnectedEvents(dates=dates, labels=labels, classes=classes, lane=lane)
        self.add_element(connected_events)

    @deprecated(msg="use add_element() instead")
    def add_image(self, date: datetime, image_path: Path, height: float, width: float,
                  lane: int = 1, classes: Optional[list[str]] = None):
        """ Add an image to the timeline that is associated with a single point in time """
        image = DatedImage(date=date, image_path=image_path, height=height, width=width,
                           lane=lane, classes=classes)
        self.add_element(image)

    @deprecated(msg="use add_element() instead")
    def add_timespan(self, start_date: datetime, end_date: datetime, text: str,
                     lane: int = 1, width: Optional[int] = None, classes: Optional[list[str]] = None):
        """ Add an entry to the timeline that is associated with a certain time span """
        timespan = TimeSpan(start_date=start_date, end_date=end_date, text=text,
                            lane=lane, width=width, classes=classes)
        self.add_element(timespan)

    def add_title(self, title: str, classes: Optional[list[str]] = None):
        """ Add a title that should be printed above the timeline """
        title = Title(text=title, classes=classes)
        self.add_element(title, layer=0)

    def save(self, file_path: Path):
        """ Save an SVG of the timeline under the given file path """
        width, height = self._coordinates.width, self._coordinates.height
        svg = SVG(width, height)
        # first, set a white background
        svg.elements.append(Rectangle(Vector(0, 0), Vector(width, height), classes=['background']))
        for i_layer in sorted(self._layer.keys()):
            layer = SvgGroup(exact_id=f'layer_{i_layer:03}')
            for element in self._layer[i_layer]:
                layer.append(element.svg(self._coordinates, self._coordinates.style))
            svg.elements.append(layer)
        svg.save_as(file_path=file_path)
