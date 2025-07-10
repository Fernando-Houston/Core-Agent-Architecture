#!/usr/bin/env python3
"""
Knowledge Base Loader for Houston Intelligence Platform - FIXED VERSION
Properly handles the nested dictionary structure in knowledge base files
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
        
        # Map agent IDs to folder names
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
                    
                    # FIXED: Properly handle different file structures
                    if isinstance(data, list):
                        # It's already a list of records
                        knowledge_records.extend(data)
                    elif isinstance(data, dict):
                        # Check if it's a nested dictionary of records
                        if data and all(isinstance(v, dict) for v in data.values()):
                            # Check if values look like knowledge records (have id, title, or content)
                            first_value = next(iter(data.values()))
                            if any(key in first_value for key in ['id', 'title', 'content', 'insight']):
                                # This is a knowledge file with nested records
                                knowledge_records.extend(data.values())
                            elif 'insights' in data:
                                # This is a structured insights file
                                knowledge_records.extend(data['insights'])
                            elif 'records' in data:
                                # This is a structured records file
                                knowledge_records.extend(data['records'])
                            else:
                                # This is likely a metadata file, skip or add as single record
                                if 'agent_name' not in data:  # Skip pure metadata files
                                    knowledge_records.append(data)
                        elif 'insights' in data:
                            knowledge_records.extend(data['insights'])
                        elif 'records' in data:
                            knowledge_records.extend(data['records'])
                        # Skip pure metadata files
                        elif 'agent_name' in data and 'categories' in data:
                            continue  # Skip expertise_summary.json type files
                        else:
                            # Single record
                            knowledge_records.append(data)
                            
            except Exception as e:
                logger.error(f"Error loading {json_file}: {str(e)}")
                continue
        
        # Cache the results
        self.knowledge_cache[agent_name] = knowledge_records
        self.last_cache_update[agent_name] = datetime.now()
        
        # Build TF-IDF matrix for searching
        self._build_tfidf_index(agent_name, knowledge_records)
        
        logger.info(f"Loaded {len(knowledge_records)} records for {agent_name}")
        
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
            
            # Handle nested content structure
            if 'content' in record and isinstance(record['content'], dict):
                content = record['content']
                if 'summary' in content:
                    text_parts.append(str(content['summary']))
                if 'key_findings' in content and isinstance(content['key_findings'], list):
                    text_parts.extend([str(f) for f in content['key_findings']])
                if 'recommendations' in content and isinstance(content['recommendations'], list):
                    text_parts.extend([str(r) for r in content['recommendations']])
                # Add any string values from metrics
                if 'metrics' in content and isinstance(content['metrics'], dict):
                    for key, value in content['metrics'].items():
                        text_parts.append(f"{key} {value}")
            elif 'content' in record:
                text_parts.append(str(record['content']))
            
            # Add other searchable fields
            for field in ['insight', 'summary', 'domain', 'category', 'subcategory']:
                if field in record:
                    text_parts.append(str(record[field]))
            
            # Add location/neighborhood info
            if 'location' in record:
                text_parts.append(str(record['location']))
            if 'neighborhood' in record:
                text_parts.append(str(record['neighborhood']))
            if 'geographic_scope' in record and isinstance(record['geographic_scope'], list):
                text_parts.extend([str(loc) for loc in record['geographic_scope']])
            
            # Add tags
            if 'tags' in record and isinstance(record['tags'], list):
                text_parts.extend([str(t) for t in record['tags']])
                
            # Combine all text
            combined_text = ' '.join(text_parts)
            texts.append(combined_text)
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,  # Include terms that appear in at least 1 document
            max_df=0.95  # Exclude terms that appear in more than 95% of documents
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            self.vectorizers[agent_name] = vectorizer
            self.tfidf_matrices[agent_name] = tfidf_matrix
            logger.info(f"Built TF-IDF index for {agent_name} with vocabulary size: {len(vectorizer.vocabulary_)}")
        except Exception as e:
            logger.error(f"Error building TF-IDF index for {agent_name}: {str(e)}")
    
    def search_knowledge(self, agent_name: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base using semantic similarity"""
        # Load knowledge if not already loaded
        records = self.load_agent_knowledge(agent_name)
        
        if not records:
            return []
        
        # If TF-IDF search is available, use it
        if agent_name in self.vectorizers and agent_name in self.tfidf_matrices:
            try:
                # Vectorize the query
                query_vector = self.vectorizers[agent_name].transform([query])
                
                # Calculate similarities
                similarities = cosine_similarity(query_vector, self.tfidf_matrices[agent_name]).flatten()
                
                # Get top k most similar records
                top_indices = similarities.argsort()[-top_k:][::-1]
                
                results = []
                for idx in top_indices:
                    if similarities[idx] > 0.05:  # Lower threshold for better recall
                        record = records[idx].copy()
                        record['relevance_score'] = float(similarities[idx])
                        results.append(record)
                
                return results
                
            except Exception as e:
                logger.warning(f"TF-IDF search failed for {agent_name}, using fallback: {str(e)}")
        
        # Fallback to keyword search
        return self.search_knowledge_fallback(agent_name, query, top_k)
    
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
            
            # Add title
            if 'title' in record:
                text_parts.append(str(record['title']))
            
            # Add content fields
            if 'content' in record and isinstance(record['content'], dict):
                content = record['content']
                for field in ['summary', 'key_findings', 'recommendations']:
                    if field in content:
                        if isinstance(content[field], list):
                            text_parts.extend([str(item) for item in content[field]])
                        else:
                            text_parts.append(str(content[field]))
            
            # Add other fields
            for field in ['insight', 'summary', 'domain', 'category', 'location', 'neighborhood']:
                if field in record:
                    text_parts.append(str(record[field]))
            
            # Add geographic scope
            if 'geographic_scope' in record and isinstance(record['geographic_scope'], list):
                text_parts.extend([str(loc) for loc in record['geographic_scope']])
            
            # Add tags
            if 'tags' in record and isinstance(record['tags'], list):
                text_parts.extend([str(t) for t in record['tags']])
            
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
                # Check multiple fields for location match
                location_lower = location.lower()
                
                # Check direct location field
                if 'location' in record and location_lower in str(record['location']).lower():
                    record_copy = record.copy()
                    record_copy['agent_source'] = agent
                    results.append(record_copy)
                    continue
                
                # Check geographic_scope
                if 'geographic_scope' in record and isinstance(record['geographic_scope'], list):
                    if any(location_lower in str(scope).lower() for scope in record['geographic_scope']):
                        record_copy = record.copy()
                        record_copy['agent_source'] = agent
                        results.append(record_copy)
                        continue
                
                # Check domain field
                if 'domain' in record and location_lower in str(record['domain']).lower():
                    record_copy = record.copy()
                    record_copy['agent_source'] = agent
                    results.append(record_copy)
                    continue
                
                # Check in title and content
                if 'title' in record and location_lower in str(record['title']).lower():
                    record_copy = record.copy()
                    record_copy['agent_source'] = agent
                    results.append(record_copy)
                    continue
                
                # Check in content summary
                if 'content' in record and isinstance(record['content'], dict):
                    if 'summary' in record['content'] and location_lower in str(record['content']['summary']).lower():
                        record_copy = record.copy()
                        record_copy['agent_source'] = agent
                        results.append(record_copy)
        
        return results
    
    def get_category_knowledge(self, category: str, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get knowledge by category (permits, trends, investments, etc.)"""
        category_keywords = {
            'permits': ['permit', 'building', 'construction', 'approval', 'zoning', 'expedited'],
            'trends': ['trend', 'growth', 'market', 'development', 'emerging', 'forecast', 'projection'],
            'investment': ['investment', 'roi', 'return', 'opportunity', 'financing', 'funding'],
            'risk': ['risk', 'flood', 'environmental', 'hazard', 'compliance', 'mitigation'],
            'developer': ['developer', 'builder', 'construction', 'project', 'development'],
            'technology': ['technology', 'tech', 'innovation', 'smart', 'proptech', 'digital']
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
                # Create searchable text
                text_parts = []
                
                # Add all text fields
                for field in ['title', 'category', 'subcategory', 'domain']:
                    if field in record:
                        text_parts.append(str(record[field]))
                
                # Add content fields
                if 'content' in record and isinstance(record['content'], dict):
                    content = record['content']
                    for field in ['summary', 'key_findings', 'recommendations']:
                        if field in content:
                            if isinstance(content[field], list):
                                text_parts.extend([str(item) for item in content[field]])
                            else:
                                text_parts.append(str(content[field]))
                
                # Add tags
                if 'tags' in record and isinstance(record['tags'], list):
                    text_parts.extend([str(t) for t in record['tags']])
                
                record_text = ' '.join(text_parts).lower()
                
                # Check if any keyword matches
                if any(keyword in record_text for keyword in keywords):
                    record_copy = record.copy()
                    record_copy['agent_source'] = agent
                    results.append(record_copy)
        
        return results
    
    def get_cross_domain_insights(self) -> List[Dict[str, Any]]:
        """Load cross-domain intelligence insights"""
        insights = []
        
        # Check both possible locations
        paths_to_check = [
            self.base_path / "Cross_Domain_Intelligence" / "cross_domain_insights.json",
            Path("Processing_Pipeline/Cross_Domain_Intelligence/cross_domain_insights.json")
        ]
        
        for cross_domain_path in paths_to_check:
            if cross_domain_path.exists():
                try:
                    with open(cross_domain_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, dict) and 'insights' in data:
                            insights.extend(data['insights'])
                        elif isinstance(data, list):
                            insights.extend(data)
                        break
                except Exception as e:
                    logger.error(f"Error loading cross-domain insights from {cross_domain_path}: {str(e)}")
        
        return insights
    
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
    """Test the fixed knowledge base loader"""
    loader = KnowledgeBaseLoader()
    
    print("Testing Fixed Knowledge Base Loader...")
    print("=" * 60)
    
    # Test loading market intelligence
    market_records = loader.load_agent_knowledge("market_intelligence")
    print(f"\nMarket Intelligence Records: {len(market_records)}")
    if market_records:
        print(f"Sample: {market_records[0].get('title', 'No title')}")
    
    # Test searching
    test_queries = [
        "permits Houston",
        "Sugar Land investment",
        "market trends",
        "expedited permit program"
    ]
    
    for query in test_queries:
        print(f"\nSearch Results for '{query}':")
        search_results = loader.search_knowledge("market_intelligence", query, top_k=3)
        for i, result in enumerate(search_results):
            title = result.get('title', 'No title')
            score = result.get('relevance_score', 0)
            print(f"{i+1}. {title} (relevance: {score:.3f})")
    
    # Test location-specific
    location_results = loader.get_location_specific_knowledge("Sugar Land")
    print(f"\nLocation-specific results for 'Sugar Land': {len(location_results)}")
    
    # Test category search
    permit_results = loader.get_category_knowledge("permits")
    print(f"\nCategory results for 'permits': {len(permit_results)}")
    
    print("\n✅ Fixed Knowledge Base Loader is working!")


if __name__ == "__main__":
    test_knowledge_loader()