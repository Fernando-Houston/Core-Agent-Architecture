import plotly.express as px
import pandas as pd

# Create the data
data = {
    "Metro": ["Austin", "San Antonio", "Fort Worth", "Houston"],
    "ImpactFee": [7200, 7200, 3500, 3240]
}

df = pd.DataFrame(data)

# Create horizontal bar chart
fig = px.bar(df, 
             x='ImpactFee', 
             y='Metro',
             orientation='h',
             title='TX Metro Water/Wastewater Fees (2024)',
             color='Metro',
             color_discrete_map={
                 'Austin': '#1FB8CD',
                 'San Antonio': '#FFC185', 
                 'Fort Worth': '#ECEBD5',
                 'Houston': '#B4413C'
             },
             text='ImpactFee')

# Update layout
fig.update_layout(
    xaxis_title='USD',
    yaxis_title='Metro',
    showlegend=False
)

# Update traces with cliponaxis
fig.update_traces(cliponaxis=False)

# Format text on bars
fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')

# Save the chart
fig.write_image('texas_metro_fees.png')