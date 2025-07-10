#!/usr/bin/env python3
"""
Master Intelligence Agent V2 - Using Real Knowledge Base
Houston Development Intelligence Platform
Coordinates all specialized agents and provides unified intelligence interface
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re
from dataclasses import dataclass
from enum import Enum
from knowledge_base_loader import KnowledgeBaseLoader
from perplexity_integration import PerplexityClient
from houston_free_data import HoustonDataAPI
import logging

logger = logging.getLogger(__name__)

class QueryIntent(Enum):
    """Types of queries the master agent can handle"""
    MARKET_ANALYSIS = "market_analysis"
    NEIGHBORHOOD_ASSESSMENT = "neighborhood_assessment"
    INVESTMENT_OPPORTUNITY = "investment_opportunity"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    RISK_ASSESSMENT = "risk_assessment"
    DEVELOPMENT_FEASIBILITY = "development_feasibility"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    COMPREHENSIVE_ANALYSIS = "comprehensive_analysis"

@dataclass
class AgentCapability:
    """Defines what each specialized agent can do"""
    name: str
    domains: List[str]
    capabilities: List[str]
    confidence_threshold: float = 0.8

class MasterIntelligenceAgent:
    def __init__(self):
        self.base_path = Path(".")
        self.agents_path = self.base_path / "6 Specialized Agents"
        self.pipeline_path = self.base_path / "Processing_Pipeline"
        
        # Initialize knowledge base loader
        self.knowledge_loader = KnowledgeBaseLoader()
        
        # Initialize Perplexity for real-time data
        self.perplexity = PerplexityClient()
        
        # Initialize Houston free data sources
        self.houston_data = HoustonDataAPI()
        
        # Define specialized agent capabilities
        self.agent_capabilities = {
            "market_intelligence": AgentCapability(
                name="Market Intelligence Agent",
                domains=["market_analysis", "competitive_landscape", "development_pipeline", "pricing_trends"],
                capabilities=["market_concentration", "developer_analysis", "project_tracking", "trend_forecasting"]
            ),
            "neighborhood_intelligence": AgentCapability(
                name="Neighborhood Intelligence Agent",
                domains=["area_analysis", "demographic_trends", "local_market_conditions"],
                capabilities=["neighborhood_scoring", "growth_projections", "investment_ratings", "infrastructure_assessment"]
            ),
            "financial_intelligence": AgentCapability(
                name="Financial Intelligence Agent",
                domains=["investment_analysis", "financing_options", "roi_calculations", "tax_optimization"],
                capabilities=["financial_modeling", "lending_analysis", "opportunity_zone_benefits", "cash_flow_projections"]
            ),
            "environmental_intelligence": AgentCapability(
                name="Environmental Intelligence Agent",
                domains=["flood_risk", "environmental_compliance", "sustainability", "climate_resilience"],
                capabilities=["risk_mapping", "compliance_requirements", "mitigation_strategies", "green_incentives"]
            ),
            "regulatory_intelligence": AgentCapability(
                name="Regulatory Intelligence Agent",
                domains=["zoning_laws", "building_codes", "permit_processes", "compliance_tracking"],
                capabilities=["zoning_analysis", "permit_guidance", "regulatory_changes", "fast_track_opportunities"]
            ),
            "technology_intelligence": AgentCapability(
                name="Technology & Innovation Intelligence Agent",
                domains=["proptech", "innovation_districts", "smart_buildings", "construction_tech"],
                capabilities=["technology_adoption", "innovation_opportunities", "efficiency_improvements", "future_trends"]
            )
        }
        
        # Map agent IDs to their folder paths
        self.agent_registry = {
            "market_intelligence": self.agents_path / "Market Intelligence Agent",
            "neighborhood_intelligence": self.agents_path / "Neighborhood Intelligence Agent",
            "financial_intelligence": self.agents_path / "Financial Intelligence Agent",
            "environmental_intelligence": self.agents_path / "Environmental Intelligence Agent",
            "regulatory_intelligence": self.agents_path / "Regulatory Intelligence Agent",
            "technology_intelligence": self.agents_path / "Technology & Innovation Intelligence Agent"
        }
        
        # Query intent patterns
        self.intent_patterns = {
            QueryIntent.MARKET_ANALYSIS: [
                r"market\s+(?:analysis|trends|conditions)",
                r"competitive\s+(?:landscape|analysis)",
                r"developer\s+(?:activity|market\s+share)",
                r"pricing\s+trends"
            ],
            QueryIntent.NEIGHBORHOOD_ASSESSMENT: [
                r"(?:neighborhood|area)\s+(?:analysis|assessment)",
                r"(?:katy|woodlands|sugar\s+land|heights|river\s+oaks|midtown|east\s+end)",
                r"local\s+market",
                r"area\s+performance"
            ],
            QueryIntent.INVESTMENT_OPPORTUNITY: [
                r"investment\s+(?:opportunity|opportunities|potential)",
                r"roi|return\s+on\s+investment",
                r"opportunity\s+zones?",
                r"best\s+(?:investments?|areas?\s+to\s+invest)"
            ],
            QueryIntent.REGULATORY_COMPLIANCE: [
                r"(?:zoning|permit|regulatory)\s+(?:requirements?|compliance)",
                r"building\s+codes?",
                r"regulatory\s+(?:changes?|updates?)",
                r"compliance\s+(?:requirements?|checklist)"
            ],
            QueryIntent.RISK_ASSESSMENT: [
                r"risk\s+(?:assessment|analysis|factors)",
                r"flood\s+(?:risk|zone)",
                r"environmental\s+(?:risks?|concerns?)",
                r"market\s+risks?"
            ],
            QueryIntent.DEVELOPMENT_FEASIBILITY: [
                r"feasibility\s+(?:study|analysis)",
                r"can\s+i\s+(?:build|develop)",
                r"development\s+potential",
                r"project\s+viability"
            ],
            QueryIntent.COMPETITIVE_INTELLIGENCE: [
                r"competitor\s+(?:analysis|activity)",
                r"what\s+are\s+(?:other\s+)?developers?\s+doing",
                r"market\s+leaders",
                r"competitive\s+(?:advantage|positioning)"
            ],
            QueryIntent.COMPREHENSIVE_ANALYSIS: [
                r"comprehensive\s+(?:analysis|report)",
                r"full\s+(?:assessment|analysis)",
                r"everything\s+about",
                r"complete\s+(?:overview|analysis)"
            ]
        }
        
        # Load cross-domain mappings
        self.cross_domain_mappings = self.load_cross_domain_mappings()
    
    def analyze_query(self, user_query: str) -> Dict[str, Any]:
        """Analyze user query and route to appropriate agents"""
        query_lower = user_query.lower()
        
        # Extract query context
        query_context = self.extract_query_context(query_lower)
        
        # Determine query intent
        intent = self.determine_intent(query_lower)
        
        # Extract location if mentioned
        location = self.extract_location(query_lower)
        
        # Identify relevant agents
        relevant_agents = self.identify_relevant_agents(intent, query_lower)
        
        # Gather intelligence from each relevant agent - NOW USING REAL DATA
        intelligence_results = self.gather_multi_agent_intelligence(
            relevant_agents, user_query, intent, location, query_context
        )
        
        # Add real-time data from Perplexity and free sources
        real_time_data = self.gather_real_time_data(user_query, location)
        if real_time_data:
            intelligence_results["real_time"] = real_time_data
        
        # Synthesize comprehensive response
        synthesized_response = self.synthesize_intelligence(
            intelligence_results, intent, user_query
        )
        
        return synthesized_response
    
    def gather_real_time_data(self, query: str, location: Optional[str]) -> Dict[str, Any]:
        """Gather real-time data from Perplexity and free sources"""
        real_time_data = {
            "live_insights": [],
            "recent_permits": [],
            "market_updates": []
        }
        
        try:
            # Get Perplexity insights
            perplexity_results = self.perplexity.search_houston_real_estate(query)
            if perplexity_results.get('answer'):
                real_time_data["live_insights"].append({
                    "source": "Perplexity AI",
                    "insight": perplexity_results['answer'],
                    "timestamp": datetime.now().isoformat()
                })
            
            # Get recent permits from Houston Open Data
            if "permit" in query.lower():
                permits = self.houston_data.get_building_permits(days_back=7, limit=10)
                real_time_data["recent_permits"] = permits
            
            # Get neighborhood data if location specified
            if location:
                neighborhood_stats = self.houston_data.get_neighborhood_demographics(location)
                if neighborhood_stats:
                    real_time_data["neighborhood_stats"] = neighborhood_stats
                    
        except Exception as e:
            logger.error(f"Error gathering real-time data: {str(e)}")
        
        return real_time_data
    
    def extract_query_context(self, query: str) -> Dict[str, Any]:
        """Extract additional context from the query"""
        context = {
            "property_type": None,
            "action_type": None,
            "time_frame": None,
            "budget_mentioned": False,
            "ranking_requested": False,
            "comparison_requested": False
        }
        
        # Check for property types
        property_types = ["residential", "commercial", "multifamily", "mixed-use", "industrial", "retail"]
        for prop_type in property_types:
            if prop_type in query:
                context["property_type"] = prop_type
                break
        
        # Check for action types
        if any(word in query for word in ["invest", "buy", "purchase", "acquire"]):
            context["action_type"] = "investment"
        elif any(word in query for word in ["develop", "build", "construct"]):
            context["action_type"] = "development"
        elif any(word in query for word in ["rent", "lease"]):
            context["action_type"] = "rental"
        
        # Check for rankings/comparisons
        if any(word in query for word in ["best", "top", "rank", "compare", "versus", "vs"]):
            context["ranking_requested"] = True
        
        # Check for specific data requests
        if any(word in query for word in ["list", "show me", "what are", "how many"]):
            context["comparison_requested"] = True
        
        return context
    
    def determine_intent(self, query: str) -> QueryIntent:
        """Determine the primary intent of the query"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return intent
        
        # Default to comprehensive analysis if no specific intent found
        return QueryIntent.COMPREHENSIVE_ANALYSIS
    
    def extract_location(self, query: str) -> Optional[str]:
        """Extract location mentioned in query"""
        locations = [
            "katy", "the woodlands", "sugar land", "houston heights", "river oaks",
            "midtown", "east end", "downtown", "energy corridor", "galleria",
            "memorial", "montrose", "west university", "bellaire", "pearland"
        ]
        
        for location in locations:
            if location in query:
                return location.title()
        
        return None
    
    def identify_relevant_agents(self, intent: QueryIntent, query: str) -> List[str]:
        """Identify which agents should be consulted for this query"""
        agent_mapping = {
            QueryIntent.MARKET_ANALYSIS: ["market_intelligence", "neighborhood_intelligence"],
            QueryIntent.NEIGHBORHOOD_ASSESSMENT: ["neighborhood_intelligence", "market_intelligence", "environmental_intelligence"],
            QueryIntent.INVESTMENT_OPPORTUNITY: ["financial_intelligence", "market_intelligence", "neighborhood_intelligence"],
            QueryIntent.REGULATORY_COMPLIANCE: ["regulatory_intelligence", "environmental_intelligence"],
            QueryIntent.RISK_ASSESSMENT: ["environmental_intelligence", "financial_intelligence", "market_intelligence"],
            QueryIntent.DEVELOPMENT_FEASIBILITY: ["regulatory_intelligence", "market_intelligence", "environmental_intelligence", "financial_intelligence"],
            QueryIntent.COMPETITIVE_INTELLIGENCE: ["market_intelligence"],
            QueryIntent.COMPREHENSIVE_ANALYSIS: list(self.agent_capabilities.keys())  # All agents
        }
        
        base_agents = agent_mapping.get(intent, ["market_intelligence"])
        
        # Add technology agent if tech-related terms mentioned
        tech_terms = ["technology", "proptech", "innovation", "smart", "ai", "automation"]
        if any(term in query for term in tech_terms):
            if "technology_intelligence" not in base_agents:
                base_agents.append("technology_intelligence")
        
        return base_agents
    
    def gather_multi_agent_intelligence(
        self, 
        agents: List[str], 
        query: str, 
        intent: QueryIntent,
        location: Optional[str],
        query_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gather intelligence from multiple specialized agents using REAL knowledge base data"""
        results = {}
        
        for agent_id in agents:
            if agent_id in self.agent_capabilities:
                # Query with real knowledge base data
                agent_data = self.query_specialized_agent(agent_id, query, intent, location, query_context)
                if agent_data:
                    results[agent_id] = agent_data
        
        # Add cross-domain insights
        cross_domain_insights = self.knowledge_loader.get_cross_domain_insights()
        if cross_domain_insights:
            results["cross_domain"] = cross_domain_insights
        
        return results
    
    def query_specialized_agent(
        self, 
        agent_id: str, 
        query: str, 
        intent: QueryIntent,
        location: Optional[str],
        query_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Query a specific specialized agent using REAL knowledge base data"""
        # Search the actual knowledge base
        search_results = self.knowledge_loader.search_knowledge(agent_id, query, top_k=5)
        
        # Get location-specific results if location is provided
        location_results = []
        if location:
            location_results = self.knowledge_loader.get_location_specific_knowledge(location, agent_id)
        
        # Get category-specific results based on intent
        category_results = []
        if intent == QueryIntent.INVESTMENT_OPPORTUNITY:
            category_results = self.knowledge_loader.get_category_knowledge("investment", agent_id)
        elif intent == QueryIntent.REGULATORY_COMPLIANCE:
            category_results = self.knowledge_loader.get_category_knowledge("permits", agent_id)
        elif intent == QueryIntent.RISK_ASSESSMENT:
            category_results = self.knowledge_loader.get_category_knowledge("risk", agent_id)
        elif "trend" in query.lower():
            category_results = self.knowledge_loader.get_category_knowledge("trends", agent_id)
        elif "permit" in query.lower():
            category_results = self.knowledge_loader.get_category_knowledge("permits", agent_id)
        
        # Combine and deduplicate results
        all_results = search_results + location_results + category_results
        seen_titles = set()
        unique_results = []
        for result in all_results:
            title = result.get('title', result.get('insight', str(result)))
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_results.append(result)
        
        # Build agent knowledge response from real data
        agent_knowledge = {
            "agent_name": self.agent_capabilities[agent_id].name,
            "confidence": 0.85,
            "insights": [],
            "data_points": [],
            "sources": []
        }
        
        # Extract insights and data points from real results
        for result in unique_results[:5]:  # Top 5 most relevant
            # Add insight
            insight = result.get('insight') or result.get('title') or result.get('content', '')
            if insight:
                agent_knowledge["insights"].append(insight)
            
            # Add data points if available
            if 'data_points' in result:
                agent_knowledge["data_points"].extend(result['data_points'])
            elif 'metrics' in result:
                for metric, value in result['metrics'].items():
                    agent_knowledge["data_points"].append({
                        "metric": metric,
                        "value": str(value)
                    })
            
            # Track source
            source = result.get('source', result.get('agent_source', agent_id))
            if source not in agent_knowledge["sources"]:
                agent_knowledge["sources"].append(source)
            
            # Update confidence based on relevance scores
            if 'relevance_score' in result:
                agent_knowledge["confidence"] = max(agent_knowledge["confidence"], result['relevance_score'])
        
        # If no results found, return None to indicate no data available
        if not agent_knowledge["insights"]:
            return None
        
        return agent_knowledge
    
    def get_cross_domain_insights(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get cross-domain insights from knowledge base"""
        return self.knowledge_loader.get_cross_domain_insights()
    
    def synthesize_intelligence(
        self, 
        results: Dict[str, Any], 
        intent: QueryIntent, 
        original_query: str
    ) -> Dict[str, Any]:
        """Synthesize multi-agent intelligence into comprehensive response"""
        # Count actual insights found
        total_insights = sum(
            len(data.get("insights", [])) 
            for data in results.values() 
            if isinstance(data, dict)
        )
        
        synthesis = {
            "query": original_query,
            "intent": intent.value,
            "timestamp": datetime.now().isoformat(),
            "confidence": self.calculate_overall_confidence(results),
            "executive_summary": self.generate_executive_summary(results, intent, original_query),
            "key_insights": self.extract_key_insights(results),
            "data_highlights": self.compile_data_highlights(results),
            "recommendations": self.generate_recommendations(results, intent),
            "risk_factors": self.identify_risk_factors(results),
            "opportunities": self.identify_opportunities(results),
            "next_steps": self.suggest_next_steps(results, intent),
            "sources": self.list_intelligence_sources(results),
            "data_quality": {
                "total_insights": total_insights,
                "agents_consulted": len(results),
                "real_time_data": "real_time" in results
            }
        }
        
        return synthesis
    
    def calculate_overall_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence score from multi-agent results"""
        confidences = []
        for agent_id, data in results.items():
            if isinstance(data, dict) and "confidence" in data:
                confidences.append(data["confidence"])
        
        return sum(confidences) / len(confidences) if confidences else 0.5
    
    def generate_executive_summary(self, results: Dict[str, Any], intent: QueryIntent, query: str) -> str:
        """Generate executive summary based on real data results"""
        # Check if we have real insights
        insights_found = False
        key_findings = []
        
        for agent_id, data in results.items():
            if isinstance(data, dict) and data.get("insights"):
                insights_found = True
                # Take first insight from each agent for summary
                key_findings.append(data["insights"][0])
        
        if not insights_found:
            return f"Limited data available for your query about {query}. Consider refining your search or checking specific neighborhoods or categories."
        
        # Create summary based on intent and actual findings
        if intent == QueryIntent.MARKET_ANALYSIS:
            summary = f"Market analysis reveals: {'; '.join(key_findings[:2])}"
        elif intent == QueryIntent.NEIGHBORHOOD_ASSESSMENT:
            summary = f"Neighborhood assessment shows: {'; '.join(key_findings[:2])}"
        elif intent == QueryIntent.INVESTMENT_OPPORTUNITY:
            summary = f"Investment opportunities identified: {'; '.join(key_findings[:2])}"
        elif intent == QueryIntent.REGULATORY_COMPLIANCE:
            summary = f"Regulatory considerations: {'; '.join(key_findings[:2])}"
        elif intent == QueryIntent.RISK_ASSESSMENT:
            summary = f"Risk assessment findings: {'; '.join(key_findings[:2])}"
        else:
            summary = f"Analysis reveals: {'; '.join(key_findings[:3])}"
        
        # Add real-time data if available
        if "real_time" in results and results["real_time"].get("live_insights"):
            summary += f" Latest update: {results['real_time']['live_insights'][0]['insight'][:100]}..."
        
        return summary
    
    def extract_key_insights(self, results: Dict[str, Any]) -> List[str]:
        """Extract top insights from all agents"""
        all_insights = []
        
        for agent_id, data in results.items():
            if isinstance(data, dict) and "insights" in data:
                # Add agent attribution to insights
                agent_name = data.get("agent_name", agent_id)
                for insight in data["insights"]:
                    all_insights.append(f"[{agent_name}] {insight}")
        
        # Add cross-domain insights
        if "cross_domain" in results:
            for cross_insight in results["cross_domain"][:3]:
                if isinstance(cross_insight, dict):
                    all_insights.append(f"[Cross-Domain] {cross_insight.get('insight', '')}")
                else:
                    all_insights.append(f"[Cross-Domain] {str(cross_insight)}")
        
        # Add real-time insights
        if "real_time" in results and results["real_time"].get("live_insights"):
            for live_insight in results["real_time"]["live_insights"][:2]:
                all_insights.append(f"[Live Data] {live_insight['insight']}")
        
        # Return top 10 insights
        return all_insights[:10] if all_insights else ["No specific insights found for this query"]
    
    def compile_data_highlights(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compile key data points from all agents"""
        data_highlights = []
        
        for agent_id, data in results.items():
            if isinstance(data, dict) and "data_points" in data:
                for point in data["data_points"]:
                    highlight = {
                        "source": data.get("agent_name", agent_id),
                        **point
                    }
                    data_highlights.append(highlight)
        
        # Add recent permits if available
        if "real_time" in results and results["real_time"].get("recent_permits"):
            for permit in results["real_time"]["recent_permits"][:3]:
                data_highlights.append({
                    "source": "Houston Open Data",
                    "metric": "Recent Permit",
                    "value": f"{permit.get('project_name', 'N/A')} - ${permit.get('project_value', 0):,.0f}"
                })
        
        # Sort by importance (simplified - in production would use more sophisticated ranking)
        return data_highlights[:15]
    
    def generate_recommendations(self, results: Dict[str, Any], intent: QueryIntent) -> List[str]:
        """Generate actionable recommendations based on real data"""
        recommendations = []
        
        # Extract recommendations from insights
        for agent_id, data in results.items():
            if isinstance(data, dict) and "insights" in data:
                for insight in data["insights"]:
                    # Look for actionable patterns in insights
                    if any(word in insight.lower() for word in ["opportunity", "recommend", "consider", "invest", "develop"]):
                        recommendations.append(insight)
        
        # Add intent-specific recommendations if we found relevant data
        if recommendations or any(r.get("insights") for r in results.values() if isinstance(r, dict)):
            if intent == QueryIntent.INVESTMENT_OPPORTUNITY:
                recommendations.append("Review specific property listings in identified high-growth areas")
                recommendations.append("Consult with local real estate professionals for detailed market analysis")
            elif intent == QueryIntent.DEVELOPMENT_FEASIBILITY:
                recommendations.append("Conduct detailed site analysis for specific properties of interest")
                recommendations.append("Engage with city planning department for pre-development meetings")
        
        return recommendations[:7] if recommendations else ["Gather more specific data for targeted recommendations"]
    
    def identify_risk_factors(self, results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify key risk factors from intelligence"""
        risks = []
        
        # Look for risk-related insights
        for agent_id, data in results.items():
            if isinstance(data, dict) and "insights" in data:
                for insight in data["insights"]:
                    if any(word in insight.lower() for word in ["risk", "challenge", "concern", "issue", "problem"]):
                        risks.append({
                            "category": data.get("agent_name", "General"),
                            "risk": insight,
                            "severity": "Medium",  # Would be calculated based on context
                            "mitigation": "Consult with specialists for detailed risk assessment"
                        })
        
        return risks[:5] if risks else []
    
    def identify_opportunities(self, results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify key opportunities from intelligence"""
        opportunities = []
        
        # Extract opportunities from insights
        for agent_id, data in results.items():
            if isinstance(data, dict) and "insights" in data:
                for insight in data["insights"]:
                    if any(word in insight.lower() for word in ["opportunity", "growth", "potential", "emerging", "trending"]):
                        opportunities.append({
                            "type": data.get("agent_name", "General"),
                            "opportunity": insight,
                            "confidence": str(data.get("confidence", 0.7))
                        })
        
        return opportunities[:5] if opportunities else []
    
    def suggest_next_steps(self, results: Dict[str, Any], intent: QueryIntent) -> List[str]:
        """Suggest concrete next steps based on analysis"""
        next_steps = []
        
        # Check if we have substantial data
        has_data = any(r.get("insights") for r in results.values() if isinstance(r, dict))
        
        if has_data:
            if intent == QueryIntent.INVESTMENT_OPPORTUNITY:
                next_steps = [
                    "Review detailed property listings in identified areas",
                    "Analyze specific ROI calculations for target properties",
                    "Schedule meetings with local real estate professionals"
                ]
            elif intent == QueryIntent.DEVELOPMENT_FEASIBILITY:
                next_steps = [
                    "Commission detailed site feasibility studies",
                    "Engage with city planning for specific requirements",
                    "Develop preliminary project pro formas"
                ]
            elif intent == QueryIntent.MARKET_ANALYSIS:
                next_steps = [
                    "Deep dive into specific market segments of interest",
                    "Track weekly permit and development activity",
                    "Monitor competitor activities in target areas"
                ]
            else:
                next_steps = [
                    "Refine search parameters for more specific insights",
                    "Explore detailed reports for areas of interest",
                    "Set up automated alerts for market changes"
                ]
        else:
            next_steps = [
                "Provide more specific query parameters (location, property type, budget)",
                "Request detailed analysis for particular neighborhoods",
                "Explore our specialized agent capabilities for targeted insights"
            ]
        
        return next_steps
    
    def list_intelligence_sources(self, results: Dict[str, Any]) -> List[str]:
        """List all intelligence sources consulted"""
        sources = set()
        
        for agent_id, data in results.items():
            if isinstance(data, dict):
                # Add agent name
                if "agent_name" in data:
                    sources.add(data["agent_name"])
                # Add specific sources mentioned
                if "sources" in data:
                    sources.update(data["sources"])
        
        # Add real-time sources
        if "real_time" in results:
            sources.add("Perplexity AI Real-Time Search")
            sources.add("Houston Open Data Portal")
        
        return list(sources)
    
    def load_cross_domain_mappings(self) -> Dict[str, Any]:
        """Load cross-domain intelligence mappings"""
        mappings_file = self.pipeline_path / "Cross_Domain_Intelligence" / "mappings.json"
        
        if mappings_file.exists():
            with open(mappings_file, 'r') as f:
                return json.load(f)
        
        # Default mappings
        return {
            "market_financial": ["pricing_lending", "developer_financing", "roi_patterns"],
            "environmental_regulatory": ["compliance_requirements", "mitigation_permits", "green_incentives"],
            "neighborhood_technology": ["smart_districts", "innovation_zones", "tech_adoption"],
            "financial_regulatory": ["tax_incentives", "opportunity_zones", "financing_regulations"]
        }
    
    def format_response_for_display(self, synthesis: Dict[str, Any]) -> str:
        """Format the synthesized response for user display"""
        display = f"""
# Houston Development Intelligence Report

**Query**: {synthesis['query']}
**Analysis Type**: {synthesis['intent'].replace('_', ' ').title()}
**Confidence**: {synthesis['confidence']*100:.1f}%
**Generated**: {synthesis['timestamp']}
**Data Quality**: {synthesis['data_quality']['total_insights']} insights from {synthesis['data_quality']['agents_consulted']} agents

## Executive Summary
{synthesis['executive_summary']}

## Key Insights
"""
        for i, insight in enumerate(synthesis['key_insights'], 1):
            display += f"{i}. {insight}\n"
        
        display += "\n## Recommendations\n"
        for i, rec in enumerate(synthesis['recommendations'], 1):
            display += f"{i}. {rec}\n"
        
        display += "\n## Opportunities\n"
        for opp in synthesis['opportunities']:
            display += f"- **{opp['type']}**: {opp['opportunity']} (Confidence: {opp['confidence']})\n"
        
        display += "\n## Risk Factors\n"
        for risk in synthesis['risk_factors']:
            display += f"- **{risk['category']}**: {risk['risk']}\n"
            display += f"  - Severity: {risk['severity']}\n"
            display += f"  - Mitigation: {risk['mitigation']}\n"
        
        display += "\n## Next Steps\n"
        for i, step in enumerate(synthesis['next_steps'], 1):
            display += f"{i}. {step}\n"
        
        display += f"\n## Intelligence Sources\n"
        for source in synthesis['sources']:
            display += f"- {source}\n"
        
        return display


def demonstrate_master_agent():
    """Demonstrate the Master Intelligence Agent capabilities"""
    master = MasterIntelligenceAgent()
    
    # Example queries
    test_queries = [
        "What are the latest building permits in Houston?",
        "Give me investment opportunities in Houston Heights",
        "What are the risks of developing in flood-prone areas?",
        "Show me the top neighborhoods for multifamily development",
        "What's the market trend in River Oaks?",
        "Find properties with tax issues in East End"
    ]
    
    print("🧠 Master Intelligence Agent V2 - Using Real Knowledge Base")
    print("=" * 60)
    
    # Test different queries
    for query in test_queries[:2]:  # Test first 2 queries
        print(f"\nProcessing Query: '{query}'")
        print("-" * 60)
        
        # Analyze query
        result = master.analyze_query(query)
        
        # Display formatted response
        formatted = master.format_response_for_display(result)
        print(formatted)
        
        print("\n" + "="*60)
    
    print("\n✅ Master Intelligence Agent V2 is using real knowledge base data!")


if __name__ == "__main__":
    demonstrate_master_agent()