"""Reusable input-validation helpers for carnaval_viz.

Each function checks one thing about the user's input and raises a
specific, informative exception when something is wrong -- so both
`bubble_chart()` and `circular_calendar()` can share the same checks
instead of duplicating logic.
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
    if df.empty:
        raise ValueError(
            "The DataFrame is empty. Pass a DataFrame that contains at "
            "least one row of data."
        )


def require_columns_exist(df: pd.DataFrame, columns: list[str]) -> None:
    """Raise KeyError if any of columns is not a column of df.

    Args:
        df: The DataFrame to check.
        columns: The column names to look for.

    Raises:
        KeyError: If any column in columns is not present in df.
    """
    missing = [column for column in columns if column not in df.columns]
    if missing:
        available = ", ".join(map(str, df.columns))
        raise KeyError(
            f"Column(s) {missing} were not found in the DataFrame. "
            f"Available columns: {available}."
        )


def require_numeric_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """Raise TypeError if any of columns is not numeric.

    Args:
        df: The DataFrame to check.
        columns: The column names that must be numeric.

    Raises:
        TypeError: If any column in columns is not a numeric dtype.
    """
    for column in columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise TypeError(
                f"Column '{column}' must be numeric, but it has dtype "
                f"'{df[column].dtype}'. Convert it first, e.g. "
                f"df['{column}'] = pd.to_numeric(df['{column}'], errors='coerce')."
            )


def coerce_datetime_column(df: pd.DataFrame, column: str) -> pd.Series:
    """Parse a column to datetime, raising an error if it's unusable.

    Args:
        df: The DataFrame containing the column.
        column: The name of the date column to parse.

    Returns:
        The column converted to pandas datetime values. Entries that can't
        be parsed become NaT (missing) rather than raising, so callers can
        drop them the same way as any other missing value.

    Raises:
        ValueError: If no value in the column can be parsed as a date.

    Note:
        Slash-separated dates (dd/mm/yyyy vs. mm/dd/yyyy) are ambiguous
        when both the day and month are 12 or less. This function relies
        on pandas to detect day-first formatting automatically, which it
        does reliably as soon as any row in the column has a day above 12
        -- true for essentially any real dataset spanning more than half a
        month. A column where every single date is ambiguous (e.g. only
        the first twelve days of a month) may be parsed as month-first
        instead.
    """
    # Deliberately not passing dayfirst=True here: pandas already infers
    # day-first vs. month-first correctly on its own as soon as any value
    # in the column has a day >12 (which real multi-day datasets almost
    # always do), for both slash-separated (dd/mm/yyyy) and ISO
    # (yyyy-mm-dd) dates. Forcing dayfirst=True instead actively corrupts
    # already-unambiguous ISO dates -- e.g. it turns "2018-01-07" into
    # July 1st instead of January 7th, because pandas infers one date
    # format from the first row and applies it to the whole column.
    parsed = pd.to_datetime(df[column], errors="coerce")
    if parsed.isna().all():
        raise ValueError(
            f"Column '{column}' has no usable date values. Expected a "
            "column of dates or date-like strings (e.g. '2018-01-07' or "
            "'07/01/2018')."
        )
    return parsed


def select_complete_rows(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Drop rows where any of columns has a missing value.

    Args:
        df: The DataFrame to filter.
        columns: The columns that must all be present (non-missing) in a
            row for that row to be kept.

    Returns:
        A copy of df containing only rows with usable values in every
        column listed in columns.

    Raises:
        ValueError: If no rows remain after dropping incomplete rows.
    """
    cleaned = df.dropna(subset=columns).copy()
    if cleaned.empty:
        raise ValueError(
            f"No usable (non-missing) rows remain across columns {columns}."
        )
    return cleaned
