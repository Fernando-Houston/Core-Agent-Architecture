import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_csv("houston_job_growth_by_sector.csv")

# Sort by job growth in descending order
df_sorted = df.sort_values('Job_Growth_2024_2025', ascending=False)

# Create color categories based on job growth using specified colors
def get_color_category(growth):
    if growth > 10000:
        return '#1f4e79'  # Dark blue for very high growth
    elif growth >= 5000:
        return '#4472c4'  # Medium blue for high growth
    elif growth >= 2000:
        return '#8db4e2'  # Light blue for moderate growth
    else:
        return '#7f7f7f'  # Gray for low growth

def get_category_label(growth):
    if growth > 10000:
        return 'Very High (>10k)'
    elif growth >= 5000:
        return 'High (5k-10k)'
    elif growth >= 2000:
        return 'Moderate (2k-5k)'
    else:
        return 'Low (<2k)'

# Assign colors and categories based on growth
df_sorted['color'] = df_sorted['Job_Growth_2024_2025'].apply(get_color_category)
df_sorted['category'] = df_sorted['Job_Growth_2024_2025'].apply(get_category_label)

# Create the bar chart
fig = go.Figure()

# Get unique categories and their colors for legend
categories = df_sorted['category'].unique()
colors = df_sorted.groupby('category')['color'].first()

# Add bars for each category to create legend
for category in ['Very High (>10k)', 'High (5k-10k)', 'Moderate (2k-5k)', 'Low (<2k)']:
    if category in df_sorted['category'].values:
        category_data = df_sorted[df_sorted['category'] == category]
        fig.add_trace(go.Bar(
            x=category_data['Sector'],
            y=category_data['Job_Growth_2024_2025'],
            marker_color=category_data['color'].iloc[0],
            text=[f"{val/1000:.1f}k" if val >= 1000 else str(val) for val in category_data['Job_Growth_2024_2025']],
            textposition='outside',
            cliponaxis=False,
            name=category,
            showlegend=True
        ))

# Update layout
fig.update_layout(
    title="Houston Job Growth by Sector (2024-2025)",
    xaxis_title="Sector",
    yaxis_title="New Jobs Added",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update x-axis to rotate labels exactly 45 degrees
fig.update_xaxes(tickangle=45)

# Format y-axis to show consistent abbreviated numbers
max_val = max(df_sorted['Job_Growth_2024_2025'])
tick_interval = 2500
tick_vals = [i for i in range(0, max_val + tick_interval, tick_interval)]
tick_texts = [f"{i/1000:.1f}k" if i >= 1000 else str(i) for i in tick_vals]

fig.update_yaxes(
    tickvals=tick_vals,
    ticktext=tick_texts
)

# Save the chart
fig.write_image("houston_job_growth_chart.png")