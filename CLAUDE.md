# PYTHON VISUALIZATION LIBRARY SPECIFICATION

## PROJECT OBJECTIVE

Build a lightweight Python visualization library that users can install with pip and import into a Jupyter notebook or Python project.

This is not an exploratory data analysis library that prints statistics, summaries, or dictionaries. Its main purpose is to create two polished, reusable data visualizations with minimal configuration.

The finished project should resemble a small, professional open-source package that could realistically be published to PyPI.

The priorities are:

- Simple installation
- A small and understandable public API
- Beautiful default visualizations
- Consistent styling
- Clear documentation
- Proper package structure
- Input validation
- Reusable code
- Beginner-friendly usage


## PROJECT THEME

Give the library a visual identity inspired by the positive, celebratory elements of Brazil, including:

- Carnival
- Samba
- Brazilian music
- Dance
- Tropical landscapes
- Rio de Janeiro
- Energy and movement
- Modern Brazilian graphic design

The inspiration should appear primarily through the color palette, styling, naming, and sample dataset.

Do not add flags, costumes, people, cultural caricatures, or decorative illustrations directly to the charts.

The charts must remain clean and professional enough to use in presentations, reports, portfolios, and notebooks.


## SUGGESTED PACKAGE NAME

Use the placeholder package name:

`carnaval_viz`

Before publishing, verify that the selected package name is available on PyPI.

The import should work as follows:

```python
import carnaval_viz as viz
```


## TECHNOLOGY REQUIREMENTS

Use:

- Python
- pandas
- matplotlib
- numpy, only when needed for numerical operations

Do not use:

- Plotly
- Dash
- Streamlit
- Flask
- Django
- Web frameworks
- Interactive dashboards
- HTML report generators

Keep the dependency list small.

The minimum supported Python version should be Python 3.10 or newer.


## PUBLIC API

Expose exactly two primary visualization functions in version 0.1.0:

1. `histogram()`
2. `correlation()`

Users should be able to access both functions directly from the top-level package:

```python
import carnaval_viz as viz

fig = viz.histogram(df, "danceability")
fig = viz.correlation(df)
```

Do not require users to import functions from internal modules.


## VISUALIZATION 1: HISTOGRAM

### FUNCTION SIGNATURE

```python
histogram(
    df,
    column,
    *,
    bins="auto",
    title=None,
    xlabel=None,
    show_mean=True,
    show_median=True,
    figsize=(10, 6)
)
```

### PURPOSE

Create a polished histogram for one numeric DataFrame column.

### REQUIRED INPUTS

- df: pandas DataFrame
- column: name of a numeric column

### OPTIONAL INPUTS

- bins: histogram bin specification; default should be "auto"
- title: custom chart title
- xlabel: custom x-axis label
- show_mean: whether to display the mean reference line
- show_median: whether to display the median reference line
- figsize: Matplotlib figure size

### BEHAVIOR

- Confirm that df is a pandas DataFrame.
- Confirm that column exists.
- Confirm that column is numeric.
- Ignore missing values when plotting.
- Raise an informative error when no usable numeric values remain.
- Calculate an appropriate bin count automatically when bins="auto".
- Create one histogram.
- Display a mean reference line when show_mean=True.
- Display a median reference line when show_median=True.
- Clearly label the mean and median values.
- Include a legend only when at least one reference line is visible.
- Use a subtle horizontal grid.
- Remove unnecessary top and right plot borders.
- Use clean spacing and readable typography.
- Generate a sensible default title when title is not supplied.
- Use the column name as the default x-axis label.
- Label the y-axis as "Count."
- Do not modify the original DataFrame.
- Do not print results.
- Do not call plt.show() inside the function.
- Return the Matplotlib Figure object.

### VISUAL DESIGN

Use a rich, saturated, Brazil-inspired palette.

The primary histogram color may be an emerald or tropical green.

Use contrasting colors for the reference lines, such as:

