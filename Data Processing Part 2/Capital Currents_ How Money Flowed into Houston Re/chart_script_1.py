import plotly.express as px
import pandas as pd

# Create the data
data = {
    "Country": ["Mexico", "India", "China", "Canada", "United Kingdom", "Other"],
    "Share": [37, 9, 6, 4, 3, 41]
}

df = pd.DataFrame(data)

# Define the color sequence using the brand colors
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C', '#B4413C']

# Create the pie chart
fig = px.pie(df, 
             values='Share', 
             names='Country',
             title='Foreign Investment in Texas RE',
             color_discrete_sequence=colors)

# Update layout for pie chart specific requirements
fig.update_layout(
    uniformtext_minsize=12, 
    uniformtext_mode='hide'
)

# Update traces to show percentage labels
fig.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

# Save the chart
fig.write_image('texas_real_estate_investment_pie.png')