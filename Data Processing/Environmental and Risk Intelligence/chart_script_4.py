import plotly.express as px
import plotly.graph_objects as go
import json

# Parse the data
data = {"coastal_project_breakdown": [{"component": "Galveston Bay Storm Surge Barrier System", "cost_billions": 31.2, "percentage": 90.75}, {"component": "Coastwide Ecosystem Restoration Plan", "cost_billions": 2.5, "percentage": 7.27}, {"component": "South Padre Island Beach Nourishment", "cost_billions": 0.68, "percentage": 1.98}]}

components = []
costs = []
percentages = []

for item in data["coastal_project_breakdown"]:
    components.append(item["component"])
    costs.append(item["cost_billions"])
    percentages.append(item["percentage"])

# Abbreviate component names to 15 characters or less
abbreviated_names = [
    "Galveston Bay",  # 12 chars
    "Ecosystem Rest",  # 14 chars  
    "Beach Nourish"   # 13 chars
]

# Use blue-ish colors from brand palette, darkest for largest component
# Largest is first (90.75%), so use darkest first
colors = ["#13343B", "#5D878F", "#1FB8CD"]

# Create pie chart
fig = go.Figure(data=[go.Pie(
    labels=abbreviated_names,
    values=costs,
    textinfo='percent',
    textposition='inside',
    marker=dict(colors=colors),
    hovertemplate='<b>%{label}</b><br>' +
                  'Cost: $%{value:.1f}b<br>' +
                  'Percent: %{percent}<br>' +
                  '<extra></extra>'
)])

fig.update_layout(
    title="Coastal Texas Project Cost Breakdown",
    uniformtext_minsize=14, 
    uniformtext_mode='hide'
)

# Save the chart
fig.write_image("coastal_project_pie.png")