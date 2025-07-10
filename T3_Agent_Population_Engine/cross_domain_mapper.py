#!/usr/bin/env python3
"""
Cross-Domain Intelligence Mapper
Creates intelligent connections between different agent domains
"""

import json
import networkx as nx
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any
from collections import defaultdict
import numpy as np
from datetime import datetime


class CrossDomainMapper:
    """Maps relationships and synergies between different intelligence domains"""
    
    def __init__(self, knowledge_base_path: Path):
        self.kb_path = knowledge_base_path
        self.intelligence_graph = nx.DiGraph()
        self.domain_connections = defaultdict(lambda: defaultdict(list))
        
        # Define domain interaction matrix
        self.domain_interactions = {
            "Market Intelligence": {
                "Financial Intelligence": ["pricing_trends", "investment_analysis", "market_valuations"],
                "Neighborhood Intelligence": ["location_premiums", "area_demand", "growth_corridors"],
                "Regulatory Intelligence": ["development_capacity", "zoning_impacts", "permit_trends"],
                "Environmental Intelligence": ["risk_pricing", "sustainability_premiums", "climate_impacts"],
                "Technology & Innovation Intelligence": ["proptech_disruption", "smart_building_demand", "innovation_hubs"]
            },
            "Financial Intelligence": {
                "Market Intelligence": ["market_conditions", "competitive_landscape", "price_discovery"],
                "Neighborhood Intelligence": ["area_roi", "demographic_drivers", "growth_potential"],
                "Regulatory Intelligence": ["tax_implications", "incentive_programs", "compliance_costs"],
                "Environmental Intelligence": ["green_financing", "risk_assessment", "insurance_costs"],
                "Technology & Innovation Intelligence": ["tech_investments", "innovation_funding", "startup_activity"]
            },
            "Neighborhood Intelligence": {
                "Market Intelligence": ["local_market_dynamics", "competition_analysis", "demand_patterns"],
                "Financial Intelligence": ["investment_hotspots", "financing_availability", "property_values"],
                "Regulatory Intelligence": ["zoning_changes", "development_restrictions", "community_planning"],
                "Environmental Intelligence": ["environmental_quality", "flood_zones", "green_spaces"],
                "Technology & Innovation Intelligence": ["smart_infrastructure", "tech_employment", "innovation_districts"]
            },
            "Environmental Intelligence": {
                "Market Intelligence": ["environmental_premiums", "risk_discounts", "sustainability_demand"],
                "Financial Intelligence": ["risk_mitigation_costs", "insurance_requirements", "green_incentives"],
                "Neighborhood Intelligence": ["area_vulnerabilities", "quality_of_life", "resilience_factors"],
                "Regulatory Intelligence": ["environmental_compliance", "permit_requirements", "regulation_changes"],
                "Technology & Innovation Intelligence": ["cleantech_solutions", "smart_monitoring", "resilience_tech"]
            },
            "Regulatory Intelligence": {
                "Market Intelligence": ["regulatory_impacts", "development_feasibility", "market_constraints"],
                "Financial Intelligence": ["compliance_costs", "tax_structures", "incentive_eligibility"],
                "Neighborhood Intelligence": ["zoning_maps", "community_regulations", "development_rights"],
                "Environmental Intelligence": ["environmental_regulations", "compliance_standards", "mitigation_requirements"],
                "Technology & Innovation Intelligence": ["tech_regulations", "innovation_policies", "smart_city_standards"]
            },
            "Technology & Innovation Intelligence": {
                "Market Intelligence": ["tech_market_trends", "innovation_demand", "disruption_patterns"],
                "Financial Intelligence": ["tech_valuations", "venture_activity", "roi_innovations"],
                "Neighborhood Intelligence": ["tech_hubs", "innovation_corridors", "smart_communities"],
                "Environmental Intelligence": ["sustainability_tech", "monitoring_systems", "efficiency_solutions"],
                "Regulatory Intelligence": ["tech_compliance", "innovation_policies", "data_regulations"]
            }
        }
        
    def build_intelligence_graph(self, intelligence_records: Dict[str, List[Dict[str, Any]]]):
        """Build a graph representation of all intelligence relationships"""
        
        # Add nodes for each intelligence record
        for domain, records in intelligence_records.items():
            for record in records:
                node_id = f"{domain}_{record['id']}"
                self.intelligence_graph.add_node(
                    node_id,
                    domain=domain,
                    record_id=record['id'],
                    title=record.get('title', ''),
                    tags=record.get('tags', []),
                    geographic_scope=record.get('geographic_scope', []),
                    confidence_score=record.get('confidence_score', 0.8)
                )
        
        # Create edges based on relationships
        self._create_tag_based_connections()
        self._create_geographic_connections()
        self._create_temporal_connections(intelligence_records)
        self._create_domain_specific_connections()
        
    def _create_tag_based_connections(self):
        """Create connections based on shared tags"""
        nodes = list(self.intelligence_graph.nodes(data=True))
        
        for i, (node1_id, node1_data) in enumerate(nodes):
            for j, (node2_id, node2_data) in enumerate(nodes[i+1:], i+1):
                # Skip if same domain
                if node1_data['domain'] == node2_data['domain']:
                    continue
                    
                # Calculate tag similarity
                tags1 = set(node1_data.get('tags', []))
                tags2 = set(node2_data.get('tags', []))
                common_tags = tags1 & tags2
                
                if len(common_tags) >= 2:
                    weight = len(common_tags) / max(len(tags1), len(tags2))
                    self.intelligence_graph.add_edge(
                        node1_id, node2_id,
                        weight=weight,
                        connection_type='tag_similarity',
                        common_tags=list(common_tags)
                    )
                    
    def _create_geographic_connections(self):
        """Create connections based on geographic overlap"""
        nodes = list(self.intelligence_graph.nodes(data=True))
        
        for i, (node1_id, node1_data) in enumerate(nodes):
            for j, (node2_id, node2_data) in enumerate(nodes[i+1:], i+1):
                # Skip if same domain
                if node1_data['domain'] == node2_data['domain']:
                    continue
                    
                # Check geographic overlap
                geo1 = set(node1_data.get('geographic_scope', []))
                geo2 = set(node2_data.get('geographic_scope', []))
                common_areas = geo1 & geo2
                
                if common_areas:
                    weight = len(common_areas) / max(len(geo1), len(geo2))
                    self.intelligence_graph.add_edge(
                        node1_id, node2_id,
                        weight=weight,
                        connection_type='geographic_overlap',
                        common_areas=list(common_areas)
                    )
                    
    def _create_temporal_connections(self, intelligence_records: Dict[str, List[Dict[str, Any]]]):
        """Create connections based on temporal relevance"""
        # Group records by temporal relevance
        temporal_groups = defaultdict(list)
        
        for domain, records in intelligence_records.items():
            for record in records:
                temporal_key = record.get('temporal_relevance', 'current')
                temporal_groups[temporal_key].append((domain, record['id']))
        
        # Connect records with same temporal relevance across domains
        for temporal_key, records in temporal_groups.items():
            domain_groups = defaultdict(list)
            for domain, record_id in records:
                domain_groups[domain].append(record_id)
            
            # Create connections between different domains
            domains = list(domain_groups.keys())
            for i, domain1 in enumerate(domains):
                for domain2 in domains[i+1:]:
                    for record1 in domain_groups[domain1]:
                        for record2 in domain_groups[domain2]:
                            node1_id = f"{domain1}_{record1}"
                            node2_id = f"{domain2}_{record2}"
                            
                            if self.intelligence_graph.has_node(node1_id) and self.intelligence_graph.has_node(node2_id):
                                self.intelligence_graph.add_edge(
                                    node1_id, node2_id,
                                    weight=0.5,
                                    connection_type='temporal_alignment',
                                    temporal_key=temporal_key
                                )
                                
    def _create_domain_specific_connections(self):
        """Create connections based on predefined domain interactions"""
        nodes = list(self.intelligence_graph.nodes(data=True))
        
        for node_id, node_data in nodes:
            source_domain = node_data['domain']
            
            if source_domain in self.domain_interactions:
                for target_domain, interaction_types in self.domain_interactions[source_domain].items():
                    # Find nodes from target domain
                    target_nodes = [
                        (n_id, n_data) for n_id, n_data in nodes 
                        if n_data['domain'] == target_domain and n_id != node_id
                    ]
                    
                    for target_id, target_data in target_nodes:
                        # Check if any interaction type matches tags or content
                        node_tags = set(node_data.get('tags', []))
                        target_tags = set(target_data.get('tags', []))
                        all_tags = node_tags | target_tags
                        
                        matching_interactions = [
                            itype for itype in interaction_types 
                            if any(itype in tag.lower() for tag in all_tags)
                        ]
                        
                        if matching_interactions:
                            weight = len(matching_interactions) / len(interaction_types)
                            self.intelligence_graph.add_edge(
                                node_id, target_id,
                                weight=weight,
                                connection_type='domain_interaction',
                                interaction_types=matching_interactions
                            )
    
    def find_cross_domain_insights(self, min_connections: int = 3) -> List[Dict[str, Any]]:
        """Find valuable cross-domain intelligence insights"""
        insights = []
        
        # Find nodes with high cross-domain connectivity
        for node in self.intelligence_graph.nodes():
            neighbors = list(self.intelligence_graph.neighbors(node))
            
            # Group neighbors by domain
            domain_neighbors = defaultdict(list)
            for neighbor in neighbors:
                neighbor_data = self.intelligence_graph.nodes[neighbor]
                domain_neighbors[neighbor_data['domain']].append(neighbor)
            
            # Check if node connects to multiple domains
            if len(domain_neighbors) >= min_connections:
                node_data = self.intelligence_graph.nodes[node]
                
                # Calculate insight value
                total_weight = sum(
                    self.intelligence_graph[node][neighbor]['weight'] 
                    for neighbor in neighbors
                )
                
                insight = {
                    "central_node": node,
                    "domain": node_data['domain'],
                    "title": node_data.get('title', ''),
                    "connected_domains": list(domain_neighbors.keys()),
                    "connection_count": len(neighbors),
                    "total_weight": total_weight,
                    "connections": self._analyze_connections(node, domain_neighbors)
                }
                
                insights.append(insight)
        
        # Sort by value (combination of connections and weight)
        insights.sort(key=lambda x: x['connection_count'] * x['total_weight'], reverse=True)
        
        return insights
    
    def _analyze_connections(self, node: str, domain_neighbors: Dict[str, List[str]]) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze the connections for a node"""
        connections = {}
        
        for domain, neighbors in domain_neighbors.items():
            domain_connections = []
            
            for neighbor in neighbors:
                edge_data = self.intelligence_graph[node][neighbor]
                neighbor_data = self.intelligence_graph.nodes[neighbor]
                
                connection = {
                    "target_node": neighbor,
                    "target_title": neighbor_data.get('title', ''),
                    "connection_type": edge_data['connection_type'],
                    "weight": edge_data['weight']
                }
                
                # Add connection-specific details
                if edge_data['connection_type'] == 'tag_similarity':
                    connection['common_tags'] = edge_data.get('common_tags', [])
                elif edge_data['connection_type'] == 'geographic_overlap':
                    connection['common_areas'] = edge_data.get('common_areas', [])
                elif edge_data['connection_type'] == 'domain_interaction':
                    connection['interaction_types'] = edge_data.get('interaction_types', [])
                    
                domain_connections.append(connection)
            
            connections[domain] = domain_connections
        
        return connections
    
    def generate_synergy_recommendations(self) -> List[Dict[str, Any]]:
        """Generate recommendations for cross-domain synergies"""
        recommendations = []
        
        # Find strong cross-domain patterns
        insights = self.find_cross_domain_insights(min_connections=2)
        
        for insight in insights[:20]:  # Top 20 insights
            # Analyze the pattern
            pattern_type = self._identify_pattern_type(insight)
            
            recommendation = {
                "pattern_type": pattern_type,
                "central_intelligence": {
                    "domain": insight['domain'],
                    "title": insight['title']
                },
                "synergy_domains": insight['connected_domains'],
                "recommendation": self._generate_recommendation_text(pattern_type, insight),
                "action_items": self._generate_action_items(pattern_type, insight),
                "potential_value": self._estimate_synergy_value(insight)
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _identify_pattern_type(self, insight: Dict[str, Any]) -> str:
        """Identify the type of cross-domain pattern"""
        domains = set([insight['domain']] + insight['connected_domains'])
        
        # Define pattern types based on domain combinations
        if 'Market Intelligence' in domains and 'Financial Intelligence' in domains:
            return 'investment_opportunity'
        elif 'Environmental Intelligence' in domains and 'Regulatory Intelligence' in domains:
            return 'compliance_requirement'
        elif 'Neighborhood Intelligence' in domains and 'Technology & Innovation Intelligence' in domains:
            return 'growth_corridor'
        elif 'Financial Intelligence' in domains and 'Regulatory Intelligence' in domains:
            return 'incentive_opportunity'
        elif len(domains) >= 4:
            return 'complex_synergy'
        else:
            return 'standard_synergy'
    
    def _generate_recommendation_text(self, pattern_type: str, insight: Dict[str, Any]) -> str:
        """Generate recommendation text based on pattern type"""
        recommendations = {
            'investment_opportunity': f"Strong investment opportunity identified connecting {insight['domain']} with market and financial factors",
            'compliance_requirement': f"Critical compliance consideration linking environmental and regulatory requirements",
            'growth_corridor': f"Emerging growth corridor identified with technology and neighborhood development synergies",
            'incentive_opportunity': f"Financial incentive opportunity available through regulatory programs",
            'complex_synergy': f"Multi-domain opportunity involving {len(insight['connected_domains'])} different intelligence areas",
            'standard_synergy': f"Cross-domain synergy between {insight['domain']} and connected intelligence domains"
        }
        
        return recommendations.get(pattern_type, "Cross-domain synergy identified")
    
    def _generate_action_items(self, pattern_type: str, insight: Dict[str, Any]) -> List[str]:
        """Generate action items based on pattern type"""
        action_templates = {
            'investment_opportunity': [
                "Conduct detailed financial analysis",
                "Review market comparables",
                "Assess investment timeline",
                "Calculate projected returns"
            ],
            'compliance_requirement': [
                "Review regulatory requirements",
                "Assess environmental impact",
                "Develop compliance strategy",
                "Engage regulatory consultants"
            ],
            'growth_corridor': [
                "Analyze demographic trends",
                "Map innovation assets",
                "Identify development opportunities",
                "Track infrastructure investments"
            ],
            'incentive_opportunity': [
                "Review incentive eligibility",
                "Calculate financial benefits",
                "Prepare application materials",
                "Engage with program administrators"
            ],
            'complex_synergy': [
                "Conduct comprehensive analysis",
                "Map stakeholder interests",
                "Develop integrated strategy",
                "Create implementation roadmap"
            ],
            'standard_synergy': [
                "Analyze connection points",
                "Identify opportunities",
                "Develop action plan",
                "Monitor developments"
            ]
        }
        
        return action_templates.get(pattern_type, ["Further investigation recommended"])
    
    def _estimate_synergy_value(self, insight: Dict[str, Any]) -> str:
        """Estimate the value of a cross-domain synergy"""
        # Simple heuristic based on connections and weights
        score = insight['connection_count'] * insight['total_weight']
        
        if score > 10:
            return "Very High"
        elif score > 5:
            return "High"
        elif score > 2:
            return "Medium"
        else:
            return "Low"
    
    def export_cross_domain_map(self, output_path: Path):
        """Export the cross-domain intelligence map"""
        # Create export data
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "graph_statistics": {
                "total_nodes": self.intelligence_graph.number_of_nodes(),
                "total_edges": self.intelligence_graph.number_of_edges(),
                "domains": self._get_domain_statistics()
            },
            "cross_domain_insights": self.find_cross_domain_insights(),
            "synergy_recommendations": self.generate_synergy_recommendations(),
            "domain_interaction_matrix": self.domain_interactions
        }
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def _get_domain_statistics(self) -> Dict[str, Dict[str, int]]:
        """Get statistics for each domain"""
        stats = {}
        
        for domain in self.domain_interactions.keys():
            domain_nodes = [
                n for n, d in self.intelligence_graph.nodes(data=True) 
                if d['domain'] == domain
            ]
            
            # Count cross-domain connections
            cross_domain_edges = 0
            for node in domain_nodes:
                for neighbor in self.intelligence_graph.neighbors(node):
                    if self.intelligence_graph.nodes[neighbor]['domain'] != domain:
                        cross_domain_edges += 1
            
            stats[domain] = {
                "node_count": len(domain_nodes),
                "cross_domain_connections": cross_domain_edges
            }
        
        return stats


if __name__ == "__main__":
    # Example usage
    mapper = CrossDomainMapper(Path("/Users/fernandox/Desktop/Core Agent Architecture/Agent_Knowledge_Bases"))
    print("Cross-Domain Intelligence Mapper initialized")
