# Create a comprehensive permit activity and builder analysis
print("HOUSTON CONSTRUCTION & PERMIT ACTIVITY ANALYSIS 2024")
print("=" * 55)

# Top home builders in Houston 2024
builders_data = {
    'Builder': ['D.R. Horton', 'Perry Homes', 'Lennar Homes', 'K Hovnanian Homes', 'David Weekley Homes'],
    'Houston_Permits_2024': [608, 275, 218, 210, 186],
    'Market_Share': ['#1 Volume Builder', 'Local Leader', 'National Player', 'Value Builder', 'Premium Quality']
}

print("\nTOP HOME BUILDERS IN HOUSTON (April 2024):")
print("-" * 45)
for i, builder in enumerate(builders_data['Builder']):
    print(f"{i+1}. {builder}: {builders_data['Houston_Permits_2024'][i]} permits ({builders_data['Market_Share'][i]})")

# Harris County property value changes by price segment
print("\n\nHARRIS COUNTY PROPERTY VALUE CHANGES 2024:")
print("-" * 45)
print("• Homes under $450K: +1% to +5% increase")
print("• Homes $450K to $1M: +7% to +12% increase")  
print("• Homes $1M to $1.5M: +7% increase")
print("• Homes over $1.5M: +9% increase")
print("• 57% of homes increased in value")
print("• 31% of homes decreased in value")
print("• 12% of homes unchanged")

# Regional permit comparison
print("\n\nTEXAS REGIONAL PERMIT ACTIVITY 2024:")
print("-" * 40)
print("• Houston Metro: 45,000 permits (38% from Harris County)")
print("• Dallas-Fort Worth: 40,500 permits")
print("• Austin: 14,468 permits")
print("• San Antonio: 10,916 permits")
print("• Houston Average Permit Value: $371,000 (Harris County)")

# Market outlook indicators
print("\n\nMARKET OUTLOOK INDICATORS:")
print("-" * 30)
print("• Inventory: 4.9-month supply (balanced market)")
print("• Absorption Rate: 18% (August 2024)")
print("• Average Days on Market: 37 days")
print("• Mortgage Rates: ~6.8% (30-year fixed)")
print("• Construction Starts: Expected 2-6% decline in 2025")
print("• Population Growth: Continuing to drive demand")

print("\n\nKEY INVESTMENT INSIGHTS:")
print("-" * 25)
insights = [
    "Suburban markets (Katy, Cypress) outperforming urban core",
    "Luxury segment showing strongest price appreciation",
    "New construction heavily concentrated in outer counties",
    "Rental demand remains strong across all price segments",
    "Energy sector diversification supporting market stability"
]

for insight in insights:
    print(f"• {insight}")

print(f"\n\nData Sources: Houston Association of Realtors, Harris County Appraisal District,")
print("Greater Houston Partnership, HBWeekly Construction Data, Opendoor Market Reports")
print("Analysis Date: July 2025")