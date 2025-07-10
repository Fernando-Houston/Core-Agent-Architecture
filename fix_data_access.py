#!/usr/bin/env python3
"""
Fix data access issues in Houston Intelligence Platform
- Fixes Perplexity method name error
- Adds fallback for TF-IDF failures
- Improves knowledge base loading
"""

import json
import os
from pathlib import Path
import shutil

def fix_perplexity_method():
    """Add the missing search_houston_real_estate method to PerplexityClient"""
    
    perplexity_file = Path("perplexity_integration.py")
    content = perplexity_file.read_text()
    
    # Add the missing method after analyze_market_trends
    new_method = '''
    def search_houston_real_estate(self, query: str) -> Dict:
        """
        Search Houston real estate data (wrapper for compatibility)
        This method was referenced in master_intelligence_agent.py
        """
        return self.search_houston_data(query, "real estate")
'''
    
    # Find where to insert
    insert_pos = content.find("# Integration with daily refresh agent")
    if insert_pos > 0:
        content = content[:insert_pos] + new_method + "\n" + content[insert_pos:]
        perplexity_file.write_text(content)
        print("✅ Added search_houston_real_estate method to PerplexityClient")
    else:
        print("❌ Could not find insertion point for method")

def fix_knowledge_base_loader():
    """Add fallback for TF-IDF failures"""
    
    loader_file = Path("knowledge_base_loader.py")
    content = loader_file.read_text()
    
    # Add improved search method with fallback
    improved_search = '''
    def search_knowledge_fallback(self, agent_name: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Fallback search when TF-IDF fails - uses simple keyword matching"""
        records = self.load_agent_knowledge(agent_name)
        if not records:
            return []
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Score each record based on keyword matches
        scored_records = []
        for record in records:
            # Create searchable text from record
            text_parts = []
            for field in ['title', 'content', 'insight', 'summary', 'location', 'neighborhood']:
                if field in record:
                    text_parts.append(str(record[field]))
            
            record_text = ' '.join(text_parts).lower()
            record_words = set(record_text.split())
            
            # Calculate simple match score
            matches = len(query_words.intersection(record_words))
            if matches > 0:
                score = matches / len(query_words)
                scored_record = record.copy()
                scored_record['relevance_score'] = score
                scored_records.append((score, scored_record))
        
        # Sort by score and return top k
        scored_records.sort(key=lambda x: x[0], reverse=True)
        return [record for _, record in scored_records[:top_k]]
'''
    
    # Find the search_knowledge method and modify it
    search_start = content.find("def search_knowledge(")
    if search_start > 0:
        # Find the end of the method
        search_end = content.find("\n    def ", search_start + 1)
        if search_end < 0:
            search_end = len(content)
        
        # Get the original method
        original_method = content[search_start:search_end]
        
        # Modify to use fallback on TF-IDF error
        modified_method = original_method.replace(
            "except Exception as e:",
            """except Exception as e:
            logger.warning(f"TF-IDF search failed for {agent_name}, using fallback: {str(e)}")
            # Use fallback search
            return self.search_knowledge_fallback(agent_name, query, top_k)"""
        )
        
        # Replace the method and add the fallback method
        content = content[:search_start] + modified_method + improved_search + content[search_end:]
        
        loader_file.write_text(content)
        print("✅ Added fallback search to knowledge_base_loader.py")
    else:
        print("❌ Could not find search_knowledge method")

def create_hugging_face_todo():
    """Create the Hugging Face enhancement plan"""
    
    hf_plan = """# Hugging Face AI Enhancement - Implementation Plan

## Current Status
- ✅ API is deployed and running
- ✅ Knowledge base files are loaded (47 files)
- ⚠️ TF-IDF search is failing (empty vocabulary errors)
- ⚠️ Basic keyword matching as fallback
- 🎯 Ready for AI enhancement with Hugging Face

## Next Steps

### 1. Fix Current Issues (In Progress)
- [x] Fix Perplexity method name error
- [x] Add fallback search for TF-IDF failures
- [ ] Deploy fixes to Railway

### 2. Hugging Face Integration (Next)
- [ ] Create houston_ai_enhancer.py with FREE models
- [ ] Integrate FinBERT for market sentiment analysis
- [ ] Add BART for report summarization
- [ ] Implement DialoGPT for conversational AI
- [ ] Create enhanced agent wrappers
- [ ] Update API endpoints

### 3. Benefits of Hugging Face Enhancement
- **Sentiment Analysis**: Analyze market news and reports
- **Summarization**: Create executive summaries automatically
- **Conversational AI**: Natural language property queries
- **Cost**: $0 (FREE models running locally)
- **Performance**: Much better than keyword matching

### 4. Implementation Timeline
1. Deploy current fixes (5 minutes)
2. Implement Hugging Face base (30 minutes)
3. Integrate with agents (20 minutes)
4. Test and deploy (10 minutes)

Total: ~1 hour to AI-powered intelligence!
"""
    
    with open("HUGGING_FACE_ENHANCEMENT_PLAN.md", "w") as f:
        f.write(hf_plan)
    
    print("✅ Created Hugging Face enhancement plan")

def main():
    """Run all fixes"""
    print("🔧 Fixing Houston Intelligence Platform data access issues...")
    print("="*60)
    
    # Fix 1: Add missing Perplexity method
    print("\n1️⃣ Fixing Perplexity method error...")
    fix_perplexity_method()
    
    # Fix 2: Add fallback search for knowledge base
    print("\n2️⃣ Adding fallback search for TF-IDF failures...")
    fix_knowledge_base_loader()
    
    # Create enhancement plan
    print("\n3️⃣ Creating Hugging Face enhancement plan...")
    create_hugging_face_todo()
    
    print("\n" + "="*60)
    print("✅ Fixes completed!")
    print("\nNext steps:")
    print("1. Run: git add -A && git commit -m 'Fix data access issues'")
    print("2. Run: git push origin main")
    print("3. Wait for Railway to redeploy")
    print("4. Implement Hugging Face enhancement for better AI capabilities")

if __name__ == "__main__":
    main()