import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create the data
data = [
    {"area": "Downtown", "x": 0, "y": 0, "projects": 3, "type": "Mixed-Use", "investment": 2012},
    {"area": "Medical Center", "x": -2, "y": -1, "projects": 3, "type": "Healthcare", "investment": 1947},
    {"area": "Energy Corridor", "x": -4, "y": 0, "projects": 2, "type": "Mixed-Use", "investment": 1000},
    {"area": "Airport/North", "x": 3, "y": 2, "projects": 2, "type": "Transportation", "investment": 4010},
    {"area": "East End", "x": 2, "y": -1, "projects": 2, "type": "Parks/Recreation", "investment": 310},
    {"area": "Galleria/Uptown", "x": -1, "y": 1, "projects": 2, "type": "Retail", "investment": 50},
    {"area": "Northwest", "x": -2, "y": 2, "projects": 2, "type": "Healthcare", "investment": 100},
    {"area": "Heights", "x": -1, "y": 0, "projects": 1, "type": "Mixed-Use", "investment": 25}
]

df = pd.DataFrame(data)

# Define color mapping for development types
color_map = {
    "Mixed-Use": "#1FB8CD",
    "Healthcare": "#FFC185", 
    "Transportation": "#ECEBD5",
    "Parks/Recreation": "#5D878F",
    "Retail": "#D2BA4C"
}

# Create the scatter plot
fig = px.scatter(
    df, 
    x="x", 
    y="y", 
    size="projects",
    color="type",
    color_discrete_map=color_map,
    hover_data={"area": True, "projects": True, "investment": True, "x": False, "y": False},
    title="Houston Development Projects by Area"
)

# Update traces to customize hover template and set cliponaxis
fig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>" +
                  "Projects: %{customdata[1]}<br>" +
                  "Investment: $%{customdata[2]}m<br>" +
                  "<extra></extra>",
    customdata=df[["area", "projects", "investment"]].values,
    cliponaxis=False
)

# Update layout with legend positioning (5 or fewer items, so center under title)
fig.update_layout(
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    xaxis_title="West ← → East",
    yaxis_title="South ← → North"
)

# Save the chart
fig.write_image("houston_development_scatter.png")