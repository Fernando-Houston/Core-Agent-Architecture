import plotly.graph_objects as go
import pandas as pd

# Create the data
data = [
    {"Loan Type": "Multifamily Over $6M", "Interest Rate": 5.34},
    {"Loan Type": "Multifamily Under $6M", "Interest Rate": 5.80},
    {"Loan Type": "Commercial Real Estate", "Interest Rate": 6.38},
    {"Loan Type": "CMBS Loan", "Interest Rate": 6.42},
    {"Loan Type": "Owner Occupied", "Interest Rate": 6.18},
    {"Loan Type": "Industrial", "Interest Rate": 6.38},
    {"Loan Type": "Office Building", "Interest Rate": 6.38},
    {"Loan Type": "NNN Single Tenant", "Interest Rate": 5.98},
    {"Loan Type": "SBA 504", "Interest Rate": 6.70},
    {"Loan Type": "Bridge Loans", "Interest Rate": 9.00}
]

df = pd.DataFrame(data)

# Abbreviate loan types to fit 15 character limit
df['Loan Type Short'] = df['Loan Type'].str.replace('Multifamily Over $6M', 'Multi >$6M')
df['Loan Type Short'] = df['Loan Type Short'].str.replace('Multifamily Under $6M', 'Multi <$6M')
df['Loan Type Short'] = df['Loan Type Short'].str.replace('Commercial Real Estate', 'CRE')
df['Loan Type Short'] = df['Loan Type Short'].str.replace('Owner Occupied', 'Owner Occ')
df['Loan Type Short'] = df['Loan Type Short'].str.replace('Office Building', 'Office')
df['Loan Type Short'] = df['Loan Type Short'].str.replace('NNN Single Tenant', 'NNN Single')
df['Loan Type Short'] = df['Loan Type Short'].str.replace('Bridge Loans', 'Bridge')

# Create the bar chart
fig = go.Figure(data=[
    go.Bar(
        x=df['Loan Type Short'],
        y=df['Interest Rate'],
        marker_color='#1FB8CD',
        hovertemplate='<b>%{x}</b><br>Rate: %{y}%<extra></extra>',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title='TX CRE Lending Rates - July 2025',
    xaxis_title='Loan Type',
    yaxis_title='Rate (%)',
    showlegend=False
)

# Update y-axis to show percentages
fig.update_yaxes(tickformat='.2f', ticksuffix='%')

# Rotate x-axis labels for better readability
fig.update_xaxes(tickangle=45)

# Save the chart
fig.write_image('cre_lending_rates.png')