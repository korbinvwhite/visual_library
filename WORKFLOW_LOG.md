# Workflow Log

This file is a running, plain-English diary of everything done in this project and why — kept up to date after every step so you can look back and follow the reasoning. It is NOT part of the `carnaval_viz` package itself; it's just for your own reference.

---

### 2026-07-28 — Project kickoff

- **What:** Took the full project specification for a new Python visualization library (`carnaval_viz`) and saved it into a file called `CLAUDE.md` at the root of the repo.
- **Why:** `CLAUDE.md` is a special file that Claude Code automatically reads for project context/instructions. Putting the spec there means any future session (or anyone else using Claude Code on this repo) automatically has the full requirements without you re-pasting them.

### 2026-07-28 — Workflow rules established

You set some ground rules for how we work together going forward:
1. **Work directly on `main`** — no more feature branches or pull requests (PRs). A PR is normally a way to propose changes on a separate branch for review before merging; skipping that is fine for a low-stakes/learning project, but worth knowing that's the tradeoff being made (no review step, no isolated branch history).
2. **Always confirm before committing or pushing.** A "commit" saves a snapshot of changes to the local project history; a "push" sends that snapshot up to GitHub (the remote/online copy). I'll describe what I'm about to save/send and wait for your go-ahead first.
3. **Explain technical terms in plain English** alongside the jargon, so this doubles as a learning resource.

### 2026-07-28 — Moved the spec onto `main`

- **What:** The CLAUDE.md file was originally created on a separate branch (`claude/python-viz-library-spec-68ut35`, a branch created automatically before the "stay on main" rule). Merged it into `main` and pushed.
- **Why:** Per the new rule, `main` should be the only branch we use.
- **Note:** Also had to fix the commit's "author" info (name/email) so GitHub shows it as a verified/normal commit instead of flagging it as unrecognized.

### 2026-07-28 — Built the `carnaval_viz` package (v0.1.0)

Implemented the full package per the CLAUDE.md spec, in the `src/` layout (a convention where the actual package code lives inside `src/<package_name>/` instead of the repo root — it prevents accidentally importing the wrong copy of the code during testing):

- **`src/carnaval_viz/colors.py`** — the Brazil-inspired color palette (emerald/tropical green, gold, ocean blue, coral, cream, charcoal, etc.) plus a custom diverging colormap (a gradient from blue → cream → green) used by the heatmap.
- **`src/carnaval_viz/styling.py`** — a shared "style" applied to both charts (fonts, grid lines, spacing, borders). It uses Matplotlib's `rc_context`, which applies settings only temporarily to figures created inside a `with` block, so importing the package never permanently changes a user's global Matplotlib settings.
- **`src/carnaval_viz/validation.py`** — reusable input-checking functions (e.g. "is this actually a DataFrame?", "does this column exist?", "is it numeric?") that both chart functions call, so error-checking logic isn't duplicated. Each raises a specific, informative Python exception (`TypeError`, `KeyError`, `ValueError`) rather than failing silently or with a cryptic message.
- **`src/carnaval_viz/histogram.py`** — the `histogram()` function: plots one numeric column's distribution with optional mean/median reference lines.
- **`src/carnaval_viz/correlation.py`** — the `correlation()` function: plots a correlation heatmap (a grid showing how strongly every pair of numeric columns move together) across all numeric columns, supporting Pearson, Spearman, and Kendall correlation methods (three different statistical ways of measuring "how related are two variables").
- **`src/carnaval_viz/__init__.py`** — wires up the public API so `import carnaval_viz as viz` exposes exactly `viz.histogram` and `viz.correlation`, nothing else.

Supporting files:
- **`pyproject.toml`** — the standard config file that describes a Python package (name, version, dependencies, supported Python versions) and tells packaging tools how to build it. Declared dependencies: pandas, matplotlib, numpy, and scipy (added because pandas' Kendall-correlation calculation delegates to scipy internally — Pearson/Spearman didn't need it, but Kendall does).
- **`.gitignore`** — tells git to ignore generated files (caches, build output, virtual environments) so they never get committed.
- **`LICENSE`** — the standard MIT open-source license text (permissive: anyone can use, modify, and redistribute the code).
- **`CHANGELOG.md`** — a version-by-version history of the *software* (separate from this file, which tracks our *conversation/workflow*).
- **`tests/`** — a pytest test suite (30 tests) covering both functions' happy paths, error handling, and the "don't modify the user's original data" requirement.
- **`examples/generate_dataset.py`** — generates a synthetic (fake but realistic) Brazilian-music-style dataset with a fixed random seed for reproducibility. Went synthetic instead of a real scraped dataset specifically to sidestep any data-licensing questions.
- **`examples/brazil_music_demo.py`** and **`examples/brazil_music_demo.ipynb`** — a script and notebook demonstrating both functions end-to-end.
- **`assets/histogram_example.png`** and **`assets/correlation_example.png`** — real output images generated by running the actual package functions (not mocked up by hand), used in the README.
- **`README.md`** — project overview, install/usage instructions, and the example images.

