"""Correlation heatmap visualization for carnaval_viz."""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from . import colors, styling, validation


def correlation(
    df: pd.DataFrame,
    *,
    method: str = "pearson",
    annotate: bool = True,
    title: str | None = None,
    figsize: tuple[float, float] | None = None,
) -> Figure:
    """Create a polished correlation heatmap for a DataFrame's numeric columns.

    Args:
        df: The pandas DataFrame containing the data.
        method: Correlation method: "pearson", "spearman", or "kendall".
        annotate: Whether to display each cell's correlation value, rounded
            to two decimal places.
        title: Custom chart title. Defaults to an auto-generated title
            based on the correlation method.
        figsize: Figure size in inches, as (width, height). Defaults to a
            size computed automatically from the number of numeric columns.

    Returns:
        The Matplotlib Figure containing the heatmap. The figure is not
        displayed automatically -- call `fig.show()` in a notebook or
        `fig.savefig(...)` to save it.

    Raises:
        TypeError: If df is not a pandas DataFrame.
        ValueError: If fewer than two usable numeric columns exist, or if
            method is not a supported correlation method.

    Example:
        >>> import pandas as pd
        >>> import carnaval_viz as viz
        >>> df = pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]})
        >>> fig = viz.correlation(df)
        >>> fig.savefig("correlation.png", dpi=300, bbox_inches="tight")
    """
    validation.require_dataframe(df)
    validation.require_supported_correlation_method(method)
    numeric_df = validation.select_numeric_columns(df)

    corr_matrix = numeric_df.corr(method=method)
    n_columns = len(corr_matrix.columns)
    resolved_figsize = figsize or _resolve_figsize(n_columns)

    with styling.carnaval_style():
        # plt.subplots() (rather than Figure() directly) registers the figure
        # with pyplot, so fig.show() works as documented in the README.
        fig, ax = plt.subplots(figsize=resolved_figsize)

        image = ax.imshow(
            corr_matrix.values,
            cmap=colors.CORRELATION_CMAP,
            vmin=-1,
            vmax=1,
            aspect="equal",
        )

        ax.set_xticks(range(n_columns))
        ax.set_yticks(range(n_columns))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr_matrix.columns)
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

        if annotate:
            _annotate_cells(ax, corr_matrix)

        colorbar = fig.colorbar(image, ax=ax, shrink=0.85)
        colorbar.set_label("Correlation")
        colorbar.outline.set_visible(False)

        ax.set_title(title or f"{method.title()} Correlation Heatmap")
        fig.tight_layout()

    return fig


def _annotate_cells(ax, corr_matrix: pd.DataFrame) -> None:
    """Write each cell's correlation value, choosing readable text color per cell."""
    values = corr_matrix.values
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            value = values[row, col]
            text_color = colors.LIGHT_CREAM if abs(value) > 0.6 else colors.DARK_CHARCOAL
            ax.text(
                col,
                row,
                f"{value:.2f}",
                ha="center",
                va="center",
                color=text_color,
                fontsize=9,
            )


def _resolve_figsize(n_columns: int) -> tuple[float, float]:
    """Scale figure size with the number of numeric columns, within sane bounds."""
    side = min(max(n_columns * 0.9, 5), 14)
    return (side, side)
