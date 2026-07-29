"""Bubble chart visualization for carnaval_viz."""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from . import colors, styling, validation


def bubble_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    size: str,
    color: str,
    *,
    title: str | None = None,
    figsize: tuple[float, float] = (10, 8),
    alpha: float = 0.7,
    annotate_top: int = 0,
    yscale: str = "log",
) -> Figure:
    """Create a publication-quality bubble chart.

    Each row in df becomes one bubble: its horizontal position comes from
    `x`, vertical position from `y`, size from `size` (square-root scaled,
    so one extreme outlier doesn't crush every other bubble to invisible),
    and color from the category in `color`.

    Args:
        df: The pandas DataFrame containing the data.
        x: Column name for the horizontal axis.
        y: Column name for the vertical axis.
        size: Column name (numeric) that determines bubble size.
        color: Column name (categorical) that determines bubble color.
        title: Custom chart title. Defaults to an auto-generated title.
        figsize: Figure size in inches, as (width, height).
        alpha: Transparency of the bubbles, from 0 (invisible) to 1 (opaque).
        annotate_top: Number of largest bubbles (by `size`) to label with
            their DataFrame index. 0 (the default) disables annotation.
        yscale: "log" (default) or "linear". Log spacing spreads out
            values that would otherwise be crushed near zero by a single
            large outlier; requires every usable `y` value to be positive.

    Returns:
        The Matplotlib Figure containing the bubble chart. Not displayed
        automatically -- call `fig.show()` or `fig.savefig(...)`.

    Raises:
        TypeError: If df is not a pandas DataFrame, or x/y/size are not numeric.
        KeyError: If x, y, size, or color is not a column of df.
        ValueError: If df is empty, no usable rows remain after dropping
            missing values, yscale is unsupported, or yscale="log" is used
            with non-positive y values.

    Example:
        >>> import pandas as pd
        >>> import carnaval_viz as viz
        >>> df = pd.read_csv("examples/rio_carnival_blocos.csv")
        >>> fig = viz.bubble_chart(
        ...     df, x="year_founded", y="estimated_audience",
        ...     size="estimated_audience", color="region",
        ... )
        >>> fig.savefig("bubble_chart.png", dpi=300, bbox_inches="tight")
    """
    validation.require_dataframe(df)
    validation.require_columns_exist(df, [x, y, size, color])
    validation.require_numeric_columns(df, [x, y, size])
    validation.require_non_negative_column(df, size)
    working = validation.select_complete_rows(df, [x, y, size, color])

    if yscale not in ("log", "linear"):
        raise ValueError(f"Unsupported yscale '{yscale}'. Choose 'log' or 'linear'.")
    if yscale == "log" and (working[y] <= 0).any():
        raise ValueError(
            f"yscale='log' requires every usable value in '{y}' to be "
            "positive, but some are zero or negative. Pass yscale='linear' "
            "instead for data that includes zero or negative values."
        )

    color_map = colors.categorical_color_map(working[color])
    legend_order = (
        working.groupby(color)[size].sum().sort_values(ascending=False).index.tolist()
    )
    marker_sizes = styling.scale_marker_sizes(working[size])
    bubble_colors = working[color].map(color_map)

    with styling.carnaval_style():
        fig, ax = plt.subplots(figsize=figsize)

        ax.scatter(
            working[x],
            working[y],
            s=marker_sizes,
            c=bubble_colors,
            alpha=alpha,
            edgecolors=styling.BUBBLE_EDGE_COLOR,
            linewidths=0.6,
        )

        if yscale == "log":
            ax.set_yscale("log")

        if annotate_top > 0:
            top_rows = working.nlargest(annotate_top, size)
            for index, row in top_rows.iterrows():
                ax.annotate(
                    str(index),
                    (row[x], row[y]),
                    xytext=(6, 6),
                    textcoords="offset points",
                    fontsize=8,
                    color=colors.DARK_CHARCOAL,
                )

        ax.legend(
            handles=styling.legend_handles_for_categories(color_map, order=legend_order),
            title=color,
            loc="best",
        )

        styling.strip_spines(ax)
        ax.set_title(title or f"Carnival Blocos: {_pretty(y)} vs. {_pretty(x)}")
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        fig.tight_layout()

    return fig


def _pretty(column_name: str) -> str:
    """Turn a snake_case column name into a title-cased display label."""
    return column_name.replace("_", " ").title()
