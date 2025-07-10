# Let's organize the key data I've gathered into structured formats for potential visualizations

# Top Houston ZIP codes by performance in 2024
top_zip_codes_2024 = {
    "ZIP Code": ["77493", "77433", "77381", "77382", "77079", "77031", "77479", "77449", "77377"],
    "Area": ["Katy", "Cypress", "The Woodlands", "The Woodlands", "Memorial/Energy Corridor", "Southwest Houston", "Sugar Land", "Katy", "Tomball"],
    "Rank": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Performance": ["#1 Hottest US Market", "#2 Hottest US Market", "8% appreciation", "8% appreciation", "8% appreciation", "7% appreciation", "7% appreciation", "Top 20 list", "Hidden gem under $300K"]
}

# Houston neighborhood appreciation data
houston_neighborhoods = {
    "Neighborhood": ["Midtown Houston", "Rice/Museum District", "Heights/Greater Heights", "Garden Oaks", "Memorial Park", "West University Place", "EaDo", "Cottage Grove", "Spring Branch", "Katy", "Cypress"],
    "5_Year_Appreciation": [86, 65, 11, 39, 48, 0, None, 16, None, None, None],
    "10_Year_Appreciation": [None, 34, None, None, 60, 30, None, None, None, 47, None],
    "Investment_Appeal": ["High ROI", "Consistent appreciation", "Premium buy-and-hold", "Strong recent growth", "Luxury, high demand", "Stable, affluent", "High development", "Up-and-coming", "High appreciation", "Strong rental demand", "Fast appreciation"]
}

# Houston permit activity by top counties
permit_activity_2024 = {
    "County": ["Harris County", "Montgomery County", "Fort Bend County", "Collin County", "Tarrant County"],
    "Permits": [1573, 690, 514, 796, 501],
    "Metro_Area": ["Houston", "Houston", "Houston", "Dallas", "Dallas"]
}

# Property value changes by price range (Harris County 2024)
property_value_changes = {
    "Price_Range": ["Under $250K", "$250K-$450K", "$450K-$1M", "$1M-$1.5M", "Over $1.5M"],
    "Value_Change": [-0.8, "1-5%", "7-12%", 7, 9],
    "Trend": ["Decrease", "Modest increase", "Strong increase", "Strong increase", "Strong increase"]
}

# Spring Branch market data
spring_branch_data = {
    "Metric": ["Median Sale Price", "YoY Change", "Days on Market", "Price per Sq Ft"],
    "June_2024": [415000, None, 94, 213],
    "June_2025": [485000, 18.3, 119, 226],
    "Change": [70000, 18.3, 25, 13]
}

# Katy Heights market data
katy_heights_data = {
    "Metric": ["Median Price/Sq Ft", "Properties Sold", "Median Appraised Value", "Median Market Value"],
    "2024_Value": [165.56, 9, 259515, 285105],
    "2023_Value": [172.27, 10, None, None],
    "Change": [-6.71, -1, None, None]
}

print("Houston Real Estate Market Intelligence Data Summary")
print("=" * 55)
print("\n1. Top Performing ZIP Codes 2024:")
for i, zip_code in enumerate(top_zip_codes_2024["ZIP Code"]):
    print(f"   {zip_code} ({top_zip_codes_2024['Area'][i]}): {top_zip_codes_2024['Performance'][i]}")

print("\n2. Houston Permit Activity Leaders 2024:")
for i, county in enumerate(permit_activity_2024["County"]):
    if permit_activity_2024["Metro_Area"][i] == "Houston":
        print(f"   {county}: {permit_activity_2024['Permits'][i]} permits")

print("\n3. Spring Branch Market Performance:")
print(f"   Median Price: ${spring_branch_data['June_2025'][0]:,} (up {spring_branch_data['Change'][1]}%)")
print(f"   Days on Market: {spring_branch_data['June_2025'][2]} days (up {spring_branch_data['Change'][2]} days)")

print("\n4. Key Market Trends:")
print("   - Houston led US in single-family permits (52,851 in 2024)")
print("   - Active listings up 31.8% year-over-year")
print("   - Luxury market ($1M+) showing strongest growth")
print("   - Suburban areas (Katy, Cypress) dominating hottest markets")