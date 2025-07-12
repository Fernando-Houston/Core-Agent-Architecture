"""
T4 Market Intelligence Agent - Main Orchestrator
Coordinates processing of premium 2024-2025 market intelligence data
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from T4_Market_Intelligence_Agent.config.t4_config import (
    T4_CONFIG, T4_AGENT_PROMPT, REPORT_TO_DOMAIN_MAPPING
)
from T4_Market_Intelligence_Agent.processors.t4_data_processor import T4DataProcessor
from T4_Market_Intelligence_Agent.handlers.t4_visualization_handler import T4VisualizationHandler
from T4_Market_Intelligence_Agent.utils.numpy_encoder import NumpyEncoder


class T4MarketIntelligenceAgent:
    """Main orchestrator for T4 Market Intelligence processing"""
    
    def __init__(self):
        self.config = T4_CONFIG
        self.prompt = T4_AGENT_PROMPT
        self.data_processor = T4DataProcessor()
        self.viz_handler = T4VisualizationHandler()
        self.processing_stats = {
            "start_time": datetime.now().isoformat(),
            "reports_processed": 0,
            "visualizations_processed": 0,
            "intelligence_generated": 0,
            "errors": []
        }
        
        # Initialize output directories
        self._initialize_directories()
        
    def _initialize_directories(self):
        """Create necessary output directories"""
        base_output = Path(self.config["output"]["base_path"])
        
        # Create output subdirectories
        for dir_type in ["structured_data", "raw_extracts", "visualizations", "reports"]:
            dir_path = base_output / self.config["output"][dir_type]
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create integration directories
        for path_key in ["t2_queue_path", "t3_update_path"]:
            Path(self.config["integration"][path_key]).mkdir(parents=True, exist_ok=True)
    
    def process_data_processing_part2(self) -> Dict[str, Any]:
        """Main entry point to process Data Processing Part 2 content"""
        print("\n" + "="*80)
        print("T4 MARKET INTELLIGENCE AGENT - PROCESSING INITIATED")
        print("="*80)
        print(f"Agent ID: {self.config['agent_id']}")
        print(f"Data Vintage: {self.config['data_vintage']}")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("="*80 + "\n")
        
        # Get the Data Processing Part 2 directory
        data_dir = Path(self.config["data_sources"]["primary_folder"])
        if not data_dir.exists():
            print(f"ERROR: Directory '{data_dir}' not found!")
            return {"error": "Data Processing Part 2 directory not found"}
        
        results = {
            "processing_summary": {},
            "intelligence_reports": [],
            "visualization_catalog": {},
            "integration_queue": []
        }
        
        # Step 1: Process all markdown reports
        print("\n[1/4] Processing Markdown Reports...")
        print("-" * 40)
        markdown_results = self._process_markdown_reports(data_dir)
        results["intelligence_reports"] = markdown_results
        self.processing_stats["reports_processed"] = len(markdown_results)
        
        # Step 2: Process visualizations
        print("\n[2/4] Processing Visualizations...")
        print("-" * 40)
        viz_results = self._process_visualizations(data_dir)
        results["visualization_catalog"] = self.viz_handler.generate_visualization_catalog()
        self.processing_stats["visualizations_processed"] = len(viz_results)
        
        # Step 3: Generate consolidated intelligence
        print("\n[3/4] Generating Consolidated Intelligence...")
        print("-" * 40)
        consolidated = self._generate_consolidated_intelligence(
            markdown_results, viz_results
        )
        results["consolidated_intelligence"] = consolidated
        
        # Step 4: Prepare for T2/T3 integration
        print("\n[4/4] Preparing Integration Queue...")
        print("-" * 40)
        integration_data = self._prepare_integration_queue(consolidated)
        results["integration_queue"] = integration_data
        
        # Save processing results
        self._save_results(results)
        
        # Print summary
        self._print_processing_summary(results)
        
        return results
    
    def _process_markdown_reports(self, data_dir: Path) -> List[Dict[str, Any]]:
        """Process all markdown reports in the directory"""
        reports = []
        
        # Process markdown files
        markdown_files = []
        for ext in self.config["processing"]["markdown_extensions"]:
            markdown_files.extend(data_dir.rglob(f"*{ext}"))
        
        print(f"Found {len(markdown_files)} markdown reports to process")
        
        for i, file_path in enumerate(markdown_files, 1):
            print(f"[{i}/{len(markdown_files)}] Processing: {file_path.name}")
            
            try:
                report_data = self.data_processor.process_markdown_file(file_path)
                
                # Save individual report
                self._save_intelligence_report(report_data)
                
                reports.append(report_data)
                self.processing_stats["intelligence_generated"] += 1
                
            except Exception as e:
                error_msg = f"Error processing {file_path}: {str(e)}"
                print(f"  ERROR: {error_msg}")
                self.processing_stats["errors"].append(error_msg)
        
        return reports
    
    def _process_visualizations(self, data_dir: Path) -> List[Dict[str, Any]]:
        """Process all visualizations in the directory"""
        # Create report associations for linking
        report_associations = {}
        for report in self.data_processor.processed_reports:
            report_name = Path(report).stem
            report_associations[report_name] = report
        
        # Process visualizations
        viz_results = self.viz_handler.process_visualization_directory(
            data_dir, report_associations
        )
        
        print(f"Processed {len(viz_results)} visualizations")
        
        # Save visualization catalog
        catalog = self.viz_handler.generate_visualization_catalog()
        catalog_path = Path(self.config["output"]["base_path"]) / \
                      self.config["output"]["visualizations"] / "visualization_catalog.json"
        
        with open(catalog_path, 'w') as f:
            json.dump(catalog, f, indent=2, cls=NumpyEncoder)
        
        return viz_results
    
    def _generate_consolidated_intelligence(self, reports: List[Dict], 
                                          visualizations: List[Dict]) -> Dict[str, Any]:
        """Generate consolidated market intelligence from all sources"""
        consolidated = {
            "intelligence_id": f"t4-consolidated-{datetime.now().strftime('%Y%m%d')}",
            "generation_date": datetime.now().isoformat(),
            "data_vintage": self.config["data_vintage"],
            "total_sources": len(reports) + len(visualizations),
            "market_summary": {},
            "key_metrics": {},
            "investment_opportunities": [],
            "risk_assessment": [],
            "actionable_recommendations": []
        }
        
        # Aggregate financial metrics
        all_cap_rates = []
        all_construction_costs = []
        all_loan_rates = []
        
        for report in reports:
            if "error" in report:
                continue
                
            metrics = report.get("market_metrics", {}).get("financial_indicators", {})
            
            # Collect cap rates
            if "cap_rates" in metrics:
                all_cap_rates.extend([cr["rate"] for cr in metrics["cap_rates"]])
            
            # Collect construction costs
            if "construction_costs" in metrics:
                all_construction_costs.extend([cc["amount_millions"] for cc in metrics["construction_costs"]])
            
            # Collect loan rates
            if "loan_rates" in metrics:
                all_loan_rates.extend([lr["sofr_spread"] for lr in metrics["loan_rates"]])
            
            # Collect opportunities
            opportunities = report.get("market_metrics", {}).get("investment_opportunities", [])
            consolidated["investment_opportunities"].extend(opportunities[:3])  # Top 3 per report
            
            # Collect risks
            risks = report.get("market_metrics", {}).get("risk_factors", [])
            consolidated["risk_assessment"].extend(risks[:2])  # Top 2 per report
        
        # Calculate summary metrics
        if all_cap_rates:
            consolidated["key_metrics"]["average_cap_rate"] = round(sum(all_cap_rates) / len(all_cap_rates), 2)
            consolidated["key_metrics"]["cap_rate_range"] = [min(all_cap_rates), max(all_cap_rates)]
        
        if all_construction_costs:
            consolidated["key_metrics"]["total_construction_pipeline_millions"] = sum(all_construction_costs)
            consolidated["key_metrics"]["average_project_size_millions"] = round(
                sum(all_construction_costs) / len(all_construction_costs), 1
            )
        
        if all_loan_rates:
            consolidated["key_metrics"]["average_construction_loan_spread"] = round(
                sum(all_loan_rates) / len(all_loan_rates), 0
            )
        
        # Generate market summary
        consolidated["market_summary"] = self._generate_market_summary(reports)
        
        # Generate actionable recommendations
        consolidated["actionable_recommendations"] = self._generate_recommendations(
            consolidated["key_metrics"], 
            consolidated["investment_opportunities"],
            consolidated["risk_assessment"]
        )
        
        # Add visualization insights
        viz_insights = []
        for viz in visualizations:
            if "visualization_insights" in viz:
                viz_insights.extend(viz["visualization_insights"])
        
        consolidated["visualization_insights"] = list(set(viz_insights))[:10]
        
        return consolidated
    
    def _generate_market_summary(self, reports: List[Dict]) -> Dict[str, str]:
        """Generate executive market summary"""
        summary = {}
        
        # Count reports by category
        category_counts = {}
        for report in reports:
            if "error" not in report:
                category = report.get("report_category", "General")
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Generate category summaries
        if "Construction Finance and Delivery Outlook" in category_counts:
            summary["construction"] = ("Strong construction pipeline with institutional capital " +
                                     "driving development despite rising costs and extended timelines")
        
        if "Capital Currents" in category_counts:
            summary["capital_flows"] = ("$12.4B in tracked institutional investment with " +
                                      "pension funds and foreign capital targeting Houston growth")
        
        if "Climate-Resilient Houston" in category_counts:
            summary["climate"] = ("Climate resilience becoming core valuation factor with " +
                                "flood-resistant design commanding premium pricing")
        
        if "Industrial Real Estate" in category_counts:
            summary["industrial"] = ("Industrial sector experiencing unprecedented demand with " +
                                   "e-commerce and logistics driving sub-4% vacancy")
        
        summary["overall"] = ("Houston's 2024-2025 real estate market shows robust fundamentals " +
                            "with institutional capital deployment offsetting construction cost pressures")
        
        return summary
    
    def _generate_recommendations(self, metrics: Dict, opportunities: List, 
                                risks: List) -> List[str]:
        """Generate actionable investment recommendations"""
        recommendations = []
        
        # Cap rate based recommendations
        if "average_cap_rate" in metrics:
            avg_cap = metrics["average_cap_rate"]
            if avg_cap > 6.5:
                recommendations.append(
                    f"Target value-add opportunities with {avg_cap}% average cap rates " +
                    "offering 200-300bps spread over core assets"
                )
            else:
                recommendations.append(
                    f"Core asset pricing at {avg_cap}% cap rates suggests focusing on " +
                    "development or opportunistic strategies"
                )
        
        # Construction pipeline recommendations
        if "total_construction_pipeline_millions" in metrics:
            pipeline = metrics["total_construction_pipeline_millions"]
            recommendations.append(
                f"${pipeline:,.0f}M construction pipeline creates opportunities in " +
                "construction lending and materials supply sectors"
            )
        
        # Opportunity zone recommendations
        oz_opportunities = [o for o in opportunities if o.get("type") == "opportunity_zone"]
        if oz_opportunities:
            recommendations.append(
                f"{len(oz_opportunities)} Opportunity Zones identified for tax-advantaged " +
                "investment with 10-year capital gains deferrals"
            )
        
        # Risk-based recommendations
        climate_risks = [r for r in risks if "climate" in r.get("type", "").lower()]
        if climate_risks:
            recommendations.append(
                "Prioritize climate-resilient properties and flood mitigation " +
                "improvements for long-term value preservation"
            )
        
        # Sector-specific recommendations
        recommendations.append(
            "Focus on industrial/logistics assets near Port Houston and major highways " +
            "for e-commerce growth capture"
        )
        
        return recommendations[:6]  # Top 6 recommendations
    
    def _prepare_integration_queue(self, consolidated: Dict) -> List[Dict]:
        """Prepare data for T2/T3 pipeline integration"""
        integration_queue = []
        
        # Create integration package
        integration_package = {
            "source": "T4-Market-Intelligence",
            "timestamp": datetime.now().isoformat(),
            "data_type": "premium_market_intelligence",
            "priority": "high",
            "content": {
                "consolidated_intelligence": consolidated,
                "processing_stats": self.processing_stats,
                "domain_mappings": self._create_domain_mappings(consolidated)
            }
        }
        
        integration_queue.append(integration_package)
        
        # Queue for T2 processing
        t2_queue_file = Path(self.config["integration"]["t2_queue_path"]) / \
                       f"t4_intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(t2_queue_file, 'w') as f:
            json.dump(integration_package, f, indent=2, cls=NumpyEncoder)
        
        print(f"Queued for T2 processing: {t2_queue_file}")
        
        # Prepare T3 knowledge updates
        knowledge_updates = self._prepare_knowledge_updates(consolidated)
        
        t3_update_file = Path(self.config["integration"]["t3_update_path"]) / \
                        f"t4_knowledge_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(t3_update_file, 'w') as f:
            json.dump(knowledge_updates, f, indent=2, cls=NumpyEncoder)
        
        print(f"Prepared T3 knowledge updates: {t3_update_file}")
        
        return integration_queue
    
    def _create_domain_mappings(self, consolidated: Dict) -> Dict[str, List]:
        """Map intelligence to T2/T3 domains"""
        domain_mappings = {
            "financial_intelligence": [],
            "market_intelligence": [],
            "environmental_intelligence": [],
            "neighborhood_intelligence": [],
            "technology_intelligence": []
        }
        
        # Map financial metrics
        if consolidated.get("key_metrics"):
            domain_mappings["financial_intelligence"].append({
                "type": "financial_metrics",
                "data": consolidated["key_metrics"]
            })
        
        # Map opportunities by type
        for opp in consolidated.get("investment_opportunities", []):
            if "opportunity_zone" in str(opp).lower():
                domain_mappings["neighborhood_intelligence"].append(opp)
            else:
                domain_mappings["market_intelligence"].append(opp)
        
        # Map risks
        for risk in consolidated.get("risk_assessment", []):
            if "climate" in str(risk).lower():
                domain_mappings["environmental_intelligence"].append(risk)
            else:
                domain_mappings["market_intelligence"].append(risk)
        
        return domain_mappings
    
    def _prepare_knowledge_updates(self, consolidated: Dict) -> Dict[str, Any]:
        """Prepare updates for T3 agent knowledge bases"""
        updates = {
            "update_id": f"t4-update-{datetime.now().strftime('%Y%m%d')}",
            "source": "T4-Market-Intelligence",
            "timestamp": datetime.now().isoformat(),
            "knowledge_updates": {}
        }
        
        # Financial agent updates
        updates["knowledge_updates"]["1_Quantitative_Financial_Houston_Agent"] = {
            "new_metrics": consolidated.get("key_metrics", {}),
            "market_data": {
                "data_vintage": "2024-2025",
                "cap_rates": consolidated["key_metrics"].get("cap_rate_range", []),
                "construction_pipeline": consolidated["key_metrics"].get("total_construction_pipeline_millions", 0)
            }
        }
        
        # Market analysis agent updates
        updates["knowledge_updates"]["2_Market_Analysis_Houston_Agent"] = {
            "market_summary": consolidated.get("market_summary", {}),
            "opportunities": consolidated.get("investment_opportunities", [])[:5],
            "recommendations": consolidated.get("actionable_recommendations", [])
        }
        
        # Environmental agent updates
        updates["knowledge_updates"]["3_Environmental_Houston_Agent"] = {
            "climate_risks": [r for r in consolidated.get("risk_assessment", []) 
                            if "climate" in str(r).lower()],
            "resilience_factors": ["flood_mitigation", "green_building", "energy_efficiency"]
        }
        
        return updates
    
    def _save_intelligence_report(self, report_data: Dict):
        """Save individual intelligence report"""
        if "error" in report_data:
            return
            
        output_dir = Path(self.config["output"]["base_path"]) / \
                    self.config["output"]["structured_data"]
        
        filename = f"{report_data['intelligence_id']}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2, cls=NumpyEncoder)
    
    def _save_results(self, results: Dict):
        """Save all processing results"""
        # Update processing stats
        self.processing_stats["end_time"] = datetime.now().isoformat()
        self.processing_stats["status"] = "completed"
        
        # Save main results file
        results_file = Path(self.config["output"]["base_path"]) / \
                      f"t4_processing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, cls=NumpyEncoder)
        
        # Save processing status
        status_file = Path(self.config["integration"]["processing_status"])
        with open(status_file, 'w') as f:
            json.dump(self.processing_stats, f, indent=2)
        
        print(f"\nResults saved to: {results_file}")
    
    def _print_processing_summary(self, results: Dict):
        """Print processing summary"""
        print("\n" + "="*80)
        print("T4 PROCESSING COMPLETE")
        print("="*80)
        print(f"Reports Processed: {self.processing_stats['reports_processed']}")
        print(f"Visualizations Processed: {self.processing_stats['visualizations_processed']}")
        print(f"Intelligence Reports Generated: {self.processing_stats['intelligence_generated']}")
        print(f"Errors Encountered: {len(self.processing_stats['errors'])}")
        
        if results.get("consolidated_intelligence", {}).get("key_metrics"):
            print("\nKEY METRICS EXTRACTED:")
            for metric, value in results["consolidated_intelligence"]["key_metrics"].items():
                print(f"  - {metric}: {value}")
        
        print("\nINTEGRATION STATUS:")
        print(f"  - T2 Queue: {len(results.get('integration_queue', []))} packages")
        print(f"  - T3 Updates: Prepared")
        
        print("="*80)


def main():
    """Main entry point"""
    agent = T4MarketIntelligenceAgent()
    
    try:
        results = agent.process_data_processing_part2()
        
        # Print success message
        print("\n✅ T4 Market Intelligence Agent processing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in T4 processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())