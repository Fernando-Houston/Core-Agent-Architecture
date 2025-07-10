#!/usr/bin/env python3
"""Simple diagnostic without external dependencies"""

from pathlib import Path

print("=== SIMPLE DIAGNOSTIC REPORT ===\n")

# 1. Check Agent_Knowledge_Bases
print("1. KNOWLEDGE BASE STRUCTURE:")
print("-" * 50)

kb_path = Path("Agent_Knowledge_Bases")
if kb_path.exists():
    print(f"✓ Agent_Knowledge_Bases exists at: {kb_path.absolute()}")
    total_kb_files = 0
    for agent_folder in kb_path.iterdir():
        if agent_folder.is_dir():
            json_files = list(agent_folder.glob("*.json"))
            total_kb_files += len(json_files)
            print(f"  - {agent_folder.name}: {len(json_files)} JSON files")
    print(f"\nTotal knowledge base files: {total_kb_files}")
else:
    print("✗ Agent_Knowledge_Bases NOT FOUND")

# 2. Check 6 Specialized Agents
print("\n2. AGENT FOLDER STRUCTURE:")
print("-" * 50)

agents_path = Path("6 Specialized Agents")
if agents_path.exists():
    print(f"✓ 6 Specialized Agents exists at: {agents_path.absolute()}")
    total_knowledge_files = 0
    for agent_folder in agents_path.iterdir():
        if agent_folder.is_dir():
            knowledge_files = list(agent_folder.glob("knowledge_*.json"))
            total_knowledge_files += len(knowledge_files)
            latest_insights = agent_folder / "latest_insights.json"
            capabilities = agent_folder / "capabilities.json"
            print(f"  - {agent_folder.name}:")
            print(f"    knowledge_*.json files: {len(knowledge_files)}")
            print(f"    latest_insights.json: {'✓' if latest_insights.exists() else '✗'}")
            print(f"    capabilities.json: {'✓' if capabilities.exists() else '✗'}")
    print(f"\nTotal knowledge_*.json files in agent folders: {total_knowledge_files}")
else:
    print("✗ 6 Specialized Agents NOT FOUND")

# 3. Check key files
print("\n3. KEY FILE CHECKS:")
print("-" * 50)

key_files = [
    "master_intelligence_agent.py",
    "knowledge_base_loader.py", 
    "houston_intelligence_api.py",
    "perplexity_integration.py",
    "houston_data_enhanced.py"
]

for file_name in key_files:
    file_path = Path(file_name)
    if file_path.exists():
        print(f"✓ {file_name}")
    else:
        print(f"✗ {file_name} NOT FOUND")

# 4. Analysis
print("\n4. ANALYSIS:")
print("-" * 50)
print("""
KEY FINDINGS:

1. Knowledge base files are stored in: Agent_Knowledge_Bases/
   - This is where the actual data is stored
   - The knowledge_base_loader.py looks here (CORRECT)

2. The API is looking for files in: 6 Specialized Agents/*/knowledge_*.json
   - This location has 0 knowledge_*.json files
   - That's why the API reports 0 knowledge files

3. The issue is a PATH MISMATCH between:
   - Where data is stored (Agent_Knowledge_Bases/)
   - Where the API looks for stats (6 Specialized Agents/)

SOLUTION OPTIONS:

Option 1: Update the API stats counter
- Modify houston_intelligence_api.py line 330
- Change from: knowledge_files = list(agent_path.glob('knowledge_*.json'))
- To look in Agent_Knowledge_Bases instead

Option 2: Ensure Railway deployment includes Agent_Knowledge_Bases
- The knowledge files might not be deployed to Railway
- Check if Agent_Knowledge_Bases is being uploaded
- May need to adjust deployment configuration
""")