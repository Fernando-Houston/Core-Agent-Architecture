import pandas as pd
import json

# Create comprehensive Houston population growth data by area
houston_population_data = {
    "Area": [
        "City of Houston",
        "Harris County", 
        "Fort Bend County",
        "Montgomery County",
        "Waller County",
        "Liberty County",
        "Chambers County",
        "Fulshear",
        "Conroe",
        "Katy",
        "Cypress", 
        "The Woodlands",
        "Sugar Land",
        "Energy Corridor",
        "Downtown Houston"
    ],
    "2020_Population": [
        2304580,
        4731122,
        822779,
        620443,
        56794,
        91628,
        45413,
        16817,
        89084,
        21894,
        181637,
        118365,
        118488,
        85000,
        9995
    ],
    "2025_Population": [
        2319119,
        4942701,
        916778,
        711354,
        63553,
        108272,
        48580,
        54629,
        98762,
        25800,
        210000,
        125000,
        125000,
        90000,
        12000
    ],
    "Growth_Rate_2020_2025": [
        0.63,
        4.47,
        11.43,
        14.64,
        11.90,
        18.17,
        6.97,
        224.58,
        10.86,
        17.84,
        15.63,
        5.61,
        5.50,
        5.88,
        20.07
    ],
    "Annual_Growth_Rate": [
        0.13,
        0.89,
        2.29,
        2.93,
        2.38,
        3.63,
        1.39,
        44.92,
        2.17,
        3.57,
        3.13,
        1.12,
        1.10,
        1.18,
        4.01
    ]
}

# Save to CSV
df_population = pd.DataFrame(houston_population_data)
df_population.to_csv("houston_population_growth_by_area.csv", index=False)
print("Houston Population Growth by Area Data:")
print(df_population.head(10))
print("\n" + "="*50 + "\n")

# Create Houston job growth data by sector
job_growth_data = {
    "Sector": [
        "Healthcare",
        "Construction", 
        "Professional Services",
        "Government",
        "Restaurants & Bars",
        "Wholesale Trade",
        "Oil & Gas Extraction",
        "Transportation & Warehousing",
        "Technology",
        "Manufacturing",
        "Education",
        "Finance",
        "Retail Trade",
        "Real Estate"
    ],
    "2024_Jobs": [
        412000,
        315000,
        385000,
        275000,
        285000,
        195000,
        165000,
        175000,
        230800,
        239500,
        185000,
        165000,
        295000,
        125000
    ],
    "2025_Projected_Jobs": [
        421700,
        325000,
        392000,
        277200,
        290200,
        198000,
        167900,
        178000,
        245000,
        242000,
        187000,
        167000,
        297000,
        127000
    ],
    "Job_Growth_2024_2025": [
        9700,
        10000,
        7000,
        2200,
        5200,
        3000,
        2900,
        3000,
        14200,
        2500,
        2000,
        2000,
        2000,
        2000
    ],
    "Growth_Rate_Percent": [
        2.35,
        3.17,
        1.82,
        0.80,
        1.82,
        1.54,
        1.76,
        1.71,
        6.15,
        1.04,
        1.08,
        1.21,
        0.68,
        1.60
    ]
}

df_jobs = pd.DataFrame(job_growth_data)
df_jobs.to_csv("houston_job_growth_by_sector.csv", index=False)
print("Houston Job Growth by Sector Data:")
print(df_jobs.head(10))
print("\n" + "="*50 + "\n")

# Create Houston housing market data
housing_data = {
    "Area": [
        "Inner Loop",
        "Energy Corridor",
        "Katy",
        "Cypress",
        "The Woodlands",
        "Sugar Land",
        "Pearland",
        "Kingwood",
        "Heights",
        "Midtown",
        "Downtown",
        "Memorial",
        "River Oaks",
        "Bellaire",
        "West University"
    ],
    "Median_Home_Price_2024": [
        485000,
        415000,
        385000,
        320000,
        475000,
        485000,
        365000,
        425000,
        525000,
        445000,
        375000,
        625000,
        1250000,
        775000,
        950000
    ],
    "Median_Home_Price_2025": [
        495000,
        425000,
        395000,
        335000,
        485000,
        495000,
        375000,
        435000,
        545000,
        465000,
        385000,
        645000,
        1285000,
        795000,
        975000
    ],
    "Price_Change_Percent": [
        2.06,
        2.41,
        2.60,
        4.69,
        2.11,
        2.06,
        2.74,
        2.35,
        3.81,
        4.49,
        2.67,
        3.20,
        2.80,
        2.58,
        2.63
    ],
    "Housing_Demand_Level": [
        "Very High",
        "High",
        "Very High",
        "High",
        "Very High",
        "Very High",
        "High",
        "Moderate",
        "Very High",
        "High",
        "Moderate",
        "Very High",
        "High",
        "High",
        "High"
    ]
}

