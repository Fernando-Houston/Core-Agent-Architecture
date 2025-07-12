import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Data from the provided JSON
data = {
    "Deal": ["Blackstone industrial", "KKR Park 8Ninety", "Hamilton Point multifamily", "BSR REIT acquisitions"],
    "Value": [718, 234, 195, 141]
}

# Create DataFrame
df = pd.DataFrame(data)

# Shorten deal names to meet 15 character limit
df['Deal_Short'] = [
    "Blackstone", 
    "KKR Park 8N", 
    "Hamilton Point", 
    "BSR REIT"
]

# Sort by value descending
df_sorted = df.sort_values('Value', ascending=True)  # ascending=True for horizontal bar to show highest at top

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        x=df_sorted['Value'],
        y=df_sorted['Deal_Short'],
        orientation='h',
        marker_color=['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F'],
        text=df_sorted['Value'],
        textposition='inside',
        textfont=dict(size=14),
        cliponaxis=False
    )
])

# Update layout with shortened title (under 40 characters)
fig.update_layout(
    title="Houston CRE Acquisitions 2024",
    xaxis_title="Value ($M)",
    yaxis_title="Deal",
    uniformtext_minsize=14,
    uniformtext_mode='hide'
)

# Save chart
fig.write_image("houston_cre_acquisitions.png")