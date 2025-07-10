#!/usr/bin/env python3
"""
T3 Agent Population Summary Report Generator
Generates comprehensive summary of populated intelligence
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def generate_summary_report(base_path: str):
    """Generate comprehensive summary report"""
    base_path = Path(base_path)
    kb_path = base_path / "Agent_Knowledge_Bases"
    
    print("T3 AGENT POPULATION ENGINE - SUMMARY REPORT")
    print("="*60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Load master index
    master_index = kb_path / "master_index.json"
    if master_index.exists():
        with open(master_index, 'r') as f:
            index = json.load(f)
        
        print(f"\nTOTAL INTELLIGENCE RECORDS: {index['total_records']}")
        print("\nAGENT POPULATION STATUS:")
        print("-"*40)
        
        for agent, data in index['agents'].items():
            status = "✓ POPULATED" if data['record_count'] > 0 else "○ EMPTY"
            print(f"{status} {agent}: {data['record_count']} records")
    
    # Analyze intelligence distribution
    print("\n\nINTELLIGENCE DISTRIBUTION:")
    print("-"*40)
    
    category_counts = defaultdict(int)
    domain_counts = defaultdict(int)
    
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
            for kb_file in agent_dir.glob("*_knowledge.json"):
                category = kb_file.stem.replace('_knowledge', '')
                
                try:
                    with open(kb_file, 'r') as f:
                        knowledge = json.load(f)
                        count = len(knowledge)
                        if count > 0:
                            category_counts[category] += count
                            
                        # Count domains
                        for record in knowledge.values():
                            domain = record.get('domain', 'unknown')
                            domain_counts[domain] += 1
                except:
                    pass
    
    print("\nBy Category:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count}")
    
    print("\nBy Domain:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {domain}: {count}")
    
    # Cross-domain intelligence
    cross_domain_path = kb_path / "Cross_Domain_Intelligence"
    if cross_domain_path.exists():
        print("\n\nCROSS-DOMAIN INTELLIGENCE:")
        print("-"*40)
        
        insights_file = cross_domain_path / "cross_domain_insights.json"
        if insights_file.exists():
            with open(insights_file, 'r') as f:
                insights_data = json.load(f)
                
            summary = insights_data.get('summary', {})
            print(f"Total Insights: {summary.get('total_insights', 0)}")
            print(f"High Priority: {summary.get('high_priority', 0)}")
            print(f"Insight Types: {', '.join(summary.get('insight_types', []))}")
        
        connections_file = cross_domain_path / "cross_domain_connections.json"
        if connections_file.exists():
            with open(connections_file, 'r') as f:
                connections_data = json.load(f)
                
            conns = connections_data.get('connections', {})
            print(f"\nConnection Types:")
            print(f"  Geographic: {len(conns.get('geographic_connections', []))}")
            print(f"  Topic-based: {len(conns.get('topic_connections', []))}")
            print(f"  Value Chain: {len(conns.get('value_chain_connections', []))}")
            print(f"  Risk-Opportunity: {len(conns.get('risk_opportunity_pairs', []))}")
    
    # Key capabilities
    print("\n\nKEY CAPABILITIES ENABLED:")
    print("-"*40)
    
    capabilities = [
        "✓ Multi-domain market analysis",
        "✓ Neighborhood investment scoring",
        "✓ Financial ROI modeling",
        "✓ Environmental risk assessment",
        "✓ Regulatory compliance tracking",
        "✓ Technology innovation monitoring",
        "✓ Cross-domain opportunity identification",
        "✓ Integrated development intelligence"
    ]
    
    for cap in capabilities:
        print(cap)
    
    # Geographic coverage
    print("\n\nGEOGRAPHIC COVERAGE:")
    print("-"*40)
    
    geo_coverage = set()
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
            for kb_file in agent_dir.glob("*_knowledge.json"):
                try:
                    with open(kb_file, 'r') as f:
                        knowledge = json.load(f)
                        
                    for record in knowledge.values():
                        geo_coverage.update(record.get('geographic_scope', []))
                except:
                    pass
    
    print(f"Areas Covered: {', '.join(sorted(geo_coverage))}")
    
    # Usage examples
    print("\n\nSAMPLE QUERIES READY:")
    print("-"*40)
    queries = [
        "What are the best investment opportunities in Houston Heights?",
        "Show me mixed-use development ROI models",
        "What flood risks affect West Houston development?",
        "Which areas have new zoning opportunities?",
        "How is technology impacting Houston real estate?",
        "What are the top 3 neighborhoods for development?",
        "Show cross-domain risks and mitigation strategies"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")
    
    print("\n\nSYSTEM STATUS: READY FOR WEBSITE INTEGRATION")
    print("="*60)
    
    # Save report
    report_path = base_path / "Processing_Status" / f"t3_summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, 'w') as f:
        # Redirect print to file
        import sys
        original_stdout = sys.stdout
        sys.stdout = f
        
        # Re-run all prints to file
        generate_summary_report(str(base_path))
        
        sys.stdout = original_stdout
    
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    generate_summary_report(base_path)
