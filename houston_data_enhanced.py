#!/usr/bin/env python3
"""
Enhanced Houston Data API with Caching and Real-time Updates
Integrates all free Houston data sources with intelligent caching
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from functools import lru_cache
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HoustonDataAPI:
    """Enhanced Houston Data API with caching and better integration"""
    
    def __init__(self):
        self.houston_data_base = "https://data.houstontx.gov/resource"
        self.census_api_key = os.getenv("CENSUS_API_KEY", "cda0d6f4c3bb30fe797126c5b51157e9776eafe6")
        self.weather_api_key = os.getenv("WEATHER_API_KEY", "demo")
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = {
            'permits': 3600,  # 1 hour
            'violations': 3600,  # 1 hour
            'weather': 1800,  # 30 minutes
            'census': 86400,  # 24 hours
            'demographics': 86400  # 24 hours
        }
    
    def _get_cache_key(self, method: str, params: Dict) -> str:
        """Generate cache key from method and parameters"""
        param_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(f"{method}:{param_str}".encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[cache_key]
    
    def _set_cache(self, cache_key: str, data: Any, duration: int):
        """Set cache with expiration"""
        self.cache[cache_key] = data
        self.cache_expiry[cache_key] = datetime.now() + timedelta(seconds=duration)
    
    def get_building_permits(self, days_back: int = 7, limit: int = 100, 
                           neighborhood: Optional[str] = None) -> List[Dict]:
        """
        Fetch recent building permits with optional neighborhood filter
        """
        cache_key = self._get_cache_key('permits', {'days_back': days_back, 'limit': limit, 'neighborhood': neighborhood})
        
        if self._is_cache_valid(cache_key):
            logger.info("📦 Returning cached permit data")
            return self.cache[cache_key]
        
        endpoint = f"{self.houston_data_base}/3tts-58vt.json"
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        params = {
            "$limit": limit,
            "$order": "permit_issue_date DESC",
            "$where": f"permit_issue_date > '{start_date}'"
        }
        
        # Add neighborhood filter if specified
        if neighborhood:
            params["$where"] += f" AND neighborhood like '%{neighborhood}%'"
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            if response.status_code == 200:
                permits = response.json()
                
                structured_permits = []
                for permit in permits:
                    # Calculate permit value category
                    value = float(permit.get("estimated_cost", 0))
                    value_category = "Small" if value < 100000 else "Medium" if value < 1000000 else "Large"
                    
                    structured_permits.append({
                        "permit_number": permit.get("permit_number", ""),
                        "address": f"{permit.get('street_number', '')} {permit.get('street_name', '')} {permit.get('street_suffix', '')}".strip(),
                        "neighborhood": permit.get("neighborhood", "Unknown"),
                        "type": permit.get("permit_type", ""),
                        "subtype": permit.get("work_description", ""),
                        "value": value,
                        "value_category": value_category,
                        "issued_date": permit.get("permit_issue_date", ""),
                        "status": permit.get("status", ""),
                        "applicant": permit.get("applicant_name", ""),
                        "contractor": permit.get("contractor_name", ""),
                        "description": permit.get("project_description", ""),
                        "source": "Houston Open Data Portal",
                        "data_freshness": datetime.now().isoformat()
                    })
                
                # Cache the results
                self._set_cache(cache_key, structured_permits, self.cache_duration['permits'])
                
                logger.info(f"✅ Fetched {len(structured_permits)} permits from Houston Open Data")
                return structured_permits
            else:
                logger.error(f"❌ Error fetching permits: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return []
    
    def get_code_violations(self, days_back: int = 30, limit: int = 50,
                          violation_type: Optional[str] = None) -> List[Dict]:
        """
        Fetch code violations - useful for finding distressed properties
        """
        cache_key = self._get_cache_key('violations', {'days_back': days_back, 'limit': limit, 'type': violation_type})
        
        if self._is_cache_valid(cache_key):
            logger.info("📦 Returning cached violation data")
            return self.cache[cache_key]
        
        endpoint = f"{self.houston_data_base}/5kz8-qxbv.json"
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        params = {
            "$limit": limit,
            "$order": "date_violation_created DESC",
            "$where": f"date_violation_created > '{start_date}'"
        }
        
        if violation_type:
            params["$where"] += f" AND violation_category like '%{violation_type}%'"
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            if response.status_code == 200:
                violations = response.json()
                
                structured_violations = []
                for violation in violations:
                    # Determine severity based on violation type
                    severity = "High" if "structural" in violation.get("violation_category", "").lower() else "Medium"
                    
                    structured_violations.append({
                        "case_number": violation.get("case_number", ""),
                        "address": violation.get("full_address", ""),
                        "violation_type": violation.get("violation_category", ""),
                        "description": violation.get("violation_description", ""),
                        "status": violation.get("case_status", ""),
                        "severity": severity,
                        "created_date": violation.get("date_violation_created", ""),
                        "neighborhood": violation.get("neighborhood", ""),
                        "zip_code": violation.get("zip_code", ""),
                        "source": "Houston Code Enforcement",
                        "opportunity_type": "Distressed Property" if severity == "High" else "Value-Add"
                    })
                
                # Cache results
                self._set_cache(cache_key, structured_violations, self.cache_duration['violations'])
                
                logger.info(f"✅ Fetched {len(structured_violations)} code violations")
                return structured_violations
            else:
                logger.error(f"❌ Error fetching violations: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return []
    
    def get_neighborhood_demographics(self, neighborhood: str) -> Dict[str, Any]:
        """
        Get demographic data for a specific Houston neighborhood
        Uses Census data where available
        """
        cache_key = self._get_cache_key('demographics', {'neighborhood': neighborhood})
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Map neighborhoods to census tracts (simplified - in production would use proper mapping)
        neighborhood_tract_map = {
            "houston heights": "1001",
            "river oaks": "1002", 
            "montrose": "1003",
            "midtown": "1004",
            "east end": "1005",
            "katy": "1006",
            "sugar land": "1007",
            "the woodlands": "1008"
        }
        
        tract = neighborhood_tract_map.get(neighborhood.lower(), "*")
        
        # Get census data
        census_data = self.get_census_data(tract)
        
        # Get recent permits for the neighborhood
        permits = self.get_building_permits(days_back=90, limit=20, neighborhood=neighborhood)
        
        # Calculate neighborhood statistics
        result = {
            "neighborhood": neighborhood,
            "demographics": census_data,
            "development_activity": {
                "recent_permits": len(permits),
                "total_permit_value": sum(p['value'] for p in permits),
                "average_permit_value": sum(p['value'] for p in permits) / len(permits) if permits else 0,
                "permit_types": {}
            },
            "market_indicators": {
                "development_heat": "High" if len(permits) > 10 else "Medium" if len(permits) > 5 else "Low",
                "investment_potential": "Strong" if len(permits) > 15 else "Moderate"
            }
        }
        
        # Count permit types
        for permit in permits:
            ptype = permit['type']
            result['development_activity']['permit_types'][ptype] = result['development_activity']['permit_types'].get(ptype, 0) + 1
        
        # Cache result
        self._set_cache(cache_key, result, self.cache_duration['demographics'])
        
        return result
    
    def get_census_data(self, census_tract: str = "*") -> Dict:
        """
        Get demographic data from US Census with caching
        """
        cache_key = self._get_cache_key('census', {'tract': census_tract})
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        if not self.census_api_key:
            return {"error": "Census API key not configured"}
        
        # Census endpoint for American Community Survey
        endpoint = "https://api.census.gov/data/2022/acs/acs5"
        
        params = {
            "get": "NAME,B01003_001E,B19013_001E,B25077_001E,B25003_001E,B25003_002E",
            "for": f"tract:{census_tract}",
            "in": "state:48 county:201",  # Texas, Harris County
            "key": self.census_api_key
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if len(data) > 1:
                    headers = data[0]
                    results = []
                    
                    for row in data[1:]:
                        tract_data = dict(zip(headers, row))
                        
                        # Calculate homeownership rate
                        total_units = int(tract_data.get("B25003_001E", 1))
                        owner_units = int(tract_data.get("B25003_002E", 0))
                        ownership_rate = (owner_units / total_units * 100) if total_units > 0 else 0
                        
                        results.append({
                            "tract": tract_data.get("tract", ""),
                            "name": tract_data.get("NAME", ""),
                            "population": int(tract_data.get("B01003_001E", 0)),
                            "median_income": int(tract_data.get("B19013_001E", 0)),
                            "median_home_value": int(tract_data.get("B25077_001E", 0)),
                            "homeownership_rate": round(ownership_rate, 1),
                            "income_category": "High" if int(tract_data.get("B19013_001E", 0)) > 75000 else "Medium" if int(tract_data.get("B19013_001E", 0)) > 50000 else "Low",
                            "source": "US Census Bureau ACS 2022"
                        })
                    
                    result = {"tracts": results} if census_tract == "*" else results[0] if results else {}
                    
                    # Cache result
                    self._set_cache(cache_key, result, self.cache_duration['census'])
                    
                    return result
                
            return {"error": f"Census API error: {response.status_code}"}
            
        except Exception as e:
            logger.error(f"❌ Census API error: {str(e)}")
            return {"error": str(e)}
    
    def get_weather_impact_analysis(self) -> Dict:
        """
        Analyze weather impact on construction and development
        """
        cache_key = self._get_cache_key('weather', {})
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Houston coordinates
        lat, lon = 29.7604, -95.3698
        
        try:
            # Get weather from NOAA
            point_url = f"https://api.weather.gov/points/{lat},{lon}"
            response = requests.get(point_url, timeout=10)
            
            if response.status_code == 200:
                point_data = response.json()
                forecast_url = point_data['properties']['forecast']
                
                forecast_response = requests.get(forecast_url, timeout=10)
                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()
                    periods = forecast_data['properties']['periods']
                    
                    # Analyze construction impact
                    rain_days = sum(1 for p in periods[:7] if 'rain' in p['detailedForecast'].lower() or 'storm' in p['detailedForecast'].lower())
                    
                    result = {
                        "current_conditions": periods[0]['detailedForecast'],
                        "construction_impact": {
                            "rating": "High" if rain_days > 3 else "Medium" if rain_days > 1 else "Low",
                            "rain_days_forecast": rain_days,
                            "recommendation": "Schedule indoor work" if rain_days > 3 else "Normal operations"
                        },
                        "weekly_summary": {
                            "favorable_days": 7 - rain_days,
                            "weather_delays_expected": rain_days > 2
                        },
                        "source": "NOAA Weather Service",
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Cache result
                    self._set_cache(cache_key, result, self.cache_duration['weather'])
                    
                    return result
            
            return {"error": "Unable to fetch weather data"}
            
        except Exception as e:
            logger.error(f"❌ Weather API error: {str(e)}")
            return {"error": str(e)}
    
    def get_investment_opportunities(self, min_violations: int = 3) -> List[Dict]:
        """
        Find investment opportunities based on code violations and permit activity
        """
        # Get recent violations
        violations = self.get_code_violations(days_back=90, limit=100)
        
        # Group by address to find properties with multiple violations
        property_violations = {}
        for violation in violations:
            addr = violation['address']
            if addr not in property_violations:
                property_violations[addr] = []
            property_violations[addr].append(violation)
        
        # Find properties with multiple violations (distressed)
        opportunities = []
        for address, viols in property_violations.items():
            if len(viols) >= min_violations:
                opportunities.append({
                    "address": address,
                    "neighborhood": viols[0]['neighborhood'],
                    "violation_count": len(viols),
                    "violation_types": list(set(v['violation_type'] for v in viols)),
                    "opportunity_score": min(10, len(viols) * 2),  # Higher score = more distressed
                    "investment_type": "Fix & Flip" if len(viols) > 5 else "Value-Add Rental",
                    "risk_level": "High" if len(viols) > 7 else "Medium",
                    "violations": viols
                })
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return opportunities
    
    def get_developer_activity_summary(self, days_back: int = 90) -> Dict:
        """
        Analyze developer activity based on permits
        """
        permits = self.get_building_permits(days_back=days_back, limit=500)
        
        # Analyze by contractor/developer
        developer_stats = {}
        neighborhood_stats = {}
        permit_type_stats = {}
        
        total_value = 0
        
        for permit in permits:
            contractor = permit.get('contractor', 'Unknown')
            neighborhood = permit.get('neighborhood', 'Unknown')
            permit_type = permit.get('type', 'Unknown')
            value = permit.get('value', 0)
            
            # Developer stats
            if contractor not in developer_stats:
                developer_stats[contractor] = {
                    'permit_count': 0,
                    'total_value': 0,
                    'neighborhoods': set()
                }
            developer_stats[contractor]['permit_count'] += 1
            developer_stats[contractor]['total_value'] += value
            developer_stats[contractor]['neighborhoods'].add(neighborhood)
            
            # Neighborhood stats
            if neighborhood not in neighborhood_stats:
                neighborhood_stats[neighborhood] = {
                    'permit_count': 0,
                    'total_value': 0
                }
            neighborhood_stats[neighborhood]['permit_count'] += 1
            neighborhood_stats[neighborhood]['total_value'] += value
            
            # Permit type stats
            if permit_type not in permit_type_stats:
                permit_type_stats[permit_type] = {
                    'count': 0,
                    'total_value': 0
                }
            permit_type_stats[permit_type]['count'] += 1
            permit_type_stats[permit_type]['total_value'] += value
            
            total_value += value
        
        # Convert sets to lists for JSON serialization
        for dev in developer_stats.values():
            dev['neighborhoods'] = list(dev['neighborhoods'])
        
        # Find top developers
        top_developers = sorted(
            [(k, v) for k, v in developer_stats.items()],
            key=lambda x: x[1]['total_value'],
            reverse=True
        )[:10]
        
        # Find hottest neighborhoods
        hot_neighborhoods = sorted(
            [(k, v) for k, v in neighborhood_stats.items()],
            key=lambda x: x[1]['permit_count'],
            reverse=True
        )[:10]
        
        return {
            "summary": {
                "total_permits": len(permits),
                "total_value": total_value,
                "average_permit_value": total_value / len(permits) if permits else 0,
                "unique_developers": len(developer_stats),
                "unique_neighborhoods": len(neighborhood_stats)
            },
            "top_developers": [
                {
                    "name": dev[0],
                    "permits": dev[1]['permit_count'],
                    "total_value": dev[1]['total_value'],
                    "neighborhoods": dev[1]['neighborhoods']
                }
                for dev in top_developers
            ],
            "hot_neighborhoods": [
                {
                    "name": n[0],
                    "permits": n[1]['permit_count'],
                    "total_value": n[1]['total_value'],
                    "avg_permit_value": n[1]['total_value'] / n[1]['permit_count']
                }
                for n in hot_neighborhoods
            ],
            "permit_types": permit_type_stats,
            "analysis_period": f"Last {days_back} days",
            "data_freshness": datetime.now().isoformat()
        }


def test_enhanced_api():
    """Test the enhanced Houston Data API"""
    print("🏙️ Enhanced Houston Data API Test")
    print("="*60)
    
    api = HoustonDataAPI()
    
    # Test neighborhood demographics
    print("\n📊 Testing Neighborhood Demographics...")
    demo = api.get_neighborhood_demographics("Houston Heights")
    print(f"Heights Development Activity: {demo['development_activity']['recent_permits']} permits")
    print(f"Total Investment: ${demo['development_activity']['total_permit_value']:,.0f}")
    
    # Test investment opportunities
    print("\n💰 Testing Investment Opportunities...")
    opportunities = api.get_investment_opportunities(min_violations=2)
    print(f"Found {len(opportunities)} distressed properties")
    if opportunities:
        top = opportunities[0]
        print(f"Top opportunity: {top['address']} ({top['violation_count']} violations)")
    
    # Test developer activity
    print("\n🏗️ Testing Developer Activity...")
    dev_summary = api.get_developer_activity_summary(days_back=30)
    print(f"Total permits: {dev_summary['summary']['total_permits']}")
    print(f"Total value: ${dev_summary['summary']['total_value']:,.0f}")
    if dev_summary['top_developers']:
        top_dev = dev_summary['top_developers'][0]
        print(f"Top developer: {top_dev['name']} - ${top_dev['total_value']:,.0f}")
    
    # Test weather impact
    print("\n🌤️ Testing Weather Impact Analysis...")
    weather = api.get_weather_impact_analysis()
    print(f"Construction Impact: {weather['construction_impact']['rating']}")
    print(f"Rain days forecast: {weather['construction_impact']['rain_days_forecast']}")
    
    print("\n✅ Enhanced API Test Complete!")


if __name__ == "__main__":
    test_enhanced_api()