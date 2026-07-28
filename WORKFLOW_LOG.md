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

