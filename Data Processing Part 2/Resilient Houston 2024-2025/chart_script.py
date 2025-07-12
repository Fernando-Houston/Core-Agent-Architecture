import plotly.graph_objects as go
import json

# Data from the provided JSON
data = [
    {"Project":"Inwood Forest","Capacity_acft":1200},
    {"Project":"Taylor Gully/Woodridge","Capacity_acft":412},
    {"Project":"Upper South Mayde","Capacity_acft":181},
    {"Project":"Meyergrove","Capacity_acft":83}
]

# Extract project names and capacities
projects = [item["Project"] for item in data]
capacities = [item["Capacity_acft"] for item in data]

# Shorten project names to fit 15 character limit
short_projects = ["Inwood Forest", "Taylor Gully", "Upper S Mayde", "Meyergrove"]

# Brand colors for the bars
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F']

# Create the bar chart
fig = go.Figure()

# Add bars with distinct colors and text labels
fig.add_trace(go.Bar(
    x=short_projects,
    y=capacities,
    marker_color=colors,
    text=capacities,
    textposition='outside',
    textfont=dict(size=14),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title="Houston Stormwater Detention (2024-25)",
    xaxis_title="Project",
    yaxis_title="Capacity (ac-ft)",
    showlegend=False
)

# Save the chart
fig.write_image("houston_stormwater_detention.png")