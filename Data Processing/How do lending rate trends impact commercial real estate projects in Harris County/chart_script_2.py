import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Load the data
data = {
    "year": [2022, 2023, 2024, 2025],
    "fed_funds_rate": [0.25, 5.25, 5.50, 4.50],
    "treasury_10yr": [2.89, 4.05, 4.25, 4.33],
    "lending_volume_index": [100, 75, 65, 85],
    "property_values_index": [100, 108, 102, 104],
    "construction_activity_index": [100, 60, 50, 55],
    "transaction_volume_index": [100, 70, 60, 75]
}

df = pd.DataFrame(data)

# Calculate interest rate spread
df['rate_spread'] = df['treasury_10yr'] - df['fed_funds_rate']

# Create the scatter plot
fig = go.Figure()

# Define colors from the brand palette
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F']

# 1. Fed Funds Rate vs. Commercial Lending Volume
fig.add_trace(go.Scatter(
    x=df['fed_funds_rate'],
    y=df['lending_volume_index'],
    mode='markers+lines',
    name='Fed Rate vs Lending',
    marker=dict(size=8, color=colors[0]),
    line=dict(color=colors[0], width=2),
    hovertemplate='Fed Rate: %{x}%<br>Lending Vol: %{y}<extra></extra>',
    cliponaxis=False
))

# 2. 10-Year Treasury Rate vs. Property Values
fig.add_trace(go.Scatter(
    x=df['treasury_10yr'],
    y=df['property_values_index'],
    mode='markers+lines',
    name='Treasury vs Values',
    marker=dict(size=8, color=colors[1]),
    line=dict(color=colors[1], width=2),
    hovertemplate='Treasury: %{x}%<br>Prop Values: %{y}<extra></extra>',
    cliponaxis=False
))

# 3. Interest Rate Spreads vs. Construction Activity
fig.add_trace(go.Scatter(
    x=df['rate_spread'],
    y=df['construction_activity_index'],
    mode='markers+lines',
    name='Spread vs Constr',
    marker=dict(size=8, color=colors[2]),
    line=dict(color=colors[2], width=2),
    hovertemplate='Rate Spread: %{x}%<br>Construction: %{y}<extra></extra>',
    cliponaxis=False
))

# 4. Fed Funds Rate vs. Transaction Volume (using Fed Rate as proxy for lending rate)
fig.add_trace(go.Scatter(
    x=df['fed_funds_rate'],
    y=df['transaction_volume_index'],
    mode='markers+lines',
    name='Fed Rate vs Trans',
    marker=dict(size=8, color=colors[3]),
    line=dict(color=colors[3], width=2),
    hovertemplate='Fed Rate: %{x}%<br>Trans Vol: %{y}<extra></extra>',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Economic Indicators vs RE Market',
    xaxis_title='Interest Rate (%)',
    yaxis_title='Market Index',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save the chart
fig.write_image('economic_indicators_scatter.png')