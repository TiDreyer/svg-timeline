""" high level timeline API classes """
from pathlib import Path
from typing import Optional

from svg_timeline.svg import SVG, CascadeStyleSheet
from svg_timeline.timeline_elements import TimeLineElement, Background, Layer
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

    @property
    def svg(self) -> SVG:
        """ Return the SVG representation of this timeline """
        width, height = self._geometry.width, self._geometry.height
        svg = SVG(width, height, css=self.css)
        # first, set a white background
        self.add_element(Background(), layer=0)
        for i_layer, elements in sorted(self._layers.items()):
            layer = Layer(elements=elements, index=i_layer)
            svg.elements.append(layer.svg(self._geometry))
        return svg

    def save(self, file_path: Path):
        """ Save an SVG of the timeline under the given file path """
        self.svg.save_as(file_path=file_path)
