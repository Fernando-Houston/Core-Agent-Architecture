#!/usr/bin/env python3
"""
Test script for Houston Intelligence Platform API
Tests the specialized endpoints with sample queries
"""

import requests
import json
from datetime import datetime

# Base URL for API
BASE_URL = "http://localhost:5000"

def test_endpoint(name, method, endpoint, data=None):
    """Test an API endpoint and display results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Endpoint: {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('status')}")
            
            # Show sample of results
            if 'total' in result:
                print(f"Total Results: {result['total']}")
            
            # Pretty print first item if it's a list
            for key in ['developments', 'permits', 'opportunities', 'developers']:
                if key in result and result[key]:
                    print(f"\nFirst {key[:-1]}:")
                    print(json.dumps(result[key][0], indent=2))
                    break
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Run all API tests"""
    print("Houston Intelligence Platform - API Test Suite")
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test health check first
    test_endpoint(
        "Health Check",
        "GET",
        "/health"
    )
    
    # Test specialized endpoints
    test_endpoint(
        "Active Developments",
        "GET",
        "/api/v1/developments/active"
    )
    
    test_endpoint(
        "Houston Heights Analysis",
        "GET",
        "/api/v1/neighborhoods/Houston Heights"
    )
    
    test_endpoint(
        "Recent Residential Permits",
        "GET",
        "/api/v1/permits/recent?type=residential&limit=5"
    )
    
    test_endpoint(
        "Market Trends",
        "GET",
        "/api/v1/market/trends"
    )
    
    test_endpoint(
        "Investment Opportunities",
        "POST",
        "/api/v1/opportunities/investment",
        {
            "budget_min": 1000000,
            "budget_max": 5000000,
            "property_types": ["mixed-use", "residential"],
            "min_roi": 15
        }
    )
    
    test_endpoint(
        "Risk Assessment - Sugar Land",
        "POST",
        "/api/v1/risks/assessment",
        {
            "location": "Sugar Land",
            "project_type": "residential"
        }
    )
    
    test_endpoint(
        "Top 5 Developers",
        "GET",
        "/api/v1/developers/top?limit=5"
    )
    
    test_endpoint(
        "Technology Innovations",
        "GET",
        "/api/v1/technology/innovations"
    )
    
    # Test main query endpoint
    test_endpoint(
        "Natural Language Query",
        "POST",
        "/api/v1/query",
        {
            "query": "What are the best investment opportunities in Houston?"
        }
    )
    
    print(f"\n{'='*60}")
    print("API Test Suite Complete")

if __name__ == "__main__":
    main()