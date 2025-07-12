import plotly.graph_objects as go
import plotly.express as px

# Data
data = [
    {"District": "Katy ISD", "Change": 11935},
    {"District": "Lamar CISD", "Change": 10267},
    {"District": "Conroe ISD", "Change": 8351},
    {"District": "Houston ISD", "Change": -20216},
    {"District": "Aldine ISD", "Change": -6883},
    {"District": "Pasadena ISD", "Change": -4123}
]

# Sort by change value (ascending order so largest gain appears at top)
data_sorted = sorted(data, key=lambda x: x['Change'], reverse=False)

# Extract districts and changes
districts = [d['District'] for d in data_sorted]
changes = [d['Change'] for d in data_sorted]

# Create colors (green for positive, red for negative)
colors = ['green' if change > 0 else 'red' for change in changes]

# Create text labels with better positioning
text_labels = []
text_positions = []
for change in changes:
    text_labels.append(f"{change:,}")
    if change < 0:
        text_positions.append('inside')
    else:
        text_positions.append('outside')

# Create horizontal bar chart
fig = go.Figure(go.Bar(
    x=changes,
    y=districts,
    orientation='h',
    marker_color=colors,
    text=text_labels,
    textposition=text_positions,
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title="Houston-Area School District Enrollment Change, 2020-2025",
    xaxis_title="Change in Students",
    yaxis_title="",
    showlegend=False
)

# Save the chart
fig.write_image("enrollment_change_chart.png")