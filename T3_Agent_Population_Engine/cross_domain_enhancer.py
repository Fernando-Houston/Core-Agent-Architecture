#!/usr/bin/env python3
"""
Cross-Domain Intelligence Enhancer
Expands relationships between different intelligence domains
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set
from collections import defaultdict
import networkx as nx
from datetime import datetime


class CrossDomainEnhancer:
    """Enhances cross-domain intelligence relationships"""
    
    def __init__(self, knowledge_base_path: Path):
        self.kb_path = knowledge_base_path
        self.enhancement_rules = self._initialize_enhancement_rules()
        self.relationship_graph = nx.MultiDiGraph()
        
    def _initialize_enhancement_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize cross-domain enhancement rules"""
        
        return {
            "environmental_financial": [
                {
                    "trigger": "flood_risk",
                    "creates": "insurance_cost",
                    "relationship": "increases",
                    "impact_function": self._flood_risk_to_insurance_cost
                },
                {
                    "trigger": "air_quality",
                    "creates": "property_value",
                    "relationship": "affects",
                    "impact_function": self._air_quality_to_property_value
                },
                {
                    "trigger": "sustainability_features",
                    "creates": "financing_incentives",
                    "relationship": "enables",
                    "impact_function": self._sustainability_to_financing
                }
            ],
            "regulatory_market": [
                {
                    "trigger": "zoning_change",
                    "creates": "development_opportunity",
                    "relationship": "creates",
                    "impact_function": self._zoning_to_opportunity
                },
                {
                    "trigger": "density_increase",
                    "creates": "land_value",
                    "relationship": "increases",
                    "impact_function": self._density_to_land_value
                },
                {
                    "trigger": "permit_streamlining",
                    "creates": "development_timeline",
                    "relationship": "reduces",
                    "impact_function": self._permit_to_timeline
                }
            ],
            "technology_neighborhood": [
                {
                    "trigger": "innovation_district",
                    "creates": "tech_employment",
                    "relationship": "attracts",
                    "impact_function": self._innovation_to_employment
                },
                {
                    "trigger": "smart_infrastructure",
                    "creates": "quality_of_life",
                    "relationship": "improves",
                    "impact_function": self._smart_to_qol
                },
                {
                    "trigger": "tech_companies",
                    "creates": "housing_demand",
                    "relationship": "drives",
                    "impact_function": self._tech_to_housing
                }
            ],
            "market_financial": [
                {
                    "trigger": "price_appreciation",
                    "creates": "investment_returns",
                    "relationship": "determines",
                    "impact_function": self._appreciation_to_returns
                },
                {
                    "trigger": "vacancy_rates",
                    "creates": "cash_flow",
                    "relationship": "impacts",
                    "impact_function": self._vacancy_to_cashflow
                },
                {
                    "trigger": "market_competition",
                    "creates": "cap_rates",
                    "relationship": "influences",
                    "impact_function": self._competition_to_caprates
                }
            ],
            "neighborhood_environmental": [
                {
                    "trigger": "green_space",
                    "creates": "air_quality",
                    "relationship": "improves",
                    "impact_function": self._greenspace_to_air
                },
                {
                    "trigger": "transit_access",
                    "creates": "carbon_footprint",
                    "relationship": "reduces",
                    "impact_function": self._transit_to_carbon
                },
                {
                    "trigger": "industrial_proximity",
                    "creates": "environmental_risk",
                    "relationship": "increases",
                    "impact_function": self._industrial_to_risk
                }
            ]
        }
    
    def enhance_cross_domain_relationships(self, current_knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance existing cross-domain relationships"""
        
        enhanced = {
            "enhanced_relationships": [],
            "new_insights": [],
            "impact_chains": [],
            "synergy_opportunities": [],
            "risk_correlations": []
        }
        
        # Build relationship graph from current knowledge
        self._build_relationship_graph(current_knowledge)
        
        # Apply enhancement rules
        for domain_pair, rules in self.enhancement_rules.items():
            for rule in rules:
                new_relationships = self._apply_enhancement_rule(rule, current_knowledge)
                enhanced['enhanced_relationships'].extend(new_relationships)
        
        # Discover impact chains
        enhanced['impact_chains'] = self._discover_impact_chains()
        
        # Identify synergy opportunities
        enhanced['synergy_opportunities'] = self._identify_synergies(current_knowledge)
        
        # Find risk correlations
        enhanced['risk_correlations'] = self._find_risk_correlations(current_knowledge)
        
        # Generate new insights from enhancements
        enhanced['new_insights'] = self._generate_new_insights(enhanced)
        
        return enhanced
    
    def _build_relationship_graph(self, knowledge: Dict[str, Any]):
        """Build graph of current relationships"""
        
        # Add nodes for each intelligence record
        if 'agents' in knowledge:
            for agent, data in knowledge['agents'].items():
                for record_id in data.get('record_ids', []):
                    self.relationship_graph.add_node(
                        record_id,
                        agent=agent,
                        type='intelligence_record'
                    )
        
        # Add edges for cross-references
        if 'cross_domain_mappings' in knowledge:
            for source_agent, mappings in knowledge['cross_domain_mappings'].items():
                for mapping in mappings:
                    self.relationship_graph.add_edge(
                        mapping['record_id'],
                        mapping['shared_with'],
                        relationship_type='shared',
                        reason=mapping['reason']
                    )
    
    def _apply_enhancement_rule(self, rule: Dict[str, Any], knowledge: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply a single enhancement rule"""
        
        new_relationships = []
        
        # Find records that match the trigger
        trigger_records = self._find_trigger_records(rule['trigger'], knowledge)
        
        for record in trigger_records:
            # Calculate impact using the rule's function
            impact = rule['impact_function'](record)
            
            if impact:
                relationship = {
                    "source_record": record['id'],
                    "source_domain": record['domain'],
                    "trigger": rule['trigger'],
                    "creates": rule['creates'],
                    "relationship_type": rule['relationship'],
                    "impact": impact,
                    "confidence": impact.get('confidence', 0.8),
                    "timestamp": datetime.now().isoformat()
                }
                
                new_relationships.append(relationship)
                
                # Add to graph
                self.relationship_graph.add_edge(
                    record['id'],
                    rule['creates'],
                    relationship_type=rule['relationship'],
                    impact=impact
                )
        
        return new_relationships
    
    def _find_trigger_records(self, trigger: str, knowledge: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find records that match a trigger condition"""
        
        matching_records = []
        
        # Search in tag index
        if 'tag_index' in knowledge:
            for tag, record_ids in knowledge['tag_index'].items():
                if trigger.lower() in tag.lower():
                    matching_records.extend([
                        {'id': rid, 'domain': self._get_record_domain(rid, knowledge)}
                        for rid in record_ids
                    ])
        
        return matching_records
    
    def _get_record_domain(self, record_id: str, knowledge: Dict[str, Any]) -> str:
        """Get domain for a record ID"""
        
        for agent, data in knowledge.get('agents', {}).items():
            if record_id in data.get('record_ids', []):
                return agent
        
        return 'unknown'
    
    # Impact calculation functions
    def _flood_risk_to_insurance_cost(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate insurance cost impact from flood risk"""
        
        # Simplified calculation - would use actual flood risk data
        base_impact = {
            "type": "insurance_premium_increase",
            "magnitude": "25-40%",
            "annual_cost_impact": "$5,000-15,000",
            "factors": [
                "FEMA flood zone designation",
                "Historical flooding events",
                "Mitigation infrastructure"
            ],
            "confidence": 0.85
        }
        
        return base_impact
    
    def _air_quality_to_property_value(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate property value impact from air quality"""
        
        return {
            "type": "property_value_adjustment",
            "magnitude": "-5% to -15%",
            "factors": [
                "PM2.5 levels",
                "Proximity to pollution sources",
                "Health impact studies"
            ],
            "confidence": 0.75
        }
    
    def _sustainability_to_financing(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate financing incentives from sustainability features"""
        
        return {
            "type": "green_financing_eligibility",
            "programs": [
                "PACE financing",
                "Green bonds",
                "ESG investment funds"
            ],
            "rate_reduction": "0.25-0.75%",
            "confidence": 0.9
        }
    
    def _zoning_to_opportunity(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate development opportunity from zoning changes"""
        
        return {
            "type": "development_potential_increase",
            "density_bonus": "20-50%",
            "use_expansion": ["mixed-use", "residential", "commercial"],
            "value_creation": "$10-50M",
            "timeline": "6-18 months",
            "confidence": 0.8
        }
    
    def _density_to_land_value(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate land value impact from density increases"""
        
        return {
            "type": "land_value_appreciation",
            "increase_per_far": "15-25%",
            "total_impact": "40-100%",
            "market_comparables": "Available",
            "confidence": 0.85
        }
    
    def _permit_to_timeline(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate timeline impact from permit streamlining"""
        
        return {
            "type": "development_timeline_reduction",
            "time_savings": "3-6 months",
            "cost_savings": "$100K-500K",
            "carrying_cost_reduction": "10-20%",
            "confidence": 0.9
        }
    
    def _innovation_to_employment(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate employment impact from innovation districts"""
        
        return {
            "type": "tech_job_creation",
            "jobs_per_acre": "50-200",
            "average_salary": "$85,000-120,000",
            "multiplier_effect": "2.5-4x",
            "confidence": 0.8
        }
    
    def _smart_to_qol(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate quality of life impact from smart infrastructure"""
        
        return {
            "type": "quality_of_life_improvement",
            "metrics": {
                "traffic_reduction": "15-25%",
                "energy_efficiency": "20-30%",
                "public_safety": "+10-15%"
            },
            "resident_satisfaction": "+20-30%",
            "confidence": 0.75
        }
    
    def _tech_to_housing(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate housing demand from tech companies"""
        
        return {
            "type": "housing_demand_surge",
            "units_per_100_jobs": "125-150",
            "price_pressure": "+5-15% annually",
            "rental_demand": "High",
            "confidence": 0.85
        }
    
    def _appreciation_to_returns(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate investment returns from appreciation"""
        
        return {
            "type": "investment_return_projection",
            "annual_return": "8-15%",
            "5_year_total": "45-100%",
            "risk_adjusted": "6-12%",
            "confidence": 0.8
        }
    
    def _vacancy_to_cashflow(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate cash flow impact from vacancy"""
        
        return {
            "type": "cash_flow_impact",
            "noi_reduction": "Direct correlation",
            "break_even_vacancy": "10-15%",
            "stabilization_period": "6-12 months",
            "confidence": 0.9
        }
    
    def _competition_to_caprates(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate cap rate impact from competition"""
        
        return {
            "type": "cap_rate_compression",
            "rate_change": "-25 to -75 bps",
            "value_impact": "+5-15%",
            "market_dynamics": "Competitive",
            "confidence": 0.75
        }
    
    def _greenspace_to_air(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate air quality impact from green space"""
        
        return {
            "type": "air_quality_improvement",
            "pm25_reduction": "10-20%",
            "health_benefits": "Significant",
            "property_premium": "3-8%",
            "confidence": 0.8
        }
    
    def _transit_to_carbon(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate carbon footprint from transit access"""
        
        return {
            "type": "carbon_reduction",
            "vehicle_miles_reduced": "30-50%",
            "co2_savings": "2-4 tons/year/household",
            "sustainability_score": "+15-25 points",
            "confidence": 0.85
        }
    
    def _industrial_to_risk(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate environmental risk from industrial proximity"""
        
        return {
            "type": "environmental_risk_increase",
            "contamination_risk": "Medium-High",
            "remediation_cost": "$100K-5M",
            "development_constraints": "Significant",
            "confidence": 0.7
        }
    
    def _discover_impact_chains(self) -> List[Dict[str, Any]]:
        """Discover multi-step impact chains"""
        
        chains = []
        
        # Find paths of length 3 or more
        for source in self.relationship_graph.nodes():
            for target in self.relationship_graph.nodes():
                if source != target:
                    try:
                        paths = list(nx.all_simple_paths(
                            self.relationship_graph, 
                            source, 
                            target, 
                            cutoff=4
                        ))
                        
                        for path in paths:
                            if len(path) >= 3:
                                chain = {
                                    "start": path[0],
                                    "end": path[-1],
                                    "steps": path,
                                    "length": len(path),
                                    "impacts": self._get_path_impacts(path)
                                }
                                chains.append(chain)
                    except:
                        continue
        
        # Sort by length and impact
        chains.sort(key=lambda x: x['length'], reverse=True)
        
        return chains[:20]  # Top 20 chains
    
    def _get_path_impacts(self, path: List[str]) -> List[Dict[str, Any]]:
        """Get impacts along a path"""
        
        impacts = []
        
        for i in range(len(path) - 1):
            edge_data = self.relationship_graph.get_edge_data(path[i], path[i+1])
            if edge_data:
                for key, data in edge_data.items():
                    impacts.append({
                        "from": path[i],
                        "to": path[i+1],
                        "type": data.get('relationship_type', 'unknown'),
                        "impact": data.get('impact', {})
                    })
        
        return impacts
    
    def _identify_synergies(self, knowledge: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify synergy opportunities between domains"""
        
        synergies = []
        
        # Pre-defined synergy patterns
        synergy_patterns = [
            {
                "domains": ["Environmental Intelligence", "Financial Intelligence"],
                "type": "Green Finance Opportunity",
                "description": "Sustainable projects qualify for preferential financing",
                "value_proposition": "Lower cost of capital + environmental benefits",
                "implementation": [
                    "Identify green-certified projects",
                    "Connect with ESG investors",
                    "Structure green bonds or PACE financing"
                ]
            },
            {
                "domains": ["Technology & Innovation Intelligence", "Neighborhood Intelligence"],
                "type": "Innovation District Development",
                "description": "Tech hubs driving neighborhood transformation",
                "value_proposition": "Job creation + property appreciation + urban renewal",
                "implementation": [
                    "Map innovation assets",
                    "Identify development sites",
                    "Create live-work-play environments"
                ]
            },
            {
                "domains": ["Regulatory Intelligence", "Market Intelligence"],
                "type": "Zoning Arbitrage",
                "description": "Regulatory changes creating value opportunities",
                "value_proposition": "Immediate value creation through entitlements",
                "implementation": [
                    "Monitor zoning changes",
                    "Identify undervalued properties",
                    "Secure entitlements before market adjustment"
                ]
            },
            {
                "domains": ["Environmental Intelligence", "Neighborhood Intelligence"],
                "type": "Resilient Community Development",
                "description": "Climate-adapted neighborhoods with premium values",
                "value_proposition": "Risk mitigation + quality of life + value premium",
                "implementation": [
                    "Assess climate vulnerabilities",
                    "Design resilient infrastructure",
                    "Market sustainability features"
                ]
            }
        ]
        
        # Check which synergies are applicable based on current knowledge
        for pattern in synergy_patterns:
            applicable = all(
                any(domain in agent for agent in knowledge.get('agents', {}).keys())
                for domain in pattern['domains']
            )
            
            if applicable:
                synergy = pattern.copy()
                synergy['relevance_score'] = self._calculate_synergy_relevance(pattern, knowledge)
                synergy['priority'] = "High" if synergy['relevance_score'] > 0.7 else "Medium"
                synergies.append(synergy)
        
        # Sort by relevance
        synergies.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return synergies
    
    def _calculate_synergy_relevance(self, pattern: Dict[str, Any], knowledge: Dict[str, Any]) -> float:
        """Calculate relevance score for a synergy pattern"""
        
        score = 0.5  # Base score
        
        # Check for related tags in knowledge
        relevant_tags = {
            "Green Finance Opportunity": ["environmental", "sustainability", "green", "financing"],
            "Innovation District Development": ["innovation", "technology", "tech", "development"],
            "Zoning Arbitrage": ["zoning", "regulatory", "entitlement", "development"],
            "Resilient Community Development": ["resilient", "climate", "sustainable", "community"]
        }
        
        pattern_tags = relevant_tags.get(pattern['type'], [])
        tag_index = knowledge.get('tag_index', {})
        
        matches = sum(1 for tag in pattern_tags if any(tag in t for t in tag_index.keys()))
        score += (matches / len(pattern_tags)) * 0.5 if pattern_tags else 0
        
        return min(1.0, score)
    
    def _find_risk_correlations(self, knowledge: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find correlated risks across domains"""
        
        risk_correlations = []
        
        # Define risk correlation patterns
        correlation_patterns = [
            {
                "risk_pair": ["flood_risk", "property_value"],
                "correlation": -0.7,
                "mechanism": "Flood risk directly reduces property values and insurability",
                "mitigation": "Flood mitigation infrastructure, elevated construction"
            },
            {
                "risk_pair": ["market_downturn", "financing_availability"],
                "correlation": -0.8,
                "mechanism": "Market downturns tighten lending standards",
                "mitigation": "Diversified financing sources, strong relationships"
            },
            {
                "risk_pair": ["regulatory_delay", "construction_cost"],
                "correlation": 0.6,
                "mechanism": "Delays increase carrying costs and material prices",
                "mitigation": "Expedited permitting, phased development"
            },
            {
                "risk_pair": ["environmental_contamination", "development_timeline"],
                "correlation": 0.9,
                "mechanism": "Remediation requirements extend project timelines",
                "mitigation": "Phase I/II assessments, environmental insurance"
            }
        ]
        
        # Check for presence of risk factors in knowledge
        for pattern in correlation_patterns:
            risk1_present = self._check_risk_presence(pattern['risk_pair'][0], knowledge)
            risk2_present = self._check_risk_presence(pattern['risk_pair'][1], knowledge)
            
            if risk1_present or risk2_present:
                correlation = {
                    "risks": pattern['risk_pair'],
                    "correlation_strength": abs(pattern['correlation']),
                    "direction": "negative" if pattern['correlation'] < 0 else "positive",
                    "mechanism": pattern['mechanism'],
                    "mitigation_strategies": pattern['mitigation'],
                    "domains_affected": self._get_affected_domains(pattern['risk_pair']),
                    "action_priority": "High" if abs(pattern['correlation']) > 0.7 else "Medium"
                }
                
                risk_correlations.append(correlation)
        
        # Sort by correlation strength
        risk_correlations.sort(key=lambda x: x['correlation_strength'], reverse=True)
        
        return risk_correlations
    
    def _check_risk_presence(self, risk_type: str, knowledge: Dict[str, Any]) -> bool:
        """Check if a risk type is present in the knowledge base"""
        
        # Check in tags
        tag_index = knowledge.get('tag_index', {})
        for tag in tag_index.keys():
            if risk_type.replace('_', ' ') in tag.lower():
                return True
        
        return False
    
    def _get_affected_domains(self, risk_pair: List[str]) -> List[str]:
        """Get domains affected by a risk pair"""
        
        domain_map = {
            "flood_risk": ["Environmental Intelligence", "Financial Intelligence"],
            "property_value": ["Market Intelligence", "Financial Intelligence"],
            "market_downturn": ["Market Intelligence", "Financial Intelligence"],
            "financing_availability": ["Financial Intelligence"],
            "regulatory_delay": ["Regulatory Intelligence"],
            "construction_cost": ["Financial Intelligence", "Market Intelligence"],
            "environmental_contamination": ["Environmental Intelligence"],
            "development_timeline": ["Market Intelligence", "Regulatory Intelligence"]
        }
        
        affected = set()
        for risk in risk_pair:
            affected.update(domain_map.get(risk, []))
        
        return list(affected)
    
    def _generate_new_insights(self, enhanced: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate new insights from enhancements"""
        
        insights = []
        
        # Insight from impact chains
        if enhanced['impact_chains']:
            for chain in enhanced['impact_chains'][:5]:  # Top 5 chains
                insight = {
                    "type": "impact_chain",
                    "title": f"Multi-step impact: {chain['start']} → {chain['end']}",
                    "description": f"Discovered {chain['length']}-step impact chain",
                    "steps": chain['steps'],
                    "implications": self._analyze_chain_implications(chain),
                    "confidence": 0.7,
                    "actionable": True
                }
                insights.append(insight)
        
        # Insights from synergies
        for synergy in enhanced['synergy_opportunities'][:3]:  # Top 3 synergies
            insight = {
                "type": "synergy_opportunity",
                "title": synergy['type'],
                "description": synergy['description'],
                "value_proposition": synergy['value_proposition'],
                "implementation_steps": synergy['implementation'],
                "priority": synergy['priority'],
                "confidence": synergy['relevance_score'],
                "actionable": True
            }
            insights.append(insight)
        
        # Insights from risk correlations
        for risk_corr in enhanced['risk_correlations'][:3]:  # Top 3 risk correlations
            insight = {
                "type": "risk_correlation",
                "title": f"Correlated risks: {' & '.join(risk_corr['risks'])}",
                "description": risk_corr['mechanism'],
                "correlation_strength": risk_corr['correlation_strength'],
                "mitigation": risk_corr['mitigation_strategies'],
                "priority": risk_corr['action_priority'],
                "confidence": 0.8,
                "actionable": True
            }
            insights.append(insight)
        
        return insights
    
    def _analyze_chain_implications(self, chain: Dict[str, Any]) -> List[str]:
        """Analyze implications of an impact chain"""
        
        implications = []
        
        if chain['length'] >= 4:
            implications.append("Complex cascading effects require holistic planning")
        
        if any('financial' in str(step).lower() for step in chain['steps']):
            implications.append("Financial impacts should be modeled across the full chain")
        
        if any('regulatory' in str(step).lower() for step in chain['steps']):
            implications.append("Regulatory changes can trigger widespread market effects")
        
        return implications


if __name__ == "__main__":
    print("Cross-Domain Intelligence Enhancer initialized")
    print("Ready to expand intelligence relationships")
