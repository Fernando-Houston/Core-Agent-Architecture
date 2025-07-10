#!/usr/bin/env python3
"""Debug knowledge base loading and search functionality"""

import json
from pathlib import Path
from knowledge_base_loader import KnowledgeBaseLoader
import sys

def debug_knowledge_base():
    print("🔍 DEBUGGING KNOWLEDGE BASE LOADER")
    print("="*80)
    
    loader = KnowledgeBaseLoader()
    
    # Test 1: Check if knowledge base path exists
    print("\n1. Checking Knowledge Base Path:")
    kb_path = Path("Agent_Knowledge_Bases")
    print(f"   - Path exists: {kb_path.exists()}")
    print(f"   - Absolute path: {kb_path.absolute()}")
    
    if kb_path.exists():
        print("\n   Available agent folders:")
        for folder in kb_path.iterdir():
            if folder.is_dir():
                json_files = list(folder.glob("*.json"))
                print(f"   - {folder.name}: {len(json_files)} JSON files")
    
    # Test 2: Load market intelligence knowledge
    print("\n2. Loading Market Intelligence Knowledge:")
    market_records = loader.load_agent_knowledge("market_intelligence")
    print(f"   - Records loaded: {len(market_records)}")
    
    if market_records:
        print("\n   Sample records structure:")
        for i, record in enumerate(market_records[:3]):
            print(f"\n   Record {i+1}:")
            print(f"   - Type: {type(record)}")
            print(f"   - Keys: {list(record.keys()) if isinstance(record, dict) else 'Not a dict'}")
            if isinstance(record, dict):
                print(f"   - Title: {record.get('title', 'NO TITLE')}")
                print(f"   - Content type: {type(record.get('content', {}))}")
                if 'content' in record and isinstance(record['content'], dict):
                    print(f"   - Content keys: {list(record['content'].keys())}")
    
    # Test 3: Test search functionality
    print("\n3. Testing Search Functionality:")
    test_queries = [
        "permits",
        "houston building permits",
        "investment opportunities",
        "Sugar Land",
        "market trends"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        results = loader.search_knowledge("market_intelligence", query, top_k=3)
        print(f"   - Results found: {len(results)}")
        
        if results:
            for j, result in enumerate(results):
                print(f"     {j+1}. {result.get('title', 'NO TITLE')} (score: {result.get('relevance_score', 0):.3f})")
        else:
            print("     No results found!")
    
    # Test 4: Check TF-IDF indexing
    print("\n4. Checking TF-IDF Index:")
    print(f"   - Vectorizers created: {list(loader.vectorizers.keys())}")
    print(f"   - TF-IDF matrices: {list(loader.tfidf_matrices.keys())}")
    
    if "market_intelligence" in loader.vectorizers:
        vectorizer = loader.vectorizers["market_intelligence"]
        print(f"   - Vocabulary size: {len(vectorizer.vocabulary_)}")
        print(f"   - Sample terms: {list(vectorizer.vocabulary_.keys())[:10]}")
    
    # Test 5: Check actual file content
    print("\n5. Checking Raw File Content:")
    sample_file = kb_path / "Market_Intelligence" / "market_analysis_knowledge.json"
    if sample_file.exists():
        with open(sample_file, 'r') as f:
            data = json.load(f)
            print(f"   - File structure: {type(data)}")
            if isinstance(data, dict):
                print(f"   - Top-level keys: {list(data.keys())[:5]}")
                # Check structure of first item
                if data:
                    first_key = list(data.keys())[0]
                    first_item = data[first_key]
                    print(f"\n   First item structure:")
                    print(f"   - ID: {first_item.get('id', 'NO ID')}")
                    print(f"   - Title: {first_item.get('title', 'NO TITLE')}")
                    print(f"   - Content: {first_item.get('content', {})}")
    
    # Test 6: Category search
    print("\n6. Testing Category Search:")
    categories = ["permits", "investment", "trends"]
    for category in categories:
        results = loader.get_category_knowledge(category, "market_intelligence")
        print(f"   - Category '{category}': {len(results)} results")
    
    print("\n" + "="*80)
    print("✅ Debug complete! Check output above for issues.")

if __name__ == "__main__":
    debug_knowledge_base()