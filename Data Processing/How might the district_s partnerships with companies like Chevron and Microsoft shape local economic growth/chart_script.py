import plotly.graph_objects as go
import plotly.io as pio

# Create a vertical flowchart showing corporate partnership flow
fig = go.Figure()

# Define positions for each level
corporate_y = 3
activities_y = 2
impact_y = 1

# Corporate Investment Level (top)
fig.add_trace(go.Scatter(
    x=[1, 3, 5],
    y=[corporate_y, corporate_y, corporate_y],
    mode='markers+text',
    marker=dict(size=120, color=['#1FB8CD', '#FFC185', '#ECEBD5']),
    text=['Microsoft<br>$1+ million', 'Chevron Tech<br>$350+ million', 'Partnership<br>Programs'],
    textposition='middle center',
    textfont=dict(size=10, color='white'),
    showlegend=False,
    hovertemplate='<b>%{text}</b><extra></extra>'
))

# Direct Activities Level (middle)
fig.add_trace(go.Scatter(
    x=[0.5, 1.5, 2.5, 3.5, 4.5],
    y=[activities_y, activities_y, activities_y, activities_y, activities_y],
    mode='markers+text',
    marker=dict(size=100, color=['#5D878F', '#D2BA4C', '#B4413C', '#964325', '#944454']),
    text=['Workforce<br>Dev', 'Startup<br>Accel', 'R&D<br>Partners', 'Tech<br>Transfer', 'Supplier<br>Dev'],
    textposition='middle center',
    textfont=dict(size=9, color='white'),
    showlegend=False,
    hovertemplate='<b>%{text}</b><extra></extra>'
))

# Economic Impact Level (bottom)
fig.add_trace(go.Scatter(
    x=[0.5, 1.5, 2.5, 3.5, 4.5],
    y=[impact_y, impact_y, impact_y, impact_y, impact_y],
    mode='markers+text',
    marker=dict(size=110, color=['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C']),
    text=['Jobs<br>13.2k', 'Output<br>$2.1b', 'Tax Rev<br>$255m', 'New Biz<br>Formation', 'Innovation<br>Ecosystem'],
    textposition='middle center',
    textfont=dict(size=9, color='white'),
    showlegend=False,
    hovertemplate='<b>%{text}</b><extra></extra>'
))

# Add arrows showing flow from corporate to activities
arrow_props = dict(arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#13343B')

# Microsoft to activities
fig.add_annotation(x=1, y=corporate_y-0.15, ax=0.5, ay=activities_y+0.15, **arrow_props)
fig.add_annotation(x=1, y=corporate_y-0.15, ax=1.5, ay=activities_y+0.15, **arrow_props)
fig.add_annotation(x=1, y=corporate_y-0.15, ax=2.5, ay=activities_y+0.15, **arrow_props)

# Chevron to activities
fig.add_annotation(x=3, y=corporate_y-0.15, ax=1.5, ay=activities_y+0.15, **arrow_props)
fig.add_annotation(x=3, y=corporate_y-0.15, ax=2.5, ay=activities_y+0.15, **arrow_props)
fig.add_annotation(x=3, y=corporate_y-0.15, ax=3.5, ay=activities_y+0.15, **arrow_props)
fig.add_annotation(x=3, y=corporate_y-0.15, ax=4.5, ay=activities_y+0.15, **arrow_props)

# Partnership programs to activities
fig.add_annotation(x=5, y=corporate_y-0.15, ax=0.5, ay=activities_y+0.15, **arrow_props)
fig.add_annotation(x=5, y=corporate_y-0.15, ax=1.5, ay=activities_y+0.15, **arrow_props)
fig.add_annotation(x=5, y=corporate_y-0.15, ax=4.5, ay=activities_y+0.15, **arrow_props)

# Add arrows from activities to impact
fig.add_annotation(x=0.5, y=activities_y-0.15, ax=0.5, ay=impact_y+0.15, **arrow_props)
fig.add_annotation(x=1.5, y=activities_y-0.15, ax=1.5, ay=impact_y+0.15, **arrow_props)
fig.add_annotation(x=2.5, y=activities_y-0.15, ax=2.5, ay=impact_y+0.15, **arrow_props)
fig.add_annotation(x=3.5, y=activities_y-0.15, ax=3.5, ay=impact_y+0.15, **arrow_props)
fig.add_annotation(x=4.5, y=activities_y-0.15, ax=4.5, ay=impact_y+0.15, **arrow_props)

# Cross-connections from activities to multiple impacts
fig.add_annotation(x=0.5, y=activities_y-0.15, ax=1.5, ay=impact_y+0.15, **arrow_props)
fig.add_annotation(x=1.5, y=activities_y-0.15, ax=0.5, ay=impact_y+0.15, **arrow_props)
fig.add_annotation(x=2.5, y=activities_y-0.15, ax=1.5, ay=impact_y+0.15, **arrow_props)
fig.add_annotation(x=3.5, y=activities_y-0.15, ax=2.5, ay=impact_y+0.15, **arrow_props)
fig.add_annotation(x=4.5, y=activities_y-0.15, ax=3.5, ay=impact_y+0.15, **arrow_props)

# Add level labels
fig.add_annotation(x=-0.5, y=corporate_y, text="Corporate<br>Investment", showarrow=False, 
                   font=dict(size=14, color='#13343B'), xanchor='center')
fig.add_annotation(x=-0.5, y=activities_y, text="Direct<br>Activities", showarrow=False, 
                   font=dict(size=14, color='#13343B'), xanchor='center')
fig.add_annotation(x=-0.5, y=impact_y, text="Economic<br>Impact", showarrow=False, 
                   font=dict(size=14, color='#13343B'), xanchor='center')

# Update layout
fig.update_layout(
    title_text="Corporate Partnership Economic Flow",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 6]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.5, 3.5]),
    plot_bgcolor='white'
)

# Update traces with cliponaxis
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("corporate_partnership_flow.png")
print("Chart saved as corporate_partnership_flow.png")