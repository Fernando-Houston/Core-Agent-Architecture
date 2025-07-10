import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Data from the provided JSON
data = [
    {"date": "2024-01", "initiative": "System Investment", "description": "$15M allocated for HouPermits system", "type": "Technology"},
    {"date": "2024-Q4", "initiative": "Staff Augmentation", "description": "Expanded contractor support for plan reviews", "type": "Staffing"},
    {"date": "2025-Q1", "initiative": "System Implementation", "description": "HouPermits system rollout begins", "type": "Technology"},
    {"date": "2025-Q2", "initiative": "Process Streamlining", "description": "Workflow optimization initiatives", "type": "Process"},
    {"date": "2025-07", "initiative": "30-Day Pilot", "description": "30-day turnaround pilot program launched", "type": "Process"},
    {"date": "2025-Q3", "initiative": "Performance Targets", "description": "New efficiency metrics implemented", "type": "Process"}
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert date strings to actual dates
def convert_date(date_str):
    if 'Q1' in date_str:
        return datetime.strptime(date_str.replace('Q1', '02'), '%Y-%m')
    elif 'Q2' in date_str:
        return datetime.strptime(date_str.replace('Q2', '05'), '%Y-%m')
    elif 'Q3' in date_str:
        return datetime.strptime(date_str.replace('Q3', '08'), '%Y-%m')
    elif 'Q4' in date_str:
        return datetime.strptime(date_str.replace('Q4', '11'), '%Y-%m')
    else:
        return datetime.strptime(date_str, '%Y-%m')

df['date_parsed'] = df['date'].apply(convert_date)

# Define colors and y-positions for each type
color_map = {
    'Technology': '#1FB8CD',
    'Process': '#FFC185', 
    'Staffing': '#ECEBD5'
}

y_positions = {
    'Technology': 3,
    'Process': 2,
    'Staffing': 1
}

# Create the figure
fig = go.Figure()

# Add scatter points for each type
for improvement_type in df['type'].unique():
    type_data = df[df['type'] == improvement_type]
    
    fig.add_trace(go.Scatter(
        x=type_data['date_parsed'],
        y=[y_positions[improvement_type]] * len(type_data),
        mode='markers+text',
        marker=dict(
            size=20,
            color=color_map[improvement_type],
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        text=type_data['initiative'],
        textposition='top center',
        textfont=dict(size=10),
        name=improvement_type,
        hovertemplate='<b>%{text}</b><br>%{customdata}<br>%{x|%b %Y}<extra></extra>',
        customdata=type_data['description'],
        cliponaxis=False
    ))

# Add horizontal timeline line
fig.add_shape(
    type="line",
    x0=df['date_parsed'].min(),
    x1=df['date_parsed'].max(),
    y0=2,
    y1=2,
    line=dict(color="gray", width=2, dash="dot"),
)

# Update layout
fig.update_layout(
    title="Houston Permitting Center Improvements<br><sub>Streamlining Development Process</sub>",
    xaxis_title="Timeline",
    yaxis=dict(
        visible=False,
        range=[0.5, 3.5]
    ),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    )
)

# Update x-axis
fig.update_xaxes(
    tickformat='%b %Y',
    dtick='M2'  # Show every 2 months
)

# Save the chart
fig.write_image("houston_permitting_timeline.png")