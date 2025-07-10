import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Create the data
data = {
    "categories": ["Zoning Laws", "Building Codes", "FEMA Flood Maps", "State Legislation - SB 840", "Permitting Process", "ADU Regulations", "ETJ Opt-Out (SB 2038)", "Fire Code"],
    "2024_status": ["No traditional zoning in Harris County/Houston", "2021 International Codes adopted Jan 1, 2024", "Expected release early 2025", "Not enacted", "Standard multi-month process", "900 sq ft max, 5 ft setbacks", "Active since Sept 2023", "2018 International Fire Code"],
    "2025_updates": ["Continues with subdivision ordinances only", "Same 2021 codes remain in effect", "Delayed until 2026", "Commercial-to-residential by right", "30-day pilot program launched", "No changes to size/setback rules", "Legal challenges ongoing", "2021 Harris County Fire Code adopted"],
    "effective_dates": ["Ongoing", "January 1, 2024", "Delayed to 2026", "September 1, 2025", "July 7, 2025", "Ongoing", "September 1, 2023", "January 1, 2025"],
    "impact_on_development": ["Relies on deed restrictions & subdivision rules", "Enhanced energy efficiency & safety standards", "Uncertainty continues for flood insurance", "Streamlines multifamily development", "Faster single-family permits", "Stable ADU development framework", "Developers can bypass city regulations", "Stricter fire safety requirements"]
}

df = pd.DataFrame(data)

# Create a stacked bar chart showing change status
change_status = []
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C', '#B4413C', '#964325', '#944454']

for i, row in df.iterrows():
    # Determine change type
    if 'No changes' in row['2025_updates'] or 'Same' in row['2025_updates'] or 'Continues' in row['2025_updates']:
        status = 'No Change'
    elif 'Delayed' in row['2025_updates']:
        status = 'Delayed'
    elif 'Legal challenges' in row['2025_updates']:
        status = 'Under Review'
    else:
        status = 'Updated'
    
    # Abbreviate category names
    category_short = row['categories']
    if len(category_short) > 15:
        if 'State Legislation' in category_short:
            category_short = 'SB 840'
        elif 'Building Codes' in category_short:
            category_short = 'Build Codes'
        elif 'Permitting Process' in category_short:
            category_short = 'Permits'
        elif 'ETJ Opt-Out' in category_short:
            category_short = 'ETJ Opt-Out'
        elif 'Fire Code' in category_short:
            category_short = 'Fire Code'
        elif 'FEMA Flood Maps' in category_short:
            category_short = 'Flood Maps'
        elif 'ADU Regulations' in category_short:
            category_short = 'ADU Rules'
        elif 'Zoning Laws' in category_short:
            category_short = 'Zoning'
    
    change_status.append({
        'Category': category_short,
        'Status': status,
        'Date': row['effective_dates'],
        'Impact': row['impact_on_development'][:40] + '...' if len(row['impact_on_development']) > 40 else row['impact_on_development']
    })

change_df = pd.DataFrame(change_status)

# Create the figure
fig = go.Figure()

# Define status colors
status_colors = {
    'Updated': '#1FB8CD',
    'No Change': '#ECEBD5', 
    'Delayed': '#FFC185',
    'Under Review': '#5D878F'
}

# Add bars for each status type
for status in ['Updated', 'No Change', 'Delayed', 'Under Review']:
    status_data = change_df[change_df['Status'] == status]
    if not status_data.empty:
        fig.add_trace(go.Bar(
            name=status,
            x=status_data['Category'],
            y=[1] * len(status_data),
            marker_color=status_colors[status],
            hovertemplate='<b>%{x}</b><br>' +
                         'Status: ' + status + '<br>' +
                         'Date: %{customdata[0]}<br>' +
                         'Impact: %{customdata[1]}<br>' +
                         '<extra></extra>',
            customdata=list(zip(status_data['Date'], status_data['Impact']))
        ))

# Update layout
fig.update_layout(
    title='Harris County Regulatory Changes',
    xaxis_title='Regulation',
    yaxis_title='Status',
    barmode='stack',
    hovermode='closest',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    showlegend=True
)

# Update axes
fig.update_xaxes(tickangle=45)
fig.update_yaxes(showticklabels=False)

# Save the chart
fig.write_image('regulatory_changes.png')