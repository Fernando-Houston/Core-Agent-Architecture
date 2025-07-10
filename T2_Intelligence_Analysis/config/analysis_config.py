"""
T2 Intelligence Analysis Configuration
"""

# Domain configurations with analysis priorities
DOMAIN_CONFIG = {
    "market_intelligence": {
        "priority": "high",
        "analysis_modules": [
            "competitive_landscape",
            "pricing_trends", 
            "market_forecasts",
            "developer_strategies"
        ],
        "key_metrics": [
            "market_share",
            "price_per_sqft",
            "absorption_rates",
            "pipeline_volume"
        ]
    },
    "neighborhood_intelligence": {
        "priority": "high",
        "analysis_modules": [
            "area_demographics",
            "growth_patterns",
            "development_hotspots",
            "infrastructure_impact"
        ],
        "key_metrics": [
            "population_growth",
            "median_income",
            "property_values",
            "permit_activity"
        ]
    },
    "financial_intelligence": {
        "priority": "high",
        "analysis_modules": [
            "roi_analysis",
            "financing_options",
            "investment_trends",
            "risk_assessment"
        ],
        "key_metrics": [
            "cap_rates",
            "irr_projections",
            "lending_rates",
            "investment_volume"
        ]
    },
    "environmental_intelligence": {
        "priority": "medium",
        "analysis_modules": [
            "flood_risk_assessment",
            "environmental_compliance",
            "sustainability_metrics",
            "climate_impact"
        ],
        "key_metrics": [
            "flood_zones",
            "air_quality_index",
            "green_certifications",
            "mitigation_costs"
        ]
    },
    "regulatory_intelligence": {
        "priority": "medium",
        "analysis_modules": [
            "zoning_analysis",
            "permit_tracking",
            "compliance_requirements",
            "policy_changes"
        ],
        "key_metrics": [
            "permit_approval_times",
            "zoning_changes",
            "compliance_rates",
            "regulatory_costs"
        ]
    },
    "technology_intelligence": {
        "priority": "medium",
        "analysis_modules": [
            "innovation_districts",
            "tech_adoption",
            "smart_city_initiatives",
            "proptech_trends"
        ],
        "key_metrics": [
            "tech_employment",
            "innovation_index",
            "smart_building_adoption",
            "tech_investment"
        ]
    }
}

# Analysis thresholds and parameters
ANALYSIS_PARAMS = {
    "confidence_threshold": 0.85,
    "min_data_points": 10,
    "trend_window_days": 90,
    "forecast_horizon_months": 12,
    "risk_categories": ["low", "medium", "high", "critical"],
    "opportunity_score_range": (0, 100)
}

# Output formats
OUTPUT_FORMATS = {
    "intelligence_report": {
        "sections": [
            "executive_summary",
            "key_findings",
            "market_insights",
            "risk_assessment",
            "opportunities",
            "recommendations",
            "data_appendix"
        ]
    },
    "agent_payload": {
        "format": "json",
        "schema_version": "1.0"
    }
}

# Shared state paths
SHARED_STATE_PATH = "/Users/fernandox/Desktop/Core Agent Architecture/shared_state"
T1_EXTRACTIONS_PATH = f"{SHARED_STATE_PATH}/t1_extractions"
T2_OUTPUTS_PATH = f"{SHARED_STATE_PATH}/t2_analysis"
T3_QUEUE_PATH = f"{SHARED_STATE_PATH}/t3_agent_queue"