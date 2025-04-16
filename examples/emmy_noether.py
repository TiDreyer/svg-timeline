""" Example script to create a timeline of Emmy Noether's life """
from pathlib import Path

from svg_timeline.style import Defaults, Colors
from svg_timeline.time_calculations import TimeSpacingPerDecade, TimeSpacingPerYear, dt
from svg_timeline.timeline import TimelinePlot
from svg_timeline.timeline_elements import TimeLineCoordinates, Event, TimeSpan, ConnectedEvents, DatedImage

# defining important dates for easier usage later on
_BIRTH = dt('1882-03-23')
_PHOTO = dt('1900')
_THESIS = dt('1907')
_TEACH_ERL = dt('1908')
_EPOCH_1 = dt('1908')
_MOVE_GOE = dt('1915-04')
_THEOREM = dt('1918')
_HABIL = dt('1919')
_EPOCH_2 = dt('1920')
_EPOCH_3 = dt('1927')
_AWARD = dt('1932')
_MOVE_USA = dt('1933')
_DEATH = dt('1935-04-14')


def main():
    """ main script function for the creation of the plot """
    # setting what percentage of the page width the arrow occupies
    Defaults.arrow_y_position = 0.85

    # initializing the timeline plot object
    coords = TimeLineCoordinates(
        start_date=dt('1879-12-01'),
        end_date=dt('1935-12-31'),
        canvas_size=(1000, 300),
    )
    timeline = TimelinePlot(
        coordinates=coords,
        time_spacing=TimeSpacingPerDecade(coords.first, coords.last),
        minor_tics=TimeSpacingPerYear(coords.first, coords.last),
    )

    # adding a title to the plot
    timeline.add_title("Emmy Noether")

    # white text is easier to read on colored timespans
    Defaults.timespan_text_color = 'white'

    # adding the image of Emmy Noether
    _image_path = Path(__file__).parent.joinpath('473px-Noether.jpeg')
    _image_scale = 0.27
    timeline.add_element(
        DatedImage(_PHOTO, _image_path, width=_image_scale*473, height=_image_scale*720, lane=1)
    )

    plot_elements = [
        # some important dates in her life
        Event(_BIRTH, 'Birth', lane=2, classes=[Colors.COLOR_A.name.lower()]),
        Event(_THESIS, 'PhD Thesis', lane=3, classes=[Colors.COLOR_B.name.lower()]),
        Event(_THEOREM, 'Noether\'s Theorem', lane=5, classes=[Colors.COLOR_E.name.lower()]),
        Event(_HABIL, 'Habilitation', lane=3, classes=[Colors.COLOR_C.name.lower()]),
        Event(_AWARD, 'Ackermann-Teuber Memorial Award', lane=5, classes=[Colors.COLOR_E.name.lower()]),

        # scholars distinguish three "epochs" in her work
        TimeSpan(_EPOCH_1, _EPOCH_2, '"1st epoch"', lane=1, classes=[Colors.COLOR_B.name.lower(), 'white_text']),
        TimeSpan(_EPOCH_2, _EPOCH_3, '"2nd epoch"', lane=1, classes=[Colors.COLOR_C.name.lower(), 'white_text']),
        TimeSpan(_EPOCH_3, _DEATH, '"3rd epoch"', lane=1, classes=[Colors.COLOR_D.name.lower(), 'white_text']),

        # the universities she was associated with
        ConnectedEvents(
            dates=[_TEACH_ERL, _MOVE_GOE, _MOVE_USA, _DEATH],
            labels=["Erlangen", "Göttingen", "USA", None],
            classes=[[Colors.COLOR_B.name.lower()], [Colors.COLOR_C.name.lower()], [Colors.COLOR_D.name.lower()], []],
            lane=2,
        ),
    ]
    for event in plot_elements:
        timeline.add_element(event)

    # adding this date on layer 2 so it is plotted on top of the other elements
    timeline.add_element(Event(_DEATH, 'Death', lane=4, classes=[Colors.COLOR_A.name.lower()]), layer=2)

    # saving the SVG
    svg_path = Path(__file__).parent.joinpath('emmy_noether.svg')
    timeline.save(svg_path)


if __name__ == '__main__':
    main()
