import pandas as pd

# Create comprehensive regulatory changes data
regulatory_data = {
    'Category': [
        'Harris County Zoning Laws',
        'Houston Building Codes', 
        'FEMA Flood Maps',
        'Texas Senate Bill 840',
        'Houston Permitting Process',
        'ADU Regulations',
        'ETJ Opt-Out (SB 2038)',
        'Harris County Fire Code'
    ],
    '2024 Status': [
        'No traditional zoning; uses subdivision ordinances and deed restrictions',
        '2021 International Codes adopted January 1, 2024 (IBC, IRC, IFC, etc.)',
        'Expected release early 2025; maps not updated since 2007',
        'Not enacted; cities maintained full zoning authority',
        'Standard multi-month permit review process',
        '900 sq ft maximum size, 5 ft setbacks from property lines',
        'Active since September 2023; allows ETJ opt-out by petition',
        '2018 International Fire Code with amendments'
    ],
    '2025 Updates': [
        'Continues with no zoning; relies on subdivision ordinances only',
        'Same 2021 codes remain in effect with Houston amendments',
        'Delayed until 2026; 100-year floodplain expected to expand significantly',
        'Commercial-to-residential conversion by right; limits municipal restrictions',
        '30-day pilot program launched July 7 for single-family permits',
        'No changes to size limits or setback requirements',
        'Legal challenges from cities; Texas Supreme Court upheld validity',
        '2021 Harris County Fire Code adopted effective January 1, 2025'
    ],
    'Effective Date': [
        'Ongoing',
        'January 1, 2024',
        'Delayed to 2026',
        'September 1, 2025',
        'July 7, 2025',
        'Ongoing since 2022',
        'September 1, 2023',
        'January 1, 2025'
    ],
    'Impact on Development': [
        'Flexibility but reliance on deed restrictions; no comprehensive land use planning',
        'Enhanced energy efficiency (8.9% savings), improved safety standards',
        'Continued uncertainty for flood insurance requirements and development planning',
        'Streamlined multifamily development in commercial zones; reduced municipal control',
        'Faster single-family home permitting; improved developer confidence',
        'Stable framework for accessory dwelling unit development',
        'Developers can bypass city development regulations in ETJ areas',
        'Stricter fire safety requirements for commercial and multifamily buildings'
    ]
}

# Create DataFrame
df = pd.DataFrame(regulatory_data)

# Display the table
print("Harris County & Houston Regulatory Intelligence: 2024-2025 Comparison")
print("=" * 80)
print()

for index, row in df.iterrows():
    print(f"{index + 1}. {row['Category']}")
    print(f"   2024 Status: {row['2024 Status']}")
    print(f"   2025 Updates: {row['2025 Updates']}")
    print(f"   Effective Date: {row['Effective Date']}")
    print(f"   Impact on Development: {row['Impact on Development']}")
    print()

# Save as CSV
df.to_csv('regulatory_changes_2024_2025.csv', index=False)
print("Data saved to regulatory_changes_2024_2025.csv")