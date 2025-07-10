# Houston Intelligence Platform - Complete Implementation Plan

## Executive Summary

The Houston Intelligence Platform currently uses hardcoded responses instead of real knowledge bases. This implementation plan provides a step-by-step guide to fix the `master_intelligence_agent.py` to dynamically load and search through actual knowledge data.

---

## 1. Implementation Plan to Fix master_intelligence_agent.py

### Phase 1: Create Knowledge Loading System

#### Step 1.1: Add Knowledge Base Loader Class
```python
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class KnowledgeBaseLoader:
    """Loads and manages access to agent knowledge bases"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.knowledge_bases = {}
        self.vectorizers = {}
        self.document_vectors = {}
        self.load_all_knowledge_bases()
    
    def load_all_knowledge_bases(self):
        """Load all agent knowledge bases"""
        kb_path = self.base_path / "Agent_Knowledge_Bases"
        
        agent_mappings = {
            "market_intelligence": "Market_Intelligence",
            "neighborhood_intelligence": "Neighborhood_Intelligence",
            "financial_intelligence": "Financial_Intelligence",
            "environmental_intelligence": "Environmental_Intelligence",
            "regulatory_intelligence": "Regulatory_Intelligence",
            "technology_intelligence": "Technology_Innovation_Intelligence"
        }
        
        for agent_id, folder_name in agent_mappings.items():
            agent_path = kb_path / folder_name
            if agent_path.exists():
                self.knowledge_bases[agent_id] = self.load_agent_knowledge(agent_path)
                self.prepare_search_index(agent_id)
    
    def load_agent_knowledge(self, agent_path: Path) -> Dict[str, Any]:
        """Load all JSON files for a specific agent"""
        knowledge = {}
        
        for json_file in agent_path.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    knowledge[json_file.stem] = data
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        return knowledge
    
    def prepare_search_index(self, agent_id: str):
        """Create TF-IDF search index for agent knowledge"""
        if agent_id not in self.knowledge_bases:
            return
        
        documents = []
        doc_ids = []
        
        # Extract searchable text from knowledge base
        for category, items in self.knowledge_bases[agent_id].items():
            if isinstance(items, dict):
                for item_id, item_data in items.items():
                    # Create searchable document
                    search_text = self.extract_searchable_text(item_data)
                    documents.append(search_text)
                    doc_ids.append((category, item_id))
        
        if documents:
            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 3)
            )
            
            # Fit and transform documents
            doc_vectors = vectorizer.fit_transform(documents)
            
            self.vectorizers[agent_id] = vectorizer
            self.document_vectors[agent_id] = {
                'vectors': doc_vectors,
                'doc_ids': doc_ids
            }
    
    def extract_searchable_text(self, item_data: Dict[str, Any]) -> str:
        """Extract all searchable text from a knowledge item"""
        text_parts = []
        
        # Add title
        if 'title' in item_data:
            text_parts.append(str(item_data['title']))
        
        # Add content
        if 'content' in item_data:
            content = item_data['content']
            if isinstance(content, dict):
                # Add summary
                if 'summary' in content:
                    text_parts.append(str(content['summary']))
                
                # Add key findings
                if 'key_findings' in content:
                    for finding in content['key_findings']:
                        text_parts.append(str(finding))
                
                # Add recommendations
                if 'recommendations' in content:
                    for rec in content['recommendations']:
                        text_parts.append(str(rec))
        
        # Add tags
        if 'tags' in item_data:
            text_parts.extend([str(tag) for tag in item_data['tags']])
        
        # Add geographic scope
        if 'geographic_scope' in item_data:
            text_parts.extend([str(loc) for loc in item_data['geographic_scope']])
        
        return ' '.join(text_parts)
    
    def search_knowledge(self, agent_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search agent knowledge base using semantic similarity"""
        if agent_id not in self.vectorizers:
            return []
        
        # Vectorize query
        query_vector = self.vectorizers[agent_id].transform([query])
        
        # Calculate similarities
        doc_data = self.document_vectors[agent_id]
        similarities = cosine_similarity(query_vector, doc_data['vectors']).flatten()
        
        # Get top results
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Relevance threshold
                category, item_id = doc_data['doc_ids'][idx]
                item_data = self.knowledge_bases[agent_id][category].get(item_id, {})
                
                results.append({
                    'category': category,
                    'item_id': item_id,
                    'score': float(similarities[idx]),
                    'data': item_data
                })
        
        return results
```

