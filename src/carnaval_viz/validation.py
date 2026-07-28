"""Reusable input-validation helpers for carnaval_viz.

Each function checks one thing about the user's input and raises a
specific, informative exception when something is wrong -- so both
`histogram()` and `correlation()` can share the same checks instead of
duplicating logic.
"""

import pandas as pd


def require_dataframe(df) -> None:
    """Raise TypeError if df is not a pandas DataFrame.

    Args:
        df: The object to check.

    Raises:
        TypeError: If df is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"Expected a pandas DataFrame, got {type(df).__name__}. "
            "Pass a DataFrame, e.g. df = pd.read_csv('your_file.csv')."
        )


def require_column_exists(df: pd.DataFrame, column: str) -> None:
    """Raise KeyError if column is not a column of df.

    Args:
        df: The DataFrame to check.
        column: The column name to look for.

    Raises:
        KeyError: If column is not present in df.
    """
    if column not in df.columns:
        available = ", ".join(map(str, df.columns))
        raise KeyError(
            f"Column '{column}' was not found in the DataFrame. "
            f"Available columns: {available}."
        )


def require_numeric_column(df: pd.DataFrame, column: str) -> pd.Series:
    """Confirm a column is numeric and return it with missing values dropped.

    Args:
        df: The DataFrame containing the column.
        column: The name of the column to validate.

    Returns:
        The column as a pandas Series with NaN values removed.

    Raises:
        TypeError: If the column's dtype is not numeric.
        ValueError: If no usable (non-missing) values remain.
    """
    series = df[column]

    # A column that is entirely missing values (e.g. all None) is reported
    # as "no usable values" rather than "wrong dtype": pandas can't infer a
    # real dtype for it, and either message would technically be accurate,
    # but this one is more actionable.
    cleaned = series.dropna()
    if cleaned.empty:
        raise ValueError(
            f"Column '{column}' has no usable (non-missing) numeric values "
            "to plot."
        )

    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError(
            f"Column '{column}' must be numeric to plot, but it has dtype "
            f"'{series.dtype}'. Convert it first, e.g. "
            f"df['{column}'] = pd.to_numeric(df['{column}'], errors='coerce')."
        )

    return cleaned


def select_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select only numeric columns from a DataFrame and confirm there are enough.

    Args:
        df: The DataFrame to inspect.

    Returns:
        A DataFrame containing only the numeric columns of df that have at
        least one usable (non-missing) value.

    Raises:
        ValueError: If fewer than two such numeric columns exist.
    """
    numeric_df = df.select_dtypes(include="number")
    usable_columns = [col for col in numeric_df.columns if numeric_df[col].notna().any()]
    numeric_df = numeric_df[usable_columns]

    if numeric_df.shape[1] < 2:
        raise ValueError(
            "At least two numeric columns with usable data are required to "
            f"compute a correlation heatmap, but only {numeric_df.shape[1]} "
            "were found. Add more numeric columns or check for missing data."
        )
    return numeric_df


def require_supported_correlation_method(method: str) -> None:
    """Raise ValueError if method is not a supported correlation method.

    Args:
        method: The correlation method name to check.

    Raises:
        ValueError: If method is not one of 'pearson', 'spearman', or 'kendall'.
    """
    supported = ("pearson", "spearman", "kendall")
    if method not in supported:
        raise ValueError(
            f"Unsupported correlation method '{method}'. "
            f"Choose one of: {', '.join(supported)}."
        )
