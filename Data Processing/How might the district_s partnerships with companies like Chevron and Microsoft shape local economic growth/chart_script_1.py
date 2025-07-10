import plotly.graph_objects as go

# Data from the provided JSON
data = {
    "employment_impact": {"direct": 5780, "indirect": 2895, "induced": 4477, "total": 13152, "multiplier": 2.28},
    "economic_output": {"direct": 1019.7, "indirect": 472.4, "induced": 640.6, "total": 2132.7, "multiplier": 2.09},
    "categories": ["Direct", "Indirect", "Induced"],
    "units": {"employment": "Jobs", "output": "Millions USD"}
}

# Extract data for the chart
employment_data = [data["employment_impact"]["direct"], data["employment_impact"]["indirect"], data["employment_impact"]["induced"]]
output_data = [data["economic_output"]["direct"], data["economic_output"]["indirect"], data["economic_output"]["induced"]]

# Colors for direct, indirect, and induced effects
colors = ['#1FB8CD', '#FFC185', '#ECEBD5']

# Create categories for x-axis (employment and output sections)
x_categories = ['Direct Jobs', 'Indirect Jobs', 'Induced Jobs', 'Direct Output', 'Indirect Output', 'Induced Output']

# Combine data (scale employment by 1000 for better visualization)
y_values = [val/1000 for val in employment_data] + [val/1000 for val in output_data]

# Create colors array matching the data
bar_colors = colors + colors

# Create bar chart
fig = go.Figure(data=[
    go.Bar(
        x=x_categories,
        y=y_values,
        marker_color=bar_colors,
        text=[f'{val/1000:.1f}k jobs' for val in employment_data] + [f'${val:.0f}m' for val in output_data],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>%{text}<extra></extra>',
        showlegend=False
    )
])

# Update layout
fig.update_layout(
    title='Houston Innovation District Impact<br><sub>Total regional economic impact of innovation district activities</sub>',
    xaxis_title='Impact Category',
    yaxis_title='Value (Jobs in 1000s, Output in $M)',
    annotations=[
        dict(
            text="Employment Multiplier: 2.28x",
            x=1, y=max(y_values) * 0.9,
            xref="x", yref="y",
            showarrow=False,
            font=dict(size=12)
        ),
        dict(
            text="Output Multiplier: 2.09x",
            x=4, y=max(y_values) * 0.9,
            xref="x", yref="y",
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

# Add vertical line to separate employment from output
fig.add_vline(x=2.5, line_dash="dash", line_color="gray", opacity=0.5)

fig.write_image('houston_economic_impact.png')