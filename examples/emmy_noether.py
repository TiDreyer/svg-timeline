""" Example script to create a timeline of Emmy Noether's life """
from pathlib import Path

from svg_timeline.css import Colors
from svg_timeline.time_calculations import TimeSpacingPerDecade, TimeSpacingPerYear, dt
from svg_timeline.timeline import TimelinePlot
from svg_timeline.timeline_elements import Event, TimeSpan, ConnectedEvents, DatedImage
from svg_timeline.timeline_geometry import TimeLineGeometry, GeometrySettings


def main():
    """ main script function for the creation of the plot """
    # defining the range of the timeline
    birth = dt('1882-03-23')
    death = dt('1935-04-14')

    style = GeometrySettings()
    style.canvas.width = 1000
    style.canvas.height = 300
    # setting at what vertical position the arrow is drawn
    style.lane.lane_zero_y = 0.85
    # white text is easier to read on colored timespans
    style.timespan.text_color = 'white'

    # initializing the timeline plot object
    coords = TimeLineGeometry(
        start_date=dt('1879-12-01'),
        end_date=dt('1935-12-31'),
        style=style,
    )
    timeline = TimelinePlot(
        coordinates=coords,
        time_spacing=TimeSpacingPerDecade(coords.first, coords.last),
        minor_tics=TimeSpacingPerYear(coords.first, coords.last),
    )

    # adding a title to the plot
    timeline.add_title("Emmy Noether")

    # adding the image of Emmy Noether
    _image_path = Path(__file__).parent.joinpath('473px-Noether.jpeg')
    _image_scale = 0.27
    timeline.add_element(
        DatedImage(dt('1900'), _image_path, width=_image_scale*473, height=_image_scale*720, lane=1)
    )

    plot_elements = [
        # some important dates in her life
        Event(birth, 'Birth', lane=2, classes=[Colors.COLOR_A.name.lower()]),
        Event(dt('1907'), 'PhD Thesis', lane=3, classes=[Colors.COLOR_B.name.lower()]),
        Event(dt('1918'), 'Noether\'s Theorem', lane=5, classes=[Colors.COLOR_E.name.lower()]),
        Event(dt('1919'), 'Habilitation', lane=3, classes=[Colors.COLOR_C.name.lower()]),
        Event(dt('1932'), 'Ackermann-Teuber Memorial Award', lane=5, classes=[Colors.COLOR_E.name.lower()]),

        # scholars distinguish three "epochs" in her work
        TimeSpan(dt('1908'), dt('1920'), '"1st epoch"', lane=1, classes=[Colors.COLOR_B.name.lower(), 'white_text']),
        TimeSpan(dt('1920'), dt('1927'), '"2nd epoch"', lane=1, classes=[Colors.COLOR_C.name.lower(), 'white_text']),
        TimeSpan(dt('1927'), death, '"3rd epoch"', lane=1, classes=[Colors.COLOR_D.name.lower(), 'white_text']),

        # the universities she was associated with
        ConnectedEvents(
            dates=[dt('1908'), dt('1915-04'), dt('1933'), death],
            labels=["Erlangen", "Göttingen", "USA", None],
            classes=[[Colors.COLOR_B.name.lower()], [Colors.COLOR_C.name.lower()], [Colors.COLOR_D.name.lower()], []],
            lane=2,
        ),
    ]
    for event in plot_elements:
        timeline.add_element(event)

    # adding this date on layer 2 so it is plotted on top of the other elements
    timeline.add_element(Event(death, 'Death', lane=4, classes=[Colors.COLOR_A.name.lower()]), layer=2)

    # saving the SVG
    svg_path = Path(__file__).parent.joinpath('emmy_noether.svg')
    timeline.save(svg_path)


if __name__ == '__main__':
    main()
