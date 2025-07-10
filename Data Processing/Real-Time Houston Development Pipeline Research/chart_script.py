import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Data from the provided JSON
data = [
    {"project": "Terminal B Transformation", "investment": 2.55, "unit": "billion"},
    {"project": "George R. Brown Convention Center", "investment": 2.0, "unit": "billion"},
    {"project": "Harris Health LBJ Hospital", "investment": 1.6, "unit": "billion"},
    {"project": "IAH Terminal Redevelopment", "investment": 1.46, "unit": "billion"},
    {"project": "Park Eight Place", "investment": 1.0, "unit": "billion"},
    {"project": "Buffalo Bayou East", "investment": 310, "unit": "million"},
    {"project": "Houston Methodist West Hospital", "investment": 247, "unit": "million"},
    {"project": "HCA North Cypress", "investment": 100, "unit": "million"},
    {"project": "Galleria Renovations", "investment": 50, "unit": "million"},
    {"project": "Main Street Promenade", "investment": 12, "unit": "million"}
]

# Convert to DataFrame and normalize to billions
df = pd.DataFrame(data)
df['investment_billions'] = df.apply(lambda x: x['investment'] if x['unit'] == 'billion' else x['investment']/1000, axis=1)

# Abbreviate project names to fit 15 character limit
df['project_abbrev'] = [
    'Terminal B',
    'Convention Ctr',
    'LBJ Hospital',
    'IAH Terminal',
    'Park Eight',
    'Buffalo Bayou',
    'Methodist West',
    'HCA N Cypress',
    'Galleria Reno',
    'Main St Prom'
]

# Sort by investment amount (descending)
df = df.sort_values('investment_billions', ascending=True)  # ascending=True for horizontal bars

# Create brand colors
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C', '#B4413C', '#964325', '#944454', '#13343B', '#DB4545']

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        y=df['project_abbrev'],
        x=df['investment_billions'],
        orientation='h',
        marker_color=colors[:len(df)],
        text=[f'${x:.2f}b' if x >= 1 else f'${x*1000:.0f}m' for x in df['investment_billions']],
        textposition='outside',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title='Houston Dev Projects 2024-25',
    xaxis_title='Investment ($b)',
    yaxis_title='Projects',
    showlegend=False
)

# Save the chart
fig.write_image('houston_development_projects.png')