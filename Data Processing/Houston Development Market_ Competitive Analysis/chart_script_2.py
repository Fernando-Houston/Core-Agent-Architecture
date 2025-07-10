import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load the data
df = pd.read_csv('houston_residential_activity_by_area_2024.csv')

# Sort by New Home Communities in descending order and take top 10
top_10 = df.nlargest(10, 'New Home Communities')

# Define colors from the brand palette
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C', 
          '#B4413C', '#964325', '#944454', '#13343B', '#DB4545']

# Create horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=top_10['New Home Communities'],
    y=top_10['Area/Region'],
    orientation='h',
    marker_color=colors[:len(top_10)],
    text=top_10['New Home Communities'],
    textposition='outside',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title="Houston Dev Activity by Area (2024)",
    xaxis_title="New Home Comm",
    yaxis_title="Area/Region",
    showlegend=False
)

# Save the chart
fig.write_image("houston_chart.png")
print("Chart saved successfully!")