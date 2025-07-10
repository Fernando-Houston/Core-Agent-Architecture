import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_csv("houston_commercial_real_estate_data.csv")

# Sort by vacancy rate in descending order
df_sorted = df.sort_values('Vacancy_Rate_Percent', ascending=False)

# Create color mapping based on vacancy rate ranges
def get_color(rate):
    if rate > 30:
        return '#B4413C'  # Red for very high (>30%)
    elif rate >= 25:
        return '#FFC185'  # Orange for high (25-30%)
    elif rate >= 20:
        return '#D2BA4C'  # Yellow for moderate (20-25%)
    elif rate >= 15:
        return '#ECEBD5'  # Light green for low (15-20%)
    else:
        return '#5D878F'  # Dark green for very low (<15%)

# Apply color mapping
df_sorted['Color'] = df_sorted['Vacancy_Rate_Percent'].apply(get_color)

# Truncate submarket names to 15 characters
df_sorted['Submarket_Short'] = df_sorted['Submarket'].apply(lambda x: x[:15] if len(x) > 15 else x)

# Create horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_sorted['Vacancy_Rate_Percent'],
    y=df_sorted['Submarket_Short'],
    orientation='h',
    marker_color=df_sorted['Color'],
    text=[f"{rate:.1f}%" for rate in df_sorted['Vacancy_Rate_Percent']],
    textposition='outside',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title="Houston CRE Vacancy Rates (2025)",
    xaxis_title="Vacancy Rate%",
    yaxis_title="Submarket",
    showlegend=False
)

# Save the chart
fig.write_image("houston_vacancy_rates.png")