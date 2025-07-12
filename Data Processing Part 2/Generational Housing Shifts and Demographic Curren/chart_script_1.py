import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create the data
data = [
    {"Country":"Mexico","Share_%":37},
    {"Country":"El Salvador","Share_%":7},
    {"Country":"Vietnam","Share_%":6},
    {"Country":"India","Share_%":6},
    {"Country":"Honduras","Share_%":6},
    {"Country":"Nigeria","Share_%":4},
    {"Country":"All Others","Share_%":34}
]

df = pd.DataFrame(data)

# Define the brand colors
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C', '#B4413C', '#964325']

# Create donut chart
fig = go.Figure(data=[go.Pie(
    labels=df['Country'], 
    values=df['Share_%'],
    hole=0.4,  # This creates the donut effect
    marker_colors=colors[:len(df)],
    textinfo='label+percent',
    textposition='inside'
)])

# Update layout
fig.update_layout(
    title="Houston Foreign-Born by Origin (2017-21)",
    uniformtext_minsize=14, 
    uniformtext_mode='hide'
)

# Save the chart
fig.write_image("houston_foreign_born_donut.png")