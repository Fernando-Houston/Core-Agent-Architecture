#!/usr/bin/env python3
"""
Comprehensive Knowledge Structuring System for T3
Structures T2 outputs into specialized agent knowledge bases
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import hashlib
import re


class KnowledgeStructurer:
    """Main class for structuring T2 intelligence into agent knowledge bases"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.t2_output_path = self.base_path / "T2_Intelligence_Output"
        self.kb_path = self.base_path / "Agent_Knowledge_Bases"
        self.kb_path.mkdir(exist_ok=True)
        
        # Agent domain mappings
        self.agent_domains = {
            "Market_Intelligence": {
                "primary_domains": ["market_forecasts", "pricing_trends", "competitive_analysis", "development_pipeline"],
                "keywords": ["market", "price", "forecast", "competition", "demand", "supply", "trend"],
                "categories": ["price_predictions", "market_analysis", "competitive_landscape", "demand_supply"]
            },
            "Neighborhood_Intelligence": {
                "primary_domains": ["houston_heights", "katy_area", "sugar_land", "the_woodlands", "memorial", "midtown"],
                "keywords": ["neighborhood", "area", "district", "community", "location", "demographic"],
                "categories": ["area_profiles", "demographic_analysis", "growth_patterns", "infrastructure_assessment"]
            },
            "Financial_Intelligence": {
                "primary_domains": ["financing_options", "investment_analysis", "lending_trends", "tax_implications"],
                "keywords": ["roi", "investment", "financing", "lending", "tax", "return", "profit", "cost"],
                "categories": ["roi_models", "financing_analysis", "investment_strategies", "risk_assessment"]
            },
            "Environmental_Intelligence": {
                "primary_domains": ["flood_risk_data", "air_quality", "environmental_regulations", "coastal_protection"],
                "keywords": ["flood", "environmental", "risk", "climate", "sustainability", "green", "pollution"],
                "categories": ["risk_assessment", "compliance_requirements", "mitigation_strategies", "sustainability_metrics"]
            },
            "Regulatory_Intelligence": {
                "primary_domains": ["zoning_data", "permit_requirements", "compliance_tracking", "planning_commission"],
                "keywords": ["zoning", "permit", "regulation", "compliance", "approval", "ordinance", "code"],
                "categories": ["zoning_updates", "permit_processes", "compliance_guidelines", "regulatory_changes"]
            },
            "Technology_Innovation_Intelligence": {
                "primary_domains": ["Innovation_districts", "smart_city_initiatives", "development_technologies", "investment_flows"],
                "keywords": ["innovation", "technology", "smart", "digital", "proptech", "startup", "tech"],
                "categories": ["innovation_hubs", "tech_adoption", "smart_infrastructure", "investment_trends"]
            }
        }
        
        # Initialize indexes
        self.geographic_index = defaultdict(list)
        self.temporal_index = defaultdict(list)
        self.priority_index = defaultdict(list)
        self.cross_domain_mappings = defaultdict(lambda: defaultdict(list))
        
    def structure_all_knowledge(self):
        """Main method to structure all T2 outputs into agent knowledge bases"""
        print("Starting comprehensive knowledge structuring...")
        
        # Process all T2 files
        t2_files = list(self.t2_output_path.glob("*.json"))
        total_insights = 0
        
        for t2_file in t2_files:
            print(f"\nProcessing: {t2_file.name}")
            insights = self.process_t2_file(t2_file)
            total_insights += insights
            
        # Build comprehensive indexes
        self.build_geographic_index()
        self.build_temporal_index()
        self.build_priority_index()
        
        # Create cross-domain mappings
        self.create_cross_domain_mappings()
        
        # Generate agent-specific knowledge structures
        self.generate_agent_knowledge_structures()
        
        # Create master intelligence catalog
        self.create_master_catalog()
        
        print(f"\nStructuring complete. Processed {total_insights} insights.")
        
    def process_t2_file(self, file_path: Path) -> int:
        """Process a single T2 file and distribute insights to agents"""
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        insights_processed = 0
        
        for insight in data.get('insights', []):
            # Enrich insight with metadata
            enriched_insight = self.enrich_insight(insight, str(file_path))
            
            # Determine agent assignments
            assigned_agents = self.assign_to_agents(enriched_insight)
            
            # Structure and save to each agent
            for agent in assigned_agents:
                self.save_to_agent(agent, enriched_insight)
                
            insights_processed += 1
            
        return insights_processed
    
    def enrich_insight(self, insight: Dict[str, Any], source_file: str) -> Dict[str, Any]:
        """Enrich insight with additional metadata and structure"""
        # Generate unique ID
        insight_id = self.generate_insight_id(insight)
        
        # Extract geographic scope
        geographic_scope = insight.get('geographic_scope', [])
        if not geographic_scope:
            # Try to extract from content
            geographic_scope = self.extract_geographic_scope(insight)
            
        # Determine temporal relevance
        temporal_relevance = insight.get('temporal_relevance', '')
        if not temporal_relevance:
            temporal_relevance = self.extract_temporal_relevance(insight)
            
        # Calculate priority score
        priority_score = self.calculate_priority_score(insight)
        
        # Structure the enriched insight
        enriched = {
            "id": insight_id,
            "timestamp": datetime.now().isoformat(),
            "source_file": source_file,
            "domain": insight.get('domain', 'general'),
            "category": insight.get('category', 'uncategorized'),
            "subcategory": insight.get('subcategory', ''),
            "title": insight.get('title', 'Untitled'),
            "content": self.structure_content(insight.get('content', {})),
            "tags": self.enhance_tags(insight.get('tags', [])),
            "geographic_scope": geographic_scope,
            "temporal_relevance": temporal_relevance,
            "priority_score": priority_score,
            "confidence_score": insight.get('confidence_score', 0.8),
            "data_points": self.structure_data_points(insight),
            "relationships": insight.get('relationships', []),
            "cross_references": [],
            "metadata": {
                "processing_date": datetime.now().isoformat(),
                "version": "1.0",
                "quality_score": self.calculate_quality_score(insight)
            }
        }
        
        return enriched
    
    def generate_insight_id(self, insight: Dict[str, Any]) -> str:
        """Generate unique ID for insight"""
        content = json.dumps(insight, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:12]
    
    def extract_geographic_scope(self, insight: Dict[str, Any]) -> List[str]:
        """Extract geographic scope from insight content"""
        scope = []
        content_str = json.dumps(insight).lower()
        
        # Houston neighborhoods and areas
        locations = [
            "houston", "houston heights", "katy", "sugar land", "the woodlands",
            "memorial", "river oaks", "montrose", "midtown", "downtown",
            "energy corridor", "galleria", "medical center", "tmc", "pearland",
            "cypress", "spring", "humble", "bellaire", "west university"
        ]
        
        for location in locations:
            if location in content_str:
                # Capitalize properly
                proper_name = ' '.join(word.capitalize() for word in location.split())
                if proper_name not in scope:
                    scope.append(proper_name)
                    
        return scope if scope else ["Houston"]
    
    def extract_temporal_relevance(self, insight: Dict[str, Any]) -> str:
        """Extract temporal relevance from insight"""
        content_str = json.dumps(insight).lower()
        
        # Look for year patterns
        year_pattern = re.findall(r'202[4-9]', content_str)
        if year_pattern:
            years = sorted(set(year_pattern))
            if len(years) == 1:
                return years[0]
            else:
                return f"{years[0]}-{years[-1]}"
                
        # Look for quarter references
        if 'q1' in content_str or 'q2' in content_str:
            return "2024-Q1Q2"
        elif 'q3' in content_str or 'q4' in content_str:
            return "2024-Q3Q4"
            
        # Default
        return "2024-2025"
    
    def calculate_priority_score(self, insight: Dict[str, Any]) -> float:
        """Calculate priority score for insight (0-1)"""
        score = 0.5  # Base score
        
        # Confidence factor
        confidence = insight.get('confidence_score', 0.8)
        score += confidence * 0.2
        
        # Content richness
        content = insight.get('content', {})
        if content.get('metrics'):
            score += 0.1
        if content.get('recommendations'):
            score += 0.15
        if content.get('key_findings') and len(content['key_findings']) > 2:
            score += 0.1
            
        # Domain importance
        domain = insight.get('domain', '')
        if any(keyword in domain for keyword in ['investment', 'roi', 'opportunity']):
            score += 0.1
        if any(keyword in domain for keyword in ['risk', 'flood', 'regulatory']):
            score += 0.05
            
        return min(score, 1.0)
    
    def structure_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Structure content for optimal querying"""
        structured = {
            "summary": content.get('summary', ''),
            "key_findings": content.get('key_findings', []),
            "metrics": content.get('metrics', {}),
            "recommendations": content.get('recommendations', []),
            "raw_data": content.get('raw_data', {})
        }
        
        # Ensure all metrics are properly typed
        for key, value in structured['metrics'].items():
            if isinstance(value, str):
                try:
                    # Try to convert to number
                    if '.' in value:
                        structured['metrics'][key] = float(value)
                    else:
                        structured['metrics'][key] = int(value)
                except:
                    pass
                    
        return structured
    
    def enhance_tags(self, tags: List[str]) -> List[str]:
        """Enhance tags with additional relevant keywords"""
        enhanced_tags = list(tags)
        
        # Add standardized tags
        tag_text = ' '.join(tags).lower()
        
        tag_mappings = {
            'investment': ['financial', 'roi', 'returns'],
            'development': ['construction', 'project', 'pipeline'],
            'risk': ['assessment', 'mitigation', 'analysis'],
            'market': ['trends', 'analysis', 'forecast'],
            'technology': ['innovation', 'smart', 'digital']
        }
        
        for base_tag, related_tags in tag_mappings.items():
            if base_tag in tag_text:
                for related in related_tags:
                    if related not in enhanced_tags:
                        enhanced_tags.append(related)
                        
        return enhanced_tags
    
    def structure_data_points(self, insight: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Structure data points for analysis"""
        data_points = []
        
        # Extract from metrics
        metrics = insight.get('content', {}).get('metrics', {})
        for metric_name, value in metrics.items():
            data_point = {
                "type": "metric",
                "name": metric_name,
                "value": value,
                "unit": self.infer_unit(metric_name, value),
                "timestamp": datetime.now().isoformat()
            }
            data_points.append(data_point)
            
        return data_points
    
    def infer_unit(self, metric_name: str, value: Any) -> str:
        """Infer unit from metric name and value"""
        name_lower = metric_name.lower()
        
        if 'percent' in name_lower or '_rate' in name_lower or 'growth' in name_lower:
            return 'percentage'
        elif 'price' in name_lower or 'cost' in name_lower or 'investment' in name_lower:
            return 'USD'
        elif 'sqft' in name_lower or 'square' in name_lower:
            return 'sqft'
        elif 'acres' in name_lower:
            return 'acres'
        elif 'days' in name_lower or 'months' in name_lower or 'years' in name_lower:
            return 'time'
        elif 'score' in name_lower or 'index' in name_lower:
            return 'index'
        else:
            return 'count'
    
    def calculate_quality_score(self, insight: Dict[str, Any]) -> float:
        """Calculate quality score for insight"""
        score = 0.0
        
        # Check completeness
        if insight.get('title'):
            score += 0.2
        if insight.get('content', {}).get('summary'):
            score += 0.2
        if insight.get('content', {}).get('key_findings'):
            score += 0.2
        if insight.get('content', {}).get('metrics'):
            score += 0.2
        if insight.get('tags'):
            score += 0.1
        if insight.get('confidence_score', 0) > 0.8:
            score += 0.1
            
        return score
    
    def assign_to_agents(self, insight: Dict[str, Any]) -> List[str]:
        """Determine which agents should receive this insight"""
        assigned_agents = []
        
        domain = insight['domain'].lower()
        tags = [t.lower() for t in insight['tags']]
        content_str = json.dumps(insight['content']).lower()
        
        for agent_name, agent_config in self.agent_domains.items():
            score = 0
            
            # Check primary domains
            if any(d in domain for d in agent_config['primary_domains']):
                score += 1.0
                
            # Check keywords
            keyword_matches = sum(1 for k in agent_config['keywords'] if k in content_str)
            score += keyword_matches * 0.1
            
            # Check tags
            tag_matches = sum(1 for t in tags if any(k in t for k in agent_config['keywords']))
            score += tag_matches * 0.2
            
            if score >= 0.3:
                assigned_agents.append(agent_name)
                
        # Ensure at least one assignment
        if not assigned_agents:
            # Default to Market Intelligence
            assigned_agents.append("Market_Intelligence")
            
        return assigned_agents
    
    def save_to_agent(self, agent_name: str, insight: Dict[str, Any]):
        """Save insight to agent's knowledge base"""
        agent_path = self.kb_path / agent_name
        agent_path.mkdir(exist_ok=True)
        
        # Determine knowledge file based on category
        category = insight['category'].replace(' ', '_').lower()
        kb_file = agent_path / f"{category}_knowledge.json"
        
        # Load existing knowledge
        knowledge = {}
        if kb_file.exists():
            with open(kb_file, 'r') as f:
                knowledge = json.load(f)
                
        # Add new insight
        knowledge[insight['id']] = insight
        
        # Save updated knowledge
        with open(kb_file, 'w') as f:
            json.dump(knowledge, f, indent=2)
            
        # Update agent metadata
        self.update_agent_metadata(agent_path)
        
        # Add to indexes
        self.add_to_indexes(agent_name, insight)
    
    def update_agent_metadata(self, agent_path: Path):
        """Update agent metadata"""
        metadata = {
            "agent_name": agent_path.name,
            "last_updated": datetime.now().isoformat(),
            "knowledge_files": [],
            "total_insights": 0,
            "categories": [],
            "geographic_coverage": [],
            "temporal_coverage": []
        }
        
        # Scan knowledge files
        for kb_file in agent_path.glob("*_knowledge.json"):
            with open(kb_file, 'r') as f:
                knowledge = json.load(f)
                
            metadata['knowledge_files'].append(kb_file.name)
            metadata['total_insights'] += len(knowledge)
            
            category = kb_file.stem.replace('_knowledge', '')
            if category not in metadata['categories']:
                metadata['categories'].append(category)
                
            # Collect geographic and temporal coverage
            for insight in knowledge.values():
                for geo in insight.get('geographic_scope', []):
                    if geo not in metadata['geographic_coverage']:
                        metadata['geographic_coverage'].append(geo)
                        
                temporal = insight.get('temporal_relevance', '')
                if temporal and temporal not in metadata['temporal_coverage']:
                    metadata['temporal_coverage'].append(temporal)
                    
        # Save metadata
        with open(agent_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def add_to_indexes(self, agent_name: str, insight: Dict[str, Any]):
        """Add insight to various indexes"""
        # Geographic index
        for geo in insight['geographic_scope']:
            self.geographic_index[geo].append({
                "agent": agent_name,
                "insight_id": insight['id'],
                "title": insight['title'],
                "priority": insight['priority_score']
            })
            
        # Temporal index
        temporal = insight['temporal_relevance']
        self.temporal_index[temporal].append({
            "agent": agent_name,
            "insight_id": insight['id'],
            "title": insight['title'],
            "priority": insight['priority_score']
        })
        
        # Priority index
        if insight['priority_score'] >= 0.8:
            priority_level = "high"
        elif insight['priority_score'] >= 0.6:
            priority_level = "medium"
        else:
            priority_level = "low"
            
        self.priority_index[priority_level].append({
            "agent": agent_name,
            "insight_id": insight['id'],
            "title": insight['title'],
            "score": insight['priority_score']
        })
    
    def build_geographic_index(self):
        """Build comprehensive geographic index"""
        print("Building geographic index...")
        
        # Save geographic index
        geo_index_path = self.kb_path / "geographic_index.json"
        
        # Sort each location's insights by priority
        sorted_index = {}
        for location, insights in self.geographic_index.items():
            sorted_insights = sorted(insights, key=lambda x: x['priority'], reverse=True)
            sorted_index[location] = {
                "total_insights": len(sorted_insights),
                "insights": sorted_insights[:20]  # Top 20 per location
            }
            
        with open(geo_index_path, 'w') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "locations": sorted_index
            }, f, indent=2)
            
        print(f"Geographic index created with {len(sorted_index)} locations")
    
    def build_temporal_index(self):
        """Build comprehensive temporal index"""
        print("Building temporal index...")
        
        # Save temporal index
        temporal_index_path = self.kb_path / "temporal_index.json"
        
        # Sort by time period
        sorted_index = {}
        for period, insights in sorted(self.temporal_index.items()):
            sorted_insights = sorted(insights, key=lambda x: x['priority'], reverse=True)
            sorted_index[period] = {
                "total_insights": len(sorted_insights),
                "insights": sorted_insights
            }
            
        with open(temporal_index_path, 'w') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "periods": sorted_index
            }, f, indent=2)
            
        print(f"Temporal index created with {len(sorted_index)} time periods")
    
    def build_priority_index(self):
        """Build priority-based index"""
        print("Building priority index...")
        
        # Save priority index
        priority_index_path = self.kb_path / "priority_index.json"
        
        # Sort insights within each priority level
        sorted_index = {}
        for level in ["high", "medium", "low"]:
            if level in self.priority_index:
                sorted_insights = sorted(
                    self.priority_index[level], 
                    key=lambda x: x['score'], 
                    reverse=True
                )
                sorted_index[level] = {
                    "total_insights": len(sorted_insights),
                    "insights": sorted_insights
                }
                
        with open(priority_index_path, 'w') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "priority_levels": sorted_index
            }, f, indent=2)
            
        print(f"Priority index created")
    
    def create_cross_domain_mappings(self):
        """Create mappings between related insights across domains"""
        print("Creating cross-domain mappings...")
        
        # Scan all agent knowledge bases
        all_insights = {}
        
        for agent_dir in self.kb_path.iterdir():
            if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
                for kb_file in agent_dir.glob("*_knowledge.json"):
                    with open(kb_file, 'r') as f:
                        knowledge = json.load(f)
                        
                    for insight_id, insight in knowledge.items():
                        all_insights[insight_id] = {
                            "agent": agent_dir.name,
                            "insight": insight
                        }
        
        # Find relationships
        relationships = []
        insights_list = list(all_insights.items())
        
        for i, (id1, data1) in enumerate(insights_list):
            for j, (id2, data2) in enumerate(insights_list[i+1:], i+1):
                if data1['agent'] != data2['agent']:
                    # Check for relationships
                    relationship_score = self.calculate_relationship_score(
                        data1['insight'], 
                        data2['insight']
                    )
                    
                    if relationship_score > 0.3:
                        relationships.append({
                            "source": {
                                "id": id1,
                                "agent": data1['agent'],
                                "title": data1['insight']['title']
                            },
                            "target": {
                                "id": id2,
                                "agent": data2['agent'],
                                "title": data2['insight']['title']
                            },
                            "score": relationship_score,
                            "type": self.determine_relationship_type(data1['insight'], data2['insight'])
                        })
        
        # Save cross-domain mappings
        mappings_path = self.kb_path / "cross_domain_mappings.json"
        with open(mappings_path, 'w') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total_relationships": len(relationships),
                "relationships": sorted(relationships, key=lambda x: x['score'], reverse=True)[:100]
            }, f, indent=2)
            
        print(f"Created {len(relationships)} cross-domain relationships")
    
    def calculate_relationship_score(self, insight1: Dict[str, Any], insight2: Dict[str, Any]) -> float:
        """Calculate relationship score between two insights"""
        score = 0.0
        
        # Geographic overlap
        geo1 = set(insight1['geographic_scope'])
        geo2 = set(insight2['geographic_scope'])
        if geo1 & geo2:
            score += 0.3
            
        # Tag overlap
        tags1 = set(insight1['tags'])
        tags2 = set(insight2['tags'])
        common_tags = tags1 & tags2
        if common_tags:
            score += len(common_tags) * 0.1
            
        # Temporal alignment
        if insight1['temporal_relevance'] == insight2['temporal_relevance']:
            score += 0.2
            
        # Domain complementarity
        domain1 = insight1['domain']
        domain2 = insight2['domain']
        if self.are_domains_complementary(domain1, domain2):
            score += 0.3
            
        return min(score, 1.0)
    
    def are_domains_complementary(self, domain1: str, domain2: str) -> bool:
        """Check if two domains are complementary"""
        complementary_pairs = [
            ('flood_risk', 'financing'),
            ('zoning', 'development'),
            ('market', 'investment'),
            ('environmental', 'regulatory'),
            ('technology', 'market'),
            ('neighborhood', 'investment')
        ]
        
        for pair in complementary_pairs:
            if (pair[0] in domain1 and pair[1] in domain2) or \
               (pair[1] in domain1 and pair[0] in domain2):
                return True
                
        return False
    
    def determine_relationship_type(self, insight1: Dict[str, Any], insight2: Dict[str, Any]) -> str:
        """Determine the type of relationship between insights"""
        domain1 = insight1['domain']
        domain2 = insight2['domain']
        
        if 'risk' in domain1 and 'mitigation' in domain2:
            return "risk_mitigation"
        elif 'market' in domain1 and 'investment' in domain2:
            return "investment_opportunity"
        elif 'regulatory' in domain1 and 'development' in domain2:
            return "regulatory_impact"
        elif 'environmental' in domain1 and 'financial' in domain2:
            return "environmental_financial"
        else:
            return "general_correlation"
    
    def generate_agent_knowledge_structures(self):
        """Generate structured knowledge for each agent"""
        print("\nGenerating agent knowledge structures...")
        
        for agent_name in self.agent_domains.keys():
            agent_path = self.kb_path / agent_name
            if agent_path.exists():
                # Create domain expertise summary
                self.create_agent_expertise_summary(agent_name, agent_path)
                
                # Create quick reference guide
                self.create_agent_quick_reference(agent_name, agent_path)
    
    def create_agent_expertise_summary(self, agent_name: str, agent_path: Path):
        """Create expertise summary for agent"""
        expertise = {
            "agent_name": agent_name,
            "generated_at": datetime.now().isoformat(),
            "primary_domains": self.agent_domains[agent_name]['primary_domains'],
            "expertise_areas": [],
            "key_insights": [],
            "geographic_expertise": {},
            "temporal_focus": {}
        }
        
        # Analyze all knowledge files
        for kb_file in agent_path.glob("*_knowledge.json"):
            with open(kb_file, 'r') as f:
                knowledge = json.load(f)
                
            category = kb_file.stem.replace('_knowledge', '')
            
            # Collect high-priority insights
            high_priority = [
                insight for insight in knowledge.values() 
                if insight['priority_score'] >= 0.8
            ]
            
            if high_priority:
                expertise['expertise_areas'].append({
                    "category": category,
                    "insight_count": len(knowledge),
                    "high_priority_count": len(high_priority),
                    "top_insights": [
                        {
                            "title": hp['title'],
                            "priority": hp['priority_score'],
                            "summary": hp['content']['summary']
                        } for hp in high_priority[:3]
                    ]
                })
        
        # Save expertise summary
        with open(agent_path / "expertise_summary.json", 'w') as f:
            json.dump(expertise, f, indent=2)
    
    def create_agent_quick_reference(self, agent_name: str, agent_path: Path):
        """Create quick reference guide for agent"""
        quick_ref = {
            "agent_name": agent_name,
            "generated_at": datetime.now().isoformat(),
            "query_examples": self.generate_query_examples(agent_name),
            "key_metrics": {},
            "top_recommendations": [],
            "critical_insights": []
        }
        
        # Collect key metrics and recommendations
        for kb_file in agent_path.glob("*_knowledge.json"):
            with open(kb_file, 'r') as f:
                knowledge = json.load(f)
                
            for insight in knowledge.values():
                # Collect metrics
                for metric, value in insight['content'].get('metrics', {}).items():
                    if metric not in quick_ref['key_metrics']:
                        quick_ref['key_metrics'][metric] = {
                            "values": [],
                            "unit": insight['data_points'][0]['unit'] if insight['data_points'] else "unknown"
                        }
                    quick_ref['key_metrics'][metric]['values'].append(value)
                    
                # Collect recommendations
                for rec in insight['content'].get('recommendations', []):
                    quick_ref['top_recommendations'].append({
                        "recommendation": rec,
                        "source": insight['title'],
                        "priority": insight['priority_score']
                    })
        
        # Sort and limit
        quick_ref['top_recommendations'] = sorted(
            quick_ref['top_recommendations'], 
            key=lambda x: x['priority'], 
            reverse=True
        )[:10]
        
        # Save quick reference
        with open(agent_path / "quick_reference.json", 'w') as f:
            json.dump(quick_ref, f, indent=2)
    
    def generate_query_examples(self, agent_name: str) -> List[str]:
        """Generate example queries for agent"""
        query_templates = {
            "Market_Intelligence": [
                "What are the current market trends in [area]?",
                "Show me price forecasts for residential properties",
                "What is the competitive landscape for developers?",
                "Which areas show the highest growth potential?"
            ],
            "Neighborhood_Intelligence": [
                "What is the investment score for [neighborhood]?",
                "Show demographic trends in [area]",
                "Which neighborhoods have the best infrastructure?",
                "What are the growth indicators for [location]?"
            ],
            "Financial_Intelligence": [
                "What ROI can I expect for mixed-use development?",
                "Show me current financing options",
                "What are the tax implications for opportunity zones?",
                "How do lending rates impact project viability?"
            ],
            "Environmental_Intelligence": [
                "What flood risks affect [area]?",
                "Show environmental compliance requirements",
                "What are the sustainability metrics for development?",
                "How does air quality impact property values?"
            ],
            "Regulatory_Intelligence": [
                "What are the current zoning regulations for [area]?",
                "Show me the permit process for commercial development",
                "What regulatory changes are coming?",
                "How long does approval typically take?"
            ],
            "Technology_Innovation_Intelligence": [
                "Which innovation districts are most active?",
                "Show smart city initiatives in Houston",
                "What PropTech solutions are being adopted?",
                "How is technology impacting development?"
            ]
        }
        
        return query_templates.get(agent_name, [])
    
    def create_master_catalog(self):
        """Create master catalog of all intelligence"""
        print("Creating master intelligence catalog...")
        
        catalog = {
            "generated_at": datetime.now().isoformat(),
            "total_insights": 0,
            "agents": {},
            "geographic_coverage": list(self.geographic_index.keys()),
            "temporal_coverage": list(self.temporal_index.keys()),
            "high_priority_insights": [],
            "cross_domain_opportunities": []
        }
        
        # Collect statistics from each agent
        for agent_dir in self.kb_path.iterdir():
            if agent_dir.is_dir() and agent_dir.name in self.agent_domains:
                agent_stats = {
                    "total_insights": 0,
                    "categories": [],
                    "high_priority_count": 0
                }
                
                for kb_file in agent_dir.glob("*_knowledge.json"):
                    with open(kb_file, 'r') as f:
                        knowledge = json.load(f)
                        
                    agent_stats['total_insights'] += len(knowledge)
                    category = kb_file.stem.replace('_knowledge', '')
                    agent_stats['categories'].append(category)
                    
                    # Count high priority
                    high_priority = sum(
                        1 for insight in knowledge.values() 
                        if insight['priority_score'] >= 0.8
                    )
                    agent_stats['high_priority_count'] += high_priority
                    
                catalog['agents'][agent_dir.name] = agent_stats
                catalog['total_insights'] += agent_stats['total_insights']
        
        # Add high priority insights
        if 'high' in self.priority_index:
            catalog['high_priority_insights'] = self.priority_index['high'][:20]
            
        # Save master catalog
        with open(self.kb_path / "master_catalog.json", 'w') as f:
            json.dump(catalog, f, indent=2)
            
        print(f"Master catalog created with {catalog['total_insights']} total insights")


def main():
    print("Knowledge Structuring System v2.0")
    print("=" * 50)
    
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    structurer = KnowledgeStructurer(base_path)
    
    # Run comprehensive structuring
    structurer.structure_all_knowledge()
    
    print("\nKnowledge structuring complete!")
    print("Agent knowledge bases are ready for query processing.")


if __name__ == "__main__":
    main()
