import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load the data
df = pd.read_csv("houston_tech_sector_impact.csv")

# Abbreviate long metric names to fit 15 character limit
df['Metric'] = df['Metric'].replace('VC Funding (millions)', 'VC Funding (m)')

# Create grouped bar chart
fig = go.Figure()

# Add 2020 values bar
fig.add_trace(go.Bar(
    x=df['Metric'],
    y=df['2020_Value'],
    name='2020',
    marker_color='#1FB8CD',
    text=df['2020_Value'],
    textposition='outside',
    cliponaxis=False
))

# Add 2025 values bar
fig.add_trace(go.Bar(
    x=df['Metric'],
    y=df['2025_Value'],
    name='2025',
    marker_color='#FFC185',
    text=df['2025_Value'],
    textposition='outside',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Houston Tech Sector Growth: 2020 vs 2025',
    xaxis_title='Metrics',
    yaxis_title='Value',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update x-axis to rotate labels 45 degrees
fig.update_xaxes(tickangle=45)

# Update y-axis to use logarithmic scale
fig.update_yaxes(type="log")

# Save the chart
fig.write_image("houston_tech_chart.png")
print("Chart saved successfully!")