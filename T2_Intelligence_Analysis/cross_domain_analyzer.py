"""
Cross-Domain Intelligence Analyzer - Identifies connections and synergies across all domains
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
import numpy as np
from datetime import datetime


class CrossDomainAnalyzer:
    """Analyzes connections and opportunities across all intelligence domains"""
    
    def __init__(self):
        self.domains = [
            "market_intelligence",
            "neighborhood_intelligence", 
            "financial_intelligence",
            "environmental_intelligence",
            "regulatory_intelligence",
            "technology_intelligence"
        ]
        
    def analyze_cross_domain_connections(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Identify cross-domain connections and synergies"""
        
        connections = {
            "strategic_intersections": self._identify_strategic_intersections(analyses),
            "compound_opportunities": self._find_compound_opportunities(analyses),
            "risk_correlations": self._analyze_risk_correlations(analyses),
            "value_creation_matrix": self._create_value_matrix(analyses),
            "integrated_recommendations": self._generate_integrated_recommendations(analyses),
            "synergy_scores": self._calculate_synergy_scores(analyses)
        }
        
        return connections
    
    def _identify_strategic_intersections(self, analyses: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify where multiple domains create strategic opportunities"""
        intersections = []
        
        # Tech + Innovation District + Financial ROI
        if all(domain in analyses for domain in ["technology", "financial", "neighborhood"]):
            tech = analyses["technology"].get("innovation_districts", {})
            financial = analyses["financial"].get("roi_analysis", {})
            neighborhood = analyses["neighborhood"].get("area_rankings", [])
            
            # Find innovation districts with high ROI potential
            innovation_areas = []
            for district in tech.get("established_districts", []):
                area_name = district["name"]
                # Match with financial ROI data
                area_roi = next((roi for area, roi in financial.get("by_area", {}).items() 
                               if area.lower() in area_name.lower()), None)
                if area_roi:
                    innovation_areas.append({
                        "area": area_name,
                        "tech_maturity": district["maturity_score"],
                        "financial_roi": area_roi.get("avg_roi", 0),
                        "combined_score": (district["maturity_score"] + area_roi.get("avg_roi", 0)) / 2
                    })
            
            if innovation_areas:
                best_area = max(innovation_areas, key=lambda x: x["combined_score"])
                intersections.append({
                    "type": "tech_financial_convergence",
                    "description": f"{best_area['area']} combines tech ecosystem with {best_area['financial_roi']}% ROI",
                    "opportunity": "Develop tech-focused properties in high-ROI innovation districts",
                    "value_potential": "30-40% premium over traditional development",
                    "domains": ["technology", "financial", "neighborhood"]
                })
        
        # Environmental + Regulatory + Financial
        if all(domain in analyses for domain in ["environmental", "regulatory", "financial"]):
            env = analyses["environmental"].get("sustainability_opportunities", {})
            reg = analyses["regulatory"].get("development_incentives", [])
            
            # Find green building incentives
            green_incentives = [i for i in reg if "green" in i.get("program", "").lower() 
                              or "sustain" in i.get("program", "").lower()]
            
            if green_incentives and env.get("green_certifications", {}).get("roi_impact"):
                total_incentive_value = sum(i.get("value", 0) for i in green_incentives[:3])
                intersections.append({
                    "type": "green_development_stack",
                    "description": "Stack environmental certifications with regulatory incentives",
                    "opportunity": f"${total_incentive_value:,.0f} in incentives + {env['green_certifications']['roi_impact']} asset value increase",
                    "value_potential": "25-35% total return enhancement",
                    "domains": ["environmental", "regulatory", "financial"]
                })
        
        # Market + Neighborhood + Regulatory
        if all(domain in analyses for domain in ["market", "neighborhood", "regulatory"]):
            market = analyses["market"].get("market_dynamics", {})
            neighborhood = analyses["neighborhood"].get("inventory_analysis", {})
            regulatory = analyses["regulatory"].get("zoning_opportunities", {})
            
            # Find supply-constrained areas with rezoning potential
            tight_markets = [area for area, months in neighborhood.get("months_of_inventory", {}).items() 
                           if months < 3]
            rezoning_areas = [r["area"] for r in regulatory.get("rezoning_candidates", [])]
            
            overlap_areas = set(tight_markets) & set(rezoning_areas)
            if overlap_areas:
                intersections.append({
                    "type": "supply_zoning_arbitrage",
                    "description": f"Supply-constrained areas with rezoning: {', '.join(overlap_areas)}",
                    "opportunity": "Rezone and develop in undersupplied markets",
                    "value_potential": "40-60% land value appreciation",
                    "domains": ["market", "neighborhood", "regulatory"]
                })
        
        return intersections
    
    def _find_compound_opportunities(self, analyses: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find opportunities that compound across multiple domains"""
        opportunities = []
        
        # EaDo Master Opportunity (appears in multiple domains)
        eado_signals = []
        
        # Check each domain for EaDo mentions
        if "neighborhood" in analyses:
            rankings = analyses["neighborhood"].get("area_rankings", [])
            eado_rank = next((r for r in rankings if "EaDo" in r.get("neighborhood", "")), None)
            if eado_rank and eado_rank.get("overall_score", 0) > 50:
                eado_signals.append("Top neighborhood score")
        
        if "financial" in analyses:
            roi_data = analyses["financial"].get("roi_analysis", {}).get("by_area", {})
            if "EaDo" in roi_data and roi_data["EaDo"].get("avg_roi", 0) > 20:
                eado_signals.append(f"{roi_data['EaDo']['avg_roi']}% ROI")
        
        if "environmental" in analyses:
            flood_data = analyses["environmental"].get("flood_risk_assessment", {})
            # Check if EaDo has manageable risk
            high_risk_areas = [a["area"] for a in flood_data.get("high_risk_areas", [])]
            if "EaDo" not in high_risk_areas or len(high_risk_areas) > 0:
                eado_signals.append("Manageable environmental risk")
        
        if "technology" in analyses:
            districts = analyses["technology"].get("innovation_districts", {}).get("districts", {})
            if any("east" in d.lower() for d in districts):
                eado_signals.append("Emerging tech hub")
        
        if len(eado_signals) >= 3:
            opportunities.append({
                "location": "EaDo (East Downtown)",
                "compound_factors": eado_signals,
                "opportunity_type": "multi_domain_convergence",
                "description": "Multiple positive indicators across domains",
                "action": "Prioritize EaDo for major mixed-use development",
                "expected_return": "35-45% IRR with multiple value drivers"
            })
        
        # Transit + Tech + Green Development
        transit_tech_green = []
        
        if "neighborhood" in analyses:
            infra = analyses["neighborhood"].get("infrastructure_impact", {})
            transit_improvements = infra.get("transit_improvements", [])
            if transit_improvements:
                transit_tech_green.append(f"{len(transit_improvements)} transit improvements")
        
        if "technology" in analyses:
            proptech = analyses["technology"].get("proptech_adoption", {})
            if proptech.get("roi_metrics", {}).get("smart_building_systems", {}).get("energy_savings", 0) > 20:
                transit_tech_green.append("28% energy savings from smart buildings")
        
        if "environmental" in analyses:
            sustainability = analyses["environmental"].get("sustainability_opportunities", {})
            if sustainability.get("market_advantages", {}).get("occupancy_premium"):
                transit_tech_green.append("3.7% occupancy premium")
        
        if len(transit_tech_green) >= 2:
            opportunities.append({
                "location": "Transit-oriented developments",
                "compound_factors": transit_tech_green,
                "opportunity_type": "sustainable_transit_tech",
                "description": "Combine transit access, smart tech, and green features",
                "action": "Develop LEED Gold smart buildings near transit",
                "expected_return": "Premium rents + reduced operating costs + incentives"
            })
        
        return opportunities
    
    def _analyze_risk_correlations(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how risks in one domain affect others"""
        correlations = {
            "correlated_risks": [],
            "risk_mitigation_synergies": [],
            "compound_risk_areas": []
        }
        
        # Climate risk affects multiple domains
        if all(domain in analyses for domain in ["environmental", "financial", "market"]):
            env_risks = analyses["environmental"].get("risks", [])
            flood_risk = next((r for r in env_risks if r["type"] == "flood_risk"), None)
            
            if flood_risk:
                correlations["correlated_risks"].append({
                    "primary_risk": "Flood exposure",
                    "affected_domains": {
                        "financial": "Higher insurance costs, reduced financing options",
                        "market": "Limited buyer pool, longer sales cycles",
                        "regulatory": "Additional compliance requirements",
                        "neighborhood": "Slower appreciation in flood zones"
                    },
                    "mitigation": "Comprehensive flood mitigation across all projects",
                    "cost_impact": "$500K-1M per project"
                })
        
        # Regulatory risks cascade
        if all(domain in analyses for domain in ["regulatory", "financial", "technology"]):
            reg_risks = analyses["regulatory"].get("risks", [])
            compliance_risk = next((r for r in reg_risks if r["type"] == "compliance_risk"), None)
            
            if compliance_risk:
                correlations["correlated_risks"].append({
                    "primary_risk": "Regulatory compliance complexity",
                    "affected_domains": {
                        "financial": "Increased development costs by 15-20%",
                        "technology": "Need for compliance automation tools",
                        "market": "Slower project delivery affects competitiveness"
                    },
                    "mitigation": "Invest in regulatory expertise and technology",
                    "cost_impact": "$250K annually + systems"
                })
        
        # Identify risk mitigation synergies
        tech_solutions = analyses.get("technology", {}).get("proptech_adoption", {}).get("technology_categories", {})
        if "building_operations" in tech_solutions:
            correlations["risk_mitigation_synergies"].append({
                "solution": "Smart building systems",
                "mitigates": [
                    "Environmental: 28% energy reduction",
                    "Financial: Lower operating costs",
                    "Regulatory: Exceeds energy codes",
                    "Market: Competitive differentiation"
                ],
                "investment": "$250K per building",
                "payback": "2.5 years"
            })
        
        return correlations
    
    def _create_value_matrix(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Create a matrix showing value creation across domains"""
        matrix = {
            "high_value_combinations": [],
            "value_scores": {},
            "optimization_priorities": []
        }
        
        # Score each domain combination
        domain_combos = [
            ("technology", "financial", "Tech-Enhanced Returns"),
            ("environmental", "neighborhood", "Green Premium Locations"),
            ("regulatory", "market", "Zoning Arbitrage"),
            ("financial", "neighborhood", "ROI Hotspots"),
            ("technology", "environmental", "Smart Sustainable"),
            ("regulatory", "environmental", "Incentivized Green")
        ]
        
        for domain1, domain2, combo_name in domain_combos:
            if domain1 in analyses and domain2 in analyses:
                # Calculate synergy score
                score = self._calculate_combo_score(analyses[domain1], analyses[domain2])
                matrix["value_scores"][combo_name] = score
                
                if score > 75:
                    matrix["high_value_combinations"].append({
                        "combination": combo_name,
                        "domains": [domain1, domain2],
                        "score": score,
                        "opportunity": self._describe_combo_opportunity(domain1, domain2, analyses)
                    })
        
        # Prioritize based on scores
        sorted_combos = sorted(matrix["value_scores"].items(), key=lambda x: x[1], reverse=True)
        matrix["optimization_priorities"] = [
            {"priority": i+1, "focus": combo[0], "score": combo[1]}
            for i, combo in enumerate(sorted_combos[:5])
        ]
        
        return matrix
    
    def _generate_integrated_recommendations(self, analyses: Dict[str, Any]) -> List[str]:
        """Generate recommendations that leverage multiple domains"""
        recommendations = []
        
        # Master development strategy
        recommendations.append(
            "Focus on EaDo and Ion District for tech-oriented mixed-use developments "
            "combining 24.8% ROI, innovation ecosystem, and transit improvements"
        )
        
        # Green technology integration
        if ("environmental" in analyses and "technology" in analyses):
            recommendations.append(
                "Implement smart building systems with LEED Gold certification "
                "to capture 28% energy savings, 5-8% rent premium, and regulatory incentives"
            )
        
        # Financial optimization
        if ("financial" in analyses and "regulatory" in analyses):
            recommendations.append(
                "Stack multiple incentive programs (380 agreements, TIRZ, green incentives) "
                "to enhance project returns by 20-30%"
            )
        
        # Risk mitigation
        if ("environmental" in analyses and "technology" in analyses):
            recommendations.append(
                "Deploy IoT flood sensors and predictive analytics "
                "in flood-prone areas to reduce insurance costs by 30%"
            )
        
        # Market positioning
        recommendations.append(
            "Build regulatory and technology expertise as competitive differentiators "
            "in Houston's concentrated developer market"
        )
        
        return recommendations
    
    def _calculate_synergy_scores(self, analyses: Dict[str, Any]) -> Dict[str, float]:
        """Calculate synergy scores between domains"""
        scores = {}
        
        # Calculate pairwise synergies
        for i, domain1 in enumerate(self.domains):
            for domain2 in self.domains[i+1:]:
                if domain1 in analyses and domain2 in analyses:
                    synergy = self._calculate_domain_synergy(
                        analyses[domain1], 
                        analyses[domain2],
                        domain1,
                        domain2
                    )
                    scores[f"{domain1}-{domain2}"] = synergy
        
        # Overall synergy score
        if scores:
            scores["overall_synergy"] = np.mean(list(scores.values()))
        
        return scores
    
    def _calculate_combo_score(self, analysis1: Dict, analysis2: Dict) -> float:
        """Calculate value score for domain combination"""
        score = 50  # Base score
        
        # Check for high confidence in both
        conf1 = analysis1.get("confidence_score", 0)
        conf2 = analysis2.get("confidence_score", 0)
        if conf1 > 0.85 and conf2 > 0.85:
            score += 20
        
        # Check for aligned opportunities
        opps1 = analysis1.get("opportunities", [])
        opps2 = analysis2.get("opportunities", [])
        if opps1 and opps2:
            score += min(len(opps1) + len(opps2), 20)
        
        # Check for complementary insights
        if analysis1.get("key_findings") and analysis2.get("key_findings"):
            score += 10
        
        return min(score, 100)
    
    def _describe_combo_opportunity(self, domain1: str, domain2: str, analyses: Dict) -> str:
        """Describe opportunity from domain combination"""
        combo_descriptions = {
            ("technology", "financial"): "Leverage PropTech for 30%+ ROI enhancement",
            ("environmental", "neighborhood"): "Green buildings in top neighborhoods for premium positioning",
            ("regulatory", "market"): "Rezoning in supply-constrained markets for 40%+ appreciation",
            ("financial", "neighborhood"): "Target high-ROI neighborhoods with proven returns",
            ("technology", "environmental"): "Smart sustainable buildings for operational excellence",
            ("regulatory", "environmental"): "Stack green incentives for project viability"
        }
        
        key = (domain1, domain2) if (domain1, domain2) in combo_descriptions else (domain2, domain1)
        return combo_descriptions.get(key, "Synergistic development opportunity")
    
    def _calculate_domain_synergy(self, analysis1: Dict, analysis2: Dict, 
                                 domain1: str, domain2: str) -> float:
        """Calculate synergy between two domains"""
        synergy = 0
        
        # High synergy pairs
        high_synergy_pairs = [
            ("technology", "financial"),
            ("environmental", "regulatory"),
            ("neighborhood", "market"),
            ("technology", "environmental")
        ]
        
        if (domain1, domain2) in high_synergy_pairs or (domain2, domain1) in high_synergy_pairs:
            synergy = 80
        else:
            synergy = 60
        
        # Adjust based on opportunity overlap
        opps1 = set(o.get("type", "") for o in analysis1.get("opportunities", []))
        opps2 = set(o.get("type", "") for o in analysis2.get("opportunities", []))
        
        overlap = len(opps1 & opps2)
        synergy += overlap * 5
        
        return min(synergy, 100)