**Validation performed (all passing):**
- Installed the package in "editable" mode (`pip install -e .`) — lets Python import the package directly from source while developing.
- Ran the test suite: `python -m pytest` → 30/30 tests passed.
- Built the distributable package: `python -m build` → produced both a wheel (`.whl`, a ready-to-install binary package format) and a source distribution (`.tar.gz`).
- Ran `python -m twine check dist/*` → both PASSED. Twine is the standard tool for uploading to PyPI; `check` validates the package without actually uploading anything.
- Confirmed `import carnaval_viz as viz; viz.__all__` returns `['histogram', 'correlation']` as required.

**Bugs found and fixed along the way:**
- An all-missing column (e.g. all `None`) was raising the wrong error type (`TypeError` about dtype instead of `ValueError` about no usable values), because pandas can't infer a real data type for an entirely-empty column. Reordered the checks so "no usable values" is checked first.
- Kendall correlation failed until `scipy` was added as a dependency (see above).

**Status:** v0.1.0 fully implemented and locally validated. Not yet committed/pushed — waiting for your review and go-ahead.

### 2026-07-28 — Renamed commit authorship to you

- **What:** Set local git identity to `korbinvwhite <kwhite11@dons.usfca.edu>`, then rewrote the author on the two existing commits on `main` (previously "Claude") using an interactive rebase, and force-pushed the rewritten history to GitHub.
- **Why:** You wanted commits to show up under your name, not Claude's.
- **Note:** Rewriting already-pushed history changes commit hashes, so anyone else with a local clone (in this case, you, on your own Mac) needs to sync their local `main` to match GitHub's rewritten version rather than merging the two — resolved via `git reset --hard origin/main` on your machine.

### 2026-07-28 — Fixed `fig.show()` not working (real bug)

- **What:** While testing the install on your machine, `hist_fig.show()` — exactly the usage shown in the README's quick-start example — raised `AttributeError: Figure.show works only for figures managed by pyplot`.
- **Root cause:** `histogram()` and `correlation()` were building their figures with Matplotlib's low-level `Figure()` class directly, instead of `plt.subplots()`. Using `Figure()` directly keeps the figure outside of "pyplot" (Matplotlib's higher-level, stateful module that also manages interactive windows) — a common choice in plotting libraries to avoid a subtle memory leak (pyplot keeps every figure it creates in memory until explicitly closed, which matters if a library gets called thousands of times in a loop, e.g. for automated batch report generation). The downside is that `.show()` doesn't work on those figures, which directly contradicted our own documented usage.
- **Fix:** Switched both functions to build their figure via `plt.subplots(figsize=...)` instead, so `.show()` works as documented. Added a note in the code for future maintainers: if `carnaval_viz` is ever used to generate a very large number of figures in a loop, call `plt.close(fig)` after each one to avoid memory buildup.
- **Verified:** Full test suite still passes (30/30); regenerated the example images to confirm output is visually unchanged; confirmed the returned figure is now pyplot-managed.
- **Status:** Fixed locally, not yet committed/pushed.

### 2026-07-29 — Pivoted to a new visual identity: bubble chart + circular calendar

You pushed your own commits directly to `main` in between sessions: a revised `CLAUDE.md` (new project spec) and a new raw dataset file (`Agenda_BL_Rua_Carnaval_Rio-2018_Imprensa.csv`, a real 2018 Rio street-Carnival parade schedule) plus a `scratch.py` test file. The revised spec replaces the original two chart types entirely with two new ones:

- **`bubble_chart()`** — a scatter plot where each point ("bubble") is one Carnival bloco: x/y position from two numeric columns, bubble size scaled from a third numeric column, and color from a categorical column (e.g. region), with an option to label the N largest bubbles.
- **`circular_calendar()`** — a circular/polar plot where each event becomes one point placed around a ring based on its calendar date (angle), all at a fixed distance from the center, sized and colored the same way as the bubble chart, with month labels running around the outside like a clock face.

**What was done:**
- Removed the old `histogram()`/`correlation()` code, tests, and synthetic dataset entirely (the revised spec says v0.1.0 exposes *exactly* the two new functions).
- Wrote `examples/prepare_dataset.py` to clean the real raw dataset: it's semicolon-separated (not comma-separated), uses Brazilian-style numbers (`"1.500"` means 1,500), has inconsistent capitalization in the region names (`"Zona norte 1"` vs `"Zona Norte 1"`), and uses day-first dates.
- Rewrote `validation.py` for the new API: multi-column existence/numeric checks, a date-parsing helper, and a helper that drops rows missing any of several required columns at once.
- Added a categorical color-mapping helper (`colors.categorical_color_map()`) and shared bubble-sizing/legend-building helpers (`styling.scale_marker_sizes()`, `styling.legend_handles_for_categories()`) so both chart functions share logic instead of duplicating it.
- Wrote `bubble_chart.py` and `circular_calendar.py`, new tests for both, a new example script/notebook, and regenerated the two README example images from the real data.
- Removed the `scipy` dependency (it was only needed for the old Kendall-correlation option, which no longer exists).
- Updated `scratch.py` (a file you added yourself) to use the new functions instead of the removed ones, since it referenced a dataset file that no longer exists.

