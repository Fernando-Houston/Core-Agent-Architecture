#!/usr/bin/env python3
"""
Test Integrated Perplexity + Refresh Agents
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_daily_refresh():
    """Test daily refresh with live data"""
    print("\n🌅 Testing Daily Refresh Agent with Perplexity...")
    
    try:
        from daily_refresh_agent import DailyRefreshAgent
        
        agent = DailyRefreshAgent()
        
        # Test permit fetching
        print("\n📋 Fetching permits...")
        permits = agent.fetch_permits()
        print(f"✅ Found {len(permits)} permits")
        
        if permits:
            print(f"Sample permit: {permits[0]['address']} - ${permits[0]['value']:,.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_weekly_refresh():
    """Test weekly refresh with live data"""
    print("\n📊 Testing Weekly Refresh Agent with Perplexity...")
    
    try:
        from weekly_refresh_agent import WeeklyRefreshAgent
        
        agent = WeeklyRefreshAgent()
        
        # Test market analysis
        print("\n📈 Analyzing market trends...")
        trends = agent.analyze_market_trends()
        
        print(f"✅ Analyzed {len(trends)} areas")
        
        for area, data in trends.items():
            if data.get('median_price'):
                print(f"{area}: ${data['median_price']:,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run integration tests"""
    print("🚀 Houston Intelligence Platform - Integration Test")
    print("="*50)
    
    # Check API key
    if not os.getenv('PERPLEXITY_API_KEY'):
        print("❌ PERPLEXITY_API_KEY not set!")
        print("Set with: export PERPLEXITY_API_KEY='pplx-your-key'")
        return
    
    # Run tests
    daily_success = test_daily_refresh()
    weekly_success = test_weekly_refresh()
    
    print("\n" + "="*50)
    print("📊 Integration Test Results")
    print("="*50)
    print(f"Daily Refresh: {'✅ Success' if daily_success else '❌ Failed'}")
    print(f"Weekly Refresh: {'✅ Success' if weekly_success else '❌ Failed'}")
    
    if daily_success and weekly_success:
        print("\n✨ All tests passed! Ready for production.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()