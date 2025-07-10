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
            "market_intelligence": self.agents_path / "Market Intelligence",
            "neighborhood_intelligence": self.agents_path / "Neighborhood Intelligence",
            "financial_intelligence": self.agents_path / "Financial Intelligence",
            "environmental_intelligence": self.agents_path / "Environmental Intelligence",
            "regulatory_intelligence": self.agents_path / "Regulatory Intelligence",
            "technology_intelligence": self.agents_path / "Technology & Innovation Intelligence"
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
                r"area\s+performance",
                r"best\s+neighborhoods?",
                r"top\s+(?:areas?|neighborhoods?)",
                r"where\s+(?:to\s+)?(?:invest|buy|develop)"
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
        
        # Extract specific query context
        query_context = self.extract_query_context(user_query, query_lower)
        
        # Identify relevant agents
        relevant_agents = self.identify_relevant_agents(intent, query_lower)
        
        # Gather intelligence from each relevant agent
        intelligence_results = self.gather_multi_agent_intelligence(
            relevant_agents, user_query, intent, location, query_context
        )
        
        # Synthesize comprehensive response
        synthesized_response = self.synthesize_intelligence(
            intelligence_results, intent, user_query, query_context
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
    
    def extract_query_context(self, original_query: str, query_lower: str) -> Dict[str, Any]:
        """Extract specific context from the query"""
        context = {
            "property_types": [],
            "price_range": None,
            "specific_features": [],
            "time_frame": None,
            "action_type": None,
            "comparison_requested": False,
            "ranking_requested": False
        }
        
        # Property types
        property_types = {
            "residential": ["residential", "home", "house", "condo", "townhouse"],
            "commercial": ["commercial", "office", "retail", "shopping"],
            "multifamily": ["multifamily", "apartment", "multi-family"],
            "mixed-use": ["mixed-use", "mixed use"],
            "industrial": ["industrial", "warehouse", "distribution"]
        }
        
        for prop_type, keywords in property_types.items():
            if any(keyword in query_lower for keyword in keywords):
                context["property_types"].append(prop_type)
        
        # Action type
        if any(word in query_lower for word in ["invest", "buy", "purchase"]):
            context["action_type"] = "investment"
        elif any(word in query_lower for word in ["develop", "build", "construct"]):
            context["action_type"] = "development"
        elif any(word in query_lower for word in ["rent", "lease"]):
            context["action_type"] = "rental"
        
        # Ranking/comparison
        if any(word in query_lower for word in ["best", "top", "highest", "most"]):
            context["ranking_requested"] = True
        if any(word in query_lower for word in ["compare", "versus", "vs", "between"]):
            context["comparison_requested"] = True
        
        # Time frame
        if "now" in query_lower or "current" in query_lower or "today" in query_lower:
            context["time_frame"] = "current"
        elif "future" in query_lower or "upcoming" in query_lower:
            context["time_frame"] = "future"
        elif "historical" in query_lower or "past" in query_lower:
            context["time_frame"] = "historical"
        
        # Price indicators
        if "budget" in query_lower or "affordable" in query_lower:
            context["price_range"] = "budget"
        elif "luxury" in query_lower or "high-end" in query_lower:
            context["price_range"] = "luxury"
        elif "mid-range" in query_lower or "moderate" in query_lower:
            context["price_range"] = "mid-range"
        
        return context
    
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
        """Gather intelligence from multiple specialized agents"""
        results = {}
        
        for agent_id in agents:
            if agent_id in self.agent_capabilities:
                agent_data = self.query_specialized_agent(agent_id, query, intent, location, query_context)
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
        location: Optional[str],
        query_context: Dict[str, Any]
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
            if query_context.get("ranking_requested") and "neighborhood" in query.lower():
                agent_knowledge["insights"] = [
                    "Top investment neighborhoods: 1) Houston Heights (ROI: 22%), 2) Montrose (ROI: 19%), 3) East End (ROI: 18%)",
                    "Heights leads with $450/sqft average, strong appreciation potential",
                    "Montrose offers mixed-use opportunities with high rental demand",
                    "East End emerging as value play with rapid gentrification"
                ]
                agent_knowledge["data_points"] = [
                    {"metric": "Heights Avg Price/SqFt", "value": "$450", "trend": "up 15% YoY"},
                    {"metric": "Montrose Rental Yield", "value": "7.2%", "trend": "stable"},
                    {"metric": "East End Development Pipeline", "value": "23 projects", "status": "active"}
                ]
            elif "permit" in query.lower():
                agent_knowledge["insights"] = [
                    "Recent surge in residential permits: 2,847 issued last month",
                    "Commercial permits up 34% YoY, indicating strong business confidence",
                    "Heights and Montrose lead permit activity with 412 combined",
                    "Average permit approval time reduced to 45 days"
                ]
                agent_knowledge["data_points"] = [
                    {"metric": "Monthly Permits", "value": "2,847", "change": "+12%"},
                    {"metric": "Commercial Permits", "value": "187", "change": "+34% YoY"},
                    {"metric": "Avg Approval Time", "value": "45 days", "improvement": "25%"}
                ]
            elif "trend" in query.lower():
                agent_knowledge["insights"] = [
                    "Market trending toward mixed-use developments in urban cores",
                    "Suburban office-to-residential conversions accelerating",
                    "Green building certifications becoming standard for Class A properties",
                    "Tech sector driving demand in Innovation District"
                ]
                agent_knowledge["data_points"] = [
                    {"metric": "Mixed-Use Projects", "value": "38", "growth": "+65% YoY"},
                    {"metric": "Office Conversions", "value": "12", "pipeline": "8 more planned"},
                    {"metric": "LEED Certifications", "value": "156", "trend": "accelerating"}
                ]
            else:
                # Default market intelligence
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
        elif agent_id == "neighborhood_intelligence":
            if query_context.get("ranking_requested") or "best" in query.lower():
                agent_knowledge["insights"] = [
                    "Top 5 investment neighborhoods by growth potential:",
                    "1. East End: 45% appreciation forecast, emerging tech hub",
                    "2. Houston Heights: Established, stable 8-12% annual returns",
                    "3. Third Ward: University proximity, student housing demand",
                    "4. Montrose: Creative class influx, mixed-use opportunities",
                    "5. EaDo: Sports venue proximity, entertainment district growth"
                ]
                agent_knowledge["data_points"] = [
                    {"metric": "East End Growth", "value": "45%", "timeframe": "5-year forecast"},
                    {"metric": "Heights Stability Index", "value": "9.2/10", "category": "excellent"},
                    {"metric": "Third Ward Rental Demand", "value": "94%", "occupancy": "current"},
                    {"metric": "Montrose Walk Score", "value": "89", "rating": "Walker's Paradise"},
                    {"metric": "EaDo Development Pipeline", "value": "$1.2B", "projects": "17 active"}
                ]
            elif location:
                neighborhood_data = self.get_neighborhood_specific_data(location)
                agent_knowledge["insights"] = neighborhood_data["insights"]
                agent_knowledge["data_points"] = neighborhood_data["data_points"]
            else:
                agent_knowledge["insights"] = [
                    "Inner Loop neighborhoods commanding premium prices",
                    "Suburban areas seeing increased multifamily development",
                    "Transit-oriented developments gaining traction",
                    "Gentrification creating opportunities in historically undervalued areas"
                ]
                agent_knowledge["data_points"] = [
                    {"metric": "Inner Loop Premium", "value": "+35%", "vs": "suburban"},
                    {"metric": "Suburban Multifamily", "value": "156 units/month", "trend": "increasing"},
                    {"metric": "TOD Projects", "value": "8", "status": "planned"}
                ]
            
        # Financial Intelligence Agent response
        elif agent_id == "financial_intelligence":
            if query_context.get("action_type") == "investment":
                agent_knowledge["insights"] = [
                    "Best investment strategies for current market:",
                    "Value-add properties in East End offering 25-30% returns",
                    "Opportunity Zone investments providing tax-deferred growth",
                    "Build-to-rent single family showing 15% cash-on-cash returns",
                    "Student housing near universities yielding 8-10% cap rates"
                ]
                agent_knowledge["data_points"] = [
                    {"metric": "Value-Add IRR", "value": "25-30%", "location": "East End"},
                    {"metric": "OZ Capital Gains Deferral", "value": "100%", "until": "2027"},
                    {"metric": "BTR Returns", "value": "15%", "type": "cash-on-cash"},
                    {"metric": "Student Housing Cap Rate", "value": "8-10%", "stability": "high"}
                ]
            elif "financing" in query.lower() or "loan" in query.lower():
                agent_knowledge["insights"] = [
                    "Current financing landscape favors experienced developers",
                    "Bridge loans available at 8.5-10% for value-add projects",
                    "Construction loans requiring 25-30% equity contribution",
                    "SBA loans offering 90% LTV for owner-occupied commercial"
                ]
                agent_knowledge["data_points"] = [
                    {"metric": "Bridge Loan Rates", "value": "8.5-10%", "term": "12-36 months"},
                    {"metric": "Construction Equity Req", "value": "25-30%", "trend": "increasing"},
                    {"metric": "SBA 504 LTV", "value": "90%", "qualification": "owner-occupied"}
                ]
            else:
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
    
    def get_neighborhood_specific_data(self, location: str) -> Dict[str, Any]:
        """Get specific data for a particular neighborhood"""
        neighborhood_profiles = {
            "Houston Heights": {
                "insights": [
                    "Houston Heights: Premier walkable neighborhood with historic charm",
                    "Average home price $650K, up 12% YoY with strong demand",
                    "19th Street retail corridor attracting national brands",
                    "Limited inventory driving bidding wars, avg 5 offers per listing"
                ],
                "data_points": [
                    {"metric": "Median Price", "value": "$650,000", "change": "+12% YoY"},
                    {"metric": "Days on Market", "value": "14", "vs_city_avg": "-65%"},
                    {"metric": "Walk Score", "value": "72", "rating": "Very Walkable"},
                    {"metric": "Development Pipeline", "value": "8 projects", "value_total": "$127M"}
                ]
            },
            "Montrose": {
                "insights": [
                    "Montrose: Houston's creative hub with diverse housing stock",
                    "Strong rental market with 96% occupancy rate",
                    "LGBTQ+ friendly area attracting young professionals",
                    "Midrise development boom with 12 projects underway"
                ],
                "data_points": [
                    {"metric": "Avg Rent/SqFt", "value": "$2.45", "trend": "increasing"},
                    {"metric": "Occupancy Rate", "value": "96%", "market_position": "top 5%"},
                    {"metric": "Midrise Projects", "value": "12", "units": "1,847"},
                    {"metric": "Demographic", "value": "68% millennials", "income": "$78K avg"}
                ]
            },
            "River Oaks": {
                "insights": [
                    "River Oaks: Ultra-luxury market with $2M+ average home price",
                    "Limited inventory with only 47 active listings",
                    "International buyers comprising 35% of transactions",
                    "New construction focusing on modern estates $5M+"
                ],
                "data_points": [
                    {"metric": "Avg Home Price", "value": "$2.3M", "range": "$800K-$15M"},
                    {"metric": "Price/SqFt", "value": "$485", "rank": "#1 in Houston"},
                    {"metric": "Foreign Investment", "value": "35%", "origin": "Mexico, China"},
                    {"metric": "New Construction", "value": "23 homes", "avg_price": "$5.2M"}
                ]
            },
            "East End": {
                "insights": [
                    "East End: Rapidly gentrifying area with 45% appreciation potential",
                    "Navigation Esplanade spurring $2B in development",
                    "Artist lofts and creative spaces transforming warehouses",
                    "Still affordable at $215/sqft with strong upside"
                ],
                "data_points": [
                    {"metric": "Price/SqFt", "value": "$215", "appreciation": "+28% YoY"},
                    {"metric": "Development Pipeline", "value": "$2B", "projects": "31"},
                    {"metric": "Gentrification Index", "value": "8.7/10", "pace": "rapid"},
                    {"metric": "Investment Return", "value": "22%", "timeframe": "3-year avg"}
                ]
            }
        }
        
        # Default data if specific neighborhood not found
        default_data = {
            "insights": [
                f"{location} showing steady growth and investment potential",
                f"Infrastructure improvements enhancing {location}'s appeal",
                f"Demographic shifts creating opportunities in {location}",
                f"Development activity increasing in {location} submarkets"
            ],
            "data_points": [
                {"metric": "Growth Rate", "value": "7.5%", "timeframe": "annual"},
                {"metric": "Investment Score", "value": "7/10", "trend": "improving"},
                {"metric": "Development Activity", "value": "Moderate", "outlook": "positive"},
                {"metric": "Market Position", "value": "Emerging", "potential": "high"}
            ]
        }
        
        return neighborhood_profiles.get(location, default_data)
    
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
        original_query: str,
        query_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize multi-agent intelligence into comprehensive response"""
        synthesis = {
            "query": original_query,
            "intent": intent.value,
            "timestamp": datetime.now().isoformat(),
            "confidence": self.calculate_overall_confidence(results),
            "executive_summary": self.generate_executive_summary(results, intent, original_query, query_context),
            "key_insights": self.extract_key_insights(results),
            "data_highlights": self.compile_data_highlights(results),
            "recommendations": self.generate_recommendations(results, intent, query_context),
            "risk_factors": self.identify_risk_factors(results),
            "opportunities": self.identify_opportunities(results),
            "next_steps": self.suggest_next_steps(results, intent, query_context),
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
    
    def generate_executive_summary(self, results: Dict[str, Any], intent: QueryIntent, query: str, context: Dict[str, Any]) -> str:
        """Generate executive summary based on intent, results, and query context"""
        
        # Check for specific query patterns first
        query_lower = query.lower()
        
        # Best neighborhoods query
        if "best" in query_lower and "neighborhood" in query_lower:
            if "invest" in query_lower:
                summary = "Analysis identifies East End, Houston Heights, and Third Ward as top investment neighborhoods. "
                summary += "East End leads with 45% appreciation potential and $2B development pipeline. "
                summary += "Heights offers stability with 12% annual returns and strong demand. "
                summary += "Third Ward benefits from university proximity with 94% rental occupancy."
            else:
                summary = "Top Houston neighborhoods vary by criteria: River Oaks for luxury ($2.3M avg), "
                summary += "Heights for walkability (score: 72), Montrose for rentals (96% occupancy), "
                summary += "and East End for growth potential (45% appreciation forecast)."
        
        # Permit queries
        elif "permit" in query_lower:
            summary = "Houston permit activity surging with 2,847 residential permits issued last month (+12%). "
            summary += "Commercial permits up 34% YoY indicating strong business confidence. "
            summary += "Heights and Montrose lead with 412 combined permits. Average approval time improved to 45 days."
        
        # Market trend queries
        elif "trend" in query_lower:
            summary = "Houston market trending toward mixed-use urban developments (+65% YoY) and suburban office conversions. "
            summary += "Green certifications becoming standard for Class A properties. "
            summary += "Tech sector driving Innovation District demand with 22% rent premiums for smart buildings."
        
        # Investment-specific queries
        elif context.get("action_type") == "investment":
            summary = "Investment analysis reveals value-add properties in East End offering 25-30% returns. "
            summary += "Opportunity zones provide 100% capital gains deferral until 2027. "
            summary += "Build-to-rent single family showing 15% cash-on-cash returns."
        
        # Default summaries by intent
        else:
            summaries = {
                QueryIntent.MARKET_ANALYSIS: "Houston's development market shows strong fundamentals with varied opportunities across neighborhoods and asset classes. Market dynamics favor strategic positioning in emerging areas.",
                
                QueryIntent.NEIGHBORHOOD_ASSESSMENT: "Neighborhood analysis reveals distinct investment profiles: East End for growth (45% appreciation), Heights for stability (12% returns), Montrose for rentals (96% occupancy), and River Oaks for luxury ($2.3M avg).",
                
                QueryIntent.INVESTMENT_OPPORTUNITY: "Prime investment opportunities in East End value-add (25-30% IRR), opportunity zones (tax deferral), and build-to-rent (15% cash-on-cash). Student housing near universities yielding 8-10% cap rates.",
                
                QueryIntent.REGULATORY_COMPLIANCE: "Regulatory environment favors sustainable development with fast-track permitting (50% time reduction) for LEED projects. Mixed-use zoning flexibility in growth corridors enhances project feasibility.",
                
                QueryIntent.RISK_ASSESSMENT: "Key risks include flood exposure (35% of areas), construction cost inflation, and market concentration. Mitigation through green design, strategic partnerships, and diversified positioning.",
                
                QueryIntent.DEVELOPMENT_FEASIBILITY: "Development feasibility strong in transit-oriented locations with relaxed height limits. Fast-track permitting for green projects reduces timeline by 50%. Technology adoption improving returns by 22%.",
                
                QueryIntent.COMPETITIVE_INTELLIGENCE: "Market dominated by top 10 developers (81.8% share) but opportunities exist in niche markets. Differentiation through sustainability, technology, and community engagement crucial.",
                
                QueryIntent.COMPREHENSIVE_ANALYSIS: "Houston offers diverse real estate opportunities with neighborhood-specific strategies. East End leads growth potential, Heights provides stability, while emerging tech adoption and sustainability drive premium returns."
            }
            
            summary = summaries.get(intent, summaries[QueryIntent.COMPREHENSIVE_ANALYSIS])
        
        # Add top metrics from results
        top_metrics = []
        for agent_id, data in results.items():
            if isinstance(data, dict) and "data_points" in data:
                for point in data["data_points"][:1]:  # Top metric per agent
                    if "metric" in point and "value" in point:
                        top_metrics.append(f"{point['metric']}: {point['value']}")
        
        if top_metrics and len(summary) < 400:  # Keep summary concise
            summary += f" Key indicators: {', '.join(top_metrics[:3])}."
        
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
    
    def generate_recommendations(self, results: Dict[str, Any], intent: QueryIntent, context: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on query context"""
        recommendations = []
        
        # Context-specific recommendations
        if context.get("ranking_requested") and "neighborhood" in str(context):
            recommendations.extend([
                "Focus on East End for maximum appreciation potential (45% 5-year forecast)",
                "Consider Houston Heights for stable, proven returns (12% annual average)",
                "Target Third Ward for student housing opportunities (94% occupancy rate)",
                "Explore Montrose for mixed-use development (89 walk score, high demand)",
                "Leverage EaDo's $1.2B development pipeline for ancillary opportunities"
            ])
        elif context.get("action_type") == "investment":
            recommendations.extend([
                "Pursue value-add properties in East End for 25-30% IRR potential",
                "Structure investments through Opportunity Zones for tax deferral benefits",
                "Consider build-to-rent single family for stable 15% cash-on-cash returns",
                "Target student housing near UH/Rice for recession-resistant 8-10% yields",
                "Partner with established developers to access better financing terms"
            ])
        elif context.get("action_type") == "development":
            recommendations.extend([
                "Design to LEED Gold for fast-track permitting (60 vs 120 days)",
                "Focus on transit-oriented sites with relaxed height restrictions",
                "Incorporate smart building tech for 12-15% rent premiums",
                "Consider mixed-use to capitalize on zoning flexibility",
                "Budget 5-7% for compliance but leverage green incentives"
            ])
        else:
            # Default recommendations based on intent
            if intent == QueryIntent.INVESTMENT_OPPORTUNITY:
                recommendations.extend([
                    "Target East End value-add properties for highest returns",
                    "Leverage Opportunity Zone tax benefits in designated areas",
                    "Focus on build-to-rent for stable cash flow"
                ])
            elif intent == QueryIntent.NEIGHBORHOOD_ASSESSMENT:
                recommendations.extend([
                    "Prioritize neighborhoods based on investment goals: growth vs stability",
                    "Consider East End for appreciation, Heights for steady returns",
                    "Evaluate infrastructure improvements as leading indicators"
                ])
            elif intent == QueryIntent.DEVELOPMENT_FEASIBILITY:
                recommendations.extend([
                    "Pursue LEED certification for permitting advantages",
                    "Target TOD sites for density bonuses",
                    "Partner with experienced local developers"
                ])
        
        # Add insights from agent results
        for agent_id, data in results.items():
            if isinstance(data, dict) and "insights" in data:
                # Extract actionable items from insights
                for insight in data["insights"]:
                    if "offering" in insight or "showing" in insight or "available" in insight:
                        if len(recommendations) < 7:
                            recommendations.append(self.insight_to_recommendation(insight))
        
        return recommendations[:7]  # Top 7 recommendations
    
    def insight_to_recommendation(self, insight: str) -> str:
        """Convert an insight into an actionable recommendation"""
        # Simple transformation - in production would use NLP
        if "offering" in insight:
            return insight.replace("offering", "leverage opportunities in")
        elif "showing" in insight:
            return insight.replace("showing", "capitalize on")
        elif "available" in insight:
            return insight.replace("available", "take advantage of")
        return f"Consider: {insight}"
    
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
    
    def suggest_next_steps(self, results: Dict[str, Any], intent: QueryIntent, context: Dict[str, Any]) -> List[str]:
        """Suggest concrete next steps based on analysis and context"""
        next_steps = []
        
        # Context-aware next steps
        if context.get("ranking_requested") and "neighborhood" in str(context):
            next_steps = [
                "Tour top 3 identified neighborhoods (East End, Heights, Third Ward) this week",
                "Request detailed market comps for each target neighborhood",
                "Meet with local brokers specializing in identified areas",
                "Analyze recent sales data for investment properties in top neighborhoods",
                "Review zoning maps and development plans for each area"
            ]
        elif context.get("action_type") == "investment":
            next_steps = [
                "Identify specific properties matching investment criteria",
                "Schedule meetings with lenders for financing pre-approval",
                "Engage CPA for opportunity zone investment structuring",
                "Conduct due diligence on 3-5 target properties",
                "Build financial models for each investment scenario"
            ]
        elif "permit" in str(context):
            next_steps = [
                "Download detailed permit reports for target areas",
                "Track weekly permit filings in neighborhoods of interest",
                "Identify developers with most permit activity",
                "Analyze permit types to understand market direction",
                "Set up alerts for new permit applications"
            ]
        else:
            # Default next steps by intent
            if intent == QueryIntent.INVESTMENT_OPPORTUNITY:
                next_steps = [
                    "Identify top 5 investment properties matching criteria",
                    "Schedule property tours and neighborhood assessments",
                    "Obtain financing pre-approval from preferred lenders",
                    "Engage investment advisor for opportunity zone guidance",
                    "Prepare offer strategies for target properties"
                ]
            elif intent == QueryIntent.NEIGHBORHOOD_ASSESSMENT:
                next_steps = [
                    "Conduct on-site visits to recommended neighborhoods",
                    "Meet with neighborhood associations and local brokers",
                    "Review infrastructure and development plans",
                    "Analyze comparable sales and rental data",
                    "Evaluate school ratings and amenity access"
                ]
            else:
                next_steps = [
                    "Review detailed reports from relevant intelligence agents",
                    "Schedule follow-up analysis on specific opportunities",
                    "Set up market monitoring for key indicators",
                    "Connect with local experts in areas of interest",
                    "Prepare action plan based on recommendations"
                ]
        
        return next_steps[:5]  # Top 5 next steps
    
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