**Bugs found and fixed along the way** (see `ISSUES.md` for the full write-up of each):
- Cleaning the real dataset silently corrupted the founding-year column (`1972` became `19720`) because the raw file wasn't read as plain text first, so pandas guessed a numeric type before the cleaning code could handle the Brazilian number format itself.
- Fixing the earlier day-first date bug (issue #4) had actually introduced a *new*, sneakier one: forcing `dayfirst=True` everywhere corrupted our own already-correct, unambiguous dates once they were saved in standard `yyyy-mm-dd` format, scattering Carnival events across the whole year in the circular calendar instead of clustering them in Jan/Feb where they belong. Fixed by letting pandas auto-detect the date format instead of forcing an assumption, and added a test specifically covering this date style so it can't silently regress again.

**Status:** Both new functions implemented and validated locally (25/25 tests passing). Not yet committed/pushed — waiting for review and go-ahead.

### 2026-07-29 — Applied a design review, redesigned the Carnival calendar

You pushed a review document, `Carnival_Visualization_Review_Notes.txt`, with specific critique of both charts. Two of its suggestions (making the calendar's radius meaningful instead of fixed, and renaming `circular_calendar()`) conflicted with the locked `CLAUDE.md` spec, so I asked which way you wanted to go before touching either — you chose to make both changes, with radius encoding event start time and the function renamed to `carnival_calendar()`.

**Bubble chart changes:**
- Bubble size now uses square-root scaling by default (configurable to `"log"` or `"linear"`) instead of linear, so one bloco with a 1.5-million-person audience no longer crushes every other bubble down to a barely-visible dot.
- Y-axis now defaults to a log scale (`yscale="log"`, with a `"linear"` opt-out) for the same reason — values were previously compressed near zero by that same outlier.
- Legend now orders regions by total audience (largest first) instead of alphabetically.
- More descriptive default title.

**Calendar changes (renamed `circular_calendar()` → `carnival_calendar()`):**
- Angle now scales across only the season's actual date range (e.g. the ~7 weeks the real dataset spans), instead of a full 365-day year — the original version left most of the circle empty since Carnival data only covers a couple of months.
- Tick labels now count down in weeks to the final event date (e.g. "3 Weeks Before", "Event Day") instead of showing all 12 month names.
- Radius is no longer fixed — it now encodes each event's start time of day (closer to center = earlier in the day), added as a new required `time` parameter. This was chosen over the review's other two radius options (audience, weeks-before-Carnival) specifically because those would have duplicated information already shown by bubble size and angle, respectively.
- Reduced maximum bubble size and increased transparency to cut down on overlap where many events cluster on the same few dates.

**Bugs found and fixed along the way** (full write-ups in `ISSUES.md` #9-10):
- The new square-root bubble scaling silently produced invalid (`NaN`) sizes for negative values instead of erroring, since a negative number has no real square root. Added explicit validation rejecting negative "size" values before any math runs, since a negative magnitude never makes sense for a bubble's size anyway.
- Fitting the season into the full 360-degree circle caused a bug where the season's first and last day landed at the identical angle (like a clock's "12" marking both an end and a start) since a date range isn't actually cyclic. Fixed by reserving a small angular gap so the two ends of the season stay visually separate.

Also updated `CLAUDE.md` itself to reflect every one of these approved changes, since it's the project's living source-of-truth spec, not a historical record.

**Status:** Both charts rebuilt and re-validated (all tests passing). Not yet committed/pushed — waiting for review and go-ahead.

### 2026-07-29 — Two readability tweaks

You asked for two small usability fixes:
- The calendar's radial time labels were in 24-hour format (e.g. "16:00", "21:00"); switched to ordinary 12-hour clock format ("4:00 PM", "9:00 PM") since that's how most people read a clock.
- The bubble chart's log-scaled y-axis was showing scientific notation (e.g. "10^6"), which most people don't translate to "1 million" instantly; added a shared formatter (`styling.use_human_readable_axis()`) that renders tick labels as "100", "1K", "10K", "100K", "1M" instead.

Both are small, self-contained changes -- no spec conflicts, no new bugs. Verified visually against the regenerated example images and re-ran the full test suite (33/33 passing).

### 2026-07-29 — Shared visual style: cream background, gold titles

Three related styling requests, all in `colors.py`/`styling.py` (the shared style both charts pull from):
- Figure background changed to a warm cream (`#FAF7F2`) instead of plain white.
- Chart titles changed to a muted gold (`#B8860B`) instead of dark charcoal.
- Confirmed the actual plotting area (as opposed to the figure background around it) stays white, sitting on top of the cream background -- this was already true by design (figure background and axes background were already two separate settings), just needed the two colors to actually differ for the contrast to become visible.

One interesting wrinkle worth noting for later: for the Carnival calendar specifically, Matplotlib's polar-plot background patch is circular, not a full rectangle -- so the white plotting area there renders as a white disk (like a clock face) rather than a white square, which arguably reads better for that chart than a plain rectangle would have. Verified both example images visually and re-ran the full test suite (33/33 passing) before checking in.

