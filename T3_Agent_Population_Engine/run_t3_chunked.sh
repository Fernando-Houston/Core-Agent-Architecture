#!/bin/bash

echo "T3 Agent Population Engine - Chunked Processing"
echo "=============================================="
echo ""

BASE_DIR="/Users/fernandox/Desktop/Core Agent Architecture"
T3_DIR="$BASE_DIR/T3_Agent_Population_Engine"

# Create sample T2 files for testing if needed
T2_DIR="$BASE_DIR/T2_Intelligence_Output"
mkdir -p "$T2_DIR"

# Check if we have T2 files
if [ ! -f "$T2_DIR/sample_t2_analysis.json" ]; then
    echo "Creating additional sample T2 file..."
    cat > "$T2_DIR/neighborhood_analysis_t2.json" << 'EOF'
{
  "analysis_id": "t2_neighborhood_001",
  "timestamp": "2024-01-10T11:00:00Z",
  "insights": [
    {
      "domain": "houston_heights",
      "category": "investment_analysis",
      "title": "Houston Heights Investment Score Analysis",
      "content": {
        "summary": "Heights shows strong investment potential with 85/100 score",
        "key_findings": [
          "15% annual appreciation over past 3 years",
          "Strong demographic growth",
          "Major infrastructure improvements planned"
        ],
        "metrics": {
          "investment_score": 85,
          "growth_rate": 15,
          "median_income": 95000,
          "development_projects": 12
        }
      },
      "tags": ["investment", "neighborhood", "houston-heights"],
      "confidence_score": 0.9
    },
    {
      "domain": "katy_area",
      "category": "development_opportunities",
      "title": "Katy Area Development Pipeline",
      "content": {
        "summary": "Significant development opportunities in Katy expansion areas",
        "key_findings": [
          "2000+ acres available for development",
          "New master-planned communities",
          "Commercial development opportunities"
        ],
        "metrics": {
          "available_acres": 2000,
          "planned_units": 5000,
          "commercial_sqft": 500000
        }
      },
      "tags": ["development", "opportunities", "katy"],
      "confidence_score": 0.88
    }
  ]
}
EOF

    cat > "$T2_DIR/financial_analysis_t2.json" << 'EOF'
{
  "analysis_id": "t2_financial_001",
  "timestamp": "2024-01-10T11:30:00Z",
  "insights": [
    {
      "domain": "financing_options",
      "category": "roi_models",
      "title": "Mixed-Use Development ROI Model",
      "content": {
        "summary": "Comprehensive ROI model for mixed-use developments",
        "key_findings": [
          "18-22% projected returns",
          "3-year break-even period",
          "Multiple financing options available"
        ],
        "metrics": {
          "projected_roi": 20,
          "break_even_months": 36,
          "initial_investment": 5000000
        }
      },
      "tags": ["roi", "financial", "mixed-use"],
      "confidence_score": 0.85
    },
    {
      "domain": "tax_implications",
      "category": "tax_strategies",
      "title": "Opportunity Zone Tax Benefits",
      "content": {
        "summary": "Tax optimization through opportunity zone investments",
        "key_findings": [
          "Capital gains deferral until 2026",
          "10% basis increase after 5 years",
          "Tax-free appreciation after 10 years"
        ],
        "recommendations": [
          "Structure investments through qualified opportunity funds",
          "Focus on long-term hold strategies",
          "Combine with other tax incentives"
        ]
      },
      "tags": ["tax", "opportunity-zone", "incentives"],
      "confidence_score": 0.92
    }
  ]
}
EOF
fi

echo "Starting T3 Chunked Processor..."
echo ""

cd "$T3_DIR"
python3 t3_chunked_processor.py
