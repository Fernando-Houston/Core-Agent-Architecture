import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load the data
data = {"price_history": [{"Year": 2017, "Price_per_sqft": 65.62}, {"Year": 2018, "Price_per_sqft": 91.22}, {"Year": 2019, "Price_per_sqft": 101.78}, {"Year": 2020, "Price_per_sqft": 120.83}, {"Year": 2021, "Price_per_sqft": 134.16}, {"Year": 2022, "Price_per_sqft": 156.91}, {"Year": 2023, "Price_per_sqft": 172.27}, {"Year": 2024, "Price_per_sqft": 165.56}], "cost_breakdown": [{"category": "Construction Cost", "percentage": 85, "value": 212500}, {"category": "Permit & Impact Fees", "percentage": 3, "value": 7400}, {"category": "Land Cost", "percentage": 12, "value": 30000}], "key_metrics": [{"metric": "Median Property Value", "value": "$285,105"}, {"metric": "Gross Rental Yield", "value": "10.1%"}, {"metric": "5-Year Appreciation", "value": "62.7%"}, {"metric": "Property Tax Rate", "value": "2.12%"}]}

# Create DataFrame from cost breakdown data
df_cost = pd.DataFrame(data['cost_breakdown'])

# Create abbreviated category names to fit character limit
df_cost['category_short'] = df_cost['category'].str.replace('Construction Cost', 'Construction')
df_cost['category_short'] = df_cost['category_short'].str.replace('Permit & Impact Fees', 'Permits & Fees')

# Create pie chart
fig = go.Figure(data=[
    go.Pie(
        labels=df_cost['category_short'],
        values=df_cost['value'],
        marker_colors=['#1FB8CD', '#FFC185', '#ECEBD5'],
        textinfo='label+percent',
        textposition='inside',
        hovertemplate='<b>%{label}</b><br>Value: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )
])

# Update layout
fig.update_layout(
    title='Katy Heights Dev Cost Breakdown',
    uniformtext_minsize=14,
    uniformtext_mode='hide'
)

# Save the chart
fig.write_image('katy_heights_cost_breakdown.png')