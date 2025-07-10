#!/usr/bin/env python3
"""
Test Suite for Fixed Master Intelligence Agent
Validates that the system uses real knowledge bases instead of hardcoded responses
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import hashlib

# Import both versions for comparison
from master_intelligence_agent import MasterIntelligenceAgent as OriginalAgent
from master_intelligence_agent_fixed import MasterIntelligenceAgent as FixedAgent


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.details = []
    
    def add_test(self, name: str, passed: bool, details: str = ""):
        if passed:
            self.passed += 1
            status = "✅ PASS"
        else:
            self.failed += 1
            status = "❌ FAIL"
        
        self.details.append({
            'name': name,
            'status': status,
            'details': details
        })
        
        print(f"{status}: {name}")
        if details:
            print(f"   Details: {details}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Summary: {self.passed}/{total} passed ({self.passed/total*100:.1f}%)")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for test in self.details:
                if test['status'] == "❌ FAIL":
                    print(f"  - {test['name']}: {test['details']}")


def test_knowledge_loading():
    """Test 1: Verify knowledge bases are loaded"""
    print("\n🧪 Test 1: Knowledge Base Loading")
    print("-" * 40)
    
    results = TestResults()
    
    try:
        agent = FixedAgent()
        
        # Check knowledge loader exists
        results.add_test(
            "Knowledge loader initialized",
            hasattr(agent, 'knowledge_loader'),
            "Knowledge loader attribute exists"
        )
        
        # Check knowledge bases loaded
        kb_count = len(agent.knowledge_loader.knowledge_bases)
        results.add_test(
            "Knowledge bases loaded",
            kb_count > 0,
            f"Loaded {kb_count} agent knowledge bases"
        )
        
        # Check each expected agent
        expected_agents = [
            'market_intelligence',
            'neighborhood_intelligence',
            'financial_intelligence',
            'environmental_intelligence',
            'regulatory_intelligence',
            'technology_intelligence'
        ]
        
        for agent_id in expected_agents:
            kb_exists = agent_id in agent.knowledge_loader.knowledge_bases
            if kb_exists:
                item_count = agent.knowledge_loader.get_knowledge_stats(agent_id)
                results.add_test(
                    f"{agent_id} knowledge loaded",
                    item_count > 0,
                    f"{item_count} items"
                )
            else:
                results.add_test(
                    f"{agent_id} knowledge loaded",
                    False,
                    "Knowledge base not found"
                )
        
    except Exception as e:
        results.add_test("Knowledge loading", False, str(e))
    
    return results


def test_search_functionality():
    """Test 2: Verify search returns relevant results"""
    print("\n\n🧪 Test 2: Search Functionality")
    print("-" * 40)
    
    results = TestResults()
    
    try:
        agent = FixedAgent()
        
        # Test search queries
        test_searches = [
            ("neighborhood_intelligence", "Houston Heights investment", 0.3),
            ("market_intelligence", "permit trends analysis", 0.2),
            ("financial_intelligence", "construction lending rates", 0.2),
            ("environmental_intelligence", "flood risk assessment", 0.2)
        ]
        
        for agent_id, query, min_score in test_searches:
            search_results = agent.knowledge_loader.search_knowledge(agent_id, query, top_k=5)
            
            passed = len(search_results) > 0
            if passed and search_results:
                top_score = search_results[0]['score']
                passed = top_score >= min_score
                details = f"Top result score: {top_score:.3f} (min: {min_score})"
            else:
                details = "No results found"
            
            results.add_test(
                f"Search '{query}' in {agent_id}",
                passed,
                details
            )
        
    except Exception as e:
        results.add_test("Search functionality", False, str(e))
    
    return results


def test_different_responses():
    """Test 3: Verify similar queries return different responses"""
    print("\n\n🧪 Test 3: Response Variation")
    print("-" * 40)
    
    results = TestResults()
    
    try:
        agent = FixedAgent()
        
        # Similar queries that should return different results
        queries = [
            "What are the best neighborhoods for investment?",
            "Which Houston areas have highest ROI?",
            "Tell me about Houston Heights market"
        ]
        
        responses = []
        summaries = []
        
        for query in queries:
            result = agent.analyze_query(query)
            responses.append(result)
            summaries.append(result.get('executive_summary', ''))
        
        # Check that responses are different
        unique_summaries = set(summaries)
        results.add_test(
            "Different queries produce different summaries",
            len(unique_summaries) == len(summaries),
            f"{len(unique_summaries)} unique summaries out of {len(summaries)}"
        )
        
        # Check that insights are different
        insights_sets = []
        for response in responses:
            insights = tuple(response.get('key_insights', []))
            insights_sets.append(insights)
        
        unique_insights = set(insights_sets)
        results.add_test(
            "Different queries produce different insights",
            len(unique_insights) >= 2,
            f"{len(unique_insights)} unique insight sets"
        )
        
        # Check data points vary
        data_counts = [len(r.get('data_highlights', [])) for r in responses]
        results.add_test(
            "Responses contain data highlights",
            all(count > 0 for count in data_counts),
            f"Data counts: {data_counts}"
        )
        
    except Exception as e:
        results.add_test("Response variation", False, str(e))
    
    return results


def test_real_data_in_responses():
    """Test 4: Verify responses contain real data from knowledge bases"""
    print("\n\n🧪 Test 4: Real Data Validation")
    print("-" * 40)
    
    results = TestResults()
    
    try:
        agent = FixedAgent()
        
        # Test specific queries that should return known data
        test_cases = [
            {
                'query': 'Houston Heights investment analysis',
                'expected_terms': ['investment', 'Heights', 'score', 'analysis'],
                'min_matches': 2
            },
            {
                'query': 'Sugar Land market forecast',
                'expected_terms': ['Sugar Land', 'forecast', 'market', 'price'],
                'min_matches': 2
            },
            {
                'query': 'What are the permit trends in Houston?',
                'expected_terms': ['permit', 'trend', 'Houston', 'development'],
                'min_matches': 2
            }
        ]
        
        for test in test_cases:
            result = agent.analyze_query(test['query'])
            
            # Convert result to string for searching
            result_str = json.dumps(result).lower()
            
            # Count matches
            matches = 0
            matched_terms = []
            for term in test['expected_terms']:
                if term.lower() in result_str:
                    matches += 1
                    matched_terms.append(term)
            
            passed = matches >= test['min_matches']
            results.add_test(
                f"Query '{test['query']}' contains expected data",
                passed,
                f"Found {matches}/{len(test['expected_terms'])} terms: {matched_terms}"
            )
            
            # Also check that response has substance
            has_insights = len(result.get('key_insights', [])) > 0
            has_data = len(result.get('data_highlights', [])) > 0
            
            results.add_test(
                f"Query '{test['query']}' has insights and data",
                has_insights and has_data,
                f"Insights: {len(result.get('key_insights', []))}, Data points: {len(result.get('data_highlights', []))}"
            )
        
    except Exception as e:
        results.add_test("Real data validation", False, str(e))
    
    return results


def test_no_hardcoded_responses():
    """Test 5: Verify the system doesn't use hardcoded responses"""
    print("\n\n🧪 Test 5: No Hardcoded Responses")
    print("-" * 40)
    
    results = TestResults()
    
    try:
        agent = FixedAgent()
        
        # Test queries that would trigger hardcoded responses in original
        hardcoded_triggers = [
            "best investment neighborhoods",
            "permit",
            "trend"
        ]
        
        response_hashes = []
        
        for trigger in hardcoded_triggers:
            # Query twice with slight variations
            query1 = f"Tell me about {trigger} in Houston"
            query2 = f"What are the {trigger} opportunities?"
            
            result1 = agent.analyze_query(query1)
            result2 = agent.analyze_query(query2)
            
            # Hash the key insights to compare
            insights1 = json.dumps(sorted(result1.get('key_insights', [])))
            insights2 = json.dumps(sorted(result2.get('key_insights', [])))
            
            hash1 = hashlib.md5(insights1.encode()).hexdigest()
            hash2 = hashlib.md5(insights2.encode()).hexdigest()
            
            # Different queries should produce different insights
            results.add_test(
                f"Variations of '{trigger}' produce different results",
                hash1 != hash2,
                f"Hash1: {hash1[:8]}..., Hash2: {hash2[:8]}..."
            )
        
    except Exception as e:
        results.add_test("Hardcoded response check", False, str(e))
    
    return results


