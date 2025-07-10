import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Load data
df = pd.read_csv('houston_stem_pipeline.csv')

# Abbreviate stage names to <=15 characters
name_map = {
    'K-12 STEM Programs': 'K12 STEM',
    'Community College STEM': 'Com Coll STEM',
    'University STEM Undergrad': 'Uni STEM UG',
    'University STEM Graduate': 'Uni STEM Grad',
    'Industry Training Programs': 'Ind Train Prog',
    'Workforce Development': 'Work Dev'
}
df['Stage'] = df['Education_Level'].map(name_map).fillna(df['Education_Level'])

# Create subplot with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add bar trace for students served (primary y-axis)
fig.add_trace(
    go.Bar(
        x=df['Stage'],
        y=df['Students_Served'],
        name='Students (k)',
        marker_color='#1FB8CD',
        text=[f"{emp:.0%}" if not pd.isna(emp) else "" for emp in df['Employment_Rate']],
        textposition='outside',
        textfont=dict(size=10)
    ),
    secondary_y=False,
)

# Add line trace for investment (secondary y-axis)
fig.add_trace(
    go.Scatter(
        x=df['Stage'],
        y=df['Annual_Investment_Millions'],
        mode='lines+markers',
        name='Investment ($M)',
        marker_color='#FFC185',
        line=dict(color='#FFC185', width=3),
        marker=dict(size=8)
    ),
    secondary_y=True,
)

# Update layout
fig.update_layout(
    title='Houston STEM Pipeline Overview',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update axis labels
fig.update_yaxes(title_text="Students (k)", secondary_y=False)
fig.update_yaxes(title_text="Investment ($M)", secondary_y=True)
fig.update_xaxes(title_text="Pipeline Stage")

# Save figure
fig.write_image('houston_stem_pipeline.png')

print("Chart created successfully!")