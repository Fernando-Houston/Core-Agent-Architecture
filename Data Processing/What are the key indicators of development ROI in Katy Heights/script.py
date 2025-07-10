import pandas as pd
import numpy as np

# Create a comprehensive dataset of key Katy Heights development ROI indicators
katy_heights_data = {
    'ROI_Indicator': [
        'Median Property Value',
        'Median Appraised Value',
        'Price per Square Foot',
        'Property Value Range',
        'Median Lot Size (sq ft)',
        'Median Year Built',
        'Property Tax Rate',
        'Annual Rent (3-4 BR)',
        'Construction Cost (per sq ft)',
        'Average Days on Market',
        'Market Absorption Rate',
        'Building Permit Fee Est.',
        'Impact Fee Estimated',
        'Price Appreciation (5-yr)',
        'Rental Yield Potential'
    ],
    'Current_Value': [
        285105,
        259515,
        165.56,
        'N/A',
        7800,
        1972,
        2.12,
        28800,
        250,
        52,
        'N/A',
        1647,
        5750,
        'N/A',
        'N/A'
    ],
    'Metric_Type': [
        'USD',
        'USD',
        'USD/sq ft',
        'USD',
        'sq ft',
        'Year',
        'Percent',
        'USD/year',
        'USD/sq ft',
        'Days',
        'Percent',
        'USD',
        'USD',
        'Percent',
        'Percent'
    ],
    'Source_Period': [
        '2024',
        '2024',
        '2024',
        '2024',
        '2024',
        '2024',
        '2024',
        '2025',
        '2024',
        '2024',
        '2024',
        '2024',
        '2024',
        '2019-2024',
        '2024'
    ]
}

# Create DataFrame
df = pd.DataFrame(katy_heights_data)

# Calculate some derived metrics
rental_monthly = 28800 / 12
property_value = 285105
gross_rental_yield = (28800 / property_value) * 100

# Historical price appreciation data
price_history = {
    'Year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Price_per_sqft': [65.62, 91.22, 101.78, 120.83, 134.16, 156.91, 172.27, 165.56],
    'Units_Sold': [3, 4, 5, 6, 11, 8, 10, 9]
}

price_df = pd.DataFrame(price_history)

# Calculate year-over-year growth
price_df['YoY_Growth'] = price_df['Price_per_sqft'].pct_change() * 100

# Calculate 5-year appreciation
five_year_appreciation = ((165.56 / 101.78) - 1) * 100

print("=== KATY HEIGHTS DEVELOPMENT ROI INDICATORS ===")
print("\nKey Property Metrics:")
print(f"Median Property Value: ${285105:,}")
print(f"Price per Square Foot: ${165.56}")
print(f"Median Lot Size: {7800:,} sq ft")
print(f"Property Tax Rate: 2.12%")
print(f"5-Year Price Appreciation: {five_year_appreciation:.1f}%")

print("\nRental Market Indicators:")
print(f"Monthly Rental Income (3-4 BR): ${rental_monthly:,.0f}")
print(f"Annual Rental Income: ${28800:,}")
print(f"Gross Rental Yield: {gross_rental_yield:.1f}%")

print("\nDevelopment Cost Indicators:")
print(f"Construction Cost: $250/sq ft")
print(f"Building Permit Fee: $1,647")
print(f"Impact Fees: $5,750")
print(f"Average Days on Market: 52 days")

print("\nPrice History Analysis:")
print(price_df.to_string(index=False))

# Save to CSV
df.to_csv('katy_heights_roi_indicators.csv', index=False)
price_df.to_csv('katy_heights_price_history.csv', index=False)

print("\n=== ANALYSIS COMPLETE ===")
print("Data saved to CSV files for further analysis")