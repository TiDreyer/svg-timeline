from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from svg_timeline.geometry import Vector
from svg_timeline.style import TimelineStyle, ClassNames
from svg_timeline.svg import SvgGroup
from svg_timeline.svg_primitives import Line, Text, Circle, Image, Rectangle
from svg_timeline.time_calculations import TimeGradient, TimeSpacing


Classes = Optional[list[str]]


class TimeLineCoordinates:
    """ class for the transfer of dates and lanes to canvas coordinates """
    def __init__(self,
                 start_date: datetime,
                 end_date: datetime,
                 style: Optional[TimelineStyle] = None,
                 ):
        """
        :param start_date: the lower boundary of the timeline
        :param end_date: the upper boundary of the timeline
        """
        self._style = style or TimelineStyle()
        self._first = start_date
        self._last = end_date
        y = self._style.arrow.y_position * self._style.canvas.height
        x1 = self._style.arrow.x_padding * self._style.canvas.width
        x2 = (1 - self._style.arrow.x_padding) * self._style.canvas.width
        self._gradient = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                      start_date=start_date, end_date=end_date)

    @property
    def style(self) -> TimelineStyle:
        """ styling information for the timeline """
        return self._style

    @property
    def first(self) -> datetime:
        """ first date of the timeline """
        return self._first

    @property
    def last(self) -> datetime:
        """ last date of the timeline """
        return self._last

    @property
    def width(self) -> int:
        """ full width of the canvas """
        return self._style.canvas.width

    @property
    def height(self) -> int:
        """ full height of the canvas """
        return self._style.canvas.height

    @property
    def lane_normal(self) -> Vector:
        """ Normal vector orthogonal to the timeline direction
        This vector is used to calculate the positions of the different lanes.
        """
        return (self._gradient.target - self._gradient.source).orthogonal(ccw=True)

    def as_coord(self, date: datetime, lane: float = 0) -> Vector:
        """ return the coordinates responding to this date on a given lane
        (default: on the time arrow)
        """
        date_coord = self._gradient.date_to_coord(date)
        lane_point = date_coord + lane * self._style.lane.width * self.lane_normal
        return lane_point


class TimeLineElement(ABC):
    """ interface definition for timeline elements """
    def svg(self, coord: TimeLineCoordinates, style: TimelineStyle) -> SvgGroup:
        raise NotImplementedError


@dataclass
class Title(TimeLineElement):
    """ the text of the title """
    text: str
    classes: Classes = None

    def svg(self, coord: TimeLineCoordinates, style: TimelineStyle) -> SvgGroup:
        classes = self.classes or []
        classes += [ClassNames.TITLE]
        text_coord = Vector(x=int(coord.width * style.title.x_position),
                            y=int(coord.height * style.title.y_position))
        title = SvgGroup(
            [Text(text_coord, self.text, classes=classes)],
            exact_id='title'
        )
        return title


@dataclass
class TimeArrow(TimeLineElement):
    """ the timeline arrow with major and minor tics """
    major_tics: TimeSpacing
    minor_tics: Optional[TimeSpacing] = None
    classes: Classes = None

    def svg(self, coord: TimeLineCoordinates, style: TimelineStyle) -> SvgGroup:
        timeline = SvgGroup(id_base='timeline')
        source = coord.as_coord(coord.first, lane=0)
        target = coord.as_coord(coord.last, lane=0)
        line = Line(source, target, classes=[ClassNames.TIMEAXIS])
        timeline.append(line)
        tic_delta = -10 * coord.lane_normal
        major_tics = SvgGroup(id_base='tics')
        for date, label in zip(self.major_tics.dates, self.major_tics.labels):
            tic_base = coord.as_coord(date)
            tic_end = tic_base + tic_delta
            text_start = tic_base + 1.5 * tic_delta
            major_tics.append(Line(source=tic_base, target=tic_end, classes=[ClassNames.MAJOR_TICK]))
            major_tics.append(Text(text_start, label, classes=[ClassNames.MAJOR_TICK]))
        timeline.append(major_tics)
        if self.minor_tics is None:
            return timeline
        minor_tics = SvgGroup(id_base='tics')
        for date in self.minor_tics.dates:
            tic_base = coord.as_coord(date)
            tic_end = tic_base + 0.5 * tic_delta
            minor_tics.append(Line(source=tic_base, target=tic_end, classes=[ClassNames.MINOR_TICK]))
        timeline.append(minor_tics)
        return timeline