#### Step 1.2: Modify MasterIntelligenceAgent.__init__
```python
def __init__(self):
    # ... existing code ...
    
    # Initialize knowledge base loader
    self.knowledge_loader = KnowledgeBaseLoader(self.base_path)
    
    # Load cross-domain mappings
    self.cross_domain_mappings = self.load_cross_domain_mappings()
```

### Phase 2: Replace Hardcoded Responses with Knowledge Search

#### Step 2.1: Rewrite query_specialized_agent Method
```python
def query_specialized_agent(
    self, 
    agent_id: str, 
    query: str, 
    intent: QueryIntent,
    location: Optional[str],
    query_context: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Query a specific specialized agent using real knowledge base"""
    
    # Build enhanced query for better search
    enhanced_query = self.build_enhanced_query(query, intent, location, query_context)
    
    # Search knowledge base
    search_results = self.knowledge_loader.search_knowledge(
        agent_id, 
        enhanced_query, 
        top_k=10
    )
    
    if not search_results:
        return None
    
    # Process search results into agent response
    agent_knowledge = {
        "agent_name": self.agent_capabilities[agent_id].name,
        "confidence": self.calculate_result_confidence(search_results),
        "insights": [],
        "data_points": []
    }
    
    # Extract insights and data points from search results
    for result in search_results[:5]:  # Top 5 results
        item_data = result['data']
        
        # Extract insights
        if 'content' in item_data:
            content = item_data['content']
            
            # Add summary as insight
            if 'summary' in content:
                agent_knowledge['insights'].append(content['summary'])
            
            # Add key findings
            if 'key_findings' in content:
                for finding in content['key_findings'][:2]:  # Max 2 per result
                    agent_knowledge['insights'].append(finding)
            
            # Extract metrics as data points
            if 'metrics' in content:
                for metric_name, metric_value in content['metrics'].items():
                    data_point = {
                        "metric": metric_name.replace('_', ' ').title(),
                        "value": str(metric_value)
                    }
                    
                    # Add additional context if available
                    if 'trends' in content:
                        data_point['trend'] = content['trends'].get(metric_name, 'stable')
                    
                    agent_knowledge['data_points'].append(data_point)
    
    # Ensure we have meaningful content
    if not agent_knowledge['insights']:
        agent_knowledge['insights'] = [
            f"Analysis based on {len(search_results)} relevant data points",
            f"Confidence level: {agent_knowledge['confidence']*100:.1f}%"
        ]
    
    return agent_knowledge

def build_enhanced_query(
    self, 
    query: str, 
    intent: QueryIntent, 
    location: Optional[str],
    query_context: Dict[str, Any]
) -> str:
    """Build enhanced query for better knowledge base search"""
    query_parts = [query]
    
    # Add location if specified
    if location:
        query_parts.append(location)
    
    # Add property types
    if query_context.get('property_types'):
        query_parts.extend(query_context['property_types'])
    
    # Add action type
    if query_context.get('action_type'):
        query_parts.append(query_context['action_type'])
    
    # Add intent-specific terms
    intent_terms = {
        QueryIntent.MARKET_ANALYSIS: ["market", "trends", "analysis", "competition"],
        QueryIntent.NEIGHBORHOOD_ASSESSMENT: ["neighborhood", "area", "location", "community"],
        QueryIntent.INVESTMENT_OPPORTUNITY: ["investment", "roi", "return", "opportunity"],
        QueryIntent.REGULATORY_COMPLIANCE: ["zoning", "permit", "regulation", "compliance"],
        QueryIntent.RISK_ASSESSMENT: ["risk", "flood", "environmental", "hazard"],
        QueryIntent.DEVELOPMENT_FEASIBILITY: ["feasibility", "development", "potential", "viability"],
        QueryIntent.COMPETITIVE_INTELLIGENCE: ["competitor", "market share", "competition"],
        QueryIntent.COMPREHENSIVE_ANALYSIS: ["comprehensive", "analysis", "overview", "assessment"]
    }
    
    if intent in intent_terms:
        query_parts.extend(intent_terms[intent])
    
    return ' '.join(query_parts)

def calculate_result_confidence(self, search_results: List[Dict[str, Any]]) -> float:
    """Calculate confidence based on search result scores"""
    if not search_results:
        return 0.5
    
    # Weight by relevance scores
    total_score = sum(r['score'] for r in search_results[:3])
    max_possible = 3.0  # Maximum if all results had perfect score
    
    # Normalize to 0.6-0.95 range
    normalized = (total_score / max_possible) * 0.35 + 0.6
    
    return min(0.95, normalized)
```