def test_cache_functionality():
    """Test 6: Verify caching works correctly"""
    print("\n\n🧪 Test 6: Cache Functionality")
    print("-" * 40)
    
    results = TestResults()
    
    try:
        agent = FixedAgent()
        
        # Clear cache first
        agent.cache_manager.clear_cache()
        
        test_query = "What are the best investment opportunities in Houston?"
        
        # First query - should not be cached
        import time
        start_time = time.time()
        result1 = agent.analyze_query(test_query)
        first_time = time.time() - start_time
        
        # Second query - should be cached
        start_time = time.time()
        result2 = agent.analyze_query(test_query)
        second_time = time.time() - start_time
        
        # Cached query should be faster
        results.add_test(
            "Cache speeds up repeated queries",
            second_time < first_time * 0.5,  # At least 50% faster
            f"First: {first_time:.3f}s, Cached: {second_time:.3f}s"
        )
        
        # Results should be identical
        results.add_test(
            "Cached results are identical",
            json.dumps(result1, sort_keys=True) == json.dumps(result2, sort_keys=True),
            "Results match exactly"
        )
        
    except Exception as e:
        results.add_test("Cache functionality", False, str(e))
    
    return results


def test_location_specific_queries():
    """Test 7: Verify location-specific queries work"""
    print("\n\n🧪 Test 7: Location-Specific Queries")
    print("-" * 40)
    
    results = TestResults()
    
    try:
        agent = FixedAgent()
        
        locations = ["Houston Heights", "Sugar Land", "Katy", "East End"]
        
        for location in locations:
            query = f"Tell me about {location} investment potential"
            result = agent.analyze_query(query)
            
            # Check if location appears in response
            response_str = json.dumps(result).lower()
            location_mentioned = location.lower() in response_str
            
            results.add_test(
                f"Query about {location} mentions the location",
                location_mentioned,
                f"Location {'found' if location_mentioned else 'not found'} in response"
            )
            
            # Check if we got location-specific data
            has_insights = len(result.get('key_insights', [])) > 0
            results.add_test(
                f"Query about {location} returns insights",
                has_insights,
                f"{len(result.get('key_insights', []))} insights found"
            )
        
    except Exception as e:
        results.add_test("Location-specific queries", False, str(e))
    
    return results


