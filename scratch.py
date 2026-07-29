import matplotlib.pyplot as plt
import pandas as pd
import carnaval_viz as viz

df = pd.read_csv("examples/brazilian_music_sample.csv")

# Histogram
hist_fig = viz.histogram(df, "danceability")

# Correlation heatmap
corr_fig = viz.correlation(df)

plt.show()  # keeps both windows open until you close them