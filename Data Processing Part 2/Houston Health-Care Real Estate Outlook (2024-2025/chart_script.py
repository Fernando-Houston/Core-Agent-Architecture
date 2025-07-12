import plotly.graph_objects as go
import pandas as pd

# Data provided
projects = [
    {"Project": "Harris Health LBJ Replacement Hospital", "InvestmentUSDm": 1600},
    {"Project": "Memorial Hermann Cypress North Tower", "InvestmentUSDm": 277.5},
    {"Project": "Houston Methodist West Campus Expansion", "InvestmentUSDm": 247},
    {"Project": "Memorial Hermann TMC Sarofim Pavilion Build-out", "InvestmentUSDm": 270}
]

# Create DataFrame
df = pd.DataFrame(projects)

# Sort descending by investment
df = df.sort_values('InvestmentUSDm', ascending=False)

# Abbreviation mapping (<=15 chars each)
name_map = {
    "Harris Health LBJ Replacement Hospital": "Harris LBJ Repl",
    "Memorial Hermann Cypress North Tower": "MH Cypress NT",
    "Houston Methodist West Campus Expansion": "HM West Campus",
    "Memorial Hermann TMC Sarofim Pavilion Build-out": "MH Sarofim PV"
}

y_labels = df['Project'].map(name_map).tolist()

# Format investment labels with abbreviations (<=15 chars)
def fmt(val):
    if val >= 1000:
        return f"${val/1000:.1f}B"
    return f"${val:.1f}M"

text_labels = [fmt(v) for v in df['InvestmentUSDm']]

# Brand colors in order
colors = ["#1FB8CD", "#FFC185", "#ECEBD5", "#5D878F"][:len(df)]

# Build figure
fig = go.Figure(go.Bar(
    x=df['InvestmentUSDm'],
    y=y_labels,
    orientation='h',
    text=text_labels,
    textposition='auto',
    marker_color=colors,
    cliponaxis=False
))

# Layout updates
fig.update_layout(
    title='Houston Hospital Expansions 2024-2025',
    xaxis_title='Invest USDm',
    yaxis_title='Project',
    showlegend=False
)

# X-axis range 0-1800
fig.update_xaxes(range=[0, 1800])

# Save chart
fig.write_image('houston_hospital_chart.png')