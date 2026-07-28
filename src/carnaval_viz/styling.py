"""Shared styling for carnaval_viz charts.

Provides a single context manager, `carnaval_style()`, that both
`histogram()` and `correlation()` use to apply consistent fonts, colors,
and spacing to just the figure being built -- without permanently changing
Matplotlib's global settings for the rest of the user's program.
"""

from contextlib import contextmanager

import matplotlib.pyplot as plt

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

# Shared reference-line style for the histogram's mean/median markers.
REFERENCE_LINE_STYLE = {
    "linewidth": 2,
    "linestyle": "--",
}


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
