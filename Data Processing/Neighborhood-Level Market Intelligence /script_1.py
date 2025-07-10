import pandas as pd

# Create a comprehensive Houston Market Intelligence summary table
houston_market_data = {
    'Neighborhood/Area': [
        'Katy (77493)', 'Cypress (77433)', 'The Woodlands (77381/77382)', 
        'Spring Branch', 'Katy Heights', 'Memorial/Energy Corridor (77079)',
        'Southwest Houston (77031)', 'Sugar Land (77479)', 'Tomball (77377)',
        'Heights', 'Montrose', 'Memorial Park', 'River Oaks', 'Midtown'
    ],
    'Median_Price_2024': [
        '$374,268', '$629,489', '$640,000', '$485,000', '$285,105', 
        'N/A', 'N/A', 'N/A', '$391,815', '$690,000', '$809,000', 
        '$1,513,500', '$2,985,000', '$367,500'
    ],
    'Price_Per_SqFt': [
        '$167', '$193', '$228', '$226', '$166', 'N/A', 'N/A', 'N/A', 
        '$172', '$328', '$308', '$380', '$558', '$210'
    ],
    'YoY_Change_2024': [
        '+0.5%', '+12.4%', '+8.0%', '+18.3%', '-3.9%', '+8.0%', 
        '+7.0%', '+7.0%', 'Hidden Gem', '+2.2%', '+3.9%', '-3.0%', 
        '-7.0%', '-4.9%'
    ],
    'Market_Status': [
        '#1 Hottest US Market', '#2 Hottest US Market', 'Strong Growth', 
        'High Appreciation', 'Affordable Entry', 'Premium Location', 
        'Emerging Market', 'Stable Growth', 'Under $300K Gem', 
        'Historic Premium', 'Cultural Hub', 'Luxury Market', 
        'Ultra-Luxury', 'Urban Living'
    ],
    'Investment_Appeal': [
        'Rental Demand', 'Fast Sales', 'Family Market', 'Development ROI', 
        'First-Time Buyers', 'Energy Corridor', 'Value Play', 'Suburban Growth',
        'Rapid Development', 'Historic Charm', 'Walkable', 'Stable Luxury',
        'Exclusive', 'Young Professionals'
    ]
}

# Create DataFrame
df = pd.DataFrame(houston_market_data)

# Display the table
print("HOUSTON NEIGHBORHOOD MARKET INTELLIGENCE SUMMARY 2024")
print("=" * 65)
print(df.to_string(index=False, max_colwidth=20))

# Save as CSV for reference
df.to_csv('houston_market_intelligence_2024.csv', index=False)

print("\n\nKEY HOUSTON MARKET STATISTICS 2024:")
print("=" * 40)
print("• Houston Metro Led US: 52,851 single-family permits")
print("• Active Listings: +31.8% year-over-year")
print("• Average Home Price: $450,235 (record high)")
print("• Median Home Price: $346,651 (stable)")
print("• Luxury Sales ($1M+): +40.6% year-over-year")
print("• Houston Counties Leading Permits:")
print("  - Harris County: 1,573 permits")
print("  - Montgomery County: 690 permits")
print("  - Fort Bend County: 514 permits")

print("\n\nTOP DEVELOPMENT ROI NEIGHBORHOODS:")
print("=" * 35)
roi_neighborhoods = [
    "Midtown Houston (86% 5-year appreciation)",
    "Rice/Museum District (65% 5-year appreciation)", 
    "Memorial Park (48% 5-year appreciation)",
    "Heights/Greater Heights (Historic premium)",
    "EaDo (High development activity)",
    "Spring Branch (Strong new construction)",
    "Katy & Cypress (Rental demand + fast appreciation)"
]

for neighborhood in roi_neighborhoods:
    print(f"• {neighborhood}")