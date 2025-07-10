import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

# Load the data
data = {
    "timeline_data": [
        {"year": 2018, "event": "Harris County voters approve $2.5 billion flood control bonds", "category": "Flood Control"},
        {"year": 2021, "event": "Gulf Coast Protection District created", "category": "Coastal Protection"},
        {"year": 2021, "event": "Climate Action Plan development begins", "category": "Climate Action"},
        {"year": 2022, "event": "Coastal Texas Project authorized by Congress", "category": "Coastal Protection"},
        {"year": 2023, "event": "Climate Action Plan approved (40% GHG reduction by 2030)", "category": "Climate Action"},
        {"year": 2024, "event": "FEMA flood maps delayed to 2025", "category": "Flood Control"},
        {"year": 2024, "event": "Harris County files TCEQ petition for stricter air standards", "category": "Air Quality"},
        {"year": 2024, "event": "$249.7M Solar for All grant awarded", "category": "Climate Action"},
        {"year": 2024, "event": "PM2.5 standards lowered to 9.0 µg/m³", "category": "Air Quality"},
        {"year": 2025, "event": "New FEMA flood maps expected", "category": "Flood Control"},
        {"year": 2025, "event": "Coastal Texas Project design work begins", "category": "Coastal Protection"}
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data['timeline_data'])

# Color mapping using the specified colors
color_map = {
    "Flood Control": "#1FB8CD",
    "Coastal Protection": "#FFC185", 
    "Climate Action": "#ECEBD5",
    "Air Quality": "#5D878F"
}

# Create better abbreviated event descriptions for display (15 char limit)
def smart_abbreviate(text, max_len=15):
    # Key abbreviations that maintain meaning
    key_terms = {
        "$2.5 billion flood control bonds": "$2.5B bonds",
        "Gulf Coast Protection District created": "GC Dist created",
        "Climate Action Plan development begins": "CAP dev begins",
        "Coastal Texas Project authorized by Congress": "Coast TX auth",
        "Climate Action Plan approved (40% GHG reduction by 2030)": "CAP approved",
        "FEMA flood maps delayed to 2025": "FEMA delay 2025",
        "Harris County files TCEQ petition for stricter air standards": "TCEQ petition",
        "$249.7M Solar for All grant awarded": "$249.7M solar",
        "PM2.5 standards lowered to 9.0 µg/m³": "PM2.5 to 9.0",
        "New FEMA flood maps expected": "New FEMA maps",
        "Coastal Texas Project design work begins": "Coast TX design"
    }
    
    return key_terms.get(text, text[:max_len])

df['display_text'] = df['event'].apply(smart_abbreviate)

# Create positioning system that handles multiple events per year
def create_positions(df):
    positions = []
    year_counts = df['year'].value_counts().to_dict()
    year_indices = {}
    
    for _, row in df.iterrows():
        year = row['year']
        if year not in year_indices:
            year_indices[year] = 0
        
        # Calculate vertical offset for multiple events in same year
        if year_counts[year] > 1:
            # Spread events vertically around the year baseline
            offset = (year_indices[year] - (year_counts[year] - 1) / 2) * 0.3
        else:
            offset = 0
            
        positions.append(offset)
        year_indices[year] += 1
    
    return positions

df['y_pos'] = create_positions(df)

# Create the timeline chart
fig = go.Figure()

# Add a baseline timeline
fig.add_trace(go.Scatter(
    x=[2018, 2025],
    y=[0, 0],
    mode='lines',
    line=dict(color='lightgray', width=2),
    showlegend=False,
    hoverinfo='skip'
))

# Add points for each category
for category in df['category'].unique():
    category_data = df[df['category'] == category]
    
    fig.add_trace(go.Scatter(
        x=category_data['year'],
        y=category_data['y_pos'],
        mode='markers+text',
        marker=dict(
            size=18,
            color=color_map[category],
            line=dict(width=2, color='white')
        ),
        text=category_data['display_text'],
        textposition='middle right',
        textfont=dict(size=10),
        name=category,
        hovertemplate='<b>%{customdata}</b><br>Year: %{x}<br>Category: ' + category + '<extra></extra>',
        customdata=category_data['event'],
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title="Harris County Environmental Timeline",
    xaxis_title="Year",
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    showlegend=True,
    yaxis_visible=False
)

# Update axes
fig.update_xaxes(
    tickmode='linear',
    tick0=2018,
    dtick=1,
    range=[2017.5, 2025.5]
)

fig.update_yaxes(
    range=[-1.5, 1.5],
    zeroline=False
)

# Save the chart
fig.write_image("harris_county_timeline.png")