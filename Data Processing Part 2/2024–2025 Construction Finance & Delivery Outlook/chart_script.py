import plotly.graph_objects as go
import plotly.io as pio

# Data from the provided JSON
quarters = ["2023-Q4", "2024-Q1", "2024-Q2", "2024-Q3"]
index_values = [1395, 1408, 1421, 1432]

# Create the line chart
fig = go.Figure()

# Add the line trace
fig.add_trace(go.Scatter(
    x=quarters,
    y=index_values,
    mode='lines+markers',
    name='Turner Building Cost Index',
    line=dict(color='#1FB8CD', width=3),
    marker=dict(size=8, color='#1FB8CD'),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Construction Cost Inflation Trend',
    xaxis_title='Quarter',
    yaxis_title='Index Value',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save as PNG
fig.write_image("construction_cost_trend.png")