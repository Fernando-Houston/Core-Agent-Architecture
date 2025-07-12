import plotly.graph_objects as go

# Data with proper abbreviated labels (<=15 chars)
data = [
    {"Policy": "Pre-2021 Std", "≤1 acre": 0.2, "1-20 acres": 0.2},
    {"Policy": "Post-2021 Min", "≤1 acre": 0.75, "1-20 acres": 0.75},
    {"Policy": "Post-21 Max100", "≤1 acre": 0.75, "1-20 acres": 1.0}
]

policies = [d["Policy"] for d in data]
small = [d["≤1 acre"] for d in data]
large = [d["1-20 acres"] for d in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    name='≤1 acre',
    x=policies,
    y=small,
    marker_color='#1FB8CD',
    cliponaxis=False
))

fig.add_trace(go.Bar(
    name='1-20 acres',
    x=policies,
    y=large,
    marker_color='#FFC185',
    cliponaxis=False
))

fig.update_layout(
    title='Houston Stormwater Detention 2021 Update',
    xaxis_title='Policy Regime',
    yaxis_title='Det Vol ac-ft/ac',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save chart
fig.write_image('houston_stormwater_detention.png')