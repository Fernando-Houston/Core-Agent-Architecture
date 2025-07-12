#!/usr/bin/env python3
"""
Demo T3 Strategic Agent - Shows the strategic structuring capabilities
"""

import json
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent))
from t3_strategic_agent import T3StrategicAgent


def create_sample_t2_analyses(base_path: Path):
    """Create sample T2 analyses for demonstration"""
    t2_path = base_path / "T2_Analysis_Results"
    t2_path.mkdir(exist_ok=True)
    
    # Sample T2 analyses
    analyses = [
        {
            "analysis_id": "t2-2024-01-15-demo1",
            "analysis_type": "market_trend",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "appreciation_rate": 8.5,
                "rental_yield": 6.2,
                "demand_score": 85,
                "inventory_months": 2.3,
                "price_volatility": 0.12
            },
            "key_findings": [
                "Strong appreciation in Houston Heights area",
                "Rental yields exceeding market average",
                "Low inventory driving competitive market"
            ],
            "market_signals": ["expansion_phase", "seller_market"],
            "confidence_score": 0.85,
            "location": "Houston Heights",
            "market_cycle_phase": "expansion"
        },
        {
            "analysis_id": "t2-2024-01-15-demo2",
            "analysis_type": "investment_opportunity",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "development_activity": 125,
                "zoning_favorability": 0.9,
                "infrastructure_investment": 45000000,
                "innovation_index": 78,
                "construction_costs": 185
            },
            "key_findings": [
                "Major infrastructure improvements in Ion District",
                "Technology sector driving real estate demand",
                "Construction costs stabilizing after recent increases"
            ],
            "market_signals": ["tech_growth", "infrastructure_catalyst"],
            "confidence_score": 0.82,
            "location": "Ion District",
            "markets": ["Houston", "Midtown", "Ion District"]
        },
        {
            "analysis_id": "t2-2024-01-15-demo3",
            "analysis_type": "risk_assessment",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "vacancy_rate": 7.8,
                "default_rate": 2.1,
                "environmental_risk": 0.35,
                "regulatory_uncertainty": 0.25,
                "market_correlation": 0.78
            },
            "key_findings": [
                "Vacancy rates rising in certain submarkets",
                "Environmental considerations for coastal properties",
                "Regulatory changes pending for development zones"
            ],
            "market_signals": ["caution_advised", "risk_mitigation_needed"],
            "confidence_score": 0.79,
            "location": "West Houston"
        }
    ]
    
    # Save sample analyses
    saved_files = []
    for analysis in analyses:
        filename = f"{analysis['analysis_id']}.json"
        filepath = t2_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(analysis, f, indent=2)
            
        saved_files.append(filename)
        print(f"  Created sample T2 analysis: {filename}")
        
    return [a['analysis_id'] for a in analyses]


def display_strategic_structure(structure: dict):
    """Display the strategic structure in a readable format"""
    print("\n" + "="*70)
    print("STRATEGIC INTELLIGENCE STRUCTURE")
    print("="*70)
    
    print(f"\nStructure ID: {structure['structure_id']}")
    print(f"Confidence Score: {structure['confidence_score']:.2%}")
    print(f"Source Analyses: {len(structure['source_analyses'])}")
    
    # Market Narrative
    print(f"\n📊 MARKET NARRATIVE")
    print("-"*40)
    narrative = structure['market_narrative']
    print(f"Summary: {narrative['summary']}")
    print(f"\nKey Trends:")
    for trend in narrative['key_trends']:
        print(f"  • {trend}")
    print(f"\nMarket Drivers:")
    for driver in narrative['market_drivers'][:3]:
        print(f"  • {driver}")
    print(f"\nOutlook: {narrative['outlook']}")
    
    # Strategic Insights
    insights = structure['strategic_insights']
    
    print(f"\n💡 OPPORTUNITIES ({len(insights['opportunities'])})")
    print("-"*40)
    for i, opp in enumerate(insights['opportunities'][:3], 1):
        print(f"\n{i}. {opp['title']}")
        print(f"   Impact: {opp['impact_level']} | Confidence: {opp['confidence']:.2%}")
        print(f"   {opp['description']}")
        print(f"   Timeline: {opp['timeline']}")
        if opp['action_items']:
            print(f"   Actions:")
            for action in opp['action_items'][:2]:
                print(f"     - {action}")
                
    print(f"\n⚠️  RISKS ({len(insights['risks'])})")
    print("-"*40)
    for i, risk in enumerate(insights['risks'][:3], 1):
        print(f"\n{i}. {risk['title']}")
        print(f"   Impact: {risk['impact_level']} | Confidence: {risk['confidence']:.2%}")
        print(f"   {risk['description']}")
        if risk['action_items']:
            print(f"   Mitigation:")
            for action in risk['action_items'][:2]:
                print(f"     - {action}")
                
    print(f"\n🎯 RECOMMENDATIONS ({len(insights['recommendations'])})")
    print("-"*40)
    for i, rec in enumerate(insights['recommendations'][:3], 1):
        print(f"\n{i}. {rec['title']}")
        print(f"   {rec['description']}")
        print(f"   Priority: {rec['impact_level']} | Timeline: {rec['timeline']}")
        
    # User Segments
    print(f"\n👥 USER SEGMENT VIEWS")
    print("-"*40)
    for segment, data in structure['user_segments'].items():
        print(f"\n{segment.upper()}:")
        print(f"  Market Readiness: {data['market_readiness']['assessment']} "
              f"(Score: {data['market_readiness']['score']})")
        
        if data['priority_insights']:
            print(f"  Top Priority: {data['priority_insights'][0]['title']}")
            
        if data['action_plan']['immediate_actions']:
            print(f"  Immediate Action: {data['action_plan']['immediate_actions'][0]}")
            
    # Metadata
    print(f"\n📈 KEY METRICS")
    print("-"*40)
    if 'key_metrics' in structure['metadata']:
        for metric, values in list(structure['metadata']['key_metrics'].items())[:5]:
            print(f"  {metric}: {values['current']} ({values['trend']})")
            
    print("\n" + "="*70)


