import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest
from matplotlib.figure import Figure

import carnaval_viz as viz


@pytest.fixture
def music_df():
    rng = np.random.default_rng(seed=7)
    return pd.DataFrame(
        {
            "danceability": rng.uniform(0, 1, size=50),
            "energy": rng.uniform(0, 1, size=50),
            "tempo": rng.uniform(60, 180, size=50),
            "genre": rng.choice(["samba", "bossa nova", "funk"], size=50),
        }
    )


def test_correlation_returns_figure(music_df):
    fig = viz.correlation(music_df)
    assert isinstance(fig, Figure)


def test_correlation_only_uses_numeric_columns(music_df):
    fig = viz.correlation(music_df)
    ax = fig.axes[0]
    assert list(ax.get_xticklabels()[i].get_text() for i in range(3)) == [
        "danceability",
        "energy",
        "tempo",
    ]


def test_correlation_handles_missing_values():
    df = pd.DataFrame(
        {
            "a": [1.0, 2.0, None, 4.0],
            "b": [4.0, None, 2.0, 1.0],
        }
    )
    fig = viz.correlation(df)
    assert isinstance(fig, Figure)


@pytest.mark.parametrize("method", ["pearson", "spearman", "kendall"])
def test_correlation_supports_all_methods(music_df, method):
    fig = viz.correlation(music_df, method=method)
    assert isinstance(fig, Figure)


def test_correlation_rejects_unsupported_method(music_df):
    with pytest.raises(ValueError):
        viz.correlation(music_df, method="not_a_method")


def test_correlation_rejects_fewer_than_two_numeric_columns():
    df = pd.DataFrame({"a": [1, 2, 3], "genre": ["x", "y", "z"]})
    with pytest.raises(ValueError):
        viz.correlation(df)


def test_correlation_annotation_toggle(music_df):
    fig_annotated = viz.correlation(music_df, annotate=True)
    fig_plain = viz.correlation(music_df, annotate=False)

    ax_annotated = fig_annotated.axes[0]
    ax_plain = fig_plain.axes[0]

    assert len(ax_annotated.texts) > 0
    assert len(ax_plain.texts) == 0


def test_correlation_does_not_modify_input(music_df):
    original = music_df.copy(deep=True)
    viz.correlation(music_df)
    pd.testing.assert_frame_equal(music_df, original)
