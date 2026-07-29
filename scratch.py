import matplotlib.pyplot as plt
import pandas as pd
import carnaval_viz as viz

df = pd.read_csv("examples/rio_carnival_blocos.csv")

# Bubble chart
bubble_fig = viz.bubble_chart(
    df,
    x="year_founded",
    y="estimated_audience",
    size="estimated_audience",
    color="region",
    annotate_top=3,
)

# Carnival calendar
calendar_fig = viz.carnival_calendar(
    df, date="event_date", time="gathering_time",
    size="estimated_audience", color="region",
)

plt.show()  # keeps both windows open until you close them