import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create the investment data
investment_data = [
    {"Project/Initiative": "Memorial Hermann TMC Expansion", "Investment ($M)": 270, "Timeline": "2025-2027", "Sector": "Healthcare"},
    {"Project/Initiative": "Harris Health LBJ Hospital", "Investment ($M)": 1600, "Timeline": "2024-2028", "Sector": "Healthcare"},
    {"Project/Initiative": "TMC BioPort Campus", "Investment ($M)": 5000, "Timeline": "2025-2030", "Sector": "Life Sciences"},
    {"Project/Initiative": "Apple Manufacturing Facility", "Investment ($M)": 500, "Timeline": "2025-2026", "Sector": "Technology"},
    {"Project/Initiative": "Harris County Solar Grant", "Investment ($M)": 250, "Timeline": "2024-2025", "Sector": "Energy"},
    {"Project/Initiative": "Houston VC Funding (2022)", "Investment ($M)": 2040, "Timeline": "2022", "Sector": "Venture Capital"},
    {"Project/Initiative": "Ion District Development", "Investment ($M)": 100, "Timeline": "2018-2030", "Sector": "Innovation"}
]

df = pd.DataFrame(investment_data)

# Abbreviate project names to fit 15 character limit
df['Short_Name'] = [
    "Memorial TMC",
    "LBJ Hospital", 
    "TMC BioPort",
    "Apple Facility",
    "Solar Grant",
    "VC Funding",
    "Ion District"
]

# Sort by investment amount for better visualization
df = df.sort_values('Investment ($M)', ascending=True)

# Create color mapping for sectors using the brand colors
sector_colors = {
    'Healthcare': '#1FB8CD',
    'Life Sciences': '#FFC185', 
    'Technology': '#ECEBD5',
    'Energy': '#5D878F',
    'Venture Capital': '#D2BA4C',
    'Innovation': '#B4413C'
}

# Create combined custom data for hover
combined_data = []
for i, row in df.iterrows():
    combined_data.append([row['Sector'], row['Timeline']])

# Create the bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    y=df['Short_Name'],
    x=df['Investment ($M)'],
    orientation='h',
    marker_color=[sector_colors[sector] for sector in df['Sector']],
    text=[f"${val}M" for val in df['Investment ($M)']],
    textposition='outside',
    cliponaxis=False,
    hovertemplate='<b>%{y}</b><br>Investment: $%{x}M<br>Sector: %{customdata[0]}<br>Timeline: %{customdata[1]}<extra></extra>',
    customdata=combined_data
))

fig.update_layout(
    title="Houston Major Investment Projects",
    xaxis_title="Investment ($M)",
    yaxis_title="Projects",
    showlegend=False
)

# Save the chart
fig.write_image("houston_investments.png")