# Changelog

## 0.1.0 - 2026-07-29

Initial release.

### Added
- `bubble_chart()`: publication-quality bubble chart (x/y position, automatically-scaled bubble size, categorical color) for Rio Carnival bloco data.
- `circular_calendar()`: circular/polar calendar plotting events by date around the calendar year, sized and colored by category.
- Shared Rio Carnival-inspired visual styling and color palette.
- Input validation with clear, actionable error messages.
- Test suite covering both visualization functions.
- Example script, notebook, and a cleaned Rio Carnival Blocos dataset.

### Changed
- Replaced the original `histogram()`/`correlation()` API (from an earlier draft of this spec) with `bubble_chart()`/`circular_calendar()` per the revised project spec.
