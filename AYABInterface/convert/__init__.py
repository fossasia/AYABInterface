"""Conversion of colors to needle positions."""
from collections import namedtuple

NeedlePositions = namedtuple("NeedlePositions", ["needle_coloring", "colors",
                                                 "two_colors"])


def _row_color(row, color):
    return [(0 if color_ == color else 1) for color_ in row]


def colors_to_needle_positions(rows):
    """Convert rows to needle positions.

    :return:
    :rtype: list
    """
    needles = []
    for row in rows:
        colors = set(row)
        if len(colors) == 1:
            needles.append([NeedlePositions(row, tuple(colors), False)])
        elif len(colors) == 2:
            color1, color2 = colors
            if color1 != row[0]:
                color1, color2 = color2, color1
            needles_ = _row_color(row, color1)
            needles.append([NeedlePositions(needles_, (color1, color2), True)])
        else:
            colors = []
            for color in row:
                if color not in colors:
                    colors.append(color)
            needles_ = []
            for color in colors:
                needles_.append(NeedlePositions(_row_color(row, color),
                                                (color,), False))
            needles.append(needles_)
    return needles

__all__ = ["colors_to_needle_positions", "NeedlePositions"]
