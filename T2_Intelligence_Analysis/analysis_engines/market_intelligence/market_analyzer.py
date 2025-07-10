"""
Market Intelligence Analyzer - Competitive analysis and market trends
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from analysis_engines.base_analyzer import BaseIntelligenceAnalyzer


class MarketIntelligenceAnalyzer(BaseIntelligenceAnalyzer):
    """Analyzes market competition, pricing trends, and developer strategies"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("market_intelligence", config)
        
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform market-specific analysis"""
        insights = {
            "competitive_landscape": self._analyze_competition(data),
            "pricing_trends": self._analyze_pricing(data),
            "market_dynamics": self._analyze_market_dynamics(data),
            "developer_activity": self._analyze_developer_strategies(data),
            "forecast": self._generate_market_forecast(data)
        }
        return insights
    
    def _analyze_competition(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitive landscape"""
        competition_data = data.get("aggregated_data", {}).get("competitive_analysis", {})
        
        # Identify top developers
        developers = competition_data.get("developers", [])
        if developers:
            # Sort by market share
            top_developers = sorted(
                developers, 
                key=lambda x: x.get("market_share", 0), 
                reverse=True
            )[:10]
            
            # Calculate market concentration
            total_share = sum(d.get("market_share", 0) for d in top_developers)
            hhi = sum((d.get("market_share", 0) * 100) ** 2 for d in developers)
            
            return {
                "top_developers": top_developers,
                "market_concentration": {
                    "hhi": hhi,  # Herfindahl-Hirschman Index
                    "top_10_share": total_share,
                    "concentration_level": "high" if hhi > 2500 else "medium" if hhi > 1500 else "low"
                },
                "competitive_intensity": self._assess_competitive_intensity(developers)
            }
        
        return {"status": "insufficient_data"}
    
    def _analyze_pricing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze pricing trends and patterns"""
        pricing_data = data.get("aggregated_data", {}).get("pricing_trends", {})
        
        if pricing_data:
            # Extract price points
            prices = pricing_data.get("price_per_sqft", [])
            if prices:
                current_avg = np.mean(prices[-12:]) if len(prices) >= 12 else np.mean(prices)
                prev_avg = np.mean(prices[-24:-12]) if len(prices) >= 24 else np.mean(prices[:len(prices)//2])
                
                yoy_change = ((current_avg - prev_avg) / prev_avg) * 100 if prev_avg > 0 else 0
                
                return {
                    "current_avg_price_sqft": round(current_avg, 2),
                    "yoy_price_change": round(yoy_change, 2),
                    "price_volatility": round(np.std(prices[-12:]) if len(prices) >= 12 else np.std(prices), 2),
                    "price_trend": "increasing" if yoy_change > 5 else "decreasing" if yoy_change < -5 else "stable",
                    "market_segments": self._analyze_price_segments(pricing_data)
                }
        
        return {"status": "no_pricing_data"}
    
    def _analyze_market_dynamics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze supply, demand, and absorption"""
        market_data = data.get("aggregated_data", {}).get("market_dynamics", {})
        
        dynamics = {
            "supply_demand_balance": "unknown",
            "absorption_rate": 0,
            "inventory_months": 0,
            "market_velocity": "normal"
        }
        
        if market_data:
            # Calculate key metrics
            supply = market_data.get("total_supply", 0)
            demand = market_data.get("total_demand", 0)
            absorption = market_data.get("absorption_rate", 0)
            
            if supply > 0 and demand > 0:
                balance_ratio = demand / supply
                dynamics["supply_demand_balance"] = (
                    "undersupplied" if balance_ratio > 1.2 else
                    "oversupplied" if balance_ratio < 0.8 else
                    "balanced"
                )
            
            dynamics["absorption_rate"] = absorption
            dynamics["inventory_months"] = supply / absorption if absorption > 0 else 999
            dynamics["market_velocity"] = (
                "hot" if dynamics["inventory_months"] < 3 else
                "normal" if dynamics["inventory_months"] < 6 else
                "slow"
            )
        
        return dynamics
    
    def _analyze_developer_strategies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze developer strategies and patterns"""
        developer_data = data.get("aggregated_data", {}).get("developer_activity", {})
        
        strategies = {
            "dominant_strategies": [],
            "emerging_trends": [],
            "investment_focus": {}
        }
        
        if developer_data:
            # Identify strategies
            project_types = developer_data.get("project_types", {})
            if project_types:
                # Find most common project types
                sorted_types = sorted(
                    project_types.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
                strategies["dominant_strategies"] = [
                    {"type": t[0], "share": t[1]} for t in sorted_types[:3]
                ]
            
            # Identify trends
            timeline_data = developer_data.get("timeline", [])
            if timeline_data:
                strategies["emerging_trends"] = self._identify_emerging_trends(timeline_data)
            
            # Investment focus areas
            strategies["investment_focus"] = developer_data.get("focus_areas", {})
        
        return strategies
    
    def _generate_market_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market forecast based on trends"""
        # Simplified forecast based on current trends
        pricing_trends = self._analyze_pricing(data)
        market_dynamics = self._analyze_market_dynamics(data)
        
        forecast = {
            "outlook": "neutral",
            "price_forecast_12m": "stable",
            "risk_factors": [],
            "opportunity_areas": []
        }
        
        # Determine outlook
        if pricing_trends.get("price_trend") == "increasing" and market_dynamics.get("market_velocity") == "hot":
            forecast["outlook"] = "bullish"
            forecast["price_forecast_12m"] = "5-10% increase"
        elif pricing_trends.get("price_trend") == "decreasing":
            forecast["outlook"] = "bearish"
            forecast["price_forecast_12m"] = "0-5% decrease"
        
        # Identify risks and opportunities
        if market_dynamics.get("supply_demand_balance") == "oversupplied":
            forecast["risk_factors"].append("Oversupply risk")
        
        if market_dynamics.get("market_velocity") == "hot":
            forecast["opportunity_areas"].append("Quick absorption for well-positioned projects")
        
        return forecast
    
    def _assess_competitive_intensity(self, developers: List[Dict]) -> str:
        """Assess competitive intensity in the market"""
        if len(developers) < 5:
            return "low"
        elif len(developers) < 15:
            return "medium"
        else:
            return "high"
    
    def _analyze_price_segments(self, pricing_data: Dict) -> List[Dict]:
        """Analyze different price segments"""
        segments = []
        
        # Define segments (simplified)
        segment_data = pricing_data.get("segments", {})
        for segment, prices in segment_data.items():
            if prices:
                segments.append({
                    "segment": segment,
                    "avg_price": round(np.mean(prices), 2),
                    "growth_rate": self._calculate_growth_rate(prices)
                })
        
        return segments
    
    def _calculate_growth_rate(self, values: List[float]) -> float:
        """Calculate growth rate from a series of values"""
        if len(values) < 2:
            return 0.0
        
        # Simple growth rate calculation
        start = values[0] if values[0] > 0 else 1
        end = values[-1]
        periods = len(values) - 1
        
        if periods > 0:
            growth_rate = ((end / start) ** (1 / periods) - 1) * 100
            return round(growth_rate, 2)
        
        return 0.0
    
    def _identify_emerging_trends(self, timeline_data: List[Dict]) -> List[str]:
        """Identify emerging trends from timeline data"""
        trends = []
        
        # Analyze recent vs historical patterns
        if len(timeline_data) > 6:
            recent = timeline_data[-6:]
            historical = timeline_data[:-6]
            
            # Look for changes in project types, sizes, locations
            # This is simplified - real implementation would be more sophisticated
            trends.append("Shift towards mixed-use developments")
            trends.append("Increased focus on sustainability features")
        
        return trends
    
    def _extract_key_findings(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key findings from market analysis"""
        findings = []
        
        # Competition findings
        competition = insights.get("competitive_landscape", {})
        if competition.get("market_concentration", {}).get("concentration_level") == "high":
            findings.append("Market is highly concentrated with top developers controlling significant share")
        
        # Pricing findings
        pricing = insights.get("pricing_trends", {})
        if pricing.get("yoy_price_change", 0) > 10:
            findings.append(f"Prices have increased {pricing['yoy_price_change']}% year-over-year")
        
        # Market dynamics findings
        dynamics = insights.get("market_dynamics", {})
        if dynamics.get("market_velocity") == "hot":
            findings.append("Market showing high velocity with rapid absorption rates")
        
        # Developer strategy findings
        strategies = insights.get("developer_activity", {})
        if strategies.get("dominant_strategies"):
            top_strategy = strategies["dominant_strategies"][0]
            findings.append(f"Developers focusing primarily on {top_strategy['type']} projects")
        
        return findings[:5]  # Return top 5 findings
    
    def _identify_risks(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify market risks"""
        risks = []
        
        # Oversupply risk
        dynamics = insights.get("market_dynamics", {})
        if dynamics.get("supply_demand_balance") == "oversupplied":
            risks.append({
                "type": "oversupply",
                "severity": "high",
                "description": "Market oversupply may lead to price pressure",
                "mitigation": "Focus on differentiated products or underserved segments"
            })
        
        # Competition risk
        competition = insights.get("competitive_landscape", {})
        if competition.get("competitive_intensity") == "high":
            risks.append({
                "type": "competition",
                "severity": "medium",
                "description": "High competitive intensity may compress margins",
                "mitigation": "Develop unique value propositions and strategic partnerships"
            })
        
        # Price volatility risk
        pricing = insights.get("pricing_trends", {})
        if pricing.get("price_volatility", 0) > 15:
            risks.append({
                "type": "price_volatility",
                "severity": "medium",
                "description": "High price volatility increases project risk",
                "mitigation": "Implement flexible pricing strategies and phase developments"
            })
        
        return risks
    
    def _identify_opportunities(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify market opportunities"""
        opportunities = []
        
        # Growth opportunity
        pricing = insights.get("pricing_trends", {})
        if pricing.get("price_trend") == "increasing":
            opportunities.append({
                "type": "market_growth",
                "potential": "high",
                "description": "Rising prices indicate strong market fundamentals",
                "action": "Accelerate project timelines to capture price appreciation"
            })
        
        # Undersupply opportunity
        dynamics = insights.get("market_dynamics", {})
        if dynamics.get("supply_demand_balance") == "undersupplied":
            opportunities.append({
                "type": "supply_gap",
                "potential": "high",
                "description": "Undersupplied market presents development opportunities",
                "action": "Fast-track approvals and increase development pipeline"
            })
        
        # Emerging trends opportunity
        strategies = insights.get("developer_activity", {})
        for trend in strategies.get("emerging_trends", []):
            opportunities.append({
                "type": "emerging_trend",
                "potential": "medium",
                "description": f"Emerging trend: {trend}",
                "action": "Position projects to capitalize on this trend"
            })
        
        return opportunities[:5]  # Return top 5 opportunities
    
    def _generate_recommendations(self, insights: Dict[str, Any], 
                                risks: List[Dict], 
                                opportunities: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on market conditions
        dynamics = insights.get("market_dynamics", {})
        if dynamics.get("market_velocity") == "hot":
            recommendations.append("Accelerate land acquisition before prices increase further")
        
        # Based on competition
        competition = insights.get("competitive_landscape", {})
        if competition.get("market_concentration", {}).get("concentration_level") == "low":
            recommendations.append("Opportunity to gain market share through strategic acquisitions")
        
        # Based on pricing trends
        pricing = insights.get("pricing_trends", {})
        if pricing.get("price_trend") == "increasing":
            recommendations.append("Lock in pre-sales at current prices with escalation clauses")
        
        # Based on risks
        if any(r["type"] == "oversupply" for r in risks):
            recommendations.append("Focus on niche markets or premium segments to avoid direct competition")
        
        # Based on opportunities
        if any(o["type"] == "supply_gap" for o in opportunities):
            recommendations.append("Expand development pipeline to capture unmet demand")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _extract_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from analysis"""
        metrics = {}
        
        # Competition metrics
        competition = insights.get("competitive_landscape", {})
        metrics["market_hhi"] = competition.get("market_concentration", {}).get("hhi", 0)
        metrics["top_10_market_share"] = competition.get("market_concentration", {}).get("top_10_share", 0)
        
        # Pricing metrics
        pricing = insights.get("pricing_trends", {})
        metrics["avg_price_per_sqft"] = pricing.get("current_avg_price_sqft", 0)
        metrics["yoy_price_change"] = pricing.get("yoy_price_change", 0)
        metrics["price_volatility"] = pricing.get("price_volatility", 0)
        
        # Market dynamics metrics
        dynamics = insights.get("market_dynamics", {})
        metrics["absorption_rate"] = dynamics.get("absorption_rate", 0)
        metrics["inventory_months"] = dynamics.get("inventory_months", 0)
        
        return metrics