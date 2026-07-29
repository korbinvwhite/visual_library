"""Clean the raw Rio Carnival Blocos dataset into a ready-to-use CSV.

The raw file (`Agenda_BL_Rua_Carnaval_Rio-2018_Imprensa.csv`) is a real 2018
Rio de Janeiro street-Carnival parade schedule. Its source/license is not
documented, so it is included here as-is for demonstration purposes only.
It has several real-world data-quality quirks this script fixes:

- It's semicolon-separated, not comma-separated (common in Brazilian data).
- Numbers use Brazilian formatting, where "." marks a thousands group
  (e.g. "1.500" means one thousand five hundred, and "1.984" in the
  founding-year column means the year 1984 -- not 1.984).
- The "Região" (region) column has inconsistent capitalization and
  whitespace across rows (e.g. "Zona Norte 1", "Zona norte 1", and
  "zona oeste" all refer to the same handful of real regions).
- Dates are day-first (dd/mm/yyyy).

Run with:
    python examples/prepare_dataset.py
"""

from pathlib import Path

import pandas as pd

RAW_PATH = Path(__file__).parent / "Agenda_BL_Rua_Carnaval_Rio-2018_Imprensa.csv"
CLEAN_PATH = Path(__file__).parent / "rio_carnival_blocos.csv"

COLUMN_RENAMES = {
    "Bloco ": "bloco_name",
    "Bairro": "neighborhood",
    "Região": "region",
    "Data": "event_date",
    "Data Relativa": "relative_date",
    "Concentração": "gathering_time",
    "Desfile": "parade_time",
    "Final": "end_time",
    "Local da Concentraçao": "gathering_location",
    "Percurso": "route",
    "Público Estimado": "estimated_audience",
    "Ano do primeiro desfile": "year_founded",
}


def _brazilian_number_to_int(series: pd.Series) -> pd.Series:
    """Convert Brazilian-formatted number strings (e.g. "1.500") to int."""
    return series.str.replace(".", "", regex=False).astype(int)


def prepare_dataframe() -> pd.DataFrame:
    """Load and clean the raw Rio Carnival Blocos dataset.

    Returns:
        A cleaned pandas DataFrame with English column names, proper
        numeric types, parsed dates, and normalized region names.
    """
    # dtype=str forces every column to be read as plain text. Without it,
    # pandas silently infers "year_founded" as a float column (since every
    # value looks numeric), which corrupts values like "1972" into "1972.0"
    # -- and then into "19720" once the thousands-separator "." is stripped.
    # Reading everything as text and converting explicitly avoids that.
    df = pd.read_csv(RAW_PATH, sep=";", encoding="utf-8-sig", dtype=str)
    # The raw file has a trailing ";" on every row, which pandas reads as an
    # extra unnamed, all-empty column.
    df = df.drop(columns=[col for col in df.columns if col.startswith("Unnamed")])
    df = df.rename(columns=COLUMN_RENAMES)

    df["estimated_audience"] = _brazilian_number_to_int(df["estimated_audience"])
    df["year_founded"] = _brazilian_number_to_int(df["year_founded"])
    df["event_date"] = pd.to_datetime(df["event_date"], dayfirst=True)
    df["region"] = df["region"].str.strip().str.title()

    return df


if __name__ == "__main__":
    prepare_dataframe().to_csv(CLEAN_PATH, index=False)
    print(f"Wrote {CLEAN_PATH}")
