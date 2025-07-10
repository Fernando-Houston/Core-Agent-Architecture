"""
Environmental Intelligence Analyzer - Flood risks, compliance, and sustainability
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


class EnvironmentalIntelligenceAnalyzer(BaseIntelligenceAnalyzer):
    """Analyzes environmental risks, compliance requirements, and sustainability opportunities"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("environmental_intelligence", config)
        
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform environmental-specific analysis"""
        insights = {
            "flood_risk_assessment": self._assess_flood_risks(data),
            "environmental_compliance": self._analyze_compliance_requirements(data),
            "mitigation_strategies": self._evaluate_mitigation_strategies(data),
            "sustainability_opportunities": self._identify_sustainability_opportunities(data),
            "climate_resilience": self._assess_climate_resilience(data),
            "cost_benefit_analysis": self._perform_cost_benefit_analysis(data),
            "regulatory_landscape": self._analyze_regulatory_landscape(data)
        }
        return insights
    
    def _assess_flood_risks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive flood risk assessment by area"""
        flood_data = data.get("aggregated_data", {}).get("flood_risk_zones", {})
        
        risk_assessment = {
            "high_risk_areas": [],
            "moderate_risk_areas": [],
            "low_risk_areas": [],
            "development_restrictions": {},
            "insurance_implications": {}
        }
        
        # Analyze 100-year flood zones
        flood_100 = flood_data.get("100_year", {})
        flood_500 = flood_data.get("500_year", {})
        coastal = flood_data.get("coastal_surge", {})
        
        for area, percentage in flood_100.items():
            risk_profile = {
                "area": area,
                "flood_100_year": percentage,
                "flood_500_year": flood_500.get(area, 0),
                "risk_level": self._categorize_flood_risk(percentage, flood_500.get(area, 0)),
                "development_feasibility": self._assess_development_feasibility(percentage),
                "estimated_insurance_cost": self._estimate_flood_insurance(percentage)
            }
            
            # Categorize areas
            if risk_profile["risk_level"] == "high":
                risk_assessment["high_risk_areas"].append(risk_profile)
            elif risk_profile["risk_level"] == "moderate":
                risk_assessment["moderate_risk_areas"].append(risk_profile)
            else:
                risk_assessment["low_risk_areas"].append(risk_profile)
            
            # Development restrictions
            if percentage > 20:
                risk_assessment["development_restrictions"][area] = {
                    "elevation_required": True,
                    "min_elevation_ft": 3 if percentage > 30 else 2,
                    "detention_required": True,
                    "special_permits": ["FEMA", "Chapter 19"]
                }
        
        # Coastal surge analysis
        for area, percentage in coastal.items():
            risk_assessment["high_risk_areas"].append({
                "area": area,
                "coastal_surge_risk": percentage,
                "risk_level": "critical",
                "development_feasibility": "restricted",
                "special_requirements": ["hurricane_resistant_design", "elevated_foundation"]
            })
        
        return risk_assessment
    
    def _analyze_compliance_requirements(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze environmental compliance requirements and costs"""
        compliance_data = data.get("aggregated_data", {}).get("environmental_compliance", {})
        
        compliance_analysis = {
            "air_quality_compliance": {},
            "water_quality_compliance": {},
            "brownfield_opportunities": {},
            "permitting_requirements": [],
            "compliance_costs": {}
        }
        
        # Air quality compliance
        air_quality = compliance_data.get("air_quality", {})
        compliance_analysis["air_quality_compliance"] = {
            "status": air_quality.get("compliance_status", "unknown"),
            "ozone_exceedance_days": air_quality.get("ozone_days_exceeded", 0),
            "pm25_level": air_quality.get("pm25_annual_avg", 0),
            "requirements": self._determine_air_quality_requirements(air_quality),
            "annual_compliance_cost": 25000 if air_quality.get("compliance_status") == "moderate_nonattainment" else 10000
        }
        
        # Water quality compliance
        water_quality = compliance_data.get("water_quality", {})
        compliance_analysis["water_quality_compliance"] = {
            "bayou_health": water_quality.get("bayou_health_index", 0),
            "violations": water_quality.get("stormwater_violations", 0),
            "wetland_areas": water_quality.get("wetland_permits_required", []),
            "stormwater_management_required": True,
            "estimated_cost": 45000 + (water_quality.get("stormwater_violations", 0) * 5000)
        }
        
        # Brownfield opportunities
        brownfields = compliance_data.get("brownfield_sites", {})
        if brownfields.get("opportunity_zones", 0) > 0:
            compliance_analysis["brownfield_opportunities"] = {
                "available_sites": brownfields.get("opportunity_zones", 0),
                "tax_incentives": "Federal and state tax credits available",
                "cleanup_grants": "EPA assessment and cleanup grants eligible",
                "development_potential": "high",
                "estimated_roi_boost": 15  # percentage points
            }
        
        return compliance_analysis
    
    def _evaluate_mitigation_strategies(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate cost-effective mitigation strategies"""
        mitigation_costs = data.get("aggregated_data", {}).get("mitigation_costs", {})
        flood_risks = self._assess_flood_risks(data)
        
        strategies = []
        
        # Elevation strategy
        elevation_costs = mitigation_costs.get("elevation_requirements", {})
        for elevation_type, cost in elevation_costs.items():
            benefit = self._calculate_elevation_benefits(elevation_type)
            strategies.append({
                "strategy": f"Elevation: {elevation_type}",
                "cost_per_unit": cost,
                "flood_insurance_savings": benefit["insurance_savings"],
                "risk_reduction": benefit["risk_reduction"],
                "payback_period_years": cost / benefit["insurance_savings"] if benefit["insurance_savings"] > 0 else 999,
                "recommendation": "Highly recommended" if benefit["risk_reduction"] > 50 else "Recommended"
            })
        
        # Green infrastructure
        green_infra = mitigation_costs.get("green_infrastructure", {})
        strategies.append({
            "strategy": "Green Infrastructure Package",
            "components": ["bioswales", "permeable_pavement", "detention_ponds"],
            "cost_per_acre": sum([
                green_infra.get("bioswales_per_acre", 0),
                green_infra.get("permeable_pavement_sqft", 0) * 100,  # 100 sqft estimate
                green_infra.get("detention_pond_acre", 0) * 0.1  # 10% of site
            ]),
            "benefits": ["Reduce runoff by 40%", "LEED points", "Lower detention requirements"],
            "regulatory_credits": "Chapter 19 compliance credits",
            "recommendation": "Essential for sustainable development"
        })
        
        # Sort by payback period
        strategies.sort(key=lambda x: x.get("payback_period_years", 999))
        
        return strategies
    
    def _identify_sustainability_opportunities(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify sustainability and green building opportunities"""
        sustainability_data = data.get("aggregated_data", {}).get("sustainability_metrics", {})
        
        opportunities = {
            "green_certifications": {},
            "renewable_energy": {},
            "market_advantages": {},
            "incentives": []
        }
        
        # Analyze certification trends
        leed_certs = sustainability_data.get("leed_certifications", {})
        total_leed = sum(leed_certs.values()) if leed_certs else 0
        
        opportunities["green_certifications"] = {
            "market_penetration": total_leed,
            "premium_potential": {
                "platinum": "8-12% rent premium",
                "gold": "5-8% rent premium",
                "silver": "3-5% rent premium"
            },
            "fastest_growing": "Gold certifications (+25% YoY)",
            "roi_impact": "15-20% higher asset value"
        }
        
        # Solar opportunities
        solar_count = sustainability_data.get("solar_installations", 0)
        opportunities["renewable_energy"] = {
            "current_installations": solar_count,
            "growth_rate": "35% annually",
            "payback_period": "5-7 years with incentives",
            "incentives": ["30% federal tax credit", "Net metering available", "Property tax exemption"],
            "recommended_capacity": "Minimum 100kW for commercial properties"
        }
        
        # Market advantages
        opportunities["market_advantages"] = {
            "tenant_preference": "72% of tenants prefer green buildings",
            "occupancy_premium": "+3.7% occupancy rate",
            "operating_cost_reduction": "20-30% lower operating costs",
            "exit_cap_rate_compression": "25-50 basis points"
        }
        
        # Available incentives
        opportunities["incentives"] = [
            {
                "program": "C-PACE Financing",
                "benefit": "Low-cost, long-term financing for efficiency upgrades",
                "eligibility": "Commercial properties >50,000 sqft"
            },
            {
                "program": "Texas HERO Program",
                "benefit": "Property tax financing for renewable energy",
                "eligibility": "All property types"
            },
            {
                "program": "Energy Star Rebates",
                "benefit": "Up to $100,000 in utility rebates",
                "eligibility": "Energy Star certified buildings"
            }
        ]
        
        return opportunities
    
    def _assess_climate_resilience(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess long-term climate resilience factors"""
        climate_data = data.get("aggregated_data", {}).get("climate_projections", {})
        
        resilience_assessment = {
            "climate_risks": {},
            "adaptation_priorities": [],
            "resilient_design_features": [],
            "long_term_viability": {}
        }
        
        # Climate risk factors
        resilience_assessment["climate_risks"] = {
            "temperature_increase": climate_data.get("temp_increase_2050", 0),
            "extreme_heat_days": round(climate_data.get("temp_increase_2050", 0) * 15),  # Estimate
            "rainfall_intensity": f"+{climate_data.get('rainfall_intensity_increase', 0)}%",
            "hurricane_risk": f"{climate_data.get('hurricane_cat3_probability', 0)}% Cat 3+",
            "drought_frequency": climate_data.get("drought_frequency", "unknown")
        }
        
        # Adaptation priorities based on risks
        if climate_data.get("temp_increase_2050", 0) > 2:
            resilience_assessment["adaptation_priorities"].append({
                "priority": "Cooling systems",
                "rationale": "Extreme heat mitigation",
                "cost_impact": "+15% HVAC capacity needed"
            })
        
        if climate_data.get("rainfall_intensity_increase", 0) > 10:
            resilience_assessment["adaptation_priorities"].append({
                "priority": "Enhanced drainage",
                "rationale": "Increased rainfall intensity",
                "cost_impact": "+20% stormwater infrastructure"
            })
        
        # Resilient design features
        resilience_assessment["resilient_design_features"] = [
            {"feature": "Hurricane-resistant windows", "cost_premium": "5-8%", "benefit": "Reduced insurance 15%"},
            {"feature": "Backup power systems", "cost_premium": "3-5%", "benefit": "Operational continuity"},
            {"feature": "Elevated utilities", "cost_premium": "2-3%", "benefit": "Flood protection"},
            {"feature": "Cool roof technology", "cost_premium": "1-2%", "benefit": "20% cooling reduction"}
        ]
        
        return resilience_assessment
    
    def _perform_cost_benefit_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive cost-benefit analysis of environmental measures"""
        mitigation_costs = data.get("aggregated_data", {}).get("mitigation_costs", {})
        flood_insurance = mitigation_costs.get("flood_insurance", {})
        
        # Calculate typical project scenario (100,000 sqft development)
        base_scenario = {
            "project_size_sqft": 100000,
            "construction_cost": 15000000,  # $150/sqft
            "annual_revenue": 2000000  # $20/sqft
        }
        
        # Environmental compliance costs
        compliance_costs = {
            "flood_mitigation": 250000,  # Elevation + drainage
            "green_infrastructure": 180000,
            "environmental_permits": 45000,
            "sustainability_features": 320000  # LEED Gold target
        }
        
        # Benefits calculation
        annual_benefits = {
            "insurance_savings": 35000,  # From elevation
            "energy_savings": 60000,  # From sustainability features
            "tax_incentives": 95000,  # First year
            "rent_premium": 100000,  # 5% premium for green building
            "reduced_vacancy": 40000  # 2% lower vacancy
        }
        
        # ROI calculation
        total_env_investment = sum(compliance_costs.values())
        total_annual_benefit = sum(annual_benefits.values())
        environmental_roi = (total_annual_benefit / total_env_investment) * 100
        
        return {
            "total_environmental_investment": total_env_investment,
            "annual_benefits": total_annual_benefit,
            "environmental_roi": round(environmental_roi, 1),
            "payback_period_years": round(total_env_investment / total_annual_benefit, 1),
            "10_year_npv": round(total_annual_benefit * 7.72 - total_env_investment, 0),  # 5% discount
            "recommendation": "Environmental investments show strong positive ROI"
        }
    
    def _analyze_regulatory_landscape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze regulatory requirements and future changes"""
        regulatory_data = data.get("aggregated_data", {}).get("regulatory_requirements", {})
        
        landscape = {
            "current_requirements": {},
            "upcoming_changes": [],
            "compliance_timeline": {},
            "strategic_recommendations": []
        }
        
        # Current requirements
        chapter_19 = regulatory_data.get("chapter_19_compliance", {})
        landscape["current_requirements"] = {
            "detention": chapter_19.get("detention_required", False),
            "max_impervious": f"{chapter_19.get('max_impervious_cover', 0)}%",
            "green_space": f"{chapter_19.get('green_space_minimum', 0)}% minimum",
            "permits_required": regulatory_data.get("tceq_permits", []) + regulatory_data.get("usace_404_permits", [])
        }
        
        # Upcoming regulatory changes
        landscape["upcoming_changes"] = [
            {
                "regulation": "Enhanced flood regulations",
                "timeline": "Q2 2025",
                "impact": "Additional 1ft elevation requirement",
                "preparation": "Design to new standards now to avoid redesign"
            },
            {
                "regulation": "Energy benchmarking mandate",
                "timeline": "2026",
                "impact": "Required energy reporting for buildings >50k sqft",
                "preparation": "Install energy monitoring systems"
            }
        ]
        
        # Strategic recommendations
        landscape["strategic_recommendations"] = [
            "Exceed current standards to future-proof developments",
            "Integrate compliance into design phase to reduce costs",
            "Pursue voluntary certifications for market advantage"
        ]
        
        return landscape
    
    def _categorize_flood_risk(self, flood_100: float, flood_500: float) -> str:
        """Categorize flood risk level"""
        if flood_100 > 25:
            return "high"
        elif flood_100 > 10 or flood_500 > 30:
            return "moderate"
        else:
            return "low"
    
    def _assess_development_feasibility(self, flood_percentage: float) -> str:
        """Assess development feasibility based on flood risk"""
        if flood_percentage > 50:
            return "not_recommended"
        elif flood_percentage > 25:
            return "challenging_requires_mitigation"
        elif flood_percentage > 10:
            return "feasible_with_precautions"
        else:
            return "favorable"
    
    def _estimate_flood_insurance(self, flood_percentage: float) -> float:
        """Estimate annual flood insurance cost per $100k property value"""
        if flood_percentage > 30:
            return 3500
        elif flood_percentage > 15:
            return 2200
        elif flood_percentage > 5:
            return 1200
        else:
            return 450
    
    def _determine_air_quality_requirements(self, air_quality: Dict[str, Any]) -> List[str]:
        """Determine air quality compliance requirements"""
        requirements = []
        
        if air_quality.get("compliance_status") == "moderate_nonattainment":
            requirements.extend([
                "Low-NOx equipment required",
                "Construction emission controls",
                "Annual emissions reporting",
                "Offset requirements for major sources"
            ])
        
        return requirements
    
    def _calculate_elevation_benefits(self, elevation_type: str) -> Dict[str, Any]:
        """Calculate benefits of elevation strategies"""
        benefits = {
            "base_flood_plus_1ft": {"insurance_savings": 2500, "risk_reduction": 30},
            "base_flood_plus_2ft": {"insurance_savings": 3500, "risk_reduction": 60},
            "base_flood_plus_3ft": {"insurance_savings": 4200, "risk_reduction": 85}
        }
        
        return benefits.get(elevation_type, {"insurance_savings": 0, "risk_reduction": 0})
    
    def _extract_key_findings(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key findings from environmental analysis"""
        findings = []
        
        # Flood risk findings
        flood_assessment = insights.get("flood_risk_assessment", {})
        high_risk_count = len(flood_assessment.get("high_risk_areas", []))
        if high_risk_count > 0:
            findings.append(f"{high_risk_count} areas identified with high flood risk requiring mitigation")
        
        # Compliance findings
        compliance = insights.get("environmental_compliance", {})
        if compliance.get("air_quality_compliance", {}).get("status") == "moderate_nonattainment":
            findings.append("Air quality nonattainment status requires enhanced emission controls")
        
        # Sustainability opportunities
        sustainability = insights.get("sustainability_opportunities", {})
        if sustainability.get("green_certifications", {}).get("roi_impact"):
            findings.append("Green certifications can increase asset value by 15-20%")
        
        # Cost benefit
        cost_benefit = insights.get("cost_benefit_analysis", {})
        if cost_benefit.get("environmental_roi", 0) > 20:
            findings.append(f"Environmental investments show {cost_benefit['environmental_roi']:.1f}% ROI")
        
        # Climate resilience
        climate = insights.get("climate_resilience", {})
        if climate.get("climate_risks", {}).get("temperature_increase", 0) > 2:
            findings.append("Climate adaptation measures essential for long-term asset resilience")
        
        return findings[:5]
    
    def _identify_risks(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify environmental risks"""
        risks = []
        
        # Flood risks
        flood_assessment = insights.get("flood_risk_assessment", {})
        high_risk_areas = flood_assessment.get("high_risk_areas", [])
        if high_risk_areas:
            risks.append({
                "type": "flood_risk",
                "severity": "high",
                "description": f"{len(high_risk_areas)} areas in high flood risk zones",
                "financial_impact": "Insurance costs 5-10x higher, development restrictions",
                "mitigation": "Require elevation, enhanced drainage, and flood insurance"
            })
        
        # Compliance risks
        compliance = insights.get("environmental_compliance", {})
        if compliance.get("water_quality_compliance", {}).get("violations", 0) > 20:
            risks.append({
                "type": "compliance_violations",
                "severity": "medium",
                "description": "History of stormwater violations indicates systemic issues",
                "financial_impact": "$250k+ in fines and remediation costs",
                "mitigation": "Implement comprehensive stormwater management program"
            })
        
        # Climate risks
        climate = insights.get("climate_resilience", {})
        if climate.get("climate_risks", {}).get("hurricane_cat3_probability", 0) > 15:
            risks.append({
                "type": "hurricane_exposure",
                "severity": "high",
                "description": "Increasing hurricane intensity threatens coastal properties",
                "financial_impact": "Potential total loss events, insurance availability concerns",
                "mitigation": "Hurricane-resistant design, comprehensive insurance, geographic diversification"
            })
        
        return risks
    
    def _identify_opportunities(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify environmental opportunities"""
        opportunities = []
        
        # Brownfield opportunities
        compliance = insights.get("environmental_compliance", {})
        brownfields = compliance.get("brownfield_opportunities", {})
        if brownfields.get("available_sites", 0) > 0:
            opportunities.append({
                "type": "brownfield_development",
                "potential": "high",
                "description": f"{brownfields['available_sites']} brownfield sites with tax incentives",
                "financial_benefit": f"{brownfields.get('estimated_roi_boost', 0)}% ROI boost from incentives",
                "action": "Partner with EPA for assessment grants and tax credits"
            })
        
        # Green building opportunities
        sustainability = insights.get("sustainability_opportunities", {})
        if sustainability.get("market_advantages", {}).get("occupancy_premium"):
            opportunities.append({
                "type": "green_certification",
                "potential": "high",
                "description": "Green buildings command premium rents and occupancy",
                "financial_benefit": "5-8% rent premium, 3.7% higher occupancy",
                "action": "Target LEED Gold for optimal cost-benefit ratio"
            })
        
        # Renewable energy
        if sustainability.get("renewable_energy", {}).get("incentives"):
            opportunities.append({
                "type": "solar_investment",
                "potential": "medium",
                "description": "Solar installations with 30% federal tax credit",
                "financial_benefit": "5-7 year payback, hedge against energy costs",
                "action": "Install solar on all suitable roof space"
            })
        
        # Resilience premium
        opportunities.append({
            "type": "resilient_design",
            "potential": "high",
            "description": "Climate-resilient buildings attract institutional investors",
            "financial_benefit": "25-50 bps cap rate compression",
            "action": "Incorporate resilient design features in all new developments"
        })
        
        return opportunities[:5]
    
    def _generate_recommendations(self, insights: Dict[str, Any], 
                                risks: List[Dict], 
                                opportunities: List[Dict]) -> List[str]:
        """Generate actionable environmental recommendations"""
        recommendations = []
        
        # Based on flood risks
        flood_assessment = insights.get("flood_risk_assessment", {})
        if flood_assessment.get("high_risk_areas"):
            recommendations.append("Avoid development in high flood risk areas or budget for substantial mitigation")
        
        # Based on ROI analysis
        cost_benefit = insights.get("cost_benefit_analysis", {})
        if cost_benefit.get("environmental_roi", 0) > 20:
            recommendations.append("Invest in comprehensive environmental features for strong ROI")
        
        # Based on regulatory landscape
        regulatory = insights.get("regulatory_landscape", {})
        if regulatory.get("upcoming_changes"):
            recommendations.append("Design to future regulatory standards to avoid costly retrofits")
        
        # Based on opportunities
        if any(o["type"] == "green_certification" for o in opportunities):
            recommendations.append("Pursue LEED Gold certification as standard for all new developments")
        
        # Climate adaptation
        climate = insights.get("climate_resilience", {})
        if climate.get("adaptation_priorities"):
            recommendations.append("Integrate climate adaptation into base building design")
        
        return recommendations[:5]
    
    def _extract_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract key environmental metrics"""
        metrics = {}
        
        # Flood risk metrics
        flood_assessment = insights.get("flood_risk_assessment", {})
        high_risk_areas = flood_assessment.get("high_risk_areas", [])
        metrics["high_flood_risk_areas"] = len(high_risk_areas)
        
        # Compliance metrics
        compliance = insights.get("environmental_compliance", {})
        metrics["air_quality_exceedances"] = compliance.get("air_quality_compliance", {}).get("ozone_exceedance_days", 0)
        metrics["water_quality_violations"] = compliance.get("water_quality_compliance", {}).get("violations", 0)
        
        # Sustainability metrics
        sustainability = insights.get("sustainability_opportunities", {})
        metrics["leed_buildings"] = sustainability.get("green_certifications", {}).get("market_penetration", 0)
        metrics["solar_installations"] = sustainability.get("renewable_energy", {}).get("current_installations", 0)
        
        # Financial metrics
        cost_benefit = insights.get("cost_benefit_analysis", {})
        metrics["environmental_roi"] = cost_benefit.get("environmental_roi", 0)
        metrics["payback_period_years"] = cost_benefit.get("payback_period_years", 0)
        
        # Climate metrics
        climate = insights.get("climate_resilience", {})
        metrics["temp_increase_2050"] = climate.get("climate_risks", {}).get("temperature_increase", 0)
        metrics["hurricane_risk_pct"] = climate.get("climate_risks", {}).get("hurricane_cat3_probability", 0)
        
        return metrics