- Mean: warm yellow or gold
- Median: ocean blue

Avoid neon colors and excessive decoration.

The final result should look significantly more polished than a default Matplotlib histogram.


## VISUALIZATION 2: CORRELATION HEATMAP

### FUNCTION SIGNATURE

```python
correlation(
    df,
    *,
    method="pearson",
    annotate=True,
    title=None,
    figsize=None
)
```

### PURPOSE

Create a polished correlation heatmap for all usable numeric columns in a DataFrame.

### REQUIRED INPUT

- df: pandas DataFrame

### OPTIONAL INPUTS

- method: correlation method; support "pearson", "spearman", and "kendall"
- annotate: whether to display correlation values
- title: custom chart title
- figsize: optional Matplotlib figure size

### BEHAVIOR

- Confirm that df is a pandas DataFrame.
- Select numeric columns automatically.
- Require at least two usable numeric columns.
- Ignore columns that contain no usable numeric data.
- Calculate the correlation matrix using the requested method.
- Raise an informative error for unsupported correlation methods.
- Display correlation values rounded to two decimal places when annotate=True.
- Use a diverging color map centered at zero.
- Keep the scale fixed from -1 to 1.
- Include a labeled color bar.
- Label the color bar "Correlation."
- Make column labels easy to read.
- Rotate labels only as much as necessary.
- Automatically adjust the figure size based on the number of numeric columns when figsize is not provided.
- Use a sensible default title when title is not supplied.
- Use a square or nearly square matrix layout.
- Avoid unnecessary chart borders and visual clutter.
- Do not modify the original DataFrame.
- Do not print results.
- Do not call plt.show() inside the function.
- Return the Matplotlib Figure object.

### VISUAL DESIGN

Use a custom Brazil-inspired diverging color map.

Suggested conceptual direction:

- Negative correlations: ocean blue
- Neutral correlations: light cream or warm neutral
- Positive correlations: tropical green

Use yellow or gold sparingly for highlights, titles, or accents rather than as the central neutral color.

Ensure that annotation text remains readable on both light and dark cells.

The heatmap should be presentation-ready without requiring additional styling.


## SHARED VISUAL STYLE

Create a shared styling module so both visualizations have a consistent identity.

The shared style should define:

- Color palette
- Figure background
- Axes background
- Font sizes
- Title styling
- Axis-label styling
- Grid appearance
- Border behavior
- Default spacing
- Reference-line styles
- Correlation color map

Suggested palette:

- Emerald green
- Tropical green
- Warm yellow or gold
- Ocean blue
- Turquoise
- Coral
- Warm orange
- Light cream
- Dark charcoal

Use the palette carefully. Do not place every color in every chart.

Favor strong contrast, accessibility, and readability.

Use fonts that ship with Matplotlib or are normally available in Python environments. Do not require users to download a custom font.

Do not permanently change global Matplotlib settings when the package is imported.

Use a local plotting context or apply styling only to the figures created by the package.


## DATASET

Use a Brazil-related dataset for examples and documentation.

### PREFERRED DATASET

Use a dataset of Brazilian music or Brazilian songs containing numeric audio features such as:

- danceability
- energy
- tempo
- loudness
- acousticness
- instrumentalness
- speechiness
- liveness
- valence
- popularity
- duration_ms

Categorical fields may include:

- artist
- song title
- genre
- release year

The dataset should contain enough numeric features to produce an informative correlation heatmap.

The histogram example should use a column such as:

- danceability
- energy
- tempo
- popularity

The dataset must be legally reusable.

Document its original source, license, creator, and any transformations performed.

Do not commit a dataset to the repository unless its license permits redistribution.

When redistribution is not permitted, include a documented script or notebook that downloads or prepares the data from its original source.

Do not rely on a private API key for the basic example.

If a suitable Brazilian music dataset cannot be found with clear reuse terms, use a reputable public Brazil-related dataset such as:

