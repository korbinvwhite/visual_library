import pandas as pd
import pytest

from carnaval_viz import validation


def test_require_dataframe_rejects_non_dataframe():
    with pytest.raises(TypeError):
        validation.require_dataframe([1, 2, 3])


def test_require_dataframe_rejects_empty_dataframe():
    with pytest.raises(ValueError):
        validation.require_dataframe(pd.DataFrame())


def test_require_dataframe_accepts_dataframe():
    validation.require_dataframe(pd.DataFrame({"a": [1]}))


def test_require_columns_exist_raises_for_missing_column():
    df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(KeyError):
        validation.require_columns_exist(df, ["a", "b"])


def test_require_columns_exist_accepts_present_columns():
    df = pd.DataFrame({"a": [1], "b": [2]})
    validation.require_columns_exist(df, ["a", "b"])


def test_require_numeric_columns_rejects_nonnumeric():
    df = pd.DataFrame({"a": ["x", "y"]})
    with pytest.raises(TypeError):
        validation.require_numeric_columns(df, ["a"])


def test_require_numeric_columns_accepts_numeric():
    df = pd.DataFrame({"a": [1, 2], "b": [3.0, 4.0]})
    validation.require_numeric_columns(df, ["a", "b"])


def test_coerce_datetime_column_parses_valid_dates():
    # Includes a day >12 ("13") so pandas can unambiguously infer a
    # day-first format for the whole column; see the note in
    # validation.coerce_datetime_column about why an all-ambiguous sample
    # (e.g. only "07/01/2018"-style rows) isn't reliably auto-detected.
    df = pd.DataFrame({"date": ["13/01/2018", "07/01/2018", "20/01/2018"]})
    parsed = validation.coerce_datetime_column(df, "date")
    assert parsed.notna().all()
    assert parsed.iloc[0] == pd.Timestamp("2018-01-13")


def test_coerce_datetime_column_parses_iso_dates():
    df = pd.DataFrame({"date": ["2018-01-07", "2018-01-13", "2018-01-20"]})
    parsed = validation.coerce_datetime_column(df, "date")
    assert parsed.notna().all()
    assert parsed.iloc[0] == pd.Timestamp("2018-01-07")


def test_coerce_datetime_column_rejects_all_unparseable():
    df = pd.DataFrame({"date": ["not a date", "also not a date"]})
    with pytest.raises(ValueError):
        validation.coerce_datetime_column(df, "date")


def test_select_complete_rows_drops_incomplete_rows():
    df = pd.DataFrame({"a": [1, None, 3], "b": [1, 2, None]})
    result = validation.select_complete_rows(df, ["a", "b"])
    assert list(result.index) == [0]


def test_select_complete_rows_raises_when_nothing_remains():
    df = pd.DataFrame({"a": [None, None], "b": [1, None]})
    with pytest.raises(ValueError):
        validation.select_complete_rows(df, ["a", "b"])
