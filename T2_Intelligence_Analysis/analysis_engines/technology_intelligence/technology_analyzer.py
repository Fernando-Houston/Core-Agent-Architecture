"""
Technology Intelligence Analyzer - PropTech, innovation districts, and smart city opportunities
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from analysis_engines.base_analyzer import BaseIntelligenceAnalyzer


class TechnologyIntelligenceAnalyzer(BaseIntelligenceAnalyzer):
    """Analyzes technology trends, innovation opportunities, and smart city initiatives"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("technology_intelligence", config)
        
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform technology-specific analysis"""
        insights = {
            "innovation_districts": self._analyze_innovation_districts(data),
            "proptech_adoption": self._analyze_proptech_trends(data),
            "smart_city_opportunities": self._identify_smart_city_opportunities(data),
            "tech_infrastructure": self._assess_tech_infrastructure(data),
            "digital_transformation": self._evaluate_digital_transformation(data),
            "investment_landscape": self._analyze_tech_investment(data),
            "competitive_positioning": self._assess_competitive_tech_position(data)
        }
        return insights
    
    def _analyze_innovation_districts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze innovation district opportunities and ecosystem strength"""
        innovation_data = data.get("aggregated_data", {}).get("innovation_districts", {})
        
        district_analysis = {
            "established_districts": [],
            "emerging_districts": [],
            "ecosystem_strength": {},
            "development_opportunities": [],
            "anchor_tenants": {}
        }
        
        # Analyze established districts
        districts = innovation_data.get("districts", {})
        for district, metrics in districts.items():
            if isinstance(metrics, dict):
                maturity_score = self._calculate_district_maturity(metrics)
                
                district_profile = {
                    "name": district,
                    "tech_companies": metrics.get("company_count", 0),
                    "employment": metrics.get("tech_employment", 0),
                    "growth_rate": metrics.get("growth_rate", 0),
                    "vacancy_rate": metrics.get("vacancy_rate", 0),
                    "avg_rent_psf": metrics.get("avg_rent", 0),
                    "maturity_score": maturity_score,
                    "key_sectors": metrics.get("focus_sectors", []),
                    "infrastructure_score": metrics.get("infrastructure_rating", 0)
                }
                
                if maturity_score > 70:
                    district_analysis["established_districts"].append(district_profile)
                else:
                    district_analysis["emerging_districts"].append(district_profile)
                
                # Identify anchor tenants
                if metrics.get("anchor_companies"):
                    district_analysis["anchor_tenants"][district] = metrics["anchor_companies"]
        
        # Ecosystem strength assessment
        ecosystem = innovation_data.get("ecosystem_metrics", {})
        district_analysis["ecosystem_strength"] = {
            "university_partnerships": ecosystem.get("university_connections", []),
            "accelerators": ecosystem.get("accelerator_count", 0),
            "vc_presence": ecosystem.get("vc_firms", 0),
            "talent_pipeline": self._assess_talent_pipeline(ecosystem),
            "startup_density": ecosystem.get("startups_per_sqmi", 0),
            "funding_availability": ecosystem.get("annual_vc_funding", 0)
        }
        
        # Development opportunities
        opportunities = innovation_data.get("development_pipeline", [])
        for opp in opportunities:
            if isinstance(opp, dict) and opp.get("tech_focus", False):
                district_analysis["development_opportunities"].append({
                    "project": opp.get("name", ""),
                    "location": opp.get("district", ""),
                    "size_sf": opp.get("square_feet", 0),
                    "completion": opp.get("completion_date", ""),
                    "pre_leasing": opp.get("pre_lease_pct", 0),
                    "tech_amenities": opp.get("smart_features", []),
                    "target_tenants": opp.get("target_sectors", [])
                })
        
        return district_analysis
    
    def _analyze_proptech_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze PropTech adoption and opportunities"""
        proptech_data = data.get("aggregated_data", {}).get("proptech", {})
        
        proptech_analysis = {
            "adoption_rates": {},
            "technology_categories": {},
            "roi_metrics": {},
            "implementation_barriers": [],
            "market_leaders": []
        }
        
        # Adoption rates by technology
        adoption = proptech_data.get("adoption_metrics", {})
        for tech, metrics in adoption.items():
            if isinstance(metrics, dict):
                proptech_analysis["adoption_rates"][tech] = {
                    "current_adoption": metrics.get("adoption_rate", 0),
                    "growth_rate": metrics.get("yoy_growth", 0),
                    "market_penetration": metrics.get("penetration", 0),
                    "projected_2025": metrics.get("adoption_rate", 0) * (1 + metrics.get("yoy_growth", 0) / 100),
                    "maturity": self._assess_tech_maturity(metrics)
                }
        
        # Technology categories and use cases
        categories = proptech_data.get("tech_categories", {})
        for category, details in categories.items():
            if isinstance(details, dict):
                proptech_analysis["technology_categories"][category] = {
                    "solutions": details.get("solutions", []),
                    "avg_cost": details.get("implementation_cost", 0),
                    "payback_period": details.get("payback_months", 0),
                    "primary_benefits": details.get("benefits", []),
                    "adoption_difficulty": details.get("complexity", "medium"),
                    "market_size": details.get("market_value", 0)
                }
        
        # ROI metrics
        roi_data = proptech_data.get("roi_analysis", {})
        proptech_analysis["roi_metrics"] = {
            "smart_building_systems": {
                "energy_savings": roi_data.get("smart_building", {}).get("energy_reduction", 0),
                "operational_savings": roi_data.get("smart_building", {}).get("opex_reduction", 0),
                "tenant_satisfaction": roi_data.get("smart_building", {}).get("satisfaction_increase", 0),
                "payback_years": roi_data.get("smart_building", {}).get("payback", 0)
            },
            "property_management_tech": {
                "efficiency_gain": roi_data.get("prop_mgmt", {}).get("efficiency", 0),
                "cost_reduction": roi_data.get("prop_mgmt", {}).get("cost_savings", 0),
                "revenue_increase": roi_data.get("prop_mgmt", {}).get("revenue_lift", 0)
            },
            "construction_tech": {
                "time_savings": roi_data.get("construction", {}).get("schedule_reduction", 0),
                "cost_savings": roi_data.get("construction", {}).get("cost_reduction", 0),
                "quality_improvement": roi_data.get("construction", {}).get("defect_reduction", 0)
            }
        }
        
        # Implementation barriers
        barriers = proptech_data.get("adoption_barriers", [])
        proptech_analysis["implementation_barriers"] = [
            {"barrier": b["name"], "impact": b["severity"], "mitigation": b["solution"]}
            for b in barriers if isinstance(b, dict)
        ]
        
        return proptech_analysis
    
    def _identify_smart_city_opportunities(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify smart city initiatives and integration opportunities"""
        smart_city_data = data.get("aggregated_data", {}).get("smart_city", {})
        
        opportunities = {
            "city_initiatives": [],
            "integration_points": {},
            "funding_programs": [],
            "pilot_opportunities": [],
            "public_private_partnerships": []
        }
        
        # Active city initiatives
        initiatives = smart_city_data.get("active_programs", [])
        for program in initiatives:
            if isinstance(program, dict):
                opportunities["city_initiatives"].append({
                    "program": program.get("name", ""),
                    "focus_area": program.get("category", ""),
                    "budget": program.get("annual_budget", 0),
                    "timeline": program.get("implementation_timeline", ""),
                    "private_sector_role": program.get("private_participation", ""),
                    "development_impact": program.get("real_estate_benefit", "")
                })
        
        # Integration points for developers
        integration = smart_city_data.get("developer_integration", {})
        opportunities["integration_points"] = {
            "smart_infrastructure": {
                "requirements": integration.get("infrastructure_standards", []),
                "incentives": integration.get("infrastructure_incentives", []),
                "certification": integration.get("smart_building_cert", "")
            },
            "data_sharing": {
                "platforms": integration.get("city_platforms", []),
                "requirements": integration.get("data_requirements", []),
                "benefits": integration.get("data_sharing_benefits", [])
            },
            "sustainability": {
                "targets": integration.get("sustainability_goals", []),
                "reporting": integration.get("reporting_requirements", []),
                "recognition": integration.get("recognition_programs", [])
            }
        }
        
        # Funding and pilot programs
        funding = smart_city_data.get("funding_opportunities", [])
        for fund in funding:
            if isinstance(fund, dict):
                opportunities["funding_programs"].append({
                    "program": fund.get("name", ""),
                    "funding_amount": fund.get("max_funding", 0),
                    "eligible_projects": fund.get("eligible_types", []),
                    "application_window": fund.get("application_period", ""),
                    "success_rate": fund.get("approval_rate", 0),
                    "matching_required": fund.get("match_requirement", False)
                })
        
        # Public-private partnership opportunities
        ppp = smart_city_data.get("ppp_opportunities", [])
        for partnership in ppp:
            if isinstance(partnership, dict):
                opportunities["public_private_partnerships"].append({
                    "project": partnership.get("name", ""),
                    "scope": partnership.get("description", ""),
                    "investment_required": partnership.get("private_investment", 0),
                    "revenue_model": partnership.get("revenue_structure", ""),
                    "timeline": partnership.get("project_timeline", ""),
                    "selection_criteria": partnership.get("selection_factors", [])
                })
        
        return opportunities
    
    def _assess_tech_infrastructure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess technology infrastructure readiness"""
        infra_data = data.get("aggregated_data", {}).get("tech_infrastructure", {})
        
        infrastructure = {
            "connectivity": {},
            "data_centers": {},
            "5g_deployment": {},
            "fiber_availability": {},
            "infrastructure_gaps": []
        }
        
        # Connectivity assessment
        connectivity = infra_data.get("connectivity_metrics", {})
        infrastructure["connectivity"] = {
            "avg_broadband_speed": connectivity.get("avg_speed_mbps", 0),
            "gigabit_coverage": connectivity.get("gigabit_coverage_pct", 0),
            "provider_competition": connectivity.get("provider_count", 0),
            "reliability_score": connectivity.get("uptime_pct", 0),
            "business_grade_availability": connectivity.get("business_fiber_pct", 0)
        }
        
        # Data center presence
        data_centers = infra_data.get("data_centers", [])
        infrastructure["data_centers"] = {
            "total_facilities": len(data_centers),
            "total_capacity_mw": sum(dc.get("capacity_mw", 0) for dc in data_centers if isinstance(dc, dict)),
            "tier_4_facilities": len([dc for dc in data_centers if isinstance(dc, dict) and dc.get("tier") == 4]),
            "edge_computing": len([dc for dc in data_centers if isinstance(dc, dict) and dc.get("edge_capable", False)]),
            "avg_pue": np.mean([dc.get("pue", 2.0) for dc in data_centers if isinstance(dc, dict)])
        }
        
        # 5G deployment status
        fiveg = infra_data.get("5g_deployment", {})
        infrastructure["5g_deployment"] = {
            "coverage_pct": fiveg.get("coverage", 0),
            "carrier_deployments": fiveg.get("carriers", []),
            "small_cell_count": fiveg.get("small_cells", 0),
            "mmwave_availability": fiveg.get("mmwave_coverage", 0),
            "deployment_timeline": fiveg.get("full_coverage_date", "2025")
        }
        
        # Identify infrastructure gaps
        gaps = infra_data.get("identified_gaps", [])
        infrastructure["infrastructure_gaps"] = [
            {
                "gap": g["type"],
                "impact": g["business_impact"],
                "resolution": g["proposed_solution"],
                "timeline": g["resolution_timeline"],
                "investment_needed": g["required_investment"]
            }
            for g in gaps if isinstance(g, dict)
        ]
        
        return infrastructure
    
    def _evaluate_digital_transformation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate digital transformation opportunities in real estate"""
        digital_data = data.get("aggregated_data", {}).get("digital_transformation", {})
        
        transformation = {
            "digital_maturity": {},
            "transformation_opportunities": [],
            "technology_stack": {},
            "implementation_roadmap": [],
            "expected_outcomes": {}
        }
        
        # Industry digital maturity
        maturity = digital_data.get("industry_maturity", {})
        transformation["digital_maturity"] = {
            "current_state": maturity.get("maturity_score", 0),
            "vs_other_industries": maturity.get("relative_position", "lagging"),
            "adoption_leaders": maturity.get("leading_companies", []),
            "common_gaps": maturity.get("typical_gaps", []),
            "maturity_by_function": maturity.get("functional_scores", {})
        }
        
        # Transformation opportunities
        opportunities = digital_data.get("transformation_areas", [])
        for opp in opportunities:
            if isinstance(opp, dict):
                transformation["transformation_opportunities"].append({
                    "area": opp.get("function", ""),
                    "current_state": opp.get("current_maturity", ""),
                    "target_state": opp.get("target_maturity", ""),
                    "technologies": opp.get("enabling_tech", []),
                    "investment_required": opp.get("investment", 0),
                    "expected_roi": opp.get("roi_pct", 0),
                    "implementation_time": opp.get("timeline_months", 0)
                })
        
        # Recommended technology stack
        stack = digital_data.get("recommended_stack", {})
        transformation["technology_stack"] = {
            "core_platforms": stack.get("platforms", []),
            "integration_layer": stack.get("integration", []),
            "analytics_tools": stack.get("analytics", []),
            "automation_tools": stack.get("automation", []),
            "estimated_cost": stack.get("total_cost", 0),
            "implementation_phases": stack.get("phases", [])
        }
        
        # Expected outcomes
        outcomes = digital_data.get("expected_benefits", {})
        transformation["expected_outcomes"] = {
            "operational_efficiency": outcomes.get("efficiency_gain", 0),
            "cost_reduction": outcomes.get("cost_savings", 0),
            "revenue_growth": outcomes.get("revenue_increase", 0),
            "customer_satisfaction": outcomes.get("nps_improvement", 0),
            "competitive_advantage": outcomes.get("market_differentiation", "")
        }
        
        return transformation
    
    def _analyze_tech_investment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technology investment landscape"""
        investment_data = data.get("aggregated_data", {}).get("tech_investment", {})
        
        investment_analysis = {
            "vc_activity": {},
            "corporate_investment": {},
            "emerging_technologies": [],
            "investment_trends": {},
            "exit_opportunities": []
        }
        
        # VC investment activity
        vc_data = investment_data.get("vc_metrics", {})
        investment_analysis["vc_activity"] = {
            "annual_investment": vc_data.get("total_invested", 0),
            "deal_count": vc_data.get("deals", 0),
            "avg_deal_size": vc_data.get("avg_deal", 0),
            "growth_rate": vc_data.get("yoy_growth", 0),
            "top_investors": vc_data.get("active_vcs", []),
            "hot_sectors": vc_data.get("top_sectors", [])
        }
        
        # Corporate venture activity
        corporate = investment_data.get("corporate_venture", {})
        investment_analysis["corporate_investment"] = {
            "active_corporates": corporate.get("companies", []),
            "investment_focus": corporate.get("focus_areas", []),
            "strategic_partnerships": corporate.get("partnerships", 0),
            "acquisition_activity": corporate.get("acquisitions", []),
            "innovation_labs": corporate.get("innovation_centers", [])
        }
        
        # Emerging technologies
        emerging = investment_data.get("emerging_tech", [])
        for tech in emerging:
            if isinstance(tech, dict):
                investment_analysis["emerging_technologies"].append({
                    "technology": tech.get("name", ""),
                    "maturity": tech.get("maturity_stage", ""),
                    "investment_momentum": tech.get("investment_growth", 0),
                    "use_cases": tech.get("applications", []),
                    "adoption_timeline": tech.get("mainstream_timeline", ""),
                    "investment_opportunity": tech.get("opportunity_size", 0)
                })
        
        return investment_analysis
    
    def _assess_competitive_tech_position(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess competitive positioning through technology"""
        competitive_data = data.get("aggregated_data", {})
        
        positioning = {
            "tech_differentiators": [],
            "competitive_gaps": [],
            "strategic_recommendations": [],
            "partnership_opportunities": []
        }
        
        # Technology differentiators
        positioning["tech_differentiators"] = [
            {
                "differentiator": "AI-powered property valuation",
                "competitive_advantage": "15% more accurate pricing",
                "implementation_cost": 250000,
                "time_to_market": "6 months"
            },
            {
                "differentiator": "IoT building management",
                "competitive_advantage": "25% operational cost reduction",
                "implementation_cost": 500000,
                "time_to_market": "12 months"
            },
            {
                "differentiator": "Blockchain property transactions",
                "competitive_advantage": "50% faster closing",
                "implementation_cost": 350000,
                "time_to_market": "9 months"
            }
        ]
        
        # Competitive gaps
        gaps = competitive_data.get("tech_gaps", [])
        for gap in gaps:
            if isinstance(gap, dict):
                positioning["competitive_gaps"].append({
                    "gap": gap.get("description", ""),
                    "impact": gap.get("business_impact", ""),
                    "competitors_ahead": gap.get("leaders", []),
                    "catch_up_cost": gap.get("investment_needed", 0),
                    "urgency": gap.get("priority", "medium")
                })
        
        # Strategic recommendations
        positioning["strategic_recommendations"] = [
            "Partner with PropTech startups for rapid innovation",
            "Establish innovation lab for technology experimentation",
            "Invest in data analytics capabilities for market intelligence",
            "Develop API-first architecture for ecosystem integration",
            "Create digital customer experience platform"
        ]
        
        # Partnership opportunities
        partners = competitive_data.get("potential_partners", [])
        for partner in partners:
            if isinstance(partner, dict):
                positioning["partnership_opportunities"].append({
                    "partner": partner.get("company", ""),
                    "technology": partner.get("technology", ""),
                    "partnership_type": partner.get("structure", ""),
                    "value_proposition": partner.get("benefit", ""),
                    "integration_complexity": partner.get("complexity", "medium")
                })
        
        return positioning
    
    def _calculate_district_maturity(self, metrics: Dict[str, Any]) -> float:
        """Calculate innovation district maturity score"""
        factors = {
            "company_density": min(metrics.get("company_count", 0) / 100, 1) * 25,
            "employment_scale": min(metrics.get("tech_employment", 0) / 10000, 1) * 25,
            "growth_momentum": min(metrics.get("growth_rate", 0) / 20, 1) * 20,
            "infrastructure": metrics.get("infrastructure_rating", 0) / 10 * 15,
            "ecosystem": min(len(metrics.get("anchor_companies", [])) / 5, 1) * 15
        }
        
        return sum(factors.values())
    
    def _assess_talent_pipeline(self, ecosystem: Dict[str, Any]) -> Dict[str, Any]:
        """Assess strength of tech talent pipeline"""
        universities = ecosystem.get("university_connections", [])
        
        return {
            "university_programs": len(universities),
            "annual_tech_graduates": ecosystem.get("tech_graduates", 0),
            "bootcamp_capacity": ecosystem.get("bootcamp_grads", 0),
            "talent_retention_rate": ecosystem.get("retention_rate", 0),
            "avg_tech_salary": ecosystem.get("avg_salary", 0),
            "talent_availability": "high" if ecosystem.get("tech_graduates", 0) > 5000 else "medium"
        }
    
    def _assess_tech_maturity(self, metrics: Dict[str, Any]) -> str:
        """Assess technology maturity level"""
        adoption = metrics.get("adoption_rate", 0)
        growth = metrics.get("yoy_growth", 0)
        
        if adoption > 60:
            return "mature"
        elif adoption > 30 or growth > 50:
            return "growth"
        elif adoption > 10:
            return "early_adoption"
        else:
            return "emerging"
    
    def _extract_key_findings(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key findings from technology analysis"""
        findings = []
        
        # Innovation district findings
        districts = insights.get("innovation_districts", {})
        established = districts.get("established_districts", [])
        if established:
            top_district = max(established, key=lambda x: x.get("maturity_score", 0))
            findings.append(f"{top_district['name']} leads innovation with {top_district['tech_companies']} tech companies")
        
        # PropTech adoption
        proptech = insights.get("proptech_adoption", {})
        adoption_rates = proptech.get("adoption_rates", {})
        if adoption_rates:
            highest_adoption = max(adoption_rates.items(), key=lambda x: x[1].get("current_adoption", 0))
            findings.append(f"{highest_adoption[0]} shows {highest_adoption[1]['current_adoption']}% adoption rate")
        
        # Smart city opportunities
        smart_city = insights.get("smart_city_opportunities", {})
        if smart_city.get("city_initiatives"):
            total_budget = sum(i["budget"] for i in smart_city["city_initiatives"])
            findings.append(f"${total_budget/1e6:.1f}M in smart city funding available")
        
        # Tech infrastructure
        infrastructure = insights.get("tech_infrastructure", {})
        if infrastructure.get("connectivity", {}).get("gigabit_coverage", 0) > 80:
            findings.append("Strong tech infrastructure with 80%+ gigabit coverage")
        
        # Investment activity
        investment = insights.get("investment_landscape", {})
        vc_activity = investment.get("vc_activity", {})
        if vc_activity.get("annual_investment", 0) > 100000000:
            findings.append(f"${vc_activity['annual_investment']/1e6:.0f}M in PropTech VC investment")
        
        return findings[:5]
    
    def _identify_risks(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify technology-related risks"""
        risks = []
        
        # Technology adoption risks
        proptech = insights.get("proptech_adoption", {})
        barriers = proptech.get("implementation_barriers", [])
        if barriers:
            highest_barrier = max(barriers, key=lambda x: x.get("impact", "medium") == "high")
            risks.append({
                "type": "adoption_barrier",
                "severity": "medium",
                "description": f"Technology adoption hindered by {highest_barrier['barrier']}",
                "impact": "Slower digital transformation and competitive disadvantage",
                "mitigation": highest_barrier.get("mitigation", "Phased implementation approach")
            })
        
        # Infrastructure gaps
        infrastructure = insights.get("tech_infrastructure", {})
        gaps = infrastructure.get("infrastructure_gaps", [])
        if gaps:
            critical_gaps = [g for g in gaps if g.get("impact", "") == "high"]
            if critical_gaps:
                risks.append({
                    "type": "infrastructure_gap",
                    "severity": "high",
                    "description": f"{len(critical_gaps)} critical infrastructure gaps identified",
                    "impact": critical_gaps[0].get("impact", ""),
                    "mitigation": "Partner with infrastructure providers for accelerated deployment"
                })
        
        # Competitive technology gap
        positioning = insights.get("competitive_positioning", {})
        comp_gaps = positioning.get("competitive_gaps", [])
        if comp_gaps:
            urgent_gaps = [g for g in comp_gaps if g.get("urgency") == "high"]
            if urgent_gaps:
                risks.append({
                    "type": "competitive_gap",
                    "severity": "medium",
                    "description": "Lagging competitors in critical technology areas",
                    "impact": "Loss of market share to tech-forward competitors",
                    "mitigation": "Accelerate technology investment and partnerships"
                })
        
        return risks
    
    def _identify_opportunities(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify technology opportunities"""
        opportunities = []
        
        # Innovation district opportunities
        districts = insights.get("innovation_districts", {})
        emerging = districts.get("emerging_districts", [])
        for district in emerging[:2]:
            opportunities.append({
                "type": "innovation_district",
                "potential": "high",
                "description": f"{district['name']} emerging tech hub with {district['growth_rate']}% growth",
                "value_creation": "Premium rents and appreciation in tech corridors",
                "action": "Acquire and develop tech-focused properties"
            })
        
        # PropTech ROI opportunities
        proptech = insights.get("proptech_adoption", {})
        roi_metrics = proptech.get("roi_metrics", {})
        if roi_metrics.get("smart_building_systems", {}).get("energy_savings", 0) > 20:
            opportunities.append({
                "type": "smart_building_tech",
                "potential": "high",
                "description": f"Smart buildings achieve {roi_metrics['smart_building_systems']['energy_savings']}% energy savings",
                "value_creation": "Lower operating costs and premium rents",
                "action": "Implement smart building systems in all new developments"
            })
        
        # Smart city integration
        smart_city = insights.get("smart_city_opportunities", {})
        funding = smart_city.get("funding_programs", [])
        if funding:
            best_program = max(funding, key=lambda x: x.get("funding_amount", 0))
            opportunities.append({
                "type": "smart_city_funding",
                "potential": "medium",
                "description": f"${best_program['funding_amount']/1e6:.1f}M available in {best_program['program']}",
                "value_creation": "Reduced development costs through grants",
                "action": f"Apply for funding by {best_program['application_window']}"
            })
        
        # Digital transformation
        digital = insights.get("digital_transformation", {})
        trans_opps = digital.get("transformation_opportunities", [])
        high_roi = [o for o in trans_opps if o.get("expected_roi", 0) > 30]
        if high_roi:
            best_opp = max(high_roi, key=lambda x: x.get("expected_roi", 0))
            opportunities.append({
                "type": "digital_transformation",
                "potential": "high",
                "description": f"{best_opp['area']} digitalization offers {best_opp['expected_roi']}% ROI",
                "value_creation": f"${best_opp['investment_required']/1e6:.1f}M investment, {best_opp['implementation_time']} month payback",
                "action": "Launch digital transformation initiative"
            })
        
        # Technology partnerships
        positioning = insights.get("competitive_positioning", {})
        partnerships = positioning.get("partnership_opportunities", [])
        if partnerships:
            opportunities.append({
                "type": "tech_partnership",
                "potential": "medium",
                "description": "Strategic PropTech partnerships available",
                "value_creation": "Accelerated innovation without full development cost",
                "action": "Establish innovation partnerships with top PropTech firms"
            })
        
        return opportunities[:5]
    
    def _generate_recommendations(self, insights: Dict[str, Any], 
                                risks: List[Dict], 
                                opportunities: List[Dict]) -> List[str]:
        """Generate actionable technology recommendations"""
        recommendations = []
        
        # Based on innovation districts
        districts = insights.get("innovation_districts", {})
        if districts.get("development_opportunities"):
            recommendations.append("Focus development in emerging innovation districts for tech tenant demand")
        
        # Based on PropTech ROI
        proptech = insights.get("proptech_adoption", {})
        roi_metrics = proptech.get("roi_metrics", {})
        if any(roi_metrics.values()):
            recommendations.append("Implement PropTech solutions with proven ROI (smart buildings, IoT, automation)")
        
        # Based on infrastructure
        infrastructure = insights.get("tech_infrastructure", {})
        if infrastructure.get("5g_deployment", {}).get("coverage_pct", 0) > 50:
            recommendations.append("Design buildings for 5G integration to attract tech tenants")
        
        # Based on digital transformation
        digital = insights.get("digital_transformation", {})
        if digital.get("transformation_opportunities"):
            recommendations.append("Launch comprehensive digital transformation program")
        
        # Based on competitive positioning
        positioning = insights.get("competitive_positioning", {})
        if positioning.get("tech_differentiators"):
            recommendations.append("Invest in AI and data analytics for competitive advantage")
        
        return recommendations[:5]
    
    def _extract_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract key technology metrics"""
        metrics = {}
        
        # Innovation district metrics
        districts = insights.get("innovation_districts", {})
        established = districts.get("established_districts", [])
        if established:
            metrics["total_tech_companies"] = sum(d["tech_companies"] for d in established)
            metrics["avg_tech_employment"] = np.mean([d["employment"] for d in established])
            metrics["avg_district_growth"] = np.mean([d["growth_rate"] for d in established])
        
        # PropTech metrics
        proptech = insights.get("proptech_adoption", {})
        adoption_rates = proptech.get("adoption_rates", {})
        if adoption_rates:
            all_adoptions = [v["current_adoption"] for v in adoption_rates.values()]
            metrics["avg_proptech_adoption"] = np.mean(all_adoptions)
            metrics["proptech_growth_rate"] = np.mean([v["growth_rate"] for v in adoption_rates.values()])
        
        # Smart building ROI
        roi_metrics = proptech.get("roi_metrics", {})
        smart_building = roi_metrics.get("smart_building_systems", {})
        metrics["smart_building_energy_savings"] = smart_building.get("energy_savings", 0)
        metrics["smart_building_payback_years"] = smart_building.get("payback_years", 0)
        
        # Infrastructure metrics
        infrastructure = insights.get("tech_infrastructure", {})
        connectivity = infrastructure.get("connectivity", {})
        metrics["gigabit_coverage_pct"] = connectivity.get("gigabit_coverage", 0)
        metrics["5g_coverage_pct"] = infrastructure.get("5g_deployment", {}).get("coverage_pct", 0)
        
        # Investment metrics
        investment = insights.get("investment_landscape", {})
        vc_activity = investment.get("vc_activity", {})
        metrics["annual_proptech_investment"] = vc_activity.get("annual_investment", 0)
        metrics["proptech_deal_count"] = vc_activity.get("deal_count", 0)
        
        return metrics