@dataclass
class Event(TimeLineElement):
    """ an event that happened at a single point in time """
    date: datetime
    text: str
    lane: float = 1
    classes: Classes = None

    def svg(self, coord: TimeLineCoordinates, style: TimelineStyle) -> SvgGroup:
        classes = self.classes or []
        classes += [ClassNames.EVENT]
        event_base = coord.as_coord(self.date)
        event_end = coord.as_coord(self.date, lane=self.lane)
        text_coord = coord.as_coord(self.date, lane=(self.lane + 0.5 if self.lane >= 0 else self.lane - 0.5))
        event = SvgGroup([
            Line(source=event_base, target=event_end, classes=classes),
            Circle(center=event_end, radius=style.event.dot_radius, classes=classes),
            Text(text_coord, self.text, classes=classes),
        ], id_base='event')
        return event


@dataclass
class ConnectedEvents(TimeLineElement):
    """ a series of events connected via lines """
    dates: list[datetime]
    labels: list[str]
    lane: float = 1
    classes: Optional[list[Classes]] = None

    def __post_init__(self):
        # validate that the length of the three lists matches
        self.classes = [[] for _ in range(len(self.dates))] if self.classes is None else self.classes
        if not len(self.dates) == len(self.labels) == len(self.classes):
            raise ValueError("dates, labels and classes need to be of the same length")

    def svg(self, coord: TimeLineCoordinates, style: TimelineStyle) -> SvgGroup:
        lines = SvgGroup([Line(
            source=coord.as_coord(self.dates[i], lane=self.lane),
            target=coord.as_coord(self.dates[i + 1], lane=self.lane),
            classes=self.classes[i],
        ) for i in range(len(self.dates)-1)])
        circles = SvgGroup([Circle(
            center=coord.as_coord(self.dates[i], lane=self.lane),
            radius=style.event.dot_radius,
            classes=self.classes[i],
        ) for i, label in enumerate(self.labels) if label is not None])
        texts = SvgGroup([Text(
            coord=coord.as_coord(self.dates[i], lane=(self.lane + 0.5 if self.lane >= 0 else self.lane - 0.5)),
            text=label,
            classes=self.classes[i],
        ) for i, label in enumerate(self.labels) if label is not None])
        connected_events = SvgGroup([lines, circles, texts], id_base='connected_events')
        return connected_events


@dataclass
class DatedImage(TimeLineElement):
    """ an image that is associated with a single point in time """
    date: datetime
    image_path: Path
    height: float
    width: float
    lane: float = 1
    classes: Classes = None

    def svg(self, coord: TimeLineCoordinates, style: TimelineStyle) -> SvgGroup:
        classes = self.classes or []
        classes += [ClassNames.IMAGE]
        event_base = coord.as_coord(self.date)
        event_end = coord.as_coord(self.date, lane=self.lane)
        image_center_left = event_end + self.height * coord.lane_normal
        image_top_left = image_center_left + self.width/2 * coord.lane_normal.orthogonal(ccw=True)
        image = SvgGroup([
            Line(source=event_base, target=event_end, classes=classes),
            Image(top_left=image_top_left, file=self.image_path, height=self.height, width=self.width, classes=classes),
        ], id_base='image')
        return image


@dataclass
class TimeSpan(TimeLineElement):
    """ an entry that is associated with a certain time span """
    start_date: datetime
    end_date: datetime
    text: str
    lane: float = 1
    width: Optional[int] = None
    classes: Classes = None

    def svg(self, coord: TimeLineCoordinates, style: TimelineStyle) -> SvgGroup:
        classes = self.classes or []
        classes += [ClassNames.TIMESPAN]
        width = self.width or style.timespan.width
        half_width_vector = width/2 * coord.lane_normal
        start_corner = coord.as_coord(self.start_date, lane=self.lane) + half_width_vector
        end_corner = coord.as_coord(self.end_date, lane=self.lane) - half_width_vector
        middle_date = self.start_date + (self.end_date - self.start_date) / 2
        text_coord = coord.as_coord(middle_date, lane=self.lane)
        timespan = SvgGroup([
            Rectangle(start_corner, end_corner, classes=classes),
            Text(text_coord, self.text, classes=classes),
        ], id_base='timespan')
        if style.timespan.use_start_stilt:
            on_timeline = coord.as_coord(self.start_date, lane=0)
            bottom_timespan = coord.as_coord(self.start_date, lane=self.lane) - half_width_vector
            timespan.append(Line(source=on_timeline, target=bottom_timespan, classes=classes))
        if style.timespan.use_end_stilt:
            on_timeline = coord.as_coord(self.end_date, lane=0)
            bottom_timespan = coord.as_coord(self.end_date, lane=self.lane) - half_width_vector
            timespan.append(Line(source=on_timeline, target=bottom_timespan, classes=classes))
        return timespan
