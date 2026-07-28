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
