import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create the data
data = [
    {"Area": "City of Houston", "Number of Zones": 99},
    {"Area": "Other Harris County Areas", "Number of Zones": 51}
]

df = pd.DataFrame(data)

# Shorten labels to meet 15-character limit
df['Area_Short'] = df['Area'].replace({
    'City of Houston': 'Houston',
    'Other Harris County Areas': 'Other Areas'
})

# Calculate percentages
df['Percentage'] = (df['Number of Zones'] / df['Number of Zones'].sum()) * 100

# Create labels with numbers and percentages
df['Label'] = df['Area_Short'] + '<br>' + df['Number of Zones'].astype(str) + ' zones<br>' + df['Percentage'].round(1).astype(str) + '%'

# Create pie chart
fig = go.Figure(data=[go.Pie(
    labels=df['Area_Short'],
    values=df['Number of Zones'],
    text=df['Label'],
    textinfo='text',
    textposition='inside',
    hovertemplate='<b>%{label}</b><br>Zones: %{value}<br>Percentage: %{percent}<extra></extra>',
    marker=dict(colors=['#1FB8CD', '#FFC185'])
)])

# Update layout
fig.update_layout(
    title='Harris County Opportunity Zones',
    uniformtext_minsize=14,
    uniformtext_mode='hide'
)

# Save the chart
fig.write_image("harris_county_opportunity_zones.png")