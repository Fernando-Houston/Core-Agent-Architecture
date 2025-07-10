# T2 Intelligence Analysis Engine

## Overview
T2 is the Intelligence Analysis Engine that transforms T1's extracted data into sophisticated market insights, competitive analysis, and actionable intelligence for Houston's real estate development market.

## Architecture

### Core Components

1. **T1 Monitor** (`monitoring/t1_monitor.py`)
   - Monitors T1 extraction completions
   - Prioritizes domains for analysis
   - Manages processing queue

2. **Base Analyzer** (`analysis_engines/base_analyzer.py`)
   - Foundation for all domain analyzers
   - Standardized analysis pipeline
   - Quality assessment and confidence scoring

3. **Domain Analyzers**
   - Market Intelligence (implemented)
   - Neighborhood Intelligence (pending)
   - Financial Intelligence (pending)
   - Environmental Intelligence (pending)
   - Regulatory Intelligence (pending)
   - Technology Intelligence (pending)

4. **Main Engine** (`t2_main.py`)
   - Orchestrates analysis pipeline
   - Manages analyzer instances
   - Coordinates with T3

## Analysis Capabilities

### Market Intelligence
- Competitive landscape analysis
- Pricing trends and forecasts
- Market dynamics (supply/demand)
- Developer strategy insights
- Risk and opportunity identification

### Key Features
- **Confidence Scoring**: Each analysis includes confidence metrics
- **Data Quality Assessment**: Validates T1 extraction quality
- **Prioritized Processing**: High-priority domains processed first
- **Real-time Monitoring**: Continuous monitoring of T1 completions

## Output Structure

Each analysis produces:
```json
{
  "domain": "market_intelligence",
  "timestamp": "2024-01-10T10:30:00",
  "confidence_score": 0.92,
  "key_findings": ["..."],
  "insights": {...},
  "risks": [...],
  "opportunities": [...],
  "recommendations": [...],
  "metrics": {...},
  "data_quality_score": 0.95
}
```

## Running T2

```bash
cd /Users/fernandox/Desktop/Core\ Agent\ Architecture/T2_Intelligence_Analysis
python t2_main.py
```

## Status Monitoring

T2 status available at:
- Status file: `shared_state/t2_analysis_status.json`
- Logs: `T2_Intelligence_Analysis/logs/`
- Outputs: `shared_state/t2_analysis/`

## Integration Points

- **Input**: Monitors `shared_state/t1_extraction_status.json`
- **Output**: Queues results in `shared_state/t3_agent_queue/`
- **Coordination**: Real-time status updates for system monitoring