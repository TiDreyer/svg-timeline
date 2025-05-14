""" high level timeline API classes """
from pathlib import Path
from typing import Optional

from svg_timeline.css import CascadeStyleSheet
from svg_timeline.svg import SVG, SvgGroup
from svg_timeline.time_spacing import TimeSpacing
from svg_timeline.timeline_elements import TimeLineElement, Title, TimeArrow, Background
from svg_timeline.timeline_geometry import TimeLineGeometry



class TimelinePlot:
    """ representation of a timeline plot
    dates, timespans etc. can be added to this timeline via method calls
    """
    def __init__(self, geometry: TimeLineGeometry,
                 layers: Optional[dict[int|str, list[TimeLineElement]]] = None,
                 css: Optional[CascadeStyleSheet] = None,
                 ):
        self._layers: dict[int, list[TimeLineElement]] = dict()
        if layers is not None:
            for i_layer, elements in layers.items():
                layer = self._layers.setdefault(int(i_layer), [])
                layer += elements
        self._css = css or CascadeStyleSheet()
        self._geometry = geometry

    def add_element(self, element: TimeLineElement, layer: int = 1) -> None:
        """ Add an element to one layer of this timeline plot """
        self._layers.setdefault(layer, []).append(element)

    @property
    def layers(self) -> dict[int, list[TimeLineElement]]:
        """ all elements currently registered in this timeline, sorted by layer """
        return self._layers

    @property
    def geometry(self) -> TimeLineGeometry:
        """ the geometry settings of this plot """
        return self._geometry

    @property
    def css(self) -> CascadeStyleSheet:
        """ the style sheet of this plot """
        return self._css

    def add_title(self, title: str, classes: Optional[list[str]] = None):
        """ Add a title that should be printed above the timeline """
        title = Title(text=title, classes=classes)
        self.add_element(title, layer=0)

    def add_timearrow(self, major_tics: TimeSpacing, minor_tics: Optional[TimeSpacing] = None):
        """ Add a timearrow to the timeline """
        self.add_element(TimeArrow(major_tics=major_tics, minor_tics=minor_tics), layer=0)

    @property
    def svg(self) -> SVG:
        """ Return the SVG representation of this timeline """
        width, height = self._geometry.width, self._geometry.height
        svg = SVG(width, height, css=self.css)
        # first, set a white background
        self.add_element(Background(), layer=-1)
        for i_layer in sorted(self._layers.keys()):
            layer = SvgGroup(exact_id=f'layer_{i_layer:03}')
            for element in self._layers[i_layer]:
                layer.append(element.svg(self._geometry))
            svg.elements.append(layer)
        return svg

    def save(self, file_path: Path):
        """ Save an SVG of the timeline under the given file path """
        self.svg.save_as(file_path=file_path)