def main():
    """Run T3 Strategic Agent demonstration"""
    if len(sys.argv) > 1:
        base_path = Path(sys.argv[1])
    else:
        base_path = Path("/Users/fernandox/Desktop/Core Agent Architecture")
        
    print("\n" + "="*70)
    print("T3 STRATEGIC AGENT DEMONSTRATION")
    print("="*70)
    
    # Create sample T2 analyses
    print("\n1. Creating sample T2 analyses...")
    analysis_ids = create_sample_t2_analyses(base_path)
    
    # Initialize T3 agent
    print("\n2. Initializing T3 Strategic Agent...")
    t3_agent = T3StrategicAgent(str(base_path))
    print("   ✓ T3 Agent initialized")
    
    # Process analyses
    print("\n3. Processing T2 analyses into strategic intelligence...")
    try:
        structure = t3_agent.process_t2_analyses(analysis_ids=analysis_ids)
        
        if structure:
            print("   ✓ Strategic structuring complete")
            
            # Display the structure
            display_strategic_structure(structure)
            
            # Show output locations
            print("\n📁 OUTPUT FILES CREATED:")
            print("-"*40)
            t3_path = base_path / "T3_Strategic_Intelligence"
            
            # Main structure
            print(f"\nMain Structure:")
            print(f"  {t3_path / f'{structure['structure_id']}.json'}")
            
            # Opportunity profiles
            print(f"\nOpportunity Profiles:")
            for file in (t3_path / "opportunities").glob(f"*{structure['structure_id']}*.json"):
                print(f"  {file}")
                
            # Risk assessments
            print(f"\nRisk Assessments:")
            for file in (t3_path / "risks").glob(f"*{structure['structure_id']}*.json"):
                print(f"  {file}")
                
            # User views
            print(f"\nUser Segment Views:")
            for file in (t3_path / "user_views").glob(f"*{structure['structure_id']}*.json"):
                print(f"  {file}")
                
            print("\n✅ T3 Strategic Intelligence Ready for Use!")
            
            # Show example queries
            print("\n💭 EXAMPLE QUERIES THIS STRUCTURE CAN ANSWER:")
            print("-"*40)
            example_queries = [
                "What are the top investment opportunities in Houston right now?",
                "What risks should developers be aware of?",
                "Is this a good time for homeowners to buy or sell?",
                "Which neighborhoods show the strongest growth potential?",
                "What's the market outlook for the next 6 months?"
            ]
            
            for query in example_queries:
                print(f"  • {query}")
                
        else:
            print("   ❌ No structure created")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    
    # Auto cleanup in non-interactive mode
    print("\nAuto-cleaning demo files...")
    t2_path = base_path / "T2_Analysis_Results"
    for analysis_id in analysis_ids:
        for file in t2_path.glob(f"*{analysis_id}*.json"):
            file.unlink()
            print(f"  Removed: {file.name}")
    print("✓ Cleanup complete")


if __name__ == "__main__":
    main()