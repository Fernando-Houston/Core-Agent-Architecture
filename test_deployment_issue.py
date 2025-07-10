#!/usr/bin/env python3
"""Test script to run the query locally and compare with API"""

from master_intelligence_agent import MasterIntelligenceAgent
import json

# Initialize the agent
print("Initializing Master Intelligence Agent...")
agent = MasterIntelligenceAgent()

# Test query
test_query = "What are the latest building permits in Houston?"
print(f"\nTesting query: '{test_query}'")

# Run the analysis
try:
    result = agent.analyze_query(test_query)
    print("\n=== LOCAL RESULT ===")
    print(f"Executive Summary: {result.get('executive_summary', 'No summary')[:200]}...")
    print(f"Key Insights: {len(result.get('key_insights', []))}")
    print(f"Data Quality - Total Insights: {result.get('data_quality', {}).get('total_insights', 0)}")
    print(f"Sources: {result.get('sources', [])}")
    
    # Check if we got real data or limited data response
    if "Limited data available" in result.get('executive_summary', ''):
        print("\n⚠️  LOCAL TEST ALSO RETURNS 'Limited data available'")
        print("This suggests the issue is in the code logic, not deployment")
    else:
        print("\n✓ LOCAL TEST RETURNS REAL DATA")
        print("This suggests the issue is with deployment (missing files)")
        
except Exception as e:
    print(f"\nError running local test: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("DIAGNOSIS:")
print("If local test returns real data but API doesn't, check:")
print("1. Agent_Knowledge_Bases folder is included in deployment")
print("2. File paths are correct for Railway environment")
print("3. No permission issues on Railway")
print("\nIf both return 'Limited data', check:")
print("1. Knowledge base loader logic")
print("2. Query processing in master agent")
print("3. Data format in knowledge base files")