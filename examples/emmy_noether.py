""" Example script to create a timeline of Emmy Noether's life """
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from svg_timeline.style import Defaults
from svg_timeline.time_calculations import TimeSpacingPerDecade, TimeSpacingPerYear
from svg_timeline.timeline import TimelinePlot

# defining important dates for easier usage later on
_BIRTH = datetime.fromisoformat('1882-03-23')
_PHOTO = datetime.fromisoformat('1900-01-01')
_THESIS = datetime.fromisoformat('1907-01-01')
_TEACH_ERL = datetime.fromisoformat('1908-01-01')
_EPOCH_1 = datetime.fromisoformat('1908-01-01')
_MOVE_GOE = datetime.fromisoformat('1915-04-01')
_THEOREM = datetime.fromisoformat('1918-01-01')
_HABIL = datetime.fromisoformat('1919-01-01')
_EPOCH_2 = datetime.fromisoformat('1920-01-01')
_EPOCH_3 = datetime.fromisoformat('1927-01-01')
_AWARD = datetime.fromisoformat('1932-01-01')
_MOVE_USA = datetime.fromisoformat('1933-01-01')
_DEATH = datetime.fromisoformat('1935-04-14')

# defining colors to be used in the plot
class Color(StrEnum):
    a='#003f5c'
    b='#58508d'
    c='#bc5090'
    d='#ff6361'
    e='#ffa600'


def main():
    """ main script function for the creation of the plot """
    # defining the range of the timeline
    start_date = datetime.fromisoformat('1881-09-01')
    end_date = datetime.fromisoformat('1936-01-01')

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
    _image_scale = 0.3
    timeline.add_image(_PHOTO, _image_path, width=_image_scale*473, height=_image_scale*720, lane=1)

    # some important dates in her life
    timeline.add_event(_BIRTH, 'Birth', lane=1, color=Color.a)
    timeline.add_event(_THESIS, 'PhD Thesis', lane=3, color=Color.b)
    timeline.add_event(_THEOREM, 'Noether\'s Theorem', lane=4, color=Color.e)
    timeline.add_event(_HABIL, 'Habilitation', lane=3, color=Color.c)
    timeline.add_event(_AWARD, 'Ackermann-Teuber Memorial Award', lane=4, color=Color.e)

    # the universities she was associated with
    timeline.add_timespan(_TEACH_ERL, _MOVE_GOE, "Erlangen", lane=1, color=Color.b)
    timeline.add_timespan(_MOVE_GOE, _MOVE_USA, "Göttingen", lane=1, color=Color.c)
    timeline.add_timespan(_MOVE_USA, _DEATH, "USA", lane=1, color=Color.d)

    # scholars distinguish three "epochs" in her work
    timeline.add_timespan(_EPOCH_1, _EPOCH_2, '"1st epoch"', lane=2, color=Color.b)
    timeline.add_timespan(_EPOCH_2, _EPOCH_3, '"2nd epoch"', lane=2, color=Color.c)
    timeline.add_timespan(_EPOCH_3, _DEATH, '"3rd epoch"', lane=2, color=Color.d)

    # adding this date last so it is plotted on top of the time spans
    timeline.add_event(_DEATH, 'Death', lane=3, color=Color.a)

    # adding a title to the plot
    timeline.add_title("Emmy Noether")

    # saving the SVG
    svg_path = Path(__file__).parent.joinpath('../output/emmy_noether.svg')
    timeline.save(svg_path)


if __name__ == '__main__':
    main()
