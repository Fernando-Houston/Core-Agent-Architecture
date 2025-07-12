import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

# Data
data = [
    {"Project":"San Jacinto Marketplace (Baytown)","Retail_SF":500},
    {"Project":"East Blocks Phase 1 (EaDo)","Retail_SF":196},
    {"Project":"Astros Entertainment District (Downtown)","Retail_SF":60},
    {"Project":"GreenStreet Revamp Retail Hub","Retail_SF":22},
    {"Project":"Summit at Renaissance Park (Greenspoint)","Retail_SF":17}
]

# Create DataFrame and sort by Retail_SF descending (ascending=True for horizontal bar to show descending order)
df = pd.DataFrame(data)
df = df.sort_values('Retail_SF', ascending=True)

# Shorten project names to meet 15 character limit, maintaining order
project_mapping = {
    "San Jacinto Marketplace (Baytown)": "San Jacinto MP",
    "East Blocks Phase 1 (EaDo)": "East Blocks P1", 
    "Astros Entertainment District (Downtown)": "Astros Ent Dst",
    "GreenStreet Revamp Retail Hub": "GreenStreet Hub",
    "Summit at Renaissance Park (Greenspoint)": "Summit at RP"
}

df['Project_Short'] = df['Project'].map(project_mapping)

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        y=df['Project_Short'],
        x=df['Retail_SF'],
        orientation='h',
        marker_color='#1FB8CD',  # Strong cyan from the color palette
        text=[f"{val}k sf" for val in df['Retail_SF']],
        textposition='outside',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title='Houston 2024 Retail & Entertainment Space',
    xaxis_title='Retail GLA (k)',
    yaxis_title='Project',
    showlegend=False
)

# Set x-axis tick marks
fig.update_xaxes(
    tickmode='array',
    tickvals=[0, 100, 200, 300, 400, 500],
    range=[0, 600]  # Add space for the text labels
)

# Save the chart
fig.write_image('houston_retail_chart.png')