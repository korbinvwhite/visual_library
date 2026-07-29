"""carnaval_viz: a Rio Carnival-inspired data visualization library.

Public API:
    bubble_chart(df, x, y, size, color, ...) -> matplotlib.figure.Figure
    circular_calendar(df, date, size, color, ...) -> matplotlib.figure.Figure

Example:
    >>> import pandas as pd
    >>> import carnaval_viz as viz
    >>> df = pd.read_csv("examples/rio_carnival_blocos.csv")
    >>> bubble_fig = viz.bubble_chart(
    ...     df, x="year_founded", y="estimated_audience",
    ...     size="estimated_audience", color="region",
    ... )
    >>> calendar_fig = viz.circular_calendar(
    ...     df, date="event_date", size="estimated_audience", color="region",
    ... )
"""

from .bubble_chart import bubble_chart
from .circular_calendar import circular_calendar

__version__ = "0.1.0"

__all__ = ["bubble_chart", "circular_calendar"]
