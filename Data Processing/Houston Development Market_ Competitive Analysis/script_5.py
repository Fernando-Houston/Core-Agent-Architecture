# Create comprehensive analysis summary
analysis_summary = {
    'Analysis Category': [
        'Market Leadership',
        'Geographic Expansion',
        'Development Strategy',
        'Land Acquisition',
        'Competitive Positioning',
        'Market Trends',
        'Investment Patterns',
        'Infrastructure Impact',
        'Economic Drivers',
        'Future Outlook'
    ],
    'Key Findings': [
        'D.R. Horton and Lennar dominate residential with 644 permits combined',
        'Grand Parkway corridor and Northwest Far submarket leading growth',
        'Shift toward master-planned communities and mixed-use developments',
        'Large portfolio acquisitions ($800M+ deals) and strategic partnerships',
        'Flight to quality in office, industrial/warehouse sector strength',
        'Smaller residential lots, suburban retail focus, urban core redevelopment',
        'Industrial leading with $25.4M SF, mixed-use at $12.3M SF',
        'Streamlined permitting, public-private partnerships increasing',
        'Population growth (+125K), employment growth (+53.7K jobs)',
        'Continued suburban expansion, industrial strength, mixed-use focus'
    ],
    'Competitive Implications': [
        'Consolidation among top builders, scale advantages critical',
        'Early positioning in growth corridors provides competitive advantage',
        'Amenity-rich, walkable communities increasingly differentiated',
        'Financial capacity for large deals separates major from minor players',
        'Quality and location trump quantity in current market',
        'Adaptation to changing consumer preferences essential',
        'Industrial/warehouse development offers strongest returns',
        'Regulatory relationships and process expertise valuable',
        'Houston remains attractive for corporate relocations',
        'Long-term growth prospects support continued investment'
    ],
    'Strategic Recommendations': [
        'Focus on scale and operational efficiency',
        'Prioritize Grand Parkway and emerging suburban corridors',
        'Invest in master-planning and mixed-use capabilities',
        'Build financial capacity for portfolio acquisitions',
        'Emphasize quality, amenities, and strategic locations',
        'Develop flexible, adaptable development models',
        'Consider industrial/warehouse development opportunities',
        'Strengthen relationships with regulatory bodies',
        'Leverage Houston\'s economic diversity and growth',
        'Maintain long-term perspective on market cycles'
    ]
}

df_analysis = pd.DataFrame(analysis_summary)

print("Houston Development Market - Competitive Analysis Summary")
print("=" * 80)
print(df_analysis)

# Save to CSV
df_analysis.to_csv('houston_competitive_analysis_2024.csv', index=False)
print("\nData saved to houston_competitive_analysis_2024.csv")

# Create final statistics summary
print("\n" + "="*80)
print("HOUSTON DEVELOPMENT MARKET - KEY STATISTICS 2024")
print("="*80)

key_stats = {
    'Metric': [
        'Total Building Permits (2023)',
        'Total Construction Awards (2024)',
        'Residential Permits (Jan 2025)',
        'Industrial Under Construction',
        'Commercial Under Construction',
        'Office Vacancy Rate',
        'Retail Vacancy Rate',
        'Industrial Vacancy Rate',
        'Median New Home Price',
        'Population Growth (2021-2022)',
        'Employment Growth (2023)',
        'Active Home Builders',
        'New Home Communities',
        'Major Projects ($100M+)'
    ],
    'Value': [
        '46,269 permits',
        '$43.8 billion',
        '1,058 permits',
        '25.4 million SF',
        '54.2 million SF',
        '27.0%',
        '5.2%',
        '3.8%',
        '$357,365',
        '+125,000 residents',
        '+53,700 jobs',
        '118 builders',
        '439 communities',
        '15+ projects'
    ],
    'National Ranking': [
        '#1 in US',
        'Top 3 metros',
        '#1 in US',
        'Top 3 metros',
        'Top 5 metros',
        'Above average',
        'Below average',
        'Below average',
        'Regional average',
        'Top 5 metros',
        'Top 10 metros',
        'Most active',
        'Most active',
        'Leading activity'
    ]
}

df_stats = pd.DataFrame(key_stats)
print(df_stats)

# Save final stats
df_stats.to_csv('houston_market_statistics_2024.csv', index=False)
print("\nData saved to houston_market_statistics_2024.csv")

print("\n" + "="*50)
print("DATA FILES CREATED FOR ANALYSIS:")
print("="*50)
print("1. houston_developers_2024.csv - Major developers and permits")
print("2. houston_commercial_sectors_2024.csv - Commercial development by sector")
print("3. houston_land_acquisition_strategies_2024.csv - Land acquisition strategies")
print("4. houston_residential_activity_by_area_2024.csv - Residential activity by area")
print("5. houston_development_trends_2024.csv - Key development trends")
print("6. houston_major_projects_2024.csv - Major development projects")
print("7. houston_competitive_analysis_2024.csv - Competitive analysis summary")
print("8. houston_market_statistics_2024.csv - Key market statistics")