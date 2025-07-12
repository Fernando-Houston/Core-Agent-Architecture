"""
T4 Market Intelligence Agent Configuration
Premium market intelligence processing configuration for 2024-2025 data
"""

import os
from datetime import datetime

# T4 Agent System Prompt
T4_AGENT_PROMPT = """
You are T4-Market-Intelligence-Agent, the premium market intelligence tier of the Houston 
Intelligence Platform. Your role is to process and serve sophisticated 2024-2025 market intelligence 
data.

PRIMARY RESPONSIBILITIES:
1. Process premium market research reports and financial analyses
2. Extract quantitative metrics from narrative market intelligence
3. Identify investment opportunities with specific parameters
4. Analyze demographic and economic trends affecting real estate
5. Provide construction finance and cost inflation insights
6. Track capital flows and institutional investment patterns

DATA SOURCES:
- 2024-2025 Construction Finance & Delivery Outlook
- Climate-Resilient Houston analysis
- Capital Flows reports ($12.4B tracked investments)
- Education & Real Estate correlations
- Generational Housing Shifts & Demographics
- Green Building Incentives
- Healthcare Real Estate Outlook
- Industrial Real Estate Landscape
- Retail & Sports-Driven Development
- Infrastructure updates (Power, Pipes, Water)

OUTPUT FORMAT:
{
    "intelligence_id": "t4-YYYY-MM-DD-XXXXX",
    "report_sources": ["report names"],
    "market_metrics": {
        "financial_indicators": {},
        "investment_opportunities": [],
        "market_forecasts": {},
        "risk_factors": []
    },
    "quantitative_data": {
        "cap_rates": {},
        "roi_projections": {},
        "cost_estimates": {},
        "demographic_trends": {}
    },
    "actionable_insights": ["specific recommendations"],
    "confidence_score": 0.95,
    "data_vintage": "2024-2025",
    "timestamp": "ISO-8601"
}

SPECIALIZED CAPABILITIES:
- Construction loan rates and financing terms (SOFR + spreads)
- Impact fee analysis by municipality
- Opportunity Zone investment tracking
- Pension fund allocation patterns
- Foreign capital flows by country
- Labor shortage impact on construction timelines
- Climate resilience factors for property valuation
- Demographic shifts affecting housing demand

ANALYTICAL PRIORITIES:
1. Financial Metrics: IRR, cap rates, loan terms, construction costs
2. Market Timing: Supply pipeline, absorption rates, price trends
3. Risk Assessment: Climate, regulatory, market cycle, construction
4. Opportunity Identification: Undervalued areas, emerging trends
5. Comparative Analysis: Neighborhood vs neighborhood, Houston vs peers

Remember: You provide institutional-grade market intelligence. Be precise with numbers, cite specific
data points, and focus on actionable financial insights. Your data is premium 2024-2025 content - 
highlight its currency and relevance.
"""

# T4 Agent Configuration
T4_CONFIG = {
    "agent_id": "T4-Market-Intelligence",
    "version": "1.0.0",
    "data_vintage": "2024-2025",
    
    # Data sources configuration
    "data_sources": {
        "primary_folder": "Data Processing Part 2",
        "report_categories": [
            "Construction Finance and Delivery Outlook",
            "Climate-Resilient Houston",
            "Capital Currents",
            "Education Real Estate",
            "Generational Housing Shifts",
            "Green Building Incentives",
            "Health-Care Real Estate",
            "Industrial Real Estate",
            "Retail Real Estate",
            "Infrastructure"
        ]
    },
    
    # Processing configuration
    "processing": {
        "markdown_extensions": [".md", ".markdown"],
        "chart_extensions": [".png", ".jpg", ".jpeg"],
        "data_extensions": [".csv", ".xlsx"],
        "script_extensions": [".py"],
        "batch_size": 10,
        "max_file_size_mb": 50
    },
    
    # Financial metrics extraction patterns
    "financial_patterns": {
        "cap_rate": r"(\d+\.?\d*)\s*%?\s*cap\s*rate",
        "roi": r"(\d+\.?\d*)\s*%?\s*(?:roi|return)",
        "irr": r"(\d+\.?\d*)\s*%?\s*irr",
        "price_psf": r"\$(\d+\.?\d*)\s*(?:per|psf|/sf)",
        "loan_rate": r"(?:SOFR|sofr)\s*\+\s*(\d+\.?\d*)",
        "construction_cost": r"\$(\d+\.?\d*)\s*(?:million|M|billion|B)\s*(?:construction|development)"
    },
    
    # Market intelligence categories
    "intelligence_categories": {
        "financial": ["cap_rates", "roi", "irr", "financing", "investment"],
        "market": ["supply", "demand", "absorption", "vacancy", "trends"],
        "risk": ["climate", "regulatory", "market_cycle", "construction"],
        "opportunity": ["undervalued", "emerging", "growth", "development"],
        "demographic": ["population", "employment", "income", "age", "migration"]
    },
    
    # Output configuration
    "output": {
        "base_path": "T4_Market_Intelligence_Agent/output",
        "structured_data": "structured_intelligence",
        "raw_extracts": "raw_extracts",
        "visualizations": "processed_visualizations",
        "reports": "intelligence_reports"
    },
    
    # Integration settings
    "integration": {
        "t2_queue_path": "shared_state/t4_to_t2_queue",
        "t3_update_path": "shared_state/t4_knowledge_updates",
        "processing_status": "shared_state/t4_processing_status.json"
    },
    
    # Quality thresholds
    "quality": {
        "min_confidence_score": 0.85,
        "min_data_points": 3,
        "max_data_age_days": 365
    }
}

# Report mapping to intelligence domains
REPORT_TO_DOMAIN_MAPPING = {
    "Construction Finance and Delivery Outlook": "financial_intelligence",
    "Climate-Resilient Houston": "environmental_intelligence",
    "Capital Currents": "financial_intelligence",
    "Education Real Estate": "market_intelligence",
    "Generational Housing Shifts": "neighborhood_intelligence",
    "Green Building Incentives": "environmental_intelligence",
    "Health-Care Real Estate": "market_intelligence",
    "Industrial Real Estate": "market_intelligence",
    "Retail Real Estate": "market_intelligence",
    "Infrastructure": "technology_intelligence"
}

# Metric extraction priorities
METRIC_PRIORITIES = {
    "high": [
        "cap_rates",
        "construction_costs",
        "loan_rates",
        "investment_volumes",
        "absorption_rates"
    ],
    "medium": [
        "demographic_trends",
        "supply_pipeline",
        "vacancy_rates",
        "rental_rates"
    ],
    "low": [
        "historical_comparisons",
        "national_benchmarks",
        "qualitative_assessments"
    ]
}