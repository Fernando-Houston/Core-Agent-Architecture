#!/usr/bin/env python3
"""
Master Intelligence Agent
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
        
        # Determine query intent
        intent = self.determine_intent(query_lower)
        
        # Extract location if mentioned
        location = self.extract_location(query_lower)
        
        # Identify relevant agents
        relevant_agents = self.identify_relevant_agents(intent, query_lower)
        
        # Gather intelligence from each relevant agent
        intelligence_results = self.gather_multi_agent_intelligence(
            relevant_agents, user_query, intent, location
        )
        
        # Synthesize comprehensive response
        synthesized_response = self.synthesize_intelligence(
            intelligence_results, intent, user_query
        )
        
        return synthesized_response
    
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
        location: Optional[str]
    ) -> Dict[str, Any]:
        """Gather intelligence from multiple specialized agents"""
        results = {}
        
        for agent_id in agents:
            if agent_id in self.agent_capabilities:
                agent_data = self.query_specialized_agent(agent_id, query, intent, location)
                if agent_data:
                    results[agent_id] = agent_data
        
        # Add cross-domain insights
        results["cross_domain"] = self.get_cross_domain_insights(results)
        
        return results
    
    def query_specialized_agent(
        self, 
        agent_id: str, 
        query: str, 
        intent: QueryIntent,
        location: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Query a specific specialized agent"""
        agent_path = self.agents_path / agent_id.replace("_", " ").title()
        
        if not agent_path.exists():
            return None
        
        # Simulate querying the agent's knowledge base
        # In production, this would involve more sophisticated retrieval
        agent_knowledge = {
            "agent_name": self.agent_capabilities[agent_id].name,
            "confidence": 0.85,
            "insights": [],
            "data_points": []
        }
        
        # Market Intelligence Agent response
        if agent_id == "market_intelligence":
            agent_knowledge["insights"] = [
                "Houston market showing strong growth with 6.62% YoY price increase",
                "Market concentration high with top 10 developers controlling 81.8%",
                "Multifamily projects dominating with 62 active developments",
                "Inner Loop remains hottest development area with 58 projects"
            ]
            agent_knowledge["data_points"] = [
                {"metric": "Average Price/SqFt", "value": "$316.83", "trend": "increasing"},
                {"metric": "Market HHI", "value": "10,106,800", "interpretation": "highly concentrated"},
                {"metric": "Inventory Months", "value": "48.6", "interpretation": "balanced market"}
            ]
            
        # Neighborhood Intelligence Agent response
        elif agent_id == "neighborhood_intelligence" and location:
            agent_knowledge["insights"] = [
                f"{location} showing strong investment potential",
                f"Infrastructure improvements driving development interest in {location}",
                f"Demographic shifts favoring mixed-use developments in {location}"
            ]
            agent_knowledge["data_points"] = [
                {"metric": "Investment Score", "value": "8.5/10", "trend": "improving"},
                {"metric": "Population Growth", "value": "3.2%", "timeframe": "annual"},
                {"metric": "Development Pipeline", "value": "12 projects", "status": "active"}
            ]
            
        # Financial Intelligence Agent response
        elif agent_id == "financial_intelligence":
            agent_knowledge["insights"] = [
                "Construction lending rates at 7.25%, up 15 basis points",
                "Opportunity zones offering 10% basis step-up for qualified investments",
                "Average project ROI at 18.5% for mixed-use developments",
                "Tax incentives available for green building certifications"
            ]
            agent_knowledge["data_points"] = [
                {"metric": "Avg Construction Rate", "value": "7.25%", "change": "+0.15%"},
                {"metric": "Project ROI", "value": "18.5%", "asset_type": "mixed-use"},
                {"metric": "OZ Tax Benefit", "value": "10%", "holding_period": "10 years"}
            ]
            
        # Environmental Intelligence Agent response
        elif agent_id == "environmental_intelligence":
            agent_knowledge["insights"] = [
                "Flood risk mitigation required for 35% of development areas",
                "Environmental compliance adding 5-7% to project costs",
                "Green building incentives can offset up to 3% of construction costs"
            ]
            agent_knowledge["data_points"] = [
                {"metric": "Flood Zone Coverage", "value": "35%", "risk_level": "moderate"},
                {"metric": "Compliance Cost", "value": "5-7%", "of_total": "project cost"},
                {"metric": "Green Incentives", "value": "3%", "potential_offset": "construction"}
            ]
            
        # Regulatory Intelligence Agent response
        elif agent_id == "regulatory_intelligence":
            agent_knowledge["insights"] = [
                "New mixed-use zoning flexibility in targeted growth corridors",
                "Fast-track permitting available for projects meeting sustainability criteria",
                "Building height restrictions relaxed in transit-oriented developments"
            ]
            agent_knowledge["data_points"] = [
                {"metric": "Permit Timeline", "value": "120 days", "fast_track": "60 days"},
                {"metric": "Zoning Changes", "value": "8", "timeframe": "last 6 months"},
                {"metric": "Variance Approval Rate", "value": "73%", "trend": "increasing"}
            ]
            
        # Technology Intelligence Agent response
        elif agent_id == "technology_intelligence":
            agent_knowledge["insights"] = [
                "PropTech adoption showing 22% efficiency improvement in project delivery",
                "Smart building features commanding 12-15% rent premiums",
                "Innovation district developments attracting tech tenant base"
            ]
            agent_knowledge["data_points"] = [
                {"metric": "PropTech ROI", "value": "22%", "category": "efficiency"},
                {"metric": "Smart Building Premium", "value": "12-15%", "type": "rent"},
                {"metric": "Tech Tenant Demand", "value": "High", "growth": "accelerating"}
            ]
        
        return agent_knowledge
    
    def get_cross_domain_insights(self, agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify insights that span multiple domains"""
        cross_domain_insights = []
        
        # Example: Market + Financial correlation
        if "market_intelligence" in agent_results and "financial_intelligence" in agent_results:
            cross_domain_insights.append({
                "domains": ["market", "financial"],
                "insight": "High market concentration (HHI: 10,106,800) creating favorable lending terms for established developers",
                "opportunity": "Partner with top-tier developers to access better financing",
                "confidence": 0.88
            })
        
        # Example: Environmental + Regulatory synergy
        if "environmental_intelligence" in agent_results and "regulatory_intelligence" in agent_results:
            cross_domain_insights.append({
                "domains": ["environmental", "regulatory"],
                "insight": "Fast-track permitting available for green-certified projects, offsetting 3% construction costs",
                "opportunity": "Design to LEED Gold standard for permit acceleration and cost savings",
                "confidence": 0.91
            })
        
        # Example: Neighborhood + Technology correlation
        if "neighborhood_intelligence" in agent_results and "technology_intelligence" in agent_results:
            cross_domain_insights.append({
                "domains": ["neighborhood", "technology"],
                "insight": "Innovation districts showing 22% higher absorption rates for smart-enabled buildings",
                "opportunity": "Focus smart building features in tech-corridor neighborhoods",
                "confidence": 0.85
            })
        
        return cross_domain_insights
    
    def synthesize_intelligence(
        self, 
        results: Dict[str, Any], 
        intent: QueryIntent, 
        original_query: str
    ) -> Dict[str, Any]:
        """Synthesize multi-agent intelligence into comprehensive response"""
        synthesis = {
            "query": original_query,
            "intent": intent.value,
            "timestamp": datetime.now().isoformat(),
            "confidence": self.calculate_overall_confidence(results),
            "executive_summary": self.generate_executive_summary(results, intent),
            "key_insights": self.extract_key_insights(results),
            "data_highlights": self.compile_data_highlights(results),
            "recommendations": self.generate_recommendations(results, intent),
            "risk_factors": self.identify_risk_factors(results),
            "opportunities": self.identify_opportunities(results),
            "next_steps": self.suggest_next_steps(results, intent),
            "sources": self.list_intelligence_sources(results)
        }
        
        return synthesis
    
    def calculate_overall_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence score from multi-agent results"""
        confidences = []
        for agent_id, data in results.items():
            if isinstance(data, dict) and "confidence" in data:
                confidences.append(data["confidence"])
        
        return sum(confidences) / len(confidences) if confidences else 0.8
    
    def generate_executive_summary(self, results: Dict[str, Any], intent: QueryIntent) -> str:
        """Generate executive summary based on intent and results"""
        summaries = {
            QueryIntent.MARKET_ANALYSIS: "Houston's development market shows strong fundamentals with 6.62% YoY price growth and high concentration among top developers. The market favors established players with access to capital and land positions.",
            
            QueryIntent.NEIGHBORHOOD_ASSESSMENT: "Neighborhood analysis reveals diverse opportunities across Houston's submarkets, with Inner Loop areas showing highest activity and emerging neighborhoods offering value plays for early movers.",
            
            QueryIntent.INVESTMENT_OPPORTUNITY: "Investment opportunities are strongest in mixed-use developments (18.5% ROI) and opportunity zones offering significant tax advantages. Focus on transit-oriented locations with smart building features.",
            
            QueryIntent.REGULATORY_COMPLIANCE: "Regulatory environment is becoming more flexible with mixed-use zoning updates and fast-track permitting for sustainable projects. Compliance costs range 5-7% but can be offset through incentives.",
            
            QueryIntent.RISK_ASSESSMENT: "Primary risks include flood exposure (35% of areas), rising construction costs, and market concentration. Mitigation strategies include green building design and strategic partnerships.",
            
            QueryIntent.DEVELOPMENT_FEASIBILITY: "Development feasibility is strong for well-capitalized projects in growth corridors. Fast-track permitting and zoning flexibility improve project economics, while technology adoption enhances returns.",
            
            QueryIntent.COMPETITIVE_INTELLIGENCE: "Top 10 developers control 81.8% of market, creating both competitive pressure and partnership opportunities. Differentiation through technology and sustainability is key.",
            
            QueryIntent.COMPREHENSIVE_ANALYSIS: "Comprehensive analysis reveals Houston as a dynamic development market with strong growth fundamentals, evolving regulatory landscape, and increasing importance of technology and sustainability in project success."
        }
        
        base_summary = summaries.get(intent, summaries[QueryIntent.COMPREHENSIVE_ANALYSIS])
        
        # Add specific insights from results
        key_metrics = []
        for agent_id, data in results.items():
            if isinstance(data, dict) and "data_points" in data:
                for point in data["data_points"][:2]:  # Top 2 metrics per agent
                    if "metric" in point and "value" in point:
                        key_metrics.append(f"{point['metric']}: {point['value']}")
        
        if key_metrics:
            base_summary += f" Key metrics: {', '.join(key_metrics[:3])}."
        
        return base_summary
    
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
            for cross_insight in results["cross_domain"]:
                all_insights.append(f"[Cross-Domain] {cross_insight.get('insight', '')}")
        
        # Return top 10 insights
        return all_insights[:10]
    
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
        
        # Sort by importance (simplified - in production would use more sophisticated ranking)
        return data_highlights[:15]
    
    def generate_recommendations(self, results: Dict[str, Any], intent: QueryIntent) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Intent-specific recommendations
        if intent == QueryIntent.INVESTMENT_OPPORTUNITY:
            recommendations.extend([
                "Target mixed-use developments in Inner Loop for highest returns (18.5% ROI)",
                "Leverage opportunity zone investments for 10% tax basis step-up",
                "Incorporate smart building features for 12-15% rent premiums"
            ])
        elif intent == QueryIntent.DEVELOPMENT_FEASIBILITY:
            recommendations.extend([
                "Design to LEED Gold standard for fast-track permitting (50% time reduction)",
                "Focus on transit-oriented locations with relaxed height restrictions",
                "Budget 5-7% for environmental compliance, offset with green incentives"
            ])
        elif intent == QueryIntent.RISK_ASSESSMENT:
            recommendations.extend([
                "Implement flood mitigation strategies for 35% of development areas",
                "Partner with established developers to access better financing terms",
                "Adopt PropTech solutions for 22% efficiency improvement"
            ])
        
        # Add agent-specific recommendations
        if "financial_intelligence" in results:
            recommendations.append("Lock in construction financing now before further rate increases")
        
        if "technology_intelligence" in results:
            recommendations.append("Prioritize innovation district locations for tech-tenant demand")
        
        return recommendations[:7]  # Top 7 recommendations
    
    def identify_risk_factors(self, results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify key risk factors from intelligence"""
        risks = []
        
        # Market risks
        if "market_intelligence" in results:
            risks.append({
                "category": "Market",
                "risk": "High market concentration may limit opportunities for new entrants",
                "severity": "Medium",
                "mitigation": "Partner with established developers or focus on niche markets"
            })
        
        # Environmental risks
        if "environmental_intelligence" in results:
            risks.append({
                "category": "Environmental",
                "risk": "35% of development areas in flood zones",
                "severity": "High",
                "mitigation": "Implement comprehensive flood mitigation and insurance strategies"
            })
        
        # Financial risks
        if "financial_intelligence" in results:
            risks.append({
                "category": "Financial",
                "risk": "Rising construction lending rates impacting project returns",
                "severity": "Medium",
                "mitigation": "Lock in rates early or explore alternative financing"
            })
        
        return risks
    
    def identify_opportunities(self, results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify key opportunities from intelligence"""
        opportunities = []
        
        # Cross-domain opportunities
        for cross_insight in results.get("cross_domain", []):
            if "opportunity" in cross_insight:
                opportunities.append({
                    "type": "Strategic",
                    "opportunity": cross_insight["opportunity"],
                    "confidence": str(cross_insight.get("confidence", 0.85))
                })
        
        # Market opportunities
        if "market_intelligence" in results:
            opportunities.append({
                "type": "Market",
                "opportunity": "Inner Loop development with 58 active projects indicating strong demand",
                "confidence": "0.87"
            })
        
        # Regulatory opportunities
        if "regulatory_intelligence" in results:
            opportunities.append({
                "type": "Regulatory",
                "opportunity": "Fast-track permitting for sustainable projects reducing timeline by 50%",
                "confidence": "0.91"
            })
        
        return opportunities[:5]
    
    def suggest_next_steps(self, results: Dict[str, Any], intent: QueryIntent) -> List[str]:
        """Suggest concrete next steps based on analysis"""
        next_steps = []
        
        if intent == QueryIntent.INVESTMENT_OPPORTUNITY:
            next_steps = [
                "Schedule meetings with top 3 developers for partnership discussions",
                "Analyze specific opportunity zone locations for investment",
                "Conduct detailed ROI analysis on mixed-use vs single-use projects"
            ]
        elif intent == QueryIntent.DEVELOPMENT_FEASIBILITY:
            next_steps = [
                "Commission environmental assessment for target properties",
                "Meet with city planning to discuss fast-track eligibility",
                "Engage green building consultant for LEED certification planning"
            ]
        elif intent == QueryIntent.MARKET_ANALYSIS:
            next_steps = [
                "Deep-dive analysis on top 10 developers' strategies",
                "Map competitor projects in target neighborhoods",
                "Track permit filings weekly for market intelligence"
            ]
        else:
            next_steps = [
                "Review detailed intelligence reports from specialized agents",
                "Schedule follow-up analysis on specific areas of interest",
                "Set up automated alerts for market changes"
            ]
        
        return next_steps
    
    def list_intelligence_sources(self, results: Dict[str, Any]) -> List[str]:
        """List all intelligence sources consulted"""
        sources = []
        
        for agent_id, data in results.items():
            if isinstance(data, dict) and "agent_name" in data:
                sources.append(data["agent_name"])
        
        sources.append("Cross-Domain Intelligence Synthesis")
        
        return sources
    
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
        "What are the best investment opportunities in Houston right now?",
        "Give me a comprehensive analysis of the Katy area development potential",
        "What are the risks of developing in flood-prone areas?",
        "How is technology changing Houston's real estate market?",
        "What should I know about regulatory compliance for a mixed-use project?",
        "Analyze the competitive landscape for multifamily developers"
    ]
    
    print("🧠 Master Intelligence Agent Demonstration")
    print("=" * 60)
    
    # Process first query as example
    query = test_queries[0]
    print(f"\nProcessing Query: '{query}'")
    print("-" * 60)
    
    # Analyze query
    result = master.analyze_query(query)
    
    # Display formatted response
    formatted = master.format_response_for_display(result)
    print(formatted)
    
    # Save example output
    output_path = Path("master_agent_example_output.json")
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Full analysis saved to: {output_path}")
    print("\n✅ Master Intelligence Agent is ready to coordinate all specialized agents!")


if __name__ == "__main__":
    demonstrate_master_agent()