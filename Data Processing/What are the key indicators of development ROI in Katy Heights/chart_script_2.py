import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Create the data from the provided JSON
data = {
    'Year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Price_per_sqft': [65.62, 91.22, 101.78, 120.83, 134.16, 156.91, 172.27, 165.56]
}

df = pd.DataFrame(data)

# Create the line chart
fig = go.Figure()

# Add the main line with markers
fig.add_trace(go.Scatter(
    x=df['Year'],
    y=df['Price_per_sqft'],
    mode='lines+markers',
    name='Price/sqft',
    line=dict(color='#1FB8CD', width=3),
    marker=dict(color='#1FB8CD', size=8),
    hovertemplate='Year: %{x}<br>Price: $%{y:.2f}/sqft<extra></extra>',
    cliponaxis=False
))

# Add trend line (simple linear regression)
x_vals = np.array(df['Year'])
y_vals = np.array(df['Price_per_sqft'])
z = np.polyfit(x_vals, y_vals, 1)
p = np.poly1d(z)
trend_y = p(x_vals)

fig.add_trace(go.Scatter(
    x=df['Year'],
    y=trend_y,
    mode='lines',
    name='Trend Line',
    line=dict(color='#FFC185', width=2, dash='dash'),
    hoverinfo='skip',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Katy Heights ROI Indicators',
    xaxis_title='Year',
    yaxis_title='Price per sqft',
    showlegend=True,
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update axes with grid lines
fig.update_xaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='rgba(128,128,128,0.2)',
    dtick=1
)

fig.update_yaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='rgba(128,128,128,0.2)',
    tickformat='$,.0f'
)

# Save the chart
fig.write_image('katy_heights_roi_chart.png')