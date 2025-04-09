""" high level timeline API classes """
from datetime import datetime
from pathlib import Path
from typing import Optional

from svg_timeline.geometry import Vector
from svg_timeline.style import Defaults, DEFAULT_CSS, ClassNames
from svg_timeline.svg import SVG, SvgGroup
from svg_timeline.svg_primitives import Rectangle, Line, Text, Circle, Image
from svg_timeline.time_calculations import TimeGradient, TimeSpacing
from svg_timeline.timeline_elements import TimeLineCoordinates


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

        y = Defaults.arrow_y_position * self._height
        x1 = Defaults.arrow_x_padding * self._width
        x2 = (1 - Defaults.arrow_x_padding) * self._width
        self._time = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                  start_date=start_date, end_date=end_date)
        self._coordinates = TimeLineCoordinates(gradient=self._time, major_tics=time_spacing, minor_tics=minor_tics)
        self._svg.elements.append(self._coordinates.time_arrow)

    def add_event(self, date: datetime, text: str,
                  lane: int = 1, classes: Optional[list[str]] = None):
        """ Add an event to the timeline that happened at a single point in time """
        classes = classes or []
        classes += [ClassNames.EVENT]
        event_base = self._time.date_to_coord(date)
        event_end = self._coordinates.to_lane_point(date, lane=lane)
        text_coord = self._coordinates.to_lane_point(date, lane=(lane+0.5 if lane >= 0 else lane-0.5))
        event = SvgGroup([
            Line(source=event_base, target=event_end, classes=classes),
            Circle(center=event_end, radius=Defaults.event_dot_radius, classes=classes),
            Text(text_coord, text, classes=classes),
        ], id_base='event')
        self._svg.elements.append(event)

    def add_connected_events(self, dates: list[datetime], labels: list[str],
                             classes: Optional[list[Optional[list[str]]]] = None,
                             lane: int = 1,
                             ) -> None:
        """ Add a series of events connected via lines """
        if classes is None:
            classes = [[] for _ in range(len(dates))]
        if not len(dates) == len(labels) == len(classes):
            raise RuntimeError("dates, labels and classes need to be of the same length")
        lines = SvgGroup([Line(
            source=self._coordinates.to_lane_point(dates[i], lane=lane),
            target=self._coordinates.to_lane_point(dates[i+1], lane=lane),
            classes=classes[i],
        ) for i in range(len(dates)-1)])
        circles = SvgGroup([Circle(
            center=self._coordinates.to_lane_point(dates[i], lane=lane),
            radius=Defaults.event_dot_radius,
            classes=classes[i],
        ) for i, label in enumerate(labels) if label is not None])
        texts = SvgGroup([Text(
            coord=self._coordinates.to_lane_point(dates[i], lane=(lane+0.5 if lane >= 0 else lane-0.5)),
            text=label,
            classes=classes[i],
        ) for i, label in enumerate(labels) if label is not None])
        connected_events = SvgGroup([lines, circles, texts], id_base='connected_events')
        self._svg.elements.append(connected_events)

    def add_image(self, date: datetime, image_path: Path, height: float, width: float,
                  lane: int = 1, classes: Optional[list[str]] = None):
        """ Add an image to the timeline that is associated with a single point in time """
        classes = classes or []
        classes += [ClassNames.IMAGE]
        event_base = self._time.date_to_coord(date)
        event_end = self._coordinates.to_lane_point(date, lane=lane)
        image_center_left = event_end + height * self._coordinates.lane_normal
        image_top_left = image_center_left + width/2 * self._coordinates.lane_normal.orthogonal(ccw=True)
        image = SvgGroup([
            Line(source=event_base, target=event_end, classes=classes),
            Image(top_left=image_top_left, file=image_path, height=height, width=width, classes=classes),
        ], id_base='image')
        self._svg.elements.append(image)

    def add_timespan(self, start_date: datetime, end_date: datetime, text: str,
                     lane: int = 1, width: Optional[int] = None, classes: Optional[list[str]] = None):
        """ Add an entry to the timeline that is associated with a certain time span """
        classes = classes or []
        classes += [ClassNames.TIMESPAN]
        width = width or Defaults.timespan_width
        half_width_vector = width/2 * self._coordinates.lane_normal
        start_corner = self._coordinates.to_lane_point(start_date, lane=lane) + half_width_vector
        end_corner = self._coordinates.to_lane_point(end_date, lane=lane) - half_width_vector
        middle_date = start_date + (end_date - start_date) / 2
        text_coord = self._coordinates.to_lane_point(middle_date, lane=lane)
        timespan = SvgGroup([
            Rectangle(start_corner, end_corner, classes=classes),
            Text(text_coord, text, classes=classes),
        ], id_base='timespan')
        if Defaults.timespan_use_start_stilt:
            on_timeline = self._coordinates.to_lane_point(start_date, lane=0)
            bottom_timespan = self._coordinates.to_lane_point(start_date, lane=lane) - half_width_vector
            timespan.append(Line(source=on_timeline, target=bottom_timespan, classes=classes))
        if Defaults.timespan_use_end_stilt:
            on_timeline = self._coordinates.to_lane_point(end_date, lane=0)
            bottom_timespan = self._coordinates.to_lane_point(end_date, lane=lane) - half_width_vector
            timespan.append(Line(source=on_timeline, target=bottom_timespan, classes=classes))
        self._svg.elements.append(timespan)

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
