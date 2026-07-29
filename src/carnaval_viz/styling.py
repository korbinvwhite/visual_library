"""Shared styling for carnaval_viz charts.

Provides a single context manager, `carnaval_style()`, that both
`bubble_chart()` and `carnival_calendar()` use to apply consistent fonts,
colors, and spacing to just the figure being built -- without permanently
changing Matplotlib's global settings for the rest of the user's program.
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

# Shared transparency for bubble markers in both charts. The calendar uses
# a lower value than the bubble chart because its points overlap much more
# (many events cluster on the same few Carnival dates).
BUBBLE_ALPHA = 0.7
CALENDAR_BUBBLE_ALPHA = 0.6
CALENDAR_MAX_BUBBLE_AREA = 900
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
    transform: str = "sqrt",
) -> np.ndarray:
    """Scale numeric values into Matplotlib scatter marker areas.

    Matplotlib's scatter `s` parameter is an area (in points^2). By default,
    values are square-root transformed before scaling, which softens the
    influence of extreme outliers (e.g. one bloco with a 1.5-million-person
    audience) so mid-sized values stay visually distinguishable, rather
    than being crushed to near-identical tiny bubbles.

    Args:
        values: The numeric values to scale (e.g. estimated audience).
        min_area: The marker area assigned to the smallest value.
        max_area: The marker area assigned to the largest value.
        transform: How to compress the values before scaling: "sqrt"
            (default, recommended when values span a wide range),
            "log" (even stronger compression), or "linear" (no
            compression -- area is directly proportional to value).

    Returns:
        A NumPy array of marker areas the same length as values.

    Raises:
        ValueError: If transform is not "sqrt", "log", or "linear".
    """
    if transform == "sqrt":
        transformed = np.sqrt(values)
    elif transform == "log":
        transformed = np.log1p(values)
    elif transform == "linear":
        transformed = values
    else:
        raise ValueError(
            f"Unsupported transform '{transform}'. Choose one of: "
            "'sqrt', 'log', 'linear'."
        )

    value_min, value_max = transformed.min(), transformed.max()
    if value_max == value_min:
        return np.full(len(values), (min_area + max_area) / 2)

    normalized = (transformed - value_min) / (value_max - value_min)
    return min_area + normalized * (max_area - min_area)


def legend_handles_for_categories(
    color_map: dict, order: list | None = None
) -> list[Line2D]:
    """Build proxy legend handles (colored dots) for a category-color mapping.

    Args:
        color_map: A dict mapping category values to hex color strings, as
            returned by `colors.categorical_color_map()`.
        order: Optional list of category values specifying the order
            legend entries should appear in (e.g. regions sorted by total
            audience, largest first). Defaults to color_map's own order.

    Returns:
        A list of Line2D proxy artists suitable for passing to
        `ax.legend(handles=...)`.
    """
    categories = order if order is not None else list(color_map.keys())
    return [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="",
            markerfacecolor=color_map[category],
            markeredgecolor=color_map[category],
            label=str(category),
        )
        for category in categories
    ]


def scale_radius(
    values: pd.Series, min_radius: float, max_radius: float
) -> np.ndarray:
    """Linearly scale numeric values into a radius range.

    Args:
        values: The numeric values to scale (e.g. hour of day, 0-24).
        min_radius: The radius assigned to the smallest value.
        max_radius: The radius assigned to the largest value.

    Returns:
        A NumPy array of radius values the same length as values.
    """
    value_min, value_max = values.min(), values.max()
    if value_max == value_min:
        return np.full(len(values), (min_radius + max_radius) / 2)

    normalized = (values - value_min) / (value_max - value_min)
    return min_radius + normalized * (max_radius - min_radius)
