#!/usr/bin/env python3
"""
Cross-Domain Intelligence Enrichment
Links intelligence across domains for comprehensive insights
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any


class CrossDomainEnricher:
    """Enriches intelligence with cross-domain connections"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.kb_path = self.base_path / "Agent_Knowledge_Bases"
        self.enrichment_path = self.kb_path / "Cross_Domain_Intelligence"
        self.enrichment_path.mkdir(exist_ok=True)
        
    def analyze_cross_domain_patterns(self):
        """Analyze patterns across all agent knowledge bases"""
        print("Analyzing cross-domain patterns...\n")
        
        # Load all intelligence records
        all_records = self.load_all_records()
        
        # Find cross-domain connections
        connections = {
            "geographic_connections": self.find_geographic_connections(all_records),
            "topic_connections": self.find_topic_connections(all_records),
            "value_chain_connections": self.find_value_chain_connections(all_records),
            "risk_opportunity_pairs": self.find_risk_opportunity_pairs(all_records)
        }
        
        # Generate insights
        insights = self.generate_cross_domain_insights(connections, all_records)
        
        # Save enriched intelligence
        self.save_enriched_intelligence(connections, insights)
        
        return connections, insights
    
    def load_all_records(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load all records from agent knowledge bases"""
        all_records = defaultdict(list)
        
        for agent_dir in self.kb_path.iterdir():
            if agent_dir.is_dir() and agent_dir.name != "Cross_Domain_Intelligence":
                agent_name = agent_dir.name
                
                for kb_file in agent_dir.glob("*_knowledge.json"):
                    try:
                        with open(kb_file, 'r') as f:
                            knowledge = json.load(f)
                            
                        for record_id, record in knowledge.items():
                            record['agent'] = agent_name
                            record['kb_file'] = kb_file.name
                            all_records[agent_name].append(record)
                    except:
                        pass
                        
        return dict(all_records)
    
    def find_geographic_connections(self, records: Dict[str, List[Dict]]) -> List[Dict]:
        """Find connections based on geographic overlap"""
        connections = []
        geo_index = defaultdict(list)
        
        # Build geographic index
        for agent, agent_records in records.items():
            for record in agent_records:
                for geo in record.get('geographic_scope', ['Houston']):
                    geo_index[geo].append({
                        'agent': agent,
                        'record': record
                    })
        
        # Find multi-agent geographic overlaps
        for geo, entries in geo_index.items():
            agents = set(e['agent'] for e in entries)
            if len(agents) > 1:
                connection = {
                    'type': 'geographic',
                    'location': geo,
                    'agents': list(agents),
                    'record_count': len(entries),
                    'insights': self.extract_geo_insights(geo, entries)
                }
                connections.append(connection)
                
        return connections
    
    def find_topic_connections(self, records: Dict[str, List[Dict]]) -> List[Dict]:
        """Find connections based on topic overlap"""
        connections = []
        tag_index = defaultdict(list)
        
        # Build tag index
        for agent, agent_records in records.items():
            for record in agent_records:
                for tag in record.get('tags', []):
                    tag_index[tag].append({
                        'agent': agent,
                        'record': record
                    })
        
        # Find multi-agent topic overlaps
        for tag, entries in tag_index.items():
            agents = set(e['agent'] for e in entries)
            if len(agents) > 1:
                connection = {
                    'type': 'topic',
                    'tag': tag,
                    'agents': list(agents),
                    'record_count': len(entries),
                    'cross_domain_value': self.assess_topic_value(tag, entries)
                }
                connections.append(connection)
                
        return connections
    
    def find_value_chain_connections(self, records: Dict[str, List[Dict]]) -> List[Dict]:
        """Find connections in the development value chain"""
        value_chains = []
        
        # Define value chain patterns
        chain_patterns = [
            {
                'name': 'Development Pipeline',
                'sequence': ['zoning', 'financing', 'construction', 'market'],
                'agents': ['Regulatory_Intelligence', 'Financial_Intelligence', 
                          'Technology_Innovation_Intelligence', 'Market_Intelligence']
            },
            {
                'name': 'Risk Management Chain',
                'sequence': ['environmental', 'regulatory', 'financial', 'market'],
                'agents': ['Environmental_Intelligence', 'Regulatory_Intelligence',
                          'Financial_Intelligence', 'Market_Intelligence']
            },
            {
                'name': 'Innovation Impact Chain',
                'sequence': ['technology', 'development', 'neighborhood', 'value'],
                'agents': ['Technology_Innovation_Intelligence', 'Market_Intelligence',
                          'Neighborhood_Intelligence', 'Financial_Intelligence']
            }
        ]
        
        for pattern in chain_patterns:
            chain_records = []
            for agent in pattern['agents']:
                if agent in records:
                    relevant = [r for r in records[agent] 
                               if any(s in str(r).lower() for s in pattern['sequence'])]
                    if relevant:
                        chain_records.append({
                            'agent': agent,
                            'records': relevant[:2]  # Top 2 relevant records
                        })
            
            if len(chain_records) >= 3:  # At least 3 agents in chain
                value_chains.append({
                    'type': 'value_chain',
                    'name': pattern['name'],
                    'agents_involved': [c['agent'] for c in chain_records],
                    'chain_strength': len(chain_records) / len(pattern['agents']),
                    'insights': self.extract_chain_insights(pattern['name'], chain_records)
                })
                
        return value_chains
    
    def find_risk_opportunity_pairs(self, records: Dict[str, List[Dict]]) -> List[Dict]:
        """Find paired risks and opportunities"""
        pairs = []
        
        # Extract risks and opportunities
        risks = []
        opportunities = []
        
        for agent, agent_records in records.items():
            for record in agent_records:
                content_str = str(record.get('content', {})).lower()
                title = record.get('title', '').lower()
                
                if 'risk' in content_str or 'risk' in title:
                    risks.append({'agent': agent, 'record': record})
                if 'opportunity' in content_str or 'opportunity' in title:
                    opportunities.append({'agent': agent, 'record': record})
        
        # Match risks with mitigation opportunities
        for risk in risks:
            risk_domain = risk['record'].get('domain', '')
            risk_geo = risk['record'].get('geographic_scope', [])
            
            for opp in opportunities:
                opp_domain = opp['record'].get('domain', '')
                opp_geo = opp['record'].get('geographic_scope', [])
                
                # Check for relationship
                if (self.domains_related(risk_domain, opp_domain) or 
                    any(g in opp_geo for g in risk_geo)):
                    
                    pairs.append({
                        'type': 'risk_opportunity',
                        'risk': {
                            'agent': risk['agent'],
                            'title': risk['record'].get('title', ''),
                            'domain': risk_domain
                        },
                        'opportunity': {
                            'agent': opp['agent'],
                            'title': opp['record'].get('title', ''),
                            'domain': opp_domain
                        },
                        'connection_strength': self.calculate_connection_strength(
                            risk['record'], opp['record']
                        )
                    })
                    
        return pairs
    
    def extract_geo_insights(self, location: str, entries: List[Dict]) -> List[str]:
        """Extract insights for a geographic area"""
        insights = []
        
        # Count agent perspectives
        agent_counts = defaultdict(int)
        for entry in entries:
            agent_counts[entry['agent']] += 1
            
        insights.append(f"{len(agent_counts)} different intelligence domains active in {location}")
        
        # Look for specific patterns
        has_market = any('Market' in e['agent'] for e in entries)
        has_env = any('Environmental' in e['agent'] for e in entries)
        has_tech = any('Technology' in e['agent'] for e in entries)
        
        if has_market and has_tech:
            insights.append(f"{location} shows tech-driven market growth potential")
        if has_env and has_market:
            insights.append(f"Environmental factors may impact {location} development")
            
        return insights
    
    def assess_topic_value(self, tag: str, entries: List[Dict]) -> str:
        """Assess the value of a cross-domain topic"""
        agent_count = len(set(e['agent'] for e in entries))
        
        if agent_count >= 4:
            return "Critical - affects multiple domains"
        elif agent_count >= 3:
            return "High - significant cross-domain impact"
        elif agent_count >= 2:
            return "Medium - notable cross-domain relevance"
        else:
            return "Low - limited cross-domain impact"
    
    def extract_chain_insights(self, chain_name: str, chain_records: List[Dict]) -> List[str]:
        """Extract insights from value chain analysis"""
        insights = []
        
        if chain_name == 'Development Pipeline':
            insights.append("Complete development intelligence from zoning to market")
            if len(chain_records) == 4:
                insights.append("All critical development stages covered")
                
        elif chain_name == 'Risk Management Chain':
            insights.append("Comprehensive risk assessment across domains")
            insights.append("Enables proactive risk mitigation strategies")
            
        elif chain_name == 'Innovation Impact Chain':
            insights.append("Technology adoption driving neighborhood transformation")
            insights.append("Innovation creating measurable value increases")
            
        return insights
    
    def domains_related(self, domain1: str, domain2: str) -> bool:
        """Check if two domains are related"""
        relations = {
            'flood': ['environmental', 'risk', 'insurance'],
            'zoning': ['regulatory', 'development', 'opportunity'],
            'financing': ['investment', 'roi', 'tax'],
            'technology': ['innovation', 'smart', 'efficiency']
        }
        
        for key, related in relations.items():
            if key in domain1.lower() and any(r in domain2.lower() for r in related):
                return True
            if key in domain2.lower() and any(r in domain1.lower() for r in related):
                return True
                
        return False
    
    def calculate_connection_strength(self, record1: Dict, record2: Dict) -> float:
        """Calculate strength of connection between records"""
        strength = 0.0
        
        # Geographic overlap
        geo1 = set(record1.get('geographic_scope', []))
        geo2 = set(record2.get('geographic_scope', []))
        if geo1 & geo2:
            strength += 0.3
            
        # Tag overlap
        tags1 = set(record1.get('tags', []))
        tags2 = set(record2.get('tags', []))
        tag_overlap = len(tags1 & tags2) / max(len(tags1 | tags2), 1)
        strength += tag_overlap * 0.4
        
        # Temporal alignment
        if record1.get('temporal_relevance') == record2.get('temporal_relevance'):
            strength += 0.3
            
        return min(strength, 1.0)
    
    def generate_cross_domain_insights(self, connections: Dict, records: Dict) -> List[Dict]:
        """Generate high-level cross-domain insights"""
        insights = []
        
        # Geographic concentration insights
        geo_conns = connections['geographic_connections']
        if geo_conns:
            top_locations = sorted(geo_conns, key=lambda x: x['record_count'], reverse=True)[:3]
            for loc in top_locations:
                insights.append({
                    'type': 'geographic_concentration',
                    'title': f"Multi-domain activity in {loc['location']}",
                    'description': f"{loc['record_count']} intelligence records across {len(loc['agents'])} domains",
                    'implications': loc['insights'],
                    'priority': 'high' if loc['record_count'] > 5 else 'medium'
                })
        
        # Value chain insights
        for chain in connections['value_chain_connections']:
            insights.append({
                'type': 'value_chain',
                'title': chain['name'],
                'description': f"Connected intelligence across {len(chain['agents_involved'])} agents",
                'implications': chain['insights'],
                'priority': 'high' if chain['chain_strength'] > 0.75 else 'medium'
            })
        
        # Risk-opportunity insights
        risk_opps = connections['risk_opportunity_pairs']
        if risk_opps:
            high_strength = [ro for ro in risk_opps if ro['connection_strength'] > 0.7]
            for ro in high_strength[:5]:
                insights.append({
                    'type': 'risk_opportunity_pair',
                    'title': f"Risk mitigation opportunity identified",
                    'description': f"{ro['risk']['title']} can be addressed by {ro['opportunity']['title']}",
                    'implications': [
                        f"Cross-domain solution spanning {ro['risk']['agent']} and {ro['opportunity']['agent']}",
                        "Integrated approach recommended"
                    ],
                    'priority': 'high'
                })
        
        return insights
    
    def save_enriched_intelligence(self, connections: Dict, insights: List[Dict]):
        """Save cross-domain intelligence"""
        # Save connections
        connections_file = self.enrichment_path / "cross_domain_connections.json"
        with open(connections_file, 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'connections': connections
            }, f, indent=2)
            
        # Save insights
        insights_file = self.enrichment_path / "cross_domain_insights.json"
        with open(insights_file, 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'insights': insights,
                'summary': {
                    'total_insights': len(insights),
                    'high_priority': len([i for i in insights if i.get('priority') == 'high']),
                    'insight_types': list(set(i['type'] for i in insights))
                }
            }, f, indent=2)
            
        print(f"\nSaved {len(connections['geographic_connections'])} geographic connections")
        print(f"Saved {len(connections['topic_connections'])} topic connections")
        print(f"Saved {len(connections['value_chain_connections'])} value chain connections")
        print(f"Saved {len(connections['risk_opportunity_pairs'])} risk-opportunity pairs")
        print(f"\nGenerated {len(insights)} cross-domain insights")
        print(f"Files saved to: {self.enrichment_path}")


def main():
    print("Cross-Domain Intelligence Enrichment")
    print("===================================\n")
    
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    enricher = CrossDomainEnricher(base_path)
    
    connections, insights = enricher.analyze_cross_domain_patterns()
    
    print("\nTop Cross-Domain Insights:")
    print("-" * 50)
    
    for insight in insights[:5]:
        print(f"\n[{insight['priority'].upper()}] {insight['title']}")
        print(f"Type: {insight['type']}")
        print(f"Description: {insight['description']}")
        if insight.get('implications'):
            print("Implications:")
            for imp in insight['implications']:
                print(f"  - {imp}")


if __name__ == "__main__":
    main()
