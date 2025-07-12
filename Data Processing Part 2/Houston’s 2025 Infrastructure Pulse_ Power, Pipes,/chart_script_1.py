import plotly.graph_objects as go
import json

# Data from the provided JSON
data = [{"Year":2015,"Capacity":80},{"Year":2023,"Capacity":160},{"Year":2025,"Capacity":400}]

# Extract years and capacities
years = [item["Year"] for item in data]
capacities = [item["Capacity"] for item in data]

# Create the line chart
fig = go.Figure()

# Add line with markers
fig.add_trace(go.Scatter(
    x=years,
    y=capacities,
    mode='lines+markers+text',
    line=dict(color='#1FB8CD', width=3),
    marker=dict(size=10, color='#1FB8CD'),
    text=[f'{cap}' for cap in capacities],
    textposition='top center',
    textfont=dict(size=12),
    name='Capacity',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title="Water Plant Expansion Capacity",
    xaxis_title="Year",
    yaxis_title="Capacity (MGD)",
    showlegend=False
)

# Update axes
fig.update_xaxes(
    tickmode='array',
    tickvals=years,
    ticktext=years
)

fig.update_yaxes(
    tickformat='.0f'
)

# Save the chart
fig.write_image("water_plant_capacity_chart.png")