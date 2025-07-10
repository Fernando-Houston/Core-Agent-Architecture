import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_csv("houston_commercial_sectors_2024.csv")

# Define colors in the specified order
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C']

# Create the bar chart
fig = px.bar(df, 
             x='Sector', 
             y='Under Construction (Million SF)',
             color='Sector',
             color_discrete_sequence=colors,
             title='Houston Commercial Development 2024-25')

# Add value labels on top of bars and set cliponaxis for traces
fig.update_traces(
    texttemplate='%{y}M',
    textposition='outside',
    cliponaxis=False
)

# Update layout
fig.update_layout(
    xaxis_title='Sector',
    yaxis_title='Constr (M SF)',
    showlegend=False  # Remove legend since colors are just for visual distinction
)

# Save the chart
fig.write_image('houston_commercial_chart.png')

print("Chart saved successfully!")
print(f"Data points: {len(df)} sectors")
print(f"Values: {df['Under Construction (Million SF)'].tolist()}")