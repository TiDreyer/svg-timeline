""" Example script to demonstrate the available colors """
from pathlib import Path

from svg_timeline.svg_style_defaults import ColorPalette, SEABORN_COLORS
from svg_timeline.notation import dt
from svg_timeline.timeline import TimelinePlot, TimeSpan
from svg_timeline.timeline_geometry import TimeLineGeometry, GeometrySettings


def draw_colors(tlp: TimelinePlot, palette: ColorPalette, base_year: int):
    n_lanes = 10
    for i in range(len(palette)):
        column = base_year + (i // n_lanes)
        row = i % n_lanes
        start = dt(str(column))
        end = dt(str(column + 1))
        tlp.add_element(TimeSpan(start, end, text=f'c{i:02}', lane=row, palette_color=i))


def main():
    """ main script function for the creation of the plot """
    # defining the range of the timeline
    geometry = TimeLineGeometry(
        start_date=dt('2000'),
        end_date=dt('2001'),
        settings=GeometrySettings(canvas_height=400, canvas_width=400, lane_zero_rel_y_position=0.95)
    )
    timeline = TimelinePlot(geometry=geometry)

    # pick one palette to plot
    # palette = DEFAULT_COLORS
    palette = SEABORN_COLORS
    timeline.css.set_color_palette(palette)

    for i in range(len(palette)):
        timeline.add_element(TimeSpan(geometry.first, geometry.last,
                                      text=f'c{i:02}', lane=i, palette_color=i))

    # saving the SVG
    svg_path = Path(__file__).parent.joinpath('color_palettes.svg')
    timeline.save(svg_path)


if __name__ == '__main__':
    main()
