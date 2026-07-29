"""Shared styling for carnaval_viz charts.

Provides a single context manager, `carnaval_style()`, that both
`histogram()` and `correlation()` use to apply consistent fonts, colors,
and spacing to just the figure being built -- without permanently changing
Matplotlib's global settings for the rest of the user's program.
"""

from contextlib import contextmanager

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from . import colors

# rcParams is Matplotlib's dictionary of default settings (font sizes,
# colors, spacing, etc.). We only ever apply these inside an
# `rc_context`, which temporarily overrides them and automatically
# restores the previous settings afterward.
_STYLE_RC = {
    "figure.facecolor": colors.FIGURE_BACKGROUND,
    "axes.facecolor": colors.AXES_BACKGROUND,
    "axes.edgecolor": colors.TEXT_COLOR,
    "axes.labelcolor": colors.TEXT_COLOR,
    "axes.titlecolor": colors.TEXT_COLOR,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "axes.axisbelow": True,
    "grid.color": colors.GRID_COLOR,
    "grid.alpha": 0.6,
    "grid.linewidth": 0.6,
    "xtick.color": colors.TEXT_COLOR,
    "ytick.color": colors.TEXT_COLOR,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "font.size": 11,
    "font.family": "sans-serif",
    "text.color": colors.TEXT_COLOR,
    "legend.fontsize": 10,
    "legend.frameon": False,
    "figure.dpi": 100,
}

# Default marker area range (in points^2, Matplotlib scatter's native size
# unit) that bubble values are scaled into.
MIN_BUBBLE_AREA = 40
MAX_BUBBLE_AREA = 2000

# Shared transparency for bubble markers in both charts.
BUBBLE_ALPHA = 0.7
BUBBLE_EDGE_COLOR = colors.LIGHT_CREAM


@contextmanager
def carnaval_style():
    """Temporarily apply the carnaval_viz look to figures created inside the block.

    Usage example:
        with carnaval_style():
            fig, ax = plt.subplots()
            ...

    Yields:
        None. Settings are restored automatically on exit, so charts
        created outside the `with` block are unaffected.
    """
    with plt.rc_context(rc=_STYLE_RC):
        yield


def strip_spines(ax):
    """Remove the top and right borders (spines) of a plot axis.

    Args:
        ax: A Matplotlib Axes object to clean up.
    """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def scale_marker_sizes(
    values: pd.Series,
    min_area: float = MIN_BUBBLE_AREA,
    max_area: float = MAX_BUBBLE_AREA,
) -> np.ndarray:
    """Scale numeric values into Matplotlib scatter marker areas.

    Matplotlib's scatter `s` parameter is an area (in points^2), so values
    are scaled linearly rather than by radius -- this keeps the visual area
    of each bubble proportional to its underlying value, which is what
    makes a bubble chart's sizes readable at a glance.

    Args:
        values: The numeric values to scale (e.g. estimated audience).
        min_area: The marker area assigned to the smallest value.
        max_area: The marker area assigned to the largest value.

    Returns:
        A NumPy array of marker areas the same length as values.
    """
    value_min, value_max = values.min(), values.max()
    if value_max == value_min:
        return np.full(len(values), (min_area + max_area) / 2)

    normalized = (values - value_min) / (value_max - value_min)
    return min_area + normalized * (max_area - min_area)


def legend_handles_for_categories(color_map: dict) -> list[Line2D]:
    """Build proxy legend handles (colored dots) for a category-color mapping.

    Args:
        color_map: A dict mapping category values to hex color strings, as
            returned by `colors.categorical_color_map()`.

    Returns:
        A list of Line2D proxy artists suitable for passing to
        `ax.legend(handles=...)`.
    """
    return [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="",
            markerfacecolor=color,
            markeredgecolor=color,
            label=str(category),
        )
        for category, color in color_map.items()
    ]