df_housing = pd.DataFrame(housing_data)
df_housing.to_csv("houston_housing_market_data.csv", index=False)
print("Houston Housing Market Data:")
print(df_housing.head(10))
print("\n" + "="*50 + "\n")

# Create commercial real estate data
commercial_data = {
    "Submarket": [
        "Energy Corridor",
        "Downtown CBD",
        "Galleria",
        "Westchase",
        "Greenway Plaza",
        "The Woodlands",
        "West Loop",
        "Katy Freeway",
        "Northwest Houston",
        "Clear Lake",
        "Medical Center",
        "Uptown",
        "Spring",
        "Cy-Fair"
    ],
    "Office_Space_SF": [
        25000000,
        45000000,
        35000000,
        18000000,
        22000000,
        12000000,
        28000000,
        15000000,
        8000000,
        6000000,
        14000000,
        16000000,
        5000000,
        7000000
    ],
    "Vacancy_Rate_Percent": [
        24.3,
        32.0,
        28.5,
        22.1,
        25.8,
        13.1,
        26.4,
        17.8,
        35.2,
        18.9,
        16.5,
        27.3,
        19.8,
        21.2
    ],
    "Average_Rent_PSF": [
        28.75,
        32.50,
        35.20,
        26.80,
        29.40,
        31.25,
        30.15,
        25.90,
        22.80,
        24.60,
        33.75,
        31.80,
        23.40,
        24.20
    ],
    "Net_Absorption_2024": [
        235000,
        -125000,
        -85000,
        45000,
        -35000,
        125000,
        -55000,
        65000,
        -45000,
        25000,
        85000,
        -25000,
        35000,
        15000
    ],
    "Primary_Industries": [
        "Energy/Oil & Gas",
        "Financial Services",
        "Mixed/Corporate",
        "Technology",
        "Professional Services",
        "Corporate HQ",
        "Mixed/Corporate",
        "Energy/Manufacturing",
        "Industrial",
        "Aerospace/NASA",
        "Healthcare",
        "Mixed/Corporate",
        "Manufacturing",
        "Mixed/Services"
    ]
}

df_commercial = pd.DataFrame(commercial_data)
df_commercial.to_csv("houston_commercial_real_estate_data.csv", index=False)
print("Houston Commercial Real Estate Data:")
print(df_commercial.head(10))
print("\n" + "="*50 + "\n")

# Create tech sector impact data
tech_data = {
    "Metric": [
        "Tech Companies",
        "Tech Jobs",
        "Tech Startups",
        "VC Funding (millions)",
        "Tech Patents",
        "Tech Establishments Growth",
        "Tech Employment Growth",
        "Average Tech Salary",
        "Tech Office Space Demand (SF)",
        "Tech Hub Locations"
    ],
    "2020_Value": [
        3500,
        200000,
        3200,
        284,
        6500,
        0,
        0,
        95000,
        2500000,
        5
    ],
    "2025_Value": [
        4000,
        230800,
        4000,
        750,
        8691,
        14,
        32,
        110000,
        3200000,
        8
    ],
    "Growth_Rate": [
        14.3,
        15.4,
        25.0,
        164.1,
        33.7,
        14.0,
        32.0,
        15.8,
        28.0,
        60.0
    ]
}

df_tech = pd.DataFrame(tech_data)
df_tech.to_csv("houston_tech_sector_impact.csv", index=False)
print("Houston Tech Sector Impact Data:")
print(df_tech.head(10))
print("\n" + "="*50 + "\n")

print("All data files have been created successfully!")
print("Files created:")
print("- houston_population_growth_by_area.csv")
print("- houston_job_growth_by_sector.csv") 
print("- houston_housing_market_data.csv")
print("- houston_commercial_real_estate_data.csv")
print("- houston_tech_sector_impact.csv")