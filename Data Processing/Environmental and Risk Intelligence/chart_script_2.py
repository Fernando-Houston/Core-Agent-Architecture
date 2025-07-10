import plotly.graph_objects as go
import plotly.io as pio

# Data for PM2.5 levels
categories = ["Houston MSA 2000", "Houston MSA 2020", "Current Harris County 2024", "New EPA Standard 2024"]
levels = [13.1, 10.1, 12.5, 9.0]
types = ["Historical", "Improved", "Current", "Standard"]

# Define colors based on the brand colors provided
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F']

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        y=categories,
        x=levels,
        orientation='h',
        marker_color=colors,
        text=[f'{level} µg/m³' for level in levels],
        textposition='auto',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title='Harris County PM2.5 Air Quality Progress',
    xaxis_title='PM2.5 Level (µg/m³)',
    yaxis_title='Measurement',
    showlegend=False
)

# Update y-axis to show abbreviated category names
fig.update_yaxes(
    tickmode='array',
    tickvals=categories,
    ticktext=['Houston 2000', 'Houston 2020', 'Harris Co 2024', 'EPA Std 2024']
)

# Save the chart
fig.write_image('harris_county_pm25_chart.png')