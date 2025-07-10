#!/usr/bin/env python3
"""
Activate Live Data for Houston Intelligence Platform
Implements the hybrid data strategy with free APIs + Perplexity
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HoustonLiveDataActivator:
    """Activates all live data sources for the platform"""
    
    def __init__(self):
        self.base_path = Path("/Users/fernandox/Desktop/Core Agent Architecture")
        self.config = self.load_config()
        
    def load_config(self):
        """Load API configurations"""
        return {
            "houston_open_data": {
                "base_url": "https://data.houstontx.gov/resource",
                "endpoints": {
                    "permits": "/3tts-58vt.json",  # Building permits
                    "inspections": "/k85k-sgqf.json",  # Inspections
                    "violations": "/azmy-mepx.json"  # Code violations
                }
            },
            "hcad": {
                "base_url": "https://public.hcad.org/records",
                "search_endpoint": "/Real.asp"
            },
            "census": {
                "base_url": "https://api.census.gov/data",
                "key": os.getenv("CENSUS_API_KEY", "")  # Free with registration
            },
            "perplexity": {
                "api_key": os.getenv("PERPLEXITY_API_KEY", ""),
                "model": "pplx-70b-online"
            }
        }
    
    def test_houston_open_data(self) -> Dict:
        """Test Houston Open Data Portal APIs"""
        logger.info("Testing Houston Open Data APIs...")
        results = {}
        
        base_url = self.config["houston_open_data"]["base_url"]
        
        # Test building permits API
        try:
            url = f"{base_url}{self.config['houston_open_data']['endpoints']['permits']}"
            params = {
                "$limit": 10,
                "$order": "permit_issue_date DESC",
                "$where": "permit_issue_date > '2024-01-01'"
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                permits = response.json()
                results["permits"] = {
                    "status": "success",
                    "count": len(permits),
                    "sample": permits[0] if permits else None
                }
                logger.info(f"✅ Permits API: Found {len(permits)} recent permits")
            else:
                results["permits"] = {"status": "error", "code": response.status_code}
                
        except Exception as e:
            results["permits"] = {"status": "error", "message": str(e)}
            logger.error(f"❌ Permits API error: {e}")
        
        return results
    
    def setup_free_apis(self) -> Dict:
        """Setup connections to all free APIs"""
        logger.info("Setting up free API connections...")
        
        free_apis = {
            "houston_permits": {
                "url": "https://data.houstontx.gov/resource/3tts-58vt.json",
                "description": "Building permits data",
                "auth_required": False
            },
            "hcad_property": {
                "url": "https://public.hcad.org/",
                "description": "Property assessments",
                "auth_required": False
            },
            "census_data": {
                "url": "https://api.census.gov/data/2023/acs/acs5",
                "description": "Demographics data",
                "auth_required": True,
                "key_url": "https://api.census.gov/data/key_signup.html"
            },
            "noaa_weather": {
                "url": "https://api.weather.gov/points/29.7604,-95.3698",
                "description": "Houston weather data",
                "auth_required": False
            }
        }
        
        return free_apis
    
    def create_live_data_fetcher(self):
        """Create a unified live data fetcher"""
        fetcher_code = '''#!/usr/bin/env python3
"""
Live Data Fetcher for Houston Intelligence Platform
Combines free APIs with Perplexity AI enhancement
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class HoustonLiveDataFetcher:
    """Fetches live data from multiple sources"""
    
    def __init__(self):
        self.sources = {
            "permits": self.fetch_houston_permits,
            "property": self.fetch_hcad_data,
            "demographics": self.fetch_census_data,
            "market": self.fetch_perplexity_market
        }
    
    def fetch_houston_permits(self, limit: int = 100) -> List[Dict]:
        """Fetch recent building permits from Houston Open Data"""
        url = "https://data.houstontx.gov/resource/3tts-58vt.json"
        params = {
            "$limit": limit,
            "$order": "permit_issue_date DESC",
            "$where": f"permit_issue_date > '{datetime.now().strftime('%Y-01-01')}'"
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                permits = response.json()
                
                # Structure for our system
                structured_permits = []
                for permit in permits:
                    structured_permits.append({
                        "permit_number": permit.get("permit_number"),
                        "address": f"{permit.get('street_number', '')} {permit.get('street_name', '')}",
                        "type": permit.get("permit_type"),
                        "value": float(permit.get("estimated_cost", 0)),
                        "issued_date": permit.get("permit_issue_date"),
                        "developer": permit.get("applicant_name"),
                        "description": permit.get("description"),
                        "source": "Houston Open Data Portal"
                    })
                
                return structured_permits
        except Exception as e:
            print(f"Error fetching permits: {e}")
            return []
    
    def fetch_hcad_data(self, address: str) -> Dict:
        """Fetch property data from HCAD (Harris County Appraisal District)"""
        # HCAD requires web scraping or their paid API
        # For now, return structure for implementation
        return {
            "address": address,
            "assessed_value": 0,
            "owner": "",
            "year_built": 0,
            "square_feet": 0,
            "source": "HCAD"
        }
    
    def fetch_census_data(self, tract: str) -> Dict:
        """Fetch demographic data from US Census API"""
        # Requires API key (free with registration)
        api_key = os.getenv("CENSUS_API_KEY", "")
        
        if not api_key:
            return {"error": "Census API key not configured"}
        
        url = "https://api.census.gov/data/2023/acs/acs5"
        params = {
            "get": "B01003_001E,B19013_001E,B25077_001E",  # Population, Income, Home Value
            "for": f"tract:{tract}",
            "in": "state:48 county:201",  # Texas, Harris County
            "key": api_key
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return {
                    "population": data[1][0],
                    "median_income": data[1][1],
                    "median_home_value": data[1][2],
                    "source": "US Census Bureau"
                }
        except Exception as e:
            print(f"Error fetching census data: {e}")
            
        return {}
    
    def fetch_perplexity_market(self, query: str) -> Dict:
        """Enhance data with Perplexity AI market intelligence"""
        from perplexity_integration import PerplexityClient
        
        client = PerplexityClient()
        result = client.search_houston_data(query, "market_intelligence")
        
        if result['success']:
            return {
                "query": query,
                "insights": result['content'],
                "citations": result.get('citations', []),
                "timestamp": datetime.now().isoformat(),
                "source": "Perplexity AI"
            }
        
        return {"error": "Failed to fetch market intelligence"}
    
    def fetch_all_live_data(self) -> Dict:
        """Fetch data from all sources"""
        live_data = {
            "timestamp": datetime.now().isoformat(),
            "permits": self.fetch_houston_permits(50),
            "market_intelligence": self.fetch_perplexity_market(
                "Houston real estate market trends and opportunities 2025"
            )
        }
        
        return live_data

# Test the fetcher
if __name__ == "__main__":
    fetcher = HoustonLiveDataFetcher()
    
    print("Fetching live Houston data...")
    data = fetcher.fetch_all_live_data()
    
    print(f"\\nFound {len(data['permits'])} recent permits")
    if data['permits']:
        print(f"Latest permit: {data['permits'][0]['address']}")
    
    print("\\nMarket Intelligence:", data['market_intelligence'].get('insights', '')[:200] + "...")
'''
        
        # Save the live data fetcher
        fetcher_path = self.base_path / "houston_live_data_fetcher.py"
        with open(fetcher_path, 'w') as f:
            f.write(fetcher_code)
        
        logger.info(f"✅ Created live data fetcher: {fetcher_path}")
        return fetcher_path
    
    def update_refresh_agents(self):
        """Update refresh agents to use live data"""
        updates = {
            "daily_refresh_agent.py": {
                "function": "fetch_permits",
                "old_pattern": "# Simulate API call",
                "new_code": '''
        from houston_live_data_fetcher import HoustonLiveDataFetcher
        fetcher = HoustonLiveDataFetcher()
        return fetcher.fetch_houston_permits(100)
'''
            },
            "weekly_refresh_agent.py": {
                "function": "analyze_market_trends",
                "old_pattern": "# Simulate trend analysis",
                "new_code": '''
        from houston_live_data_fetcher import HoustonLiveDataFetcher
        fetcher = HoustonLiveDataFetcher()
        return fetcher.fetch_perplexity_market("Houston real estate weekly market analysis")
'''
            }
        }
        
        logger.info("📝 Update instructions for refresh agents:")
        for file, update in updates.items():
            logger.info(f"\nFile: {file}")
            logger.info(f"Function: {update['function']}")
            logger.info(f"Replace simulation with live data fetching")
    
    def create_activation_script(self):
        """Create a script to activate all live data sources"""
        activation_script = '''#!/bin/bash
# Activate Live Data for Houston Intelligence Platform

echo "🚀 Activating Live Data Sources..."

# Check for environment variables
if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "⚠️  Warning: PERPLEXITY_API_KEY not set"
    echo "   Set it with: export PERPLEXITY_API_KEY='your-key-here'"
fi

if [ -z "$CENSUS_API_KEY" ]; then
    echo "⚠️  Warning: CENSUS_API_KEY not set"
    echo "   Get free key at: https://api.census.gov/data/key_signup.html"
fi

# Test Houston Open Data
echo "\\n📊 Testing Houston Open Data Portal..."
python3 -c "
import requests
r = requests.get('https://data.houstontx.gov/resource/3tts-58vt.json?$limit=1')
if r.status_code == 200:
    print('✅ Houston Open Data: Connected')
else:
    print('❌ Houston Open Data: Failed')
"

# Test Perplexity if key exists
if [ ! -z "$PERPLEXITY_API_KEY" ]; then
    echo "\\n🤖 Testing Perplexity AI..."
    python3 -c "
from perplexity_integration import PerplexityClient
client = PerplexityClient()
print('✅ Perplexity AI: Configured')
"
fi

echo "\\n✨ Live data activation complete!"
echo "\\nNext steps:"
echo "1. Run: python3 houston_live_data_fetcher.py"
echo "2. Update refresh agents to use live data"
echo "3. Test the API endpoints with real data"
'''
        
        script_path = self.base_path / "activate_live_data.sh"
        with open(script_path, 'w') as f:
            f.write(activation_script)
        
        os.chmod(script_path, 0o755)
        logger.info(f"✅ Created activation script: {script_path}")
        
        return script_path

def main():
    """Main activation process"""
    logger.info("🚀 Houston Intelligence Platform - Live Data Activation")
    
    activator = HoustonLiveDataActivator()
    
    # Step 1: Test Houston Open Data
    logger.info("\n1️⃣ Testing Houston Open Data APIs...")
    test_results = activator.test_houston_open_data()
    
    # Step 2: Setup free APIs
    logger.info("\n2️⃣ Setting up free API connections...")
    free_apis = activator.setup_free_apis()
    
    # Step 3: Create live data fetcher
    logger.info("\n3️⃣ Creating unified live data fetcher...")
    fetcher_path = activator.create_live_data_fetcher()
    
    # Step 4: Provide refresh agent updates
    logger.info("\n4️⃣ Refresh agent update instructions...")
    activator.update_refresh_agents()
    
    # Step 5: Create activation script
    logger.info("\n5️⃣ Creating activation script...")
    script_path = activator.create_activation_script()
    
    logger.info("\n✅ Live Data Activation Complete!")
    logger.info("\nTo activate:")
    logger.info(f"1. cd '{activator.base_path}'")
    logger.info("2. export PERPLEXITY_API_KEY='your-key-here'")
    logger.info("3. ./activate_live_data.sh")
    logger.info("4. python3 houston_live_data_fetcher.py")

if __name__ == "__main__":
    main()