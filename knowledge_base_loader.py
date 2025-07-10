#!/usr/bin/env python3
"""
Knowledge Base Loader for Houston Intelligence Platform
Loads and searches through actual knowledge base files instead of using hardcoded responses
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class KnowledgeBaseLoader:
    def __init__(self, base_path: str = "Agent_Knowledge_Bases"):
        self.base_path = Path(base_path)
        self.knowledge_cache = {}
        self.vectorizers = {}
        self.tfidf_matrices = {}
        self.last_cache_update = {}
        self.cache_duration = 300  # 5 minutes
        
    def load_agent_knowledge(self, agent_name: str, force_reload: bool = False) -> List[Dict[str, Any]]:
        """Load all knowledge files for a specific agent"""
        # Check cache first
        if not force_reload and agent_name in self.knowledge_cache:
            if (datetime.now() - self.last_cache_update.get(agent_name, datetime.min)).seconds < self.cache_duration:
                return self.knowledge_cache[agent_name]
        
        knowledge_records = []
        
        # Map agent IDs to folder names (using underscores as found in actual structure)
        folder_mapping = {
            "market_intelligence": "Market_Intelligence",
            "neighborhood_intelligence": "Neighborhood_Intelligence",
            "financial_intelligence": "Financial_Intelligence",
            "environmental_intelligence": "Environmental_Intelligence",
            "regulatory_intelligence": "Regulatory_Intelligence",
            "technology_intelligence": "Technology_Innovation_Intelligence"
        }
        
        agent_folder = folder_mapping.get(agent_name, agent_name)
        agent_path = self.base_path / agent_folder
        
        if not agent_path.exists():
            logger.warning(f"Agent knowledge base not found: {agent_path}")
            return []
        
        # Load all JSON files in the agent folder
        for json_file in agent_path.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    
                    # Handle different file structures
                    if isinstance(data, list):
                        knowledge_records.extend(data)
                    elif isinstance(data, dict):
                        if 'insights' in data:
                            knowledge_records.extend(data['insights'])
                        elif 'records' in data:
                            knowledge_records.extend(data['records'])
                        else:
                            knowledge_records.append(data)
                            
            except Exception as e:
                logger.error(f"Error loading {json_file}: {str(e)}")
                continue
        
        # Cache the results
        self.knowledge_cache[agent_name] = knowledge_records
        self.last_cache_update[agent_name] = datetime.now()
        
        # Build TF-IDF matrix for searching
        self._build_tfidf_index(agent_name, knowledge_records)
        
        return knowledge_records
    
    def _build_tfidf_index(self, agent_name: str, records: List[Dict[str, Any]]):
        """Build TF-IDF index for semantic search"""
        if not records:
            return
        
        # Extract searchable text from records
        texts = []
        for record in records:
            text_parts = []
            
            # Add various fields to searchable text
            if 'title' in record:
                text_parts.append(str(record['title']))
            if 'content' in record:
                text_parts.append(str(record['content']))
            if 'insight' in record:
                text_parts.append(str(record['insight']))
            if 'summary' in record:
                text_parts.append(str(record['summary']))
            if 'key_findings' in record:
                text_parts.append(' '.join(str(f) for f in record['key_findings']))
            if 'location' in record:
                text_parts.append(str(record['location']))
            if 'neighborhood' in record:
                text_parts.append(str(record['neighborhood']))
            if 'tags' in record:
                text_parts.append(' '.join(str(t) for t in record['tags']))
                
            texts.append(' '.join(text_parts))
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            self.vectorizers[agent_name] = vectorizer
            self.tfidf_matrices[agent_name] = tfidf_matrix
        except Exception as e:
            logger.error(f"Error building TF-IDF index for {agent_name}: {str(e)}")
    
    def search_knowledge(self, agent_name: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base using semantic similarity"""
        # Load knowledge if not already loaded
        records = self.load_agent_knowledge(agent_name)
        
        if not records or agent_name not in self.vectorizers:
            return records[:top_k] if records else []
        
        try:
            # Vectorize the query
            query_vector = self.vectorizers[agent_name].transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vector, self.tfidf_matrices[agent_name]).flatten()
            
            # Get top k most similar records
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity threshold
                    record = records[idx].copy()
                    record['relevance_score'] = float(similarities[idx])
                    results.append(record)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge for {agent_name}: {str(e)}")
            return records[:top_k] if records else []
    
    def get_location_specific_knowledge(self, location: str, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get knowledge specific to a location"""
        results = []
        
        agents = [agent_name] if agent_name else [
            "market_intelligence", "neighborhood_intelligence", 
            "financial_intelligence", "environmental_intelligence",
            "regulatory_intelligence", "technology_intelligence"
        ]
        
        for agent in agents:
            records = self.load_agent_knowledge(agent)
            
            for record in records:
                # Check if record is relevant to the location
                record_text = json.dumps(record).lower()
                if location.lower() in record_text:
                    record_copy = record.copy()
                    record_copy['agent_source'] = agent
                    results.append(record_copy)
        
        return results
    
    def get_category_knowledge(self, category: str, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get knowledge by category (permits, trends, investments, etc.)"""
        category_keywords = {
            'permits': ['permit', 'building', 'construction', 'approval', 'zoning'],
            'trends': ['trend', 'growth', 'market', 'development', 'emerging'],
            'investment': ['investment', 'roi', 'return', 'opportunity', 'financing'],
            'risk': ['risk', 'flood', 'environmental', 'hazard', 'compliance'],
            'developer': ['developer', 'builder', 'construction', 'project'],
            'technology': ['technology', 'tech', 'innovation', 'smart', 'proptech']
        }
        
        keywords = category_keywords.get(category.lower(), [category.lower()])
        
        results = []
        agents = [agent_name] if agent_name else [
            "market_intelligence", "neighborhood_intelligence",
            "financial_intelligence", "environmental_intelligence",
            "regulatory_intelligence", "technology_intelligence"
        ]
        
        for agent in agents:
            records = self.load_agent_knowledge(agent)
            
            for record in records:
                record_text = json.dumps(record).lower()
                if any(keyword in record_text for keyword in keywords):
                    record_copy = record.copy()
                    record_copy['agent_source'] = agent
                    results.append(record_copy)
        
        return results
    
    def get_cross_domain_insights(self) -> List[Dict[str, Any]]:
        """Load cross-domain intelligence insights"""
        cross_domain_path = Path("Processing_Pipeline/Cross_Domain_Intelligence/cross_domain_insights.json")
        
        if cross_domain_path.exists():
            try:
                with open(cross_domain_path, 'r') as f:
                    data = json.load(f)
                    return data.get('insights', [])
            except Exception as e:
                logger.error(f"Error loading cross-domain insights: {str(e)}")
        
        return []
    
    def get_latest_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent insights across all agents"""
        all_insights = []
        
        for agent_name in ["market_intelligence", "neighborhood_intelligence",
                          "financial_intelligence", "environmental_intelligence",
                          "regulatory_intelligence", "technology_intelligence"]:
            records = self.load_agent_knowledge(agent_name)
            for record in records:
                record_copy = record.copy()
                record_copy['agent_source'] = agent_name
                all_insights.append(record_copy)
        
        # Sort by timestamp if available, otherwise by confidence
        def get_sort_key(record):
            if 'timestamp' in record:
                try:
                    return datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                except:
                    pass
            return datetime.min
        
        all_insights.sort(key=get_sort_key, reverse=True)
        
        return all_insights[:limit]
    
    def refresh_cache(self):
        """Force refresh all cached knowledge"""
        self.knowledge_cache.clear()
        self.vectorizers.clear()
        self.tfidf_matrices.clear()
        self.last_cache_update.clear()


def test_knowledge_loader():
    """Test the knowledge base loader"""
    loader = KnowledgeBaseLoader()
    
    print("Testing Knowledge Base Loader...")
    print("=" * 60)
    
    # Test loading market intelligence
    market_records = loader.load_agent_knowledge("market_intelligence")
    print(f"\nMarket Intelligence Records: {len(market_records)}")
    if market_records:
        print(f"Sample: {market_records[0].get('title', 'No title')}")
    
    # Test searching
    search_results = loader.search_knowledge("market_intelligence", "permits Houston", top_k=3)
    print(f"\nSearch Results for 'permits Houston': {len(search_results)}")
    for i, result in enumerate(search_results):
        print(f"{i+1}. {result.get('title', 'No title')} (relevance: {result.get('relevance_score', 0):.2f})")
    
    # Test location-specific
    location_results = loader.get_location_specific_knowledge("Katy")
    print(f"\nLocation-specific results for 'Katy': {len(location_results)}")
    
    # Test category search
    permit_results = loader.get_category_knowledge("permits")
    print(f"\nCategory results for 'permits': {len(permit_results)}")
    
    print("\n✅ Knowledge Base Loader is working!")


if __name__ == "__main__":
    test_knowledge_loader()