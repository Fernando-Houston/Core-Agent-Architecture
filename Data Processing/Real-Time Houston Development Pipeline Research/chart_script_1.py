import plotly.graph_objects as go
import plotly.io as pio

# Data for Houston construction permits
years = ["2020", "2021", "2022", "2023", "2024", "2025*"]
permits = [49915, 47000, 48500, 50200, 52851, 40000]

# Create the line chart
fig = go.Figure()

# Add the line trace
fig.add_trace(go.Scatter(
    x=years, 
    y=permits,
    mode='lines+markers',
    name='Permits',
    line=dict(color='#1FB8CD', width=3),
    marker=dict(size=8, color='#1FB8CD'),
    hovertemplate='<b>%{x}</b><br>Permits: %{y:,.0f}<extra></extra>'
))

# Update layout
fig.update_layout(
    title="Houston Building Permits 2020-2025",
    xaxis_title="Year",
    yaxis_title="Num of Permits",
    showlegend=False,
    hovermode='x unified'
)

# Update axes with grid lines
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='lightgray'
)

# Format y-axis to show numbers in thousands
fig.update_yaxes(
    tickvals=[40000, 45000, 50000, 55000],
    ticktext=['40k', '45k', '50k', '55k']
)

# Save the chart
fig.write_image("houston_permits_chart.png")