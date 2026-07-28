import pandas as pd
import carnaval_viz as viz


df = pd.read_csv("examples/brazilian_music_sample.csv")

hist_fig = viz.histogram(df, "danceability")
hist_fig.show()   # pops up the chart
