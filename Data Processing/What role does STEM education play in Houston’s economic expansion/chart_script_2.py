import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_csv('houston_stem_employers.csv')

# Create the scatter plot
fig = px.scatter(
    df, 
    x='STEM_Jobs', 
    y='Average_Salary',
    color='Sector',
    size='STEM_Jobs',
    hover_data=['Company'],
    color_discrete_sequence=['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C'],
    title='Houston STEM Jobs vs Salary by Sector'
)

# Update layout
fig.update_layout(
    xaxis_title='STEM Jobs',
    yaxis_title='Avg Salary ($)',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Format x-axis with k for thousands
fig.update_xaxes(
    tickformat='.0f',
    tickvals=[0, 3000, 6000, 9000, 12000, 15000],
    ticktext=['0', '3k', '6k', '9k', '12k', '15k']
)

# Format y-axis with dollar signs and k for thousands
fig.update_yaxes(
    tickformat='$,.0f',
    tickvals=[80000, 90000, 100000, 110000, 120000, 130000, 140000],
    ticktext=['$80k', '$90k', '$100k', '$110k', '$120k', '$130k', '$140k']
)

# Save the chart
fig.write_image('scatter_plot.png')
print("Chart saved as scatter_plot.png")