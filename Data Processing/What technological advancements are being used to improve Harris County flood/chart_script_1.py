import plotly.graph_objects as go
import json

# Data from the provided JSON
data = {
    "categories": [
        {"category": "Real-time Monitoring", "systems": [
            {"name": "Flood Warning Stations", "count": 139},
            {"name": "AI-Enhanced Radar Sensors", "count": 54},
            {"name": "Automated Alert Systems", "count": 2}
        ]},
        {"category": "AI/Machine Learning", "systems": [
            {"name": "ML Models", "count": 5},
            {"name": "Predictive Systems", "count": 2},
            {"name": "Quantum Computing Research", "count": 1}
        ]},
        {"category": "Advanced Mapping", "systems": [
            {"name": "LiDAR Datasets", "count": 3},
            {"name": "Digital Elevation Models", "count": 2},
            {"name": "Comprehensive Map Updates", "count": 1}
        ]},
        {"category": "Data Analytics", "systems": [
            {"name": "Digital Twin Projects", "count": 1},
            {"name": "Blockchain Security Systems", "count": 1},
            {"name": "Data Fusion Frameworks", "count": 3}
        ]}
    ]
}

# Prepare data for grouped bar chart
fig = go.Figure()

# Colors for each category
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F']

# Create all x-axis labels and corresponding y values
x_labels = []
y_values = []
bar_colors = []
category_names = []

for i, cat_data in enumerate(data['categories']):
    # Abbreviate category names within 15 character limit
    if cat_data['category'] == 'Real-time Monitoring':
        cat_name = 'Realtime Mon'
    elif cat_data['category'] == 'AI/Machine Learning':
        cat_name = 'AI/ML Apps'
    elif cat_data['category'] == 'Advanced Mapping':
        cat_name = 'Adv Mapping'
    elif cat_data['category'] == 'Data Analytics':
        cat_name = 'Data Analytics'
    
    category_names.append(cat_name)
    
    for system in cat_data['systems']:
        # Abbreviate system names within 15 character limit
        system_name = system['name']
        if len(system_name) > 15:
            if 'Flood Warning' in system_name:
                system_name = 'Flood Warn Stn'
            elif 'AI-Enhanced' in system_name:
                system_name = 'AI Radar Sens'
            elif 'Automated Alert' in system_name:
                system_name = 'Auto Alert Sys'
            elif 'Digital Elevation' in system_name:
                system_name = 'Digital Elev'
            elif 'Comprehensive Map' in system_name:
                system_name = 'Map Updates'
            elif 'Digital Twin' in system_name:
                system_name = 'Digital Twin'
            elif 'Blockchain Security' in system_name:
                system_name = 'Blockchain Sec'
            elif 'Data Fusion' in system_name:
                system_name = 'Data Fusion'
            elif 'Quantum Computing' in system_name:
                system_name = 'Quantum Comp'
            elif 'Predictive Systems' in system_name:
                system_name = 'Predictive Sys'
        
        x_labels.append(system_name)
        y_values.append(system['count'])
        bar_colors.append(colors[i])

# Create the grouped bar chart
fig.add_trace(go.Bar(
    x=x_labels,
    y=y_values,
    marker_color=bar_colors,
    text=y_values,
    textposition='outside',
    cliponaxis=False,
    showlegend=False
))

# Add category traces for legend
for i, (cat_name, color) in enumerate(zip(category_names, colors)):
    fig.add_trace(go.Bar(
        x=[None],
        y=[None],
        marker_color=color,
        name=cat_name,
        showlegend=True
    ))

# Update layout
fig.update_layout(
    title='Harris County Flood Tech Systems',
    xaxis_title='Tech Systems',
    yaxis_title='Count',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save the chart
fig.write_image('harris_county_flood_tech_chart.png')