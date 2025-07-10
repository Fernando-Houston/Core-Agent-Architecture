import pandas as pd

# Create a comprehensive summary table of lending rate impacts
impact_data = {
    'Impact Area': [
        'Lending Rates (Current)',
        'Lending Rates (Current)',
        'Lending Rates (Current)',
        'Lending Rates (Current)',
        'Lending Rates (Current)',
        'Market Activity',
        'Market Activity',
        'Market Activity',
        'Property Values',
        'Property Values',
        'Property Values',
        'Construction Activity',
        'Construction Activity',
        'Financing Challenges',
        'Financing Challenges',
        'Rent Performance'
    ],
    'Metric': [
        'Multifamily (>$6M)',
        'Multifamily (<$6M)',
        'Commercial/Office/Retail',
        'Industrial',
        'Bridge Loans',
        'Transaction Volume Change',
        'Commercial Lending Volume',
        'CBRE Lending Index',
        'Multifamily Property Values',
        'Office Property Values',
        'Commercial Property Values (Overall)',
        'Industrial Construction',
        'Construction Deliveries',
        'Maturing Loans in 2025',
        'Refinancing Rate Premium',
        'Industrial Rent Growth (5-year)'
    ],
    'Current Status/Impact': [
        '5.34%',
        '5.80%',
        '6.38%',
        '6.38%',
        '9.00%',
        '-40% (2022-2024)',
        '+16% (2024-2025)',
        '+90% year-over-year',
        '+0.8% increase',
        '-7.7% decrease',
        '+2% increase',
        '-49% (36.2M to 18.6M sf)',
        '-29% quarterly decline',
        '$957 billion nationwide',
        '75-100% increase in debt service',
        '+38% increase'
    ],
    'Implication': [
        'Most favorable CRE rates',
        'Competitive multifamily rates',
        'Higher rates limit development',
        'Constrained industrial growth',
        'Expensive short-term financing',
        'Significant market slowdown',
        'Recovery signs emerging',
        'Lending activity rebounding',
        'Stable demand, rental strength',
        'Work-from-home impact',
        'Market showing resilience',
        'Major construction decline',
        'Supply constraints emerging',
        'Refinancing pressure wave',
        'Cash flow stress for owners',
        'Strong rental fundamentals'
    ]
}

# Create DataFrame
df = pd.DataFrame(impact_data)

# Display the table
print("HARRIS COUNTY COMMERCIAL REAL ESTATE: LENDING RATE IMPACTS SUMMARY")
print("=" * 80)
print(df.to_string(index=False))

# Save as CSV for reference
df.to_csv('harris_county_cre_lending_impacts.csv', index=False)
print("\n\nTable saved as 'harris_county_cre_lending_impacts.csv'")

# Create a focused analysis of rate progression
rate_progression = {
    'Property Type': [
        'Multifamily (>$6M)',
        'Multifamily (<$6M)',
        'Commercial/Office',
        'Industrial',
        'Bridge Loans'
    ],
    '2022 Rate': ['3.5%', '4.0%', '4.2%', '4.2%', '7.0%'],
    '2023 Rate': ['6.0%', '6.5%', '6.8%', '6.8%', '8.5%'],
    '2024 Rate': ['5.8%', '6.2%', '6.6%', '6.6%', '8.8%'],
    '2025 Rate': ['5.34%', '5.80%', '6.38%', '6.38%', '9.00%'],
    'Rate Change (2022-2025)': ['+1.84%', '+1.80%', '+2.18%', '+2.18%', '+2.00%']
}

df_rates = pd.DataFrame(rate_progression)
print("\n\nCOMMERCIAL LENDING RATE PROGRESSION (2022-2025)")
print("=" * 60)
print(df_rates.to_string(index=False))

# Save rate progression table
df_rates.to_csv('harris_county_lending_rate_progression.csv', index=False)
print("\n\nRate progression table saved as 'harris_county_lending_rate_progression.csv'")