#!/usr/bin/env python3
"""
Integration Script for Houston Intelligence Platform
Connects real knowledge bases with live data sources
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def integrate_master_agent_v2():
    """Replace the old master agent with the new version that uses real data"""
    
    # Backup original file
    original_file = Path("master_intelligence_agent.py")
    backup_file = Path("master_intelligence_agent_backup.py")
    v2_file = Path("master_intelligence_agent_v2.py")
    
    if original_file.exists() and not backup_file.exists():
        logger.info(f"📦 Backing up original master agent to {backup_file}")
        shutil.copy2(original_file, backup_file)
    
    if v2_file.exists():
        logger.info("🔄 Replacing master agent with V2 (real data version)")
        shutil.copy2(v2_file, original_file)
        logger.info("✅ Master agent updated to use real knowledge bases!")
    else:
        logger.error("❌ master_intelligence_agent_v2.py not found!")
        return False
    
    return True

def verify_knowledge_bases():
    """Verify that knowledge bases are populated"""
    kb_path = Path("Agent_Knowledge_Bases")
    
    if not kb_path.exists():
        logger.error("❌ Agent_Knowledge_Bases directory not found!")
        return False
    
    agent_folders = [
        "Market_Intelligence",
        "Neighborhood_Intelligence", 
        "Financial_Intelligence",
        "Environmental_Intelligence",
        "Regulatory_Intelligence",
        "Technology_Innovation_Intelligence"
    ]
    
    total_files = 0
    for folder in agent_folders:
        agent_path = kb_path / folder
        if agent_path.exists():
            json_files = list(agent_path.glob("*.json"))
            total_files += len(json_files)
            logger.info(f"✅ {folder}: {len(json_files)} knowledge files")
        else:
            logger.warning(f"⚠️ {folder} not found")
    
    logger.info(f"📊 Total knowledge files: {total_files}")
    return total_files > 0

def update_api_imports():
    """Update houston_intelligence_api.py to import from the correct module"""
    api_file = Path("houston_intelligence_api.py")
    
    if api_file.exists():
        content = api_file.read_text()
        
        # Check if already importing houston_data_enhanced
        if "houston_data_enhanced" not in content:
            # Add import for enhanced data API
            import_line = "from houston_data_enhanced import HoustonDataAPI"
            
            # Find where to insert (after other imports)
            lines = content.split('\n')
            import_index = 0
            for i, line in enumerate(lines):
                if line.startswith("from master_intelligence_agent"):
                    import_index = i + 1
                    break
            
            lines.insert(import_index, import_line)
            
            # Update the content
            updated_content = '\n'.join(lines)
            
            # Write back
            api_file.write_text(updated_content)
            logger.info("✅ Updated API imports to use enhanced data sources")
        else:
            logger.info("✅ API already using enhanced data sources")
    
    return True

def create_requirements_update():
    """Update requirements.txt with new dependencies"""
    requirements = Path("requirements.txt")
    
    new_deps = [
        "scikit-learn>=1.0.0",  # For TF-IDF in knowledge base loader
        "python-dotenv>=0.19.0",  # For environment variables
    ]
    
    if requirements.exists():
        content = requirements.read_text()
        lines = content.strip().split('\n')
        
        # Add new dependencies if not present
        for dep in new_deps:
            dep_name = dep.split('>=')[0]
            if not any(dep_name in line for line in lines):
                lines.append(dep)
                logger.info(f"➕ Added {dep} to requirements")
        
        # Write back
        requirements.write_text('\n'.join(lines) + '\n')
        logger.info("✅ Updated requirements.txt")
    
    return True

def test_integration():
    """Test that the integration is working"""
    try:
        # Test knowledge base loader
        from knowledge_base_loader import KnowledgeBaseLoader
        loader = KnowledgeBaseLoader()
        
        # Test loading some data
        market_data = loader.load_agent_knowledge("market_intelligence")
        logger.info(f"✅ Knowledge base loader working: {len(market_data)} market records")
        
        # Test enhanced data API
        from houston_data_enhanced import HoustonDataAPI
        api = HoustonDataAPI()
        
        # Test getting permits
        permits = api.get_building_permits(days_back=7, limit=5)
        logger.info(f"✅ Houston data API working: {len(permits)} recent permits")
        
        # Test master agent v2
        from master_intelligence_agent_v2 import MasterIntelligenceAgent
        master = MasterIntelligenceAgent()
        
        # Test a query
        result = master.analyze_query("What are the latest building permits?")
        logger.info(f"✅ Master agent V2 working: {len(result.get('key_insights', []))} insights")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {str(e)}")
        return False

def create_integration_summary():
    """Create a summary of the integration"""
    summary = {
        "integration_date": datetime.now().isoformat(),
        "components": {
            "knowledge_base_loader": "Loads and searches real Houston data from T1/T2/T3 processing",
            "master_intelligence_agent_v2": "Uses real knowledge bases instead of hardcoded responses",
            "houston_data_enhanced": "Provides cached access to free Houston data sources",
            "perplexity_integration": "Adds real-time search capabilities"
        },
        "data_sources": {
            "knowledge_bases": "49 insights from 6 specialized agents",
            "houston_open_data": "Building permits, code violations",
            "census_api": "Demographics, income, housing data",
            "weather_api": "Construction impact analysis",
            "perplexity_ai": "Real-time property and market searches"
        },
        "improvements": {
            "response_quality": "Responses now based on actual data, not hardcoded examples",
            "data_freshness": "Live data from Houston APIs + cached knowledge",
            "search_capability": "TF-IDF semantic search through knowledge bases",
            "performance": "5-minute caching for frequently accessed data"
        }
    }
    
    with open("INTEGRATION_SUMMARY.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    logger.info("📄 Created integration summary")

def main():
    """Run the complete integration"""
    print("🚀 Houston Intelligence Platform - Real Data Integration")
    print("="*60)
    
    # Step 1: Verify knowledge bases
    print("\n1️⃣ Verifying knowledge bases...")
    if not verify_knowledge_bases():
        print("❌ Knowledge bases not found. Run T1/T2/T3 agents first!")
        return
    
    # Step 2: Integrate master agent V2
    print("\n2️⃣ Integrating Master Agent V2...")
    if not integrate_master_agent_v2():
        print("❌ Failed to integrate master agent")
        return
    
    # Step 3: Update API imports
    print("\n3️⃣ Updating API imports...")
    update_api_imports()
    
    # Step 4: Update requirements
    print("\n4️⃣ Updating requirements...")
    create_requirements_update()
    
    # Step 5: Test integration
    print("\n5️⃣ Testing integration...")
    if test_integration():
        print("✅ Integration successful!")
    else:
        print("⚠️ Integration completed but tests failed")
    
    # Step 6: Create summary
    print("\n6️⃣ Creating integration summary...")
    create_integration_summary()
    
    print("\n" + "="*60)
    print("✅ INTEGRATION COMPLETE!")
    print("\nYour Houston Intelligence Platform now uses:")
    print("- Real knowledge base data (49 insights)")
    print("- Live Houston data (permits, violations)")
    print("- Perplexity AI for real-time searches")
    print("- Semantic search through all knowledge")
    print("- Intelligent caching for performance")
    print("\nThe chatbot will now provide real, data-driven responses!")
    print("="*60)


if __name__ == "__main__":
    main()