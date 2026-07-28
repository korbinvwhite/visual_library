import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest
from matplotlib.figure import Figure

import carnaval_viz as viz


@pytest.fixture
def music_df():
    rng = np.random.default_rng(seed=42)
    return pd.DataFrame({"danceability": rng.uniform(0, 1, size=50)})


def test_histogram_returns_figure(music_df):
    fig = viz.histogram(music_df, "danceability")
    assert isinstance(fig, Figure)


def test_histogram_handles_missing_values():
    df = pd.DataFrame({"danceability": [0.5, None, 0.7, None, 0.9]})
    fig = viz.histogram(df, "danceability")
    assert isinstance(fig, Figure)


def test_histogram_rejects_non_dataframe():
    with pytest.raises(TypeError):
        viz.histogram([1, 2, 3], "danceability")


def test_histogram_rejects_missing_column(music_df):
    with pytest.raises(KeyError):
        viz.histogram(music_df, "not_a_column")


def test_histogram_rejects_nonnumeric_column():
    df = pd.DataFrame({"genre": ["samba", "bossa nova", "funk"]})
    with pytest.raises(TypeError):
        viz.histogram(df, "genre")


def test_histogram_rejects_all_missing_column():
    df = pd.DataFrame({"danceability": [None, None, None]})
    with pytest.raises(ValueError):
        viz.histogram(df, "danceability")


def test_histogram_mean_and_median_lines_toggle(music_df):
    fig_both = viz.histogram(music_df, "danceability", show_mean=True, show_median=True)
    fig_neither = viz.histogram(music_df, "danceability", show_mean=False, show_median=False)

    ax_both = fig_both.axes[0]
    ax_neither = fig_neither.axes[0]

    assert ax_both.get_legend() is not None
    assert ax_neither.get_legend() is None


def test_histogram_does_not_modify_input(music_df):
    original = music_df.copy(deep=True)
    viz.histogram(music_df, "danceability")
    pd.testing.assert_frame_equal(music_df, original)
