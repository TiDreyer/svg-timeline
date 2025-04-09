""" high level timeline API classes """
from datetime import datetime
from pathlib import Path
from typing import Optional

from svg_timeline.geometry import Vector
from svg_timeline.style import Defaults, DEFAULT_CSS, ClassNames
from svg_timeline.svg import SVG, SvgGroup
from svg_timeline.svg_primitives import Rectangle, Line, Text, Circle, Image
from svg_timeline.time_calculations import TimeSpacing
from svg_timeline.timeline_elements import TimeLineCoordinates, Event, ConnectedEvents, DatedImage, TimeSpan


class TimelinePlot:
    """ representation of a timeline plot
    dates, timespans etc. can be added to this timeline via method calls
    """
    def __init__(self, start_date: datetime, end_date: datetime,
                 time_spacing: TimeSpacing, minor_tics: Optional[TimeSpacing] = None,
                 size: tuple[int, int] = (800, 600)):
        self._width, self._height = size
        self._svg = SVG(self._width, self._height, style=DEFAULT_CSS)
        # set a white background
        self._svg.elements.append(Rectangle(Vector(0, 0), Vector(*size), classes=['background']))

        self._coordinates = TimeLineCoordinates(
            start_date=start_date, end_date=end_date,
            canvas_size=size,
            major_tics=time_spacing, minor_tics=minor_tics,
        )
        self._svg.elements.append(self._coordinates.time_arrow)

    def add_event(self, date: datetime, text: str,
                  lane: int = 1, classes: Optional[list[str]] = None):
        """ Add an event to the timeline that happened at a single point in time """
        event = Event(date=date, text=text, lane=lane, classes=classes)
        self._svg.elements.append(event.svg(self._coordinates))

    def add_connected_events(self, dates: list[datetime], labels: list[str],
                             classes: Optional[list[Optional[list[str]]]] = None,
                             lane: int = 1,
                             ) -> None:
        """ Add a series of events connected via lines """
        connected_events = ConnectedEvents(dates=dates, labels=labels, classes=classes, lane=lane)
        self._svg.elements.append(connected_events.svg(self._coordinates))

    def add_image(self, date: datetime, image_path: Path, height: float, width: float,
                  lane: int = 1, classes: Optional[list[str]] = None):
        """ Add an image to the timeline that is associated with a single point in time """
        image = DatedImage(date=date, image_path=image_path, height=height, width=width,
                           lane=lane, classes=classes)
        self._svg.elements.append(image.svg(self._coordinates))

    def add_timespan(self, start_date: datetime, end_date: datetime, text: str,
                     lane: int = 1, width: Optional[int] = None, classes: Optional[list[str]] = None):
        """ Add an entry to the timeline that is associated with a certain time span """
        timespan = TimeSpan(start_date=start_date, end_date=end_date, text=text,
                            lane=lane, width=width, classes=classes)
        self._svg.elements.append(timespan.svg(self._coordinates))

    def add_title(self, title: str, classes: Optional[list[str]] = None):
        """ Add a title that should be printed above the timeline """
        classes = classes or []
        classes += [ClassNames.TITLE]
        text_coord = Vector(x=int(self._width * Defaults.title_x_position),
                            y=int(self._height * Defaults.title_y_position))
        self._svg.elements += [Text(text_coord, title, classes=classes)]

    def save(self, file_path: Path):
        """ Save an SVG of the timeline under the given file path """
        self._svg.save_as(file_path=file_path)
