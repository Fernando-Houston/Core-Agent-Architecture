import plotly.graph_objects as go
import plotly.express as px
import json

# Data from provided JSON
data = {
    "lending_rates": {
        "2022": {"multifamily_large": 3.5, "multifamily_small": 4.0, "retail": 4.2, "office": 4.2, "industrial": 4.2, "bridge": 7.0},
        "2023": {"multifamily_large": 6.0, "multifamily_small": 6.5, "retail": 6.8, "office": 6.8, "industrial": 6.8, "bridge": 8.5},
        "2024": {"multifamily_large": 5.8, "multifamily_small": 6.2, "retail": 6.6, "office": 6.6, "industrial": 6.6, "bridge": 8.8},
        "2025": {"multifamily_large": 5.34, "multifamily_small": 5.80, "retail": 6.38, "office": 6.38, "industrial": 6.38, "bridge": 9.00}
    }
}

# Extract years and create traces
years = [2022, 2023, 2024, 2025]
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C', '#B4413C']

# Create figure
fig = go.Figure()

# Property types and their labels (shortened to 15 chars)
property_types = [
    ('multifamily_large', 'Multifam >$6M'),
    ('multifamily_small', 'Multifam <$6M'),
    ('retail', 'Retail'),
    ('office', 'Office'),
    ('industrial', 'Industrial'),
    ('bridge', 'Bridge Loans')
]

# Add traces for each property type
for i, (prop_type, label) in enumerate(property_types):
    rates = [data['lending_rates'][str(year)][prop_type] for year in years]
    
    # Create hover text that includes impact data for 2025
    hover_text = []
    for j, year in enumerate(years):
        if year == 2025:
            if prop_type == 'multifamily_large':
                hover_text.append(f'<b>{label}</b><br>Year: {year}<br>Rate: {rates[j]:.2f}%<br>Property +0.8%<br>$957b loans due')
            elif prop_type == 'office':
                hover_text.append(f'<b>{label}</b><br>Year: {year}<br>Rate: {rates[j]:.2f}%<br>Property -7.7%<br>Vol. down 40%')
            elif prop_type == 'industrial':
                hover_text.append(f'<b>{label}</b><br>Year: {year}<br>Rate: {rates[j]:.2f}%<br>Construction -50%<br>Vol. down 40%')
            else:
                hover_text.append(f'<b>{label}</b><br>Year: {year}<br>Rate: {rates[j]:.2f}%<br>Vol. down 40%')
        else:
            hover_text.append(f'<b>{label}</b><br>Year: {year}<br>Rate: {rates[j]:.2f}%')
    
    # Different marker sizes for 2025 to emphasize current data
    marker_sizes = [8 if year != 2025 else 12 for year in years]
    
    fig.add_trace(go.Scatter(
        x=years,
        y=rates,
        mode='lines+markers',
        name=label,
        line=dict(color=colors[i], width=3),
        marker=dict(size=marker_sizes, color=colors[i], symbol='circle'),
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title='Harris County Commercial Lending Rates',
    xaxis_title='Year',
    yaxis_title='Interest Rate (%)',
    hovermode='closest',
    legend=dict(
        orientation='v',
        yanchor='top',
        y=0.98,
        xanchor='left',
        x=1.02
    )
)

# Update axes
fig.update_xaxes(
    tickmode='linear',
    dtick=1,
    range=[2021.5, 2025.5]
)

fig.update_yaxes(
    ticksuffix='%',
    range=[0, 10]
)

# Save the chart
fig.write_image('harris_county_lending_rates.png')