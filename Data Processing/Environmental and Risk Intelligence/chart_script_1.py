import plotly.graph_objects as go
import plotly.io as pio

# Data from the provided instructions (correcting the Non-Federal amount)
funding_data = [
    {"program": "Coastal Texas Project (Federal)", "amount": 19410, "type": "Federal Infrastructure"},
    {"program": "Harris County Flood Control Bonds", "amount": 2500, "type": "Local Bonds"},
    {"program": "Coastal Texas Project (Non-Federal)", "amount": 11790, "type": "State/Local"},
    {"program": "EPA Solar for All Grant", "amount": 249.7, "type": "Federal Grant"},
    {"program": "EPA Climate Pollution Reduction Grant", "amount": 1.0, "type": "Federal Grant"},
    {"program": "EPA Community Air Monitoring Grant", "amount": 0.5, "type": "Federal Grant"}
]

# Sort by amount descending for better visualization
funding_data_sorted = sorted(funding_data, key=lambda x: x['amount'], reverse=True)

# Extract data for plotting
programs = [item['program'] for item in funding_data_sorted]
amounts = [item['amount'] for item in funding_data_sorted]
types = [item['type'] for item in funding_data_sorted]

# Abbreviate program names to fit 15 character limit for labels
abbreviated_programs = []
for program in programs:
    if "Coastal Texas Project (Federal)" in program:
        abbreviated_programs.append("Coastal TX Fed")
    elif "Harris County Flood Control Bonds" in program:
        abbreviated_programs.append("HC Flood Bonds")
    elif "Coastal Texas Project (Non-Federal)" in program:
        abbreviated_programs.append("Coastal TX NF")
    elif "EPA Solar for All Grant" in program:
        abbreviated_programs.append("EPA Solar")
    elif "EPA Climate Pollution Reduction Grant" in program:
        abbreviated_programs.append("EPA Climate")
    elif "EPA Community Air Monitoring Grant" in program:
        abbreviated_programs.append("EPA Air Mon")
    else:
        abbreviated_programs.append(program[:15])

# Brand colors mapped by type
type_colors = {
    'Federal Infrastructure': '#1FB8CD',
    'State/Local': '#FFC185', 
    'Local Bonds': '#ECEBD5',
    'Federal Grant': '#5D878F'
}

bar_colors = [type_colors[t] for t in types]

# Format amounts for display (with "m", "b" abbreviations)
def format_amount(amount):
    if amount >= 1000:
        return f"${amount/1000:.1f}b"
    else:
        return f"${amount:.0f}m"

formatted_amounts = [format_amount(amount) for amount in amounts]

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        y=abbreviated_programs,
        x=amounts,
        orientation='h',
        marker_color=bar_colors,
        text=formatted_amounts,
        textposition='outside',
        cliponaxis=False,
        hovertemplate='<b>%{y}</b><br>Amount: $%{x:.0f}M<br><extra></extra>'
    )
])

# Update layout
fig.update_layout(
    title="Environmental Grants - Houston Region<br><sub>Major Environmental Investments</sub>",
    xaxis_title="Amount ($M)",
    yaxis_title="Program"
)

# Save the chart
fig.write_image("environmental_grants_chart.png")