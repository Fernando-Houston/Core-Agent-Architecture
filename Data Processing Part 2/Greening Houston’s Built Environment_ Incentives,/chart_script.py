import plotly.graph_objects as go
import plotly.io as pio

# Data from the provided JSON
data = {
    "LEED Certified": 1,
    "LEED Silver": 2.5,
    "LEED Gold": 5,
    "LEED Platinum": 10,
    "Solar/Wind Exemption": 100
}

# Sort data by percentage (lowest to highest)
sorted_data = sorted(data.items(), key=lambda x: x[1])
programs = [item[0] for item in sorted_data]
percentages = [item[1] for item in sorted_data]

# Create horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=percentages,
    y=programs,
    orientation='h',
    marker_color='#1FB8CD',  # Primary brand color
    text=[f'{p}%' for p in percentages],
    textposition='outside',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Property Tax Abatement Rates',
    xaxis_title='Abatement %',
    yaxis_title='Program',
    showlegend=False
)

# Update x-axis to show range 0-100%
fig.update_xaxes(range=[0, 105])

# Save the chart
fig.write_image('property_tax_chart.png')