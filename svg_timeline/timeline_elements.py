""" different elements that can be added to a timeline plot """
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Self

from svg_timeline.geometry import Vector
from svg_timeline.css import ClassNames
from svg_timeline.svg import SvgGroup
from svg_timeline.svg_primitives import Line, Text, Circle, Image, Rectangle
from svg_timeline.time_spacing import TimeSpacing
from svg_timeline.timeline_geometry import TimeLineGeometry

Classes = Optional[list[str]]


class TimeLineElement(ABC):
    """ interface definition for timeline elements """
    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        """ generate the SVG representation of this element """
        raise NotImplementedError


@dataclass
class Layer(TimeLineElement):
    """ a layer of the plot """
    elements: list[TimeLineElement]
    index: int

    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        layer = SvgGroup(exact_id=f'layer_{self.index:03}')
        for element in self.elements:
            layer.append(element.svg(geometry))
        return layer


@dataclass
class Background(TimeLineElement):
    """ the background of the plot """
    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        width, height = geometry.width, geometry.height
        bkg = Rectangle(Vector(0, 0), Vector(width, height), classes=['background'])
        return SvgGroup([bkg], exact_id='background')


@dataclass
class Title(TimeLineElement):
    """ the text of the title """
    text: str
    rel_x_position: float = 1/2
    rel_y_position: float = 1/17
    palette_color: int = 0
    classes: Classes = None

    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        classes = self.classes.copy() if self.classes else []
        classes += [ClassNames.TITLE, f'c{self.palette_color:02}']
        text_coord = Vector(x=int(geometry.width * self.rel_x_position),
                            y=int(geometry.height * self.rel_y_position))
        title = SvgGroup(
            [Text(text_coord, self.text, classes=classes)],
            exact_id='title'
        )
        return title


@dataclass
class TimeArrowTics(TimeLineElement):
    """ the tics on a timeline arrow"""
    spacing: TimeSpacing
    major: bool = True
    palette_color: int = 0
    classes: Classes = None

    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        classes = self.classes.copy() if self.classes else []
        classes += [ClassNames.TIME_ARROW, f'c{self.palette_color:02}']
        tic_delta = (-10 if self.major else -5) * geometry.lane_normal
        tic_group = SvgGroup(id_base='tics')
        for date, label in zip(self.spacing.dates, self.spacing.labels):
            tic_base = geometry.as_coord(date)
            tic_end = tic_base + tic_delta
            tic_classes = classes + [ClassNames.TIME_ARROW_MAJOR_TIC if self.major else
                                     ClassNames.TIME_ARROW_MINOR_TIC]
            tic_group.append(Line(source=tic_base, target=tic_end, classes=tic_classes + [ClassNames.COLORED]))
            if self.major:
                text_start = tic_base + 1.5 * tic_delta
                tic_group.append(Text(text_start, label, classes=tic_classes))
        return tic_group


@dataclass
class TimeArrow(TimeLineElement):
    """ the timeline arrow with major and minor tics """
    major_tics: TimeSpacing
    minor_tics: Optional[TimeSpacing] = None
    palette_color: int = 0
    classes: Classes = None

    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        classes = self.classes.copy() if self.classes else []
        classes += [ClassNames.TIME_ARROW, f'c{self.palette_color:02}']
        timeline = SvgGroup(id_base='timeline')
        source = geometry.as_coord(geometry.first, lane=0)
        target = geometry.as_coord(geometry.last, lane=0)
        line = Line(source, target, classes=classes + [ClassNames.TIME_ARROW_AXIS, ClassNames.COLORED])
        timeline.append(line)
        major_tics = TimeArrowTics(spacing=self.major_tics, major=True,
                                   palette_color=self.palette_color, classes=self.classes)
        timeline.append(major_tics.svg(geometry=geometry))
        if self.minor_tics is not None:
            minor_tics = TimeArrowTics(spacing=self.minor_tics, major=False,
                                       palette_color=self.palette_color, classes=self.classes)
            timeline.append(minor_tics.svg(geometry=geometry))
        return timeline


@dataclass
class Event(TimeLineElement):
    """ an event that happened at a single point in time """
    date: datetime
    text: str
    dot_radius: float = 3
    lane: float = 1
    palette_color: int = 0
    classes: Classes = None

    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        classes = self.classes.copy() if self.classes else []
        classes += [ClassNames.EVENT, f'c{self.palette_color:02}']
        event_base = geometry.as_coord(self.date)
        event_end = geometry.as_coord(self.date, lane=self.lane)
        text_coord = geometry.as_coord(self.date, lane=(self.lane + 0.5 if self.lane >= 0 else self.lane - 0.5))
        event = SvgGroup([
            Line(source=event_base, target=event_end, classes=classes + [ClassNames.COLORED]),
            Circle(center=event_end, radius=self.dot_radius, classes=classes + [ClassNames.COLORED]),
            Text(text_coord, self.text, classes=classes),
        ], id_base='event')
        return event


