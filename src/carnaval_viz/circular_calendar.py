"""Circular calendar visualization for carnaval_viz."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from . import colors, styling, validation

_MONTH_LABELS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]
# Day-of-year (non-leap) that each month starts on, used to place the month
# labels around the circle at even calendar positions.
_MONTH_START_DAYS = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

_POINT_RADIUS = 1.0


def circular_calendar(
    df: pd.DataFrame,
    date: str,
    size: str,
    color: str,
    *,
    title: str | None = None,
    figsize: tuple[float, float] = (10, 10),
) -> Figure:
    """Display events around a circular calendar.

    Each row in df becomes one point placed around a circle: its angular
    position comes from `date` (mapped onto the calendar year), its size
    from `size`, and its color from the category in `color`. All points sit
    at the same distance from the center -- the circular layout represents
    a full year (or season) at a glance, not a magnitude.

    Args:
        df: The pandas DataFrame containing the data.
        date: Column name containing event dates (parsed automatically).
        size: Column name (numeric) that determines point size.
        color: Column name (categorical) that determines point color.
        title: Custom chart title. Defaults to "Circular Calendar".
        figsize: Figure size in inches, as (width, height).

    Returns:
        The Matplotlib Figure containing the circular calendar. Not
        displayed automatically -- call `fig.show()` or `fig.savefig(...)`.

    Raises:
        TypeError: If df is not a pandas DataFrame, or size is not numeric.
        KeyError: If date, size, or color is not a column of df.
        ValueError: If df is empty, the date column has no parseable dates,
            or no usable rows remain after dropping missing values.

    Example:
        >>> import pandas as pd
        >>> import carnaval_viz as viz
        >>> df = pd.read_csv("examples/rio_carnival_blocos.csv")
        >>> fig = viz.circular_calendar(
        ...     df, date="event_date", size="estimated_audience", color="region",
        ... )
        >>> fig.savefig("circular_calendar.png", dpi=300, bbox_inches="tight")
    """
    validation.require_dataframe(df)
    validation.require_columns_exist(df, [date, size, color])
    validation.require_numeric_columns(df, [size])

    working = df.copy()
    working[date] = validation.coerce_datetime_column(working, date)
    working = validation.select_complete_rows(working, [date, size, color])

    color_map = colors.categorical_color_map(working[color])
    marker_sizes = styling.scale_marker_sizes(working[size])
    point_colors = working[color].map(color_map)
    theta = _dates_to_angles(working[date])

    with styling.carnaval_style():
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, polar=True)
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)

        ax.scatter(
            theta,
            np.full(len(working), _POINT_RADIUS),
            s=marker_sizes,
            c=point_colors,
            alpha=styling.BUBBLE_ALPHA,
            edgecolors=styling.BUBBLE_EDGE_COLOR,
            linewidths=0.6,
        )

        month_angles = [2 * np.pi * day / 365 for day in _MONTH_START_DAYS]
        ax.set_xticks(month_angles)
        ax.set_xticklabels(_MONTH_LABELS)
        ax.set_yticklabels([])
        ax.set_ylim(0, _POINT_RADIUS * 1.15)

        ax.legend(
            handles=styling.legend_handles_for_categories(color_map),
            title=color,
            loc="upper right",
            bbox_to_anchor=(1.25, 1.1),
        )

        ax.set_title(title or "Circular Calendar", pad=30)
        fig.tight_layout()

    return fig


def _dates_to_angles(dates: pd.Series) -> np.ndarray:
    """Map a Series of dates onto angular positions (0 to 2*pi) around a year."""
    days_in_year = np.where(dates.dt.is_leap_year, 366, 365)
    return 2 * np.pi * (dates.dt.dayofyear - 1) / days_in_year
