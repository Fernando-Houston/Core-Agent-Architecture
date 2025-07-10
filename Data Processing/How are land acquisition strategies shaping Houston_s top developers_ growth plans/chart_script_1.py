!pip install kaleido

import plotly.graph_objects as go
import plotly.express as px

# Data
data = [
    {"company": "Starwood Capital/Land Tejas", "value": 800, "details": "11 communities, 16,000+ lots"},
    {"company": "Hines West Houston", "value": 600, "details": "3,000 acres, 7,000+ homes"},
    {"company": "Hines Iowa Colony", "value": 200, "details": "954 acres, 2,100 homes"},
    {"company": "Stream Realty Industrial", "value": 50, "details": "40.7 acres"}
]

# Abbreviate company names to fit 15 character limit
company_names = [
    "Starwood/Tejas",
    "Hines West",
    "Hines Iowa", 
    "Stream Realty"
]

values = [d["value"] for d in data]
details = [d["details"] for d in data]

# Brand colors in order
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F']

# Create hover text combining value and details
hover_text = [f"${v}M<br>{d}" for v, d in zip(values, details)]

# Create text labels for bars
text_labels = [f"${v}M<br>{d}" for v, d in zip(values, details)]

# Create bar chart
fig = go.Figure(data=[
    go.Bar(
        x=company_names,
        y=values,
        text=text_labels,
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>%{text}<extra></extra>',
        marker_color=colors,
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title="Houston Land Acquisition Deals 2024-25",
    xaxis_title="Company",
    yaxis_title="Value ($M)",
    showlegend=False
)

# Save chart
fig.write_image("houston_land_deals.png")