import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the Houston housing market data
df = pd.read_csv("houston_housing_market_data.csv")

# Create color mapping using brand colors that match the requested colors
color_mapping = {
    'Very High': '#DB4545',  # Soft red (for red)
    'High': '#FFC185',       # Light orange (for orange)
    'Moderate': '#D2BA4C'    # Moderate yellow (for yellow)
}

# Create the scatter plot with area labels
fig = px.scatter(
    df, 
    x='Median_Home_Price_2025', 
    y='Price_Change_Percent',
    color='Housing_Demand_Level',
    color_discrete_map=color_mapping,
    text='Area',  # Add area labels
    title='Houston Housing vs Growth 2025',
    labels={
        'Median_Home_Price_2025': 'Med Home Price',
        'Price_Change_Percent': 'Price Chg (%)',
        'Housing_Demand_Level': 'Demand Level'
    }
)

# Update traces to use cliponaxis=False and make points larger
fig.update_traces(
    cliponaxis=False,
    marker=dict(size=10),
    textposition="top center"
)

# Update layout with formatting
fig.update_layout(
    xaxis_tickformat='$,.0f'
)

# Update axis labels to match requirements while staying under 15 characters
fig.update_xaxes(title_text='Med Home Price')
fig.update_yaxes(title_text='Price Chg (%)')

# Center legend under title if 5 or fewer items
unique_levels = df['Housing_Demand_Level'].nunique()
if unique_levels <= 5:
    fig.update_layout(
        legend=dict(
            orientation='h', 
            yanchor='bottom', 
            y=1.05, 
            xanchor='center', 
            x=0.5
        )
    )

# Save the chart
fig.write_image('houston_housing_scatter.png')
print("Chart saved as houston_housing_scatter.png")