import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest
from matplotlib.figure import Figure

import carnaval_viz as viz


@pytest.fixture
def blocos_df():
    rng = np.random.default_rng(seed=11)
    return pd.DataFrame(
        {
            "year_founded": rng.integers(1950, 2020, size=30),
            "estimated_audience": rng.integers(100, 100_000, size=30),
            "region": rng.choice(["Centro", "Zona Sul", "Zona Norte"], size=30),
        }
    )


def test_bubble_chart_returns_figure(blocos_df):
    fig = viz.bubble_chart(
        blocos_df, x="year_founded", y="estimated_audience",
        size="estimated_audience", color="region",
    )
    assert isinstance(fig, Figure)


def test_bubble_chart_handles_missing_values(blocos_df):
    df = blocos_df.copy()
    df.loc[0, "estimated_audience"] = None
    fig = viz.bubble_chart(
        df, x="year_founded", y="estimated_audience",
        size="estimated_audience", color="region",
    )
    assert isinstance(fig, Figure)


def test_bubble_chart_scales_bubble_sizes(blocos_df):
    fig = viz.bubble_chart(
        blocos_df, x="year_founded", y="estimated_audience",
        size="estimated_audience", color="region",
    )
    sizes = fig.axes[0].collections[0].get_sizes()
    assert sizes.min() != sizes.max()


def test_bubble_chart_rejects_non_dataframe():
    with pytest.raises(TypeError):
        viz.bubble_chart([1, 2, 3], x="a", y="b", size="c", color="d")


def test_bubble_chart_rejects_missing_column(blocos_df):
    with pytest.raises(KeyError):
        viz.bubble_chart(
            blocos_df, x="year_founded", y="estimated_audience",
            size="estimated_audience", color="not_a_column",
        )


def test_bubble_chart_annotate_top(blocos_df):
    fig = viz.bubble_chart(
        blocos_df, x="year_founded", y="estimated_audience",
        size="estimated_audience", color="region", annotate_top=3,
    )
    assert len(fig.axes[0].texts) == 3


def test_bubble_chart_does_not_modify_input(blocos_df):
    original = blocos_df.copy(deep=True)
    viz.bubble_chart(
        blocos_df, x="year_founded", y="estimated_audience",
        size="estimated_audience", color="region",
    )
    pd.testing.assert_frame_equal(blocos_df, original)
