import pandas as pd
import json

# Create a comprehensive dataset of Houston's tech and innovation metrics
houston_tech_data = {
    'Innovation Districts': {
        'Ion District': {
            'size_acres': 16,
            'building_sq_ft': 266000,
            'development_timeline': '2018-2030',
            'total_planned_sq_ft': 3000000,
            'key_tenants': ['Microsoft', 'Chevron Technology Ventures', 'Greentown Labs']
        },
        'Downtown Innovation Corridor': {
            'size_miles': 4,
            'key_facilities': ['Launch Pad', 'WeWork Labs', 'MassChallenge', 'Station Houston']
        }
    },
    'Texas Medical Center': {
        'expansion_projects': {
            'Memorial Hermann TMC': {
                'investment': 270000000,
                'completion_year': 2027,
                'additional_beds': 252,
                'sq_ft_expansion': 300000
            },
            'TMC Helix Park': {
                'size_acres': 37,
                'investment_timeline': '2023-2026',
                'focus': 'Life sciences research and commercial development'
            },
            'Harris Health LBJ': {
                'investment': 1600000000,
                'completion_year': 2028,
                'beds': 390,
                'sq_ft': 1300000
            }
        },
        'biomanufacturing_campus': {
            'TMC_BioPort': {
                'size_acres': 500,
                'projected_jobs': 100000,
                'timeline': '2025-2030'
            }
        }
    },
    'Energy Transition': {
        'Energy Corridor': {
            'office_space_sq_ft': 25000000,
            'class_a_percentage': 80,
            'dining_retail_sq_ft': 3500000,
            'jobs': 100000
        },
        'renewable_projects': {
            'HyVelocity Hub': 'Selected as one of 7 national clean hydrogen hubs',
            'solar_investments': 20000000,
            'harris_county_solar_grant': 250000000
        }
    },
    'Tech Ecosystem': {
        'workforce': {
            'tech_workers': 230800,
            'tech_firms': 9100,
            'venture_backed_startups': 1000,
            'job_growth_2022': 0.456,
            'tech_job_postings_growth': 0.456
        },
        'venture_capital': {
            'vc_funding_2022': 2040000000,
            'deals_2022': 256,
            'five_year_funding': 6420000000,
            'active_vc_funds': 11,
            'total_vcs': 30
        },
        'patents': {
            'tech_patents_2020_2024': 8691,
            'rank_nationally': 1
        }
    },
    'Harris County Tech': {
        'broadband_initiative': {
            'households_without_broadband': 171000,
            'task_force_established': 2025,
            'investment_focus': 'Digital divide closure'
        },
        'apple_investment': {
            'facility_sq_ft': 250000,
            'opening_year': 2026,
            'focus': 'AI-driven manufacturing'
        }
    }
}

# Create summary statistics
tech_metrics = pd.DataFrame({
    'Metric': [
        'Tech Workers',
        'Tech Firms', 
        'Venture-Backed Startups',
        'VC Funding 2022 ($M)',
        'Tech Patents (2020-2024)',
        'Ion District Size (acres)',
        'TMC Helix Park Size (acres)',
        'Energy Corridor Office Space (M sq ft)',
        'Projected TMC BioPort Jobs',
        'Harris County Households Without Broadband'
    ],
    'Value': [
        230800,
        9100,
        1000,
        2040,
        8691,
        16,
        37,
        25,
        100000,
        171000
    ],
    'Category': [
        'Workforce',
        'Companies',
        'Startups',
        'Investment',
        'Innovation',
        'Infrastructure',
        'Infrastructure', 
        'Infrastructure',
        'Future Growth',
        'Digital Divide'
    ]
})

print("Houston Technology & Innovation District Intelligence - Key Metrics")
print("=" * 70)
print(tech_metrics.to_string(index=False))
print("\n")

# Create investment summary
investment_data = pd.DataFrame({
    'Project/Initiative': [
        'Memorial Hermann TMC Expansion',
        'Harris Health LBJ Hospital',
        'TMC BioPort Campus',
        'Apple Manufacturing Facility',
        'Harris County Solar Grant',
        'Houston VC Funding (2022)',
        'Ion District Development'
    ],
    'Investment ($M)': [
        270,
        1600,
        5000,  # Estimated based on job creation
        500,   # Part of Apple's broader investment
        250,
        2040,
        100    # Ion building cost
    ],
    'Timeline': [
        '2025-2027',
        '2024-2028',
        '2025-2030',
        '2025-2026',
        '2024-2025',
        '2022',
        '2018-2030'
    ],
    'Sector': [
        'Healthcare',
        'Healthcare',
        'Life Sciences',
        'Technology',
        'Energy',
        'Venture Capital',
        'Innovation'
    ]
})

print("Major Investment Projects and Initiatives")
print("=" * 50)
print(investment_data.to_string(index=False))
print("\n")

# Save data for chart creation
tech_metrics.to_csv('houston_tech_metrics.csv', index=False)
investment_data.to_csv('houston_investment_data.csv', index=False)

# Create geographic distribution data
districts_data = pd.DataFrame({
    'District/Area': [
        'Ion District (Midtown)',
        'Texas Medical Center',
        'Energy Corridor',
        'Downtown Innovation Corridor',
        'TMC Helix Park',
        'Harris County (County-wide)'
    ],
    'Primary Focus': [
        'Tech Innovation & Startups',
        'Life Sciences & Healthcare',
        'Energy & Commercial',
        'Tech Incubation',
        'Life Sciences Research',
        'Digital Infrastructure'
    ],
    'Key Metrics': [
        '16 acres, 266K sq ft anchor building',
        '37-acre expansion, $1.6B+ investments',
        '25M sq ft office space, 100K jobs',
        '4-mile corridor, multiple facilities',
        '37 acres, research focus',
        '171K households need broadband'
    ]
})

print("Houston Innovation Districts Geographic Distribution")
print("=" * 55)
print(districts_data.to_string(index=False))

districts_data.to_csv('houston_districts_data.csv', index=False)