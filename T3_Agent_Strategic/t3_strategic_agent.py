#!/usr/bin/env python3
"""
T3 Strategic Agent - Strategic Structuring Layer
Transforms T2 analyses into actionable intelligence for decision-making
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
from collections import defaultdict
import statistics


@dataclass
class StrategicInsight:
    """Represents a strategic insight derived from T2 analyses"""
    type: str  # opportunity, risk, recommendation
    title: str
    description: str
    impact_level: str  # high, medium, low
    confidence: float
    supporting_data: List[Dict[str, Any]]
    action_items: List[str]
    timeline: str  # immediate, short-term, long-term
    user_segments: List[str]  # investors, developers, homeowners


@dataclass
class MarketNarrative:
    """Market narrative structure"""
    summary: str
    key_trends: List[str]
    market_drivers: List[str]
    outlook: str
    confidence: float


@dataclass
class UserSegmentView:
    """User-specific view of intelligence"""
    segment: str
    priority_insights: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    risk_factors: List[Dict[str, Any]]
    action_plan: Dict[str, Any]


class T3StrategicAgent:
    """
    T3 Strategic Agent - Structures analyzed data into actionable intelligence
    """
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.t2_path = self.base_path / "T2_Analysis_Results"
        self.t3_path = self.base_path / "T3_Strategic_Intelligence"
        self.t3_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.opportunities_path = self.t3_path / "opportunities"
        self.risks_path = self.t3_path / "risks"
        self.narratives_path = self.t3_path / "narratives"
        self.user_views_path = self.t3_path / "user_views"
        
        for path in [self.opportunities_path, self.risks_path, 
                     self.narratives_path, self.user_views_path]:
            path.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Load configuration
        self.load_configuration()
        
        # Initialize synthesis engine
        self.synthesis_engine = IntelligenceSynthesizer()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_path = self.t3_path / "t3_strategic.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('T3-Strategic')
        
    def load_configuration(self):
        """Load strategic configuration"""
        self.config = {
            'confidence_threshold': 0.75,
            'impact_weights': {
                'financial': 0.35,
                'market': 0.25,
                'risk': 0.20,
                'growth': 0.20
            },
            'user_segments': {
                'investors': {
                    'focus': ['roi', 'appreciation', 'cash_flow', 'market_timing'],
                    'risk_tolerance': 'moderate'
                },
                'developers': {
                    'focus': ['zoning', 'permits', 'construction_costs', 'demand'],
                    'risk_tolerance': 'high'
                },
                'homeowners': {
                    'focus': ['value', 'neighborhood', 'schools', 'safety'],
                    'risk_tolerance': 'low'
                }
            },
            'timeline_definitions': {
                'immediate': '0-3 months',
                'short-term': '3-12 months',
                'long-term': '1-5 years'
            }
        }
        
    def process_t2_analyses(self, analysis_ids: List[str] = None) -> Dict[str, Any]:
        """
        Process T2 analyses and structure into strategic intelligence
        """
        try:
            # Load T2 analyses
            if analysis_ids:
                analyses = self._load_specific_analyses(analysis_ids)
            else:
                analyses = self._load_recent_analyses()
                
            if not analyses:
                self.logger.warning("No T2 analyses found to process")
                return None
                
            # Generate structure ID
            structure_id = f"t3-{datetime.now().strftime('%Y-%m-%d')}-{uuid.uuid4().hex[:5]}"
            
            self.logger.info(f"Processing {len(analyses)} T2 analyses into structure {structure_id}")
            
            # Synthesize insights
            strategic_insights = self._synthesize_strategic_insights(analyses)
            
            # Create market narrative
            market_narrative = self._create_market_narrative(analyses, strategic_insights)
            
            # Generate user segment views
            user_segments = self._generate_user_segments(strategic_insights, analyses)
            
            # Calculate overall confidence
            confidence_score = self._calculate_confidence(analyses, strategic_insights)
            
            # Build final structure
            strategic_structure = {
                'structure_id': structure_id,
                'source_analyses': [a['analysis_id'] for a in analyses],
                'strategic_insights': {
                    'opportunities': [self._format_insight(i) for i in strategic_insights['opportunities']],
                    'risks': [self._format_insight(i) for i in strategic_insights['risks']],
                    'recommendations': [self._format_insight(i) for i in strategic_insights['recommendations']]
                },
                'market_narrative': asdict(market_narrative),
                'user_segments': user_segments,
                'confidence_score': confidence_score,
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'total_insights': sum(len(v) for v in strategic_insights.values()),
                    'primary_markets': self._extract_primary_markets(analyses),
                    'key_metrics': self._extract_key_metrics(analyses)
                }
            }
            
            # Save strategic structure
            self._save_strategic_structure(strategic_structure)
            
            # Generate specialized outputs
            self._generate_opportunity_profiles(strategic_insights['opportunities'], structure_id)
            self._generate_risk_assessments(strategic_insights['risks'], structure_id)
            self._save_user_views(user_segments, structure_id)
            
            self.logger.info(f"Strategic structuring complete: {structure_id}")
            
            return strategic_structure
            
        except Exception as e:
            self.logger.error(f"Error in strategic structuring: {e}")
            raise
            
    def _load_specific_analyses(self, analysis_ids: List[str]) -> List[Dict[str, Any]]:
        """Load specific T2 analyses by ID"""
        analyses = []
        for analysis_id in analysis_ids:
            for file in self.t2_path.glob(f"*{analysis_id}*.json"):
                try:
                    with open(file, 'r') as f:
                        analyses.append(json.load(f))
                except Exception as e:
                    self.logger.error(f"Error loading analysis {file}: {e}")
        return analyses
        
    def _load_recent_analyses(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Load recent T2 analyses"""
        analyses = []
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        for file in self.t2_path.glob("*.json"):
            if file.stat().st_mtime > cutoff_time:
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        if data.get('confidence_score', 0) >= self.config['confidence_threshold']:
                            analyses.append(data)
                except Exception as e:
                    self.logger.error(f"Error loading analysis {file}: {e}")
                    
        return sorted(analyses, key=lambda x: x.get('timestamp', ''), reverse=True)
        
    def _synthesize_strategic_insights(self, analyses: List[Dict[str, Any]]) -> Dict[str, List[StrategicInsight]]:
        """Synthesize strategic insights from T2 analyses"""
        insights = {
            'opportunities': [],
            'risks': [],
            'recommendations': []
        }
        
        # Extract patterns across analyses
        patterns = self._extract_patterns(analyses)
        
        # Generate opportunities
        for pattern in patterns['positive_trends']:
            if pattern['strength'] > 0.7:
                opportunity = self._create_opportunity(pattern, analyses)
                insights['opportunities'].append(opportunity)
                
        # Identify risks
        for pattern in patterns['negative_trends']:
            if pattern['severity'] > 0.6:
                risk = self._create_risk(pattern, analyses)
                insights['risks'].append(risk)
                
        # Create recommendations
        recommendations = self._generate_recommendations(
            insights['opportunities'],
            insights['risks'],
            analyses
        )
        insights['recommendations'] = recommendations
        
        return insights
        
    def _extract_patterns(self, analyses: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract patterns from analyses"""
        patterns = {
            'positive_trends': [],
            'negative_trends': [],
            'market_signals': []
        }
        
        # Aggregate metrics across analyses
        metric_aggregates = defaultdict(list)
        
        for analysis in analyses:
            if 'metrics' in analysis:
                for metric, value in analysis['metrics'].items():
                    if isinstance(value, (int, float)):
                        metric_aggregates[metric].append(value)
                        
        # Identify trends
        for metric, values in metric_aggregates.items():
            if len(values) >= 3:
                trend = self._calculate_trend(values)
                
                if trend['direction'] == 'increasing' and trend['strength'] > 0.5:
                    patterns['positive_trends'].append({
                        'metric': metric,
                        'trend': trend,
                        'strength': trend['strength'],
                        'data_points': len(values)
                    })
                elif trend['direction'] == 'decreasing' and trend['strength'] > 0.5:
                    patterns['negative_trends'].append({
                        'metric': metric,
                        'trend': trend,
                        'severity': trend['strength'],
                        'data_points': len(values)
                    })
                    
        # Extract market signals
        for analysis in analyses:
            if 'market_signals' in analysis:
                patterns['market_signals'].extend(analysis['market_signals'])
                
        return patterns
        
    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend from values"""
        if len(values) < 2:
            return {'direction': 'stable', 'strength': 0}
            
        # Simple linear regression
        n = len(values)
        x = list(range(n))
        
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return {'direction': 'stable', 'strength': 0}
            
        slope = numerator / denominator
        
        # Determine direction and strength
        if slope > 0.1:
            direction = 'increasing'
        elif slope < -0.1:
            direction = 'decreasing'
        else:
            direction = 'stable'
            
        # Calculate R-squared for strength
        y_pred = [slope * xi + (y_mean - slope * x_mean) for xi in x]
        ss_res = sum((values[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((values[i] - y_mean) ** 2 for i in range(n))
        
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        return {
            'direction': direction,
            'strength': abs(r_squared),
            'slope': slope
        }
        
    def _create_opportunity(self, pattern: Dict[str, Any], analyses: List[Dict[str, Any]]) -> StrategicInsight:
        """Create opportunity from pattern"""
        # Map metrics to opportunity types
        opportunity_map = {
            'appreciation_rate': 'Property Value Growth Opportunity',
            'rental_yield': 'Cash Flow Investment Opportunity',
            'development_activity': 'Development Opportunity',
            'demand_score': 'High Demand Market Opportunity',
            'innovation_index': 'Emerging Tech Hub Opportunity'
        }
        
        title = opportunity_map.get(pattern['metric'], f"{pattern['metric'].replace('_', ' ').title()} Opportunity")
        
        # Generate description based on trend
        trend_desc = f"{pattern['trend']['strength']*100:.1f}% confidence"
        description = f"Strong {pattern['trend']['direction']} trend detected with {trend_desc}. "
        description += f"Based on {pattern['data_points']} data points showing consistent growth pattern."
        
        # Determine impact and timeline
        impact_level = 'high' if pattern['strength'] > 0.8 else 'medium'
        timeline = 'immediate' if pattern['trend']['slope'] > 0.5 else 'short-term'
        
        # Extract supporting data
        supporting_data = []
        for analysis in analyses[-3:]:  # Last 3 analyses
            if pattern['metric'] in analysis.get('metrics', {}):
                supporting_data.append({
                    'source': analysis['analysis_id'],
                    'value': analysis['metrics'][pattern['metric']],
                    'timestamp': analysis['timestamp']
                })
                
        # Generate action items
        action_items = self._generate_opportunity_actions(pattern['metric'], pattern['trend'])
        
        # Determine relevant user segments
        user_segments = self._determine_user_segments(pattern['metric'])
        
        return StrategicInsight(
            type='opportunity',
            title=title,
            description=description,
            impact_level=impact_level,
            confidence=pattern['strength'],
            supporting_data=supporting_data,
            action_items=action_items,
            timeline=timeline,
            user_segments=user_segments
        )
        
    def _create_risk(self, pattern: Dict[str, Any], analyses: List[Dict[str, Any]]) -> StrategicInsight:
        """Create risk assessment from pattern"""
        # Map metrics to risk types
        risk_map = {
            'vacancy_rate': 'Rising Vacancy Risk',
            'price_volatility': 'Market Volatility Risk',
            'construction_costs': 'Cost Escalation Risk',
            'inventory_months': 'Oversupply Risk',
            'default_rate': 'Credit Risk'
        }
        
        title = risk_map.get(pattern['metric'], f"{pattern['metric'].replace('_', ' ').title()} Risk")
        
        # Generate description
        severity_desc = f"{pattern['severity']*100:.1f}% severity"
        description = f"Concerning {pattern['trend']['direction']} trend with {severity_desc}. "
        description += f"Analysis of {pattern['data_points']} data points indicates potential risk exposure."
        
        # Determine impact and timeline
        impact_level = 'high' if pattern['severity'] > 0.8 else 'medium'
        timeline = 'immediate' if abs(pattern['trend']['slope']) > 0.5 else 'short-term'
        
        # Extract supporting data
        supporting_data = []
        for analysis in analyses[-3:]:
            if pattern['metric'] in analysis.get('metrics', {}):
                supporting_data.append({
                    'source': analysis['analysis_id'],
                    'value': analysis['metrics'][pattern['metric']],
                    'timestamp': analysis['timestamp']
                })
                
        # Generate mitigation actions
        action_items = self._generate_risk_mitigations(pattern['metric'], pattern['severity'])
        
        # Determine affected user segments
        user_segments = ['investors', 'developers', 'homeowners']  # Risks affect all
        
        return StrategicInsight(
            type='risk',
            title=title,
            description=description,
            impact_level=impact_level,
            confidence=pattern['severity'],
            supporting_data=supporting_data,
            action_items=action_items,
            timeline=timeline,
            user_segments=user_segments
        )
        
    def _generate_recommendations(self, opportunities: List[StrategicInsight], 
                                risks: List[StrategicInsight], 
                                analyses: List[Dict[str, Any]]) -> List[StrategicInsight]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Balance opportunities and risks
        for opp in opportunities:
            # Find related risks
            related_risks = [r for r in risks if self._are_related(opp, r)]
            
            if not related_risks or opp.confidence > max(r.confidence for r in related_risks):
                # Opportunity outweighs risks
                rec = self._create_positive_recommendation(opp, related_risks)
                recommendations.append(rec)
                
        # Address unmitigated risks
        for risk in risks:
            if risk.impact_level == 'high' and risk.confidence > 0.8:
                rec = self._create_defensive_recommendation(risk)
                recommendations.append(rec)
                
        # Add market-timing recommendations
        market_rec = self._create_market_timing_recommendation(analyses)
        if market_rec:
            recommendations.append(market_rec)
            
        return recommendations
        
    def _create_market_narrative(self, analyses: List[Dict[str, Any]], 
                               insights: Dict[str, List[StrategicInsight]]) -> MarketNarrative:
        """Create comprehensive market narrative"""
        # Extract key themes
        themes = self._extract_market_themes(analyses)
        
        # Build summary
        opp_count = len(insights['opportunities'])
        risk_count = len(insights['risks'])
        
        if opp_count > risk_count * 1.5:
            market_tone = "bullish"
            summary = f"The Houston real estate market shows strong positive momentum with {opp_count} identified opportunities. "
        elif risk_count > opp_count * 1.5:
            market_tone = "cautious"
            summary = f"Market conditions suggest caution with {risk_count} risk factors requiring attention. "
        else:
            market_tone = "balanced"
            summary = "The Houston market presents a balanced outlook with both opportunities and risks. "
            
        summary += f"Key themes include {', '.join(themes['primary'][:3])}."
        
        # Identify key trends
        key_trends = []
        for insight in insights['opportunities'][:3]:
            key_trends.append(f"{insight.title}: {insight.description.split('.')[0]}")
            
        # Market drivers
        market_drivers = self._identify_market_drivers(analyses)
        
        # Generate outlook
        outlook = self._generate_market_outlook(market_tone, insights, analyses)
        
        # Calculate narrative confidence
        all_insights = insights['opportunities'] + insights['risks'] + insights['recommendations']
        avg_confidence = statistics.mean([i.confidence for i in all_insights]) if all_insights else 0.5
        
        return MarketNarrative(
            summary=summary,
            key_trends=key_trends,
            market_drivers=market_drivers,
            outlook=outlook,
            confidence=avg_confidence
        )
        
    def _generate_user_segments(self, insights: Dict[str, List[StrategicInsight]], 
                              analyses: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Generate user-specific views"""
        user_segments = {}
        
        for segment, config in self.config['user_segments'].items():
            # Filter relevant insights
            relevant_insights = []
            for insight_list in insights.values():
                relevant_insights.extend([i for i in insight_list if segment in i.user_segments])
                
            # Prioritize by focus areas
            priority_insights = self._prioritize_for_segment(relevant_insights, config['focus'])
            
            # Generate segment-specific recommendations
            segment_recommendations = self._generate_segment_recommendations(
                segment, priority_insights, config
            )
            
            # Identify relevant risks
            risk_factors = [i for i in insights['risks'] 
                          if self._is_relevant_risk(i, segment, config['risk_tolerance'])]
            
            # Create action plan
            action_plan = self._create_segment_action_plan(
                segment, priority_insights[:3], risk_factors[:2]
            )
            
            user_segments[segment] = {
                'priority_insights': [self._format_insight(i) for i in priority_insights[:5]],
                'recommendations': segment_recommendations,
                'risk_factors': [self._format_insight(r) for r in risk_factors[:3]],
                'action_plan': action_plan,
                'market_readiness': self._assess_market_readiness(segment, insights, analyses)
            }
            
        return user_segments
        
    def _format_insight(self, insight: StrategicInsight) -> Dict[str, Any]:
        """Format insight for output"""
        return {
            'type': insight.type,
            'title': insight.title,
            'description': insight.description,
            'impact_level': insight.impact_level,
            'confidence': round(insight.confidence, 3),
            'action_items': insight.action_items,
            'timeline': insight.timeline,
            'supporting_data': insight.supporting_data
        }
        
    def _save_strategic_structure(self, structure: Dict[str, Any]):
        """Save strategic structure"""
        filename = f"{structure['structure_id']}.json"
        filepath = self.t3_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(structure, f, indent=2)
            
        self.logger.info(f"Saved strategic structure: {filename}")
        
    def _generate_opportunity_actions(self, metric: str, trend: Dict[str, Any]) -> List[str]:
        """Generate action items for opportunity"""
        actions = {
            'appreciation_rate': [
                "Research comparable properties in high-appreciation areas",
                "Analyze factors driving appreciation (employment, infrastructure)",
                "Consider timing entry before peak acceleration"
            ],
            'rental_yield': [
                "Calculate cash-on-cash returns for target properties",
                "Verify rental demand through vacancy rate analysis",
                "Evaluate property management options"
            ],
            'development_activity': [
                "Identify parcels near development zones",
                "Research zoning changes and permit activity",
                "Connect with local development firms"
            ]
        }
        
        return actions.get(metric, [
            f"Monitor {metric} trends closely",
            "Conduct detailed market analysis",
            "Consult with local experts"
        ])
        
    def _generate_risk_mitigations(self, metric: str, severity: float) -> List[str]:
        """Generate mitigation actions for risks"""
        mitigations = {
            'vacancy_rate': [
                "Diversify property portfolio across submarkets",
                "Focus on properties with stable tenant demand",
                "Consider value-add improvements to attract tenants"
            ],
            'price_volatility': [
                "Implement dollar-cost averaging for acquisitions",
                "Maintain adequate cash reserves",
                "Consider hedging strategies"
            ],
            'construction_costs': [
                "Lock in material prices with suppliers",
                "Consider modular or prefab alternatives",
                "Phase development projects strategically"
            ]
        }
        
        base_actions = mitigations.get(metric, [
            f"Monitor {metric} indicators weekly",
            "Develop contingency plans",
            "Reduce exposure to affected areas"
        ])
        
        if severity > 0.8:
            base_actions.insert(0, "IMMEDIATE ACTION REQUIRED")
            
        return base_actions
        
    def _determine_user_segments(self, metric: str) -> List[str]:
        """Determine relevant user segments for metric"""
        segment_map = {
            'appreciation_rate': ['investors', 'homeowners'],
            'rental_yield': ['investors'],
            'development_activity': ['developers', 'investors'],
            'school_ratings': ['homeowners'],
            'zoning_changes': ['developers'],
            'construction_costs': ['developers']
        }
        
        return segment_map.get(metric, ['investors', 'developers', 'homeowners'])
        
    def _are_related(self, opp: StrategicInsight, risk: StrategicInsight) -> bool:
        """Check if opportunity and risk are related"""
        # Simple keyword matching for now
        opp_keywords = set(opp.title.lower().split() + opp.description.lower().split())
        risk_keywords = set(risk.title.lower().split() + risk.description.lower().split())
        
        common_keywords = opp_keywords.intersection(risk_keywords)
        return len(common_keywords) > 3
        
    def _create_positive_recommendation(self, opportunity: StrategicInsight, 
                                      risks: List[StrategicInsight]) -> StrategicInsight:
        """Create recommendation based on opportunity"""
        title = f"Capitalize on {opportunity.title}"
        
        description = f"Strong opportunity identified with {opportunity.confidence:.1%} confidence. "
        if risks:
            description += f"While {len(risks)} risk factors exist, the opportunity outweighs concerns. "
        description += "Recommended action within the " + opportunity.timeline + " timeframe."
        
        # Combine actions from opportunity and risk mitigation
        action_items = opportunity.action_items.copy()
        for risk in risks[:1]:  # Add top risk mitigation
            action_items.append(f"Mitigate: {risk.action_items[0]}")
            
        return StrategicInsight(
            type='recommendation',
            title=title,
            description=description,
            impact_level=opportunity.impact_level,
            confidence=opportunity.confidence * 0.9,  # Slight reduction for risks
            supporting_data=opportunity.supporting_data,
            action_items=action_items,
            timeline=opportunity.timeline,
            user_segments=opportunity.user_segments
        )
        
    def _create_defensive_recommendation(self, risk: StrategicInsight) -> StrategicInsight:
        """Create defensive recommendation for high risk"""
        title = f"Defensive Strategy for {risk.title}"
        
        description = f"High-confidence risk identified requiring defensive action. "
        description += f"{risk.description} Immediate protective measures recommended."
        
        action_items = ["PRIORITY: " + risk.action_items[0]] + risk.action_items[1:]
        
        return StrategicInsight(
            type='recommendation',
            title=title,
            description=description,
            impact_level='high',
            confidence=risk.confidence,
            supporting_data=risk.supporting_data,
            action_items=action_items,
            timeline='immediate',
            user_segments=risk.user_segments
        )
        
    def _create_market_timing_recommendation(self, analyses: List[Dict[str, Any]]) -> Optional[StrategicInsight]:
        """Create market timing recommendation"""
        # Extract timing indicators
        timing_signals = []
        
        for analysis in analyses:
            if 'market_cycle_phase' in analysis:
                timing_signals.append(analysis['market_cycle_phase'])
                
        if not timing_signals:
            return None
            
        # Determine consensus
        phase_counts = defaultdict(int)
        for signal in timing_signals:
            phase_counts[signal] += 1
            
        dominant_phase = max(phase_counts.items(), key=lambda x: x[1])[0]
        confidence = phase_counts[dominant_phase] / len(timing_signals)
        
        if confidence < 0.6:
            return None
            
        # Generate recommendation based on phase
        timing_recs = {
            'expansion': {
                'title': 'Market Expansion Phase - Accelerate Acquisition',
                'description': 'Market indicators suggest expansion phase. Favorable conditions for property acquisition.',
                'actions': ['Increase acquisition pace', 'Leverage favorable financing', 'Focus on growth markets']
            },
            'peak': {
                'title': 'Market Peak Phase - Selective Strategy Required',
                'description': 'Market approaching peak conditions. Shift to selective, high-quality acquisitions.',
                'actions': ['Focus on cash flow over appreciation', 'Reduce leverage', 'Consider profit-taking']
            },
            'contraction': {
                'title': 'Market Contraction Phase - Defensive Positioning',
                'description': 'Market showing contraction signs. Defensive strategies recommended.',
                'actions': ['Build cash reserves', 'Focus on stable assets', 'Prepare for opportunities']
            }
        }
        
        rec_data = timing_recs.get(dominant_phase, timing_recs['expansion'])
        
        return StrategicInsight(
            type='recommendation',
            title=rec_data['title'],
            description=rec_data['description'],
            impact_level='high',
            confidence=confidence,
            supporting_data=[{'phase': dominant_phase, 'confidence': confidence}],
            action_items=rec_data['actions'],
            timeline='immediate',
            user_segments=['investors', 'developers']
        )
        
    def _extract_market_themes(self, analyses: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Extract market themes from analyses"""
        themes = defaultdict(int)
        
        # Count theme occurrences
        for analysis in analyses:
            if 'key_findings' in analysis:
                for finding in analysis['key_findings']:
                    # Extract keywords (simplified)
                    words = finding.lower().split()
                    for word in words:
                        if len(word) > 5:  # Significant words only
                            themes[word] += 1
                            
        # Sort by frequency
        sorted_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'primary': [theme[0] for theme in sorted_themes[:5]],
            'secondary': [theme[0] for theme in sorted_themes[5:10]]
        }
        
    def _identify_market_drivers(self, analyses: List[Dict[str, Any]]) -> List[str]:
        """Identify key market drivers"""
        drivers = set()
        
        driver_keywords = {
            'employment': 'Job growth and employment expansion',
            'population': 'Population growth and demographic shifts',
            'infrastructure': 'Infrastructure development and improvements',
            'technology': 'Technology sector growth and innovation',
            'energy': 'Energy sector dynamics',
            'interest': 'Interest rate environment',
            'inventory': 'Housing inventory levels',
            'demand': 'Buyer and renter demand patterns'
        }
        
        for analysis in analyses:
            text = json.dumps(analysis).lower()
            for keyword, driver in driver_keywords.items():
                if keyword in text:
                    drivers.add(driver)
                    
        return list(drivers)[:5]
        
    def _generate_market_outlook(self, tone: str, insights: Dict[str, List[StrategicInsight]], 
                               analyses: List[Dict[str, Any]]) -> str:
        """Generate market outlook statement"""
        outlooks = {
            'bullish': "The Houston real estate market is positioned for continued growth with multiple "
                      "expansion catalysts. Investors should consider accelerating acquisition timelines "
                      "while maintaining discipline on underwriting standards.",
            'cautious': "Market conditions warrant a cautious approach with selective opportunities. "
                       "Focus on defensive positioning while preparing to capitalize on market dislocations.",
            'balanced': "The market presents a balanced risk-reward profile. Successful strategies will "
                       "require careful market selection and thorough due diligence on individual opportunities."
        }
        
        base_outlook = outlooks[tone]
        
        # Add specific insight
        if insights['opportunities']:
            top_opp = insights['opportunities'][0]
            base_outlook += f" {top_opp.title} represents a particularly compelling near-term opportunity."
            
        return base_outlook
        
    def _calculate_confidence(self, analyses: List[Dict[str, Any]], 
                            insights: Dict[str, List[StrategicInsight]]) -> float:
        """Calculate overall structure confidence"""
        confidences = []
        
        # Analysis confidences
        for analysis in analyses:
            if 'confidence_score' in analysis:
                confidences.append(analysis['confidence_score'])
                
        # Insight confidences
        for insight_list in insights.values():
            confidences.extend([i.confidence for i in insight_list])
            
        return statistics.mean(confidences) if confidences else 0.5
        
    def _extract_primary_markets(self, analyses: List[Dict[str, Any]]) -> List[str]:
        """Extract primary markets from analyses"""
        markets = defaultdict(int)
        
        for analysis in analyses:
            if 'location' in analysis:
                markets[analysis['location']] += 1
            if 'markets' in analysis:
                for market in analysis['markets']:
                    markets[market] += 1
                    
        sorted_markets = sorted(markets.items(), key=lambda x: x[1], reverse=True)
        return [market[0] for market in sorted_markets[:5]]
        
    def _extract_key_metrics(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract key metrics summary"""
        metrics_summary = {}
        metrics_values = defaultdict(list)
        
        for analysis in analyses:
            if 'metrics' in analysis:
                for metric, value in analysis['metrics'].items():
                    if isinstance(value, (int, float)):
                        metrics_values[metric].append(value)
                        
        for metric, values in metrics_values.items():
            if values:
                metrics_summary[metric] = {
                    'current': values[-1],  # Most recent
                    'average': statistics.mean(values),
                    'trend': 'increasing' if values[-1] > values[0] else 'decreasing'
                }
                
        return metrics_summary
        
    def _prioritize_for_segment(self, insights: List[StrategicInsight], 
                               focus_areas: List[str]) -> List[StrategicInsight]:
        """Prioritize insights for user segment"""
        scored_insights = []
        
        for insight in insights:
            score = insight.confidence
            
            # Boost score for focus area matches
            insight_text = (insight.title + " " + insight.description).lower()
            for focus in focus_areas:
                if focus.lower() in insight_text:
                    score *= 1.2
                    
            # Factor in impact level
            if insight.impact_level == 'high':
                score *= 1.3
            elif insight.impact_level == 'medium':
                score *= 1.1
                
            scored_insights.append((score, insight))
            
        # Sort by score
        scored_insights.sort(key=lambda x: x[0], reverse=True)
        
        return [insight for score, insight in scored_insights]
        
    def _generate_segment_recommendations(self, segment: str, insights: List[StrategicInsight], 
                                        config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate segment-specific recommendations"""
        recommendations = []
        
        segment_templates = {
            'investors': {
                'roi_focus': "Target properties with {metric}% returns in {location}",
                'timing': "Optimal entry window: {timeline}",
                'strategy': "Recommended strategy: {approach}"
            },
            'developers': {
                'opportunity': "Development opportunity in {location} with {metric}",
                'permits': "Expedited permitting available for {property_type}",
                'demand': "Strong demand indicators for {product_type}"
            },
            'homeowners': {
                'value': "Your property value trend: {direction} {percentage}%",
                'neighborhood': "{location} showing {trend} in key metrics",
                'action': "Consider {action} to maximize value"
            }
        }
        
        templates = segment_templates.get(segment, {})
        
        # Generate recommendations from insights
        for insight in insights[:3]:
            if insight.type == 'opportunity':
                rec_template = templates.get('opportunity', templates.get('roi_focus', ''))
                if rec_template and insight.supporting_data:
                    rec = {
                        'title': f"{segment.title()} Opportunity: {insight.title}",
                        'description': insight.description,
                        'action': insight.action_items[0] if insight.action_items else "Review opportunity details",
                        'priority': 'high' if insight.impact_level == 'high' else 'medium',
                        'timeline': insight.timeline
                    }
                    recommendations.append(rec)
                    
        return recommendations
        
    def _is_relevant_risk(self, risk: StrategicInsight, segment: str, risk_tolerance: str) -> bool:
        """Check if risk is relevant to segment"""
        # All high impact risks are relevant
        if risk.impact_level == 'high':
            return True
            
        # Filter by risk tolerance
        if risk_tolerance == 'low' and risk.confidence > 0.6:
            return True
        elif risk_tolerance == 'moderate' and risk.confidence > 0.7:
            return True
        elif risk_tolerance == 'high' and risk.confidence > 0.8:
            return True
            
        return False
        
    def _create_segment_action_plan(self, segment: str, opportunities: List[StrategicInsight], 
                                   risks: List[StrategicInsight]) -> Dict[str, Any]:
        """Create actionable plan for segment"""
        plan = {
            'immediate_actions': [],
            'short_term_goals': [],
            'risk_mitigation': [],
            'success_metrics': []
        }
        
        # Immediate actions from top opportunities
        for opp in opportunities:
            if opp.timeline == 'immediate' and opp.action_items:
                plan['immediate_actions'].extend(opp.action_items[:2])
                
        # Short-term goals
        for opp in opportunities:
            if opp.timeline == 'short-term':
                plan['short_term_goals'].append({
                    'goal': opp.title,
                    'timeline': self.config['timeline_definitions']['short-term'],
                    'confidence': f"{opp.confidence:.0%}"
                })
                
        # Risk mitigation
        for risk in risks:
            if risk.action_items:
                plan['risk_mitigation'].append({
                    'risk': risk.title,
                    'action': risk.action_items[0],
                    'priority': risk.impact_level
                })
                
        # Success metrics by segment
        segment_metrics = {
            'investors': ['ROI achieved', 'Portfolio value growth', 'Cash flow targets'],
            'developers': ['Projects completed', 'Permit approval rate', 'Cost vs budget'],
            'homeowners': ['Property value appreciation', 'Neighborhood improvement', 'Quality of life']
        }
        
        plan['success_metrics'] = segment_metrics.get(segment, ['Performance vs market'])
        
        return plan
        
    def _assess_market_readiness(self, segment: str, insights: Dict[str, List[StrategicInsight]], 
                               analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess market readiness for segment"""
        readiness_score = 0.5  # Base score
        factors = []
        
        # Positive factors
        opp_count = len([i for i in insights['opportunities'] if segment in i.user_segments])
        if opp_count > 3:
            readiness_score += 0.2
            factors.append(f"{opp_count} relevant opportunities identified")
            
        # Negative factors
        risk_count = len([i for i in insights['risks'] if segment in i.user_segments and i.impact_level == 'high'])
        if risk_count > 2:
            readiness_score -= 0.2
            factors.append(f"{risk_count} high-impact risks present")
            
        # Market phase bonus/penalty
        for analysis in analyses:
            if 'market_cycle_phase' in analysis:
                if analysis['market_cycle_phase'] == 'expansion':
                    readiness_score += 0.1
                    factors.append("Market in expansion phase")
                elif analysis['market_cycle_phase'] == 'contraction':
                    readiness_score -= 0.1
                    factors.append("Market in contraction phase")
                break
                
        # Segment-specific adjustments
        if segment == 'investors' and any('cash_flow' in str(i) for i in insights['opportunities']):
            readiness_score += 0.1
            factors.append("Strong cash flow opportunities")
            
        readiness_score = max(0.1, min(0.9, readiness_score))  # Bound between 0.1 and 0.9
        
        return {
            'score': round(readiness_score, 2),
            'assessment': 'High' if readiness_score > 0.7 else 'Moderate' if readiness_score > 0.4 else 'Low',
            'factors': factors
        }
        
    def _generate_opportunity_profiles(self, opportunities: List[StrategicInsight], structure_id: str):
        """Generate detailed opportunity profiles"""
        for i, opp in enumerate(opportunities[:5]):  # Top 5 opportunities
            profile = {
                'profile_id': f"{structure_id}-opp-{i+1}",
                'opportunity': self._format_insight(opp),
                'investment_thesis': self._generate_investment_thesis(opp),
                'market_analysis': self._generate_opportunity_analysis(opp),
                'execution_plan': self._generate_execution_plan(opp),
                'risk_assessment': self._assess_opportunity_risks(opp),
                'generated_at': datetime.now().isoformat()
            }
            
            filename = f"opportunity_profile_{structure_id}_{i+1}.json"
            filepath = self.opportunities_path / filename
            
            with open(filepath, 'w') as f:
                json.dump(profile, f, indent=2)
                
    def _generate_risk_assessments(self, risks: List[StrategicInsight], structure_id: str):
        """Generate detailed risk assessments"""
        if not risks:
            return
            
        assessment = {
            'assessment_id': f"{structure_id}-risk",
            'risk_summary': {
                'total_risks': len(risks),
                'high_impact': len([r for r in risks if r.impact_level == 'high']),
                'immediate_action': len([r for r in risks if r.timeline == 'immediate'])
            },
            'risk_matrix': self._create_risk_matrix(risks),
            'mitigation_strategies': self._compile_mitigation_strategies(risks),
            'monitoring_plan': self._create_risk_monitoring_plan(risks),
            'generated_at': datetime.now().isoformat()
        }
        
        filename = f"risk_assessment_{structure_id}.json"
        filepath = self.risks_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(assessment, f, indent=2)
            
    def _save_user_views(self, user_segments: Dict[str, Dict[str, Any]], structure_id: str):
        """Save user-specific views"""
        for segment, data in user_segments.items():
            view = {
                'view_id': f"{structure_id}-{segment}",
                'segment': segment,
                'data': data,
                'generated_at': datetime.now().isoformat()
            }
            
            filename = f"user_view_{structure_id}_{segment}.json"
            filepath = self.user_views_path / filename
            
            with open(filepath, 'w') as f:
                json.dump(view, f, indent=2)
                
    def _generate_investment_thesis(self, opportunity: StrategicInsight) -> str:
        """Generate investment thesis for opportunity"""
        thesis = f"Investment Thesis: {opportunity.title}\n\n"
        thesis += f"Core Opportunity: {opportunity.description}\n\n"
        thesis += f"Expected Timeline: {opportunity.timeline.replace('_', ' ').title()}\n"
        thesis += f"Confidence Level: {opportunity.confidence:.0%}\n\n"
        thesis += "Key Value Drivers:\n"
        
        for i, action in enumerate(opportunity.action_items[:3], 1):
            thesis += f"{i}. {action}\n"
            
        return thesis
        
    def _generate_opportunity_analysis(self, opportunity: StrategicInsight) -> Dict[str, Any]:
        """Generate detailed opportunity analysis"""
        return {
            'market_dynamics': "Favorable market conditions support this opportunity",
            'competitive_landscape': "Limited competition in target segment",
            'timing_analysis': f"Optimal entry window: {opportunity.timeline}",
            'resource_requirements': "Standard capital requirements for market entry"
        }
        
    def _generate_execution_plan(self, opportunity: StrategicInsight) -> Dict[str, Any]:
        """Generate execution plan for opportunity"""
        phases = []
        
        if opportunity.timeline == 'immediate':
            phases.append({
                'phase': 'Phase 1: Immediate Actions (0-30 days)',
                'actions': opportunity.action_items[:2]
            })
            phases.append({
                'phase': 'Phase 2: Implementation (30-90 days)',
                'actions': opportunity.action_items[2:4] if len(opportunity.action_items) > 2 else ['Execute strategy']
            })
        else:
            phases.append({
                'phase': 'Phase 1: Preparation (0-60 days)',
                'actions': opportunity.action_items[:2]
            })
            phases.append({
                'phase': 'Phase 2: Execution (60-180 days)',
                'actions': opportunity.action_items[2:] if len(opportunity.action_items) > 2 else ['Implement plan']
            })
            
        return {
            'phases': phases,
            'success_criteria': ['ROI targets met', 'Timeline adherence', 'Risk mitigation effective'],
            'monitoring': 'Weekly progress reviews recommended'
        }
        
    def _assess_opportunity_risks(self, opportunity: StrategicInsight) -> List[Dict[str, str]]:
        """Assess risks specific to opportunity"""
        # Generic risk assessment for opportunities
        common_risks = [
            {'risk': 'Market conditions change', 'mitigation': 'Monitor indicators weekly'},
            {'risk': 'Competition increases', 'mitigation': 'Act within specified timeline'},
            {'risk': 'Execution challenges', 'mitigation': 'Maintain flexibility in approach'}
        ]
        
        if opportunity.impact_level == 'high':
            common_risks.append({'risk': 'High stakes require precision', 'mitigation': 'Engage expert advisors'})
            
        return common_risks
        
    def _create_risk_matrix(self, risks: List[StrategicInsight]) -> List[Dict[str, Any]]:
        """Create risk matrix"""
        matrix = []
        
        for risk in risks:
            likelihood = 'High' if risk.confidence > 0.8 else 'Medium' if risk.confidence > 0.6 else 'Low'
            impact = risk.impact_level.capitalize()
            
            matrix.append({
                'risk': risk.title,
                'likelihood': likelihood,
                'impact': impact,
                'risk_score': risk.confidence * (0.9 if risk.impact_level == 'high' else 0.6),
                'timeline': risk.timeline
            })
            
        return sorted(matrix, key=lambda x: x['risk_score'], reverse=True)
        
    def _compile_mitigation_strategies(self, risks: List[StrategicInsight]) -> List[Dict[str, Any]]:
        """Compile mitigation strategies"""
        strategies = []
        
        # Group by impact level
        high_impact = [r for r in risks if r.impact_level == 'high']
        medium_impact = [r for r in risks if r.impact_level == 'medium']
        
        if high_impact:
            strategies.append({
                'priority': 'Critical',
                'risks_addressed': [r.title for r in high_impact],
                'strategies': list(set(action for r in high_impact for action in r.action_items[:2]))
            })
            
        if medium_impact:
            strategies.append({
                'priority': 'Important',
                'risks_addressed': [r.title for r in medium_impact],
                'strategies': list(set(action for r in medium_impact for action in r.action_items[:1]))
            })
            
        return strategies
        
    def _create_risk_monitoring_plan(self, risks: List[StrategicInsight]) -> Dict[str, Any]:
        """Create risk monitoring plan"""
        return {
            'monitoring_frequency': 'Weekly' if any(r.timeline == 'immediate' for r in risks) else 'Bi-weekly',
            'key_indicators': list(set(data['source'] for r in risks for data in r.supporting_data)),
            'escalation_triggers': [
                'Any risk confidence increases by >10%',
                'New high-impact risks identified',
                'Mitigation strategies prove ineffective'
            ],
            'review_schedule': 'Monthly comprehensive review'
        }


class IntelligenceSynthesizer:
    """Synthesizes intelligence from multiple sources"""
    
    def __init__(self):
        self.synthesis_rules = {
            'correlation_threshold': 0.7,
            'pattern_confidence': 0.8,
            'minimum_sources': 2
        }
        
    def synthesize(self, data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize intelligence from data points"""
        # Implementation would include sophisticated synthesis logic
        # For now, returning a simplified version
        return {
            'synthesis_complete': True,
            'data_points_processed': len(data_points),
            'patterns_identified': []
        }


def main():
    """Demo T3 Strategic Agent"""
    import sys
    
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
        
    # Initialize T3 agent
    t3_agent = T3StrategicAgent(base_path)
    
    print("\n" + "="*60)
    print("T3 STRATEGIC AGENT - Strategic Structuring Layer")
    print("="*60)
    
    # Process recent T2 analyses
    print("\nProcessing recent T2 analyses...")
    
    try:
        structure = t3_agent.process_t2_analyses()
        
        if structure:
            print(f"\n✓ Strategic structure created: {structure['structure_id']}")
            print(f"  Source analyses: {len(structure['source_analyses'])}")
            print(f"  Opportunities: {len(structure['strategic_insights']['opportunities'])}")
            print(f"  Risks: {len(structure['strategic_insights']['risks'])}")
            print(f"  Recommendations: {len(structure['strategic_insights']['recommendations'])}")
            print(f"  Confidence: {structure['confidence_score']:.2%}")
            
            # Show market narrative
            print(f"\nMarket Narrative:")
            print(f"  {structure['market_narrative']['summary']}")
            
            # Show user segments
            print(f"\nUser Segments:")
            for segment, data in structure['user_segments'].items():
                print(f"  {segment.title()}:")
                print(f"    - Priority insights: {len(data['priority_insights'])}")
                print(f"    - Recommendations: {len(data['recommendations'])}")
                print(f"    - Market readiness: {data['market_readiness']['assessment']}")
                
        else:
            print("\nNo T2 analyses available for processing")
            
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        
    print("\n" + "="*60)
    print("T3 Strategic Agent Ready")
    print("="*60)


if __name__ == "__main__":
    main()