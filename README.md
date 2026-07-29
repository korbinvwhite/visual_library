# carnaval_viz

A lightweight, Rio Carnival-inspired Python visualization library. It creates two polished, presentation-ready charts — a bubble chart and a Carnival calendar — with minimal configuration, built on top of pandas and Matplotlib.

<p align="center">
  <img src="assets/bubble_chart_example.png" width="48%" alt="Example bubble chart" />
  <img src="assets/carnival_calendar_example.png" width="48%" alt="Example Carnival calendar" />
</p>

## Installation

```bash
pip install -e .
```

(This project is not yet published to PyPI — see [Development](#development) below to install it locally in "editable" mode, meaning changes to the source code take effect immediately without reinstalling.)

## Quick start

```python
import matplotlib.pyplot as plt
import pandas as pd
import carnaval_viz as viz

df = pd.read_csv("examples/rio_carnival_blocos.csv")

# Both functions default to this dataset's column names, so no column
# arguments are needed for the common case.
bubble_fig = viz.bubble_chart(df)
calendar_fig = viz.carnival_calendar(df)

plt.show()  # keeps both windows open until you close them
```

Both functions return a Matplotlib `Figure` (rather than displaying anything automatically), so you can save them:

```python
bubble_fig.savefig("bubble_chart.png", dpi=300, bbox_inches="tight")
calendar_fig.savefig("carnival_calendar.png", dpi=300, bbox_inches="tight")
```

## API

### `viz.bubble_chart(df, x="year_founded", y="estimated_audience", size="estimated_audience", color="region", *, title=None, figsize=(10, 8), alpha=0.7, annotate_top=3, yscale="log")`

Plots one bubble per row: `x`/`y` position, bubble size from `size` (square-root scaled by default, so one extreme outlier doesn't crush every other bubble to invisible), and color from the category in `color` (legend ordered by total `size`, largest first). The y-axis defaults to a log scale (`yscale="log"`) so values aren't crushed near zero by a large outlier — pass `yscale="linear"` if your y-column can be zero or negative. Missing values are dropped automatically. `annotate_top` labels the N largest bubbles (by `size`) with their DataFrame index — pass `0` to disable. Raises `TypeError`/`KeyError`/`ValueError` with a clear message for invalid input (not a DataFrame, missing/non-numeric/negative columns, empty dataset, or no usable rows).

### `viz.carnival_calendar(df, date="event_date", time="gathering_time", size="estimated_audience", color="region", *, title=None, figsize=(10, 10))`

Plots one point per row around a calendar wheel scoped to the season the data actually spans (not a full, mostly-empty year): angular position from `date`, radius from `time` (event clock time — earlier events sit closer to the center), point size from `size`, and color from the category in `color`. Tick labels count down in weeks to the final event date (e.g. "3 Weeks Before", "Event Day").

Both functions' default column names match `examples/rio_carnival_blocos.csv`. Pass your own column names as keyword arguments (e.g. `viz.bubble_chart(df, x="my_column")`) to use a different dataset.

## Dataset

The example dataset (`examples/rio_carnival_blocos.csv`) is a real 2018 Rio de Janeiro street-Carnival ("bloco") parade schedule, cleaned from the raw file `examples/Agenda_BL_Rua_Carnaval_Rio-2018_Imprensa.csv` by `examples/prepare_dataset.py`. That script fixes several real-world data-quality quirks: semicolon-separated fields, Brazilian-style thousands separators in numbers (e.g. `"1.500"` means 1,500, not 1.5), and inconsistent capitalization in the region column.

**This dataset's original source/license is not documented.** It's included here for demonstration purposes only — if you plan to redistribute this project, verify (or replace) the dataset's licensing first.

## Development

Clone the repository, then install it in editable mode along with development tools (testing, building, and linting utilities):

```bash
python -m pip install -e ".[dev]"
```

### Testing

```bash
python -m pytest
```

### Regenerating the cleaned dataset and example images

```bash
python examples/prepare_dataset.py
python examples/rio_carnival_demo.py
```

### Building the package

```bash
python -m build
python -m twine check dist/*
```

This produces a wheel (`.whl`, a pre-built package format) and a source distribution (`.tar.gz`) in `dist/`, and `twine check` verifies they're valid for publishing (no actual publishing happens as part of this).

## License

The **software** is released under the [MIT License](LICENSE). The **example dataset**'s license is undocumented (see [Dataset](#dataset) above) — treat it as demonstration-only.
