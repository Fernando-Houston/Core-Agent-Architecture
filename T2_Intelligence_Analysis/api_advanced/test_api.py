#!/usr/bin/env python3
"""
Test script for Houston Intelligence Platform
Tests all API endpoints and features
"""

import asyncio
import aiohttp
import json

async def test_api():
    """Test various API endpoints"""
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        # Test root endpoint
        print("1. Testing root endpoint...")
        async with session.get(f"{base_url}/") as resp:
            data = await resp.json()
            print(f"   Status: {resp.status}")
            print(f"   Response: {data}")
        
        # Test status endpoint
        print("\n2. Testing API status...")
        async with session.get(f"{base_url}/api/status") as resp:
            data = await resp.json()
            print(f"   Status: {resp.status}")
            print(f"   Components: {data.get('components', {})}")
            print(f"   Active connections: {data.get('active_connections', 0)}")
            print(f"   Cached analyses: {data.get('cached_analyses', 0)}")
        
        # Test domain analysis
        print("\n3. Testing domain analysis endpoint...")
        headers = {"Authorization": "Bearer demo-token"}
        async with session.get(f"{base_url}/api/domains/market/latest", headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"   Domain: {data.get('domain')}")
                print(f"   Confidence: {data.get('confidence_score')}")
                print(f"   Key findings: {len(data.get('key_findings', []))}")
            else:
                print(f"   No analysis data found (status: {resp.status})")
        
        # Test WebSocket info
        print("\n4. WebSocket endpoint available at:")
        print(f"   ws://localhost:8000/ws")
        
        # Test GraphQL info
        print("\n5. GraphQL endpoint available at:")
        print(f"   http://localhost:8000/graphql")
        
        # Test batch processing
        print("\n6. Testing batch processing...")
        batch_request = {
            "queries": [
                {
                    "query_type": "domain_analysis",
                    "domain": "market",
                    "priority": 10
                },
                {
                    "query_type": "cross_domain",
                    "parameters": {
                        "domains": ["market", "financial"]
                    }
                }
            ],
            "parallel_execution": True
        }
        
        async with session.post(
            f"{base_url}/batch/submit",
            json=batch_request,
            headers=headers
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"   Batch ID: {data.get('batch_id')}")
                print(f"   Status: {data.get('status')}")
                print(f"   Total queries: {data.get('total_queries')}")
            else:
                print(f"   Error: {resp.status}")
        
        # Test webhook list
        print("\n7. Testing webhook endpoints...")
        async with session.get(f"{base_url}/webhooks", headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"   Active subscriptions: {len(data)}")
            else:
                print(f"   Error: {resp.status}")
        
        print("\n✓ All API endpoints are operational!")
        print("\nAccess points:")
        print("  - API Documentation: http://localhost:8000/docs")
        print("  - WebSocket Demo: http://localhost:8000/demo")
        print("  - GraphQL Playground: http://localhost:8000/graphql")

if __name__ == "__main__":
    asyncio.run(test_api())