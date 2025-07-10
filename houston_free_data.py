#!/usr/bin/env python3
"""
Houston Free Data Sources Integration
Implements actual API calls to free Houston data sources
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HoustonFreeDataClient:
    """Client for accessing free Houston data sources"""
    
    def __init__(self):
        self.houston_data_base = "https://data.houstontx.gov/resource"
        self.census_base = "https://api.census.gov/data"
        self.weather_base = "https://api.weather.gov"
        
    def get_building_permits(self, days_back: int = 7, limit: int = 100) -> List[Dict]:
        """
        Fetch recent building permits from Houston Open Data Portal
        No API key required!
        """
        endpoint = f"{self.houston_data_base}/3tts-58vt.json"
        
        # Calculate date for query
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        params = {
            "$limit": limit,
            "$order": "permit_issue_date DESC",
            "$where": f"permit_issue_date > '{start_date}'"
        }
        
        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                permits = response.json()
                
                # Structure for our system
                structured_permits = []
                for permit in permits:
                    structured_permits.append({
                        "permit_number": permit.get("permit_number", ""),
                        "address": f"{permit.get('street_number', '')} {permit.get('street_name', '')} {permit.get('street_suffix', '')}".strip(),
                        "type": permit.get("permit_type", ""),
                        "subtype": permit.get("work_description", ""),
                        "value": float(permit.get("estimated_cost", 0)),
                        "issued_date": permit.get("permit_issue_date", ""),
                        "status": permit.get("status", ""),
                        "applicant": permit.get("applicant_name", ""),
                        "contractor": permit.get("contractor_name", ""),
                        "description": permit.get("project_description", ""),
                        "source": "Houston Open Data Portal",
                        "data_freshness": datetime.now().isoformat()
                    })
                
                logger.info(f"✅ Fetched {len(structured_permits)} permits from Houston Open Data")
                return structured_permits
            else:
                logger.error(f"❌ Error fetching permits: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return []
    
    def get_code_violations(self, days_back: int = 30, limit: int = 50) -> List[Dict]:
        """
        Fetch recent code violations from Houston Open Data
        Useful for identifying distressed properties
        """
        endpoint = f"{self.houston_data_base}/5kz8-qxbv.json"
        
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        params = {
            "$limit": limit,
            "$order": "date_violation_created DESC",
            "$where": f"date_violation_created > '{start_date}'"
        }
        
        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                violations = response.json()
                
                structured_violations = []
                for violation in violations:
                    structured_violations.append({
                        "case_number": violation.get("case_number", ""),
                        "address": violation.get("full_address", ""),
                        "violation_type": violation.get("violation_category", ""),
                        "description": violation.get("violation_description", ""),
                        "status": violation.get("case_status", ""),
                        "created_date": violation.get("date_violation_created", ""),
                        "neighborhood": violation.get("neighborhood", ""),
                        "zip_code": violation.get("zip_code", ""),
                        "source": "Houston Code Enforcement"
                    })
                
                logger.info(f"✅ Fetched {len(structured_violations)} code violations")
                return structured_violations
            else:
                logger.error(f"❌ Error fetching violations: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return []
    
    def get_hcad_search_url(self, address: str) -> str:
        """
        Generate HCAD search URL for property data
        HCAD doesn't have a free API, but we can generate search URLs
        """
        # Clean address for URL
        clean_address = address.replace(" ", "+")
        search_url = f"https://public.hcad.org/records/QuickSearch.asp?SearchVal={clean_address}"
        
        return {
            "search_url": search_url,
            "note": "HCAD requires manual lookup or web scraping",
            "alternative": "Use Perplexity AI to search HCAD public records"
        }
    
    def get_houston_weather(self) -> Dict:
        """
        Get Houston weather data from NOAA
        Free, no API key required
        """
        # Houston coordinates
        lat, lon = 29.7604, -95.3698
        
        try:
            # Get grid endpoint
            point_url = f"{self.weather_base}/points/{lat},{lon}"
            response = requests.get(point_url)
            
            if response.status_code == 200:
                point_data = response.json()
                forecast_url = point_data['properties']['forecast']
                
                # Get forecast
                forecast_response = requests.get(forecast_url)
                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()
                    
                    return {
                        "current_forecast": forecast_data['properties']['periods'][0],
                        "weekly_forecast": forecast_data['properties']['periods'][:7],
                        "source": "NOAA Weather Service",
                        "timestamp": datetime.now().isoformat()
                    }
            
            return {"error": "Unable to fetch weather data"}
            
        except Exception as e:
            logger.error(f"❌ Weather API error: {str(e)}")
            return {"error": str(e)}
    
    def get_census_data(self, census_tract: str = "*", api_key: Optional[str] = None) -> Dict:
        """
        Get demographic data from US Census
        Requires free API key from: https://api.census.gov/data/key_signup.html
        """
        if not api_key:
            # Try to get from environment
            api_key = os.getenv('CENSUS_API_KEY')
            
        if not api_key:
            return {
                "error": "Census API key required",
                "get_key_url": "https://api.census.gov/data/key_signup.html",
                "note": "Free registration required"
            }
        
        # Get key demographics for Houston (Harris County = 201)
        endpoint = f"{self.census_base}/2022/acs/acs5"
        
        params = {
            "get": "NAME,B01003_001E,B19013_001E,B25077_001E",  # Name, Population, Income, Home Value
            "for": f"tract:{census_tract}",
            "in": "state:48 county:201",  # Texas, Harris County
            "key": api_key
        }
        
        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                data = response.json()
                
                # Process census data
                if len(data) > 1:  # First row is headers
                    results = []
                    headers = data[0]
                    
                    for row in data[1:]:
                        tract_data = dict(zip(headers, row))
                        results.append({
                            "tract": tract_data.get("tract", ""),
                            "name": tract_data.get("NAME", ""),
                            "population": int(tract_data.get("B01003_001E", 0)),
                            "median_income": int(tract_data.get("B19013_001E", 0)),
                            "median_home_value": int(tract_data.get("B25077_001E", 0)),
                            "source": "US Census Bureau"
                        })
                    
                    logger.info(f"✅ Fetched census data for {len(results)} tracts")
                    return {"tracts": results}
                
            return {"error": f"Census API error: {response.status_code}"}
            
        except Exception as e:
            logger.error(f"❌ Census API error: {str(e)}")
            return {"error": str(e)}
    
    def get_houston_gis_data(self) -> Dict:
        """
        Get Houston GIS data endpoints
        Free geospatial data for mapping
        """
        return {
            "gis_portal": "https://cohgis-mycity.opendata.arcgis.com/",
            "datasets": {
                "city_limits": "https://cohgis-mycity.opendata.arcgis.com/datasets/houston-city-limit",
                "super_neighborhoods": "https://cohgis-mycity.opendata.arcgis.com/datasets/super-neighborhoods",
                "council_districts": "https://cohgis-mycity.opendata.arcgis.com/datasets/city-council-districts",
                "zip_codes": "https://cohgis-mycity.opendata.arcgis.com/datasets/zip-codes",
                "flood_plains": "https://cohgis-mycity.opendata.arcgis.com/datasets/floodplains"
            },
            "note": "Download as GeoJSON, Shapefile, or CSV"
        }
    
    def get_all_free_data_summary(self) -> Dict:
        """
        Get a summary of all available free data sources
        """
        permits = self.get_building_permits(days_back=7, limit=5)
        violations = self.get_code_violations(days_back=30, limit=5)
        weather = self.get_houston_weather()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "data_sources": {
                "building_permits": {
                    "recent_count": len(permits),
                    "sample": permits[0] if permits else None,
                    "api_status": "✅ Active" if permits else "❌ Error"
                },
                "code_violations": {
                    "recent_count": len(violations),
                    "sample": violations[0] if violations else None,
                    "api_status": "✅ Active" if violations else "❌ Error"
                },
                "weather": {
                    "current": weather.get("current_forecast", {}).get("detailedForecast", "N/A"),
                    "api_status": "✅ Active" if "error" not in weather else "❌ Error"
                },
                "census": {
                    "status": "Requires API key (free)",
                    "signup_url": "https://api.census.gov/data/key_signup.html"
                },
                "hcad": {
                    "status": "Web interface only",
                    "url": "https://public.hcad.org/"
                },
                "gis_data": self.get_houston_gis_data()
            }
        }
        
        return summary

# Integration with refresh agents
def integrate_with_daily_refresh():
    """
    Example of how to integrate with daily refresh agent
    """
    client = HoustonFreeDataClient()
    
    # Get fresh permit data
    permits = client.get_building_permits(days_back=1)
    
    # Get code violations (potential opportunities)
    violations = client.get_code_violations(days_back=7)
    
    return {
        "permits": permits,
        "violations": violations,
        "timestamp": datetime.now().isoformat()
    }

# Test the implementation
if __name__ == "__main__":
    print("🏙️ Houston Free Data Sources Test")
    print("="*50)
    
    client = HoustonFreeDataClient()
    
    # Test building permits
    print("\n📋 Testing Building Permits API...")
    permits = client.get_building_permits(days_back=7, limit=3)
    if permits:
        print(f"✅ Found {len(permits)} recent permits")
        for permit in permits:
            print(f"  - {permit['address']}: ${permit['value']:,.0f} ({permit['type']})")
    
    # Test code violations
    print("\n⚠️  Testing Code Violations API...")
    violations = client.get_code_violations(days_back=30, limit=3)
    if violations:
        print(f"✅ Found {len(violations)} recent violations")
        for violation in violations:
            print(f"  - {violation['address']}: {violation['violation_type']}")
    
    # Test weather
    print("\n🌤️  Testing Weather API...")
    weather = client.get_houston_weather()
    if "current_forecast" in weather:
        print(f"✅ Current forecast: {weather['current_forecast']['shortForecast']}")
    
    # Show all available sources
    print("\n📊 All Free Data Sources Summary:")
    summary = client.get_all_free_data_summary()
    print(json.dumps(summary, indent=2))