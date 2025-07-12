#!/usr/bin/env python3
"""
Run T2 Analytical Agent
Process T1 extractions and generate analytical insights
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.t2_analytical_agent import T2AnalyticalAgent


async def process_single_file():
    """Process a single T1 extraction file"""
    agent = T2AnalyticalAgent()
    
    # Process both test files
    t1_files = [
        Path("/Users/fernandox/Desktop/Core Agent Architecture/shared_state/t1_extractions/t1-2025-01-10-permit-data.json"),
        Path("/Users/fernandox/Desktop/Core Agent Architecture/shared_state/t1_extractions/t1-2025-01-10-property-data.json")
    ]
    
    for t1_file in t1_files:
        if t1_file.exists():
            print(f"\n{'='*60}")
            print(f"Processing T1 extraction: {t1_file.name}")
            print('='*60)
            analysis = await agent.process_t1_data(t1_file)
            
            if analysis:
                print(f"\nAnalysis Complete!")
                print(f"Analysis ID: {analysis.analysis_id}")
                print(f"Confidence Score: {analysis.confidence_score:.2%}")
                print(f"Processing Time: {analysis.processing_time_ms}ms")
                
                print("\nKey Metrics:")
                for metric, value in list(analysis.metrics.calculated_values.items())[:5]:
                    if isinstance(value, float):
                        print(f"  - {metric}: {value:,.2f}")
                    else:
                        print(f"  - {metric}: {value}")
                
                print("\nInsights:")
                for insight in analysis.insights:
                    print(f"  • {insight}")
                
                print("\nAnomalies Detected:")
                if analysis.metrics.anomalies:
                    for anomaly in analysis.metrics.anomalies[:3]:
                        print(f"  ⚠️ {anomaly['type']}: {anomaly.get('description', 'See details in analysis')}")
                else:
                    print("  ✓ No significant anomalies detected")
                
                print(f"\nAnalysis saved to: shared_state/t2_analysis/{analysis.analysis_id}.json")
            else:
                print("Failed to process T1 data")
        else:
            print(f"T1 file not found: {t1_file}")


async def run_continuous_monitoring():
    """Run T2 agent in continuous monitoring mode"""
    agent = T2AnalyticalAgent()
    
    print("Starting T2 Analytical Agent in monitoring mode...")
    print("Monitoring for new T1 extractions...")
    print("Press Ctrl+C to stop\n")
    
    try:
        await agent.monitor_t1_extractions()
    except KeyboardInterrupt:
        print("\nStopping T2 agent...")


async def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        await run_continuous_monitoring()
    else:
        await process_single_file()


if __name__ == "__main__":
    asyncio.run(main())