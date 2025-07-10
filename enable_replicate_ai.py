#!/usr/bin/env python3
"""
Enable Replicate AI Integration
Updates the API to use Replicate-enhanced intelligence
"""

import shutil
from pathlib import Path

def enable_replicate():
    """Enable Replicate AI in the Houston Intelligence API"""
    
    # Read the current API file
    api_file = Path("houston_intelligence_api.py")
    content = api_file.read_text()
    
    # Replace the import and initialization
    new_content = content.replace(
        "from master_intelligence_agent import MasterIntelligenceAgent",
        """from master_intelligence_agent import MasterIntelligenceAgent
try:
    from master_intelligence_agent_replicate import ReplicateEnhancedMasterAgent
    REPLICATE_AVAILABLE = True
except ImportError:
    REPLICATE_AVAILABLE = False"""
    )
    
    new_content = new_content.replace(
        """# Initialize Master Intelligence Agent
intelligence_agent = MasterIntelligenceAgent()
logger.info("Using Master Intelligence Agent")""",
        """# Initialize Master Intelligence Agent
USE_REPLICATE = os.getenv('USE_REPLICATE', 'true').lower() == 'true'
if USE_REPLICATE and REPLICATE_AVAILABLE:
    try:
        intelligence_agent = ReplicateEnhancedMasterAgent()
        logger.info("🚀 Using Replicate-Enhanced Master Intelligence Agent")
    except Exception as e:
        logger.warning(f"Failed to initialize Replicate: {e}. Using standard agent.")
        intelligence_agent = MasterIntelligenceAgent()
else:
    intelligence_agent = MasterIntelligenceAgent()
    logger.info("Using Master Intelligence Agent")"""
    )
    
    # Write the updated content
    api_file.write_text(new_content)
    
    print("✅ Replicate AI integration enabled!")
    print("\nFeatures added:")
    print("- Llama 2 70B for sophisticated market analysis")
    print("- BLIP-2 for property image analysis")
    print("- Stable Diffusion for development visualizations")
    print("- Mistral 7B for quick investment analysis")
    print("\nCost: ~$0.001-0.002 per request")
    print("\nSet REPLICATE_API_TOKEN environment variable in Railway")

if __name__ == "__main__":
    enable_replicate()