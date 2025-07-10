import pandas as pd

# Create a comprehensive summary table of Harris County environmental programs and their status
environmental_programs = {
    'Program/Initiative': [
        'FEMA Flood Map Updates',
        'Harris County Climate Action Plan',
        'Gulf Coast Protection District',
        'Coastal Texas Project',
        'EPA Solar for All Grant',
        'Air Quality Monitoring (CAMP)',
        'PM2.5 Standards Compliance',
        'Ozone Nonattainment Status',
        'Harris County Flood Control Bonds',
        'Environmental Justice Programs'
    ],
    'Current Status': [
        'Delayed to 2025',
        'Approved - 40% GHG reduction by 2030',
        'Operational since 2021',
        'Design phase initiated 2024',
        '$249.7M awarded to Harris County coalition',
        'Active in 8+ communities',
        'Likely nonattainment designation',
        'Serious nonattainment (2015 standard)',
        '$2.5B approved 2018, ongoing projects',
        'Multiple EPA grants awarded 2024'
    ],
    'Key Impact': [
        'Expanded flood zones expected',
        'County operations carbon reduction',
        '5-county coastal protection oversight',
        '$34.4B hurricane protection system',
        '20%+ utility bill reductions',
        'Real-time pollution monitoring',
        'Stricter health protection standards',
        'Required emissions reductions',
        'Enhanced flood infrastructure',
        'Community-based environmental advocacy'
    ],
    'Timeline': [
        '2025',
        '2023-2030',
        '2021-ongoing',
        '2024-2030s',
        '2024-2030',
        '2020-ongoing',
        '2024-2027',
        '2018-2027',
        '2018-ongoing',
        '2024-ongoing'
    ]
}

df = pd.DataFrame(environmental_programs)

# Save as CSV for reference
df.to_csv('harris_county_environmental_programs.csv', index=False)

print("Harris County Environmental and Risk Intelligence Programs Summary")
print("=" * 70)
print(df.to_string(index=False))
print(f"\nTotal programs tracked: {len(df)}")
print(f"Data saved to: harris_county_environmental_programs.csv")