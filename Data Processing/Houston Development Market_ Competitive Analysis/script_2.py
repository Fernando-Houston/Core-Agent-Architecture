# Create comprehensive data about Houston land acquisition strategies
land_acquisition_data = {
    'Developer/Strategy': [
        'Starwood Land/Land Tejas',
        'Hines',
        'Howard Hughes Corporation',
        'Johnson Development',
        'Midway',
        'Wolff Companies',
        'Windy Hill Development',
        'Rooted Development',
        'Texas Group',
        'SYI Development',
        'MAK Development Group',
        'Venture Capital/Private Equity',
        'Public-Private Partnerships',
        'International Investors',
        'Regional Developers'
    ],
    'Primary Strategy': [
        'Master-planned communities acquisition',
        'Mixed-use urban development',
        'Large-scale master planning',
        'Suburban master communities',
        'Urban redevelopment/adaptive reuse',
        'Commercial corridor development',
        'Large tract residential development',
        'Master-planned residential focus',
        'Subdivision development for builders',
        'Mixed-use commercial development',
        'Residential/mixed-use development',
        'Opportunistic value-add acquisitions',
        'Infrastructure-tied development',
        'Trophy asset acquisitions',
        'Infill/suburban expansion'
    ],
    'Focus Areas': [
        'Katy, Cypress, Montgomery County',
        'Downtown, Energy Corridor, TMC',
        'Bridgeland, The Woodlands area',
        'Fulshear, Missouri City, Conroe',
        'East River, CityCentre, Energy Corridor',
        'I-10 West, Energy Corridor',
        'Grand Parkway, 290 Corridor',
        'Greater Houston suburban',
        'Metro-wide subdivision development',
        'Mixed-use development areas',
        'Houston metro residential',
        'Value-add properties metro-wide',
        'Major infrastructure corridors',
        'Premium locations (River Oaks, etc.)',
        'Emerging suburban markets'
    ],
    'Recent Activity Scale': [
        'Large ($800M+ portfolio)',
        'Large ($2B+ projects)',
        'Large (11,500+ acres)',
        'Large (20+ communities)',
        'Large (Multi-billion projects)',
        'Medium (Multiple projects)',
        'Medium (300+ acre projects)',
        'Medium (Regional focus)',
        'Medium (Builder-focused)',
        'Medium (Commercial focus)',
        'Small (Local projects)',
        'Large (Institutional scale)',
        'Large (Infrastructure scale)',
        'Large (Trophy acquisitions)',
        'Medium (Market-specific)'
    ],
    'Key Trends': [
        'Portfolio acquisitions from major developers',
        'Transit-oriented development focus',
        'Long-term master planning approach',
        'Suburban amenity-rich communities',
        'Urban core redevelopment/adaptive reuse',
        'Energy sector-focused development',
        'Grand Parkway corridor expansion',
        'Builder partnership model',
        'National builder acquisition focus',
        'Commercial mixed-use emphasis',
        'Residential/commercial mixed development',
        'Distressed asset opportunities',
        'Public infrastructure alignment',
        'Luxury/trophy asset focus',
        'Market-specific opportunities'
    ]
}

df_land_strategies = pd.DataFrame(land_acquisition_data)

print("Houston Land Acquisition Strategies by Developer Type (2024)")
print("=" * 80)
print(df_land_strategies[['Developer/Strategy', 'Primary Strategy', 'Focus Areas', 'Recent Activity Scale']])

# Save to CSV
df_land_strategies.to_csv('houston_land_acquisition_strategies_2024.csv', index=False)
print("\nData saved to houston_land_acquisition_strategies_2024.csv")

# Create summary statistics
print("\n" + "="*50)
print("SUMMARY STATISTICS")
print("="*50)

activity_scale_counts = df_land_strategies['Recent Activity Scale'].value_counts()
print("\nActivity Scale Distribution:")
for scale, count in activity_scale_counts.items():
    print(f"  {scale}: {count} entities")

# Geographic focus analysis
geographic_focus = {}
for areas in df_land_strategies['Focus Areas']:
    locations = [area.strip() for area in areas.split(',')]
    for location in locations:
        if location in geographic_focus:
            geographic_focus[location] += 1
        else:
            geographic_focus[location] = 1

print("\nMost Targeted Geographic Areas:")
sorted_areas = sorted(geographic_focus.items(), key=lambda x: x[1], reverse=True)
for area, count in sorted_areas[:10]:
    print(f"  {area}: {count} developers")