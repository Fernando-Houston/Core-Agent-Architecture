import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# Load the data
df = pd.read_csv('houston_developers_2024.csv')

# Filter for developers with permits > 0 and get top 5
df_filtered = df[df['January 2025 Permits'] > 0].copy()
df_top5 = df_filtered.nlargest(5, 'January 2025 Permits')

# Sort by permits in ascending order for horizontal bar chart (so highest is at top)
df_top5 = df_top5.sort_values('January 2025 Permits', ascending=True)

# Abbreviate developer names to fit 15 character limit
df_top5['Short_Name'] = df_top5['Developer'].str[:15]

# Create the horizontal bar chart
fig = go.Figure()

# Use the brand colors for each developer
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C']

# Add the bars
fig.add_trace(go.Bar(
    y=df_top5['Short_Name'],
    x=df_top5['January 2025 Permits'],
    orientation='h',
    marker_color=colors[:len(df_top5)],
    text=df_top5['January 2025 Permits'],
    textposition='outside',
    textfont=dict(size=12),
    hovertemplate='<b>%{customdata[0]}</b><br>' +
                  'Permits: %{x}<br>' +
                  'Avg Home Value: $%{customdata[1]:,.0f}<extra></extra>',
    customdata=list(zip(df_top5['Developer'], df_top5['Average Home Value ($)'])),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Top 5 Houston Devs - Jan 2025',
    xaxis_title='Permits',
    yaxis_title='Developer',
    showlegend=False
)

# Save the chart
fig.write_image('houston_developers_chart.png')

print("Chart created successfully!")
print(f"Top 5 developers by permits:")
for i, row in df_top5.sort_values('January 2025 Permits', ascending=False).iterrows():
    print(f"{row['Developer']}: {row['January 2025 Permits']} permits, Avg Value: ${row['Average Home Value ($)']:,.0f}")