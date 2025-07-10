import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Data from the provided JSON
data = {
    "zip_codes": ["77493", "77433", "77381", "77382", "77079", "77031", "77479", "77449", "77377"],
    "areas": ["Katy", "Cypress", "The Woodlands", "The Woodlands", "Memorial/Energy Corridor", "Southwest Houston", "Sugar Land", "Katy", "Tomball"],
    "performance_type": ["National Rank", "National Rank", "Appreciation %", "Appreciation %", "Appreciation %", "Appreciation %", "Appreciation %", "National Rank", "Hidden Gem"],
    "performance_value": [1, 2, 8, 8, 8, 7, 7, 20, 5]
}

# Create DataFrame
df = pd.DataFrame(data)

# Create shortened labels for x-axis (ZIP + shortened area names)
area_short = {
    "Katy": "Katy",
    "Cypress": "Cypress", 
    "The Woodlands": "Woodlands",
    "Memorial/Energy Corridor": "Memorial",
    "Southwest Houston": "SW Houston",
    "Sugar Land": "Sugar Land",
    "Tomball": "Tomball"
}

df['area_short'] = df['areas'].map(area_short)
df['x_label'] = df['zip_codes'] + '<br>' + df['area_short']

# Create custom colors based on performance type
color_map = {
    'National Rank': '#1FB8CD',
    'Appreciation %': '#FFC185', 
    'Hidden Gem': '#ECEBD5'
}

df['color'] = df['performance_type'].map(color_map)

# Create hover text
hover_text = []
for i, row in df.iterrows():
    if row['performance_type'] == 'National Rank':
        hover_text.append(f"ZIP: {row['zip_codes']}<br>Area: {row['areas']}<br>Rank: #{row['performance_value']}")
    elif row['performance_type'] == 'Appreciation %':
        hover_text.append(f"ZIP: {row['zip_codes']}<br>Area: {row['areas']}<br>Appreciation: {row['performance_value']}%")
    else:  # Hidden Gem
        hover_text.append(f"ZIP: {row['zip_codes']}<br>Area: {row['areas']}<br>Under: $300k")

# Create the bar chart
fig = go.Figure()

# Add bars for each performance type
for perf_type in df['performance_type'].unique():
    mask = df['performance_type'] == perf_type
    fig.add_trace(go.Bar(
        x=df[mask]['x_label'],
        y=df[mask]['performance_value'],
        name=perf_type,
        marker_color=df[mask]['color'].iloc[0],
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=[hover_text[i] for i in df[mask].index],
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title='Top Houston ZIP Codes 2024',
    xaxis_title='ZIP Code',
    yaxis_title='Performance Value',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    xaxis=dict(tickangle=45)
)

# Save the chart
fig.write_image('houston_zip_performance_2024.png')