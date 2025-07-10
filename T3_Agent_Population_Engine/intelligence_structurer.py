#!/usr/bin/env python3
"""
Intelligence Structuring System
Advanced structuring for neighborhood and financial intelligence
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from collections import defaultdict
import pandas as pd


class NeighborhoodIntelligenceStructurer:
    """Structure neighborhood intelligence with investment scores and rankings"""
    
    def __init__(self):
        self.scoring_weights = {
            "growth_rate": 0.25,
            "median_income": 0.20,
            "development_activity": 0.20,
            "infrastructure_quality": 0.15,
            "market_appreciation": 0.20
        }
        
    def structure_neighborhood_intelligence(self, raw_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Structure neighborhood data with comprehensive scoring"""
        
        structured = {
            "neighborhood_profiles": {},
            "investment_scores": {},
            "development_opportunities": [],
            "price_trajectories": {},
            "infrastructure_impacts": {},
            "comparative_analysis": {},
            "heat_maps": {}
        }
        
        # Process each neighborhood
        neighborhoods = self._extract_neighborhoods(raw_intelligence)
        
        for neighborhood in neighborhoods:
            profile = self._create_neighborhood_profile(neighborhood, raw_intelligence)
            structured['neighborhood_profiles'][neighborhood['name']] = profile
            
            # Calculate investment score
            investment_score = self._calculate_comprehensive_investment_score(profile)
            structured['investment_scores'][neighborhood['name']] = investment_score
            
            # Identify development opportunities
            opportunities = self._identify_development_opportunities(neighborhood, raw_intelligence)
            structured['development_opportunities'].extend(opportunities)
            
            # Model price trajectory
            trajectory = self._model_price_trajectory(neighborhood, raw_intelligence)
            structured['price_trajectories'][neighborhood['name']] = trajectory
            
            # Assess infrastructure impact
            impact = self._assess_infrastructure_impact(neighborhood, raw_intelligence)
            structured['infrastructure_impacts'][neighborhood['name']] = impact
            
        # Generate comparative analysis
        structured['comparative_analysis'] = self._generate_comparative_analysis(structured)
        
        # Create heat maps
        structured['heat_maps'] = self._create_investment_heat_maps(structured)
        
        return structured
        
    def _extract_neighborhoods(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract unique neighborhoods from intelligence data"""
        neighborhoods = []
        seen = set()
        
        for insight in data.get('insights', []):
            for area in insight.get('geographic_scope', []):
                if area not in seen and area != 'Houston':
                    neighborhoods.append({
                        "name": area,
                        "insights": [insight]
                    })
                    seen.add(area)
                elif area in seen:
                    # Add insight to existing neighborhood
                    for n in neighborhoods:
                        if n['name'] == area:
                            n['insights'].append(insight)
                            
        return neighborhoods
        
    def _create_neighborhood_profile(self, neighborhood: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive neighborhood profile"""
        
        profile = {
            "name": neighborhood['name'],
            "demographics": {},
            "market_metrics": {},
            "development_status": {},
            "infrastructure": {},
            "growth_indicators": {},
            "risk_factors": {}
        }
        
        # Aggregate data from insights
        for insight in neighborhood['insights']:
            content = insight.get('content', {})
            metrics = content.get('metrics', {})
            
            # Extract demographics
            if 'population' in metrics:
                profile['demographics']['population'] = metrics['population']
            if 'median_income' in metrics:
                profile['demographics']['median_income'] = metrics['median_income']
                
            # Extract market metrics
            if 'median_price' in metrics:
                profile['market_metrics']['median_price'] = metrics['median_price']
            if 'price_growth' in metrics:
                profile['market_metrics']['appreciation_rate'] = metrics['price_growth']
                
            # Development activity
            if 'development' in insight.get('tags', []):
                profile['development_status']['active_projects'] = metrics.get('project_count', 0)
                profile['development_status']['investment_volume'] = metrics.get('total_investment', 0)
                
        return profile
        
    def _calculate_comprehensive_investment_score(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed investment score with breakdown"""
        
        scores = {
            "overall_score": 0,
            "components": {},
            "grade": "",
            "investment_recommendation": "",
            "confidence_level": 0.8
        }
        
        # Calculate component scores
        components = {
            "growth_potential": self._score_growth_potential(profile),
            "market_stability": self._score_market_stability(profile),
            "development_activity": self._score_development_activity(profile),
            "demographics_strength": self._score_demographics(profile),
            "infrastructure_quality": self._score_infrastructure(profile)
        }
        
        scores['components'] = components
        
        # Calculate weighted overall score
        total_score = sum(components.values()) / len(components)
        scores['overall_score'] = round(total_score, 2)
        
        # Assign grade
        if total_score >= 85:
            scores['grade'] = 'A'
            scores['investment_recommendation'] = 'Highly Recommended'
        elif total_score >= 75:
            scores['grade'] = 'B'
            scores['investment_recommendation'] = 'Recommended'
        elif total_score >= 65:
            scores['grade'] = 'C'
            scores['investment_recommendation'] = 'Moderate Opportunity'
        else:
            scores['grade'] = 'D'
            scores['investment_recommendation'] = 'Higher Risk'
            
        return scores
        
    def _score_growth_potential(self, profile: Dict[str, Any]) -> float:
        """Score growth potential (0-100)"""
        score = 50  # Base score
        
        # Population growth
        pop_growth = profile.get('growth_indicators', {}).get('population_growth', 0)
        score += min(pop_growth * 5, 25)
        
        # Development activity
        projects = profile.get('development_status', {}).get('active_projects', 0)
        score += min(projects * 2, 20)
        
        # Market appreciation
        appreciation = profile.get('market_metrics', {}).get('appreciation_rate', 0)
        score += min(appreciation * 3, 25)
        
        return min(100, score)
        
    def _score_market_stability(self, profile: Dict[str, Any]) -> float:
        """Score market stability (0-100)"""
        # Implementation for market stability scoring
        return 75.0  # Placeholder
        
    def _score_development_activity(self, profile: Dict[str, Any]) -> float:
        """Score development activity (0-100)"""
        score = 40  # Base score
        
        # Active projects
        projects = profile.get('development_status', {}).get('active_projects', 0)
        score += min(projects * 5, 30)
        
        # Investment volume
        investment = profile.get('development_status', {}).get('investment_volume', 0)
        if investment > 100000000:  # $100M+
            score += 30
        elif investment > 50000000:  # $50M+
            score += 20
        elif investment > 10000000:  # $10M+
            score += 10
            
        return min(100, score)
        
    def _score_demographics(self, profile: Dict[str, Any]) -> float:
        """Score demographic strength (0-100)"""
        score = 50  # Base score
        
        # Median income
        income = profile.get('demographics', {}).get('median_income', 0)
        if income > 100000:
            score += 30
        elif income > 75000:
            score += 20
        elif income > 50000:
            score += 10
            
        # Population size
        population = profile.get('demographics', {}).get('population', 0)
        if population > 50000:
            score += 20
        elif population > 25000:
            score += 10
            
        return min(100, score)
        
    def _score_infrastructure(self, profile: Dict[str, Any]) -> float:
        """Score infrastructure quality (0-100)"""
        # Placeholder - would use actual infrastructure data
        return 70.0
        
    def _identify_development_opportunities(self, neighborhood: Dict[str, Any], data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify and rank development opportunities"""
        opportunities = []
        
        for insight in neighborhood['insights']:
            if 'development' in insight.get('tags', []) or 'opportunity' in insight.get('tags', []):
                opportunity = {
                    "location": neighborhood['name'],
                    "type": self._classify_opportunity_type(insight),
                    "description": insight.get('title', ''),
                    "investment_required": insight.get('content', {}).get('metrics', {}).get('investment', 0),
                    "projected_roi": insight.get('content', {}).get('metrics', {}).get('roi', 0),
                    "timeline": insight.get('content', {}).get('metrics', {}).get('timeline', 'TBD'),
                    "risk_level": self._assess_opportunity_risk(insight),
                    "score": self._score_opportunity(insight)
                }
                opportunities.append(opportunity)
                
        # Sort by score
        opportunities.sort(key=lambda x: x['score'], reverse=True)
        
        return opportunities
        
    def _classify_opportunity_type(self, insight: Dict[str, Any]) -> str:
        """Classify the type of development opportunity"""
        tags = insight.get('tags', [])
        content = json.dumps(insight.get('content', {})).lower()
        
        if 'mixed-use' in tags or 'mixed use' in content:
            return 'Mixed-Use Development'
        elif 'residential' in tags or 'housing' in content:
            return 'Residential Development'
        elif 'commercial' in tags or 'retail' in content:
            return 'Commercial Development'
        elif 'industrial' in tags:
            return 'Industrial Development'
        else:
            return 'General Development'
            
    def _assess_opportunity_risk(self, insight: Dict[str, Any]) -> str:
        """Assess risk level of opportunity"""
        confidence = insight.get('confidence_score', 0.5)
        
        if confidence > 0.8:
            return 'Low'
        elif confidence > 0.6:
            return 'Medium'
        else:
            return 'High'
            
    def _score_opportunity(self, insight: Dict[str, Any]) -> float:
        """Score development opportunity (0-100)"""
        score = 50  # Base score
        
        # ROI component
        roi = insight.get('content', {}).get('metrics', {}).get('roi', 0)
        score += min(roi, 30)
        
        # Confidence component
        confidence = insight.get('confidence_score', 0.5)
        score += confidence * 20
        
        return min(100, score)
        
    def _model_price_trajectory(self, neighborhood: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Model price trajectory for neighborhood"""
        
        trajectory = {
            "current_median": 0,
            "1_year_projection": 0,
            "3_year_projection": 0,
            "5_year_projection": 0,
            "growth_factors": [],
            "risk_factors": [],
            "confidence_interval": {}
        }
        
        # Extract current pricing
        for insight in neighborhood['insights']:
            metrics = insight.get('content', {}).get('metrics', {})
            if 'median_price' in metrics:
                trajectory['current_median'] = metrics['median_price']
                
            # Calculate projections based on growth rate
            growth_rate = metrics.get('price_growth', 3.5) / 100  # Default 3.5%
            
            if trajectory['current_median'] > 0:
                trajectory['1_year_projection'] = trajectory['current_median'] * (1 + growth_rate)
                trajectory['3_year_projection'] = trajectory['current_median'] * ((1 + growth_rate) ** 3)
                trajectory['5_year_projection'] = trajectory['current_median'] * ((1 + growth_rate) ** 5)
                
            # Identify growth and risk factors
            if 'key_findings' in insight.get('content', {}):
                for finding in insight['content']['key_findings']:
                    if any(word in finding.lower() for word in ['growth', 'increase', 'demand']):
                        trajectory['growth_factors'].append(finding)
                    elif any(word in finding.lower() for word in ['risk', 'concern', 'challenge']):
                        trajectory['risk_factors'].append(finding)
                        
        return trajectory
        
    def _assess_infrastructure_impact(self, neighborhood: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess infrastructure impact on development potential"""
        
        impact = {
            "transportation_score": 0,
            "utilities_score": 0,
            "education_score": 0,
            "healthcare_score": 0,
            "overall_impact": "",
            "improvement_projects": [],
            "constraints": []
        }
        
        # Analyze infrastructure mentions in insights
        for insight in neighborhood['insights']:
            content = json.dumps(insight.get('content', {})).lower()
            
            # Transportation
            if any(word in content for word in ['transit', 'highway', 'transportation']):
                impact['transportation_score'] = 75  # Placeholder
                
            # Education
            if any(word in content for word in ['school', 'education', 'university']):
                impact['education_score'] = 80  # Placeholder
                
        # Calculate overall impact
        avg_score = np.mean([s for s in [impact['transportation_score'], impact['utilities_score'], 
                             impact['education_score'], impact['healthcare_score']] if s > 0])
        
        if avg_score >= 80:
            impact['overall_impact'] = 'Highly Supportive'
        elif avg_score >= 60:
            impact['overall_impact'] = 'Supportive'
        else:
            impact['overall_impact'] = 'Needs Improvement'
            
        return impact
        
    def _generate_comparative_analysis(self, structured: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparative analysis across neighborhoods"""
        
        analysis = {
            "rankings": {},
            "best_for_categories": {},
            "investment_tiers": {},
            "opportunity_matrix": {}
        }
        
        # Rank by investment scores
        scores = structured['investment_scores']
        ranked = sorted(scores.items(), key=lambda x: x[1]['overall_score'], reverse=True)
        
        analysis['rankings'] = {
            "by_overall_score": [item[0] for item in ranked],
            "top_3": [item[0] for item in ranked[:3]],
            "emerging_markets": self._identify_emerging_markets(structured)
        }
        
        # Categorize best neighborhoods for different purposes
        analysis['best_for_categories'] = {
            "residential_development": self._find_best_for_category(structured, 'residential'),
            "commercial_development": self._find_best_for_category(structured, 'commercial'),
            "mixed_use_development": self._find_best_for_category(structured, 'mixed-use'),
            "long_term_appreciation": self._find_best_for_appreciation(structured)
        }
        
        return analysis
        
    def _identify_emerging_markets(self, structured: Dict[str, Any]) -> List[str]:
        """Identify emerging market neighborhoods"""
        emerging = []
        
        for neighborhood, trajectory in structured['price_trajectories'].items():
            # High growth projection with moderate current prices
            growth = (trajectory['3_year_projection'] - trajectory['current_median']) / trajectory['current_median'] if trajectory['current_median'] > 0 else 0
            
            if growth > 0.15 and trajectory['current_median'] < 400000:  # 15% growth, under $400k median
                emerging.append(neighborhood)
                
        return emerging
        
    def _find_best_for_category(self, structured: Dict[str, Any], category: str) -> List[str]:
        """Find best neighborhoods for specific development category"""
        suitable = []
        
        for opportunity in structured['development_opportunities']:
            if category.lower() in opportunity['type'].lower():
                if opportunity['location'] not in suitable:
                    suitable.append(opportunity['location'])
                    
        return suitable[:3]  # Top 3
        
    def _find_best_for_appreciation(self, structured: Dict[str, Any]) -> List[str]:
        """Find neighborhoods with best appreciation potential"""
        appreciation_scores = {}
        
        for neighborhood, trajectory in structured['price_trajectories'].items():
            if trajectory['current_median'] > 0:
                projected_growth = (trajectory['5_year_projection'] - trajectory['current_median']) / trajectory['current_median']
                appreciation_scores[neighborhood] = projected_growth
                
        # Sort and return top 3
        sorted_neighborhoods = sorted(appreciation_scores.items(), key=lambda x: x[1], reverse=True)
        return [n[0] for n in sorted_neighborhoods[:3]]
        
    def _create_investment_heat_maps(self, structured: Dict[str, Any]) -> Dict[str, Any]:
        """Create investment heat map data"""
        
        heat_maps = {
            "investment_score_map": {},
            "opportunity_density_map": {},
            "price_growth_map": {},
            "risk_map": {}
        }
        
        # Investment score heat map
        for neighborhood, scores in structured['investment_scores'].items():
            heat_maps['investment_score_map'][neighborhood] = {
                "value": scores['overall_score'],
                "color_intensity": scores['overall_score'] / 100,
                "label": f"{neighborhood}: {scores['grade']}"
            }
            
        # Opportunity density
        opportunity_counts = defaultdict(int)
        for opp in structured['development_opportunities']:
            opportunity_counts[opp['location']] += 1
            
        max_opportunities = max(opportunity_counts.values()) if opportunity_counts else 1
        for neighborhood, count in opportunity_counts.items():
            heat_maps['opportunity_density_map'][neighborhood] = {
                "value": count,
                "color_intensity": count / max_opportunities,
                "label": f"{neighborhood}: {count} opportunities"
            }
            
        return heat_maps


class FinancialIntelligenceStructurer:
    """Structure financial intelligence with ROI models and risk matrices"""
    
    def __init__(self):
        self.risk_factors = {
            "market_volatility": 0.2,
            "regulatory_changes": 0.15,
            "economic_conditions": 0.25,
            "competition": 0.15,
            "execution_risk": 0.25
        }
        
    def structure_financial_intelligence(self, raw_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Structure financial data with comprehensive analysis"""
        
        structured = {
            "roi_calculation_models": {},
            "financing_option_comparisons": [],
            "tax_optimization_strategies": [],
            "investment_risk_matrices": {},
            "financial_scenarios": {},
            "funding_landscape": {}
        }
        
        # Process financial insights
        financial_insights = [i for i in raw_intelligence.get('insights', []) 
                            if 'financial' in i.get('domain', '') or 
                            any(tag in i.get('tags', []) for tag in ['investment', 'financing', 'roi'])]
        
        for insight in financial_insights:
            # Build ROI models
            if 'roi' in insight.get('tags', []):
                roi_model = self._build_roi_model(insight)
                structured['roi_calculation_models'][insight.get('title', 'Unnamed')] = roi_model
                
            # Extract financing options
            if 'financing' in insight.get('tags', []):
                financing_options = self._extract_financing_options(insight)
                structured['financing_option_comparisons'].extend(financing_options)
                
            # Identify tax strategies
            if 'tax' in insight.get('tags', []):
                tax_strategies = self._identify_tax_strategies(insight)
                structured['tax_optimization_strategies'].extend(tax_strategies)
                
        # Build risk matrices
        structured['investment_risk_matrices'] = self._build_risk_matrices(financial_insights)
        
        # Create financial scenarios
        structured['financial_scenarios'] = self._create_financial_scenarios(structured)
        
        # Map funding landscape
        structured['funding_landscape'] = self._map_funding_landscape(financial_insights)
        
        return structured
        
    def _build_roi_model(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive ROI calculation model"""
        
        metrics = insight.get('content', {}).get('metrics', {})
        
        model = {
            "model_type": "comprehensive_roi",
            "inputs": {
                "initial_investment": metrics.get('initial_investment', 0),
                "projected_revenue": metrics.get('projected_revenue', 0),
                "operating_expenses": metrics.get('operating_expenses', 0),
                "financing_costs": metrics.get('financing_costs', 0)
            },
            "calculations": {},
            "sensitivity_analysis": {},
            "break_even_analysis": {},
            "risk_adjusted_returns": {}
        }
        
        # Basic ROI calculation
        if model['inputs']['initial_investment'] > 0:
            net_return = (model['inputs']['projected_revenue'] - 
                         model['inputs']['operating_expenses'] - 
                         model['inputs']['financing_costs'])
            
            model['calculations']['basic_roi'] = (net_return / model['inputs']['initial_investment']) * 100
            model['calculations']['net_present_value'] = self._calculate_npv(model['inputs'])
            model['calculations']['internal_rate_return'] = self._calculate_irr(model['inputs'])
            
        # Sensitivity analysis
        model['sensitivity_analysis'] = self._perform_sensitivity_analysis(model['inputs'])
        
        # Break-even analysis
        model['break_even_analysis'] = self._calculate_break_even(model['inputs'])
        
        # Risk-adjusted returns
        model['risk_adjusted_returns'] = self._calculate_risk_adjusted_returns(model)
        
        return model
        
    def _calculate_npv(self, inputs: Dict[str, Any], discount_rate: float = 0.08) -> float:
        """Calculate Net Present Value"""
        # Simplified NPV calculation
        cash_flows = []
        initial = -inputs['initial_investment']
        annual_cash_flow = inputs['projected_revenue'] - inputs['operating_expenses'] - inputs['financing_costs']
        
        # Assume 5-year project
        for year in range(1, 6):
            discounted_flow = annual_cash_flow / ((1 + discount_rate) ** year)
            cash_flows.append(discounted_flow)
            
        npv = initial + sum(cash_flows)
        return round(npv, 2)
        
    def _calculate_irr(self, inputs: Dict[str, Any]) -> float:
        """Calculate Internal Rate of Return"""
        # Simplified IRR estimation
        roi = (inputs['projected_revenue'] - inputs['operating_expenses'] - 
               inputs['financing_costs']) / inputs['initial_investment']
        
        # Approximate IRR based on simple ROI
        irr = roi / 5  # Assuming 5-year project
        return round(irr * 100, 2)
        
    def _perform_sensitivity_analysis(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Perform sensitivity analysis on key variables"""
        
        base_case = self._calculate_npv(inputs)
        sensitivity = {}
        
        # Test revenue sensitivity
        revenue_scenarios = [-0.2, -0.1, 0, 0.1, 0.2]  # -20% to +20%
        revenue_impacts = []
        
        for scenario in revenue_scenarios:
            adjusted_inputs = inputs.copy()
            adjusted_inputs['projected_revenue'] *= (1 + scenario)
            npv = self._calculate_npv(adjusted_inputs)
            revenue_impacts.append({
                "scenario": f"{scenario*100:+.0f}%",
                "npv": npv,
                "impact": npv - base_case
            })
            
        sensitivity['revenue_sensitivity'] = revenue_impacts
        
        # Similar analysis for costs
        sensitivity['cost_sensitivity'] = self._analyze_cost_sensitivity(inputs, base_case)
        
        return sensitivity
        
    def _analyze_cost_sensitivity(self, inputs: Dict[str, Any], base_case: float) -> List[Dict[str, Any]]:
        """Analyze cost sensitivity"""
        cost_scenarios = [-0.2, -0.1, 0, 0.1, 0.2]
        cost_impacts = []
        
        for scenario in cost_scenarios:
            adjusted_inputs = inputs.copy()
            adjusted_inputs['operating_expenses'] *= (1 + scenario)
            npv = self._calculate_npv(adjusted_inputs)
            cost_impacts.append({
                "scenario": f"{scenario*100:+.0f}%",
                "npv": npv,
                "impact": npv - base_case
            })
            
        return cost_impacts
        
    def _calculate_break_even(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate break-even analysis"""
        
        annual_cash_flow = (inputs['projected_revenue'] - 
                           inputs['operating_expenses'] - 
                           inputs['financing_costs'])
        
        break_even = {
            "break_even_period": 0,
            "cumulative_cash_flows": [],
            "break_even_revenue": 0
        }
        
        if annual_cash_flow > 0:
            break_even['break_even_period'] = inputs['initial_investment'] / annual_cash_flow
            
            # Calculate cumulative cash flows
            cumulative = -inputs['initial_investment']
            for year in range(1, 11):
                cumulative += annual_cash_flow
                break_even['cumulative_cash_flows'].append({
                    "year": year,
                    "cumulative": cumulative,
                    "positive": cumulative > 0
                })
                
        # Break-even revenue calculation
        if inputs['projected_revenue'] > 0:
            margin = 1 - (inputs['operating_expenses'] + inputs['financing_costs']) / inputs['projected_revenue']
            if margin > 0:
                break_even['break_even_revenue'] = inputs['initial_investment'] / margin
                
        return break_even
        
    def _calculate_risk_adjusted_returns(self, model: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk-adjusted returns"""
        
        base_roi = model['calculations'].get('basic_roi', 0)
        
        risk_adjusted = {
            "risk_free_rate": 3.5,  # Treasury rate
            "risk_premium": 0,
            "sharpe_ratio": 0,
            "risk_adjusted_roi": 0,
            "confidence_intervals": {}
        }
        
        # Calculate risk premium
        total_risk = sum(self.risk_factors.values())
        risk_adjusted['risk_premium'] = base_roi * total_risk * 0.5  # 50% of risk translates to premium
        
        # Risk-adjusted ROI
        risk_adjusted['risk_adjusted_roi'] = base_roi - risk_adjusted['risk_premium']
        
        # Sharpe ratio (simplified)
        if risk_adjusted['risk_premium'] > 0:
            risk_adjusted['sharpe_ratio'] = (base_roi - risk_adjusted['risk_free_rate']) / risk_adjusted['risk_premium']
            
        # Confidence intervals
        risk_adjusted['confidence_intervals'] = {
            "90%": {
                "lower": risk_adjusted['risk_adjusted_roi'] * 0.8,
                "upper": risk_adjusted['risk_adjusted_roi'] * 1.2
            },
            "95%": {
                "lower": risk_adjusted['risk_adjusted_roi'] * 0.7,
                "upper": risk_adjusted['risk_adjusted_roi'] * 1.3
            }
        }
        
        return risk_adjusted
        
    def _extract_financing_options(self, insight: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and compare financing options"""
        
        options = []
        content = insight.get('content', {})
        
        # Parse financing information
        if 'financing_sources' in content:
            for source in content['financing_sources']:
                option = {
                    "source_name": source.get('name', 'Unknown'),
                    "type": source.get('type', 'Traditional'),
                    "interest_rate": source.get('rate', 0),
                    "terms": source.get('terms', {}),
                    "requirements": source.get('requirements', []),
                    "pros": source.get('advantages', []),
                    "cons": source.get('disadvantages', []),
                    "total_cost": self._calculate_financing_cost(source),
                    "suitability_score": self._score_financing_suitability(source)
                }
                options.append(option)
                
        return options
        
    def _calculate_financing_cost(self, source: Dict[str, Any]) -> float:
        """Calculate total cost of financing"""
        rate = source.get('rate', 0) / 100
        term = source.get('terms', {}).get('years', 30)
        amount = source.get('terms', {}).get('max_amount', 1000000)
        
        # Simple interest calculation
        total_interest = amount * rate * term
        fees = source.get('fees', 0)
        
        return amount + total_interest + fees
        
    def _score_financing_suitability(self, source: Dict[str, Any]) -> float:
        """Score financing option suitability"""
        score = 50  # Base score
        
        # Lower rates are better
        rate = source.get('rate', 10)
        if rate < 5:
            score += 30
        elif rate < 7:
            score += 20
        elif rate < 10:
            score += 10
            
        # Flexible terms are better
        if 'flexible' in str(source.get('terms', {})).lower():
            score += 10
            
        # Fewer requirements are better
        requirements = len(source.get('requirements', []))
        if requirements < 3:
            score += 10
        elif requirements > 5:
            score -= 10
            
        return min(100, max(0, score))
        
    def _identify_tax_strategies(self, insight: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify tax optimization strategies"""
        
        strategies = []
        content = insight.get('content', {})
        
        # Common real estate tax strategies
        if 'tax' in json.dumps(content).lower():
            strategies.extend([
                {
                    "strategy": "1031 Exchange",
                    "description": "Defer capital gains through like-kind property exchange",
                    "potential_savings": "Up to 20% of capital gains",
                    "requirements": ["Identify replacement property within 45 days", "Complete exchange within 180 days"],
                    "risk_level": "Low"
                },
                {
                    "strategy": "Opportunity Zone Investment",
                    "description": "Invest in designated opportunity zones for tax benefits",
                    "potential_savings": "Defer and reduce capital gains tax",
                    "requirements": ["Invest in qualified opportunity fund", "Hold for minimum periods"],
                    "risk_level": "Medium"
                },
                {
                    "strategy": "Cost Segregation",
                    "description": "Accelerate depreciation on property components",
                    "potential_savings": "Increase cash flow by 5-10%",
                    "requirements": ["Professional cost segregation study", "Detailed property analysis"],
                    "risk_level": "Low"
                }
            ])
            
        return strategies
        
    def _build_risk_matrices(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build comprehensive risk assessment matrices"""
        
        risk_matrix = {
            "risk_categories": {},
            "risk_heat_map": {},
            "mitigation_strategies": {},
            "overall_risk_score": 0
        }
        
        # Define risk categories
        categories = [
            "market_risk",
            "financial_risk",
            "regulatory_risk",
            "environmental_risk",
            "execution_risk"
        ]
        
        for category in categories:
            risk_matrix['risk_categories'][category] = {
                "probability": self._assess_risk_probability(category, insights),
                "impact": self._assess_risk_impact(category, insights),
                "score": 0,
                "level": ""
            }
            
            # Calculate risk score (probability * impact)
            prob = risk_matrix['risk_categories'][category]['probability']
            impact = risk_matrix['risk_categories'][category]['impact']
            score = prob * impact
            
            risk_matrix['risk_categories'][category]['score'] = score
            
            # Assign risk level
            if score >= 7:
                risk_matrix['risk_categories'][category]['level'] = "High"
            elif score >= 4:
                risk_matrix['risk_categories'][category]['level'] = "Medium"
            else:
                risk_matrix['risk_categories'][category]['level'] = "Low"
                
            # Add to heat map
            risk_matrix['risk_heat_map'][category] = {
                "x": prob,
                "y": impact,
                "size": score,
                "color": "red" if score >= 7 else "yellow" if score >= 4 else "green"
            }
            
        # Calculate overall risk score
        total_score = sum(cat['score'] for cat in risk_matrix['risk_categories'].values())
        risk_matrix['overall_risk_score'] = total_score / len(categories)
        
        # Generate mitigation strategies
        risk_matrix['mitigation_strategies'] = self._generate_mitigation_strategies(risk_matrix)
        
        return risk_matrix
        
    def _assess_risk_probability(self, category: str, insights: List[Dict[str, Any]]) -> float:
        """Assess probability of risk occurring (1-10)"""
        # Simplified probability assessment
        base_probabilities = {
            "market_risk": 6,
            "financial_risk": 5,
            "regulatory_risk": 4,
            "environmental_risk": 3,
            "execution_risk": 5
        }
        
        return base_probabilities.get(category, 5)
        
    def _assess_risk_impact(self, category: str, insights: List[Dict[str, Any]]) -> float:
        """Assess impact of risk if it occurs (1-10)"""
        # Simplified impact assessment
        base_impacts = {
            "market_risk": 7,
            "financial_risk": 8,
            "regulatory_risk": 6,
            "environmental_risk": 7,
            "execution_risk": 6
        }
        
        return base_impacts.get(category, 5)
        
    def _generate_mitigation_strategies(self, risk_matrix: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate risk mitigation strategies"""
        
        strategies = {}
        
        for category, risk_data in risk_matrix['risk_categories'].items():
            if risk_data['level'] == "High":
                strategies[category] = self._get_high_risk_mitigation(category)
            elif risk_data['level'] == "Medium":
                strategies[category] = self._get_medium_risk_mitigation(category)
            else:
                strategies[category] = ["Monitor and maintain current controls"]
                
        return strategies
        
    def _get_high_risk_mitigation(self, category: str) -> List[str]:
        """Get mitigation strategies for high-risk categories"""
        
        mitigation_map = {
            "market_risk": [
                "Diversify development portfolio across submarkets",
                "Implement phased development approach",
                "Secure pre-leasing commitments",
                "Consider market hedging strategies"
            ],
            "financial_risk": [
                "Secure fixed-rate financing",
                "Maintain higher contingency reserves (15-20%)",
                "Implement strict cost controls",
                "Consider joint venture partnerships"
            ],
            "regulatory_risk": [
                "Engage regulatory consultants early",
                "Build relationships with planning officials",
                "Submit preliminary plans for feedback",
                "Monitor regulatory changes actively"
            ],
            "environmental_risk": [
                "Conduct comprehensive environmental assessments",
                "Purchase environmental insurance",
                "Implement robust mitigation measures",
                "Engage environmental consultants"
            ],
            "execution_risk": [
                "Select experienced contractors with strong track records",
                "Implement detailed project management systems",
                "Build in schedule buffers",
                "Maintain strong vendor relationships"
            ]
        }
        
        return mitigation_map.get(category, ["Implement comprehensive risk management plan"])
        
    def _get_medium_risk_mitigation(self, category: str) -> List[str]:
        """Get mitigation strategies for medium-risk categories"""
        
        mitigation_map = {
            "market_risk": [
                "Monitor market indicators closely",
                "Maintain flexibility in development plans",
                "Build relationships with potential tenants"
            ],
            "financial_risk": [
                "Maintain 10-15% contingency reserves",
                "Regular financial monitoring and reporting",
                "Consider multiple financing sources"
            ],
            "regulatory_risk": [
                "Stay informed on regulatory changes",
                "Maintain compliance documentation",
                "Build buffer time for approvals"
            ],
            "environmental_risk": [
                "Conduct standard environmental assessments",
                "Follow best practices for environmental protection",
                "Maintain environmental compliance"
            ],
            "execution_risk": [
                "Use proven contractors and vendors",
                "Implement regular progress monitoring",
                "Maintain clear communication channels"
            ]
        }
        
        return mitigation_map.get(category, ["Implement standard risk controls"])
        
    def _create_financial_scenarios(self, structured: Dict[str, Any]) -> Dict[str, Any]:
        """Create multiple financial scenarios"""
        
        scenarios = {
            "base_case": {},
            "optimistic": {},
            "pessimistic": {},
            "stress_test": {}
        }
        
        # Use first ROI model as basis
        if structured['roi_calculation_models']:
            base_model = list(structured['roi_calculation_models'].values())[0]
            
            # Base case
            scenarios['base_case'] = {
                "assumptions": "Current market conditions",
                "roi": base_model['calculations'].get('basic_roi', 0),
                "npv": base_model['calculations'].get('net_present_value', 0),
                "break_even": base_model['break_even_analysis'].get('break_even_period', 0)
            }
            
            # Optimistic scenario (20% better)
            scenarios['optimistic'] = {
                "assumptions": "Strong market growth, low interest rates",
                "roi": scenarios['base_case']['roi'] * 1.2,
                "npv": scenarios['base_case']['npv'] * 1.3,
                "break_even": scenarios['base_case']['break_even'] * 0.8
            }
            
            # Pessimistic scenario (20% worse)
            scenarios['pessimistic'] = {
                "assumptions": "Market slowdown, rising costs",
                "roi": scenarios['base_case']['roi'] * 0.8,
                "npv": scenarios['base_case']['npv'] * 0.7,
                "break_even": scenarios['base_case']['break_even'] * 1.3
            }
            
            # Stress test (40% worse)
            scenarios['stress_test'] = {
                "assumptions": "Severe market downturn, financing constraints",
                "roi": scenarios['base_case']['roi'] * 0.6,
                "npv": scenarios['base_case']['npv'] * 0.5,
                "break_even": scenarios['base_case']['break_even'] * 1.7
            }
            
        return scenarios
        
    def _map_funding_landscape(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map the funding landscape"""
        
        landscape = {
            "traditional_lending": {
                "availability": "High",
                "typical_rates": "4-7%",
                "typical_ltv": "65-80%",
                "best_for": "Stabilized properties, experienced developers"
            },
            "private_equity": {
                "availability": "Medium",
                "typical_returns": "15-25% IRR",
                "typical_equity": "80-90%",
                "best_for": "Value-add opportunities, large projects"
            },
            "crowdfunding": {
                "availability": "Medium",
                "typical_rates": "8-12%",
                "typical_raise": "$1-10M",
                "best_for": "Smaller projects, community-focused developments"
            },
            "opportunity_zone_funds": {
                "availability": "High in designated zones",
                "tax_benefits": "Capital gains deferral and reduction",
                "requirements": "Must be in opportunity zone",
                "best_for": "Long-term holds in designated areas"
            },
            "reit_partnerships": {
                "availability": "Low-Medium",
                "typical_structure": "Joint venture or acquisition",
                "benefits": "Access to capital markets",
                "best_for": "Institutional-quality projects"
            }
        }
        
        return landscape


if __name__ == "__main__":
    print("Intelligence Structuring System initialized")
    print("Ready to process neighborhood and financial intelligence from T2")
