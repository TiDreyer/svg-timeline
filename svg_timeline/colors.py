""" Color palettes that can be configured for a plot """
from dataclasses import dataclass


@dataclass
class Color:
    """ a color with corresponding foreground text color"""
    color: str
    top_text_color: str = '#000000'  # default to black text


class ColorPalette(tuple[Color]):
    """ a pre-defined list of colors to be used for a plot """
    pass


DEFAULT_COLORS = ColorPalette((
    Color('#000000', '#ffffff'),  # black with white text
    Color('#003f5c', '#ffffff'),  # dark blue with white text
    Color('#58508d', '#ffffff'),  # purple-blue with white text
    Color('#bc5090'),  # purple
    Color('#ff6361'),  # light red
    Color('#ffa600'),  # golden
))

# Default seaborn color palette as generated via:
# > print(sns.color_palette().as_hex())
SEABORN_COLORS = ColorPalette((
    Color('#000000', '#ffffff'),  # black with white text
    Color('#1f77b4'),  # blue
    Color('#ff7f0e'),  # orange
    Color('#2ca02c'),  # green
    Color('#d62728'),  # red
    Color('#9467bd'),  # purple
    Color('#8c564b'),  # brown
    Color('#e377c2'),  # pink
    Color('#7f7f7f'),  # grey
    Color('#bcbd22'),  # lime
    Color('#17becf'),  # cyan
))
