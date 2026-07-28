"""Color palette for carnaval_viz.

Defines the Brazil-inspired color palette shared by every chart in the
package, plus a diverging colormap (a gradient of colors used to represent
a range of numbers, here running from ocean blue -> cream -> tropical
green) for the correlation heatmap.
"""

from matplotlib.colors import LinearSegmentedColormap

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

# Roles used by the styling module and the two chart functions.
HISTOGRAM_BAR_COLOR = TROPICAL_GREEN
MEAN_LINE_COLOR = GOLD
MEDIAN_LINE_COLOR = OCEAN_BLUE

FIGURE_BACKGROUND = "#FFFFFF"
AXES_BACKGROUND = "#FFFFFF"
GRID_COLOR = "#D9D2C4"
TEXT_COLOR = DARK_CHARCOAL

# Diverging colormap for the correlation heatmap: negative correlations
# render ocean blue, zero renders light cream, positive correlations
# render tropical green.
CORRELATION_CMAP = LinearSegmentedColormap.from_list(
    "carnaval_viz_correlation",
    [OCEAN_BLUE, LIGHT_CREAM, TROPICAL_GREEN],
)
