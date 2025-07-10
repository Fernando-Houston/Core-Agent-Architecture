#!/usr/bin/env python3
"""
Fix existing knowledge bases and complete structuring
"""

import json
from pathlib import Path
from datetime import datetime
import sys
from typing import Dict, Any

sys.path.append('/Users/fernandox/Desktop/Core Agent Architecture/T3_Agent_Population_Engine')
from knowledge_structurer_v2 import KnowledgeStructurer


def fix_existing_knowledge(kb_path: Path):
    """Fix existing knowledge files by adding missing fields"""
    print("Fixing existing knowledge files...")
    
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
            print(f"  Checking {agent_dir.name}...")
            
            for kb_file in agent_dir.glob("*_knowledge.json"):
                try:
                    with open(kb_file, 'r') as f:
                        knowledge = json.load(f)
                    
                    modified = False
                    
                    for insight_id, insight in knowledge.items():
                        # Add missing priority_score
                        if 'priority_score' not in insight:
                            # Calculate based on available data
                            score = 0.5
                            if insight.get('confidence_score', 0) > 0.8:
                                score += 0.2
                            if insight.get('content', {}).get('metrics'):
                                score += 0.1
                            if insight.get('content', {}).get('recommendations'):
                                score += 0.15
                            
                            insight['priority_score'] = min(score, 1.0)
                            modified = True
                        
                        # Add missing data_points if needed
                        if 'data_points' not in insight or not insight['data_points']:
                            insight['data_points'] = []
                            # Extract from metrics if available
                            metrics = insight.get('content', {}).get('metrics', {})
                            for metric_name, value in metrics.items():
                                insight['data_points'].append({
                                    "type": "metric",
                                    "name": metric_name,
                                    "value": value,
                                    "unit": infer_unit(metric_name),
                                    "timestamp": insight.get('timestamp', datetime.now().isoformat())
                                })
                            modified = True
                        
                        # Add missing metadata
                        if 'metadata' not in insight:
                            insight['metadata'] = {
                                "processing_date": insight.get('timestamp', datetime.now().isoformat()),
                                "version": "1.0",
                                "quality_score": calculate_quality_score(insight)
                            }
                            modified = True
                        
                        # Ensure geographic_scope is a list
                        if 'geographic_scope' in insight and isinstance(insight['geographic_scope'], str):
                            insight['geographic_scope'] = [insight['geographic_scope']]
                            modified = True
                        elif 'geographic_scope' not in insight:
                            insight['geographic_scope'] = ["Houston"]
                            modified = True
                        
                        # Ensure temporal_relevance exists
                        if 'temporal_relevance' not in insight:
                            insight['temporal_relevance'] = "2024-2025"
                            modified = True
                    
                    if modified:
                        # Save fixed knowledge
                        with open(kb_file, 'w') as f:
                            json.dump(knowledge, f, indent=2)
                        print(f"    Fixed {kb_file.name}")
                        
                except Exception as e:
                    print(f"    Error processing {kb_file}: {e}")


def infer_unit(metric_name: str) -> str:
    """Infer unit from metric name"""
    name_lower = metric_name.lower()
    
    if 'percent' in name_lower or 'rate' in name_lower:
        return 'percentage'
    elif 'price' in name_lower or 'cost' in name_lower:
        return 'USD'
    elif 'sqft' in name_lower:
        return 'sqft'
    elif 'months' in name_lower or 'days' in name_lower:
        return 'time'
    elif 'score' in name_lower or 'index' in name_lower:
        return 'index'
    else:
        return 'count'


def calculate_quality_score(insight: Dict[str, Any]) -> float:
    """Calculate quality score for insight"""
    score = 0.0
    
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


def complete_structuring():
    """Complete the knowledge structuring process"""
    print("\nCompleting knowledge structuring...")
    
    base_path = Path("/Users/fernandox/Desktop/Core Agent Architecture")
    
    # Create the indexes and structures
    print("\nCreating comprehensive indexes...")
    
    # Geographic index
    create_geographic_index(base_path)
    
    # Temporal index
    create_temporal_index(base_path)
    
    # Priority index
    create_priority_index(base_path)
    
    # Cross-domain mappings
    create_cross_domain_mappings(base_path)
    
    # Agent expertise summaries
    create_agent_summaries(base_path)
    
    # Master catalog
    create_master_catalog(base_path)
    
    print("\nKnowledge structuring complete!")


