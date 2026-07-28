"""Histogram visualization for carnaval_viz."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from . import colors, styling, validation


def histogram(
    df: pd.DataFrame,
    column: str,
    *,
    bins="auto",
    title: str | None = None,
    xlabel: str | None = None,
    show_mean: bool = True,
    show_median: bool = True,
    figsize: tuple[float, float] = (10, 6),
) -> Figure:
    """Create a polished histogram for one numeric DataFrame column.

    Args:
        df: The pandas DataFrame containing the data.
        column: Name of the numeric column to plot.
        bins: Bin specification passed to Matplotlib's hist. Defaults to
            "auto", which lets Matplotlib/NumPy choose a sensible bin count.
        title: Custom chart title. Defaults to an auto-generated title
            based on the column name.
        xlabel: Custom x-axis label. Defaults to the column name.
        show_mean: Whether to draw a vertical line at the mean.
        show_median: Whether to draw a vertical line at the median.
        figsize: Figure size in inches, as (width, height).

    Returns:
        The Matplotlib Figure containing the histogram. The figure is not
        displayed automatically -- call `fig.show()` in a notebook or
        `fig.savefig(...)` to save it.

    Raises:
        TypeError: If df is not a pandas DataFrame, or column is not numeric.
        KeyError: If column is not a column of df.
        ValueError: If column has no usable (non-missing) numeric values.

    Example:
        >>> import pandas as pd
        >>> import carnaval_viz as viz
        >>> df = pd.DataFrame({"danceability": [0.6, 0.7, 0.8, 0.65]})
        >>> fig = viz.histogram(df, "danceability")
        >>> fig.savefig("danceability.png", dpi=300, bbox_inches="tight")
    """
    validation.require_dataframe(df)
    validation.require_column_exists(df, column)
    values = validation.require_numeric_column(df, column)

    resolved_bins = _resolve_bin_count(values) if bins == "auto" else bins

    with styling.carnaval_style():
        fig, ax = _new_figure(figsize)

        ax.hist(
            values,
            bins=resolved_bins,
            color=colors.HISTOGRAM_BAR_COLOR,
            edgecolor=colors.FIGURE_BACKGROUND,
            linewidth=0.8,
        )

        legend_handles = []
        if show_mean:
            mean_value = values.mean()
            ax.axvline(
                mean_value,
                color=colors.MEAN_LINE_COLOR,
                **styling.REFERENCE_LINE_STYLE,
            )
            legend_handles.append(
                Line2D(
                    [0],
                    [0],
                    color=colors.MEAN_LINE_COLOR,
                    label=f"Mean: {mean_value:.2f}",
                    **styling.REFERENCE_LINE_STYLE,
                )
            )

        if show_median:
            median_value = values.median()
            ax.axvline(
                median_value,
                color=colors.MEDIAN_LINE_COLOR,
                **styling.REFERENCE_LINE_STYLE,
            )
            legend_handles.append(
                Line2D(
                    [0],
                    [0],
                    color=colors.MEDIAN_LINE_COLOR,
                    label=f"Median: {median_value:.2f}",
                    **styling.REFERENCE_LINE_STYLE,
                )
            )

        if legend_handles:
            ax.legend(handles=legend_handles, loc="upper right")

        styling.strip_spines(ax)
        ax.set_title(title or f"Distribution of {column}")
        ax.set_xlabel(xlabel or column)
        ax.set_ylabel("Count")
        fig.tight_layout()

    return fig


def _new_figure(figsize: tuple[float, float]):
    """Create a new Figure and single Axes pair.

    Uses `plt.subplots()` (rather than instantiating `Figure()` directly) so
    the returned figure is registered with pyplot and `fig.show()` works as
    documented in the README. Callers that generate many figures in a loop
    should call `plt.close(fig)` afterward to free memory, since pyplot
    keeps a reference to every figure it creates until closed.
    """
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def _resolve_bin_count(values: pd.Series) -> int:
    """Pick a reasonable bin count for a numeric series using NumPy's auto rule."""
    bin_edges = np.histogram_bin_edges(values, bins="auto")
    return max(len(bin_edges) - 1, 1)