- Brazilian Olist e-commerce data
- Brazilian city statistics
- Brazilian football statistics
- Brazilian coffee production data

For the Olist dataset, useful numeric columns may include:

- payment_value
- freight_value
- price
- review_score
- delivery time
- number of installments


## PROJECT STRUCTURE

Use a modern src layout:

```
project-root/
├── src/
│   └── carnaval_viz/
│       ├── __init__.py
│       ├── histogram.py
│       ├── correlation.py
│       ├── colors.py
│       ├── styling.py
│       └── validation.py
├── tests/
│   ├── test_histogram.py
│   ├── test_correlation.py
│   └── test_validation.py
├── examples/
│   ├── brazil_music_demo.py
│   └── brazil_music_demo.ipynb
├── assets/
│   ├── histogram_example.png
│   └── correlation_example.png
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
└── CHANGELOG.md
```


## TOP-LEVEL PACKAGE EXPORTS

Configure `__init__.py` so that these imports work:

```python
import carnaval_viz as viz

viz.histogram(...)
viz.correlation(...)
```

Define `__all__` appropriately.

Do not expose internal helpers as part of the primary public API.


## INPUT VALIDATION

Create reusable validation helpers.

Validation must produce clear, actionable exceptions.

Examples:

- TypeError when df is not a pandas DataFrame
- KeyError or ValueError when a requested column does not exist
- TypeError or ValueError when the histogram column is not numeric
- ValueError when a numeric column contains no usable values
- ValueError when fewer than two usable numeric columns exist for the correlation heatmap
- ValueError when the correlation method is unsupported

Error messages should explain what went wrong and how the user can fix it.


## RETURN VALUES

Both public functions must return a Matplotlib Figure.

Example:

```python
fig = viz.histogram(df, "danceability")
fig.savefig("danceability.png", dpi=300, bbox_inches="tight")
```

The functions should not call plt.show() automatically.

This allows the library to work in notebooks, scripts, tests, and automated report-generation workflows.


## CODE QUALITY

All public functions must include:

- Type hints
- Clear docstrings
- Parameter descriptions
- Return-value descriptions
- Documented exceptions
- A short usage example

Follow standard Python formatting and naming conventions.

Keep functions focused.

Do not create one large function that handles multiple unrelated chart types.

Avoid duplicated style or validation code.

Do not modify input DataFrames.

Do not suppress errors silently.

Do not include unnecessary abstraction or complex class hierarchies.


## TESTING REQUIREMENTS

Use pytest.

Test the following histogram behavior:

- A valid numeric column creates a Figure.
- Missing values do not cause failure.
- An invalid DataFrame input raises an informative error.
- A missing column raises an informative error.
- A nonnumeric column raises an informative error.
- An all-missing numeric column raises an informative error.
- Mean and median lines can be enabled or disabled.
- The input DataFrame remains unchanged.

Test the following correlation behavior:

- A valid DataFrame creates a Figure.
- Only numeric columns are included.
- Missing values are handled.
- Pearson correlation works.
- Spearman correlation works.
- Kendall correlation works.
- An unsupported method raises an informative error.
- Fewer than two usable numeric columns raises an informative error.
- Annotation can be enabled or disabled.
- The input DataFrame remains unchanged.

Configure tests to run without opening graphical windows by using a noninteractive Matplotlib backend.


## PACKAGING

Create a valid pyproject.toml.

Include:

- Build-system configuration
- Package name
- Version
- Description
- Python version requirement
- Dependencies
- Author placeholder
- License information
- README reference
- Project classifiers
- Optional development dependencies
- Package-discovery configuration for the src layout

Initial version:

`0.1.0`

Runtime dependencies should remain minimal.

Suggested runtime dependencies:

- pandas
- matplotlib
- numpy, only if required

Suggested development dependencies:

- pytest
- build
- twine
- ruff or another lightweight linting tool


## README REQUIREMENTS

The README must include:

1. Project name
2. One-paragraph description
3. Example images of both visualizations
4. Installation instructions
5. Quick-start example
6. API documentation
7. Dataset source and license
8. Development instructions
9. Testing instructions
10. Build instructions
11. License information

### QUICK-START EXAMPLE

```python
import pandas as pd
import carnaval_viz as viz

df = pd.read_csv("brazilian_music.csv")

hist_fig = viz.histogram(df, "danceability")
hist_fig.show()

corr_fig = viz.correlation(df)
corr_fig.show()
```

Also demonstrate saving figures:

```python
hist_fig.savefig(
    "danceability_histogram.png",
    dpi=300,
    bbox_inches="tight"
)

corr_fig.savefig(
    "music_correlation.png",
    dpi=300,
    bbox_inches="tight"
)
```


## EXAMPLE OUTPUTS

Generate and save two example images:

1. A histogram using a Brazilian music feature such as danceability
2. A correlation heatmap using the numeric Brazilian music features

Store the images in the assets directory and display them in the README.

The screenshots should be generated by the actual package functions, not manually recreated.


## LOCAL DEVELOPMENT

The package must support editable installation:

```
python -m pip install -e .
```

The following must work after installation:

```python
import carnaval_viz as viz

print(viz.__all__)
```

The result should include:

```
histogram
correlation
```


## BUILD AND VALIDATION

The project must successfully run:

```
python -m pytest
python -m build
python -m twine check dist/*
```

The build should produce:

- A wheel file
- A source distribution

Do not publish to TestPyPI or PyPI unless explicitly instructed to do so.

Do not require API tokens or credentials to build or test the project.


## LICENSE

Use a standard open-source license, preferably MIT, unless another license is required.

Use the official license text.

Do not invent custom license wording.

Make sure the dataset license is handled separately from the software license.


## GITIGNORE

Include common generated files and directories:

- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`
- `.venv/`
- `venv/`
- `dist/`
- `build/`
- `*.egg-info/`
- `.ipynb_checkpoints/`
- generated temporary files

Do not commit authentication tokens, passwords, secrets, or environment files containing credentials.


## OUT OF SCOPE FOR VERSION 0.1.0

Do not build:

- A dashboard
- A web application
- An HTML report
- A command-line interface
- A custom plotting backend
- A plugin system
- Machine-learning analysis
- AI-generated chart commentary
- Automatic storytelling
- Support for Polars, Spark, Dask, or Arrow
- More than the two required public visualizations
- Complex themes or theme switching
- User authentication
- Data downloading that requires private credentials


## POSSIBLE FUTURE FEATURES

Do not implement these in version 0.1.0.

Possible later additions include:

- scatter()
- boxplot()
- violin()
- categorical_bar()
- missing_heatmap()
- density()
- time_series()
- pairplot()
- geographic map visualizations
- additional visual themes


## DEFINITION OF DONE

The task is complete only when:

- The package uses the required src layout.
- The package installs successfully in editable mode.
- The two visualization functions work through the top-level import.
- Both functions return Matplotlib Figure objects.
- Both functions validate their inputs.
- The original DataFrame is never modified.
- The plots share a consistent Brazil-inspired style.
- A legal, documented Brazil-related example dataset is used.
- Example images are generated from the actual functions.
- The README contains installation and usage documentation.
- Automated tests pass.
- The package builds into a wheel and source distribution.
- Twine validation passes.
- No publishing credentials are required.
- No PyPI upload occurs without explicit permission.


## FINAL DELIVERABLES

Provide:

- The complete project directory
- All Python source files
- pyproject.toml
- README.md
- LICENSE
- CHANGELOG.md
- Tests
- Example script
- Example notebook
- Two generated visualization images
- Dataset attribution and preparation instructions
- Commands for installation, testing, building, and validating the package

At the end, provide a concise completion report that lists:

- Files created
- Public functions implemented
- Dataset used
- Tests run and their results
- Build results
- Any assumptions or limitations