### Phase 3: Add Perplexity Integration

#### Step 3.1: Create Perplexity Data Fetcher
```python
import aiohttp
import asyncio
from datetime import datetime, timedelta

class PerplexityDataFetcher:
    """Fetches real-time data from Perplexity API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('PERPLEXITY_API_KEY')
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
    
    async def fetch_real_time_data(self, query: str, location: str = "Houston") -> Dict[str, Any]:
        """Fetch real-time data from Perplexity"""
        cache_key = f"{query}_{location}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                return cached_data
        
        # Prepare enhanced query
        enhanced_query = f"{query} {location} Texas real estate development 2024 2025"
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'model': 'pplx-7b-online',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a Houston real estate intelligence expert. Provide specific, current data with numbers and dates.'
                        },
                        {
                            'role': 'user',
                            'content': enhanced_query
                        }
                    ]
                }
                
                async with session.post(
                    'https://api.perplexity.ai/chat/completions',
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = self.parse_perplexity_response(data)
                        
                        # Cache result
                        self.cache[cache_key] = (result, datetime.now())
                        
                        return result
                    else:
                        return {'error': f'API returned status {response.status}'}
                        
        except Exception as e:
            return {'error': str(e)}
    
    def parse_perplexity_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Perplexity response into structured data"""
        try:
            content = response_data['choices'][0]['message']['content']
            
            # Extract metrics using regex patterns
            metrics = {}
            
            # Price patterns
            price_pattern = r'\$([0-9,]+(?:\.[0-9]+)?[KMB]?)'
            prices = re.findall(price_pattern, content)
            if prices:
                metrics['prices'] = prices[:3]
            
            # Percentage patterns
            percent_pattern = r'([0-9]+(?:\.[0-9]+)?)\s*%'
            percentages = re.findall(percent_pattern, content)
            if percentages:
                metrics['percentages'] = percentages[:3]
            
            # Number patterns
            number_pattern = r'\b([0-9]{1,3}(?:,[0-9]{3})*)\b'
            numbers = re.findall(number_pattern, content)
            if numbers:
                metrics['counts'] = numbers[:3]
            
            return {
                'content': content,
                'metrics': metrics,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}

# Add to MasterIntelligenceAgent.__init__
self.perplexity_fetcher = PerplexityDataFetcher()
```

### Phase 4: Implement Free Data Sources

#### Step 4.1: Create Houston Free Data Collector
```python
class HoustonFreeDataCollector:
    """Collects free, publicly available Houston data"""
    
    def __init__(self):
        self.data_sources = {
            'permits': 'https://data.houstontx.gov/resource/jbxr-prhf.json',
            'crime': 'https://data.houstontx.gov/resource/9e3t-zr3p.json',
            'demographics': 'https://api.census.gov/data/2022/acs/acs5',
            'weather': 'https://api.weather.gov/gridpoints/HGX/'
        }
        self.cache = {}
    
    async def fetch_permit_data(self, area: str = None) -> Dict[str, Any]:
        """Fetch recent building permit data"""
        url = self.data_sources['permits']
        params = {
            '$limit': 100,
            '$order': 'date_issued DESC',
            '$where': "date_issued > '2024-01-01'"
        }
        
        if area:
            params['$where'] += f" AND neighborhood LIKE '%{area}%'"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.process_permit_data(data)
        except Exception as e:
            print(f"Error fetching permit data: {e}")
            return {}
    
    def process_permit_data(self, raw_data: List[Dict]) -> Dict[str, Any]:
        """Process raw permit data into insights"""
        if not raw_data:
            return {}
        
        # Count by type
        permit_types = {}
        total_value = 0
        neighborhoods = {}
        
        for permit in raw_data:
            # Count by type
            permit_type = permit.get('permit_type', 'Unknown')
            permit_types[permit_type] = permit_types.get(permit_type, 0) + 1
            
            # Sum values
            try:
                value = float(permit.get('estimated_cost', 0))
                total_value += value
            except:
                pass
            
            # Count by neighborhood
            neighborhood = permit.get('neighborhood', 'Unknown')
            neighborhoods[neighborhood] = neighborhoods.get(neighborhood, 0) + 1
        
        # Get top neighborhoods
        top_neighborhoods = sorted(
            neighborhoods.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return {
            'total_permits': len(raw_data),
            'total_value': f"${total_value:,.0f}",
            'permit_types': dict(list(permit_types.items())[:5]),
            'top_neighborhoods': dict(top_neighborhoods),
            'avg_value': f"${total_value/len(raw_data):,.0f}" if raw_data else "$0"
        }
    
    async def fetch_market_indicators(self) -> Dict[str, Any]:
        """Fetch various market indicators from free sources"""
        indicators = {}
        
        # This would connect to free APIs like:
        # - Federal Reserve Economic Data (FRED)
        # - Census Bureau API
        # - OpenWeatherMap (for weather risks)
        # - USGS (for geological data)
        
        return indicators

# Add to MasterIntelligenceAgent.__init__
self.free_data_collector = HoustonFreeDataCollector()
```

