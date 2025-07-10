"""
Regulatory Intelligence Analyzer - Zoning, permits, and regulatory opportunities
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from analysis_engines.base_analyzer import BaseIntelligenceAnalyzer


class RegulatoryIntelligenceAnalyzer(BaseIntelligenceAnalyzer):
    """Analyzes regulatory landscape, zoning opportunities, and permit optimization"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("regulatory_intelligence", config)
        
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform regulatory-specific analysis"""
        insights = {
            "zoning_opportunities": self._analyze_zoning_opportunities(data),
            "permit_optimization": self._analyze_permit_processes(data),
            "regulatory_changes": self._track_regulatory_changes(data),
            "compliance_strategies": self._develop_compliance_strategies(data),
            "development_incentives": self._identify_development_incentives(data),
            "risk_assessment": self._assess_regulatory_risks(data),
            "strategic_positioning": self._analyze_strategic_positioning(data)
        }
        return insights
    
    def _analyze_zoning_opportunities(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze zoning opportunities and potential rezoning targets"""
        zoning_data = data.get("aggregated_data", {}).get("zoning_analysis", {})
        
        opportunities = {
            "rezoning_candidates": [],
            "by_right_development": [],
            "overlay_districts": {},
            "density_bonuses": [],
            "mixed_use_potential": []
        }
        
        # Analyze rezoning opportunities
        rezoning_areas = zoning_data.get("rezoning_activity", {})
        for area, activity in rezoning_areas.items():
            if isinstance(activity, dict):
                success_rate = activity.get("approval_rate", 0)
                if success_rate > 60:
                    opportunities["rezoning_candidates"].append({
                        "area": area,
                        "current_zoning": activity.get("from_zoning", ""),
                        "target_zoning": activity.get("to_zoning", ""),
                        "approval_probability": success_rate,
                        "typical_timeline": activity.get("avg_days", 180),
                        "value_uplift": self._calculate_zoning_uplift(activity),
                        "recommended_use": activity.get("highest_value_use", "mixed-use")
                    })
        
        # Identify by-right opportunities
        by_right = zoning_data.get("by_right_zones", {})
        for zone, details in by_right.items():
            if isinstance(details, dict) and details.get("development_potential", 0) > 70:
                opportunities["by_right_development"].append({
                    "zone": zone,
                    "allowed_uses": details.get("permitted_uses", []),
                    "max_density": details.get("max_far", 0),
                    "height_limit": details.get("max_height", 0),
                    "setback_requirements": details.get("setbacks", {}),
                    "development_score": details.get("development_potential", 0)
                })
        
        # Overlay district benefits
        overlays = zoning_data.get("overlay_districts", {})
        for district, benefits in overlays.items():
            if isinstance(benefits, dict):
                opportunities["overlay_districts"][district] = {
                    "incentives": benefits.get("incentives", []),
                    "reduced_parking": benefits.get("parking_reduction", 0),
                    "height_bonus": benefits.get("height_bonus", 0),
                    "expedited_permitting": benefits.get("fast_track", False),
                    "estimated_value": self._estimate_overlay_value(benefits)
                }
        
        # Density bonus programs
        density_programs = zoning_data.get("density_bonus_programs", [])
        for program in density_programs:
            if isinstance(program, dict):
                opportunities["density_bonuses"].append({
                    "program": program.get("name", ""),
                    "bonus_percentage": program.get("max_bonus", 0),
                    "requirements": program.get("requirements", []),
                    "cost_benefit": self._analyze_density_bonus_roi(program),
                    "recommendation": "pursue" if program.get("max_bonus", 0) > 25 else "evaluate"
                })
        
        return opportunities
    
    def _analyze_permit_processes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze permit processes and optimization opportunities"""
        permit_data = data.get("aggregated_data", {}).get("permitting", {})
        
        permit_analysis = {
            "approval_times": {},
            "fast_track_options": [],
            "common_delays": [],
            "optimization_strategies": [],
            "cost_analysis": {}
        }
        
        # Analyze approval times by permit type
        approval_times = permit_data.get("average_timelines", {})
        for permit_type, timeline in approval_times.items():
            if isinstance(timeline, dict):
                permit_analysis["approval_times"][permit_type] = {
                    "standard_days": timeline.get("standard", 0),
                    "expedited_days": timeline.get("expedited", 0),
                    "approval_rate": timeline.get("approval_rate", 0),
                    "revision_probability": timeline.get("revision_rate", 0),
                    "cost": timeline.get("base_cost", 0)
                }
        
        # Fast track opportunities
        fast_track = permit_data.get("expedited_programs", [])
        for program in fast_track:
            if isinstance(program, dict):
                time_savings = program.get("time_reduction", 0)
                if time_savings > 30:
                    permit_analysis["fast_track_options"].append({
                        "program": program.get("name", ""),
                        "eligibility": program.get("requirements", []),
                        "time_savings_pct": time_savings,
                        "additional_cost": program.get("premium_cost", 0),
                        "roi": self._calculate_fast_track_roi(program),
                        "recommended": time_savings > 40
                    })
        
        # Common delay factors
        delays = permit_data.get("delay_analysis", {})
        for factor, impact in delays.items():
            if isinstance(impact, dict) and impact.get("frequency", 0) > 20:
                permit_analysis["common_delays"].append({
                    "factor": factor,
                    "frequency_pct": impact.get("frequency", 0),
                    "avg_delay_days": impact.get("avg_delay", 0),
                    "mitigation": impact.get("prevention_strategy", ""),
                    "cost_impact": impact.get("cost_per_day", 0) * impact.get("avg_delay", 0)
                })
        
        # Optimization strategies
        permit_analysis["optimization_strategies"] = [
            {
                "strategy": "Pre-application meetings",
                "benefit": "30% reduction in revisions",
                "cost": 5000,
                "implementation": "Schedule 60 days before submission"
            },
            {
                "strategy": "Third-party review",
                "benefit": "40-50% time reduction",
                "cost": 15000,
                "implementation": "Use city-approved consultants"
            },
            {
                "strategy": "Phased permitting",
                "benefit": "Start construction 3-6 months earlier",
                "cost": 8000,
                "implementation": "Submit foundation permits separately"
            }
        ]
        
        return permit_analysis
    
    def _track_regulatory_changes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Track and analyze regulatory changes and trends"""
        regulatory_data = data.get("aggregated_data", {}).get("regulatory_changes", {})
        
        change_analysis = {
            "recent_changes": [],
            "upcoming_changes": [],
            "trend_analysis": {},
            "impact_assessment": {},
            "preparation_strategies": []
        }
        
        # Recent regulatory changes
        recent = regulatory_data.get("recent_changes", [])
        for change in recent:
            if isinstance(change, dict):
                change_analysis["recent_changes"].append({
                    "regulation": change.get("name", ""),
                    "effective_date": change.get("effective_date", ""),
                    "category": change.get("category", ""),
                    "impact": change.get("impact_description", ""),
                    "compliance_required": change.get("mandatory", True),
                    "adaptation_cost": change.get("compliance_cost", 0)
                })
        
        # Upcoming changes
        upcoming = regulatory_data.get("proposed_changes", [])
        for proposal in upcoming:
            if isinstance(proposal, dict):
                probability = proposal.get("passage_probability", 0)
                if probability > 50:
                    change_analysis["upcoming_changes"].append({
                        "proposal": proposal.get("name", ""),
                        "timeline": proposal.get("expected_date", ""),
                        "probability_pct": probability,
                        "impact_level": proposal.get("impact_level", "medium"),
                        "preparation_needed": proposal.get("prep_time_months", 6),
                        "early_compliance_benefit": proposal.get("early_adopter_benefit", "")
                    })
        
        # Trend analysis
        trends = regulatory_data.get("regulatory_trends", {})
        change_analysis["trend_analysis"] = {
            "direction": trends.get("overall_direction", "increasing_regulation"),
            "focus_areas": trends.get("focus_areas", []),
            "enforcement_intensity": trends.get("enforcement_trend", "increasing"),
            "business_impact": trends.get("cost_trend", "increasing")
        }
        
        return change_analysis
    
    def _develop_compliance_strategies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive compliance strategies"""
        compliance_data = data.get("aggregated_data", {}).get("compliance", {})
        
        strategies = {
            "proactive_compliance": [],
            "cost_optimization": {},
            "risk_mitigation": [],
            "competitive_advantages": []
        }
        
        # Proactive compliance opportunities
        requirements = compliance_data.get("key_requirements", {})
        for req_type, details in requirements.items():
            if isinstance(details, dict):
                strategies["proactive_compliance"].append({
                    "requirement": req_type,
                    "current_standard": details.get("current", ""),
                    "future_standard": details.get("projected", ""),
                    "early_adoption_benefit": details.get("early_benefit", ""),
                    "implementation_cost": details.get("cost", 0),
                    "competitive_advantage": details.get("market_differentiation", False)
                })
        
        # Cost optimization
        strategies["cost_optimization"] = {
            "bundled_submissions": "Save 20% on permit fees",
            "annual_permits": "Reduce per-project costs by 30%",
            "self_certification": "Cut inspection time by 50%",
            "digital_submissions": "Reduce processing time by 25%"
        }
        
        # Risk mitigation
        risk_areas = compliance_data.get("high_risk_areas", [])
        for risk in risk_areas:
            if isinstance(risk, dict):
                strategies["risk_mitigation"].append({
                    "risk_area": risk.get("area", ""),
                    "violation_probability": risk.get("violation_rate", 0),
                    "typical_penalty": risk.get("avg_penalty", 0),
                    "mitigation_strategy": risk.get("best_practice", ""),
                    "compliance_cost": risk.get("prevention_cost", 0),
                    "roi": (risk.get("avg_penalty", 0) * risk.get("violation_rate", 0) / 100) / max(risk.get("prevention_cost", 1), 1)
                })
        
        return strategies
    
    def _identify_development_incentives(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify available development incentives and programs"""
        incentive_data = data.get("aggregated_data", {}).get("incentive_programs", {})
        
        incentives = []
        
        # Tax incentives
        tax_programs = incentive_data.get("tax_incentives", [])
        for program in tax_programs:
            if isinstance(program, dict):
                incentives.append({
                    "type": "tax_incentive",
                    "program": program.get("name", ""),
                    "benefit": program.get("benefit_description", ""),
                    "value": program.get("estimated_value", 0),
                    "requirements": program.get("eligibility", []),
                    "duration": program.get("term_years", 0),
                    "application_deadline": program.get("deadline", ""),
                    "success_rate": program.get("approval_rate", 0),
                    "recommended": program.get("estimated_value", 0) > 100000
                })
        
        # Development incentives
        dev_incentives = incentive_data.get("development_incentives", [])
        for incentive in dev_incentives:
            if isinstance(incentive, dict):
                incentives.append({
                    "type": "development_incentive",
                    "program": incentive.get("name", ""),
                    "benefit": incentive.get("benefit_type", ""),
                    "value": incentive.get("max_benefit", 0),
                    "requirements": incentive.get("requirements", []),
                    "geographic_limits": incentive.get("eligible_areas", []),
                    "project_minimums": incentive.get("min_investment", 0),
                    "job_requirements": incentive.get("job_creation", 0),
                    "clawback_provisions": incentive.get("clawback", False)
                })
        
        # Grant programs
        grants = incentive_data.get("grant_programs", [])
        for grant in grants:
            if isinstance(grant, dict) and grant.get("funding_available", 0) > 0:
                incentives.append({
                    "type": "grant",
                    "program": grant.get("name", ""),
                    "max_award": grant.get("max_grant", 0),
                    "matching_required": grant.get("match_requirement", 0),
                    "eligible_uses": grant.get("eligible_expenses", []),
                    "application_window": grant.get("application_period", ""),
                    "competitive": grant.get("competitive", True),
                    "success_factors": grant.get("selection_criteria", [])
                })
        
        # Sort by value
        incentives.sort(key=lambda x: x.get("value", 0) or x.get("max_award", 0), reverse=True)
        
        return incentives[:10]  # Top 10 incentives
    
    def _assess_regulatory_risks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess regulatory risks and compliance challenges"""
        risk_data = data.get("aggregated_data", {}).get("regulatory_risks", {})
        
        risk_assessment = {
            "high_risk_areas": [],
            "enforcement_trends": {},
            "penalty_analysis": {},
            "mitigation_priorities": []
        }
        
        # High risk regulatory areas
        risk_areas = risk_data.get("risk_areas", {})
        for area, risk_level in risk_areas.items():
            if isinstance(risk_level, dict) and risk_level.get("risk_score", 0) > 7:
                risk_assessment["high_risk_areas"].append({
                    "area": area,
                    "risk_score": risk_level.get("risk_score", 0),
                    "primary_concern": risk_level.get("main_issue", ""),
                    "recent_violations": risk_level.get("violations_ytd", 0),
                    "avg_penalty": risk_level.get("avg_fine", 0),
                    "compliance_complexity": risk_level.get("complexity", "high")
                })
        
        # Enforcement trends
        enforcement = risk_data.get("enforcement_data", {})
        risk_assessment["enforcement_trends"] = {
            "inspection_frequency": enforcement.get("inspections_per_project", 0),
            "violation_rate": enforcement.get("violation_rate", 0),
            "fine_trend": enforcement.get("fine_trend", "increasing"),
            "focus_areas": enforcement.get("enforcement_priorities", []),
            "grace_period": enforcement.get("typical_cure_period", 30)
        }
        
        # Penalty analysis
        penalties = risk_data.get("penalty_data", {})
        risk_assessment["penalty_analysis"] = {
            "avg_fine_per_violation": penalties.get("avg_fine", 0),
            "max_fine_observed": penalties.get("max_fine", 0),
            "stop_work_probability": penalties.get("stop_work_rate", 0),
            "criminal_prosecution_risk": penalties.get("criminal_referrals", 0) > 0,
            "reputation_impact": penalties.get("public_disclosure", True)
        }
        
        return risk_assessment
    
    def _analyze_strategic_positioning(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze strategic positioning opportunities through regulatory expertise"""
        strategic_data = data.get("aggregated_data", {})
        
        positioning = {
            "competitive_advantages": [],
            "first_mover_opportunities": [],
            "regulatory_arbitrage": [],
            "partnership_opportunities": []
        }
        
        # Competitive advantages through compliance
        positioning["competitive_advantages"] = [
            {
                "advantage": "Expedited permitting track record",
                "benefit": "30% faster project delivery",
                "requirement": "95%+ permit approval rate",
                "market_value": "Premium pricing justified"
            },
            {
                "advantage": "Green building expertise",
                "benefit": "Access to sustainability incentives",
                "requirement": "LEED AP on staff",
                "market_value": "Institutional investor preference"
            }
        ]
        
        # First mover opportunities
        upcoming_regs = strategic_data.get("regulatory_changes", {}).get("proposed_changes", [])
        for reg in upcoming_regs:
            if isinstance(reg, dict) and reg.get("early_adopter_benefit"):
                positioning["first_mover_opportunities"].append({
                    "opportunity": reg.get("name", ""),
                    "timeline": reg.get("expected_date", ""),
                    "first_mover_benefit": reg.get("early_adopter_benefit", ""),
                    "investment_required": reg.get("prep_cost", 0),
                    "competitive_moat": reg.get("complexity", "medium")
                })
        
        # Regulatory arbitrage
        zoning_data = strategic_data.get("zoning_analysis", {})
        for zone, details in zoning_data.get("arbitrage_opportunities", {}).items():
            if isinstance(details, dict):
                positioning["regulatory_arbitrage"].append({
                    "location": zone,
                    "opportunity": details.get("arbitrage_type", ""),
                    "value_delta": details.get("value_difference", 0),
                    "execution_complexity": details.get("complexity", "medium"),
                    "timeline": details.get("execution_months", 12)
                })
        
        return positioning
    
    def _calculate_zoning_uplift(self, activity: Dict[str, Any]) -> float:
        """Calculate value uplift from rezoning"""
        current_value = activity.get("current_value_psf", 100)
        target_value = activity.get("target_value_psf", 150)
        
        uplift = ((target_value - current_value) / current_value) * 100
        return round(uplift, 1)
    
    def _estimate_overlay_value(self, benefits: Dict[str, Any]) -> float:
        """Estimate value of overlay district benefits"""
        value = 0
        
        # Parking reduction value (assume $25k per space)
        value += benefits.get("parking_reduction", 0) * 25000
        
        # Height bonus value (assume $50 per additional sqft)
        value += benefits.get("height_bonus", 0) * 1000 * 50  # 1000 sqft per floor estimate
        
        # Fast track value (time value of money)
        if benefits.get("fast_track", False):
            value += 100000  # Estimated value of faster delivery
        
        return value
    
    def _analyze_density_bonus_roi(self, program: Dict[str, Any]) -> Dict[str, float]:
        """Analyze ROI of density bonus programs"""
        bonus_pct = program.get("max_bonus", 0)
        requirement_cost = program.get("compliance_cost", 0)
        
        # Assume $200/sqft development value
        bonus_value = bonus_pct * 200 * 1000  # Per 1000 sqft of bonus
        
        roi = ((bonus_value - requirement_cost) / requirement_cost * 100) if requirement_cost > 0 else 999
        
        return {
            "bonus_value": bonus_value,
            "requirement_cost": requirement_cost,
            "net_benefit": bonus_value - requirement_cost,
            "roi_pct": round(roi, 1)
        }
    
    def _calculate_fast_track_roi(self, program: Dict[str, Any]) -> float:
        """Calculate ROI of fast track programs"""
        time_saved_days = program.get("time_reduction", 0) * program.get("standard_timeline", 180) / 100
        daily_carry_cost = 5000  # Estimated daily carrying cost
        
        savings = time_saved_days * daily_carry_cost
        cost = program.get("premium_cost", 0)
        
        roi = ((savings - cost) / cost * 100) if cost > 0 else 999
        return round(roi, 1)
    
    def _extract_key_findings(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key findings from regulatory analysis"""
        findings = []
        
        # Zoning opportunities
        zoning = insights.get("zoning_opportunities", {})
        rezoning_candidates = zoning.get("rezoning_candidates", [])
        if rezoning_candidates:
            best = max(rezoning_candidates, key=lambda x: x.get("value_uplift", 0))
            findings.append(f"{best['area']} rezoning opportunity offers {best['value_uplift']}% value uplift")
        
        # Permit optimization
        permits = insights.get("permit_optimization", {})
        fast_track = permits.get("fast_track_options", [])
        if fast_track:
            best_program = max(fast_track, key=lambda x: x.get("time_savings_pct", 0))
            findings.append(f"Fast track permits can reduce timeline by {best_program['time_savings_pct']}%")
        
        # Development incentives
        incentives = insights.get("development_incentives", [])
        if incentives:
            total_value = sum(i.get("value", 0) or i.get("max_award", 0) for i in incentives[:3])
            findings.append(f"${total_value:,.0f} in development incentives available")
        
        # Regulatory changes
        changes = insights.get("regulatory_changes", {})
        upcoming = changes.get("upcoming_changes", [])
        if upcoming:
            high_impact = [c for c in upcoming if c.get("impact_level") == "high"]
            if high_impact:
                findings.append(f"{len(high_impact)} high-impact regulatory changes expected")
        
        # Strategic positioning
        positioning = insights.get("strategic_positioning", {})
        if positioning.get("first_mover_opportunities"):
            findings.append("First-mover advantages available in upcoming regulatory changes")
        
        return findings[:5]
    
    def _identify_risks(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify regulatory risks"""
        risks = []
        
        # Compliance risks
        risk_assessment = insights.get("risk_assessment", {})
        high_risk_areas = risk_assessment.get("high_risk_areas", [])
        if high_risk_areas:
            highest_risk = max(high_risk_areas, key=lambda x: x.get("risk_score", 0))
            risks.append({
                "type": "compliance_risk",
                "severity": "high",
                "description": f"{highest_risk['area']} compliance complexity with {highest_risk['recent_violations']} recent violations",
                "financial_impact": f"Average penalty ${highest_risk['avg_penalty']:,.0f}",
                "mitigation": "Implement comprehensive compliance program with regular audits"
            })
        
        # Regulatory change risks
        changes = insights.get("regulatory_changes", {})
        if changes.get("trend_analysis", {}).get("direction") == "increasing_regulation":
            risks.append({
                "type": "regulatory_burden",
                "severity": "medium",
                "description": "Increasing regulatory complexity and enforcement intensity",
                "financial_impact": "15-20% increase in compliance costs projected",
                "mitigation": "Build regulatory expertise and automate compliance processes"
            })
        
        # Permit delay risks
        permits = insights.get("permit_optimization", {})
        common_delays = permits.get("common_delays", [])
        if common_delays:
            total_delay_cost = sum(d.get("cost_impact", 0) for d in common_delays)
            risks.append({
                "type": "permit_delays",
                "severity": "medium",
                "description": "Common permit delays averaging 30-60 days",
                "financial_impact": f"${total_delay_cost:,.0f} average delay cost",
                "mitigation": "Use pre-application meetings and third-party review"
            })
        
        return risks
    
    def _identify_opportunities(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify regulatory opportunities"""
        opportunities = []
        
        # Rezoning opportunities
        zoning = insights.get("zoning_opportunities", {})
        rezoning = zoning.get("rezoning_candidates", [])
        for candidate in rezoning[:2]:  # Top 2
            opportunities.append({
                "type": "rezoning_arbitrage",
                "potential": "high",
                "description": f"{candidate['area']} rezoning to {candidate['target_zoning']}",
                "value_creation": f"{candidate['value_uplift']}% land value increase",
                "action": f"File rezoning application (approval probability {candidate['approval_probability']}%)"
            })
        
        # Density bonus opportunities
        density_bonuses = zoning.get("density_bonuses", [])
        for bonus in density_bonuses:
            if bonus.get("cost_benefit", {}).get("roi_pct", 0) > 50:
                opportunities.append({
                    "type": "density_bonus",
                    "potential": "high",
                    "description": f"{bonus['program']} offers {bonus['bonus_percentage']}% density increase",
                    "value_creation": f"{bonus['cost_benefit']['roi_pct']}% ROI",
                    "action": "Incorporate affordable housing to qualify for bonus"
                })
        
        # Incentive opportunities
        incentives = insights.get("development_incentives", [])
        for incentive in incentives[:2]:  # Top 2
            opportunities.append({
                "type": "financial_incentive",
                "potential": "medium" if incentive.get("value", 0) < 500000 else "high",
                "description": incentive["program"],
                "value_creation": f"${incentive.get('value', 0) or incentive.get('max_award', 0):,.0f}",
                "action": f"Apply by {incentive.get('application_deadline', 'next cycle')}"
            })
        
        # Strategic positioning
        positioning = insights.get("strategic_positioning", {})
        if positioning.get("first_mover_opportunities"):
            opportunities.append({
                "type": "first_mover_advantage",
                "potential": "high",
                "description": "Early adoption of upcoming regulations",
                "value_creation": "Competitive moat and premium positioning",
                "action": "Begin compliance preparations now"
            })
        
        return opportunities[:5]
    
    def _generate_recommendations(self, insights: Dict[str, Any], 
                                risks: List[Dict], 
                                opportunities: List[Dict]) -> List[str]:
        """Generate actionable regulatory recommendations"""
        recommendations = []
        
        # Based on zoning opportunities
        zoning = insights.get("zoning_opportunities", {})
        if zoning.get("rezoning_candidates"):
            recommendations.append("Pursue strategic rezoning in high-uplift areas with >60% approval probability")
        
        # Based on permit optimization
        permits = insights.get("permit_optimization", {})
        if permits.get("fast_track_options"):
            recommendations.append("Utilize fast-track permitting for 40%+ timeline reduction on eligible projects")
        
        # Based on incentives
        incentives = insights.get("development_incentives", [])
        if sum(i.get("value", 0) or i.get("max_award", 0) for i in incentives) > 1000000:
            recommendations.append("Stack multiple incentive programs to maximize project returns")
        
        # Based on compliance
        if any(r["type"] == "compliance_risk" for r in risks):
            recommendations.append("Establish dedicated compliance team to manage regulatory complexity")
        
        # Based on strategic positioning
        positioning = insights.get("strategic_positioning", {})
        if positioning.get("competitive_advantages"):
            recommendations.append("Build regulatory expertise as competitive differentiator")
        
        return recommendations[:5]
    
    def _extract_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract key regulatory metrics"""
        metrics = {}
        
        # Zoning metrics
        zoning = insights.get("zoning_opportunities", {})
        rezoning = zoning.get("rezoning_candidates", [])
        if rezoning:
            metrics["avg_rezoning_uplift"] = np.mean([r["value_uplift"] for r in rezoning])
            metrics["rezoning_approval_rate"] = np.mean([r["approval_probability"] for r in rezoning])
        
        # Permit metrics
        permits = insights.get("permit_optimization", {})
        approval_times = permits.get("approval_times", {})
        if approval_times:
            standard_times = [t["standard_days"] for t in approval_times.values() if isinstance(t, dict)]
            metrics["avg_permit_days"] = np.mean(standard_times) if standard_times else 0
        
        fast_track = permits.get("fast_track_options", [])
        if fast_track:
            metrics["max_fast_track_savings"] = max(f["time_savings_pct"] for f in fast_track)
        
        # Incentive metrics
        incentives = insights.get("development_incentives", [])
        metrics["total_incentives_available"] = sum(
            i.get("value", 0) or i.get("max_award", 0) for i in incentives
        )
        
        # Risk metrics
        risk_assessment = insights.get("risk_assessment", {})
        enforcement = risk_assessment.get("enforcement_trends", {})
        metrics["violation_rate"] = enforcement.get("violation_rate", 0)
        metrics["avg_penalty"] = risk_assessment.get("penalty_analysis", {}).get("avg_fine_per_violation", 0)
        
        return metrics