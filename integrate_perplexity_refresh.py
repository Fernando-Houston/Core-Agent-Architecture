#!/usr/bin/env python3
"""
Integrate Perplexity API with Refresh Agents
Updates the daily, weekly, and monthly refresh agents to use live data
"""

import os
from pathlib import Path
from datetime import datetime

def create_perplexity_parsers():
    """Create parser functions for Perplexity responses"""
    parser_code = '''#!/usr/bin/env python3
"""
Perplexity Response Parsers
Convert Perplexity AI responses into structured data
"""

import re
import json
from typing import Dict, List, Optional
from datetime import datetime

class PerplexityParser:
    """Parse Perplexity responses into structured data"""
    
    @staticmethod
    def parse_permits(content: str) -> List[Dict]:
        """Extract permit information from Perplexity response"""
        permits = []
        
        # Look for permit patterns in the response
        # Example: "123 Main St - $2.5M commercial development"
        permit_pattern = r'(\d+\s+[\w\s]+(?:St|Ave|Rd|Blvd|Dr|Ln|Way))\s*[-–]\s*\$?([\d.,]+)(?:M|K)?\s*(\w+)'
        
        matches = re.findall(permit_pattern, content)
        
        for i, match in enumerate(matches):
            address, value_str, permit_type = match
            
            # Convert value string to number
            value = value_str.replace(',', '')
            if 'M' in content[content.find(value_str):content.find(value_str)+10]:
                value = float(value) * 1000000
            elif 'K' in content[content.find(value_str):content.find(value_str)+10]:
                value = float(value) * 1000
            else:
                value = float(value)
            
            permits.append({
                "permit_number": f"2025-{str(i+1).zfill(6)}",
                "address": address.strip(),
                "type": permit_type.lower(),
                "value": value,
                "issued_date": datetime.now().strftime("%Y-%m-%d"),
                "source": "Perplexity AI",
                "confidence": 0.8
            })
        
        return permits
    
    @staticmethod
    def parse_market_data(content: str) -> Dict:
        """Extract market statistics from Perplexity response"""
        market_data = {
            "median_price": None,
            "inventory": None,
            "days_on_market": None,
            "price_trend": None,
            "key_insights": []
        }
        
        # Extract median price
        price_pattern = r'median\s+(?:home\s+)?price[:\s]+\$?([\d,]+)'
        price_match = re.search(price_pattern, content, re.IGNORECASE)
        if price_match:
            market_data["median_price"] = int(price_match.group(1).replace(',', ''))
        
        # Extract inventory
        inventory_pattern = r'(\d+)\s+(?:homes?|properties)\s+(?:for sale|available|on market)'
        inventory_match = re.search(inventory_pattern, content, re.IGNORECASE)
        if inventory_match:
            market_data["inventory"] = int(inventory_match.group(1))
        
        # Extract days on market
        dom_pattern = r'(\d+)\s+days?\s+on\s+market'
        dom_match = re.search(dom_pattern, content, re.IGNORECASE)
        if dom_match:
            market_data["days_on_market"] = int(dom_match.group(1))
        
        # Determine price trend
        if 'increase' in content.lower() or 'up' in content.lower():
            market_data["price_trend"] = "increasing"
        elif 'decrease' in content.lower() or 'down' in content.lower():
            market_data["price_trend"] = "decreasing"
        else:
            market_data["price_trend"] = "stable"
        
        # Extract key insights (sentences with important info)
        sentences = content.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in ['growth', 'demand', 'inventory', 'trend', 'forecast']):
                market_data["key_insights"].append(sentence.strip())
        
        return market_data
    
    @staticmethod
    def parse_developments(content: str) -> List[Dict]:
        """Extract development project information"""
        developments = []
        
        # Look for development patterns
        # Example: "East River mixed-use project by Hines"
        dev_pattern = r'([A-Z][\w\s]+?)\s+(?:mixed-use|residential|commercial|retail)\s+(?:project|development)(?:\s+by\s+([\w\s]+))?'
        
        matches = re.findall(dev_pattern, content)
        
        for project_name, developer in matches:
            developments.append({
                "name": project_name.strip(),
                "developer": developer.strip() if developer else "Unknown",
                "type": "mixed-use" if "mixed-use" in content else "commercial",
                "status": "announced",
                "source": "Perplexity AI",
                "announcement_date": datetime.now().strftime("%Y-%m-%d")
            })
        
        return developments
    
    @staticmethod
    def parse_investment_opportunities(content: str) -> List[Dict]:
        """Extract investment opportunities"""
        opportunities = []
        
        # Extract areas mentioned with investment potential
        area_pattern = r'([\w\s]+)\s+(?:offers?|shows?|has)\s+(?:strong|high|good)\s+(?:investment|ROI|return)'
        
        matches = re.findall(area_pattern, content, re.IGNORECASE)
        
        for area in matches:
            opportunities.append({
                "location": area.strip(),
                "type": "investment_opportunity",
                "potential": "high",
                "source": "Perplexity AI",
                "identified_date": datetime.now().strftime("%Y-%m-%d")
            })
        
        return opportunities

# Testing functions
if __name__ == "__main__":
    # Test permit parsing
    test_permit_content = """
    Recent permits issued in Houston:
    - 123 Main Street - $2.5M commercial development
    - 456 Westheimer Rd - $1.2M residential project
    - 789 Memorial Drive - $5M mixed-use development
    """
    
    parser = PerplexityParser()
    permits = parser.parse_permits(test_permit_content)
    print("Parsed Permits:", json.dumps(permits, indent=2))
    
    # Test market parsing
    test_market_content = """
    Houston Heights market update: The median home price is $485,000, 
    up 5% from last year. Currently 156 homes for sale with average 
    45 days on market. Demand remains strong with multiple offers common.
    """
    
    market_data = parser.parse_market_data(test_market_content)
    print("\\nParsed Market Data:", json.dumps(market_data, indent=2))
'''
    
    # Save parser file
    parser_path = Path("perplexity_parsers.py")
    with open(parser_path, 'w') as f:
        f.write(parser_code)
    
    print(f"✅ Created parser file: {parser_path}")
    return parser_path