def create_geographic_index(base_path: Path):
    """Create geographic index"""
    kb_path = base_path / "Agent_Knowledge_Bases"
    geo_index = {}
    
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
            for kb_file in agent_dir.glob("*_knowledge.json"):
                with open(kb_file, 'r') as f:
                    knowledge = json.load(f)
                    
                for insight_id, insight in knowledge.items():
                    for geo in insight.get('geographic_scope', ['Houston']):
                        if geo not in geo_index:
                            geo_index[geo] = []
                        
                        geo_index[geo].append({
                            "agent": agent_dir.name,
                            "insight_id": insight_id,
                            "title": insight['title'],
                            "priority": insight.get('priority_score', 0.5)
                        })
    
    # Sort and save
    sorted_index = {}
    for location, insights in sorted(geo_index.items()):
        sorted_insights = sorted(insights, key=lambda x: x['priority'], reverse=True)
        sorted_index[location] = {
            "total_insights": len(sorted_insights),
            "insights": sorted_insights[:20]
        }
    
    with open(kb_path / "geographic_index.json", 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "locations": sorted_index
        }, f, indent=2)
    
    print(f"  Geographic index created with {len(sorted_index)} locations")


def create_temporal_index(base_path: Path):
    """Create temporal index"""
    kb_path = base_path / "Agent_Knowledge_Bases"
    temporal_index = {}
    
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
            for kb_file in agent_dir.glob("*_knowledge.json"):
                with open(kb_file, 'r') as f:
                    knowledge = json.load(f)
                    
                for insight_id, insight in knowledge.items():
                    temporal = insight.get('temporal_relevance', '2024-2025')
                    if temporal not in temporal_index:
                        temporal_index[temporal] = []
                    
                    temporal_index[temporal].append({
                        "agent": agent_dir.name,
                        "insight_id": insight_id,
                        "title": insight['title'],
                        "priority": insight.get('priority_score', 0.5)
                    })
    
    # Sort and save
    sorted_index = {}
    for period, insights in sorted(temporal_index.items()):
        sorted_insights = sorted(insights, key=lambda x: x['priority'], reverse=True)
        sorted_index[period] = {
            "total_insights": len(sorted_insights),
            "insights": sorted_insights
        }
    
    with open(kb_path / "temporal_index.json", 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "periods": sorted_index
        }, f, indent=2)
    
    print(f"  Temporal index created with {len(sorted_index)} time periods")


def create_priority_index(base_path: Path):
    """Create priority index"""
    kb_path = base_path / "Agent_Knowledge_Bases"
    priority_index = {"high": [], "medium": [], "low": []}
    
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
            for kb_file in agent_dir.glob("*_knowledge.json"):
                with open(kb_file, 'r') as f:
                    knowledge = json.load(f)
                    
                for insight_id, insight in knowledge.items():
                    priority = insight.get('priority_score', 0.5)
                    
                    if priority >= 0.8:
                        level = "high"
                    elif priority >= 0.6:
                        level = "medium"
                    else:
                        level = "low"
                    
                    priority_index[level].append({
                        "agent": agent_dir.name,
                        "insight_id": insight_id,
                        "title": insight['title'],
                        "score": priority
                    })
    
    # Sort within each level
    sorted_index = {}
    for level in ["high", "medium", "low"]:
        sorted_insights = sorted(priority_index[level], key=lambda x: x['score'], reverse=True)
        sorted_index[level] = {
            "total_insights": len(sorted_insights),
            "insights": sorted_insights
        }
    
    with open(kb_path / "priority_index.json", 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "priority_levels": sorted_index
        }, f, indent=2)
    
    print(f"  Priority index created")


