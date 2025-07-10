# Create comprehensive Houston development trends data
development_trends_2024 = {
    'Category': [
        'Residential Permits',
        'Commercial Construction',
        'Industrial Development',
        'Land Values',
        'Office Market',
        'Retail Development',
        'Mixed-Use Projects',
        'Infrastructure Investment',
        'Population Growth',
        'Employment Growth'
    ],
    'Key Metrics': [
        'Houston led nation with 46,269 permits in 2023',
        '$43.8B in contracts awarded in 2024 (+31% YoY)',
        '25.4M SF under construction, 3.8% vacancy',
        'Median new home price: $357,365 (+19% premium)',
        '27% vacancy rate, 0.6M SF under construction',
        '3.7M SF under development, 5.2% vacancy',
        '$2.5B East River, $350M Plant project',
        'Harris County streamlined permitting process',
        'Houston metro added 125,000 residents 2021-2022',
        '53,700 jobs added in first 10 months of 2023'
    ],
    'Major Trends': [
        'Suburban expansion along Grand Parkway',
        'Industrial/warehouse sector dominance',
        'Northwest Far submarket leading with 3.4M SF',
        'Flight to quality, smaller new homes',
        'Downtown vacancy challenges, flight to quality',
        'Smaller format, neighborhood-focused retail',
        'Urban core redevelopment emphasis',
        'Public-private partnerships increasing',
        'Continued migration to Houston metro',
        'Energy, healthcare, aerospace driving growth'
    ],
    'Geographic Focus': [
        'Katy, Cypress, The Woodlands, Montgomery County',
        'Energy Corridor, Northwest, East River',
        'Grand Parkway, 290 Corridor, Waller County',
        'Beyond Beltway 8, eastern Harris County',
        'Downtown, Energy Corridor, Uptown',
        'Suburban growth corridors, infill development',
        'Downtown, East End, Energy Corridor',
        'Major transportation corridors',
        'Suburban communities, master-planned developments',
        'Energy Corridor, TMC, Downtown, Aerospace'
    ],
    'Key Players': [
        'D.R. Horton, Lennar, Perry Homes',
        'Hines, Midway, Skanska, Weitzman',
        'Prologis, EastGroup, Duke Realty',
        'HAR data, HCAD assessments',
        'Transwestern, JLL, CBRE, Colliers',
        'Weitzman, Fidelis, MetroNational',
        'Hines, Midway, Texas Medical Center',
        'Harris County, City of Houston',
        'Greater Houston Partnership',
        'Texas Workforce Commission'
    ]
}

df_trends = pd.DataFrame(development_trends_2024)

print("Houston Development Trends 2024 - Key Metrics by Category")
print("=" * 80)
print(df_trends)

# Save to CSV
df_trends.to_csv('houston_development_trends_2024.csv', index=False)
print("\nData saved to houston_development_trends_2024.csv")

# Create major projects summary
major_projects_2024 = {
    'Project Name': [
        'East River',
        'Texas Medical Center Innovation District',
        'Bridgeland',
        'Sunterra',
        'Manvel Town Center',
        'Buffalo Bayou East',
        'GreenStreet',
        'Astros Entertainment District',
        'The Plant/Second Ward',
        'Discovery Green projects',
        'Tesla Megapack Facility',
        'Grainger Distribution Center',
        'Swift Building',
        'Ashford Yard',
        'Memorial Town Square'
    ],
    'Developer': [
        'Midway',
        'Texas Medical Center',
        'Howard Hughes Corporation',
        'Land Tejas/Starwood Land',
        'Weitzman',
        'Buffalo Bayou Partnership',
        'Rebees',
        'Houston Astros',
        'Elkus Manfredi',
        'Skanska',
        'Tesla',
        'Grainger Inc.',
        'Heights redevelopment',
        'West Houston',
        'MetroNational'
    ],
    'Type': [
        'Mixed-Use',
        'Medical/Research',
        'Master-Planned Community',
        'Master-Planned Community',
        'Retail/Commercial',
        'Mixed-Use/Infrastructure',
        'Mixed-Use',
        'Entertainment/Hospitality',
        'Mixed-Use',
        'Office/Commercial',
        'Industrial',
        'Industrial',
        'Mixed-Use',
        'Mixed-Use',
        'Mixed-Use'
    ],
    'Investment': [
        '$2.5B',
        '$1.5B+',
        '$1B+',
        '$500M+',
        '$300M+',
        '$310M',
        '$50M+',
        '$200M+',
        '$350M',
        '$100M+',
        '$375M',
        '$225M',
        '$75M+',
        '$200M+',
        '$150M+'
    ],
    'Status': [
        'Under Construction',
        'Multiple phases',
        'Active development',
        'Active sales',
        'Under construction',
        'In progress',
        'Under renovation',
        'Planning',
        'Under construction',
        'Under construction',
        'Under construction',
        'Under construction',
        'Under construction',
        'Planning',
        'Under construction'
    ]
}

df_projects = pd.DataFrame(major_projects_2024)

print("\n" + "="*80)
print("MAJOR HOUSTON DEVELOPMENT PROJECTS 2024")
print("="*80)
print(df_projects[['Project Name', 'Developer', 'Type', 'Investment', 'Status']])

# Save to CSV
df_projects.to_csv('houston_major_projects_2024.csv', index=False)
print("\nData saved to houston_major_projects_2024.csv")