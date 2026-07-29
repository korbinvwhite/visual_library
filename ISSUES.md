# Issues We Ran Into

A running list of problems hit while building and testing `carnaval_viz`, what caused them, and how they were fixed. Kept separate from `WORKFLOW_LOG.md` (which covers the whole workflow) so this can be scanned quickly as a "gotchas" reference.

---

### 1. All-missing column raised the wrong kind of error

**What went wrong:** A column that was entirely empty (all missing values) was raising a `TypeError` about "wrong data type" instead of a `ValueError` about "no usable data."

**Cause:** When a pandas column has no real values at all, pandas can't figure out what type it "should" be, so it defaults to a generic `object` type — which looks identical to a column of actual text data from the validation code's point of view.

**Fix:** Reordered the validation checks to test for "is everything missing?" before testing "is this numeric?" so the more accurate, more useful error message wins.

---

### 2. Kendall correlation method crashed with a missing-module error

**What went wrong:** `correlation(df, method="kendall")` failed with `ModuleNotFoundError: No module named 'scipy'`, even though Pearson and Spearman worked fine.

**Cause:** Under the hood, pandas' Kendall-correlation calculation specifically depends on a separate package called `scipy` (a scientific-computing library), while the other two methods don't need it.

**Fix:** Added `scipy` as an official dependency in `pyproject.toml` so it gets installed automatically alongside the package.

---

### 3. Commits showed "Claude" as the author instead of you

**What went wrong:** The first two commits on `main` were authored under Claude's identity rather than yours.

**Cause:** Git records whichever name/email is configured at commit time, and the working session's git identity was set to Claude by default.

**Fix:** Set git's local identity to `korbinvwhite`, then rewrote the author on those two commits and force-pushed the corrected history to GitHub. Side effect: because rewriting history changes the underlying commit IDs, your separate local clone on your Mac ended up with a diverged, outdated copy of `main` — fixed by resetting your local branch to match GitHub's corrected version (`git reset --hard origin/main`).

---

### 4. Real-world Brazilian dataset failed to load with a parsing error

**What went wrong:** Loading a real Carnival-related CSV file (`Agenda_BL_Rua_Carnaval_Rio-2018_Imprensa.csv`) with `pd.read_csv(...)` failed with a "wrong number of fields" error.

**Cause:** `pd.read_csv()` assumes comma-separated values by default, but many Brazilian/European datasets use a **semicolon (`;`)** as the column separator instead — partly because commas are already used as the decimal point in those locales (e.g. `3,14` instead of `3.14`).

**Fix:** Load the file with the separator specified explicitly: `pd.read_csv(path, sep=";")`.

---

### 5. Package "installed" but still wasn't found (`ModuleNotFoundError`)