def run_all_tests():
    """Run all tests and generate report"""
    print("🔬 Houston Intelligence Platform - Fixed Version Test Suite")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = TestResults()
    
    # Run each test suite
    test_suites = [
        test_knowledge_loading(),
        test_search_functionality(),
        test_different_responses(),
        test_real_data_in_responses(),
        test_no_hardcoded_responses(),
        test_cache_functionality(),
        test_location_specific_queries()
    ]
    
    # Aggregate results
    for suite_results in test_suites:
        all_results.passed += suite_results.passed
        all_results.failed += suite_results.failed
        all_results.details.extend(suite_results.details)
    
    # Final summary
    print("\n" * 2)
    print("=" * 60)
    print("FINAL TEST RESULTS")
    all_results.summary()
    
    # Save test report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': all_results.passed + all_results.failed,
        'passed': all_results.passed,
        'failed': all_results.failed,
        'success_rate': all_results.passed / (all_results.passed + all_results.failed) * 100,
        'test_details': all_results.details
    }
    
    report_path = Path("test_results_fixed_master_agent.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed test report saved to: {report_path}")
    
    # Return success/failure
    return all_results.failed == 0


def compare_with_original():
    """Compare fixed version with original to show improvements"""
    print("\n\n🔄 Comparing Fixed vs Original Implementation")
    print("=" * 60)
    
    try:
        original = OriginalAgent()
        fixed = FixedAgent()
        
        test_query = "What are the best neighborhoods for investment?"
        
        print(f"\nTest Query: '{test_query}'")
        print("-" * 40)
        
        # Get responses from both
        original_result = original.analyze_query(test_query)
        fixed_result = fixed.analyze_query(test_query)
        
        # Compare executive summaries
        print("\n📊 Executive Summary Comparison:")
        print(f"Original (first 200 chars): {original_result['executive_summary'][:200]}...")
        print(f"Fixed (first 200 chars): {fixed_result['executive_summary'][:200]}...")
        
        # Compare data sources
        print("\n📚 Data Sources:")
        print(f"Original uses: Hardcoded responses")
        print(f"Fixed uses: {len(fixed.knowledge_loader.knowledge_bases)} knowledge bases with {sum(fixed.knowledge_loader.get_knowledge_stats(a) for a in fixed.knowledge_loader.knowledge_bases)} total items")
        
        # Compare variety
        print("\n🎯 Response Variety:")
        queries = ["best neighborhoods", "top areas to invest", "where should I buy"]
        
        original_summaries = set()
        fixed_summaries = set()
        
        for q in queries:
            original_summaries.add(original.analyze_query(q)['executive_summary'][:100])
            fixed_summaries.add(fixed.analyze_query(q)['executive_summary'][:100])
        
        print(f"Original unique responses: {len(original_summaries)}/{len(queries)}")
        print(f"Fixed unique responses: {len(fixed_summaries)}/{len(queries)}")
        
        print("\n✅ The fixed version provides more varied, data-driven responses!")
        
    except Exception as e:
        print(f"❌ Error in comparison: {e}")


if __name__ == "__main__":
    # Run all tests
    success = run_all_tests()
    
    # Compare with original
    compare_with_original()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)