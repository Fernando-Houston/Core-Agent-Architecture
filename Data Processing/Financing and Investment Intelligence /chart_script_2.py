import plotly.graph_objects as go
import plotly.express as px

# Data for the chart
data = [
    {"Program Type": "Standard Tax Abatement", "Max Abatement Percentage": 50},
    {"Program Type": "LEED Certified Projects", "Max Abatement Percentage": 55},
    {"Program Type": "Target Area Projects", "Max Abatement Percentage": 60},
    {"Program Type": "Target Area + Job Creation (100+ jobs)", "Max Abatement Percentage": 70},
    {"Program Type": "Green Building Certification", "Max Abatement Percentage": 55}
]

# Extract data for plotting
program_types = [item["Program Type"] for item in data]
percentages = [item["Max Abatement Percentage"] for item in data]

# Abbreviate program types to meet 15 character limit
abbreviated_types = [
    "Standard Tax",
    "LEED Certified", 
    "Target Area",
    "Target+Jobs",
    "Green Building"
]

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        y=abbreviated_types,
        x=percentages,
        orientation='h',
        marker_color='#1FB8CD',
        text=[f'{p}%' for p in percentages],
        textposition='outside',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title="Harris County Tax Abatement Benefits",
    xaxis_title="Abatement %",
    yaxis_title="Program Type"
)

# Update axes
fig.update_xaxes(range=[0, 80])
fig.update_yaxes(categoryorder='total ascending')

# Save the chart
fig.write_image("harris_county_tax_abatement.png")