import plotly.graph_objects as go

# Load the data
data = {
    "timeline_data": [
        {"year": 2001, "technology": "TSARP with LiDAR", "description": "Tropical Storm Allison Recovery Project uses LiDAR technology", "category": "mapping"},
        {"year": 2007, "technology": "FEMA Flood Maps", "description": "Adoption of comprehensive flood maps", "category": "mapping"},
        {"year": 2017, "technology": "Hurricane Harvey", "description": "Catalyst for advanced flood risk assessment", "category": "event"},
        {"year": 2018, "technology": "MAAPnext Project", "description": "Comprehensive flood hazard assessment initiative", "category": "assessment"},
        {"year": 2019, "technology": "AI Radar Sensors", "description": "Deployment of 54 AI-enhanced radar discharge sensors", "category": "sensors"},
        {"year": 2020, "technology": "FIRST System", "description": "Flood Information & Response System for Houston", "category": "ai_ml"},
        {"year": 2021, "technology": "FloodGNN", "description": "Graph neural network flood prediction model", "category": "ai_ml"},
        {"year": 2022, "technology": "MaxFloodCast", "description": "Machine learning model for flood depth prediction", "category": "ai_ml"},
        {"year": 2023, "technology": "Quantum Computing", "description": "Research into quantum flood prediction algorithms", "category": "emerging"},
        {"year": 2024, "technology": "FEMA AI Automation", "description": "AI-driven flood map automation initiatives", "category": "ai_ml"},
        {"year": 2025, "technology": "Updated Flood Maps", "description": "Release of comprehensive updated flood maps", "category": "mapping"}
    ]
}

# Define colors for categories
color_map = {
    "mapping": "#1FB8CD",
    "event": "#FFC185", 
    "assessment": "#ECEBD5",
    "sensors": "#5D878F",
    "ai_ml": "#D2BA4C",
    "emerging": "#B4413C"
}

# Abbreviate technology names to fit 15 character limit
tech_names = {
    "TSARP with LiDAR": "TSARP LiDAR",
    "FEMA Flood Maps": "FEMA Maps",
    "Hurricane Harvey": "Harvey Impact",
    "MAAPnext Project": "MAAPnext",
    "AI Radar Sensors": "AI Radar",
    "FIRST System": "FIRST System",
    "FloodGNN": "FloodGNN",
    "MaxFloodCast": "MaxFloodCast",
    "Quantum Computing": "Quantum Tech",
    "FEMA AI Automation": "FEMA AI Auto",
    "Updated Flood Maps": "Updated Maps"
}

# Create the timeline chart
fig = go.Figure()

# Add main timeline line
fig.add_trace(go.Scatter(
    x=[2000, 2026],
    y=[0, 0],
    mode='lines',
    line=dict(color='lightgray', width=4),
    showlegend=False,
    hoverinfo='skip'
))

# Add timeline markers and connecting lines
for i, item in enumerate(data["timeline_data"]):
    y_pos = 0.4 if i % 2 == 0 else -0.4  # Alternate above and below timeline
    
    # Add connecting line from timeline to marker
    fig.add_trace(go.Scatter(
        x=[item["year"], item["year"]],
        y=[0, y_pos],
        mode='lines',
        line=dict(color=color_map[item["category"]], width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add marker with text
    fig.add_trace(go.Scatter(
        x=[item["year"]],
        y=[y_pos],
        mode='markers+text',
        marker=dict(
            size=14,
            color=color_map[item["category"]],
            line=dict(width=2, color='white')
        ),
        text=tech_names[item["technology"]],
        textposition="top center" if y_pos > 0 else "bottom center",
        textfont=dict(size=10),
        showlegend=False,
        hovertemplate=f"<b>{item['technology']}</b><br>" +
                     f"Year: {item['year']}<br>" +
                     f"Category: {item['category'].replace('_', ' ').title()}<br>" +
                     f"{item['description']}<extra></extra>"
    ))

# Update layout
fig.update_layout(
    title="Harris County Flood Tech Evolution",
    xaxis_title="Year",
    yaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[-0.7, 0.7]
    ),
    xaxis=dict(
        range=[1999, 2027],
        tickmode='linear',
        dtick=2,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1
    ),
    showlegend=False,
    plot_bgcolor='white'
)

# Save the chart
fig.write_image("flood_tech_timeline.png")