import plotly.graph_objects as go
import pandas as pd

# Create the data
data = {
    "metrics": [
        {"metric": "Housing Affordability", "houston": 4.7, "traditional": 6.2, "note": "Lower is better"},
        {"metric": "Development Speed", "houston": 8.5, "traditional": 4.2, "note": "Higher is better"},
        {"metric": "Mixed-Use Development", "houston": 8.0, "traditional": 3.5, "note": "Higher is better"},
        {"metric": "Regulatory Flexibility", "houston": 9.0, "traditional": 2.8, "note": "Higher is better"},
        {"metric": "Housing Supply Response", "houston": 8.2, "traditional": 3.8, "note": "Higher is better"}
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data["metrics"])

# Abbreviate metric names to fit 15 character limit
metric_names = [
    "Housing Afford",
    "Dev Speed", 
    "Mixed-Use Dev",
    "Reg Flexibility",
    "Supply Response"
]

# Create the grouped bar chart
fig = go.Figure()

# Add Houston bars
fig.add_trace(go.Bar(
    name='Houston',
    x=metric_names,
    y=df['houston'],
    marker_color='#1FB8CD',
    cliponaxis=False
))

# Add Traditional Cities bars
fig.add_trace(go.Bar(
    name='Traditional',
    x=metric_names,
    y=df['traditional'],
    marker_color='#FFC185',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Houston vs Traditional Zoning Cities',
    xaxis_title='Metrics',
    yaxis_title='Score',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save the chart
fig.write_image('houston_comparison.png')