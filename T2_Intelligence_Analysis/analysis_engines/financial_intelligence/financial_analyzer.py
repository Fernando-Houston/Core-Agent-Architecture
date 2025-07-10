"""
Financial Intelligence Analyzer - ROI analysis, financing trends, and investment patterns
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


class FinancialIntelligenceAnalyzer(BaseIntelligenceAnalyzer):
    """Analyzes financial metrics, ROI projections, and investment opportunities"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("financial_intelligence", config)
        
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform financial-specific analysis"""
        insights = {
            "roi_analysis": self._analyze_roi_metrics(data),
            "lending_trends": self._analyze_lending_environment(data),
            "investment_patterns": self._analyze_investment_flows(data),
            "financing_options": self._evaluate_financing_options(data),
            "market_valuations": self._assess_market_valuations(data),
            "cash_flow_projections": self._project_cash_flows(data),
            "risk_adjusted_returns": self._calculate_risk_adjusted_returns(data)
        }
        return insights
    
    def _analyze_roi_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze return on investment metrics by project type and area"""
        financial_data = data.get("aggregated_data", {}).get("project_returns", {})
        
        roi_analysis = {
            "by_project_type": {},
            "by_area": {},
            "top_performers": [],
            "risk_return_profiles": {}
        }
        
        # Analyze by project type
        for project_type, returns in financial_data.get("by_type", {}).items():
            if isinstance(returns, list) and returns:
                avg_roi = np.mean(returns)
                std_dev = np.std(returns)
                sharpe_ratio = (avg_roi - 5) / std_dev if std_dev > 0 else 0  # 5% risk-free rate
                
                roi_analysis["by_project_type"][project_type] = {
                    "avg_roi": round(avg_roi, 2),
                    "std_deviation": round(std_dev, 2),
                    "sharpe_ratio": round(sharpe_ratio, 2),
                    "risk_level": self._categorize_risk(std_dev),
                    "percentile_25": round(np.percentile(returns, 25), 2),
                    "percentile_75": round(np.percentile(returns, 75), 2)
                }
        
        # Analyze by area
        for area, metrics in financial_data.get("by_area", {}).items():
            if isinstance(metrics, dict):
                roi_analysis["by_area"][area] = {
                    "avg_roi": metrics.get("avg_return", 0),
                    "cap_rate": metrics.get("cap_rate", 0),
                    "payback_period": metrics.get("payback_years", 0),
                    "irr": self._calculate_irr(metrics)
                }
        
        # Identify top performers
        all_projects = []
        for area, area_data in roi_analysis["by_area"].items():
            all_projects.append({
                "location": area,
                "roi": area_data["avg_roi"],
                "irr": area_data["irr"],
                "risk_adjusted_return": area_data["avg_roi"] / max(area_data.get("payback_period", 1), 1)
            })
        
        roi_analysis["top_performers"] = sorted(
            all_projects, 
            key=lambda x: x["risk_adjusted_return"], 
            reverse=True
        )[:5]
        
        return roi_analysis
    
    def _analyze_lending_environment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current lending trends and availability"""
        lending_data = data.get("aggregated_data", {}).get("lending_metrics", {})
        
        analysis = {
            "current_rates": {},
            "lending_availability": {},
            "trend_direction": "stable",
            "optimal_ltv_ratios": {},
            "preferred_lenders": []
        }
        
        # Current rate environment
        rates = lending_data.get("interest_rates", {})
        if rates:
            analysis["current_rates"] = {
                "construction_loans": rates.get("construction", 0),
                "permanent_financing": rates.get("permanent", 0),
                "bridge_loans": rates.get("bridge", 0),
                "hard_money": rates.get("hard_money", 0)
            }
            
            # Determine trend
            rate_history = lending_data.get("rate_history", [])
            if len(rate_history) >= 3:
                recent_avg = np.mean(rate_history[-3:])
                older_avg = np.mean(rate_history[-6:-3]) if len(rate_history) >= 6 else rate_history[0]
                
                if recent_avg > older_avg + 0.5:
                    analysis["trend_direction"] = "rising"
                elif recent_avg < older_avg - 0.5:
                    analysis["trend_direction"] = "falling"
        
        # Lending availability
        availability = lending_data.get("availability", {})
        for loan_type, metrics in availability.items():
            if isinstance(metrics, dict):
                analysis["lending_availability"][loan_type] = {
                    "approval_rate": metrics.get("approval_rate", 0),
                    "avg_ltv": metrics.get("avg_ltv", 0),
                    "avg_days_to_close": metrics.get("days_to_close", 0),
                    "availability_score": self._calculate_availability_score(metrics)
                }
        
        # Optimal LTV ratios by project type
        analysis["optimal_ltv_ratios"] = {
            "stabilized_multifamily": 75,
            "new_construction": 65,
            "value_add": 70,
            "land_acquisition": 50
        }
        
        # Preferred lenders
        lenders = lending_data.get("active_lenders", [])
        analysis["preferred_lenders"] = sorted(
            lenders, 
            key=lambda x: x.get("market_share", 0), 
            reverse=True
        )[:5]
        
        return analysis
    
    def _analyze_investment_flows(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze investment patterns and capital flows"""
        investment_data = data.get("aggregated_data", {}).get("investment_activity", {})
        
        flow_analysis = {
            "total_volume": 0,
            "by_investor_type": {},
            "geographic_distribution": {},
            "asset_class_preference": {},
            "foreign_investment": {},
            "trend_indicators": {}
        }
        
        # Total investment volume
        flow_analysis["total_volume"] = investment_data.get("total_volume_ytd", 0)
        
        # By investor type
        investor_breakdown = investment_data.get("by_investor_type", {})
        for investor_type, metrics in investor_breakdown.items():
            if isinstance(metrics, dict):
                flow_analysis["by_investor_type"][investor_type] = {
                    "volume": metrics.get("volume", 0),
                    "deal_count": metrics.get("deals", 0),
                    "avg_deal_size": metrics.get("volume", 0) / max(metrics.get("deals", 1), 1),
                    "yoy_growth": metrics.get("yoy_growth", 0)
                }
        
        # Geographic preferences
        geo_data = investment_data.get("by_area", {})
        total_geo_investment = sum(geo_data.values()) if geo_data else 1
        
        for area, volume in geo_data.items():
            flow_analysis["geographic_distribution"][area] = {
                "volume": volume,
                "percentage": round((volume / total_geo_investment) * 100, 1)
            }
        
        # Asset class preferences
        asset_prefs = investment_data.get("by_asset_class", {})
        flow_analysis["asset_class_preference"] = {
            asset: {"allocation": pct, "trend": "increasing" if pct > 20 else "stable"}
            for asset, pct in asset_prefs.items()
        }
        
        # Foreign investment analysis
        flow_analysis["foreign_investment"] = {
            "percentage": investment_data.get("foreign_percentage", 0),
            "top_countries": investment_data.get("top_foreign_sources", []),
            "trend": "increasing" if investment_data.get("foreign_percentage", 0) > 15 else "stable"
        }
        
        return flow_analysis
    
    def _evaluate_financing_options(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate and rank financing options"""
        lending = self._analyze_lending_environment(data)
        market_data = data.get("aggregated_data", {})
        
        options = []
        
        # Traditional bank financing
        if lending["current_rates"].get("permanent_financing", 0) < 6:
            options.append({
                "type": "Traditional Bank Loan",
                "pros": ["Low rates", "Long-term stability", "High LTV available"],
                "cons": ["Slower approval", "Strict requirements"],
                "best_for": "Stabilized properties with strong cash flow",
                "cost": lending["current_rates"]["permanent_financing"],
                "ltv_range": "65-80%",
                "recommendation_score": 85
            })
        
        # Construction loans
        if lending["lending_availability"].get("construction", {}).get("availability_score", 0) > 70:
            options.append({
                "type": "Construction Loan",
                "pros": ["Tailored for development", "Interest-only period", "Converts to permanent"],
                "cons": ["Higher rates", "Requires experience"],
                "best_for": "Ground-up development projects",
                "cost": lending["current_rates"]["construction_loans"],
                "ltv_range": "60-70%",
                "recommendation_score": 78
            })
        
        # Bridge financing
        options.append({
            "type": "Bridge Loan",
            "pros": ["Quick closing", "Flexible terms", "Less documentation"],
            "cons": ["Higher cost", "Short term"],
            "best_for": "Quick acquisitions and value-add projects",
            "cost": lending["current_rates"]["bridge_loans"],
            "ltv_range": "65-75%",
            "recommendation_score": 72
        })
        
        # Joint venture equity
        if market_data.get("equity_availability", "high") == "high":
            options.append({
                "type": "Joint Venture Equity",
                "pros": ["No debt service", "Shared risk", "Access to expertise"],
                "cons": ["Diluted returns", "Shared control"],
                "best_for": "Large-scale or high-risk projects",
                "cost": "20-30% equity participation",
                "ltv_range": "N/A",
                "recommendation_score": 75
            })
        
        # EB-5 financing
        options.append({
            "type": "EB-5 Investment",
            "pros": ["Low cost (3-5%)", "Long-term capital", "No personal guarantees"],
            "cons": ["Complex process", "Job creation requirements"],
            "best_for": "Large projects in targeted employment areas",
            "cost": "3-5%",
            "ltv_range": "20-40% of total cost",
            "recommendation_score": 68
        })
        
        # Sort by recommendation score
        options.sort(key=lambda x: x["recommendation_score"], reverse=True)
        
        return options
    
    def _assess_market_valuations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess current market valuations and pricing efficiency"""
        valuation_data = data.get("aggregated_data", {}).get("valuations", {})
        
        assessment = {
            "price_to_rent_ratios": {},
            "cap_rate_spreads": {},
            "valuation_indicators": {},
            "market_efficiency": "fair_value"
        }
        
        # Price to rent ratios
        for area, metrics in valuation_data.get("by_area", {}).items():
            if isinstance(metrics, dict):
                price = metrics.get("avg_price", 0)
                annual_rent = metrics.get("avg_rent", 0) * 12
                
                if annual_rent > 0:
                    p2r_ratio = price / annual_rent
                    assessment["price_to_rent_ratios"][area] = {
                        "ratio": round(p2r_ratio, 1),
                        "valuation": "overvalued" if p2r_ratio > 20 else "undervalued" if p2r_ratio < 15 else "fair"
                    }
        
        # Cap rate analysis
        cap_rates = valuation_data.get("cap_rates", {})
        treasury_yield = 4.5  # 10-year treasury
        
        for property_type, rate in cap_rates.items():
            spread = rate - treasury_yield
            assessment["cap_rate_spreads"][property_type] = {
                "cap_rate": rate,
                "spread": round(spread, 2),
                "attractiveness": "attractive" if spread > 3 else "neutral" if spread > 2 else "tight"
            }
        
        # Overall market valuation
        avg_p2r = np.mean(list(r["ratio"] for r in assessment["price_to_rent_ratios"].values())) if assessment["price_to_rent_ratios"] else 17
        
        if avg_p2r > 22:
            assessment["market_efficiency"] = "overvalued"
        elif avg_p2r < 14:
            assessment["market_efficiency"] = "undervalued"
        
        return assessment
    
    def _project_cash_flows(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Project cash flows for typical development scenarios"""
        market_metrics = data.get("aggregated_data", {})
        
        projections = {
            "multifamily_300_units": self._project_multifamily_cash_flow(market_metrics),
            "mixed_use_development": self._project_mixed_use_cash_flow(market_metrics),
            "office_to_residential": self._project_conversion_cash_flow(market_metrics)
        }
        
        return projections
    
    def _project_multifamily_cash_flow(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Project cash flow for typical multifamily development"""
        # Assumptions based on market data
        units = 300
        avg_rent = metrics.get("avg_rent", {}).get("multifamily", 1500)
        construction_cost_psf = metrics.get("construction_costs", {}).get("multifamily", 150)
        avg_unit_size = 850
        
        total_cost = units * avg_unit_size * construction_cost_psf
        
        # Revenue projections
        year1_occupancy = 0.65  # Lease-up year
        stabilized_occupancy = 0.94
        
        projections = {
            "total_development_cost": total_cost,
            "year_1": {
                "revenue": units * avg_rent * 12 * year1_occupancy,
                "noi": units * avg_rent * 12 * year1_occupancy * 0.65,  # 65% NOI margin
                "cash_flow": -total_cost * 0.3  # Equity investment
            },
            "year_2": {
                "revenue": units * avg_rent * 12 * stabilized_occupancy,
                "noi": units * avg_rent * 12 * stabilized_occupancy * 0.65
            },
            "stabilized_noi": units * avg_rent * 12 * stabilized_occupancy * 0.65,
            "projected_value": (units * avg_rent * 12 * stabilized_occupancy * 0.65) / 0.055,  # 5.5% cap
            "equity_multiple": 0  # Calculate below
        }
        
        # Calculate equity multiple
        equity_investment = total_cost * 0.3
        exit_proceeds = projections["projected_value"] - (total_cost * 0.7)  # Pay off debt
        projections["equity_multiple"] = round(exit_proceeds / equity_investment, 2)
        
        return projections
    
    def _project_mixed_use_cash_flow(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Project cash flow for mixed-use development"""
        # Simplified projection
        retail_sf = 20000
        office_sf = 30000
        residential_units = 150
        
        retail_rent_psf = metrics.get("avg_rent", {}).get("retail", 35)
        office_rent_psf = metrics.get("avg_rent", {}).get("office", 28)
        res_rent = metrics.get("avg_rent", {}).get("multifamily", 1500)
        
        annual_revenue = (
            retail_sf * retail_rent_psf +
            office_sf * office_rent_psf +
            residential_units * res_rent * 12
        )
        
        return {
            "stabilized_revenue": annual_revenue,
            "stabilized_noi": annual_revenue * 0.60,  # 60% NOI margin for mixed-use
            "projected_value": annual_revenue * 0.60 / 0.06,  # 6% cap rate
            "development_timeline": "24-30 months"
        }
    
    def _project_conversion_cash_flow(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Project cash flow for office to residential conversion"""
        # Conversion assumptions
        building_sf = 100000
        units = 120  # After conversion
        conversion_cost_psf = 125
        
        total_cost = building_sf * conversion_cost_psf
        
        return {
            "conversion_cost": total_cost,
            "projected_units": units,
            "stabilized_revenue": units * metrics.get("avg_rent", {}).get("multifamily", 1500) * 12,
            "projected_noi": units * metrics.get("avg_rent", {}).get("multifamily", 1500) * 12 * 0.65,
            "conversion_timeline": "18-24 months"
        }
    
    def _calculate_risk_adjusted_returns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk-adjusted returns for different strategies"""
        roi_data = self._analyze_roi_metrics(data)
        
        risk_adjusted = {
            "by_strategy": {},
            "optimal_portfolio": {},
            "risk_recommendations": []
        }
        
        # Calculate Sharpe ratios for different strategies
        strategies = {
            "core": {"return": 8, "volatility": 5},
            "value_add": {"return": 15, "volatility": 12},
            "opportunistic": {"return": 20, "volatility": 20},
            "development": {"return": 25, "volatility": 25}
        }
        
        risk_free_rate = 4.5
        
        for strategy, metrics in strategies.items():
            sharpe = (metrics["return"] - risk_free_rate) / metrics["volatility"]
            risk_adjusted["by_strategy"][strategy] = {
                "expected_return": metrics["return"],
                "volatility": metrics["volatility"],
                "sharpe_ratio": round(sharpe, 2),
                "risk_level": "low" if metrics["volatility"] < 10 else "medium" if metrics["volatility"] < 20 else "high"
            }
        
        # Optimal portfolio allocation
        risk_adjusted["optimal_portfolio"] = {
            "conservative": {"core": 70, "value_add": 20, "opportunistic": 10},
            "moderate": {"core": 40, "value_add": 40, "opportunistic": 20},
            "aggressive": {"core": 20, "value_add": 30, "opportunistic": 30, "development": 20}
        }
        
        return risk_adjusted
    
    def _categorize_risk(self, std_dev: float) -> str:
        """Categorize risk level based on standard deviation"""
        if std_dev < 5:
            return "low"
        elif std_dev < 15:
            return "medium"
        else:
            return "high"
    
    def _calculate_irr(self, metrics: Dict[str, Any]) -> float:
        """Calculate internal rate of return"""
        # Simplified IRR calculation
        initial_investment = metrics.get("initial_investment", 1000000)
        annual_cash_flow = metrics.get("annual_cash_flow", 150000)
        exit_value = metrics.get("exit_value", initial_investment * 1.5)
        hold_period = metrics.get("hold_period", 5)
        
        # Simple approximation
        total_return = (annual_cash_flow * hold_period + exit_value) / initial_investment
        annualized_return = (total_return ** (1/hold_period)) - 1
        
        return round(annualized_return * 100, 2)
    
    def _calculate_availability_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate lending availability score"""
        approval_rate = metrics.get("approval_rate", 0)
        days_to_close = metrics.get("days_to_close", 60)
        
        # Lower days to close is better
        speed_score = max(0, 100 - days_to_close)
        
        return round((approval_rate + speed_score) / 2, 1)
    
    def _extract_key_findings(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key findings from financial analysis"""
        findings = []
        
        # ROI findings
        roi = insights.get("roi_analysis", {})
        top_performers = roi.get("top_performers", [])
        if top_performers:
            best = top_performers[0]
            findings.append(f"{best['location']} offers highest risk-adjusted returns with {best['roi']:.1f}% ROI")
        
        # Lending environment
        lending = insights.get("lending_trends", {})
        if lending.get("trend_direction") == "falling":
            findings.append("Favorable lending environment with falling rates creates acquisition opportunities")
        
        # Investment flows
        flows = insights.get("investment_patterns", {})
        if flows.get("total_volume", 0) > 1000000000:
            findings.append(f"Strong investment activity with ${flows['total_volume']/1e9:.1f}B in capital flows")
        
        # Valuations
        valuations = insights.get("market_valuations", {})
        if valuations.get("market_efficiency") == "undervalued":
            findings.append("Market valuations suggest buying opportunity with favorable price-to-rent ratios")
        
        # Best financing option
        financing = insights.get("financing_options", [])
        if financing:
            best_option = financing[0]
            findings.append(f"{best_option['type']} recommended with {best_option['recommendation_score']} score")
        
        return findings[:5]
    
    def _identify_risks(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify financial risks"""
        risks = []
        
        # Interest rate risk
        lending = insights.get("lending_trends", {})
        if lending.get("trend_direction") == "rising":
            risks.append({
                "type": "interest_rate",
                "severity": "high",
                "description": "Rising interest rates increasing project costs",
                "impact": "2-3% reduction in project returns",
                "mitigation": "Lock in rates early or use fixed-rate financing"
            })
        
        # Valuation risk
        valuations = insights.get("market_valuations", {})
        if valuations.get("market_efficiency") == "overvalued":
            risks.append({
                "type": "valuation",
                "severity": "medium",
                "description": "Elevated valuations may compress future returns",
                "impact": "10-15% potential price correction",
                "mitigation": "Focus on value-add opportunities and cash flow"
            })
        
        # Liquidity risk
        flows = insights.get("investment_patterns", {})
        if flows.get("foreign_investment", {}).get("percentage", 0) > 25:
            risks.append({
                "type": "liquidity",
                "severity": "medium",
                "description": "High reliance on foreign capital creates volatility risk",
                "impact": "Potential capital flight in global downturn",
                "mitigation": "Diversify capital sources and maintain strong banking relationships"
            })
        
        return risks
    
    def _identify_opportunities(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify financial opportunities"""
        opportunities = []
        
        # Financing opportunities
        lending = insights.get("lending_trends", {})
        if any(rate < 5 for rate in lending.get("current_rates", {}).values()):
            opportunities.append({
                "type": "low_cost_financing",
                "potential": "high",
                "description": "Historic low rates enable attractive project economics",
                "action": "Refinance existing assets and leverage for new acquisitions"
            })
        
        # ROI opportunities
        roi = insights.get("roi_analysis", {})
        for performer in roi.get("top_performers", [])[:2]:
            opportunities.append({
                "type": "high_roi_market",
                "potential": "high",
                "description": f"{performer['location']} showing {performer['roi']:.1f}% returns",
                "action": f"Focus development in {performer['location']} for maximum returns"
            })
        
        # Cash flow opportunities
        projections = insights.get("cash_flow_projections", {})
        multifamily = projections.get("multifamily_300_units", {})
        if multifamily.get("equity_multiple", 0) > 2:
            opportunities.append({
                "type": "multifamily_development",
                "potential": "high",
                "description": f"Multifamily projects projecting {multifamily['equity_multiple']}x equity multiple",
                "action": "Accelerate multifamily pipeline to capture strong fundamentals"
            })
        
        return opportunities[:5]
    
    def _generate_recommendations(self, insights: Dict[str, Any], 
                                risks: List[Dict], 
                                opportunities: List[Dict]) -> List[str]:
        """Generate actionable financial recommendations"""
        recommendations = []
        
        # Based on financing environment
        financing = insights.get("financing_options", [])
        if financing:
            top_option = financing[0]
            recommendations.append(f"Utilize {top_option['type']} for optimal capital structure")
        
        # Based on ROI analysis
        roi = insights.get("roi_analysis", {})
        by_type = roi.get("by_project_type", {})
        if by_type:
            best_type = max(by_type.items(), key=lambda x: x[1].get("sharpe_ratio", 0))
            recommendations.append(f"Focus on {best_type[0]} projects with {best_type[1]['sharpe_ratio']} Sharpe ratio")
        
        # Based on market valuations
        valuations = insights.get("market_valuations", {})
        if valuations.get("market_efficiency") == "undervalued":
            recommendations.append("Accelerate acquisitions while valuations remain attractive")
        
        # Risk management
        if any(r["type"] == "interest_rate" for r in risks):
            recommendations.append("Hedge interest rate exposure with caps or swaps on floating rate debt")
        
        # Portfolio strategy
        risk_adjusted = insights.get("risk_adjusted_returns", {})
        recommendations.append("Adopt moderate portfolio allocation: 40% core, 40% value-add, 20% opportunistic")
        
        return recommendations[:5]
    
    def _extract_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract key financial metrics"""
        metrics = {}
        
        # ROI metrics
        roi = insights.get("roi_analysis", {})
        all_rois = []
        for area_data in roi.get("by_area", {}).values():
            all_rois.append(area_data.get("avg_roi", 0))
        
        if all_rois:
            metrics["avg_market_roi"] = np.mean(all_rois)
            metrics["max_market_roi"] = max(all_rois)
        
        # Lending metrics
        lending = insights.get("lending_trends", {})
        rates = lending.get("current_rates", {})
        if rates:
            metrics["avg_lending_rate"] = np.mean(list(rates.values()))
            metrics["construction_loan_rate"] = rates.get("construction_loans", 0)
        
        # Investment flow metrics
        flows = insights.get("investment_patterns", {})
        metrics["total_investment_volume"] = flows.get("total_volume", 0)
        metrics["foreign_investment_pct"] = flows.get("foreign_investment", {}).get("percentage", 0)
        
        # Valuation metrics
        valuations = insights.get("market_valuations", {})
        p2r_ratios = [v["ratio"] for v in valuations.get("price_to_rent_ratios", {}).values()]
        if p2r_ratios:
            metrics["avg_price_to_rent"] = np.mean(p2r_ratios)
        
        # Cash flow metrics
        projections = insights.get("cash_flow_projections", {})
        multifamily = projections.get("multifamily_300_units", {})
        metrics["multifamily_equity_multiple"] = multifamily.get("equity_multiple", 0)
        
        return metrics