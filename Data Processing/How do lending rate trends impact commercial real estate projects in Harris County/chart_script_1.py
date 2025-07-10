import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Data from the provided JSON
market_impacts = {
    "Transaction Volume Change": -40,
    "Construction Starts Change": -50, 
    "Multifamily Value Change": 0.8,
    "Office Value Change": -7.7,
    "Retail Value Change": 2.0
}

# Create DataFrame
df = pd.DataFrame(list(market_impacts.items()), columns=['Metric', 'Change'])

# Abbreviate metric names to fit 15 character limit
df['Metric_Short'] = [
    'Transaction Vol',
    'Construction',
    'Multifamily',
    'Office',
    'Retail'
]

# Create colors based on positive/negative values
colors = []
for val in df['Change']:
    if val < 0:
        colors.append('#B4413C')  # Moderate red for negative
    else:
        colors.append('#1FB8CD')  # Strong cyan for positive

# Create bar chart
fig = go.Figure(data=[
    go.Bar(
        x=df['Metric_Short'],
        y=df['Change'],
        marker_color=colors,
        text=[f"{val}%" for val in df['Change']],
        textposition='outside',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title="Harris County CRE Market Impact",
    xaxis_title="Market Segment",
    yaxis_title="Change (%)",
    showlegend=False
)

# Save the chart
fig.write_image("harris_county_cre_impact.png")