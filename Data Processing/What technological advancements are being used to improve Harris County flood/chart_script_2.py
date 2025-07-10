import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Data
data = {
    "systems": [
        {"name": "MaxFloodCast ML Model", "accuracy": 94.9, "type": "ML"},
        {"name": "FloodGNN Graph Neural Network", "accuracy": 98.0, "type": "Deep Learning"},
        {"name": "Random Forest Model", "accuracy": 80.3, "type": "ML"},
        {"name": "Artificial Neural Network", "accuracy": 85.0, "type": "Deep Learning"},
        {"name": "Support Vector Machine", "accuracy": 81.8, "type": "ML"},
        {"name": "Traditional Physics-Based Models", "accuracy": 72.0, "type": "Traditional"},
        {"name": "Quantum ML Models", "accuracy": 76.0, "type": "Quantum"}
    ]
}

# Create DataFrame
df = pd.DataFrame(data["systems"])

# Abbreviate names to keep under 15 characters
name_mapping = {
    "MaxFloodCast ML Model": "MaxFloodCast",
    "FloodGNN Graph Neural Network": "FloodGNN",
    "Random Forest Model": "Random Forest",
    "Artificial Neural Network": "ANN",
    "Support Vector Machine": "SVM",
    "Traditional Physics-Based Models": "Physics-Based",
    "Quantum ML Models": "Quantum ML"
}

df['short_name'] = df['name'].map(name_mapping)

# Sort by accuracy for better visualization
df = df.sort_values('accuracy')

# Define colors for each type
color_map = {
    "ML": "#1FB8CD",
    "Deep Learning": "#FFC185", 
    "Traditional": "#ECEBD5",
    "Quantum": "#5D878F"
}

# Create horizontal bar chart
fig = go.Figure()

for system_type in df['type'].unique():
    subset = df[df['type'] == system_type]
    fig.add_trace(go.Bar(
        y=subset['short_name'],
        x=subset['accuracy'],
        name=system_type,
        orientation='h',
        marker_color=color_map[system_type],
        text=[f"{acc}%" for acc in subset['accuracy']],
        textposition='outside',
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title="AI Flood Prediction System Accuracy",
    xaxis_title="Accuracy (%)",
    yaxis_title="System",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    xaxis=dict(range=[0, 105])
)

# Save the chart
fig.write_image("flood_prediction_accuracy_chart.png")