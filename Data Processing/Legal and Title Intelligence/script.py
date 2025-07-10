import pandas as pd

# Create a comprehensive dataset of Houston property development legal issues
houston_legal_issues = {
    'Issue_Category': [
        'Title Issues', 'Title Issues', 'Title Issues', 'Title Issues', 'Title Issues',
        'Deed Restrictions', 'Deed Restrictions', 'Deed Restrictions', 'Deed Restrictions',
        'Eminent Domain', 'Eminent Domain', 'Eminent Domain', 'Eminent Domain',
        'Litigation Trends', 'Litigation Trends', 'Litigation Trends', 'Litigation Trends'
    ],
    'Specific_Issue': [
        'Mortgage Liens', 'Tax Liens', 'Boundary Disputes', 'Defective Deeds', 'Missing Heirs',
        'City Enforcement Challenges', 'Private HOA Conflicts', 'Amendment Processes', 'Compliance Monitoring',
        'TxDOT Highway Projects', 'Pipeline Development', 'Texas Central Railway', 'Fair Compensation Disputes',
        'Construction Contract Disputes', 'Development Delays', 'Zoning Conflicts', 'Environmental Compliance'
    ],
    'Frequency_Level': [
        'Very High', 'High', 'High', 'Medium', 'Medium',
        'High', 'Very High', 'Medium', 'High',
        'Medium', 'High', 'Low', 'Medium',
        'High', 'Very High', 'Medium', 'Medium'
    ],
    'Impact_on_Development': [
        'Critical - Can halt transactions', 'Critical - Financial liability', 'High - Delays and costs', 'High - Transaction delays', 'Medium - Due diligence issues',
        'High - Development restrictions', 'Critical - Project modifications', 'Medium - Planning delays', 'High - Ongoing compliance',
        'Critical - Property loss', 'High - Easement requirements', 'High - Route restrictions', 'High - Compensation disputes',
        'High - Project delays and costs', 'Critical - Timeline and budget', 'Medium - Design limitations', 'High - Regulatory compliance'
    ],
    'Primary_Authority': [
        'County Clerk/Courts', 'Tax Assessor/Courts', 'Surveyor/Courts', 'County Clerk/Title Company', 'Probate Court/Estate Attorney',
        'City of Houston Legal Dept', 'HOA/Private Enforcement', 'HOA/Community Vote', 'City/HOA Monitoring',
        'TxDOT/State Courts', 'Railroad Commission/Federal', 'Federal/State Courts', 'Eminent Domain Courts',
        'Civil Courts/Arbitration', 'Civil Courts/Mediation', 'City Planning/Courts', 'EPA/TCEQ/Courts'
    ],
    'Typical_Resolution_Time': [
        '2-6 months', '3-12 months', '6-18 months', '1-3 months', '6-24 months',
        '3-12 months', '6-18 months', '12-36 months', 'Ongoing',
        '12-60 months', '18-36 months', '24-60 months', '12-36 months',
        '6-24 months', '12-36 months', '6-18 months', '12-48 months'
    ],
    '2024_Trend': [
        'Increasing', 'Stable', 'Increasing', 'Stable', 'Stable',
        'Increasing', 'Increasing', 'Stable', 'Increasing',
        'Stable', 'Increasing', 'Decreasing', 'Stable',
        'Increasing', 'Increasing', 'Stable', 'Increasing'
    ]
}

# Create DataFrame
df = pd.DataFrame(houston_legal_issues)

# Display summary
print("Houston Property Development Legal Issues Summary")
print("=" * 60)
print(f"Total Issues Tracked: {len(df)}")
print(f"Categories: {df['Issue_Category'].nunique()}")
print("\nFrequency Distribution:")
print(df['Frequency_Level'].value_counts())
print("\n2024 Trends:")
print(df['2024_Trend'].value_counts())

# Save to CSV
df.to_csv('houston_property_legal_issues_2024.csv', index=False)
print(f"\nData saved to houston_property_legal_issues_2024.csv")
print(f"File contains {len(df)} rows and {len(df.columns)} columns")

# Display first few rows
print("\nSample Data:")
print(df.head(10).to_string(index=False))