import pandas as pd
import pytest

from carnaval_viz import validation


def test_require_dataframe_rejects_non_dataframe():
    with pytest.raises(TypeError):
        validation.require_dataframe([1, 2, 3])


def test_require_dataframe_accepts_dataframe():
    validation.require_dataframe(pd.DataFrame({"a": [1]}))


def test_require_column_exists_raises_for_missing_column():
    df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(KeyError):
        validation.require_column_exists(df, "b")


def test_require_numeric_column_rejects_nonnumeric():
    df = pd.DataFrame({"a": ["x", "y"]})
    with pytest.raises(TypeError):
        validation.require_numeric_column(df, "a")


def test_require_numeric_column_rejects_all_missing():
    df = pd.DataFrame({"a": [None, None]})
    with pytest.raises(ValueError):
        validation.require_numeric_column(df, "a")


def test_require_numeric_column_drops_missing_values():
    df = pd.DataFrame({"a": [1.0, None, 3.0]})
    result = validation.require_numeric_column(df, "a")
    assert list(result) == [1.0, 3.0]


def test_select_numeric_columns_requires_at_least_two():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    with pytest.raises(ValueError):
        validation.select_numeric_columns(df)


def test_select_numeric_columns_keeps_only_numeric():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": ["x", "y"]})
    result = validation.select_numeric_columns(df)
    assert list(result.columns) == ["a", "b"]


def test_require_supported_correlation_method_rejects_unknown():
    with pytest.raises(ValueError):
        validation.require_supported_correlation_method("not_a_method")


@pytest.mark.parametrize("method", ["pearson", "spearman", "kendall"])
def test_require_supported_correlation_method_accepts_known(method):
    validation.require_supported_correlation_method(method)
