#!/usr/bin/env python3
"""
Integration Script - Apply Fix to Master Intelligence Agent
This script helps integrate the fixed version into your system
"""

import shutil
from pathlib import Path
import json
from datetime import datetime


def backup_original():
    """Create backup of original master_intelligence_agent.py"""
    original = Path("master_intelligence_agent.py")
    backup = Path(f"master_intelligence_agent_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
    
    if original.exists():
        shutil.copy2(original, backup)
        print(f"✅ Created backup: {backup}")
        return True
    else:
        print("❌ Original file not found")
        return False


def integrate_knowledge_loader():
    """Integrate the knowledge base loader into the existing file"""
    print("\n🔧 Integration Steps:")
    print("-" * 40)
    
    # Check if knowledge_base_loader.py exists
    if not Path("knowledge_base_loader.py").exists():
        print("❌ knowledge_base_loader.py not found!")
        return False
    
    # Check if fixed version exists
    if not Path("master_intelligence_agent_fixed.py").exists():
        print("❌ master_intelligence_agent_fixed.py not found!")
        return False
    
    print("\n📋 To integrate the fix into your system:")
    print("\n1. First, backup your original file:")
    print("   python integrate_fix.py --backup")
    
    print("\n2. Replace the original with the fixed version:")
    print("   cp master_intelligence_agent_fixed.py master_intelligence_agent.py")
    
    print("\n3. Ensure knowledge_base_loader.py is in the same directory")
    
    print("\n4. Install required dependencies:")
    print("   pip install scikit-learn numpy")
    
    print("\n5. Test the integration:")
    print("   python test_fixed_master_agent.py")
    
    print("\n📌 Or use the fixed version directly:")
    print("   from master_intelligence_agent_fixed import MasterIntelligenceAgent")
    
    return True


def verify_knowledge_bases():
    """Verify that knowledge bases are available"""
    print("\n🔍 Verifying Knowledge Bases...")
    print("-" * 40)
    
    kb_path = Path("Agent_Knowledge_Bases")
    if not kb_path.exists():
        print(f"❌ Knowledge base directory not found: {kb_path}")
        return False
    
    expected_agents = {
        "Market_Intelligence": ["market_analysis_knowledge.json"],
        "Neighborhood_Intelligence": ["investment_analysis_knowledge.json"],
        "Financial_Intelligence": ["investment_analysis_knowledge.json"],
        "Environmental_Intelligence": ["risk_assessment_knowledge.json"],
        "Regulatory_Intelligence": ["permit_process_knowledge.json"],
        "Technology_Innovation_Intelligence": ["tech_investment_knowledge.json"]
    }
    
    all_good = True
    for agent_dir, expected_files in expected_agents.items():
        agent_path = kb_path / agent_dir
        if agent_path.exists():
            json_files = list(agent_path.glob("*.json"))
            print(f"✅ {agent_dir}: {len(json_files)} knowledge files")
        else:
            print(f"❌ {agent_dir}: Directory not found")
            all_good = False
    
    return all_good


def create_example_usage():
    """Create an example usage script"""
    example_code = '''#!/usr/bin/env python3
"""
Example Usage of Fixed Master Intelligence Agent
"""

from master_intelligence_agent_fixed import MasterIntelligenceAgent

def main():
    # Initialize the fixed agent
    print("Initializing Houston Intelligence Platform...")
    agent = MasterIntelligenceAgent()
    
    # Example queries
    queries = [
        "What are the best neighborhoods for investment in Houston?",
        "Tell me about Houston Heights development opportunities",
        "What are the risks of developing in flood zones?",
        "Show me Sugar Land market analysis"
    ]
    
    print("\\n" + "="*60)
    print("Houston Intelligence Platform - Example Usage")
    print("="*60)
    
    for query in queries:
        print(f"\\n🔍 Query: {query}")
        print("-" * 40)
        
        # Get analysis
        result = agent.analyze_query(query)
        
        # Display key information
        print(f"\\n📊 Executive Summary:")
        print(result['executive_summary'])
        
        print(f"\\n💡 Top 3 Insights:")
        for i, insight in enumerate(result['key_insights'][:3], 1):
            print(f"{i}. {insight}")
        
        print(f"\\n📈 Key Data Points:")
        for data in result['data_highlights'][:3]:
            print(f"- {data['metric']}: {data['value']}")
        
        print(f"\\n✅ Confidence: {result['confidence']*100:.1f}%")
        print(f"📚 Sources: {len(result['sources'])} intelligence agents consulted")
        
        input("\\nPress Enter for next query...")


if __name__ == "__main__":
    main()
'''
    
    with open("example_usage_fixed.py", "w") as f:
        f.write(example_code)
    
    print("\n✅ Created example_usage_fixed.py")


def main():
    """Main integration helper"""
    print("🚀 Houston Intelligence Platform - Fix Integration Helper")
    print("=" * 60)
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--backup":
        backup_original()
        return
    
    # Verify environment
    print("\n1️⃣ Checking environment...")
    kb_ok = verify_knowledge_bases()
    
    if not kb_ok:
        print("\n⚠️  Some knowledge bases are missing!")
        print("   The system will still work but with reduced data.")
    
    # Show integration steps
    integrate_knowledge_loader()
    
    # Create example
    create_example_usage()
    
    print("\n✨ Integration helper complete!")
    print("\n📝 Summary of created files:")
    print("  - knowledge_base_loader.py: Core knowledge base search functionality")
    print("  - master_intelligence_agent_fixed.py: Fixed version using real data")
    print("  - test_fixed_master_agent.py: Comprehensive test suite")
    print("  - example_usage_fixed.py: Example usage script")
    print("  - IMPLEMENTATION_PLAN_HOUSTON_INTELLIGENCE_FIX.md: Detailed documentation")
    
    print("\n🎯 Next Steps:")
    print("  1. Run tests: python test_fixed_master_agent.py")
    print("  2. Try example: python example_usage_fixed.py")
    print("  3. Integrate into your system using the steps above")


if __name__ == "__main__":
    main()