""" Example script to create a timeline of Emmy Noether's life """
from pathlib import Path

from svg_timeline.style import Defaults, Colors
from svg_timeline.time_calculations import TimeSpacingPerDecade, TimeSpacingPerYear, dt
from svg_timeline.timeline import TimelinePlot

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
    # defining the range of the timeline
    start_date = dt('1879-12-01')
    end_date = dt('1935-12-31')

    # setting what percentage of the page width the arrow occupies
    Defaults.arrow_y_position = 0.85

    # initializing the timeline plot object
    timeline = TimelinePlot(
        size=(1000, 300),
        start_date=start_date,
        end_date=end_date,
        time_spacing=TimeSpacingPerDecade(start_date, end_date),
        minor_tics=TimeSpacingPerYear(start_date, end_date),
    )

    # white text is easier to read on colored timespans
    Defaults.timespan_text_color = 'white'

    # adding the image of Emmy Noether
    _image_path = Path(__file__).parent.joinpath('473px-Noether.jpeg')
    _image_scale = 0.27
    timeline.add_image(_PHOTO, _image_path, width=_image_scale*473, height=_image_scale*720, lane=1)

    # some important dates in her life
    timeline.add_event(_BIRTH, 'Birth', lane=2, classes=[Colors.COLOR_A.name.lower()])
    timeline.add_event(_THESIS, 'PhD Thesis', lane=3, classes=[Colors.COLOR_B.name.lower()])
    timeline.add_event(_THEOREM, 'Noether\'s Theorem', lane=5, classes=[Colors.COLOR_E.name.lower()])
    timeline.add_event(_HABIL, 'Habilitation', lane=3, classes=[Colors.COLOR_C.name.lower()])
    timeline.add_event(_AWARD, 'Ackermann-Teuber Memorial Award', lane=5, classes=[Colors.COLOR_E.name.lower()])

    # scholars distinguish three "epochs" in her work
    timeline.add_timespan(_EPOCH_1, _EPOCH_2, '"1st epoch"', lane=1, classes=[Colors.COLOR_B.name.lower(), 'white_text'])
    timeline.add_timespan(_EPOCH_2, _EPOCH_3, '"2nd epoch"', lane=1, classes=[Colors.COLOR_C.name.lower(), 'white_text'])
    timeline.add_timespan(_EPOCH_3, _DEATH, '"3rd epoch"', lane=1, classes=[Colors.COLOR_D.name.lower(), 'white_text'])

    # the universities she was associated with
    timeline.add_connected_events(
        dates=[_TEACH_ERL, _MOVE_GOE, _MOVE_USA, _DEATH],
        labels=["Erlangen", "Göttingen", "USA", None],
        classes=[[Colors.COLOR_B.name.lower()], [Colors.COLOR_C.name.lower()], [Colors.COLOR_D.name.lower()], []],
        lane=2,
    )

    # adding this date last so it is plotted on top of the time spans
    timeline.add_event(_DEATH, 'Death', lane=4, classes=[Colors.COLOR_A.name.lower()])

    # adding a title to the plot
    timeline.add_title("Emmy Noether")

    # saving the SVG
    svg_path = Path(__file__).parent.joinpath('emmy_noether.svg')
    timeline.save(svg_path)


if __name__ == '__main__':
    main()
