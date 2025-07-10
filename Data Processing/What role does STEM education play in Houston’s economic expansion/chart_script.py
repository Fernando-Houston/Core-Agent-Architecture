import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Load the data
df = pd.read_csv("houston_stem_economic_impact.csv")

# Create abbreviated category names (15 char limit)
df['Category_Short'] = df['Category'].apply(lambda x: x[:15] if len(x) <= 15 else x[:12] + '...')

# Create formatted values for display
def format_value(row):
    value = row['Value']
    unit = row['Unit']
    
    if 'Billion' in unit:
        return f"{value:.1f}b"
    elif 'Thousand' in unit:
        if value >= 1000:
            return f"{value/1000:.1f}k"
        else:
            return f"{value:.0f}k"
    elif 'Percentage' in unit:
        return f"{value:.1f}%"
    else:
        return f"{value:.1f}"

df['Value_Formatted'] = df.apply(format_value, axis=1)

# Define color mapping based on unit types
color_mapping = {
    'Billion USD': '#1FB8CD',      # Strong cyan for large economic impacts
    'Thousand USD': '#FFC185',     # Light orange for salary data
    'Thousand Jobs': '#ECEBD5',    # Light green for job metrics
    'Thousand Workers': '#5D878F', # Cyan for workforce data
    'Percentage': '#D2BA4C'        # Moderate yellow for percentage metrics
}

# Map colors to each row based on unit
df['Color'] = df['Unit'].map(color_mapping)

# Create the bar chart
fig = go.Figure()

# Add bars with custom colors and cliponaxis=False
fig.add_trace(go.Bar(
    x=df['Category_Short'],
    y=df['Value'],
    marker_color=df['Color'],
    text=df['Value_Formatted'],
    textposition='auto',
    cliponaxis=False,
    hovertemplate='<b>%{customdata[0]}</b><br>' +
                  'Value: %{customdata[1]}<br>' +
                  'Unit: %{customdata[2]}<br>' +
                  '<extra></extra>',
    customdata=df[['Category', 'Value_Formatted', 'Unit']],
    showlegend=False
))

# Update layout
fig.update_layout(
    title='Houston STEM Economic Impact Analysis',
    xaxis_title='Category',
    yaxis_title='Value'
)

# Update axes
fig.update_xaxes(tickangle=45)
fig.update_yaxes(tickformat='.0f')

# Save the chart
fig.write_image("houston_stem_impact.png")

print("Chart saved successfully!")
print(f"Number of categories: {len(df)}")
print("Categories included:")
for i, row in df.iterrows():
    print(f"- {row['Category']}: {row['Value']} {row['Unit']}")