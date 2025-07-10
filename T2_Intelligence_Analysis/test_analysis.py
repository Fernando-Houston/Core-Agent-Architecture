#!/usr/bin/env python3
"""
Test script to process available T1 extractions through T2 analysis
"""

import sys
import json
from pathlib import Path

# Add to Python path
sys.path.append(str(Path(__file__).parent))

from config.analysis_config import DOMAIN_CONFIG, SHARED_STATE_PATH, T2_OUTPUTS_PATH
from analysis_engines.neighborhood_intelligence.neighborhood_analyzer import NeighborhoodIntelligenceAnalyzer
from analysis_engines.financial_intelligence.financial_analyzer import FinancialIntelligenceAnalyzer


def test_neighborhood_analysis():
    """Test neighborhood intelligence analysis"""
    print("\n=== Testing Neighborhood Intelligence Analysis ===")
    
    analyzer = NeighborhoodIntelligenceAnalyzer(DOMAIN_CONFIG["neighborhood_intelligence"])
    input_file = f"{SHARED_STATE_PATH}/t1_extractions/neighborhood_intelligence_extracted.json"
    
    if Path(input_file).exists():
        result = analyzer.analyze(input_file)
        output_file = analyzer.save_results(result, T2_OUTPUTS_PATH)
        
        print(f"✓ Analysis completed with {result.confidence_score:.2%} confidence")
        print(f"✓ Key findings: {len(result.key_findings)}")
        print(f"✓ Top finding: {result.key_findings[0] if result.key_findings else 'None'}")
        print(f"✓ Results saved to: {output_file}")
        
        # Queue for T3
        queue_for_t3("neighborhood_intelligence", output_file, result)
    else:
        print(f"✗ Input file not found: {input_file}")


def test_financial_analysis():
    """Test financial intelligence analysis"""
    print("\n=== Testing Financial Intelligence Analysis ===")
    
    analyzer = FinancialIntelligenceAnalyzer(DOMAIN_CONFIG["financial_intelligence"])
    input_file = f"{SHARED_STATE_PATH}/t1_extractions/financial_intelligence_extracted.json"
    
    if Path(input_file).exists():
        result = analyzer.analyze(input_file)
        output_file = analyzer.save_results(result, T2_OUTPUTS_PATH)
        
        print(f"✓ Analysis completed with {result.confidence_score:.2%} confidence")
        print(f"✓ Key findings: {len(result.key_findings)}")
        print(f"✓ Top finding: {result.key_findings[0] if result.key_findings else 'None'}")
        print(f"✓ Results saved to: {output_file}")
        
        # Queue for T3
        queue_for_t3("financial_intelligence", output_file, result)
    else:
        print(f"✗ Input file not found: {input_file}")


def queue_for_t3(domain: str, output_file: str, result):
    """Queue results for T3"""
    from datetime import datetime
    
    t3_queue_file = Path(SHARED_STATE_PATH) / "t3_agent_queue" / f"{domain}_ready.json"
    t3_queue_file.parent.mkdir(exist_ok=True)
    
    queue_entry = {
        "domain": domain,
        "analysis_file": output_file,
        "timestamp": datetime.now().isoformat(),
        "confidence": result.confidence_score,
        "key_metrics": result.metrics,
        "priority": DOMAIN_CONFIG.get(domain, {}).get("priority", "medium"),
        "status": "ready_for_agent_population"
    }
    
    with open(t3_queue_file, 'w') as f:
        json.dump(queue_entry, f, indent=2)
    
    print(f"✓ Queued for T3 agent population")


def show_summary():
    """Show analysis summary"""
    print("\n=== T2 Analysis Summary ===")
    
    # Check completed analyses
    output_dir = Path(T2_OUTPUTS_PATH)
    if output_dir.exists():
        analysis_files = list(output_dir.glob("*_analysis_*.json"))
        print(f"Total analyses completed: {len(analysis_files)}")
        
        for file in sorted(analysis_files)[-5:]:  # Show last 5
            with open(file) as f:
                data = json.load(f)
            print(f"\n{data['domain']}:")
            print(f"  - Confidence: {data['confidence_score']:.2%}")
            print(f"  - Key findings: {len(data['key_findings'])}")
            print(f"  - Risks identified: {len(data['risks'])}")
            print(f"  - Opportunities: {len(data['opportunities'])}")


if __name__ == "__main__":
    test_neighborhood_analysis()
    test_financial_analysis()
    show_summary()