"""carnaval_viz: a small, Brazil-inspired data visualization library.

Public API:
    histogram(df, column, ...) -> matplotlib.figure.Figure
    correlation(df, ...) -> matplotlib.figure.Figure

Example:
    >>> import pandas as pd
    >>> import carnaval_viz as viz
    >>> df = pd.read_csv("brazilian_music.csv")
    >>> hist_fig = viz.histogram(df, "danceability")
    >>> corr_fig = viz.correlation(df)
"""

from .correlation import correlation
from .histogram import histogram

__version__ = "0.1.0"

__all__ = ["histogram", "correlation"]
