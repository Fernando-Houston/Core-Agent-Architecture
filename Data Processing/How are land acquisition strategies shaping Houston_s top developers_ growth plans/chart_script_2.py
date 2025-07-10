import plotly.graph_objects as go
import json

# Data from the provided JSON
data = [
  {"area": "Grand Parkway Corridor", "percentage": 35},
  {"area": "290 Corridor/Waller County", "percentage": 25},
  {"area": "Energy Corridor", "percentage": 20},
  {"area": "Northwest Far Submarket", "percentage": 15},
  {"area": "Other Areas", "percentage": 5}
]

# Abbreviate area names to meet 15 character limit
abbreviated_areas = [
    "Grand Parkway",
    "290/Waller Co", 
    "Energy Corridor",
    "Northwest Far",
    "Other Areas"
]

percentages = [item["percentage"] for item in data]

# Brand colors in order
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C']

# Create horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=percentages,
    y=abbreviated_areas,
    orientation='h',
    marker_color=colors,
    text=[f"{p}%" for p in percentages],
    textposition='auto',
    textfont=dict(size=14, color='black')
))

fig.update_layout(
    title="Houston Development Geographic Concentration 2025",
    xaxis_title="Percentage (%)",
    yaxis_title="Geographic Area",
    showlegend=False
)

# Save the chart
fig.write_image("houston_development_chart.png")