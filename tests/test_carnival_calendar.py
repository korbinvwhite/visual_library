import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest
from matplotlib.figure import Figure

import carnaval_viz as viz


@pytest.fixture
def blocos_df():
    rng = np.random.default_rng(seed=13)
    dates = pd.date_range("2018-01-01", "2018-02-28", periods=30)
    return pd.DataFrame(
        {
            "event_date": dates.strftime("%d/%m/%Y"),
            "gathering_time": rng.choice(["14:00:00", "16:00:00", "18:00:00"], size=30),
            "estimated_audience": rng.integers(100, 100_000, size=30),
            "region": rng.choice(["Centro", "Zona Sul", "Zona Norte"], size=30),
        }
    )


def test_carnival_calendar_returns_figure(blocos_df):
    fig = viz.carnival_calendar(
        blocos_df, date="event_date", time="gathering_time",
        size="estimated_audience", color="region",
    )
    assert isinstance(fig, Figure)


def test_carnival_calendar_converts_dates_to_angles(blocos_df):
    fig = viz.carnival_calendar(
        blocos_df, date="event_date", time="gathering_time",
        size="estimated_audience", color="region",
    )
    offsets = fig.axes[0].collections[0].get_offsets()
    angles = offsets[:, 0]
    assert (angles >= 0).all() and (angles <= 2 * np.pi).all()


def test_carnival_calendar_varies_radius_by_time(blocos_df):
    fig = viz.carnival_calendar(
        blocos_df, date="event_date", time="gathering_time",
        size="estimated_audience", color="region",
    )
    offsets = fig.axes[0].collections[0].get_offsets()
    radii = offsets[:, 1]
    assert radii.min() != radii.max()


def test_carnival_calendar_handles_missing_values(blocos_df):
    df = blocos_df.copy()
    df.loc[0, "estimated_audience"] = None
    fig = viz.carnival_calendar(
        df, date="event_date", time="gathering_time",
        size="estimated_audience", color="region",
    )
    assert isinstance(fig, Figure)


def test_carnival_calendar_rejects_invalid_dates(blocos_df):
    df = blocos_df.copy()
    df["event_date"] = "not a real date"
    with pytest.raises(ValueError):
        viz.carnival_calendar(
            df, date="event_date", time="gathering_time",
            size="estimated_audience", color="region",
        )


def test_carnival_calendar_rejects_missing_column(blocos_df):
    with pytest.raises(KeyError):
        viz.carnival_calendar(
            blocos_df, date="not_a_column", time="gathering_time",
            size="estimated_audience", color="region",
        )


def test_carnival_calendar_does_not_modify_input(blocos_df):
    original = blocos_df.copy(deep=True)
    viz.carnival_calendar(
        blocos_df, date="event_date", time="gathering_time",
        size="estimated_audience", color="region",
    )
    pd.testing.assert_frame_equal(blocos_df, original)
