# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "svg-timeline",
# ]
# [tool.uv.sources]
# svg-timeline = { path = "../" }
# ///
""" Example script to create a timeline of Emmy Noether's life """
from pathlib import Path

from svg_timeline.time_spacing import TimeSpacingPerDecade, TimeSpacingPerYear
from svg_timeline.timeline import TimelinePlot, Title, TimeArrow, Event, ConnectedEvents, DatedImage, TimeSpan
from svg_timeline.timeline_geometry import TimeLineGeometry, GeometrySettings


def main():
    """ main script function for the creation of the plot """
    # defining the range of the timeline
    birth = '1882-03-23'
    death = '1935-04-14'

    geo_settings = GeometrySettings()
    geo_settings.canvas_width = 1000
    geo_settings.canvas_height = 300
    # setting at what vertical position the arrow is drawn
    geo_settings.lane_zero_rel_y_position = 0.85

    # initializing the timeline plot object
    geometry = TimeLineGeometry(
        start_date='1879-12-01',
        end_date='1935-12-31',
        settings=geo_settings,
    )
    timeline = TimelinePlot(geometry=geometry)

    # adding a title to the plot
    timeline.add_element(Title("Emmy Noether"), layer=2)
    timeline.add_element(TimeArrow(
        major_tics=TimeSpacingPerDecade(geometry.first, geometry.last),
        minor_tics=TimeSpacingPerYear(geometry.first, geometry.last),
    ), layer=2)

    # adding the image of Emmy Noether
    _image_path = Path(__file__).parent.joinpath('473px-Noether.jpeg')
    _image_scale = 0.27
    timeline.add_element(
        DatedImage.from_path('1900', _image_path, width=_image_scale*473, height=_image_scale*720, lane=1)
    )

    plot_elements = [
        # some important dates in her life
        Event(birth, 'Birth', lane=2, palette_color=1),
        Event('1907', 'PhD Thesis', lane=3, palette_color=2),
        Event('1918', 'Noether\'s Theorem', lane=5, palette_color=5),
        Event('1919', 'Habilitation', lane=3, palette_color=3),
        Event('1932', 'Ackermann-Teuber Memorial Award', lane=5, palette_color=5),

        # scholars distinguish three "epochs" in her work
        TimeSpan('1908', '1920', '"1st epoch"', lane=1, palette_color=2),
        TimeSpan('1920', '1927', '"2nd epoch"', lane=1, palette_color=3),
        TimeSpan('1927', death, '"3rd epoch"', lane=1, palette_color=4),

        # the universities she was associated with
        ConnectedEvents(
            dates=['1908', '1915-04', '1933', death],
            labels=["Erlangen", "Göttingen", "USA", None],
            palette_colors=[2, 3, 4, 0],
            lane=2,
        ),
    ]
    for event in plot_elements:
        timeline.add_element(event)

    # adding this date on layer 2 so it is plotted on top of the other elements
    timeline.add_element(Event(death, 'Death', lane=4, palette_color=1), layer=2)

    # saving the SVG
    svg_path = Path(__file__).parent.joinpath('emmy_noether.svg')
    timeline.save(svg_path)

    # # saving as JSON (uncomment to update test data)
    # from svg_timeline.json_serialize import save_json
    # json_path = Path(__file__).parent.joinpath('../test/files/emmy_noether.json')
    # save_json(timeline, json_path)


if __name__ == '__main__':
    main()