### Phase 5: Add Caching and Performance Optimization

#### Step 5.1: Implement Smart Caching
```python
from functools import lru_cache
import hashlib

class CacheManager:
    """Manages caching for knowledge base queries"""
    
    def __init__(self, cache_dir: Path = Path("cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache = {}
        self.cache_ttl = timedelta(hours=6)
    
    def get_cache_key(self, agent_id: str, query: str, context: Dict) -> str:
        """Generate cache key from query parameters"""
        cache_data = f"{agent_id}:{query}:{sorted(context.items())}"
        return hashlib.md5(cache_data.encode()).hexdigest()
    
    def get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached result if valid"""
        # Check memory cache first
        if cache_key in self.memory_cache:
            result, timestamp = self.memory_cache[cache_key]
            if datetime.now() - timestamp < self.cache_ttl:
                return result
        
        # Check disk cache
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    
                timestamp = datetime.fromisoformat(cached_data['timestamp'])
                if datetime.now() - timestamp < self.cache_ttl:
                    # Update memory cache
                    self.memory_cache[cache_key] = (cached_data['result'], timestamp)
                    return cached_data['result']
            except:
                pass
        
        return None
    
    def cache_result(self, cache_key: str, result: Dict[str, Any]):
        """Cache query result"""
        timestamp = datetime.now()
        
        # Update memory cache
        self.memory_cache[cache_key] = (result, timestamp)
        
        # Save to disk
        cache_file = self.cache_dir / f"{cache_key}.json"
        cache_data = {
            'timestamp': timestamp.isoformat(),
            'result': result
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)

# Add to MasterIntelligenceAgent.__init__
self.cache_manager = CacheManager()
```

---

## 2. Testing Strategy

### Test Suite 1: Knowledge Base Loading
```python
def test_knowledge_loading():
    """Test that knowledge bases are properly loaded"""
    master = MasterIntelligenceAgent()
    
    # Test each agent has knowledge loaded
    for agent_id in master.agent_capabilities.keys():
        assert agent_id in master.knowledge_loader.knowledge_bases
        kb = master.knowledge_loader.knowledge_bases[agent_id]
        assert len(kb) > 0
        print(f"✓ {agent_id}: {sum(len(v) for v in kb.values())} knowledge items")

def test_search_functionality():
    """Test search returns relevant results"""
    master = MasterIntelligenceAgent()
    
    test_queries = [
        ("Heights investment ROI", "neighborhood_intelligence"),
        ("flood risk mitigation", "environmental_intelligence"),
        ("construction lending rates", "financial_intelligence"),
        ("permit approval timeline", "regulatory_intelligence")
    ]
    
    for query, expected_agent in test_queries:
        results = master.knowledge_loader.search_knowledge(expected_agent, query)
        assert len(results) > 0
        assert results[0]['score'] > 0.3
        print(f"✓ '{query}' returned {len(results)} results")

def test_different_responses():
    """Test that similar queries return different, data-driven responses"""
    master = MasterIntelligenceAgent()
    
    queries = [
        "What are the best neighborhoods for investment?",
        "Which areas have the highest ROI?",
        "Where should I invest in Houston?"
    ]
    
    responses = []
    for query in queries:
        result = master.analyze_query(query)
        responses.append(result['executive_summary'])
    
    # Ensure responses are different but relevant
    for i in range(len(responses)):
        for j in range(i+1, len(responses)):
            similarity = calculate_text_similarity(responses[i], responses[j])
            assert 0.3 < similarity < 0.9  # Similar topic but different content
            print(f"✓ Responses {i+1} and {j+1} similarity: {similarity:.2f}")
```

