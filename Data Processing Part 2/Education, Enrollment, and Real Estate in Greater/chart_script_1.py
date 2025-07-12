import plotly.graph_objects as go
import pandas as pd

# Data for the chart
data = [
    {"Project":"Freshman Residence Hall","Cost":179},
    {"Project":"Medical Research Building","Cost":78},
    {"Project":"Engineering Tech Building (Sugar Land)","Cost":65},
    {"Project":"Dining Commons","Cost":64},
    {"Project":"Centennial Walkway & Grove","Cost":43}
]

# Create DataFrame and sort by cost (highest to lowest)
df = pd.DataFrame(data)
df = df.sort_values('Cost', ascending=False)

# Abbreviate project names to fit character limit
project_names = []
for project in df['Project']:
    if len(project) > 15:
        if "Residence Hall" in project:
            project_names.append("Freshman Res")
        elif "Research Building" in project:
            project_names.append("Medical Res")
        elif "Engineering Tech" in project:
            project_names.append("Engineering")
        elif "Dining Commons" in project:
            project_names.append("Dining")
        elif "Centennial" in project:
            project_names.append("Centennial")
    else:
        project_names.append(project)

# Create the bar chart
fig = go.Figure(data=[
    go.Bar(
        x=project_names,
        y=df['Cost'],
        marker_color='#C8102E',  # UH red color
        text=[f"${cost}M" for cost in df['Cost']],
        textposition='outside',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title="Major UH Capital Projects 2024-2027",
    xaxis_title="Project",
    yaxis_title="Cost (M)",
    showlegend=False
)

# Save the chart
fig.write_image("uh_capital_projects_chart.png")