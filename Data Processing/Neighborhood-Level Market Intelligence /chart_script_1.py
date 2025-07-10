import plotly.graph_objects as go
import pandas as pd

# Create the data
data = {
    "counties": ["Harris Co.", "Montgomery Co.", "Fort Bend Co.", "Collin Co.", "Tarrant Co."],
    "permits": [1573, 690, 514, 796, 501],
    "metro_areas": ["Houston", "Houston", "Houston", "Dallas", "Dallas"]
}

df = pd.DataFrame(data)

# Sort by permits in ascending order for horizontal bar chart (smallest at bottom)
df = df.sort_values('permits', ascending=True)

# Create color mapping - Houston counties in cyan, Dallas counties in orange
color_map = {"Houston": "#1FB8CD", "Dallas": "#FFC185"}
colors = [color_map[metro] for metro in df['metro_areas']]

# Create horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df['permits'],
    y=df['counties'],
    orientation='h',
    marker_color=colors,
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title="Top 5 Counties Permits 2024",
    xaxis_title="Permits",
    yaxis_title="County"
)

# Update axes with proper formatting
fig.update_xaxes(
    tickvals=[500, 1000, 1500],
    ticktext=["500", "1k", "1.5k"]
)

# Save the chart
fig.write_image("permit_chart.png")