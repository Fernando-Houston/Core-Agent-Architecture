import plotly.graph_objects as go
import pandas as pd
import json

# Parse the data
data = {"price_history": [{"Year": 2017, "Price_per_sqft": 65.62}, {"Year": 2018, "Price_per_sqft": 91.22}, {"Year": 2019, "Price_per_sqft": 101.78}, {"Year": 2020, "Price_per_sqft": 120.83}, {"Year": 2021, "Price_per_sqft": 134.16}, {"Year": 2022, "Price_per_sqft": 156.91}, {"Year": 2023, "Price_per_sqft": 172.27}, {"Year": 2024, "Price_per_sqft": 165.56}], "cost_breakdown": [{"category": "Construction Cost", "percentage": 85, "value": 212500}, {"category": "Land Cost", "percentage": 12, "value": 30000}, {"category": "Permit & Impact Fees", "percentage": 3, "value": 7400}], "key_metrics": [{"metric": "Median Property Value", "value": "$285,105"}, {"metric": "Gross Rental Yield", "value": "10.1%"}, {"metric": "5-Year Appreciation", "value": "62.7%"}, {"metric": "Property Tax Rate", "value": "2.12%"}], "additional_metrics": [{"metric": "Median Lot Size", "value": "7,800 sq ft"}, {"metric": "Average Days on Market", "value": "52 days"}, {"metric": "Monthly Rental Income", "value": "$2,400"}, {"metric": "Current Price/sq ft", "value": "$165.56"}]}

# Create DataFrame for price history
df = pd.DataFrame(data['price_history'])

# Create bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df['Year'],
    y=df['Price_per_sqft'],
    marker_color='#1FB8CD',
    hovertemplate='<b>%{x}</b><br>$%{y:.2f}/sq ft<extra></extra>',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Price/Sq Ft History (2017-2024)',
    xaxis_title='Year',
    yaxis_title='Price/Sq Ft ($)',
)

# Save the chart
fig.write_image('katy_heights_roi_analysis.png')