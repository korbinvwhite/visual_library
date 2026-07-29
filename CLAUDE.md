PYTHON VISUALIZATION LIBRARY SPECIFICATION

PROJECT OBJECTIVE

Build a lightweight Python visualization library that transforms event-based datasets into visually engaging, publication-quality graphics. The library should focus on storytelling and beautiful visualizations rather than generic statistical charts.

The finished project should resemble a polished open-source package that could realistically be published to PyPI.

The priorities are:

- Simple installation
- Small, intuitive API
- Beautiful default visualizations
- Consistent styling
- Clear documentation
- Proper package structure
- Input validation
- Reusable code
- Beginner-friendly usage

------------------------------------------------------------

PROJECT THEME

The library should be inspired by the energy and color of Rio de Janeiro's Carnival.

The visual identity should reflect:

- Carnival
- Samba
- Street blocos
- Tropical colors
- Brazilian graphic design
- Celebration and movement

Do not use clip art, flags, costumes, or decorative graphics.

The charts should remain professional and presentation-ready.

------------------------------------------------------------

PACKAGE NAME

Use:

carnaval_viz

Import:

import carnaval_viz as viz

------------------------------------------------------------

TECHNOLOGY

Use:

- Python
- pandas
- matplotlib
- numpy (only if needed)

Do not use:

- Plotly
- Dash
- Streamlit
- Flask
- Django

Minimum Python version:

Python 3.10

------------------------------------------------------------

PUBLIC API

Version 0.1.0 exposes exactly two public functions:

viz.bubble_chart()

viz.circular_calendar()

------------------------------------------------------------

VISUALIZATION 1

Bubble Chart

Function:

bubble_chart(
    df,
    x,
    y,
    size,
    color,
    *,
    title=None,
    figsize=(10,8),
    alpha=0.7,
    annotate_top=0
)

Purpose

Create a publication-quality bubble chart.

Each row represents one Carnival bloco.

Default usage:

x = Year Founded

y = Estimated Audience

Bubble Size = Estimated Audience

Bubble Color = Region

Requirements

- Validate DataFrame
- Validate all required columns
- Ignore missing values
- Scale bubble sizes automatically
- Apply transparency
- Add legend
- Use Brazil-inspired color palette
- Clean typography
- Remove unnecessary borders
- Light grid
- Optional annotation of largest events
- Return the Matplotlib Figure
- Never call plt.show()

------------------------------------------------------------

VISUALIZATION 2

Circular Calendar

Function:

circular_calendar(
    df,
    date,
    size,
    color,
    *,
    title=None,
    figsize=(10,10)
)

Purpose

Display Carnival events around a circular calendar.

The circular layout represents the Carnival season.

Each event becomes one point.

Visual Mapping

Angle

↓

Event Date

Radius

↓

Fixed

Bubble Size

↓

Estimated Audience

Bubble Color

↓

Region

Requirements

- Validate DataFrame
- Validate columns
- Convert dates automatically
- Convert dates into angular positions
- Scale bubbles automatically
- Brazil-inspired palette
- Region legend
- Month labels around the outside
- Radial grid
- Clean typography
- Return the Matplotlib Figure
- Never call plt.show()

------------------------------------------------------------

SHARED STYLE

Create a shared styling module.

Define:

- Color palette
- Fonts
- Grid style
- Bubble transparency
- Figure background
- Axis styling
- Legend styling
- Title styling

Suggested palette

- Emerald Green
- Tropical Green
- Ocean Blue
- Turquoise
- Gold
- Coral
- Warm Orange
- Light Cream
- Charcoal

Avoid rainbow colors and default Matplotlib styling.

------------------------------------------------------------

DATASET

Use the supplied Rio Carnival Blocos dataset.

Expected columns include:

- Bloco Name
- Estimated Audience
- Neighborhood
- Region
- Event Date
- Start Time
- End Time
- Year Founded

The dataset should be used throughout:

- README
- Example notebook
- Example script
- Screenshots

------------------------------------------------------------

PROJECT STRUCTURE

project-root/

src/
    carnaval_viz/
        __init__.py
        bubble_chart.py
        circular_calendar.py
        styling.py
        colors.py
        validation.py

tests/

examples/

assets/

README.md

pyproject.toml

LICENSE

CHANGELOG.md

------------------------------------------------------------

INPUT VALIDATION

Create reusable validation helpers.

Raise informative exceptions for:

- Invalid DataFrame
- Missing columns
- Invalid date column
- Invalid numeric columns
- Empty datasets
- Missing usable values

------------------------------------------------------------

RETURN VALUES

Both functions must return a Matplotlib Figure.

Example

fig = viz.bubble_chart(...)

fig.savefig("bubble_chart.png")

------------------------------------------------------------

CODE QUALITY

Use:

- Type hints
- Docstrings
- Clear parameter descriptions
- Return descriptions
- Usage examples

Do not modify the original DataFrame.

------------------------------------------------------------

TESTING

Use pytest.

Test Bubble Chart

- Creates Figure
- Handles missing values
- Bubble scaling
- Invalid inputs
- Missing columns
- Input DataFrame unchanged

Test Circular Calendar

- Creates Figure
- Correct date conversion
- Handles missing values
- Invalid dates
- Missing columns
- Input DataFrame unchanged

------------------------------------------------------------

PACKAGING

Create a valid pyproject.toml.

Version

0.1.0

Runtime dependencies

- pandas
- matplotlib
- numpy (if needed)

Development dependencies

- pytest
- build
- twine
- ruff

------------------------------------------------------------

README

Include

- Project description
- Installation
- Quick Start
- API
- Dataset description
- Example images
- Development instructions
- Testing
- Build instructions
- License

Example

import pandas as pd
import carnaval_viz as viz

df = pd.read_csv("rio_carnival.csv")

viz.bubble_chart(
    df,
    x="Year Founded",
    y="Estimated Audience",
    size="Estimated Audience",
    color="Region"
)

viz.circular_calendar(
    df,
    date="Event Date",
    size="Estimated Audience",
    color="Region"
)

------------------------------------------------------------

EXAMPLE OUTPUTS

Generate two screenshots.

1.

Bubble Chart

Year Founded vs Estimated Audience

Bubble Size = Audience

Color = Region

2.

Circular Calendar

Every Carnival event plotted around a circular calendar

Bubble Size = Audience

Color = Region

------------------------------------------------------------

LICENSE

MIT License

------------------------------------------------------------

OUT OF SCOPE

Do not build

- Dashboard
- Web application
- CLI
- AI features
- Interactive web graphics
- Plotly support
- Additional chart types

------------------------------------------------------------

FUTURE FEATURES

Potential future additions

- Timeline View
- Festival Heatmap
- Route Map
- Neighborhood Density Map
- Daily Attendance Timeline
- Event Network Graph
- Geographic Scatter Map
- Animated Carnival Progression
- Bloco Popularity Rankings

------------------------------------------------------------

DEFINITION OF DONE

The project is complete when:

- Package installs successfully
- Both public functions work
- Bubble Chart generates correctly
- Circular Calendar generates correctly
- Shared styling is implemented
- Validation is complete
- Tests pass
- README is complete
- Screenshots are generated
- Package builds successfully
- No publishing occurs without permission

------------------------------------------------------------

FINAL DELIVERABLES

Provide:

- Complete project directory
- All Python source files
- Tests
- README
- pyproject.toml
- LICENSE
- CHANGELOG
- Example notebook
- Example script
- Bubble Chart screenshot
- Circular Calendar screenshot
- Installation instructions
- Build instructions
- Test instructions