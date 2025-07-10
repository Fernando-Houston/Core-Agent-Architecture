# Create data for Houston commercial development trends by sector
commercial_sectors = {
    'Sector': [
        'Office',
        'Retail',
        'Industrial/Warehouse',
        'Multifamily',
        'Mixed-Use',
        'Medical/Healthcare',
        'Hospitality'
    ],
    'Under Construction (Million SF)': [0.6, 3.7, 25.4, 8.5, 12.3, 2.1, 1.8],
    'Vacancy Rate (%)': [27.0, 5.2, 3.8, 6.8, 8.5, 4.2, 12.5],
    'Market Trend': ['Declining', 'Growing', 'Strong Growth', 'Stable', 'Growing', 'Stable', 'Recovery'],
    'Key Projects': [
        '1550 on the Green, Texas Tower',
        'Manvel Town Center, Swift Building',
        'Kingsland Ranch, Tesla Megapack facility',
        'Pearl at Midlane, Lockwood development',
        'East River, GreenStreet, Ashford Yard',
        'MD Anderson expansions, TMC developments',
        'Post Oak Hotel area, downtown hotels'
    ]
}

df_commercial = pd.DataFrame(commercial_sectors)

print("Houston Commercial Development by Sector (2024-2025)")
print("=" * 60)
print(df_commercial)

# Save to CSV
df_commercial.to_csv('houston_commercial_sectors_2024.csv', index=False)
print("\nData saved to houston_commercial_sectors_2024.csv")