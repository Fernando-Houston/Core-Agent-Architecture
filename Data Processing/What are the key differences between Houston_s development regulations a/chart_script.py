import plotly.graph_objects as go
import json

# Load the comparison data
data = {
    "comparison_data": [
        {"aspect": "Land Use Control", "houston": "No use-based zoning districts", "traditional": "Mandatory use-based districts (R1, C1, I1, etc.)"},
        {"aspect": "Primary Regulations", "houston": "Deed restrictions (private, voluntary)", "traditional": "Municipal zoning ordinances"},
        {"aspect": "Governing Bodies", "houston": "Subdivision ordinances", "traditional": "Planning commissions"},
        {"aspect": "Appeals Process", "houston": "Development codes", "traditional": "Zoning boards of appeals"},
        {"aspect": "Development Pattern", "houston": "Market-driven land use", "traditional": "Government-controlled land use"},
        {"aspect": "Flexibility", "houston": "Flexible development patterns", "traditional": "Predetermined development patterns"},
        {"aspect": "Enforcement", "houston": "Private enforcement mechanisms", "traditional": "Government enforcement"},
        {"aspect": "Coverage", "houston": "City enforces some deed restrictions", "traditional": "Comprehensive zoning maps"}
    ]
}

# Extract data for the table
aspects = []
houston_values = []
traditional_values = []

for item in data["comparison_data"]:
    aspects.append(item["aspect"])
    houston_values.append(item["houston"])
    traditional_values.append(item["traditional"])

# Create the table
fig = go.Figure(data=[go.Table(
    header=dict(
        values=["Aspect", "Houston Dev Regs", "Traditional Zone"],
        fill_color='#1FB8CD',
        align='left',
        font=dict(color='white', size=14)
    ),
    cells=dict(
        values=[aspects, houston_values, traditional_values],
        fill_color=[['#ECEBD5', '#FFC185'] * 4],
        align='left',
        font=dict(color='black', size=12),
        height=40
    )
)])

fig.update_layout(
    title="Houston vs Traditional Zoning Laws"
)

# Save the chart
fig.write_image("houston_zoning_comparison.png")