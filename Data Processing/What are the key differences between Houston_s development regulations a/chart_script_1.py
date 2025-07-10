import plotly.graph_objects as go
import plotly.express as px
import json

# Load the data
data = {
    "houston_process": [
        {"step": 1, "description": "Check deed restrictions (if any)", "color": "#FF6B6B"},
        {"step": 2, "description": "Apply for building permit", "color": "#FF6B6B"},
        {"step": 3, "description": "Submit development plan", "color": "#FF6B6B"},
        {"step": 4, "description": "Code compliance review", "color": "#FF6B6B"},
        {"step": 5, "description": "Permit issued (if compliant)", "color": "#FF6B6B"},
        {"step": 6, "description": "Begin construction", "color": "#FF6B6B"}
    ],
    "traditional_process": [
        {"step": 1, "description": "Check zoning designation", "color": "#4ECDC4"},
        {"step": 2, "description": "Apply for permits/approvals", "color": "#4ECDC4"},
        {"step": 3, "description": "Planning commission review", "color": "#4ECDC4"},
        {"step": 4, "description": "Public hearings (if required)", "color": "#4ECDC4"},
        {"step": 5, "description": "Variance request (if needed)", "color": "#4ECDC4"},
        {"step": 6, "description": "Zoning board appeal (if needed)", "color": "#4ECDC4"},
        {"step": 7, "description": "Final approval/denial", "color": "#4ECDC4"},
        {"step": 8, "description": "Begin construction (if approved)", "color": "#4ECDC4"}
    ]
}

# Create abbreviated labels (15 char limit)
houston_labels = ["Check deed", "Apply permit", "Submit plan", "Code review", "Permit issued", "Begin constr"]
traditional_labels = ["Check zoning", "Apply permits", "Planning rev", "Public hearing", "Variance req", "Zoning appeal", "Final approval", "Begin constr"]

# Create the figure
fig = go.Figure()

# Add Houston process (positioned on the left side)
houston_y = list(range(len(houston_labels)-1, -1, -1))  # Reverse order to go top to bottom
fig.add_trace(go.Scatter(
    x=[-0.5] * len(houston_labels),
    y=houston_y,
    mode='markers+text',
    marker=dict(size=30, color='#FF6B6B'),
    text=houston_labels,
    textposition="middle right",
    name='Houston',
    cliponaxis=False,
    textfont=dict(size=12)
))

# Add Traditional process (positioned on the right side)
traditional_y = list(range(len(traditional_labels)-1, -1, -1))  # Reverse order to go top to bottom
fig.add_trace(go.Scatter(
    x=[0.5] * len(traditional_labels),
    y=traditional_y,
    mode='markers+text',
    marker=dict(size=30, color='#4ECDC4'),
    text=traditional_labels,
    textposition="middle left",
    name='Traditional',
    cliponaxis=False,
    textfont=dict(size=12)
))

# Add connecting arrows for Houston process
for i in range(len(houston_labels) - 1):
    fig.add_trace(go.Scatter(
        x=[-0.5, -0.5],
        y=[houston_y[i], houston_y[i+1]],
        mode='lines',
        line=dict(color='#FF6B6B', width=3),
        showlegend=False,
        cliponaxis=False
    ))
    # Add arrow marker
    fig.add_trace(go.Scatter(
        x=[-0.5],
        y=[houston_y[i+1]],
        mode='markers',
        marker=dict(size=10, color='#FF6B6B', symbol='triangle-down'),
        showlegend=False,
        cliponaxis=False
    ))

# Add connecting arrows for Traditional process
for i in range(len(traditional_labels) - 1):
    fig.add_trace(go.Scatter(
        x=[0.5, 0.5],
        y=[traditional_y[i], traditional_y[i+1]],
        mode='lines',
        line=dict(color='#4ECDC4', width=3),
        showlegend=False,
        cliponaxis=False
    ))
    # Add arrow marker
    fig.add_trace(go.Scatter(
        x=[0.5],
        y=[traditional_y[i+1]],
        mode='markers',
        marker=dict(size=10, color='#4ECDC4', symbol='triangle-down'),
        showlegend=False,
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title='Development Process Comparison',
    xaxis_title='',
    yaxis_title='Process Steps',
    yaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[-1, max(len(houston_labels), len(traditional_labels))]
    ),
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[-1.5, 1.5]
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    showlegend=True
)

# Save the chart
fig.write_image('development_process_comparison.png')