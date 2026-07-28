"""Generate the synthetic Brazilian-music example dataset used by carnaval_viz.

This dataset is SYNTHETIC. It does not come from a real streaming service or
API. Values are randomly generated (with a fixed seed for reproducibility)
using ranges typical of real audio-feature datasets (e.g. danceability and
energy between 0 and 1, tempo in beats per minute, etc.), so the example
charts look realistic without requiring any external data source, API key,
or license review.

Run this script directly to (re)generate examples/brazilian_music_sample.csv:
    python examples/generate_dataset.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

GENRES = ["samba", "bossa nova", "funk carioca", "MPB", "forro", "axe"]
ARTISTS = [f"Artist {letter}" for letter in "ABCDEFGHIJ"]


def generate_sample_dataframe(n_rows: int = 200, seed: int = 2026) -> pd.DataFrame:
    """Build a synthetic table of Brazilian-music-style audio features.

    Args:
        n_rows: Number of synthetic songs to generate.
        seed: Random seed, fixed by default so the output is reproducible.

    Returns:
        A pandas DataFrame with numeric audio-feature columns and a few
        categorical columns (artist, genre, release_year).
    """
    rng = np.random.default_rng(seed)

    energy = rng.uniform(0.2, 1.0, n_rows)
    # Danceability correlates loosely with energy, with noise added, to give
    # the example correlation heatmap something interesting to show.
    danceability = np.clip(energy * 0.6 + rng.uniform(0, 0.4, n_rows), 0, 1)
    valence = np.clip(energy * 0.4 + rng.uniform(0, 0.6, n_rows), 0, 1)

    df = pd.DataFrame(
        {
            "artist": rng.choice(ARTISTS, n_rows),
            "genre": rng.choice(GENRES, n_rows),
            "release_year": rng.integers(1998, 2025, n_rows),
            "danceability": danceability,
            "energy": energy,
            "valence": valence,
            "tempo": rng.uniform(70, 160, n_rows),
            "loudness": rng.uniform(-18, -3, n_rows),
            "acousticness": rng.uniform(0, 1, n_rows),
            "instrumentalness": rng.uniform(0, 0.3, n_rows),
            "speechiness": rng.uniform(0.02, 0.4, n_rows),
            "liveness": rng.uniform(0.02, 0.5, n_rows),
            "popularity": rng.integers(20, 100, n_rows),
            "duration_ms": rng.integers(150_000, 300_000, n_rows),
        }
    )
    return df


if __name__ == "__main__":
    output_path = Path(__file__).parent / "brazilian_music_sample.csv"
    generate_sample_dataframe().to_csv(output_path, index=False)
    print(f"Wrote {output_path}")
