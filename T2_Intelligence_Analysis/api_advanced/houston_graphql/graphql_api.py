"""
GraphQL API for Houston Intelligence Platform
Provides flexible querying alongside REST API
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from strawberry.permission import BasePermission
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import asyncio
from dataclasses import dataclass


# GraphQL Types
@strawberry.type
class Metric:
    """Individual metric data"""
    name: str
    value: float
    unit: Optional[str] = None
    change_percentage: Optional[float] = None
    trend: Optional[str] = None


@strawberry.type
class KeyFinding:
    """Key finding from analysis"""
    finding: str
    importance: str
    domain: str
    confidence: float


@strawberry.type
class Opportunity:
    """Investment opportunity"""
    type: str
    potential: str
    description: str
    location: Optional[str] = None
    action: str
    expected_roi: Optional[float] = None


@strawberry.type
class Risk:
    """Risk assessment"""
    type: str
    severity: str
    description: str
    mitigation: str
    financial_impact: Optional[str] = None
    probability: Optional[float] = None


@strawberry.type
class DomainAnalysis:
    """Domain-specific analysis results"""
    domain: str
    confidence_score: float
    timestamp: str
    key_findings: List[KeyFinding]
    opportunities: List[Opportunity]
    risks: List[Risk]
    metrics: List[Metric]
    recommendations: List[str]


@strawberry.type
class CrossDomainInsight:
    """Cross-domain analysis insight"""
    domains: List[str]
    insight_type: str
    description: str
    synergy_score: float
    value_potential: str
    action_items: List[str]


@strawberry.type
class MarketSnapshot:
    """Current market snapshot"""
    timestamp: str
    overall_confidence: float
    market_sentiment: str
    top_opportunities: List[Opportunity]
    critical_risks: List[Risk]
    trending_areas: List[str]
    key_metrics: List[Metric]


@strawberry.type
class NeighborhoodProfile:
    """Detailed neighborhood profile"""
    name: str
    overall_score: float
    investment_grade: str
    price_growth: float
    inventory_months: float
    days_on_market: int
    demographic_profile: str  # JSON string representation
    infrastructure_score: float
    growth_drivers: List[str]
    opportunities: List[Opportunity]
    risks: List[Risk]


@strawberry.type
class IntelligenceUpdate:
    """Real-time intelligence update"""
    update_id: str
    update_type: str
    domain: str
    timestamp: str
    priority: str
    data: str  # JSON string representation
    confidence: float


@strawberry.type
class BatchQueryStatus:
    """Batch query status"""
    batch_id: str
    status: str
    total_queries: int
    completed_queries: int
    failed_queries: int
    progress_percentage: float
    estimated_completion: Optional[str] = None


@strawberry.type
class PredictiveAnalysis:
    """Predictive analysis results"""
    domain: str
    prediction_horizon: str
    scenarios: str  # JSON string representation
    confidence_intervals: str  # JSON string representation
    key_drivers: List[str]
    recommendations: List[str]


# Input Types
@strawberry.input
class DomainFilter:
    """Filter for domain queries"""
    domains: Optional[List[str]] = None
    min_confidence: Optional[float] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


@strawberry.input
class MetricFilter:
    """Filter for metric queries"""
    metric_names: Optional[List[str]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    trend: Optional[str] = None


@strawberry.input
class LocationFilter:
    """Filter for location-based queries"""
    neighborhoods: Optional[List[str]] = None
    min_score: Optional[float] = None
    investment_grade: Optional[str] = None


@strawberry.input
class AnalysisRequest:
    """Request for new analysis"""
    domain: str
    analysis_type: str
    parameters: Optional[str] = None  # JSON string representation
    priority: Optional[int] = 5


# Permissions
class IsAuthenticated(BasePermission):
    """Check if user is authenticated"""
    message = "User is not authenticated"
    
    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        # In production, implement proper authentication
        return True  # Simplified for demo


# Data Service
class IntelligenceDataService:
    """Service for accessing intelligence data"""
    
    def __init__(self):
        self.data_path = Path("/Users/fernandox/Desktop/Core Agent Architecture/shared_state/t2_analysis")
        self._cache = {}
    
    async def get_domain_analysis(self, domain: str) -> Optional[DomainAnalysis]:
        """Get latest domain analysis"""
        # Look for latest analysis file
        analysis_files = list(self.data_path.glob(f"{domain}_analysis_*.json"))
        if not analysis_files:
            return None
        
        latest_file = max(analysis_files, key=lambda f: f.stat().st_mtime)
        
        # Load and parse
        with open(latest_file, 'r') as f:
            data = json.load(f)
        
        # Convert to GraphQL type
        return DomainAnalysis(
            domain=domain,
            confidence_score=data.get("confidence_score", 0),
            timestamp=data.get("timestamp", ""),
            key_findings=[
                KeyFinding(
                    finding=f,
                    importance="high",
                    domain=domain,
                    confidence=data.get("confidence_score", 0)
                )
                for f in data.get("key_findings", [])
            ],
            opportunities=[
                Opportunity(
                    type=opp.get("type", ""),
                    potential=opp.get("potential", ""),
                    description=opp.get("description", ""),
                    location=opp.get("location"),
                    action=opp.get("action", ""),
                    expected_roi=opp.get("projected_roi")
                )
                for opp in data.get("opportunities", [])
            ],
            risks=[
                Risk(
                    type=risk.get("type", ""),
                    severity=risk.get("severity", ""),
                    description=risk.get("description", ""),
                    mitigation=risk.get("mitigation", ""),
                    financial_impact=risk.get("financial_impact")
                )
                for risk in data.get("risks", [])
            ],
            metrics=[
                Metric(
                    name=k,
                    value=v,
                    unit=self._infer_unit(k)
                )
                for k, v in data.get("metrics", {}).items()
                if isinstance(v, (int, float))
            ],
            recommendations=data.get("recommendations", [])
        )
    
    async def get_all_domains(self, filter: Optional[DomainFilter] = None) -> List[DomainAnalysis]:
        """Get analysis for all domains with optional filter"""
        domains = ["market", "neighborhood", "financial", "environmental", "regulatory", "technology"]
        
        if filter and filter.domains:
            domains = [d for d in domains if d in filter.domains]
        
        analyses = []
        for domain in domains:
            analysis = await self.get_domain_analysis(domain)
            if analysis:
                # Apply filters
                if filter:
                    if filter.min_confidence and analysis.confidence_score < filter.min_confidence:
                        continue
                    # Add more filter logic as needed
                analyses.append(analysis)
        
        return analyses
    
    async def get_cross_domain_insights(self) -> List[CrossDomainInsight]:
        """Get cross-domain insights"""
        # Load cross-domain analysis
        cross_domain_files = list(self.data_path.glob("cross_domain_analysis_*.json"))
        if not cross_domain_files:
            return []
        
        latest_file = max(cross_domain_files, key=lambda f: f.stat().st_mtime)
        
        with open(latest_file, 'r') as f:
            data = json.load(f)
        
        insights = []
        
        # Parse strategic intersections
        for intersection in data.get("strategic_intersections", []):
            insights.append(CrossDomainInsight(
                domains=intersection.get("domains", []),
                insight_type=intersection.get("type", ""),
                description=intersection.get("description", ""),
                synergy_score=85.0,  # Default if not provided
                value_potential=intersection.get("value_potential", ""),
                action_items=[intersection.get("opportunity", "")]
            ))
        
        # Parse value creation matrix
        value_matrix = data.get("value_creation_matrix", {})
        for combo in value_matrix.get("high_value_combinations", []):
            insights.append(CrossDomainInsight(
                domains=combo.get("domains", []),
                insight_type="value_combination",
                description=combo.get("opportunity", ""),
                synergy_score=combo.get("score", 0),
                value_potential="High",
                action_items=["Leverage domain synergies"]
            ))
        
        return insights
    
    async def get_market_snapshot(self) -> MarketSnapshot:
        """Get current market snapshot"""
        # Aggregate data from multiple domains
        all_analyses = await self.get_all_domains()
        
        # Compile snapshot
        all_opportunities = []
        all_risks = []
        all_metrics = []
        
        for analysis in all_analyses:
            all_opportunities.extend(analysis.opportunities)
            all_risks.extend(analysis.risks)
            all_metrics.extend(analysis.metrics)
        
        # Sort and filter
        top_opportunities = sorted(
            all_opportunities,
            key=lambda x: x.expected_roi or 0,
            reverse=True
        )[:5]
        
        critical_risks = [r for r in all_risks if r.severity in ["high", "critical"]][:5]
        
        # Determine market sentiment
        avg_confidence = sum(a.confidence_score for a in all_analyses) / len(all_analyses) if all_analyses else 0
        sentiment = "bullish" if avg_confidence > 0.85 else "neutral" if avg_confidence > 0.7 else "bearish"
        
        return MarketSnapshot(
            timestamp=datetime.now().isoformat(),
            overall_confidence=avg_confidence,
            market_sentiment=sentiment,
            top_opportunities=top_opportunities,
            critical_risks=critical_risks,
            trending_areas=["EaDo", "Ion District", "Midtown"],  # Placeholder
            key_metrics=all_metrics[:10]
        )
    
    async def get_neighborhood_profile(self, name: str) -> Optional[NeighborhoodProfile]:
        """Get detailed neighborhood profile"""
        # Load neighborhood analysis
        neighborhood_analysis = await self.get_domain_analysis("neighborhood")
        if not neighborhood_analysis:
            return None
        
        # Find specific neighborhood data (simplified)
        return NeighborhoodProfile(
            name=name,
            overall_score=75.5,
            investment_grade="B+",
            price_growth=12.5,
            inventory_months=2.5,
            days_on_market=25,
            demographic_profile=json.dumps({
                "median_income": 85000,
                "population_growth": 3.5,
                "median_age": 32
            }),
            infrastructure_score=8.5,
            growth_drivers=["Tech sector growth", "Transit improvements"],
            opportunities=[
                Opportunity(
                    type="growth_market",
                    potential="high",
                    description=f"Strong growth in {name}",
                    location=name,
                    action="Acquire properties",
                    expected_roi=22.5
                )
            ],
            risks=[]
        )
    
    async def run_predictive_analysis(self, domain: str, horizon: str) -> PredictiveAnalysis:
        """Run predictive analysis for domain"""
        # Simulate predictive analysis
        await asyncio.sleep(1)  # Simulate processing
        
        return PredictiveAnalysis(
            domain=domain,
            prediction_horizon=horizon,
            scenarios=json.dumps({
                "optimistic": {"roi": 25.5, "growth": 15.2},
                "base": {"roi": 18.3, "growth": 10.5},
                "pessimistic": {"roi": 12.1, "growth": 5.8}
            }),
            confidence_intervals=json.dumps({
                "roi": {"lower": 12.1, "upper": 25.5},
                "growth": {"lower": 5.8, "upper": 15.2}
            }),
            key_drivers=[
                "Interest rates",
                "Population growth",
                "Tech sector expansion"
            ],
            recommendations=[
                f"Focus on {domain} opportunities",
                "Maintain portfolio flexibility",
                "Monitor leading indicators"
            ]
        )
    
    def _infer_unit(self, metric_name: str) -> Optional[str]:
        """Infer unit from metric name"""
        if "rate" in metric_name or "pct" in metric_name or "percentage" in metric_name:
            return "%"
        elif "price" in metric_name or "cost" in metric_name or "value" in metric_name:
            return "$"
        elif "days" in metric_name or "months" in metric_name or "years" in metric_name:
            return "time"
        elif "score" in metric_name:
            return "points"
        return None


# GraphQL Query and Mutation
@strawberry.type
class Query:
    """GraphQL queries"""
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def domain_analysis(
        self,
        info: Info,
        domain: str
    ) -> Optional[DomainAnalysis]:
        """Get analysis for a specific domain"""
        service = info.context["intelligence_service"]
        return await service.get_domain_analysis(domain)
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def all_domains(
        self,
        info: Info,
        filter: Optional[DomainFilter] = None
    ) -> List[DomainAnalysis]:
        """Get analysis for all domains"""
        service = info.context["intelligence_service"]
        return await service.get_all_domains(filter)
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def cross_domain_insights(
        self,
        info: Info
    ) -> List[CrossDomainInsight]:
        """Get cross-domain insights"""
        service = info.context["intelligence_service"]
        return await service.get_cross_domain_insights()
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def market_snapshot(
        self,
        info: Info
    ) -> MarketSnapshot:
        """Get current market snapshot"""
        service = info.context["intelligence_service"]
        return await service.get_market_snapshot()
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def neighborhood_profile(
        self,
        info: Info,
        name: str
    ) -> Optional[NeighborhoodProfile]:
        """Get detailed neighborhood profile"""
        service = info.context["intelligence_service"]
        return await service.get_neighborhood_profile(name)
    
    @strawberry.field
    async def search_opportunities(
        self,
        info: Info,
        min_roi: Optional[float] = None,
        location: Optional[str] = None,
        potential: Optional[str] = None
    ) -> List[Opportunity]:
        """Search for opportunities based on criteria"""
        service = info.context["intelligence_service"]
        all_domains = await service.get_all_domains()
        
        opportunities = []
        for domain in all_domains:
            for opp in domain.opportunities:
                # Apply filters
                if min_roi and (not opp.expected_roi or opp.expected_roi < min_roi):
                    continue
                if location and opp.location != location:
                    continue
                if potential and opp.potential != potential:
                    continue
                opportunities.append(opp)
        
        return opportunities
    
    @strawberry.field
    async def risk_assessment(
        self,
        info: Info,
        severity: Optional[str] = None,
        domain: Optional[str] = None
    ) -> List[Risk]:
        """Get risk assessment"""
        service = info.context["intelligence_service"]
        
        if domain:
            analysis = await service.get_domain_analysis(domain)
            risks = analysis.risks if analysis else []
        else:
            all_domains = await service.get_all_domains()
            risks = []
            for analysis in all_domains:
                risks.extend(analysis.risks)
        
        # Apply severity filter
        if severity:
            risks = [r for r in risks if r.severity == severity]
        
        return risks


@strawberry.type
class Mutation:
    """GraphQL mutations"""
    
    @strawberry.mutation
    async def request_analysis(
        self,
        info: Info,
        request: AnalysisRequest
    ) -> str:
        """Request new analysis"""
        # In production, this would trigger actual analysis
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.domain}"
        
        # Queue analysis request
        # ... implementation ...
        
        return analysis_id
    
    @strawberry.mutation
    async def run_predictive_analysis(
        self,
        info: Info,
        domain: str,
        horizon: str = "6_months"
    ) -> PredictiveAnalysis:
        """Run predictive analysis"""
        service = info.context["intelligence_service"]
        return await service.run_predictive_analysis(domain, horizon)
    
    @strawberry.mutation
    async def subscribe_to_updates(
        self,
        info: Info,
        domains: List[str],
        update_types: List[str]
    ) -> bool:
        """Subscribe to real-time updates"""
        # In production, this would set up WebSocket subscriptions
        return True


@strawberry.type
class Subscription:
    """GraphQL subscriptions for real-time updates"""
    
    @strawberry.subscription
    async def intelligence_updates(
        self,
        info: Info,
        domains: Optional[List[str]] = None
    ) -> IntelligenceUpdate:
        """Subscribe to intelligence updates"""
        # Simulate real-time updates
        update_count = 0
        while True:
            await asyncio.sleep(10)  # Update every 10 seconds
            
            update_count += 1
            domain = domains[0] if domains else "market"
            
            yield IntelligenceUpdate(
                update_id=f"update_{update_count}",
                update_type="metric_change",
                domain=domain,
                timestamp=datetime.now().isoformat(),
                priority="normal",
                data=json.dumps({
                    "metric": "market_activity",
                    "old_value": 100,
                    "new_value": 100 + (update_count % 10)
                }),
                confidence=0.95
            )


# Create GraphQL schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)

# FastAPI app
app = FastAPI(title="Houston Intelligence GraphQL API")

# Security
security = HTTPBearer()

# Context dependency
async def get_context(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get GraphQL context"""
    # In production, validate token and get user
    return {
        "intelligence_service": IntelligenceDataService(),
        "user": {"id": "user123", "role": "analyst"}
    }

# Add GraphQL route
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app.include_router(graphql_app, prefix="/graphql")

# Add GraphQL playground (for development)
@app.get("/")
async def graphql_playground():
    """Redirect to GraphQL playground"""
    return {"message": "Visit /graphql for GraphQL playground"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)