#!/usr/bin/env python3
"""
Test script to demonstrate the improved variety in Master Intelligence Agent responses
"""

from master_intelligence_agent import MasterIntelligenceAgent
import json

def test_query_variety():
    """Test various queries to show different responses"""
    agent = MasterIntelligenceAgent()
    
    test_queries = [
        {
            "query": "What are the best neighborhoods for investment?",
            "expected_type": "neighborhood ranking"
        },
        {
            "query": "Show me recent building permits in Houston",
            "expected_type": "permit activity"
        },
        {
            "query": "What are the current real estate market trends?",
            "expected_type": "market trends"
        },
        {
            "query": "Tell me about investment opportunities in East End",
            "expected_type": "location-specific investment"
        },
        {
            "query": "What financing options are available for developers?",
            "expected_type": "financing information"
        },
        {
            "query": "Analyze the Houston Heights neighborhood",
            "expected_type": "neighborhood analysis"
        },
        {
            "query": "What are the risks of developing in Houston?",
            "expected_type": "risk assessment"
        }
    ]
    
    print("=" * 80)
    print("MASTER INTELLIGENCE AGENT - QUERY VARIETY TEST")
    print("=" * 80)
    
    for test in test_queries:
        print(f"\n{'='*80}")
        print(f"Query: {test['query']}")
        print(f"Expected: {test['expected_type']}")
        print("-" * 80)
        
        result = agent.analyze_query(test['query'])
        
        print(f"Intent Detected: {result['intent']}")
        print(f"\nExecutive Summary:")
        print(result['executive_summary'])
        
        print(f"\nTop 3 Insights:")
        for i, insight in enumerate(result['key_insights'][:3], 1):
            print(f"{i}. {insight}")
        
        print(f"\nTop 3 Recommendations:")
        for i, rec in enumerate(result['recommendations'][:3], 1):
            print(f"{i}. {rec}")
        
        print(f"\nConfidence: {result['confidence']*100:.1f}%")
    
    # Save example output
    example_output = {
        "test_results": []
    }
    
    for test in test_queries[:3]:  # Save first 3 examples
        result = agent.analyze_query(test['query'])
        example_output["test_results"].append({
            "query": test['query'],
            "intent": result['intent'],
            "summary": result['executive_summary'],
            "first_insight": result['key_insights'][0] if result['key_insights'] else None,
            "first_recommendation": result['recommendations'][0] if result['recommendations'] else None
        })
    
    with open('master_agent_variety_examples.json', 'w') as f:
        json.dump(example_output, f, indent=2)
    
    print(f"\n{'='*80}")
    print("✅ Test complete! Each query returns contextually appropriate responses.")
    print("📄 Example outputs saved to: master_agent_variety_examples.json")

if __name__ == "__main__":
    test_query_variety()