**What went wrong:** `pip install -e .` reported success, but running a script still failed with `ModuleNotFoundError: No module named 'matplotlib'` (and earlier, couldn't find `carnaval_viz` at all).

**Cause:** The install and the script run were happening in two different Python environments — one in a conda environment (`base`), the other in this project's isolated `.venv` folder. Installing a package into one environment doesn't make it available in another; each Python environment keeps its own separate set of installed packages.

**Fix:** Ran the install using the `.venv` environment's own `pip` specifically (`.venv/bin/pip install -e ".[dev]"`), matching the environment the script was actually executed with.

---

### 6. `fig.show()` didn't work, even though the README says it should

**What went wrong:** Calling `.show()` on a figure returned by `histogram()` raised `AttributeError: Figure.show works only for figures managed by pyplot`.

**Cause:** The chart functions were building figures using Matplotlib's low-level `Figure()` class directly rather than the more common `plt.subplots()`. That approach is sometimes preferred in library code because it avoids a memory-leak risk (Matplotlib's higher-level `pyplot` module keeps every figure it creates in memory until it's explicitly closed), but it also disconnects the figure from `pyplot`, so `.show()` has nothing to hook into.

**Fix:** Switched both `histogram()` and `correlation()` to build their figure with `plt.subplots()` instead, restoring `.show()` support to match the documented usage. Left a note in the code that anyone generating a very large number of figures in a loop should call `plt.close(fig)` afterward to avoid the memory-buildup issue this design originally avoided.

---

### 7. Cleaning the real Rio Carnival dataset silently corrupted the founding year

**What went wrong:** After writing a script to clean up the raw Rio Carnival blocos CSV (which uses Brazilian-style numbers like `"1.500"` meaning 1,500), the cleaned `year_founded` column ended up with nonsense values like `19720` instead of `1972`.

**Cause:** The cleaning script read the raw file without forcing every column to be read as plain text. Because every value in the `year_founded` column happened to *look* numeric, pandas silently converted it to a decimal-number (`float`) column while loading the file — turning `"1972"` into `1972.0`. When the cleaning step later converted that back to text to strip out the Brazilian thousands-separator dots, `1972.0` became the text `"1972.0"`, and stripping the dot out of *that* produced `"19720"` — the decimal point from the automatic float conversion got mistaken for a thousands separator.

**Fix:** Read the raw CSV with every column forced to plain text (`dtype=str`) from the start, so pandas never silently guesses a numeric type before the cleaning code gets a chance to interpret the Brazilian number format correctly itself.

---

### 8. Fixing one date-format bug accidentally introduced a worse one

**What went wrong:** After building `circular_calendar()`, real event dates were plotted spread evenly across the whole year instead of clustered in Carnival season (January/February) as they should be. Investigating traced it back to the shared date-parsing helper: it had been set to always assume day-first dates (`dayfirst=True`) to correctly handle Brazilian-style `dd/mm/yyyy` dates elsewhere in the project (see issue #4). But applied to our own *already-cleaned* dataset — which stores dates in the unambiguous `yyyy-mm-dd` (ISO) format — that same setting silently corrupted them (e.g. turning January 7th into July 1st) instead of leaving them alone.

**Cause:** Forcing `dayfirst=True` isn't a safe blanket setting: pandas uses it to help *guess* a date format from the first few rows, then applies that one guess to the entire column. For an ISO-formatted column this guess overrides what should be an unambiguous, already-correct format, actively making it wrong.

**Fix:** Removed the forced `dayfirst=True` entirely from the shared parser and let pandas auto-detect the format instead — it reliably figures out day-first vs. month-first on its own as soon as it sees any date in the column with a day above 12 (true of nearly any real multi-day dataset), and it never touches already-unambiguous ISO dates. Added a test covering ISO-format dates specifically, alongside the existing Brazilian-format test, so this class of regression gets caught automatically going forward.

---

### 9. Square-root bubble scaling silently broke on negative values

**What went wrong:** After adding square-root scaling to make bubble sizes read better (per the design review), a test that inserted a negative test value into the audience column produced a Python warning (`invalid value encountered in sqrt`) instead of a clear error, and would have silently rendered that bubble with a nonsensical, missing size.

**Cause:** The square root of a negative number isn't a real number, so NumPy returns `NaN` (not-a-number) instead of raising an error. Since a bubble's size represents a magnitude (like an audience count), a negative value doesn't make sense for it in the first place -- but nothing was checking for that before the math ran.

**Fix:** Added an explicit check that rejects negative values in the "size" column with a clear `ValueError` before any scaling happens, for both `bubble_chart()` and `carnival_calendar()`, instead of letting the math fail silently.

---

### 10. The Carnival calendar's season start and end overlapped at the same spot

**What went wrong:** After reworking the calendar to focus on just the Carnival season (instead of a full, mostly-empty year), the tick labels for "6 Weeks Before" and "Event Day" rendered on top of each other at the top of the circle, unreadable.

**Cause:** The season's date range was mapped onto the *entire* 360-degree circle, so the first day and the last day of the season landed at the exact same angle (0 degrees = 360 degrees, the same spot) -- the same way a clock's "12" marks both an ending and a beginning. But a date range isn't cyclic like a repeating clock face or calendar year; it has two genuinely different ends that shouldn't visually coincide.

**Fix:** Reserved a small gap (20 degrees) at the top of the circle and mapped the season across the remaining ~340 degrees instead of the full circle, so the season's start and end stay visually distinct.
