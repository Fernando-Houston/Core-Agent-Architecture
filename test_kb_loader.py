#!/usr/bin/env python3
"""Test the knowledge base loader to see if it's working"""

from knowledge_base_loader import KnowledgeBaseLoader
import json

# Initialize the loader
loader = KnowledgeBaseLoader()

# Test loading for each agent
agents = [
    "market_intelligence",
    "neighborhood_intelligence", 
    "financial_intelligence",
    "environmental_intelligence",
    "regulatory_intelligence",
    "technology_intelligence"
]

for agent in agents:
    print(f"\n=== Testing {agent} ===")
    try:
        records = loader.load_agent_knowledge(agent)
        print(f"Loaded {len(records)} records")
        if records:
            print(f"Sample record: {json.dumps(records[0], indent=2)[:200]}...")
    except Exception as e:
        print(f"Error loading {agent}: {str(e)}")

# Test searching
print("\n=== Testing search functionality ===")
try:
    results = loader.search_knowledge("market_intelligence", "Sugar Land pricing")
    print(f"Found {len(results)} results for 'Sugar Land pricing'")
    if results:
        print(f"Top result: {json.dumps(results[0], indent=2)[:200]}...")
except Exception as e:
    print(f"Error searching: {str(e)}")