@dataclass
class ConnectedEvents(TimeLineElement):
    """ a series of events connected via lines """
    dates: list[datetime]
    labels: list[str]
    dot_radius: float = 3
    lane: float = 1
    palette_colors: list[int] | int = 0
    common_classes: Optional[Classes] = None
    individual_classes: Optional[list[Classes]] = None

    def __post_init__(self):
        # fill defaults for optional attributes:
        self.common_classes = self.common_classes or []
        if self.individual_classes is None:
            self.individual_classes = [[] for _ in range(len(self.dates))]
        if isinstance(self.palette_colors, int):
            self.palette_colors = [self.palette_colors for _ in range(len(self.dates))]
        # validate that the length of the three lists matches
        if not len(self.dates) == len(self.labels) == len(self.classes):
            raise ValueError("dates, labels and classes need to be of the same length")

    @property
    def classes(self) -> list[Classes]:
        return [self.common_classes + individual for individual in self.individual_classes]

    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        classes = self.classes.copy() if self.classes else []
        classes += [ClassNames.CONNECTED_EVENTS]
        n_dates = len(self.dates)
        groups = [[] for _ in range(n_dates)]
        for i in range(n_dates - 1):
            groups[i].append(Line(
                source=geometry.as_coord(self.dates[i], lane=self.lane),
                target=geometry.as_coord(self.dates[i + 1], lane=self.lane),
                classes=classes[i] + [f'c{self.palette_colors[i]:02}', ClassNames.COLORED],
            ))
        for i, label in enumerate(self.labels):
            if label is None:
                continue
            groups[i].append(Circle(
                center=geometry.as_coord(self.dates[i], lane=self.lane),
                radius=self.dot_radius,
                classes=classes[i] + [f'c{self.palette_colors[i]:02}', ClassNames.COLORED],
            ))
            groups[i].append(Text(
                coord=geometry.as_coord(self.dates[i], lane=(self.lane + 0.5 if self.lane >= 0 else self.lane - 0.5)),
                text=label,
                classes=classes[i] + [ClassNames.COLORED],
            ))
        connected_events = SvgGroup([SvgGroup(group) for group in groups], id_base='connected_events')
        return connected_events


@dataclass
class DatedImage(TimeLineElement):
    """ an image that is associated with a single point in time """
    date: datetime
    image_data: str
    height: float
    width: float
    lane: float = 1
    palette_color: int = 0
    classes: Classes = None

    @classmethod
    def from_path(cls, date: datetime, file_path: Path, width: float, height: float,
                  lane: float = 1, palette_color: int = 0, classes: Classes = None) -> Self:
        xlink_href = Image.xlink_href_from_file_path(file=file_path)
        return cls(date=date, image_data=xlink_href, height=height, width=width,
                   lane=lane, palette_color=palette_color, classes=classes)

    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        classes = self.classes.copy() if self.classes else []
        classes += [ClassNames.IMAGE, f'c{self.palette_color:02}']
        event_base = geometry.as_coord(self.date)
        event_end = geometry.as_coord(self.date, lane=self.lane)
        image_center_left = event_end + self.height * geometry.lane_normal
        image_top_left = image_center_left + self.width / 2 * geometry.lane_normal.orthogonal(ccw=True)
        image = SvgGroup([
            Line(source=event_base, target=event_end, classes=classes + [ClassNames.COLORED]),
            Image(top_left=image_top_left, xlink_href=self.image_data, height=self.height, width=self.width, classes=classes),
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
    palette_color: int = 0
    classes: Classes = None

    def svg(self, geometry: TimeLineGeometry) -> SvgGroup:
        classes = self.classes.copy() if self.classes else []
        classes += [ClassNames.TIMESPAN, f'c{self.palette_color:02}']
        # if no explicit width is set, fill 60% of a lane
        width = self.width or 0.6 * geometry.settings.lane_height
        half_width_vector = width / 2 * geometry.lane_normal
        start_corner = geometry.as_coord(self.start_date, lane=self.lane) + half_width_vector
        end_corner = geometry.as_coord(self.end_date, lane=self.lane) - half_width_vector
        middle_date = self.start_date + (self.end_date - self.start_date) / 2
        text_coord = geometry.as_coord(middle_date, lane=self.lane)
        timespan = SvgGroup([
            Rectangle(start_corner, end_corner, classes=classes + [ClassNames.COLORED]),
            Text(text_coord, self.text, classes=classes + [ClassNames.TOP_TEXT]),
        ], id_base='timespan')
        return timespan
