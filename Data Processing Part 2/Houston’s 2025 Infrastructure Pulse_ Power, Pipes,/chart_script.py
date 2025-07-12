# Install kaleido for image export
!pip -q install kaleido

import pandas as pd
import plotly.graph_objects as go

# Provided data
data = [
    {"Upgrade": "Storm-resilient poles", "Quantity": 26000},
    {"Upgrade": "Underground power lines (miles)", "Quantity": 400},
    {"Upgrade": "Automation devices", "Quantity": 5100},
    {"Upgrade": "Vegetation cleared (miles)", "Quantity": 4000}
]

df = pd.DataFrame(data)

# Create labels under 15 characters (required by strict instructions)
label_map = {
    "Storm-resilient poles": "Storm poles",
    "Underground power lines (miles)": "Underground mi",
    "Automation devices": "Automation dev",
    "Vegetation cleared (miles)": "Vegetation mi"
}

df["Label"] = df["Upgrade"].map(label_map)

# Brand colors in order
colors = ["#1FB8CD", "#FFC185", "#ECEBD5", "#5D878F"]

# Create horizontal bar chart
fig = go.Figure(go.Bar(
    x=df["Quantity"],
    y=df["Label"],
    orientation="h",
    marker=dict(color=colors),
    cliponaxis=False,
    text=[f"{q:,.0f}" for q in df["Quantity"]],
    textposition="outside",
    textfont=dict(size=14, color="black")
))

# Layout updates - title must be under 40 characters per strict instructions
fig.update_layout(
    title="CenterPoint Houston Key Upgrades 2014-25",
    showlegend=False
)

fig.update_xaxes(title_text="Quantity", tickformat="~s")
fig.update_yaxes(title_text="Upgrade Type")

# Save figure
file_path = "centerpoint_upgrades_chart.png"
fig.write_image(file_path)
fig