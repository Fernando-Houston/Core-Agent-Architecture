import plotly.graph_objects as go
import pandas as pd

# Create the data
data = [
    {"MSA":"Houston–Pasadena–The Woodlands","Providers":1487},
    {"MSA":"Dallas–Fort Worth–Arlington","Providers":1439},
    {"MSA":"San Antonio–New Braunfels","Providers":550}
]

df = pd.DataFrame(data)

# Sort by provider count descending
df = df.sort_values('Providers', ascending=True)  # ascending=True for horizontal bar to show highest at top

# Abbreviate MSA names to fit 15 character limit (strict requirement)
df['MSA_Short'] = df['MSA'].replace({
    'Houston–Pasadena–The Woodlands': 'Houston Metro',
    'Dallas–Fort Worth–Arlington': 'Dallas Metro', 
    'San Antonio–New Braunfels': 'San Antonio'
})

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        x=df['Providers'],
        y=df['MSA_Short'],
        orientation='h',
        text=df['Providers'],
        textposition='inside',
        textfont=dict(color='white', size=14),
        marker_color='#1FB8CD',
        cliponaxis=False
    )
])

# Update layout with title under 40 characters
fig.update_layout(
    title='Texas Medicaid Telemedicine FY 2023',
    xaxis_title='Provider Count',
    yaxis_title='MSA'
)

# Update axes with gridlines
fig.update_xaxes(range=[0, 1600], showgrid=True)
fig.update_yaxes(showgrid=True)

# Save the chart
fig.write_image('medicaid_telemedicine_providers.png')