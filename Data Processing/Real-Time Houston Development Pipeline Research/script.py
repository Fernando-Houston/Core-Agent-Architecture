import pandas as pd

# Create a comprehensive table of Houston development projects
development_data = [
    {
        'Project Name': 'Terminal B Transformation',
        'Investment': '$2.55 billion',
        'Timeline': '2024-2026',
        'Status': 'Under Construction',
        'Category': 'Transportation',
        'Description': 'Complete overhaul of IAH Terminal B with new gates, processor, and facilities'
    },
    {
        'Project Name': 'George R. Brown Convention Center',
        'Investment': '$2.0 billion',
        'Timeline': '2025-2028',
        'Status': 'Planning/Design',
        'Category': 'Entertainment',
        'Description': 'Major transformation including 700,000 sq ft building and Central Plaza'
    },
    {
        'Project Name': 'Harris Health LBJ Hospital',
        'Investment': '$1.6 billion',
        'Timeline': '2024-2028',
        'Status': 'Under Construction',
        'Category': 'Healthcare',
        'Description': '12-story Level I trauma-capable facility with 390 private rooms'
    },
    {
        'Project Name': 'IAH Terminal Redevelopment',
        'Investment': '$1.46 billion',
        'Timeline': '2019-2025',
        'Status': 'Final Phase',
        'Category': 'Transportation',
        'Description': 'Terminal D-West Pier completed, International Central Processor ongoing'
    },
    {
        'Project Name': 'Park Eight Place',
        'Investment': '$1.0 billion',
        'Timeline': '2025-2028',
        'Status': 'Planning',
        'Category': 'Mixed-Use',
        'Description': '70-acre mixed-use development on former Halliburton campus'
    },
    {
        'Project Name': 'Buffalo Bayou East',
        'Investment': '$310 million',
        'Timeline': '2022-2032',
        'Status': 'Phase 1 Complete',
        'Category': 'Parks/Recreation',
        'Description': '10-year plan extending Buffalo Bayou Park into East End and Fifth Ward'
    },
    {
        'Project Name': 'Houston Methodist West Hospital',
        'Investment': '$247 million',
        'Timeline': '2024-2027',
        'Status': 'Under Construction',
        'Category': 'Healthcare',
        'Description': '129,000 sq ft expansion with 36-bed observation unit and new ORs'
    },
    {
        'Project Name': 'HCA North Cypress',
        'Investment': '$100 million',
        'Timeline': '2024-2026',
        'Status': 'Under Construction',
        'Category': 'Healthcare',
        'Description': 'Patient tower with 22-bed rehabilitation unit and 31-bed medical surgical unit'
    },
    {
        'Project Name': 'Galleria Renovations',
        'Investment': '$50 million',
        'Timeline': '2024-2025',
        'Status': 'Under Construction',
        'Category': 'Retail',
        'Description': 'Interior/exterior revitalization including 155,000 sq ft of new flooring'
    },
    {
        'Project Name': 'Main Street Promenade',
        'Investment': '$12 million',
        'Timeline': '2025-2026',
        'Status': 'Under Construction',
        'Category': 'Urban Development',
        'Description': 'Seven-block pedestrian-friendly corridor in downtown Houston'
    }
]

df = pd.DataFrame(development_data)

# Save to CSV
df.to_csv('houston_development_projects.csv', index=False)

print("Houston Development Projects Summary")
print("=" * 50)
print(f"Total Projects: {len(df)}")
print(f"Total Investment: Over $10 billion")
print(f"Categories: {', '.join(df['Category'].unique())}")
print("\nProject Details:")
print(df.to_string(index=False))

# Create a summary by category
category_summary = df.groupby('Category').agg({
    'Investment': 'count',
    'Project Name': lambda x: ', '.join(x[:2])  # Show first 2 projects in each category
}).rename(columns={'Investment': 'Number of Projects', 'Project Name': 'Sample Projects'})

print("\n\nSummary by Category:")
print("=" * 50)
print(category_summary.to_string())