def create_updated_daily_refresh():
    """Create updated daily refresh agent with Perplexity integration"""
    
    updated_code = '''def fetch_permits(self):
        """Fetch latest building permits using Perplexity"""
        from perplexity_integration import PerplexityClient
        from perplexity_parsers import PerplexityParser
        
        self.log("Fetching building permits via Perplexity AI...")
        
        client = PerplexityClient()
        parser = PerplexityParser()
        
        # Query for recent permits
        result = client.search_houston_data(
            "Houston building permits issued this week major commercial residential projects addresses values",
            "permits"
        )
        
        if result['success']:
            # Parse the response to extract permit data
            permits = parser.parse_permits(result['content'])
            self.log(f"Found {len(permits)} permits from Perplexity")
            
            # Add citations to each permit
            for permit in permits:
                permit['citations'] = result.get('citations', [])
            
            return permits
        else:
            self.log(f"Error fetching permits: {result.get('error')}")
            return []
    
    def fetch_mls_updates(self):
        """Fetch MLS updates using Perplexity"""
        from perplexity_data_replacement import PerplexityDataAggregator
        
        self.log("Fetching MLS updates via Perplexity...")
        
        aggregator = PerplexityDataAggregator()
        
        # Get data for key areas
        areas = ["Houston Heights", "River Oaks", "Montrose", "The Woodlands"]
        all_listings = []
        
        for area in areas:
            self.log(f"Fetching listings for {area}...")
            data = aggregator.get_mls_alternative_data(area)
            
            if data.get('listings'):
                all_listings.extend(data['listings'])
        
        self.log(f"Found {len(all_listings)} total listings")
        return all_listings'''
    
    print("\n📝 Update Instructions for daily_refresh_agent.py:")
    print("Replace the fetch_permits() and fetch_mls_updates() functions with:")
    print("-" * 60)
    print(updated_code)
    print("-" * 60)