### Test Suite 2: Real Data Validation
```python
def test_real_data_in_responses():
    """Validate responses contain real data from knowledge bases"""
    master = MasterIntelligenceAgent()
    
    # Test specific data points appear in responses
    test_cases = [
        {
            'query': 'Houston Heights investment analysis',
            'expected_data': ['85', 'investment_score', '15%', 'appreciation'],
            'agent': 'neighborhood_intelligence'
        },
        {
            'query': 'Sugar Land market forecast',
            'expected_data': ['425000', 'median', '12-18%', 'projection'],
            'agent': 'neighborhood_intelligence'
        }
    ]
    
    for test in test_cases:
        result = master.analyze_query(test['query'])
        response_text = json.dumps(result)
        
        matches = 0
        for expected in test['expected_data']:
            if expected.lower() in response_text.lower():
                matches += 1
        
        assert matches >= 2  # At least 2 expected data points
        print(f"✓ '{test['query']}' contains {matches}/{len(test['expected_data'])} expected data points")
```

---

## 3. Additional Improvements

### 3.1 Perplexity Integration for Real-Time Data
```python
# Add to master_intelligence_agent.py
async def enrich_with_real_time_data(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich response with real-time data from Perplexity"""
    
    # Extract key topics from query
    query_topics = self.extract_query_topics(synthesis['query'])
    
    # Fetch real-time data
    real_time_insights = []
    for topic in query_topics[:2]:  # Limit API calls
        data = await self.perplexity_fetcher.fetch_real_time_data(
            topic, 
            synthesis.get('location', 'Houston')
        )
        
        if 'content' in data:
            real_time_insights.append({
                'topic': topic,
                'insight': data['content'][:200] + '...',
                'metrics': data.get('metrics', {}),
                'source': 'Real-time data'
            })
    
    # Add to synthesis
    synthesis['real_time_insights'] = real_time_insights
    
    return synthesis
```

### 3.2 Free Houston Data Integration
```python
# Add periodic data refresh
class DataRefreshScheduler:
    """Schedules regular updates of free data sources"""
    
    def __init__(self, master_agent):
        self.master_agent = master_agent
        self.schedule_daily_refresh()
    
    def schedule_daily_refresh(self):
        """Run daily at 6 AM"""
        schedule.every().day.at("06:00").do(self.refresh_all_data)
    
    async def refresh_all_data(self):
        """Refresh all free data sources"""
        print("Starting daily data refresh...")
        
        # Fetch permit data
        permit_data = await self.master_agent.free_data_collector.fetch_permit_data()
        
        # Update knowledge base with fresh data
        self.update_knowledge_base('market_intelligence', {
            'id': f'permits_{datetime.now().strftime("%Y%m%d")}',
            'title': 'Daily Permit Update',
            'content': {
                'summary': f"Houston issued {permit_data.get('total_permits', 0)} permits",
                'metrics': permit_data
            },
            'timestamp': datetime.now().isoformat()
        })
        
        print("Data refresh completed")
```

### 3.3 Feedback Loop Implementation
```python
class FeedbackCollector:
    """Collects and processes user feedback for continuous improvement"""
    
    def __init__(self, db_path: str = "feedback.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize feedback database"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                response_id TEXT,
                rating INTEGER,
                comment TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def collect_feedback(self, query: str, response_id: str, rating: int, comment: str = ""):
        """Store user feedback"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (query, response_id, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (query, response_id, rating, comment))
        
        conn.commit()
        conn.close()
    
    def analyze_feedback(self) -> Dict[str, Any]:
        """Analyze feedback to identify improvement areas"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get average ratings
        cursor.execute('''
            SELECT AVG(rating) as avg_rating, COUNT(*) as count
            FROM feedback
            WHERE timestamp > datetime('now', '-7 days')
        ''')
        
        avg_rating, count = cursor.fetchone()
        
        # Get low-rated queries
        cursor.execute('''
            SELECT query, AVG(rating) as avg_rating, COUNT(*) as count
            FROM feedback
            WHERE rating < 3
            GROUP BY query
            ORDER BY count DESC
            LIMIT 10
        ''')
        
        problem_queries = cursor.fetchall()
        
        conn.close()
        
        return {
            'avg_rating': avg_rating,
            'total_feedback': count,
            'problem_queries': problem_queries
        }
```

---

## 4. Knowledge Base Enhancement

