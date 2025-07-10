import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Create the data
data = {
    "dates": ["2023-09-01", "2024-01-01", "2025-01-01", "2025-07-07", "2025-09-01", "2026-01-01"],
    "events": ["SB 2038 ETJ Opt-Out", "Houston Building Codes", "Harris County Fire Code", "Houston 30-Day Permitting Pilot", "Texas SB 840 Commercial-to-Residential", "FEMA Flood Maps"],
    "categories": ["State", "Local Houston", "Harris County", "Local Houston", "State", "Federal"],
    "descriptions": ["Allows ETJ opt-out by petition", "2021 International Codes adopted", "2021 Fire Code effective", "30-day permit pilot launched", "Commercial-to-residential by right", "Updated flood maps delayed"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Convert dates to datetime
df['date_obj'] = pd.to_datetime(df['dates'])

# Create better abbreviated event names (keeping under 15 chars but more meaningful)
event_abbrev = {
    "SB 2038 ETJ Opt-Out": "SB 2038 ETJ",
    "Houston Building Codes": "Houston Codes",
    "Harris County Fire Code": "Fire Code",
    "Houston 30-Day Permitting Pilot": "30-Day Permits",
    "Texas SB 840 Commercial-to-Residential": "SB 840 Com-Res",
    "FEMA Flood Maps": "FEMA Maps"
}

df['event_short'] = df['events'].map(event_abbrev)

# Define colors for categories
color_map = {
    'State': '#1FB8CD',        # Strong cyan
    'Local Houston': '#FFC185',  # Light orange
    'Harris County': '#ECEBD5',  # Light green
    'Federal': '#5D878F'       # Cyan
}

# Create vertical positions to stagger markers and avoid overlap
y_positions = [1.3, 0.7, 1.3, 0.7, 1.3, 0.7]
df['y_pos'] = y_positions

# Create the figure
fig = go.Figure()

# Add markers for each event
for category in df['categories'].unique():
    cat_data = df[df['categories'] == category]
    
    fig.add_trace(go.Scatter(
        x=cat_data['date_obj'],
        y=cat_data['y_pos'],
        mode='markers+text',
        marker=dict(
            size=15,
            color=color_map[category],
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        text=cat_data['event_short'],
        textposition='top center',
        name=category,
        hovertemplate='<b>%{customdata[0]}</b><br>' +
                     'Date: %{x}<br>' +
                     'Category: ' + category + '<br>' +
                     'Details: %{customdata[1]}<br>' +
                     '<extra></extra>',
        customdata=list(zip(cat_data['events'], cat_data['descriptions'])),
        cliponaxis=False
    ))

# Add horizontal lines connecting the timeline
fig.add_trace(go.Scatter(
    x=[df['date_obj'].min(), df['date_obj'].max()],
    y=[1, 1],
    mode='lines',
    line=dict(color='lightgray', width=2),
    showlegend=False,
    hoverinfo='skip'
))

# Add vertical lines from timeline to markers
for i, row in df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['date_obj'], row['date_obj']],
        y=[1, row['y_pos']],
        mode='lines',
        line=dict(color='lightgray', width=1, dash='dot'),
        showlegend=False,
        hoverinfo='skip'
    ))

# Update layout
fig.update_layout(
    title='Harris County & Houston Regulatory Timeline',
    xaxis_title='Date',
    yaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[0.3, 1.8]
    ),
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        minor=dict(showgrid=True, gridcolor='lightgray', gridwidth=0.5)
    ),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white'
)

# Save the chart
fig.write_image('regulatory_timeline.png')

print("Chart saved as regulatory_timeline.png")