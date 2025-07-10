import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create the data
data = [
    {"Category": "Title Issues", "Impact_Level": 40, "Subcategories": "Liens, Boundary Disputes, Defective Deeds, Missing Heirs, Easement Conflicts"},
    {"Category": "Deed Restrictions", "Impact_Level": 30, "Subcategories": "Enforcement Challenges, Compliance Issues, Amendment Processes, City vs Private Enforcement"},
    {"Category": "Litigation Trends", "Impact_Level": 20, "Subcategories": "Construction Disputes, Contract Breaches, Development Delays, Zoning Conflicts"},
    {"Category": "Eminent Domain", "Impact_Level": 10, "Subcategories": "Texas Central Railway, TxDOT Projects, Pipeline Development, Fair Compensation Disputes"}
]

df = pd.DataFrame(data)

# Brand colors
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F']

# Create the bar chart
fig = go.Figure(data=[
    go.Bar(
        x=df['Category'],
        y=df['Impact_Level'],
        text=[f"{val}%" for val in df['Impact_Level']],
        textposition='outside',
        marker_color=colors,
        hovertemplate='<b>%{x}</b><br>Impact: %{y}%<br><extra></extra>',
        cliponaxis=False
    )
])

# Update layout
fig.update_layout(
    title="Houston Property Dev Legal Issues",
    xaxis_title="Issue Category",
    yaxis_title="Impact Level (%)",
    showlegend=False
)

# Update axes
fig.update_xaxes(tickangle=45)
fig.update_yaxes(range=[0, 45])

# Save the chart
fig.write_image("houston_legal_issues.png")