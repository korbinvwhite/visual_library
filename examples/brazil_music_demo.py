"""Demo script for carnaval_viz using the synthetic Brazilian-music dataset.

Run with:
    python examples/brazil_music_demo.py

This regenerates the two example images stored in assets/ and shown in the
README: a histogram of the "danceability" feature, and a correlation
heatmap across all numeric audio features.
"""

from pathlib import Path

import carnaval_viz as viz
from generate_dataset import generate_sample_dataframe

ASSETS_DIR = Path(__file__).parent.parent / "assets"


def main() -> None:
    df = generate_sample_dataframe()

    hist_fig = viz.histogram(df, "danceability")
    hist_fig.savefig(
        ASSETS_DIR / "histogram_example.png", dpi=300, bbox_inches="tight"
    )

    corr_fig = viz.correlation(df)
    corr_fig.savefig(
        ASSETS_DIR / "correlation_example.png", dpi=300, bbox_inches="tight"
    )

    print(f"Saved example images to {ASSETS_DIR}")


if __name__ == "__main__":
    main()
