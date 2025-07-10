"""
Neighborhood Intelligence Analyzer - Area-specific insights and opportunities
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


class NeighborhoodIntelligenceAnalyzer(BaseIntelligenceAnalyzer):
    """Analyzes neighborhood-specific trends, opportunities, and growth patterns"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("neighborhood_intelligence", config)
        
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform neighborhood-specific analysis"""
        insights = {
            "area_rankings": self._rank_neighborhoods(data),
            "price_trends_by_area": self._analyze_area_prices(data),
            "inventory_analysis": self._analyze_inventory(data),
            "growth_patterns": self._identify_growth_patterns(data),
            "investment_opportunities": self._identify_investment_opportunities(data),
            "demographic_insights": self._analyze_demographics(data),
            "infrastructure_impact": self._assess_infrastructure_impact(data)
        }
        return insights
    
    def _rank_neighborhoods(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank neighborhoods by various metrics"""
        neighborhoods = data.get("aggregated_data", {}).get("neighborhoods", {})
        
        rankings = []
        for name, metrics in neighborhoods.items():
            score = self._calculate_neighborhood_score(metrics)
            rankings.append({
                "neighborhood": name,
                "overall_score": score,
                "price_growth": metrics.get("price_growth", 0),
                "inventory_level": metrics.get("inventory", 0),
                "days_on_market": metrics.get("dom", 0),
                "investment_grade": self._determine_investment_grade(score),
                "key_strengths": self._identify_strengths(metrics)
            })
        
        # Sort by overall score
        rankings.sort(key=lambda x: x["overall_score"], reverse=True)
        return rankings[:10]  # Top 10 neighborhoods
    
    def _analyze_area_prices(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze price trends by area"""
        price_data = data.get("aggregated_data", {}).get("price_trends", {})
        
        analysis = {
            "hottest_areas": [],
            "cooling_areas": [],
            "stable_areas": [],
            "price_predictions": {}
        }
        
        for area, prices in price_data.items():
            if isinstance(prices, list) and len(prices) > 0:
                trend = self._calculate_price_trend(prices)
                forecast = self._forecast_prices(prices)
                
                area_analysis = {
                    "area": area,
                    "current_price": prices[-1] if prices else 0,
                    "yoy_change": trend["yoy_change"],
                    "momentum": trend["momentum"],
                    "forecast_12m": forecast
                }
                
                # Categorize areas
                if trend["momentum"] > 0.05:
                    analysis["hottest_areas"].append(area_analysis)
                elif trend["momentum"] < -0.02:
                    analysis["cooling_areas"].append(area_analysis)
                else:
                    analysis["stable_areas"].append(area_analysis)
                
                analysis["price_predictions"][area] = forecast
        
        # Sort by momentum
        analysis["hottest_areas"].sort(key=lambda x: x["momentum"], reverse=True)
        analysis["cooling_areas"].sort(key=lambda x: x["momentum"])
        
        return analysis
    
    def _analyze_inventory(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze inventory levels and trends"""
        inventory_data = data.get("aggregated_data", {}).get("inventory", {})
        
        analysis = {
            "current_levels": {},
            "supply_demand_ratio": {},
            "months_of_inventory": {},
            "inventory_trends": {}
        }
        
        for area, inv_data in inventory_data.items():
            if isinstance(inv_data, dict):
                supply = inv_data.get("active_listings", 0)
                demand = inv_data.get("monthly_sales", 1)
                
                analysis["current_levels"][area] = supply
                analysis["supply_demand_ratio"][area] = supply / demand if demand > 0 else 999
                analysis["months_of_inventory"][area] = supply / demand if demand > 0 else 999
                
                # Determine trend
                if analysis["months_of_inventory"][area] < 3:
                    analysis["inventory_trends"][area] = "sellers_market"
                elif analysis["months_of_inventory"][area] > 6:
                    analysis["inventory_trends"][area] = "buyers_market"
                else:
                    analysis["inventory_trends"][area] = "balanced"
        
        return analysis
    
    def _identify_growth_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify neighborhood growth patterns"""
        development_data = data.get("aggregated_data", {}).get("development_activity", {})
        
        patterns = {
            "emerging_hotspots": [],
            "mature_markets": [],
            "transitioning_areas": [],
            "growth_drivers": {}
        }
        
        for area, activity in development_data.items():
            if isinstance(activity, dict):
                permits = activity.get("building_permits", 0)
                new_construction = activity.get("new_construction", 0)
                commercial_dev = activity.get("commercial_development", 0)
                
                # Calculate growth score
                growth_score = (permits * 0.3 + new_construction * 0.5 + commercial_dev * 0.2)
                
                area_profile = {
                    "area": area,
                    "growth_score": growth_score,
                    "permit_activity": permits,
                    "new_construction": new_construction,
                    "development_type": self._categorize_development(activity)
                }
                
                # Categorize areas
                if growth_score > 75:
                    patterns["emerging_hotspots"].append(area_profile)
                elif growth_score > 40:
                    patterns["transitioning_areas"].append(area_profile)
                else:
                    patterns["mature_markets"].append(area_profile)
                
                # Identify growth drivers
                patterns["growth_drivers"][area] = self._identify_growth_drivers(activity)
        
        return patterns
    
    def _identify_investment_opportunities(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific investment opportunities by area"""
        opportunities = []
        
        # Combine various data sources
        price_analysis = self._analyze_area_prices(data)
        inventory_analysis = self._analyze_inventory(data)
        growth_patterns = self._identify_growth_patterns(data)
        
        # Find undervalued areas with growth potential
        for area in growth_patterns.get("emerging_hotspots", []):
            area_name = area["area"]
            
            opp = {
                "area": area_name,
                "opportunity_type": "emerging_growth",
                "investment_thesis": f"High growth activity ({area['growth_score']:.0f} score) with {area['permit_activity']} new permits",
                "risk_level": "medium",
                "projected_roi": self._calculate_projected_roi(area_name, data),
                "recommended_strategy": "Buy and develop",
                "time_horizon": "3-5 years"
            }
            opportunities.append(opp)
        
        # Find areas with favorable supply/demand dynamics
        for area, ratio in inventory_analysis.get("supply_demand_ratio", {}).items():
            if ratio < 2:  # Low inventory
                opp = {
                    "area": area,
                    "opportunity_type": "supply_constrained",
                    "investment_thesis": f"Low inventory ({ratio:.1f} months) creating price pressure",
                    "risk_level": "low",
                    "projected_roi": 15 + (2 - ratio) * 5,  # Higher ROI for tighter markets
                    "recommended_strategy": "Quick development and sale",
                    "time_horizon": "1-2 years"
                }
                opportunities.append(opp)
        
        # Sort by projected ROI
        opportunities.sort(key=lambda x: x.get("projected_roi", 0), reverse=True)
        return opportunities[:10]  # Top 10 opportunities
    
    def _analyze_demographics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze demographic trends by neighborhood"""
        demo_data = data.get("aggregated_data", {}).get("demographics", {})
        
        insights = {
            "high_income_areas": [],
            "growing_population": [],
            "young_professional_hubs": [],
            "family_neighborhoods": []
        }
        
        for area, demographics in demo_data.items():
            if isinstance(demographics, dict):
                profile = {
                    "area": area,
                    "median_income": demographics.get("median_income", 0),
                    "population_growth": demographics.get("pop_growth_rate", 0),
                    "median_age": demographics.get("median_age", 0),
                    "household_size": demographics.get("avg_household_size", 0)
                }
                
                # Categorize areas
                if profile["median_income"] > 100000:
                    insights["high_income_areas"].append(profile)
                
                if profile["population_growth"] > 3:
                    insights["growing_population"].append(profile)
                
                if 25 <= profile["median_age"] <= 35:
                    insights["young_professional_hubs"].append(profile)
                
                if profile["household_size"] > 2.5:
                    insights["family_neighborhoods"].append(profile)
        
        return insights
    
    def _assess_infrastructure_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess infrastructure developments and their impact"""
        infra_data = data.get("aggregated_data", {}).get("infrastructure", {})
        
        impact_analysis = {
            "transit_improvements": [],
            "school_districts": [],
            "commercial_development": [],
            "overall_impact_scores": {}
        }
        
        for area, infrastructure in infra_data.items():
            if isinstance(infrastructure, dict):
                # Calculate infrastructure score
                transit_score = infrastructure.get("transit_access", 0) * 10
                school_score = infrastructure.get("school_rating", 0) * 10
                amenity_score = infrastructure.get("amenity_score", 0)
                
                overall_score = (transit_score * 0.4 + school_score * 0.4 + amenity_score * 0.2)
                
                impact_analysis["overall_impact_scores"][area] = overall_score
                
                # Identify specific improvements
                if infrastructure.get("new_transit"):
                    impact_analysis["transit_improvements"].append({
                        "area": area,
                        "improvement": infrastructure.get("new_transit"),
                        "impact": "High - expect 10-15% price appreciation"
                    })
        
        return impact_analysis
    
    def _calculate_neighborhood_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall neighborhood score"""
        # Weighted scoring system
        price_growth = metrics.get("price_growth", 0) * 0.3
        low_inventory = (100 - metrics.get("inventory", 50)) * 0.2
        quick_sales = (100 - metrics.get("dom", 50)) * 0.2
        population_growth = metrics.get("pop_growth", 0) * 10 * 0.15
        income_level = min(metrics.get("median_income", 50000) / 1000, 100) * 0.15
        
        return min(price_growth + low_inventory + quick_sales + population_growth + income_level, 100)
    
    def _determine_investment_grade(self, score: float) -> str:
        """Determine investment grade based on score"""
        if score >= 80:
            return "A+"
        elif score >= 70:
            return "A"
        elif score >= 60:
            return "B+"
        elif score >= 50:
            return "B"
        else:
            return "C"
    
    def _identify_strengths(self, metrics: Dict[str, Any]) -> List[str]:
        """Identify neighborhood strengths"""
        strengths = []
        
        if metrics.get("price_growth", 0) > 10:
            strengths.append("Strong price appreciation")
        if metrics.get("dom", 90) < 30:
            strengths.append("Quick sales")
        if metrics.get("school_rating", 0) > 8:
            strengths.append("Excellent schools")
        if metrics.get("transit_score", 0) > 7:
            strengths.append("Great transit access")
        
        return strengths
    
    def _calculate_price_trend(self, prices: List[float]) -> Dict[str, float]:
        """Calculate price trend metrics"""
        if len(prices) < 2:
            return {"yoy_change": 0, "momentum": 0}
        
        # Year over year change
        current = prices[-1]
        year_ago = prices[-12] if len(prices) >= 12 else prices[0]
        yoy_change = ((current - year_ago) / year_ago) * 100 if year_ago > 0 else 0
        
        # Recent momentum (last 3 months)
        if len(prices) >= 3:
            recent_change = ((prices[-1] - prices[-3]) / prices[-3]) if prices[-3] > 0 else 0
            momentum = recent_change * 4  # Annualized
        else:
            momentum = yoy_change / 100
        
        return {"yoy_change": yoy_change, "momentum": momentum}
    
    def _forecast_prices(self, prices: List[float]) -> float:
        """Simple price forecast for next 12 months"""
        if len(prices) < 3:
            return prices[-1] if prices else 0
        
        # Simple linear regression forecast
        recent_prices = prices[-6:] if len(prices) >= 6 else prices
        avg_monthly_change = (recent_prices[-1] - recent_prices[0]) / len(recent_prices)
        
        # Project 12 months forward with some dampening
        forecast = prices[-1] + (avg_monthly_change * 12 * 0.8)  # 80% of trend continues
        
        return round(forecast, 2)
    
    def _categorize_development(self, activity: Dict[str, Any]) -> str:
        """Categorize development type"""
        res = activity.get("residential", 0)
        com = activity.get("commercial", 0)
        mixed = activity.get("mixed_use", 0)
        
        total = res + com + mixed
        if total == 0:
            return "minimal"
        
        if mixed / total > 0.3:
            return "mixed_use_focus"
        elif res / total > 0.6:
            return "residential_focus"
        elif com / total > 0.4:
            return "commercial_focus"
        else:
            return "balanced"
    
    def _identify_growth_drivers(self, activity: Dict[str, Any]) -> List[str]:
        """Identify what's driving growth in an area"""
        drivers = []
        
        if activity.get("tech_companies", 0) > 5:
            drivers.append("Tech sector growth")
        if activity.get("new_schools", 0) > 0:
            drivers.append("Education infrastructure")
        if activity.get("transit_projects", 0) > 0:
            drivers.append("Transit improvements")
        if activity.get("retail_development", 0) > 10000:
            drivers.append("Retail expansion")
        
        return drivers
    
    def _calculate_projected_roi(self, area: str, data: Dict[str, Any]) -> float:
        """Calculate projected ROI for an area"""
        # Simplified ROI calculation
        base_roi = 12.0  # Base return
        
        # Adjustments based on various factors
        price_data = data.get("aggregated_data", {}).get("price_trends", {}).get(area, [])
        if price_data:
            trend = self._calculate_price_trend(price_data)
            base_roi += trend["yoy_change"] * 0.5
        
        return round(min(max(base_roi, 5), 30), 1)  # Cap between 5-30%
    
    def _extract_key_findings(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key findings from neighborhood analysis"""
        findings = []
        
        # Top neighborhoods
        rankings = insights.get("area_rankings", [])
        if rankings:
            top_area = rankings[0]
            findings.append(f"{top_area['neighborhood']} leads with {top_area['overall_score']:.1f} score and {top_area['investment_grade']} grade")
        
        # Price trends
        price_analysis = insights.get("price_trends_by_area", {})
        if price_analysis.get("hottest_areas"):
            hottest = price_analysis["hottest_areas"][0]
            findings.append(f"{hottest['area']} showing strongest momentum with {hottest['yoy_change']:.1f}% YoY growth")
        
        # Inventory insights
        inventory = insights.get("inventory_analysis", {})
        tight_markets = [area for area, months in inventory.get("months_of_inventory", {}).items() if months < 2]
        if tight_markets:
            findings.append(f"{len(tight_markets)} neighborhoods have critically low inventory (<2 months)")
        
        # Growth patterns
        growth = insights.get("growth_patterns", {})
        if growth.get("emerging_hotspots"):
            findings.append(f"{len(growth['emerging_hotspots'])} emerging hotspots identified with high development activity")
        
        # Investment opportunities
        opportunities = insights.get("investment_opportunities", [])
        if opportunities:
            best = opportunities[0]
            findings.append(f"Top opportunity: {best['area']} with {best['projected_roi']:.1f}% projected ROI")
        
        return findings[:5]
    
    def _identify_risks(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify neighborhood-specific risks"""
        risks = []
        
        # Cooling markets risk
        price_analysis = insights.get("price_trends_by_area", {})
        cooling_areas = price_analysis.get("cooling_areas", [])
        if cooling_areas:
            risks.append({
                "type": "market_cooling",
                "severity": "medium",
                "description": f"{len(cooling_areas)} neighborhoods showing price declines",
                "affected_areas": [a["area"] for a in cooling_areas[:3]],
                "mitigation": "Avoid new developments in cooling areas or focus on value-add strategies"
            })
        
        # Oversupply risk
        inventory = insights.get("inventory_analysis", {})
        oversupplied = [area for area, months in inventory.get("months_of_inventory", {}).items() if months > 9]
        if oversupplied:
            risks.append({
                "type": "oversupply",
                "severity": "high",
                "description": f"{len(oversupplied)} neighborhoods have >9 months inventory",
                "affected_areas": oversupplied[:3],
                "mitigation": "Delay new projects or pivot to rental strategies"
            })
        
        # Demographic shifts
        demographics = insights.get("demographic_insights", {})
        if not demographics.get("growing_population"):
            risks.append({
                "type": "population_stagnation",
                "severity": "low",
                "description": "Limited population growth in key areas",
                "mitigation": "Focus on areas with employment growth or transit improvements"
            })
        
        return risks
    
    def _identify_opportunities(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify neighborhood opportunities"""
        opportunities = []
        
        # Already have investment opportunities from analysis
        inv_opps = insights.get("investment_opportunities", [])
        for opp in inv_opps[:3]:  # Top 3
            opportunities.append({
                "type": opp["opportunity_type"],
                "potential": "high" if opp["projected_roi"] > 20 else "medium",
                "description": opp["investment_thesis"],
                "action": opp["recommended_strategy"],
                "location": opp["area"]
            })
        
        # Infrastructure opportunities
        infra = insights.get("infrastructure_impact", {})
        for improvement in infra.get("transit_improvements", [])[:2]:
            opportunities.append({
                "type": "infrastructure_catalyst",
                "potential": "high",
                "description": f"New transit in {improvement['area']}: {improvement['improvement']}",
                "action": "Acquire properties near transit before appreciation",
                "location": improvement["area"]
            })
        
        # Demographic opportunities
        demo = insights.get("demographic_insights", {})
        if demo.get("young_professional_hubs"):
            opportunities.append({
                "type": "demographic_shift",
                "potential": "medium",
                "description": f"{len(demo['young_professional_hubs'])} areas attracting young professionals",
                "action": "Develop modern apartments and mixed-use projects",
                "location": ", ".join([h["area"] for h in demo["young_professional_hubs"][:3]])
            })
        
        return opportunities[:5]
    
    def _generate_recommendations(self, insights: Dict[str, Any], 
                                risks: List[Dict], 
                                opportunities: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on top neighborhoods
        rankings = insights.get("area_rankings", [])
        if rankings:
            top_areas = [r["neighborhood"] for r in rankings[:3]]
            recommendations.append(f"Prioritize development in top-ranked areas: {', '.join(top_areas)}")
        
        # Based on inventory
        inventory = insights.get("inventory_analysis", {})
        tight_markets = [area for area, months in inventory.get("months_of_inventory", {}).items() if months < 3]
        if tight_markets:
            recommendations.append(f"Fast-track projects in supply-constrained areas: {', '.join(tight_markets[:3])}")
        
        # Based on price trends
        price_analysis = insights.get("price_trends_by_area", {})
        if price_analysis.get("hottest_areas"):
            recommendations.append("Lock in land acquisitions in high-momentum areas before further appreciation")
        
        # Based on opportunities
        if opportunities:
            if any(o["type"] == "infrastructure_catalyst" for o in opportunities):
                recommendations.append("Acquire properties near planned transit improvements for 10-15% appreciation")
        
        # Based on risks
        if any(r["type"] == "oversupply" for r in risks):
            recommendations.append("Shift focus to build-to-rent in oversupplied markets")
        
        return recommendations[:5]
    
    def _extract_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from analysis"""
        metrics = {}
        
        # Top area metrics
        rankings = insights.get("area_rankings", [])
        if rankings:
            metrics["top_area_score"] = rankings[0]["overall_score"]
            metrics["avg_top5_score"] = np.mean([r["overall_score"] for r in rankings[:5]])
        
        # Price metrics
        price_analysis = insights.get("price_trends_by_area", {})
        all_yoy_changes = []
        for area_group in ["hottest_areas", "cooling_areas", "stable_areas"]:
            areas = price_analysis.get(area_group, [])
            all_yoy_changes.extend([a["yoy_change"] for a in areas])
        
        if all_yoy_changes:
            metrics["avg_yoy_price_change"] = np.mean(all_yoy_changes)
            metrics["max_yoy_price_change"] = max(all_yoy_changes)
        
        # Inventory metrics
        inventory = insights.get("inventory_analysis", {})
        months_inv = list(inventory.get("months_of_inventory", {}).values())
        if months_inv:
            metrics["avg_months_inventory"] = np.mean(months_inv)
            metrics["min_months_inventory"] = min(months_inv)
        
        # Opportunity metrics
        opportunities = insights.get("investment_opportunities", [])
        if opportunities:
            rois = [o["projected_roi"] for o in opportunities]
            metrics["avg_projected_roi"] = np.mean(rois)
            metrics["max_projected_roi"] = max(rois)
        
        return metrics