"""Demo script for carnaval_viz using the Rio Carnival Blocos dataset.

Run with:
    python examples/rio_carnival_demo.py

This regenerates the two example images stored in assets/ and shown in the
README -- a bubble chart of blocos by founding year and audience size, and
a Carnival calendar of every event across the season -- and then displays
both charts in windows that stay open until you close them.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import carnaval_viz as viz
from prepare_dataset import CLEAN_PATH, prepare_dataframe

ASSETS_DIR = Path(__file__).parent.parent / "assets"


def main() -> None:
    if not CLEAN_PATH.exists():
        prepare_dataframe().to_csv(CLEAN_PATH, index=False)
    df = pd.read_csv(CLEAN_PATH)

    # Both functions default to this dataset's column names (year_founded,
    # estimated_audience, region, event_date, gathering_time), so no column
    # arguments are needed for the common case.
    bubble_fig = viz.bubble_chart(df)
    bubble_fig.savefig(
        ASSETS_DIR / "bubble_chart_example.png", dpi=300, bbox_inches="tight"
    )

    calendar_fig = viz.carnival_calendar(df)
    calendar_fig.savefig(
        ASSETS_DIR / "carnival_calendar_example.png", dpi=300, bbox_inches="tight"
    )

    print(f"Saved example images to {ASSETS_DIR}")

    plt.show()  # keeps both windows open until you close them


if __name__ == "__main__":
    main()
