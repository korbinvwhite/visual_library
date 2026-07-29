"""Color palette for carnaval_viz.

Defines the Brazil-inspired color palette shared by every chart in the
package, plus a diverging colormap (a gradient of colors used to represent
a range of numbers, here running from ocean blue -> cream -> tropical
green) for the correlation heatmap.
"""

import itertools

# Core palette. Named after the visual theme so usage reads clearly,
# e.g. colors.EMERALD instead of an unlabeled hex code.
EMERALD = "#0B6E4F"
TROPICAL_GREEN = "#1FA774"
GOLD = "#F2B705"
OCEAN_BLUE = "#0A5C8A"
TURQUOISE = "#12A4B0"
CORAL = "#F2542D"
WARM_ORANGE = "#F28C28"
LIGHT_CREAM = "#FBF4E4"
DARK_CHARCOAL = "#2B2B2B"

FIGURE_BACKGROUND = "#FAF7F2"
AXES_BACKGROUND = "#FFFFFF"
GRID_COLOR = "#D9D2C4"
TEXT_COLOR = DARK_CHARCOAL
TITLE_COLOR = "#B8860B"

# Qualitative palette used to color categories (e.g. Region) in the bubble
# chart and circular calendar. Ordered for strong contrast between
# neighbors; cycles if there are more categories than colors.
CATEGORICAL_PALETTE = [
    EMERALD,
    GOLD,
    OCEAN_BLUE,
    CORAL,
    TURQUOISE,
    WARM_ORANGE,
    TROPICAL_GREEN,
    DARK_CHARCOAL,
]


def categorical_color_map(categories) -> dict:
    """Assign a consistent palette color to each distinct category.

    Args:
        categories: An iterable of category values (e.g. a DataFrame
            column). Order is determined by first appearance in sorted,
            de-duplicated form so the same categories always map to the
            same colors across calls.

    Returns:
        A dict mapping each distinct category value to a hex color string.
    """
    unique_categories = sorted(set(categories), key=str)
    palette_cycle = itertools.cycle(CATEGORICAL_PALETTE)
    return {category: color for category, color in zip(unique_categories, palette_cycle)}