### 4.1 Adding New Data Sources
```python
class KnowledgeBaseUpdater:
    """Tools for updating and enhancing knowledge bases"""
    
    def add_knowledge_item(
        self, 
        agent_id: str, 
        category: str, 
        item_data: Dict[str, Any]
    ):
        """Add new knowledge item to agent's knowledge base"""
        kb_path = Path("Agent_Knowledge_Bases") / self.get_agent_folder(agent_id)
        category_file = kb_path / f"{category}.json"
        
        # Load existing data
        if category_file.exists():
            with open(category_file, 'r') as f:
                knowledge = json.load(f)
        else:
            knowledge = {}
        
        # Generate unique ID
        item_id = hashlib.md5(
            f"{item_data.get('title', '')}_{datetime.now()}".encode()
        ).hexdigest()[:12]
        
        # Add metadata
        item_data['id'] = item_id
        item_data['timestamp'] = datetime.now().isoformat()
        item_data['version'] = '1.0'
        
        # Add to knowledge base
        knowledge[item_id] = item_data
        
        # Save updated knowledge
        with open(category_file, 'w') as f:
            json.dump(knowledge, f, indent=2)
        
        # Update search index
        self.update_search_index(agent_id)
    
    def bulk_import_data(self, data_source: str, mapping: Dict[str, str]):
        """Import data from external sources"""
        # Implementation for CSV, JSON, API imports
        pass
```

### 4.2 Update Mechanisms
```python
# Automated update pipeline
class AutomatedUpdatePipeline:
    def __init__(self):
        self.sources = {
            'permits': PermitDataUpdater(),
            'market': MarketDataUpdater(),
            'news': NewsDataUpdater()
        }
    
    async def run_updates(self):
        """Run all data updates"""
        for source_name, updater in self.sources.items():
            try:
                new_data = await updater.fetch_latest()
                self.process_and_store(source_name, new_data)
            except Exception as e:
                print(f"Error updating {source_name}: {e}")
```

### 4.3 Versioning System
```python
class KnowledgeVersionControl:
    """Version control for knowledge base changes"""
    
    def create_snapshot(self, agent_id: str) -> str:
        """Create versioned snapshot of knowledge base"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"{agent_id}_{timestamp}"
        
        # Copy current knowledge to snapshots directory
        source = Path("Agent_Knowledge_Bases") / agent_id
        destination = Path("snapshots") / snapshot_id
        
        shutil.copytree(source, destination)
        
        # Create metadata
        metadata = {
            'snapshot_id': snapshot_id,
            'agent_id': agent_id,
            'timestamp': datetime.now().isoformat(),
            'file_count': len(list(destination.glob("*.json")))
        }
        
        with open(destination / "snapshot_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return snapshot_id
    
    def rollback_to_snapshot(self, snapshot_id: str):
        """Rollback knowledge base to specific version"""
        # Implementation for rollback functionality
        pass
```

---

## Implementation Steps

1. **Phase 1 (Day 1-2)**: Implement KnowledgeBaseLoader class
   - Load existing knowledge bases
   - Create search functionality
   - Test with sample queries

2. **Phase 2 (Day 3-4)**: Replace hardcoded responses
   - Modify query_specialized_agent method
   - Implement enhanced query building
   - Test response generation

3. **Phase 3 (Day 5)**: Add real-time data
   - Integrate Perplexity API
   - Add free data sources
   - Test data enrichment

4. **Phase 4 (Day 6)**: Optimize performance
   - Implement caching
   - Add async operations
   - Performance testing

5. **Phase 5 (Day 7)**: Testing and refinement
   - Run full test suite
   - Fix edge cases
   - Document changes

## Success Metrics

1. **Response Quality**
   - 100% of responses use real knowledge base data
   - Average confidence score > 0.75
   - User satisfaction rating > 4.5/5

2. **Performance**
   - Average response time < 2 seconds
   - Cache hit rate > 60%
   - Support 100+ concurrent queries

3. **Data Freshness**
   - Daily updates from free sources
   - Real-time data for time-sensitive queries
   - Knowledge base growth of 10% monthly

## Maintenance Plan

1. **Daily**: Automated data refresh from free sources
2. **Weekly**: Review feedback and update problem areas
3. **Monthly**: Full knowledge base audit and enhancement
4. **Quarterly**: Major version update with new features

This implementation plan provides a complete roadmap to transform the Houston Intelligence Platform from using hardcoded responses to a dynamic, knowledge-driven system with real-time data integration.