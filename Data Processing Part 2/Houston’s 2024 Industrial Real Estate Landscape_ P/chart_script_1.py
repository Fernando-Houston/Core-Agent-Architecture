import plotly.graph_objects as go
import json

# Load the data
data_json = {"Submarket":["Northwest Far","East-Southeast Far","North Far","East-Southeast Near"],"UnderConstruction_MSF":[3.4,2.5,2.2,2.1]}

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        y=data_json["Submarket"],
        x=data_json["UnderConstruction_MSF"],
        orientation='h',
        marker_color='#1FB8CD',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title="Houston Industrial Construction Q4 2024",
    xaxis_title="Sq Ft (Millions)",
    yaxis_title="Submarket"
)

# Save the chart
fig.write_image("houston_industrial_construction.png")