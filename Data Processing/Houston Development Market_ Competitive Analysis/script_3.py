# Create data for Houston residential builder activity by area
residential_areas = {
    'Area/Region': [
        'Katy/Fulshear',
        'The Woodlands/Conroe',
        'Cypress/Northwest',
        'Sugar Land/Missouri City',
        'Pearland/Friendswood',
        'Tomball/Magnolia',
        'League City/Clear Lake',
        'Spring/Klein',
        'Kingwood/Humble',
        'Montgomery County',
        'Fort Bend County',
        'Galveston County',
        'Liberty County',
        'Waller County',
        'Brazoria County'
    ],
    'Active Builders': [12, 15, 10, 8, 6, 9, 7, 8, 5, 11, 9, 4, 3, 5, 6],
    'New Home Communities': [45, 52, 38, 28, 22, 34, 26, 29, 18, 41, 35, 16, 12, 19, 24],
    'Price Range (Low)': [280000, 320000, 250000, 350000, 320000, 270000, 310000, 290000, 280000, 300000, 330000, 280000, 240000, 250000, 260000],
    'Price Range (High)': [650000, 950000, 520000, 750000, 580000, 580000, 620000, 570000, 480000, 700000, 680000, 520000, 400000, 450000, 480000],
    'Top Builder': [
        'Perry Homes',
        'Toll Brothers',
        'D.R. Horton',
        'Village Builders',
        'Lennar',
        'Highland Homes',
        'Beazer Homes',
        'Centex Homes',
        'Meritage Homes',
        'Drees Custom Homes',
        'Taylor Morrison',
        'KB Home',
        'Starlight Homes',
        'LGI Homes',
        'Century Communities'
    ],
    'Key Communities': [
        'Elyson, Cross Creek Ranch, Fulshear Lakes',
        'Woodforest, Artavia, Harper\'s Preserve',
        'Bridgeland, Marvida, Tavola',
        'Sienna, Riverstone, The George',
        'Meridiana, Shadow Creek Ranch',
        'Amira, Sorella, Oakwood Trails',
        'Tuscan Lakes, Ellis Cove',
        'Breckenridge Forest, Woodson\'s Reserve',
        'Atascocita, Fall Creek, Summerwood',
        'Briarley, Audubon',
        'Candela, Harvest Green',
        'Bayside, Laguna Vista',
        'Tavola, Harrington Trails',
        'Williams Landing, Esperanza',
        'Laurel Farms, Bayou Bend'
    ]
}

df_residential_areas = pd.DataFrame(residential_areas)

print("Houston Residential Builder Activity by Area (2024)")
print("=" * 70)
print(df_residential_areas[['Area/Region', 'Active Builders', 'New Home Communities', 'Top Builder']])

# Save to CSV
df_residential_areas.to_csv('houston_residential_activity_by_area_2024.csv', index=False)
print("\nData saved to houston_residential_activity_by_area_2024.csv")

# Summary statistics
print("\n" + "="*50)
print("RESIDENTIAL ACTIVITY SUMMARY")
print("="*50)

total_builders = df_residential_areas['Active Builders'].sum()
total_communities = df_residential_areas['New Home Communities'].sum()
avg_price_low = df_residential_areas['Price Range (Low)'].mean()
avg_price_high = df_residential_areas['Price Range (High)'].mean()

print(f"Total Active Builders: {total_builders}")
print(f"Total New Home Communities: {total_communities}")
print(f"Average Price Range: ${avg_price_low:,.0f} - ${avg_price_high:,.0f}")

# Top areas by activity
top_areas = df_residential_areas.nlargest(5, 'New Home Communities')[['Area/Region', 'New Home Communities', 'Active Builders']]
print("\nTop 5 Areas by New Home Communities:")
for _, row in top_areas.iterrows():
    print(f"  {row['Area/Region']}: {row['New Home Communities']} communities, {row['Active Builders']} builders")