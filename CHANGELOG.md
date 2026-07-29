# Changelog

## 0.1.0 - 2026-07-29

Initial release.

### Added
- `bubble_chart()`: publication-quality bubble chart (x/y position, square-root-scaled bubble size, categorical color, log-scaled y-axis by default) for Rio Carnival bloco data.
- `carnival_calendar()`: calendar wheel scoped to the actual event season, plotting events by date (angle) and time of day (radius), sized and colored by category.
- Shared Rio Carnival-inspired visual styling and color palette.
- Input validation with clear, actionable error messages.
- Test suite covering both visualization functions.
- Example script, notebook, and a cleaned Rio Carnival Blocos dataset.

### Changed
- Replaced the original `histogram()`/`correlation()` API (from an earlier draft of this spec) with `bubble_chart()`/`circular_calendar()` per the revised project spec.
- Following a design review, renamed `circular_calendar()` to `carnival_calendar()` and reworked it: angle now scopes to the season's own date range instead of the full year (with tick labels counting down in weeks to the final event date), and radius now encodes event time of day instead of being fixed.
- `bubble_chart()`: switched to square-root bubble scaling and a log-scaled y-axis (both configurable) to prevent a single large outlier from crushing every other value; legend now orders categories by total size instead of alphabetically; improved default title.
