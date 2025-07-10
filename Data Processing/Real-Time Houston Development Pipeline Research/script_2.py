# Create a summary of Houston zoning and development ordinance changes
import pandas as pd

# Zoning and Development Changes Data
zoning_changes = [
    {
        'Initiative': 'Affordable Housing Code Changes',
        'Date': 'September 2023',
        'Description': 'Allow more garage apartments, courtyard-style houses, and small multi-family buildings',
        'Impact': 'Boost affordable housing stock',
        'Status': 'Approved'
    },
    {
        'Initiative': 'Frontloader House Restrictions',
        'Date': 'September 2023',
        'Description': 'New limits on houses with short driveways, banned in 10 neighborhoods',
        'Impact': 'Address sidewalk blocking concerns',
        'Status': 'Approved'
    },
    {
        'Initiative': 'Sidewalk Ordinance Amendments',
        'Date': 'December 2024',
        'Description': 'Expanded exemption criteria for single-family residential construction',
        'Impact': 'Streamline development process',
        'Status': 'Approved'
    },
    {
        'Initiative': '30-Day Permitting Pilot',
        'Date': 'July 2025',
        'Description': 'Goal to issue single-family residential permits within 30 days',
        'Impact': 'Reduce development delays',
        'Status': 'Launched'
    },
    {
        'Initiative': 'HouPermits System',
        'Date': 'Q1 2025',
        'Description': 'New electronic permitting system rollout',
        'Impact': 'Modernize permitting process',
        'Status': 'Implementation'
    },
    {
        'Initiative': 'Chapter 42 Development Code Updates',
        'Date': 'Ongoing 2024-2025',
        'Description': 'Comprehensive review of land development ordinances',
        'Impact': 'Improve development standards',
        'Status': 'Under Review'
    }
]

# Create DataFrame
zoning_df = pd.DataFrame(zoning_changes)

# Save to CSV
zoning_df.to_csv('houston_zoning_changes.csv', index=False)

print("HOUSTON ZONING AND DEVELOPMENT ORDINANCE CHANGES 2024-2025")
print("=" * 70)
print(zoning_df.to_string(index=False))

# Status summary
status_summary = zoning_df['Status'].value_counts()
print(f"\n\nSTATUS SUMMARY")
print("=" * 30)
for status, count in status_summary.items():
    print(f"{status}: {count} initiatives")

# Recent City Council Activity
print(f"\n\nRECENT CITY COUNCIL ACTIVITY")
print("=" * 40)
print("• June 2025: Planning Commission meetings on development regulations")
print("• July 2025: Budget and Fiscal Affairs committee active on infrastructure")
print("• Q2 2025: Quality of Life Committee reviewing residential developments")
print("• Ongoing: Public hearings on sidewalk and zoning amendments")
print("• 2024-2025: Multiple ordinances passed for streamlined development")

# Key Achievements
print(f"\n\nKEY ACHIEVEMENTS")
print("=" * 25)
print("• Houston leads US in building permits (52,851 in 2024)")
print("• $15 million investment in permitting system improvements")
print("• 30-day permitting pilot program launched")
print("• Affordable housing development code changes approved")
print("• Over $10 billion in major development projects underway")
print("• Streamlined sidewalk exemption process implemented")