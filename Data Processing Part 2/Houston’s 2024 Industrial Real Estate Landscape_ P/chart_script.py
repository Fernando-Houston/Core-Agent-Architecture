import plotly.graph_objects as go
import plotly.io as pio

# Data
years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
teus = [2.18, 2.46, 2.70, 2.987, 2.99, 3.47, 3.975, 3.826, 4.14]

# Create figure
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=years,
    y=teus,
    mode='lines+markers+text',
    line=dict(color='#1FB8CD', width=3),
    marker=dict(size=10, color='#1FB8CD'),
    text=[f'{val:.2f}' for val in teus],
    textposition='top center',
    cliponaxis=False,
    name='TEUs'
))

# Layout updates
fig.update_layout(
    title="Port Houston Container Growth, 2016-2024",
    xaxis_title="Year",
    yaxis_title="Volume (M TEUs)",
    showlegend=False
)

# Save image
file_path = "port_houston_container_growth.png"
fig.write_image(file_path)