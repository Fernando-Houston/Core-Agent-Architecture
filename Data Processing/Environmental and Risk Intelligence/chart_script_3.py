import plotly.graph_objects as go
import json

# Load the data
data = {"ozone_improvement": [{"year": "2000", "days_above_standard": 70, "status": "Baseline"}, {"year": "2018", "days_above_standard": 25, "status": "Improved"}]}

# Extract data for the chart
years = [item["year"] for item in data["ozone_improvement"]]
days = [item["days_above_standard"] for item in data["ozone_improvement"]]
status = [item["status"] for item in data["ozone_improvement"]]

# Create colors based on status - using brand colors for contrast
colors = ['#B4413C', '#ECEBD5']  # Red for baseline, light green for improved

# Create the bar chart
fig = go.Figure(data=[
    go.Bar(
        x=years,
        y=days,
        marker_color=colors,
        text=days,
        textposition='outside',
        cliponaxis=False,
        name='Days Above EPA Standard'
    )
])

# Update layout
fig.update_layout(
    title='Ozone Quality: 64% Improvement',
    xaxis_title='Year',
    yaxis_title='Days Above EPA',
    showlegend=False
)

# Save the chart
fig.write_image("ozone_improvement_chart.png")