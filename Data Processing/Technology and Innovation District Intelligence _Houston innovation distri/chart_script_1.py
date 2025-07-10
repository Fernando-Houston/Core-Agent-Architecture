import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Create the data with units in the labels
workforce_data = [
    {"Metric": "Tech Workers", "Value": 230800, "Category": "Workforce", "Unit": "workers"},
    {"Metric": "Tech Firms", "Value": 9100, "Category": "Workforce", "Unit": "firms"},
    {"Metric": "Venture Startups", "Value": 1000, "Category": "Workforce", "Unit": "startups"}
]

innovation_data = [
    {"Metric": "Tech Patents", "Value": 8691, "Category": "Innovation", "Unit": "patents"},
    {"Metric": "VC Funding", "Value": 2040, "Category": "Innovation", "Unit": "$M"}
]

infrastructure_data = [
    {"Metric": "Ion District", "Value": 16, "Category": "Infrastructure", "Unit": "acres"},
    {"Metric": "TMC Helix Park", "Value": 37, "Category": "Infrastructure", "Unit": "acres"},
    {"Metric": "Energy Corridor", "Value": 25, "Category": "Infrastructure", "Unit": "M sq ft"}
]

# Combine all data
all_data = workforce_data + innovation_data + infrastructure_data
df = pd.DataFrame(all_data)

# Create formatted values for display with units
def format_value_with_unit(value, unit):
    if value >= 1000000:
        return f"{value/1000000:.1f}m {unit}"
    elif value >= 1000:
        return f"{value/1000:.1f}k {unit}"
    else:
        return f"{value} {unit}"

df['Formatted_Value'] = df.apply(lambda row: format_value_with_unit(row['Value'], row['Unit']), axis=1)

# Define colors for each category
color_map = {
    'Workforce': '#1FB8CD',
    'Innovation': '#FFC185', 
    'Infrastructure': '#ECEBD5'
}

# Create the bar chart
fig = go.Figure()

for category in df['Category'].unique():
    category_data = df[df['Category'] == category]
    fig.add_trace(go.Bar(
        x=category_data['Metric'],
        y=category_data['Value'],
        name=category,
        marker_color=color_map[category],
        text=category_data['Formatted_Value'],
        textposition='outside',
        cliponaxis=False
    ))

# Update layout with logarithmic scale
fig.update_layout(
    title="Houston Tech Ecosystem Metrics",
    xaxis_title="Metrics",
    yaxis_title="Value (Log Scale)",
    barmode='group',
    yaxis_type="log",
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    )
)

# Update axes
fig.update_xaxes(tickangle=45)

# Save the chart
fig.write_image("houston_tech_ecosystem.png")