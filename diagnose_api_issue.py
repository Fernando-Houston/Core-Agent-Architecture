#!/usr/bin/env python3
"""Diagnostic script to identify the API issue"""

import json
from pathlib import Path
from master_intelligence_agent import MasterIntelligenceAgent
from knowledge_base_loader import KnowledgeBaseLoader

print("=== DIAGNOSTIC REPORT ===\n")

# 1. Check local file structure
print("1. LOCAL FILE STRUCTURE CHECK:")
print("-" * 50)

# Check Agent_Knowledge_Bases
kb_path = Path("Agent_Knowledge_Bases")
if kb_path.exists():
    print(f"✓ Agent_Knowledge_Bases exists")
    for agent_folder in kb_path.iterdir():
        if agent_folder.is_dir():
            json_files = list(agent_folder.glob("*.json"))
            print(f"  - {agent_folder.name}: {len(json_files)} JSON files")
else:
    print("✗ Agent_Knowledge_Bases NOT FOUND")

# Check 6 Specialized Agents
agents_path = Path("6 Specialized Agents")
if agents_path.exists():
    print(f"\n✓ 6 Specialized Agents exists")
    for agent_folder in agents_path.iterdir():
        if agent_folder.is_dir():
            knowledge_files = list(agent_folder.glob("knowledge_*.json"))
            print(f"  - {agent_folder.name}: {len(knowledge_files)} knowledge_*.json files")
else:
    print("\n✗ 6 Specialized Agents NOT FOUND")

# 2. Test Master Intelligence Agent
print("\n\n2. MASTER INTELLIGENCE AGENT CHECK:")
print("-" * 50)

try:
    master = MasterIntelligenceAgent()
    print(f"✓ Master agent initialized")
    print(f"  Agent registry paths:")
    for agent_id, path in master.agent_registry.items():
        exists = "✓" if path.exists() else "✗"
        print(f"  {exists} {agent_id}: {path}")
except Exception as e:
    print(f"✗ Error initializing master agent: {e}")

# 3. Test Knowledge Base Loader
print("\n\n3. KNOWLEDGE BASE LOADER CHECK:")
print("-" * 50)

try:
    kb_loader = KnowledgeBaseLoader()
    print(f"✓ Knowledge base loader initialized")
    print(f"  Base path: {kb_loader.base_path}")
    print(f"  Base path exists: {kb_loader.base_path.exists()}")
    
    # Test loading for one agent
    test_agent = "market_intelligence"
    records = kb_loader.load_agent_knowledge(test_agent)
    print(f"  Test load '{test_agent}': {len(records)} records")
except Exception as e:
    print(f"✗ Error with knowledge base loader: {e}")

# 4. Test API endpoints
print("\n\n4. API ENDPOINT TESTS:")
print("-" * 50)
print("(Skipping API tests - use curl commands separately)")

# 5. DIAGNOSIS
print("\n\n5. DIAGNOSIS:")
print("-" * 50)

print("""
The issue appears to be a PATH MISMATCH:

1. The knowledge base files are stored in: Agent_Knowledge_Bases/
2. The API is looking for files in: 6 Specialized Agents/*/knowledge_*.json
3. The knowledge loader uses: Agent_Knowledge_Bases/ (correct)
4. The API stats counter uses: agent_registry paths (incorrect)

This means:
- The knowledge loader CAN find the files (that's why queries work partially)
- But the API stats report 0 files (because it's looking in wrong place)
- The "Limited data" response suggests the query processing might have issues

RECOMMENDATIONS:
1. Either move knowledge files to match the expected structure
2. Or update the API to look in the correct location
3. Ensure the deployed Railway app includes the Agent_Knowledge_Bases directory
""")