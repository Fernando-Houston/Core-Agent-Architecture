#!/usr/bin/env python3
"""
Test All Houston Data Sources
Verifies FREE APIs + Perplexity AI + HCAD search
"""

import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file

print("🚀 Testing All Houston Intelligence Data Sources")
print("="*60)

# Check environment variables
print("\n🔐 Environment Variables:")
perplexity_key = os.getenv('PERPLEXITY_API_KEY', '')
census_key = os.getenv('CENSUS_API_KEY', '')

print(f"✅ Perplexity API Key: {'Configured' if perplexity_key.startswith('pplx-') else '❌ Missing'}")
print(f"✅ Census API Key: {'Configured' if census_key else '❌ Missing'}")

# Test imports
try:
    from houston_free_data import HoustonFreeDataClient
    from perplexity_integration import PerplexityClient
    from hcad_perplexity_search import HCADPerplexitySearch
    print("\n✅ All modules imported successfully")
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    exit(1)

# Test FREE Houston APIs
print("\n" + "="*60)
print("🏙️ Testing FREE Houston APIs")
print("="*60)

free_client = HoustonFreeDataClient()

# 1. Test Building Permits (FREE - No Key Required)
print("\n1️⃣ Houston Building Permits API:")
try:
    permits = free_client.get_building_permits(days_back=7, limit=3)
    if permits:
        print(f"✅ SUCCESS: Found {len(permits)} recent permits")
        print(f"   Latest: {permits[0]['address']} - ${permits[0]['value']:,.0f}")
    else:
        print("⚠️  No permits found (API may be down)")
except Exception as e:
    print(f"❌ ERROR: {e}")

# 2. Test Code Violations (FREE - No Key Required)
print("\n2️⃣ Houston Code Violations API:")
try:
    violations = free_client.get_code_violations(days_back=30, limit=3)
    if violations:
        print(f"✅ SUCCESS: Found {len(violations)} code violations")
        print(f"   Latest: {violations[0]['address']}")
    else:
        print("⚠️  No violations found")
except Exception as e:
    print(f"❌ ERROR: {e}")

# 3. Test Weather API (FREE - No Key Required)
print("\n3️⃣ NOAA Weather API:")
try:
    weather = free_client.get_houston_weather()
    if 'current_forecast' in weather:
        print(f"✅ SUCCESS: {weather['current_forecast']['shortForecast']}")
        print(f"   Temperature: {weather['current_forecast']['temperature']}°{weather['current_forecast']['temperatureUnit']}")
    else:
        print("⚠️  Weather data not available")
except Exception as e:
    print(f"❌ ERROR: {e}")

# 4. Test Census API (FREE with Key)
print("\n4️⃣ US Census API:")
if census_key:
    try:
        # Test with all tracts in Harris County
        census_data = free_client.get_census_data(census_tract="*", api_key=census_key)
        if 'tracts' in census_data:
            print(f"✅ SUCCESS: Found data for {len(census_data['tracts'])} census tracts")
            if census_data['tracts']:
                sample = census_data['tracts'][0]
                print(f"   Sample: {sample['name']}")
                print(f"   Population: {sample['population']:,}")
                print(f"   Median Income: ${sample['median_income']:,}")
        else:
            print(f"⚠️  Census API returned: {census_data}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
else:
    print("⚠️  SKIPPED: No Census API key configured")

# Test Perplexity AI
print("\n" + "="*60)
print("🤖 Testing Perplexity AI Integration")
print("="*60)

if perplexity_key:
    perplexity_client = PerplexityClient()
    
    # Test basic query
    print("\n5️⃣ Perplexity Market Analysis:")
    try:
        result = perplexity_client.analyze_market_trends("Houston Heights")
        if result['success']:
            print("✅ SUCCESS: Market analysis retrieved")
            print(f"   Preview: {result['content'][:100]}...")
        else:
            print(f"❌ FAILED: {result.get('error')}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
else:
    print("⚠️  SKIPPED: No Perplexity API key configured")

# Test HCAD Search via Perplexity
print("\n" + "="*60)
print("🏢 Testing HCAD Search via Perplexity")
print("="*60)

if perplexity_key:
    hcad_search = HCADPerplexitySearch()
    
    print("\n6️⃣ HCAD Property Search:")
    try:
        property_data = hcad_search.search_property("1000 Louisiana St, Houston, TX")
        if not property_data.get('error'):
            print("✅ SUCCESS: Property data retrieved via Perplexity")
            print(f"   Owner: {property_data.get('owner', 'N/A')}")
            print(f"   Value: ${property_data.get('appraised_value', 0):,}")
        else:
            print(f"⚠️  {property_data.get('error')}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
else:
    print("⚠️  SKIPPED: Requires Perplexity API")

# Summary
print("\n" + "="*60)
print("📊 Data Sources Summary")
print("="*60)

print("\n✅ FREE APIs (No Key Required):")
print("  • Houston Building Permits - data.houstontx.gov")
print("  • Houston Code Violations - data.houstontx.gov")
print("  • NOAA Weather - api.weather.gov")

print("\n✅ FREE APIs (Key Required):")
print(f"  • US Census - {'ACTIVE' if census_key else 'Need key from census.gov'}")

print("\n💰 PAID APIs:")
print(f"  • Perplexity AI ($20/mo) - {'ACTIVE' if perplexity_key else 'Need key'}")

print("\n🔧 Workarounds:")
print("  • HCAD - Using Perplexity to search public records")

print("\n💡 Total Monthly Cost: $20 (vs $1,800 traditional)")
print("\n✨ Testing complete!")