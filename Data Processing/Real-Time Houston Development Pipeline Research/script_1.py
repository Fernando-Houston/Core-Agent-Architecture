# Create a comprehensive summary of Houston infrastructure and permit data
import pandas as pd

# Infrastructure Projects Data
infrastructure_data = [
    {
        'Project': 'Spring Cypress Road Rehabilitation',
        'Investment': '$6.5 million',
        'Timeline': '2024-2026',
        'Area': 'Harris County Precinct 3',
        'Status': 'Under Construction',
        'Type': 'Road Infrastructure'
    },
    {
        'Project': 'Holderrieth Road Segment 2',
        'Investment': '$31.2 million',
        'Timeline': '2024-2026',
        'Area': 'Harris County Precinct 3',
        'Status': 'Under Construction',
        'Type': 'Road Infrastructure'
    },
    {
        'Project': 'METRORapid Gulfton Corridor',
        'Investment': '$220 million',
        'Timeline': '2024-2027',
        'Area': 'Southwest Houston',
        'Status': 'Planning',
        'Type': 'Public Transit'
    },
    {
        'Project': 'METRO Maintenance of Way Facility',
        'Investment': '$30 million',
        'Timeline': '2024-2026',
        'Area': 'Burnett Transit Center',
        'Status': 'Under Construction',
        'Type': 'Public Transit'
    },
    {
        'Project': 'Kuykendahl Road Expansion',
        'Investment': '$12.5 million',
        'Timeline': '2024-2025',
        'Area': 'Harris County Precinct 3',
        'Status': 'Under Construction',
        'Type': 'Road Infrastructure'
    },
    {
        'Project': 'Gosling Road Bridge',
        'Investment': '$9.4 million',
        'Timeline': '2024-2025',
        'Area': 'Harris County Precinct 3',
        'Status': 'Under Construction',
        'Type': 'Bridge/Infrastructure'
    },
    {
        'Project': 'Harris County Flood Control Projects',
        'Investment': '$715 million',
        'Timeline': '2024-2027',
        'Area': 'Harris County',
        'Status': 'Ongoing',
        'Type': 'Flood Control'
    },
    {
        'Project': 'Post Oak Boulevard Improvements',
        'Investment': '$192 million',
        'Timeline': '2023-2025',
        'Area': 'Galleria/Uptown',
        'Status': 'Final Phase',
        'Type': 'Road Infrastructure'
    }
]

# Construction Permits Data (Recent Statistics)
permits_data = [
    {
        'Month': 'May 2025',
        'Houston Metro Permits': 3118,
        'Construction Value': '$923.7 million',
        'Average Value': '$296,235',
        'Leading Counties': 'Harris (1,532), Montgomery (858)'
    },
    {
        'Month': 'Jan-Feb 2025',
        'Houston Metro Permits': 11000,
        'Construction Value': '$3.26 billion',
        'Average Value': '$296,363',
        'Leading Counties': 'Harris, Montgomery, Fort Bend'
    },
    {
        'Month': '2024 Total',
        'Houston Metro Permits': 52851,
        'Construction Value': '$15.6 billion',
        'Average Value': '$295,000',
        'Leading Counties': 'Harris, Montgomery, Fort Bend'
    }
]

# Create DataFrames
infrastructure_df = pd.DataFrame(infrastructure_data)
permits_df = pd.DataFrame(permits_data)

# Save to CSV files
infrastructure_df.to_csv('houston_infrastructure_projects.csv', index=False)
permits_df.to_csv('houston_construction_permits.csv', index=False)

print("HOUSTON INFRASTRUCTURE PROJECTS 2024-2025")
print("=" * 50)
print(infrastructure_df.to_string(index=False))

print("\n\nHOUSTON CONSTRUCTION PERMITS - RECENT DATA")
print("=" * 50)
print(permits_df.to_string(index=False))

# Summary statistics
total_infrastructure_investment = infrastructure_df['Investment'].str.replace('$', '').str.replace(' million', '').str.replace(' billion', '000').astype(float).sum()
print(f"\n\nSUMMARY STATISTICS")
print("=" * 50)
print(f"Total Infrastructure Investment: ${total_infrastructure_investment:,.0f} million")
print(f"Number of Major Infrastructure Projects: {len(infrastructure_df)}")
print(f"Houston Leading US in Building Permits: Yes (52,851 permits in 2024)")
print(f"Projected 2025 Permits: ~40,000 (decline due to higher interest rates)")

# Project types breakdown
project_types = infrastructure_df['Type'].value_counts()
print(f"\nInfrastructure Project Types:")
for ptype, count in project_types.items():
    print(f"  {ptype}: {count} projects")