import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
import pandas as pd

# Data from the provided JSON
spring_branch_prices = [415000, 485000]
spring_branch_dates = ["June 2024", "June 2025"]
katy_heights_price = [285105]
katy_heights_date = ["2024"]

# Convert dates to datetime for proper plotting
spring_branch_datetime = [datetime.strptime(date, "%B %Y") for date in spring_branch_dates]
katy_heights_datetime = [datetime.strptime("June 2024", "%B %Y")]  # Using June 2024 as reference point

# Create the figure
fig = go.Figure()

# Add Spring Branch line
fig.add_trace(go.Scatter(
    x=spring_branch_datetime,
    y=[price/1000 for price in spring_branch_prices],  # Convert to thousands for better readability
    mode='lines+markers',
    name='Spring Branch',
    line=dict(color='#1FB8CD', width=3),
    marker=dict(size=8),
    hovertemplate='<b>Spring Branch</b><br>' +
                  'Date: %{x|%b %Y}<br>' +
                  'Median Price: $%{y:.0f}k<extra></extra>',
    cliponaxis=False
))

# Add Katy Heights point
fig.add_trace(go.Scatter(
    x=katy_heights_datetime,
    y=[katy_heights_price[0]/1000],
    mode='markers',
    name='Katy Heights',
    marker=dict(color='#FFC185', size=10),
    hovertemplate='<b>Katy Heights</b><br>' +
                  'Date: %{x|%b %Y}<br>' +
                  'Median Price: $%{y:.0f}k<extra></extra>',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Harris County Market Performance',
    xaxis_title='Date',
    yaxis_title='Median Price ($k)',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    hovermode='closest'
)

# Update axes
fig.update_xaxes(
    tickformat='%b %Y'
)

fig.update_yaxes(
    tickformat='$,.0f'
)

# Save the chart
fig.write_image("harris_county_market_performance.png")
fig.show()