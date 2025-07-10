#!/usr/bin/env python3
"""
Test Perplexity API Integration
Run this to verify your API key and test queries
"""

import os
import json
from datetime import datetime

# Check if requests is installed
try:
    import requests
except ImportError:
    print("❌ Error: 'requests' package not installed")
    print("📦 Install with: pip3 install requests")
    exit(1)

# Import our Perplexity client
try:
    from perplexity_integration import PerplexityClient
except ImportError:
    print("❌ Error: Could not import PerplexityClient")
    print("Make sure you're in the Core Agent Architecture directory")
    exit(1)

def test_api_key():
    """Test if API key is configured"""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    
    if not api_key:
        print("❌ PERPLEXITY_API_KEY not set!")
        print("\n📝 To set your API key:")
        print("   export PERPLEXITY_API_KEY='pplx-your-key-here'")
        print("\n🔑 Get your key at: https://www.perplexity.ai/settings/api")
        return False
    
    if not api_key.startswith('pplx-'):
        print("⚠️  Warning: API key should start with 'pplx-'")
        return False
    
    print(f"✅ API Key configured: {api_key[:10]}...")
    return True

def test_basic_query():
    """Test a basic Perplexity query"""
    print("\n🧪 Testing basic query...")
    
    client = PerplexityClient()
    result = client.search_houston_data(
        "Houston real estate market overview 2025",
        "market_overview"
    )
    
    if result['success']:
        print("✅ Query successful!")
        print(f"📝 Response preview: {result['content'][:200]}...")
        if result.get('citations'):
            print(f"📚 Citations: {len(result['citations'])} sources")
        return True
    else:
        print(f"❌ Query failed: {result.get('error')}")
        return False

def test_houston_queries():
    """Test Houston-specific queries"""
    print("\n🏙️ Testing Houston-specific queries...")
    
    client = PerplexityClient()
    
    test_queries = [
        {
            "name": "Building Permits",
            "query": "Houston building permits issued January 2025 major projects",
            "type": "permits"
        },
        {
            "name": "Market Trends",
            "query": "Houston Heights real estate median price trends 2025",
            "type": "market"
        },
        {
            "name": "Development News",
            "query": "New mixed-use developments announced Houston 2025",
            "type": "developments"
        }
    ]
    
    results = []
    for test in test_queries:
        print(f"\n📊 Testing: {test['name']}")
        result = client.search_houston_data(test['query'], test['type'])
        
        if result['success']:
            print(f"✅ Success! Found data about {test['name']}")
            print(f"Preview: {result['content'][:150]}...")
            results.append({
                "query": test['name'],
                "success": True,
                "has_citations": bool(result.get('citations'))
            })
        else:
            print(f"❌ Failed: {result.get('error')}")
            results.append({
                "query": test['name'],
                "success": False,
                "error": result.get('error')
            })
    
    return results

def test_daily_updates():
    """Test the daily updates function"""
    print("\n📅 Testing daily updates function...")
    
    client = PerplexityClient()
    updates = client.get_daily_updates()
    
    if updates:
        print(f"✅ Retrieved {len(updates)} daily updates")
        for topic, content in updates.items():
            print(f"\n📌 {topic}")
            print(f"   {content[:100]}...")
    else:
        print("❌ No daily updates retrieved")
    
    return updates

def test_property_research():
    """Test property-specific research"""
    print("\n🏠 Testing property research...")
    
    client = PerplexityClient()
    test_address = "1000 Main St, Houston, TX"
    
    result = client.research_property(test_address)
    
    if result['success']:
        print(f"✅ Property research successful for: {test_address}")
        print(f"📝 Found: {result['content'][:200]}...")
    else:
        print(f"❌ Property research failed: {result.get('error')}")
    
    return result

def test_market_analysis():
    """Test market analysis for different areas"""
    print("\n📈 Testing market analysis...")
    
    client = PerplexityClient()
    areas = ["Houston Heights", "River Oaks", "Montrose"]
    
    for area in areas:
        print(f"\n🏘️ Analyzing: {area}")
        result = client.analyze_market_trends(area)
        
        if result['success']:
            print(f"✅ Found market data for {area}")
            print(f"Preview: {result['content'][:150]}...")
        else:
            print(f"❌ Failed to analyze {area}")

def save_test_results(results):
    """Save test results for reference"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"perplexity_test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {filename}")

def main():
    """Run all tests"""
    print("🚀 Perplexity API Integration Test Suite")
    print("="*50)
    
    # Test 1: API Key
    if not test_api_key():
        print("\n⚠️  Please configure your API key first!")
        return
    
    # Test 2: Basic Query
    basic_success = test_basic_query()
    
    if not basic_success:
        print("\n⚠️  Basic query failed. Check your API key and internet connection.")
        return
    
    # Test 3: Houston Queries
    houston_results = test_houston_queries()
    
    # Test 4: Daily Updates
    daily_updates = test_daily_updates()
    
    # Test 5: Property Research
    property_result = test_property_research()
    
    # Test 6: Market Analysis
    test_market_analysis()
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Summary")
    print("="*50)
    
    successful_tests = sum(1 for r in houston_results if r['success'])
    total_tests = len(houston_results)
    
    print(f"✅ API Key: Configured")
    print(f"✅ Basic Query: Successful")
    print(f"📈 Houston Queries: {successful_tests}/{total_tests} successful")
    print(f"📅 Daily Updates: {'✅' if daily_updates else '❌'}")
    print(f"🏠 Property Research: {'✅' if property_result.get('success') else '❌'}")
    
    # Save results
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": True,
        "basic_query_success": basic_success,
        "houston_queries": houston_results,
        "daily_updates_count": len(daily_updates) if daily_updates else 0
    }
    
    save_test_results(all_results)
    
    print("\n✨ Perplexity integration test complete!")
    print("\n🎯 Next steps:")
    print("1. Update refresh agents to use live Perplexity data")
    print("2. Run the full pipeline with real data")
    print("3. Deploy to production")

if __name__ == "__main__":
    main()