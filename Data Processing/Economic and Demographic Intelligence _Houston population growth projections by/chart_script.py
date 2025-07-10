import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_csv("houston_population_growth_by_area.csv")

# Sort by growth rate in descending order
df = df.sort_values('Growth_Rate_2020_2025', ascending=True)  # ascending=True for horizontal bar to show highest at top

# Create color mapping based on growth rate ranges
def get_color(rate):
    if rate > 10:
        return '#ECEBD5'  # Light green for high growth
    elif rate >= 5:
        return '#D2BA4C'  # Moderate yellow for moderate growth
    else:
        return '#B4413C'  # Moderate red for low growth

# Apply color mapping
df['color'] = df['Growth_Rate_2020_2025'].apply(get_color)

# Create horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df['Growth_Rate_2020_2025'],
    y=df['Area'],
    orientation='h',
    marker_color=df['color'],
    hovertemplate='<b>%{y}</b><br>Growth Rate: %{x}%<extra></extra>',
    cliponaxis=False,
    text=[f"{rate}%" for rate in df['Growth_Rate_2020_2025']],
    textposition='outside'
))

# Update layout
fig.update_layout(
    title="Houston Pop Growth by Area (2020-25)",
    xaxis_title="Growth Rate (%)",
    yaxis_title="Area",
    showlegend=False
)

# Save the chart
fig.write_image("houston_population_growth_chart.png")