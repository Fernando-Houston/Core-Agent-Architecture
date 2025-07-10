import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Data from the provided JSON
neighborhoods = ["Spring Branch", "Katy", "Katy Heights", "The Woodlands", "Memorial Park", "River Oaks", "Heights", "Montrose"]
median_prices = [485000, 374268, 285105, 640000, 1513500, 2985000, 690000, 809000]

# Create a DataFrame
df = pd.DataFrame({
    'Neighborhood': neighborhoods,
    'Median_Price': median_prices
})

# Define price ranges and assign colors
def assign_color(price):
    if price < 400000:
        return '#1FB8CD'  # Strong cyan
    elif price < 600000:
        return '#FFC185'  # Light orange
    elif price < 800000:
        return '#ECEBD5'  # Light green
    elif price < 1000000:
        return '#5D878F'  # Cyan
    else:
        return '#D2BA4C'  # Moderate yellow

# Add color column
df['Color'] = df['Median_Price'].apply(assign_color)

# Create the bar chart
fig = go.Figure(data=[
    go.Bar(
        x=df['Neighborhood'],
        y=df['Median_Price'],
        marker_color=df['Color'],
        cliponaxis=False,
        hovertemplate='<b>%{x}</b><br>Price: $%{y:,.0f}<extra></extra>'
    )
])

# Format y-axis to show abbreviated numbers
fig.update_yaxes(
    title="Median Price",
    tickformat=".2s",
    ticksuffix=""
)

# Update x-axis
fig.update_xaxes(
    title="Neighborhood",
    tickangle=45
)

# Update layout
fig.update_layout(
    title="Houston Home Prices 2024",
    showlegend=False
)

# Save the chart
fig.write_image("houston_home_prices.png")