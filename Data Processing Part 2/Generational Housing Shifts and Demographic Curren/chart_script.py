import plotly.graph_objs as go
import pandas as pd

# Create the data
data = [
    {"Submarket": "Brookshire", "Sales_Growth_%": 257.6},
    {"Submarket": "Waller", "Sales_Growth_%": 76.9},
    {"Submarket": "Conroe Northwest", "Sales_Growth_%": 75.3},
    {"Submarket": "Porter/New Caney West", "Sales_Growth_%": 71.4},
    {"Submarket": "Magnolia/1488 West", "Sales_Growth_%": 55.3},
    {"Submarket": "Fulshear/S. Brookshire/Simonton", "Sales_Growth_%": 45.8}
]

# Abbreviate submarket names to fit 15 character limit
abbrev_map = {
    "Brookshire": "Brookshire",
    "Waller": "Waller", 
    "Conroe Northwest": "Conroe NW",
    "Porter/New Caney West": "Porter/NC W",
    "Magnolia/1488 West": "Magnolia/1488",
    "Fulshear/S. Brookshire/Simonton": "Fulshear/SB"
}

df = pd.DataFrame(data)
df["Submarket_Short"] = df["Submarket"].map(abbrev_map)

# Sort descending by growth rate (highest first)
df = df.sort_values("Sales_Growth_%", ascending=True)  # ascending=True for horizontal bars puts highest at top

# Create horizontal bar chart
fig = go.Figure(go.Bar(
    x=df['Sales_Growth_%'],
    y=df['Submarket_Short'],
    orientation='h',
    marker_color='#1FB8CD',
    text=[f"{val}%" for val in df['Sales_Growth_%']],
    textposition='outside',
    cliponaxis=False,
    hovertemplate="%{y}<br>%{x}%<extra></extra>"
))

# Update layout
fig.update_layout(
    title="Houston's Top Growth Submarkets Q3 2024",
    xaxis_title="Sales Growth %",
    yaxis_title="Submarket"
)

# Save the chart
fig.write_image("houston_submarkets_growth_chart.png")