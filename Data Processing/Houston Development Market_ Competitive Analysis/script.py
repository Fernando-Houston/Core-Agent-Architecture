import pandas as pd
import numpy as np

# Create data for major Houston developers and their current projects/activities
developers_data = {
    'Developer': [
        'D.R. Horton',
        'Lennar Homes', 
        'Perry Homes',
        'Century Communities',
        'David Weekley Homes',
        'Hines',
        'Howard Hughes Corporation',
        'Johnson Development',
        'Midway',
        'Land Tejas/Starwood Land',
        'Wolff Companies',
        'Windham Development',
        'Westin Homes',
        'Taylor Morrison',
        'Meritage Homes'
    ],
    'January 2025 Permits': [326, 318, 183, 143, 88, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Average Home Value ($)': [262482, 244463, 322269, 250985, 332542, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Type': ['Residential', 'Residential', 'Residential', 'Residential', 'Residential', 
             'Mixed-Use', 'Mixed-Use', 'Mixed-Use', 'Mixed-Use', 'Mixed-Use',
             'Commercial', 'Residential', 'Residential', 'Residential', 'Residential'],
    'Major Projects 2024': [
        'Breckenridge Forest, City Gate, Park\'s Edge',
        'Flagstone, Piccolina, Tavola Collections',
        'Artavia, Elyson, Sienna, Candela',
        'Laurel Farms, Mavera',
        'Cross Creek Ranch, Briarley',
        'East River, Discovery Green projects',
        'Bridgeland master-planned community',
        '20 active communities, 100+ model homes',
        'East River, CityCentre expansions',
        'Sunterra, Marvida developments',
        'Beacon Hill, Central Park, Ten Oaks',
        'Indian Springs, Mesa Vista, Gulf Breeze',
        'Premium communities across Houston',
        'Cross Creek West, Audubon',
        'Harper\'s Preserve, Artavia 60ft lots'
    ]
}

# Create DataFrame
df_developers = pd.DataFrame(developers_data)

# Display the data
print("Major Houston Developers - Current Activity (2024-2025)")
print("=" * 60)
print(df_developers[['Developer', 'January 2025 Permits', 'Type', 'Major Projects 2024']])

# Save to CSV for chart creation
df_developers.to_csv('houston_developers_2024.csv', index=False)
print("\nData saved to houston_developers_2024.csv")