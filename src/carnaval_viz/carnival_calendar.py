"""Carnival calendar visualization for carnaval_viz."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from . import colors, styling, validation

_MIN_RADIUS = 0.3
_MAX_RADIUS = 1.0
_N_RADIAL_TICKS = 4

# The season's date range is mapped onto only part of the full circle, not
# all 2*pi radians of it -- otherwise the first and last day of the season
# would land at the exact same angle (like a clock's 12 marking both an
# end and a start), since a date range isn't actually cyclic the way a
# calendar year is. This reserves a gap at the top to keep them visually
# distinct.
_GAP_RADIANS = np.radians(20)
_SPAN_RADIANS = 2 * np.pi - _GAP_RADIANS


def carnival_calendar(
    df: pd.DataFrame,
    date: str,
    time: str,
    size: str,
    color: str,
    *,
    title: str | None = None,
    figsize: tuple[float, float] = (10, 10),
) -> Figure:
    """Display events around a Carnival-season calendar wheel.

    Each row in df becomes one point placed around a circle: its angular
    position comes from `date` (mapped across just the date range present
    in the data, not the full year, so a short event season isn't lost in
    a mostly-empty circle), its distance from the center comes from `time`
    (the event's clock time, so earlier events sit closer to the center
    and later ones nearer the rim), its size from `size`, and its color
    from the category in `color`.

    Args:
        df: The pandas DataFrame containing the data.
        date: Column name containing event dates (parsed automatically).
        time: Column name containing clock times (e.g. "16:00:00"),
            parsed automatically and mapped to radius.
        size: Column name (numeric) that determines point size.
        color: Column name (categorical) that determines point color.
        title: Custom chart title. Defaults to "Rio Carnival Parade Calendar".
        figsize: Figure size in inches, as (width, height).

    Returns:
        The Matplotlib Figure containing the calendar. Not displayed
        automatically -- call `fig.show()` or `fig.savefig(...)`.

    Raises:
        TypeError: If df is not a pandas DataFrame, or size is not numeric.
        KeyError: If date, time, size, or color is not a column of df.
        ValueError: If df is empty, the date or time column has no
            parseable values, or no usable rows remain after dropping
            missing values.

    Example:
        >>> import pandas as pd
        >>> import carnaval_viz as viz
        >>> df = pd.read_csv("examples/rio_carnival_blocos.csv")
        >>> fig = viz.carnival_calendar(
        ...     df, date="event_date", time="gathering_time",
        ...     size="estimated_audience", color="region",
        ... )
        >>> fig.savefig("carnival_calendar.png", dpi=300, bbox_inches="tight")
    """
    validation.require_dataframe(df)
    validation.require_columns_exist(df, [date, time, size, color])
    validation.require_numeric_columns(df, [size])
    validation.require_non_negative_column(df, size)

    working = df.copy()
    working[date] = validation.coerce_datetime_column(working, date)
    working[time] = validation.coerce_time_of_day_column(working, time)
    working = validation.select_complete_rows(working, [date, time, size, color])

    color_map = colors.categorical_color_map(working[color])
    marker_sizes = styling.scale_marker_sizes(
        working[size], max_area=styling.CALENDAR_MAX_BUBBLE_AREA
    )
    point_colors = working[color].map(color_map)

    min_date, max_date = working[date].min(), working[date].max()
    theta = _dates_to_angles(working[date], min_date, max_date)
    radii = styling.scale_radius(working[time], _MIN_RADIUS, _MAX_RADIUS)

    with styling.carnaval_style():
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, polar=True)
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)

        ax.scatter(
            theta,
            radii,
            s=marker_sizes,
            c=point_colors,
            alpha=styling.CALENDAR_BUBBLE_ALPHA,
            edgecolors=styling.BUBBLE_EDGE_COLOR,
            linewidths=0.6,
        )

        tick_angles, tick_labels = _weeks_before_ticks(min_date, max_date)
        ax.set_xticks(tick_angles)
        ax.set_xticklabels(tick_labels)

        radial_ticks = np.linspace(_MIN_RADIUS, _MAX_RADIUS, _N_RADIAL_TICKS)
        hour_min, hour_max = working[time].min(), working[time].max()
        hour_ticks = np.linspace(hour_min, hour_max, _N_RADIAL_TICKS)
        ax.set_rticks(radial_ticks)
        ax.set_yticklabels([_format_hour(hour) for hour in hour_ticks])
        ax.set_ylim(0, _MAX_RADIUS * 1.15)

        ax.legend(
            handles=styling.legend_handles_for_categories(color_map),
            title=color,
            loc="upper right",
            bbox_to_anchor=(1.25, 1.1),
        )

        ax.set_title(title or "Rio Carnival Parade Calendar", pad=30)
        fig.tight_layout()

    return fig


def _dates_to_angles(dates: pd.Series, min_date, max_date) -> np.ndarray:
    """Map dates onto angular positions across the season's own span.

    Unlike a full-year calendar, this spreads the actual event dates across
    almost the whole circle (see _GAP_RADIANS) -- so a season that only
    spans a few weeks isn't squeezed into a small arc surrounded by empty
    space.
    """
    span_days = (max_date - min_date).days
    if span_days == 0:
        return np.zeros(len(dates))
    return _SPAN_RADIANS * (dates - min_date).dt.days / span_days


def _weeks_before_ticks(min_date, max_date) -> tuple[list[float], list[str]]:
    """Build tick angles/labels counting down in weeks to the final event date."""
    span_days = (max_date - min_date).days
    if span_days == 0:
        return [0.0], ["Event Day"]

    n_weeks = span_days // 7
    tick_days = [week * 7 for week in range(n_weeks + 1)]
    if tick_days[-1] != span_days:
        tick_days.append(span_days)

    angles = [_SPAN_RADIANS * day / span_days for day in tick_days]
    labels = []
    for day in tick_days:
        weeks_before = round((span_days - day) / 7)
        if weeks_before == 0:
            labels.append("Event Day")
        elif weeks_before == 1:
            labels.append("1 Week Before")
        else:
            labels.append(f"{weeks_before} Weeks Before")
    return angles, labels


def _format_hour(hour: float) -> str:
    """Format a fractional 24-hour value (e.g. 16.5) as a 12-hour clock string ("4:30 PM")."""
    hours_24 = int(hour) % 24
    minutes = int(round((hour - int(hour)) * 60))
    period = "AM" if hours_24 < 12 else "PM"
    hours_12 = hours_24 % 12 or 12
    return f"{hours_12}:{minutes:02d} {period}"
