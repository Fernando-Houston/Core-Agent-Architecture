import plotly.graph_objects as go

# Data for Land Banking vs Direct Purchase pie chart
strategies = ["Land Banking/Options", "Direct Purchase", "Joint Ventures"]
percentages = [60, 25, 15]

# Create pie chart with brand colors
colors = ['#1FB8CD', '#FFC185', '#ECEBD5']

fig = go.Figure(data=[go.Pie(
    labels=strategies,
    values=percentages,
    marker=dict(colors=colors),
    textinfo='label+percent',
    hovertemplate='<b>%{label}</b><br>%{percent}<br>%{value}%<extra></extra>'
)])

# Update layout for pie chart
fig.update_layout(
    title='Land Acquisition Strategy Distribution',
    uniformtext_minsize=14, 
    uniformtext_mode='hide'
)

# Save the chart
fig.write_image("houston_acquisition_strategy.png")