def create_cross_domain_mappings(base_path: Path):
    """Create simplified cross-domain mappings"""
    kb_path = base_path / "Agent_Knowledge_Bases"
    
    # Count domain overlaps
    domain_connections = {}
    
    # Get all insights
    all_insights = []
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
            for kb_file in agent_dir.glob("*_knowledge.json"):
                with open(kb_file, 'r') as f:
                    knowledge = json.load(f)
                for insight_id, insight in knowledge.items():
                    all_insights.append({
                        "id": insight_id,
                        "agent": agent_dir.name,
                        "tags": insight.get('tags', []),
                        "geographic_scope": insight.get('geographic_scope', []),
                        "title": insight['title']
                    })
    
    # Find connections
    connections = []
    for i in range(len(all_insights)):
        for j in range(i+1, len(all_insights)):
            if all_insights[i]['agent'] != all_insights[j]['agent']:
                # Check for common tags or geography
                common_tags = set(all_insights[i]['tags']) & set(all_insights[j]['tags'])
                common_geo = set(all_insights[i]['geographic_scope']) & set(all_insights[j]['geographic_scope'])
                
                if len(common_tags) >= 2 or (common_geo and len(common_tags) >= 1):
                    connections.append({
                        "source": {
                            "id": all_insights[i]['id'],
                            "agent": all_insights[i]['agent'],
                            "title": all_insights[i]['title']
                        },
                        "target": {
                            "id": all_insights[j]['id'],
                            "agent": all_insights[j]['agent'],
                            "title": all_insights[j]['title']
                        },
                        "common_tags": list(common_tags),
                        "common_locations": list(common_geo)
                    })
    
    with open(kb_path / "cross_domain_mappings.json", 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_relationships": len(connections),
            "relationships": connections[:100]  # Top 100
        }, f, indent=2)
    
    print(f"  Created {len(connections)} cross-domain relationships")


def create_agent_summaries(base_path: Path):
    """Create expertise summaries for each agent"""
    kb_path = base_path / "Agent_Knowledge_Bases"
    
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
            summary = {
                "agent_name": agent_dir.name,
                "generated_at": datetime.now().isoformat(),
                "total_insights": 0,
                "categories": {},
                "top_insights": []
            }
            
            all_insights = []
            
            for kb_file in agent_dir.glob("*_knowledge.json"):
                with open(kb_file, 'r') as f:
                    knowledge = json.load(f)
                
                category = kb_file.stem.replace('_knowledge', '')
                summary['categories'][category] = len(knowledge)
                summary['total_insights'] += len(knowledge)
                
                for insight in knowledge.values():
                    all_insights.append(insight)
            
            # Get top insights by priority
            top_insights = sorted(all_insights, key=lambda x: x.get('priority_score', 0), reverse=True)[:5]
            summary['top_insights'] = [
                {
                    "title": i['title'],
                    "priority": i.get('priority_score', 0),
                    "summary": i.get('content', {}).get('summary', '')
                } for i in top_insights
            ]
            
            with open(agent_dir / "expertise_summary.json", 'w') as f:
                json.dump(summary, f, indent=2)
    
    print("  Created agent expertise summaries")


def create_master_catalog(base_path: Path):
    """Create master catalog"""
    kb_path = base_path / "Agent_Knowledge_Bases"
    
    catalog = {
        "generated_at": datetime.now().isoformat(),
        "total_insights": 0,
        "agents": {},
        "geographic_coverage": set(),
        "temporal_coverage": set(),
        "high_priority_count": 0
    }
    
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
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
                
                for insight in knowledge.values():
                    if insight.get('priority_score', 0) >= 0.8:
                        agent_stats['high_priority_count'] += 1
                        catalog['high_priority_count'] += 1
                    
                    catalog['geographic_coverage'].update(insight.get('geographic_scope', []))
                    catalog['temporal_coverage'].add(insight.get('temporal_relevance', '2024-2025'))
            
            catalog['agents'][agent_dir.name] = agent_stats
            catalog['total_insights'] += agent_stats['total_insights']
    
    # Convert sets to lists for JSON
    catalog['geographic_coverage'] = sorted(list(catalog['geographic_coverage']))
    catalog['temporal_coverage'] = sorted(list(catalog['temporal_coverage']))
    
    with open(kb_path / "master_catalog.json", 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"  Master catalog created with {catalog['total_insights']} total insights")


def main():
    print("Knowledge Structure Fix and Complete")
    print("=" * 50)
    
    base_path = Path("/Users/fernandox/Desktop/Core Agent Architecture")
    kb_path = base_path / "Agent_Knowledge_Bases"
    
    # First, fix existing knowledge
    fix_existing_knowledge(kb_path)
    
    # Then complete structuring
    complete_structuring()
    
    print("\nAll knowledge bases are now properly structured!")
    print("Ready for comprehensive query processing.")


if __name__ == "__main__":
    main()