def create_updated_weekly_refresh():
    """Create updated weekly refresh agent with Perplexity integration"""
    
    updated_code = '''def analyze_market_trends(self):
        """Analyze market trends using Perplexity"""
        from perplexity_integration import PerplexityClient
        from perplexity_parsers import PerplexityParser
        
        self.log("Analyzing market trends via Perplexity AI...")
        
        client = PerplexityClient()
        parser = PerplexityParser()
        
        trends = {}
        areas = ["Houston Heights", "River Oaks", "Montrose", "Midtown", "The Woodlands"]
        
        for area in areas:
            self.log(f"Analyzing {area}...")
            result = client.analyze_market_trends(area)
            
            if result['success']:
                # Parse market data
                market_data = parser.parse_market_data(result['content'])
                market_data['raw_analysis'] = result['content']
                market_data['citations'] = result.get('citations', [])
                trends[area] = market_data
            else:
                self.log(f"Error analyzing {area}: {result.get('error')}")
        
        return trends
    
    def get_competitive_analysis(self):
        """Get competitive developer analysis using Perplexity"""
        from perplexity_integration import PerplexityClient
        
        self.log("Fetching competitive analysis...")
        
        client = PerplexityClient()
        
        # Query for top developers and their activity
        result = client.search_houston_data(
            "Top Houston real estate developers 2025 projects market share DR Horton Lennar Perry Homes",
            "competitive_analysis"
        )
        
        if result['success']:
            return {
                "analysis": result['content'],
                "citations": result.get('citations', []),
                "timestamp": datetime.now().isoformat()
            }
        
        return {}'''
    
    print("\n📝 Update Instructions for weekly_refresh_agent.py:")
    print("Replace the market analysis functions with:")
    print("-" * 60)
    print(updated_code)
    print("-" * 60)

def create_integration_test():
    """Create a test script for the integrated system"""
    
    test_code = '''#!/usr/bin/env python3
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
    print("\\n🌅 Testing Daily Refresh Agent with Perplexity...")
    
    try:
        from daily_refresh_agent import DailyRefreshAgent
        
        agent = DailyRefreshAgent()
        
        # Test permit fetching
        print("\\n📋 Fetching permits...")
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
    print("\\n📊 Testing Weekly Refresh Agent with Perplexity...")
    
    try:
        from weekly_refresh_agent import WeeklyRefreshAgent
        
        agent = WeeklyRefreshAgent()
        
        # Test market analysis
        print("\\n📈 Analyzing market trends...")
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
    
    print("\\n" + "="*50)
    print("📊 Integration Test Results")
    print("="*50)
    print(f"Daily Refresh: {'✅ Success' if daily_success else '❌ Failed'}")
    print(f"Weekly Refresh: {'✅ Success' if weekly_success else '❌ Failed'}")
    
    if daily_success and weekly_success:
        print("\\n✨ All tests passed! Ready for production.")
    else:
        print("\\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()'''
    
    # Save test file
    test_path = Path("test_integration.py")
    with open(test_path, 'w') as f:
        f.write(test_code)
    
    os.chmod(test_path, 0o755)
    print(f"\n✅ Created integration test: {test_path}")

def main():
    """Main integration process"""
    print("🚀 Perplexity API Integration for Houston Intelligence Platform")
    print("="*60)
    
    # Step 1: Create parsers
    print("\n1️⃣ Creating Perplexity response parsers...")
    create_perplexity_parsers()
    
    # Step 2: Show daily refresh updates
    print("\n2️⃣ Daily Refresh Agent Updates:")
    create_updated_daily_refresh()
    
    # Step 3: Show weekly refresh updates
    print("\n3️⃣ Weekly Refresh Agent Updates:")
    create_updated_weekly_refresh()
    
    # Step 4: Create integration test
    print("\n4️⃣ Creating integration test script...")
    create_integration_test()
    
    print("\n✅ Perplexity Integration Guide Complete!")
    print("\n📋 Next Steps:")
    print("1. Get your API key from: https://www.perplexity.ai/settings/api")
    print("2. Set environment variable: export PERPLEXITY_API_KEY='pplx-your-key'")
    print("3. Install requests: pip3 install requests")
    print("4. Run test: python3 test_perplexity.py")
    print("5. Update refresh agents with the code shown above")
    print("6. Test integration: python3 test_integration.py")

if __name__ == "__main__":
    main()