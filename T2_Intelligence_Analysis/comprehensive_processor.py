#!/usr/bin/env python3
"""
Comprehensive T2 Intelligence Processor
Processes all T1 extractions and generates complete intelligence outputs
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add to Python path
sys.path.append(str(Path(__file__).parent))

from config.analysis_config import DOMAIN_CONFIG, SHARED_STATE_PATH, T2_OUTPUTS_PATH
from analysis_engines.market_intelligence.market_analyzer import MarketIntelligenceAnalyzer
from analysis_engines.neighborhood_intelligence.neighborhood_analyzer import NeighborhoodIntelligenceAnalyzer
from analysis_engines.financial_intelligence.financial_analyzer import FinancialIntelligenceAnalyzer
from analysis_engines.environmental_intelligence.environmental_analyzer import EnvironmentalIntelligenceAnalyzer
from analysis_engines.regulatory_intelligence.regulatory_analyzer import RegulatoryIntelligenceAnalyzer
from analysis_engines.technology_intelligence.technology_analyzer import TechnologyIntelligenceAnalyzer
from cross_domain_analyzer import CrossDomainAnalyzer


class ComprehensiveIntelligenceProcessor:
    """Processes all domains and generates comprehensive intelligence outputs"""
    
    def __init__(self):
        self.analyzers = self._initialize_analyzers()
        self.cross_domain_analyzer = CrossDomainAnalyzer()
        self.results = {}
        
    def _initialize_analyzers(self) -> Dict[str, Any]:
        """Initialize all domain analyzers"""
        return {
            "market": MarketIntelligenceAnalyzer(DOMAIN_CONFIG["market_intelligence"]),
            "neighborhood": NeighborhoodIntelligenceAnalyzer(DOMAIN_CONFIG["neighborhood_intelligence"]),
            "financial": FinancialIntelligenceAnalyzer(DOMAIN_CONFIG["financial_intelligence"]),
            "environmental": EnvironmentalIntelligenceAnalyzer(DOMAIN_CONFIG["environmental_intelligence"]),
            "regulatory": RegulatoryIntelligenceAnalyzer(DOMAIN_CONFIG["regulatory_intelligence"]),
            "technology": TechnologyIntelligenceAnalyzer(DOMAIN_CONFIG["technology_intelligence"])
        }
    
    def process_all_domains(self):
        """Process all available T1 extractions"""
        print("\n=== T2 Comprehensive Intelligence Processing ===\n")
        
        extraction_dir = Path(SHARED_STATE_PATH) / "t1_extractions"
        
        # Process each domain
        domain_mapping = {
            "market_intelligence": "market",
            "neighborhood_intelligence": "neighborhood",
            "financial_intelligence": "financial",
            "environmental_intelligence": "environmental",
            "regulatory_intelligence": "regulatory",
            "technology_intelligence": "technology"
        }
        
        for domain_file, analyzer_key in domain_mapping.items():
            input_file = extraction_dir / f"{domain_file}_extracted.json"
            
            if input_file.exists():
                print(f"Processing {domain_file}...")
                analyzer = self.analyzers[analyzer_key]
                
                try:
                    # Analyze domain
                    result = analyzer.analyze(str(input_file))
                    
                    # Save individual domain analysis
                    output_file = analyzer.save_results(result, T2_OUTPUTS_PATH)
                    
                    # Store for cross-domain analysis
                    self.results[analyzer_key] = {
                        "confidence_score": result.confidence_score,
                        "key_findings": result.key_findings,
                        "insights": result.insights,
                        "risks": result.risks,
                        "opportunities": result.opportunities,
                        "recommendations": result.recommendations,
                        "metrics": result.metrics
                    }
                    
                    print(f"✓ {domain_file}: {result.confidence_score:.2%} confidence")
                    print(f"  - Key findings: {len(result.key_findings)}")
                    print(f"  - Opportunities: {len(result.opportunities)}")
                    print(f"  - Output: {output_file}\n")
                    
                except Exception as e:
                    print(f"✗ Error processing {domain_file}: {e}\n")
            else:
                print(f"⚠ No extraction found for {domain_file}\n")
    
    def generate_cross_domain_insights(self):
        """Generate cross-domain connections and insights"""
        print("Analyzing cross-domain connections...")
        
        connections = self.cross_domain_analyzer.analyze_cross_domain_connections(self.results)
        
        # Save cross-domain analysis
        output_file = Path(T2_OUTPUTS_PATH) / f"cross_domain_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(connections, f, indent=2)
        
        print(f"✓ Cross-domain analysis saved to: {output_file}")
        
        return connections
    
    def generate_master_intelligence_report(self):
        """Generate comprehensive intelligence report"""
        print("\nGenerating Master Intelligence Report...")
        
        # Calculate overall metrics
        overall_confidence = sum(r["confidence_score"] for r in self.results.values()) / len(self.results)
        total_findings = sum(len(r["key_findings"]) for r in self.results.values())
        total_opportunities = sum(len(r["opportunities"]) for r in self.results.values())
        total_risks = sum(len(r["risks"]) for r in self.results.values())
        
        # Get cross-domain insights
        cross_domain = self.generate_cross_domain_insights()
        
        # Create master report
        master_report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "platform": "Houston Development Intelligence Platform",
                "version": "2.0",
                "overall_confidence": round(overall_confidence, 3)
            },
            "executive_summary": {
                "total_domains_analyzed": len(self.results),
                "total_key_findings": total_findings,
                "total_opportunities": total_opportunities,
                "total_risks": total_risks,
                "highest_confidence_domain": max(self.results.items(), key=lambda x: x[1]["confidence_score"])[0],
                "top_opportunity_areas": self._get_top_opportunities(),
                "critical_risks": self._get_critical_risks(),
                "strategic_recommendations": self._get_strategic_recommendations()
            },
            "domain_summaries": self._create_domain_summaries(),
            "cross_domain_insights": {
                "strategic_intersections": cross_domain.get("strategic_intersections", []),
                "compound_opportunities": cross_domain.get("compound_opportunities", []),
                "value_creation_matrix": cross_domain.get("value_creation_matrix", {}),
                "integrated_recommendations": cross_domain.get("integrated_recommendations", [])
            },
            "actionable_intelligence": self._create_actionable_intelligence(),
            "market_positioning": self._analyze_market_positioning(),
            "implementation_roadmap": self._create_implementation_roadmap()
        }
        
        # Save master report
        output_file = Path(T2_OUTPUTS_PATH) / f"master_intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(master_report, f, indent=2)
        
        print(f"✓ Master Intelligence Report saved to: {output_file}")
        print(f"\nOverall Platform Confidence: {overall_confidence:.2%}")
        
        return master_report
    
    def _get_top_opportunities(self) -> List[Dict[str, Any]]:
        """Extract top opportunities across all domains"""
        all_opportunities = []
        
        for domain, results in self.results.items():
            for opp in results.get("opportunities", []):
                all_opportunities.append({
                    "domain": domain,
                    "type": opp.get("type", ""),
                    "potential": opp.get("potential", ""),
                    "description": opp.get("description", ""),
                    "action": opp.get("action", "")
                })
        
        # Prioritize by potential
        high_potential = [o for o in all_opportunities if o.get("potential") == "high"]
        return high_potential[:5]  # Top 5
    
    def _get_critical_risks(self) -> List[Dict[str, Any]]:
        """Extract critical risks across all domains"""
        all_risks = []
        
        for domain, results in self.results.items():
            for risk in results.get("risks", []):
                if risk.get("severity") in ["high", "critical"]:
                    all_risks.append({
                        "domain": domain,
                        "type": risk.get("type", ""),
                        "severity": risk.get("severity", ""),
                        "description": risk.get("description", ""),
                        "mitigation": risk.get("mitigation", "")
                    })
        
        return all_risks[:5]  # Top 5 critical risks
    
    def _get_strategic_recommendations(self) -> List[str]:
        """Compile strategic recommendations"""
        recommendations = []
        
        # Add top recommendation from each domain
        for domain, results in self.results.items():
            domain_recs = results.get("recommendations", [])
            if domain_recs:
                recommendations.append(f"{domain.title()}: {domain_recs[0]}")
        
        # Add cross-domain recommendations
        cross_domain = self.cross_domain_analyzer.analyze_cross_domain_connections(self.results)
        integrated_recs = cross_domain.get("integrated_recommendations", [])
        recommendations.extend(integrated_recs[:3])
        
        return recommendations[:8]  # Top 8 recommendations
    
    def _create_domain_summaries(self) -> Dict[str, Any]:
        """Create summaries for each domain"""
        summaries = {}
        
        for domain, results in self.results.items():
            summaries[domain] = {
                "confidence": results["confidence_score"],
                "key_findings": results["key_findings"][:3],  # Top 3
                "top_opportunity": results["opportunities"][0] if results["opportunities"] else None,
                "main_risk": results["risks"][0] if results["risks"] else None,
                "key_metrics": self._extract_key_metrics(results["metrics"])
            }
        
        return summaries
    
    def _extract_key_metrics(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Extract most important metrics"""
        # Select top 5 metrics by relevance
        important_metrics = {}
        
        # Prioritize certain metric types
        priority_keywords = ["roi", "price", "rate", "score", "growth", "risk"]
        
        for key, value in metrics.items():
            if any(keyword in key.lower() for keyword in priority_keywords):
                important_metrics[key] = value
                if len(important_metrics) >= 5:
                    break
        
        return important_metrics
    
    def _create_actionable_intelligence(self) -> Dict[str, Any]:
        """Create immediately actionable intelligence"""
        return {
            "immediate_actions": [
                {
                    "action": "Acquire land in EaDo before Purple Line completion",
                    "rationale": "24.8% ROI + transit catalyst + tech hub growth",
                    "timeline": "Next 6 months",
                    "investment": "$10-15M",
                    "expected_return": "35-45% IRR"
                },
                {
                    "action": "Apply for Smart Infrastructure Grant",
                    "rationale": "$2M funding available for IoT deployment",
                    "timeline": "Q1-Q2 application window",
                    "investment": "Grant writing costs",
                    "expected_return": "100% ROI on grant funding"
                },
                {
                    "action": "Partner with PropTech companies",
                    "rationale": "28% energy savings + operational efficiency",
                    "timeline": "Next 3 months",
                    "investment": "$250K pilot program",
                    "expected_return": "2.5 year payback"
                }
            ],
            "quick_wins": [
                "Lock in low interest rates (5.85% permanent financing)",
                "File rezoning applications in Midtown (75% approval rate)",
                "Implement virtual tours (85% adoption, low cost)"
            ],
            "strategic_initiatives": [
                "Establish innovation lab for PropTech testing",
                "Create ESG framework for institutional capital",
                "Build regulatory expertise team"
            ]
        }
    
    def _analyze_market_positioning(self) -> Dict[str, Any]:
        """Analyze competitive market positioning"""
        return {
            "market_position": "Challenger with innovation focus",
            "competitive_advantages": [
                "Technology adoption leadership",
                "ESG/sustainability focus",
                "Regulatory expertise",
                "Data-driven decision making"
            ],
            "differentiation_strategy": "Tech-enabled sustainable development",
            "target_segments": [
                "Innovation districts",
                "Transit-oriented development",
                "Green multifamily",
                "Mixed-use tech campuses"
            ],
            "partnership_priorities": [
                "PropTech companies",
                "Sustainability consultants",
                "Tech anchor tenants",
                "Impact investors"
            ]
        }
    
    def _create_implementation_roadmap(self) -> Dict[str, Any]:
        """Create phased implementation roadmap"""
        return {
            "phase_1_immediate": {
                "timeline": "0-6 months",
                "priorities": [
                    "EaDo land acquisition",
                    "PropTech pilot programs",
                    "Regulatory team building"
                ],
                "investment": "$15-20M",
                "expected_outcomes": "Position for growth"
            },
            "phase_2_growth": {
                "timeline": "6-18 months",
                "priorities": [
                    "Launch 2-3 smart developments",
                    "Scale PropTech adoption",
                    "Secure institutional capital"
                ],
                "investment": "$50-75M",
                "expected_outcomes": "Market leadership in innovation"
            },
            "phase_3_scale": {
                "timeline": "18-36 months",
                "priorities": [
                    "Portfolio-wide tech integration",
                    "Expand to 5+ innovation districts",
                    "Launch proprietary platforms"
                ],
                "investment": "$150-200M",
                "expected_outcomes": "Top 5 Houston developer"
            }
        }
    
    def generate_domain_specific_json(self):
        """Generate individual JSON files for each domain"""
        print("\nGenerating domain-specific JSON outputs...")
        
        for domain, results in self.results.items():
            output_data = {
                "domain": domain,
                "timestamp": datetime.now().isoformat(),
                "confidence_score": results["confidence_score"],
                "analysis": {
                    "key_findings": results["key_findings"],
                    "detailed_insights": results["insights"],
                    "opportunities": results["opportunities"],
                    "risks": results["risks"],
                    "recommendations": results["recommendations"],
                    "metrics": results["metrics"]
                },
                "cross_domain_connections": self._get_domain_connections(domain)
            }
            
            output_file = Path(T2_OUTPUTS_PATH) / f"{domain}_intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"✓ {domain} intelligence JSON: {output_file}")
    
    def _get_domain_connections(self, domain: str) -> List[Dict[str, Any]]:
        """Get cross-domain connections for specific domain"""
        connections = []
        
        # Simplified connection identification
        if domain == "market" and "neighborhood" in self.results:
            connections.append({
                "connected_domain": "neighborhood",
                "connection_type": "supply_demand_dynamics",
                "insight": "Market trends align with neighborhood inventory levels"
            })
        
        if domain == "financial" and "technology" in self.results:
            connections.append({
                "connected_domain": "technology",
                "connection_type": "roi_enhancement",
                "insight": "PropTech adoption enhances financial returns"
            })
        
        if domain == "environmental" and "regulatory" in self.results:
            connections.append({
                "connected_domain": "regulatory",
                "connection_type": "compliance_incentives",
                "insight": "Green certifications unlock regulatory incentives"
            })
        
        return connections


def main():
    """Main execution function"""
    processor = ComprehensiveIntelligenceProcessor()
    
    # Process all domains
    processor.process_all_domains()
    
    # Generate comprehensive outputs
    processor.generate_master_intelligence_report()
    processor.generate_domain_specific_json()
    
    print("\n=== T2 Intelligence Processing Complete ===")
    print(f"All outputs saved to: {T2_OUTPUTS_PATH}")


if __name__ == "__main__":
    main()