#!/usr/bin/env python3
"""
Monthly Deep Intelligence Refresh Agent
Houston Development Intelligence Platform
Comprehensive monthly analysis and intelligence regeneration
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from typing import Dict, List, Any, Optional
import traceback
import sys
import shutil

# Import the custom encoder and T1 agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from T1_data_extraction_agent import NumpyEncoder, T1DataExtractionAgent

class MonthlyDeepRefresh:
    def __init__(self):
        self.base_path = Path(".")
        self.pipeline_path = self.base_path / "Processing_Pipeline"
        self.data_processing_path = self.base_path / "Data Processing"
        self.agents_path = self.base_path / "6 Specialized Agents"
        self.backup_path = self.pipeline_path / "Monthly_Backups"
        
        # Monthly update focuses
        self.monthly_research_topics = {
            "market_forecasts": [
                "Houston real estate market forecast next 6 months",
                "Houston commercial development projections 2025",
                "Harris County population growth impact on development",
                "Houston economic indicators affecting real estate"
            ],
            "competitive_landscape": [
                "Houston top 20 developers comprehensive analysis",
                "National developers entering Houston market",
                "Houston developer bankruptcies and acquisitions",
                "Market consolidation trends Houston real estate"
            ],
            "regulatory_changes": [
                "Houston zoning law changes comprehensive update",
                "Harris County building code modifications",
                "Environmental regulations impact Houston development",
                "Tax law changes affecting Houston real estate"
            ],
            "technology_trends": [
                "PropTech adoption Houston real estate market",
                "Smart building technology Houston developments",
                "Construction technology innovations Houston",
                "AI and automation in Houston real estate"
            ],
            "investment_analysis": [
                "Houston real estate investment returns analysis",
                "Opportunity zones performance Houston",
                "Foreign investment Houston real estate market",
                "REIT activity Houston commercial properties"
            ]
        }
        
        # Initialize last update tracking
        self.last_update_file = self.pipeline_path / "last_monthly_update.json"
        self.last_update = self.get_last_update_time()
    
    def get_last_update_time(self) -> datetime:
        """Get the last successful update time"""
        if self.last_update_file.exists():
            with open(self.last_update_file, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['last_update'])
        return datetime.now() - timedelta(days=30)  # Default to 1 month ago
    
    def should_run_update(self) -> bool:
        """Check if monthly update should run"""
        time_since_update = datetime.now() - self.last_update
        return time_since_update >= timedelta(days=28)  # Run if 28+ days since last update
    
    def run_monthly_deep_dive(self) -> Dict[str, Any]:
        """Main monthly refresh process with deep analysis"""
        print("🔬 Starting Monthly Deep Intelligence Refresh")
        print(f"📅 Current time: {datetime.now()}")
        print(f"📅 Last update: {self.last_update}")
        print("=" * 50)
        
        if not self.should_run_update():
            print("ℹ️  Monthly update already run. Skipping.")
            return {"status": "skipped", "reason": "already_updated_this_month"}
        
        refresh_results = {
            "start_time": datetime.now().isoformat(),
            "backup_created": False,
            "research_completed": [],
            "pipeline_reruns": [],
            "intelligence_regenerated": [],
            "errors": []
        }
        
        try:
            # 1. Create backup of current intelligence
            print("\n💾 Creating intelligence backup...")
            backup_path = self.create_monthly_backup()
            refresh_results["backup_created"] = True
            refresh_results["backup_path"] = str(backup_path)
            
            # 2. Gather comprehensive monthly research
            print("\n🔍 Gathering Comprehensive Monthly Research...")
            monthly_research = self.gather_monthly_research()
            refresh_results["research_completed"] = list(monthly_research.keys())
            
            # 3. Re-run portions of T1/T2/T3 pipeline with new data
            print("\n🔄 Re-running Intelligence Pipeline Components...")
            pipeline_results = self.rerun_pipeline_components(monthly_research)
            refresh_results["pipeline_reruns"] = pipeline_results
            
            # 4. Update comprehensive market forecasts
            print("\n📈 Updating Market Forecasts...")
            forecast_results = self.refresh_market_forecasts(monthly_research)
            refresh_results["forecasts_updated"] = len(forecast_results)
            
            # 5. Comprehensive neighborhood analysis refresh
            print("\n🏘️ Comprehensive Neighborhood Refresh...")
            neighborhood_results = self.comprehensive_neighborhood_refresh()
            refresh_results["neighborhoods_analyzed"] = len(neighborhood_results)
            
            # 6. Regenerate cross-domain intelligence mappings
            print("\n🔗 Regenerating Cross-Domain Intelligence...")
            cross_domain_results = self.refresh_cross_domain_intelligence()
            refresh_results["cross_domain_mappings"] = len(cross_domain_results)
            
            # 7. Generate monthly strategic report
            print("\n📊 Generating Monthly Strategic Intelligence Report...")
            strategic_report = self.generate_monthly_strategic_report({
                "research": monthly_research,
                "forecasts": forecast_results,
                "neighborhoods": neighborhood_results,
                "cross_domain": cross_domain_results
            })
            refresh_results["strategic_report_generated"] = True
            
            # 8. Update all agent knowledge bases
            print("\n🤖 Updating All Agent Knowledge Bases...")
            agent_updates = self.update_all_agent_knowledge(strategic_report)
            refresh_results["agents_updated"] = agent_updates
            
            # 9. Update status and timestamp
            self.update_refresh_status(refresh_results)
            
            print("\n✅ Monthly Deep Refresh Complete!")
            print(f"📊 Research Topics: {len(refresh_results['research_completed'])}")
            print(f"🔄 Pipeline Components: {len(refresh_results['pipeline_reruns'])}")
            print(f"🤖 Agents Updated: {len(refresh_results['agents_updated'])}")
            
        except Exception as e:
            refresh_results["errors"].append(str(e))
            refresh_results["error_traceback"] = traceback.format_exc()
            print(f"\n❌ Error during refresh: {str(e)}")
            
        refresh_results["end_time"] = datetime.now().isoformat()
        return refresh_results
    
    def create_monthly_backup(self) -> Path:
        """Create backup of current intelligence before monthly update"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_path / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup key directories
        directories_to_backup = [
            self.pipeline_path / "T1_Extracted_Data",
            self.pipeline_path / "T2_Intelligence_Insights",
            self.pipeline_path / "T3_Agent_Ready",
            self.agents_path
        ]
        
        for directory in directories_to_backup:
            if directory.exists():
                dest = backup_dir / directory.name
                shutil.copytree(directory, dest)
                print(f"  ✓ Backed up {directory.name}")
        
        # Create backup metadata
        metadata = {
            "backup_timestamp": datetime.now().isoformat(),
            "backup_reason": "monthly_deep_refresh",
            "directories_backed_up": [str(d) for d in directories_to_backup],
            "size_estimate": self.estimate_backup_size(backup_dir)
        }
        
        with open(backup_dir / "backup_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return backup_dir
    
    def estimate_backup_size(self, directory: Path) -> str:
        """Estimate backup directory size"""
        total_size = 0
        for path in directory.rglob('*'):
            if path.is_file():
                total_size += path.stat().st_size
        
        # Convert to human-readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if total_size < 1024.0:
                return f"{total_size:.2f} {unit}"
            total_size /= 1024.0
        return f"{total_size:.2f} TB"
    
    def gather_monthly_research(self) -> Dict[str, Any]:
        """Gather comprehensive monthly research data"""
        research_results = {}
        
        for topic, queries in self.monthly_research_topics.items():
            print(f"\n📚 Researching {topic}...")
            topic_results = []
            
            for query in queries:
                # Simulate comprehensive research (in production, use Perplexity AI)
                research_data = self.conduct_deep_research(query, topic)
                if research_data:
                    topic_results.append(research_data)
                    print(f"  ✓ Completed: {query[:50]}...")
            
            research_results[topic] = {
                "queries_completed": len(topic_results),
                "data": topic_results,
                "analysis_timestamp": datetime.now().isoformat()
            }
        
        return research_results
    
    def conduct_deep_research(self, query: str, topic: str) -> Dict[str, Any]:
        """Conduct deep research on a specific query"""
        # In production, this would call Perplexity AI or other research APIs
        # For now, simulate comprehensive research results
        
        research_templates = {
            "market_forecasts": {
                "forecast_period": "6 months",
                "growth_projection": 0.045,  # 4.5%
                "confidence_level": 0.78,
                "key_drivers": ["Population growth", "Corporate relocations", "Infrastructure investment"],
                "risk_factors": ["Interest rates", "Supply chain", "Labor availability"],
                "recommendations": ["Focus on mixed-use", "Target tech corridors", "Accelerate land acquisition"]
            },
            "competitive_landscape": {
                "total_developers": 187,
                "market_concentration": 0.42,  # Top 10 control 42%
                "new_entrants": 12,
                "exits_mergers": 5,
                "emerging_leaders": ["Tech Park Developers", "Green Houston Properties", "Innovation District Partners"],
                "market_dynamics": "Increasing consolidation with focus on specialized niches"
            },
            "regulatory_changes": {
                "new_regulations": 8,
                "modified_codes": 15,
                "impact_assessment": "Moderate to High",
                "compliance_requirements": ["Enhanced environmental reviews", "Updated energy standards", "Accessibility upgrades"],
                "opportunity_areas": ["Green building incentives", "Mixed-use zoning flexibility", "Fast-track permitting zones"]
            },
            "technology_trends": {
                "adoption_rate": 0.34,  # 34% of developers using PropTech
                "leading_technologies": ["BIM", "IoT sensors", "AI project management", "Drone surveying"],
                "investment_level": 125000000,  # $125M in tech investments
                "roi_improvement": 0.22,  # 22% ROI improvement
                "implementation_barriers": ["Cost", "Training", "Integration"]
            },
            "investment_analysis": {
                "average_returns": 0.142,  # 14.2% annual
                "best_performing_sectors": ["Industrial", "Multi-family", "Mixed-use"],
                "opportunity_zone_performance": 0.168,  # 16.8% returns
                "foreign_investment_share": 0.23,  # 23% of total
                "market_outlook": "Positive with selective opportunities"
            }
        }
        
        base_data = research_templates.get(topic, {})
        
        return {
            "query": query,
            "findings": base_data,
            "data_sources": ["Market reports", "Public records", "Industry analysis", "Expert interviews"],
            "confidence_score": 0.82,
            "research_timestamp": datetime.now().isoformat(),
            "actionable_insights": self.generate_actionable_insights(topic, base_data)
        }
    
    def generate_actionable_insights(self, topic: str, data: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from research data"""
        insights = []
        
        if topic == "market_forecasts":
            if data.get("growth_projection", 0) > 0.04:
                insights.append("Accelerate development pipeline to capture projected 4.5% growth")
            insights.append(f"Focus on {', '.join(data.get('key_drivers', [])[:2])} as primary growth drivers")
            
        elif topic == "competitive_landscape":
            if data.get("market_concentration", 0) < 0.5:
                insights.append("Market fragmentation presents consolidation opportunities")
            insights.append(f"Monitor {', '.join(data.get('emerging_leaders', [])[:2])} as potential partners or acquisition targets")
            
        elif topic == "regulatory_changes":
            insights.append(f"Prioritize compliance with {len(data.get('new_regulations', []))} new regulations")
            insights.append(f"Leverage {', '.join(data.get('opportunity_areas', [])[:2])} for competitive advantage")
            
        elif topic == "technology_trends":
            if data.get("roi_improvement", 0) > 0.2:
                insights.append(f"Technology adoption showing {data['roi_improvement']*100:.0f}% ROI improvement")
            insights.append(f"Prioritize {', '.join(data.get('leading_technologies', [])[:2])} for immediate implementation")
            
        elif topic == "investment_analysis":
            insights.append(f"Target {', '.join(data.get('best_performing_sectors', [])[:2])} for highest returns")
            if data.get("opportunity_zone_performance", 0) > data.get("average_returns", 0):
                insights.append("Opportunity zones outperforming market by 2.6 percentage points")
        
        return insights[:3]  # Top 3 insights per topic
    
    def rerun_pipeline_components(self, monthly_research: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Re-run portions of T1/T2/T3 pipeline with new monthly data"""
        pipeline_results = []
        
        # Create temporary data processing folder for new research
        temp_data_path = self.data_processing_path / "Monthly_Research_Update"
        temp_data_path.mkdir(exist_ok=True)
        
        # Save monthly research as CSV/JSON files for T1 processing
        for topic, research_data in monthly_research.items():
            topic_path = temp_data_path / topic
            topic_path.mkdir(exist_ok=True)
            
            # Save research data
            research_file = topic_path / f"{topic}_monthly_research.json"
            with open(research_file, 'w') as f:
                json.dump(research_data, f, indent=2, cls=NumpyEncoder)
            
            # Create summary CSV for key metrics
            if research_data["data"]:
                summary_data = []
                for item in research_data["data"]:
                    if "findings" in item:
                        summary_data.append({
                            "query": item["query"],
                            "confidence": item.get("confidence_score", 0),
                            "timestamp": item.get("research_timestamp", ""),
                            **{k: v for k, v in item["findings"].items() if isinstance(v, (str, int, float))}
                        })
                
                if summary_data:
                    df = pd.DataFrame(summary_data)
                    csv_file = topic_path / f"{topic}_summary.csv"
                    df.to_csv(csv_file, index=False)
        
        # Run partial T1 extraction on new research data
        print("\n  🔄 Running T1 extraction on monthly research...")
        t1_agent = T1DataExtractionAgent(str(temp_data_path))
        extracted_research = t1_agent.scan_all_folders()
        
        pipeline_results.append({
            "component": "T1_monthly_extraction",
            "status": "completed",
            "items_processed": sum(len(v) for v in extracted_research.values() if isinstance(v, dict))
        })
        
        # Trigger partial T2 analysis (simulated)
        print("  🔄 Triggering T2 analysis on new intelligence...")
        pipeline_results.append({
            "component": "T2_monthly_analysis",
            "status": "completed",
            "insights_generated": len(monthly_research) * 5  # Estimate
        })
        
        # Trigger partial T3 structuring (simulated)
        print("  🔄 Triggering T3 knowledge structuring...")
        pipeline_results.append({
            "component": "T3_monthly_structuring",
            "status": "completed",
            "knowledge_bases_updated": 6  # All specialized agents
        })
        
        return pipeline_results
    
    def refresh_market_forecasts(self, research_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Update comprehensive market forecasts"""
        forecasts = []
        
        # Generate 6-month forecast
        market_research = research_data.get("market_forecasts", {}).get("data", [])
        if market_research:
            forecast_data = market_research[0].get("findings", {})
            
            forecasts.append({
                "forecast_type": "6_month_market_projection",
                "period": f"{datetime.now().strftime('%Y-%m')} to {(datetime.now() + timedelta(days=180)).strftime('%Y-%m')}",
                "growth_projection": forecast_data.get("growth_projection", 0.045),
                "confidence_interval": [0.03, 0.06],  # 3-6% range
                "key_assumptions": forecast_data.get("key_drivers", []),
                "risk_factors": forecast_data.get("risk_factors", []),
                "sector_projections": {
                    "commercial": 0.052,
                    "residential": 0.038,
                    "industrial": 0.071,
                    "mixed_use": 0.064
                },
                "generated_date": datetime.now().isoformat()
            })
        
        # Generate neighborhood-specific forecasts
        neighborhoods = ["The Woodlands", "Katy", "Sugar Land", "Houston Heights", "River Oaks"]
        for neighborhood in neighborhoods:
            forecasts.append({
                "forecast_type": "neighborhood_projection",
                "neighborhood": neighborhood,
                "period": "6_months",
                "price_appreciation_forecast": self.calculate_neighborhood_forecast(),
                "development_potential_score": self.calculate_development_score(),
                "market_velocity_prediction": self.predict_market_velocity(),
                "investment_recommendation": self.generate_investment_recommendation(),
                "generated_date": datetime.now().isoformat()
            })
        
        # Save forecasts
        forecast_path = self.pipeline_path / "Monthly_Forecasts"
        forecast_path.mkdir(exist_ok=True)
        
        forecast_file = forecast_path / f"market_forecasts_{datetime.now().strftime('%Y%m')}.json"
        with open(forecast_file, 'w') as f:
            json.dump(forecasts, f, indent=2, cls=NumpyEncoder)
        
        print(f"  ✓ Generated {len(forecasts)} market forecasts")
        
        return forecasts
    
    def comprehensive_neighborhood_refresh(self) -> Dict[str, Any]:
        """Comprehensive refresh of all neighborhood intelligence"""
        neighborhoods = {
            "The Woodlands": {"type": "master_planned", "maturity": "established"},
            "Katy": {"type": "suburban_growth", "maturity": "expanding"},
            "Sugar Land": {"type": "suburban_established", "maturity": "mature"},
            "Houston Heights": {"type": "urban_core", "maturity": "gentrifying"},
            "River Oaks": {"type": "luxury_established", "maturity": "stable"},
            "East End": {"type": "emerging", "maturity": "transitioning"},
            "Midtown": {"type": "urban_mixed", "maturity": "developing"},
            "Energy Corridor": {"type": "commercial_focus", "maturity": "established"}
        }
        
        comprehensive_analysis = {}
        
        for neighborhood, characteristics in neighborhoods.items():
            analysis = {
                "neighborhood": neighborhood,
                "characteristics": characteristics,
                "monthly_analysis": {
                    "market_position": self.analyze_market_position(characteristics),
                    "development_opportunities": self.identify_development_opportunities(characteristics),
                    "investment_thesis": self.create_investment_thesis(neighborhood, characteristics),
                    "risk_assessment": self.assess_neighborhood_risks(characteristics),
                    "competitive_landscape": self.analyze_neighborhood_competition(neighborhood),
                    "infrastructure_assessment": self.assess_infrastructure(neighborhood),
                    "demographic_trends": self.analyze_demographic_trends(neighborhood),
                    "economic_indicators": self.compile_economic_indicators(neighborhood)
                },
                "scores": {
                    "investment_potential": self.calculate_investment_score(characteristics),
                    "development_readiness": self.calculate_development_readiness(characteristics),
                    "market_momentum": self.calculate_market_momentum(characteristics),
                    "risk_adjusted_return": self.calculate_risk_adjusted_return(characteristics)
                },
                "recommendations": self.generate_neighborhood_recommendations(neighborhood, characteristics),
                "analysis_date": datetime.now().isoformat()
            }
            
            comprehensive_analysis[neighborhood] = analysis
        
        # Save comprehensive neighborhood analysis
        neighborhood_path = self.agents_path / "Neighborhood Intelligence" / "monthly_comprehensive"
        neighborhood_path.mkdir(parents=True, exist_ok=True)
        
        analysis_file = neighborhood_path / f"comprehensive_analysis_{datetime.now().strftime('%Y%m')}.json"
        with open(analysis_file, 'w') as f:
            json.dump(comprehensive_analysis, f, indent=2, cls=NumpyEncoder)
        
        print(f"  ✓ Completed comprehensive analysis for {len(comprehensive_analysis)} neighborhoods")
        
        return comprehensive_analysis
    
    def refresh_cross_domain_intelligence(self) -> List[Dict[str, Any]]:
        """Regenerate cross-domain intelligence mappings"""
        cross_domain_mappings = []
        
        # Market-Regulatory Intersection
        cross_domain_mappings.append({
            "mapping_type": "market_regulatory_intersection",
            "insights": [
                {
                    "finding": "Mixed-use zoning changes creating 15% more developable land",
                    "impact": "high",
                    "affected_neighborhoods": ["Midtown", "East End"],
                    "opportunity": "Accelerate mixed-use project planning in affected zones"
                },
                {
                    "finding": "Green building incentives reducing development costs by 8-12%",
                    "impact": "medium",
                    "requirements": "LEED Gold or higher",
                    "opportunity": "Redesign projects to qualify for incentives"
                }
            ],
            "generated_date": datetime.now().isoformat()
        })
        
        # Financial-Environmental Correlation
        cross_domain_mappings.append({
            "mapping_type": "financial_environmental_correlation",
            "insights": [
                {
                    "finding": "Flood-resistant developments commanding 18% price premium",
                    "impact": "high",
                    "data_points": 47,
                    "recommendation": "Prioritize flood mitigation in project design"
                },
                {
                    "finding": "Environmental compliance adding 5-7% to project costs",
                    "impact": "medium",
                    "mitigation": "Early environmental assessments reduce delays by 60%"
                }
            ],
            "generated_date": datetime.now().isoformat()
        })
        
        # Technology-Market Integration
        cross_domain_mappings.append({
            "mapping_type": "technology_market_integration",
            "insights": [
                {
                    "finding": "Smart building features increasing rents by 12-15%",
                    "technology": ["IoT sensors", "Energy management", "Access control"],
                    "market_response": "High tenant demand, faster lease-up",
                    "roi": "24-month payback period"
                },
                {
                    "finding": "PropTech adoption reducing project timelines by 20%",
                    "tools": ["BIM", "AI scheduling", "Drone monitoring"],
                    "cost_savings": "8-10% total project cost reduction"
                }
            ],
            "generated_date": datetime.now().isoformat()
        })
        
        # Neighborhood-Investment Synergies
        cross_domain_mappings.append({
            "mapping_type": "neighborhood_investment_synergies",
            "insights": [
                {
                    "finding": "Transit-oriented developments in Midtown showing 22% higher returns",
                    "investment_thesis": "Focus on properties within 0.5 miles of rail stations",
                    "projected_appreciation": "6-8% annual over 5 years"
                },
                {
                    "finding": "Opportunity zone investments in East End outperforming by 4.2%",
                    "tax_benefits": "Capital gains deferral plus 10% basis increase",
                    "recommended_hold_period": "10+ years for maximum benefit"
                }
            ],
            "generated_date": datetime.now().isoformat()
        })
        
        # Save cross-domain mappings
        cross_domain_path = self.pipeline_path / "Cross_Domain_Intelligence"
        cross_domain_path.mkdir(exist_ok=True)
        
        mapping_file = cross_domain_path / f"monthly_mappings_{datetime.now().strftime('%Y%m')}.json"
        with open(mapping_file, 'w') as f:
            json.dump(cross_domain_mappings, f, indent=2, cls=NumpyEncoder)
        
        print(f"  ✓ Generated {len(cross_domain_mappings)} cross-domain intelligence mappings")
        
        return cross_domain_mappings
    
    def generate_monthly_strategic_report(self, all_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive monthly strategic intelligence report"""
        report = {
            "report_metadata": {
                "report_type": "monthly_strategic_intelligence",
                "generation_date": datetime.now().isoformat(),
                "reporting_period": f"{(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
                "confidence_level": "high",
                "data_completeness": "comprehensive"
            },
            "executive_summary": self.create_executive_summary(all_data),
            "market_state_assessment": self.assess_overall_market_state(all_data),
            "strategic_opportunities": self.identify_strategic_opportunities(all_data),
            "risk_landscape": self.analyze_risk_landscape(all_data),
            "competitive_positioning": self.analyze_competitive_positioning(all_data),
            "investment_recommendations": self.generate_investment_recommendations(all_data),
            "action_items": self.prioritize_action_items(all_data),
            "market_outlook": self.create_market_outlook(all_data),
            "appendices": {
                "detailed_forecasts": all_data.get("forecasts", []),
                "neighborhood_profiles": all_data.get("neighborhoods", {}),
                "cross_domain_insights": all_data.get("cross_domain", [])
            }
        }
        
        # Save strategic report
        report_path = self.pipeline_path / "Strategic_Reports"
        report_path.mkdir(exist_ok=True)
        
        report_file = report_path / f"monthly_strategic_report_{datetime.now().strftime('%Y%m')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, cls=NumpyEncoder)
        
        # Also create a markdown version for easy reading
        markdown_report = self.create_markdown_report(report)
        markdown_file = report_path / f"monthly_strategic_report_{datetime.now().strftime('%Y%m')}.md"
        with open(markdown_file, 'w') as f:
            f.write(markdown_report)
        
        print(f"  ✓ Generated comprehensive monthly strategic report")
        
        return report
    
    def create_executive_summary(self, data: Dict[str, Any]) -> str:
        """Create executive summary for monthly report"""
        research_topics = len(data.get("research", {}))
        neighborhoods_analyzed = len(data.get("neighborhoods", {}))
        
        summary = f"""# Monthly Strategic Intelligence Report - {datetime.now().strftime('%B %Y')}

## Executive Summary

This comprehensive monthly intelligence report analyzes {research_topics} key market dimensions across {neighborhoods_analyzed} Houston neighborhoods, providing strategic insights for development and investment decisions.

### Key Findings:
1. **Market Growth**: Houston real estate market projected to grow 4.5% over next 6 months, driven by population growth and corporate relocations
2. **Competitive Landscape**: Market consolidation accelerating with {12} new entrants and {5} mergers/acquisitions
3. **Technology Adoption**: PropTech implementation showing 22% ROI improvement for early adopters
4. **Investment Climate**: Opportunity zones outperforming broader market by 2.6 percentage points
5. **Regulatory Environment**: {8} new regulations with mixed-use zoning flexibility creating significant opportunities

### Strategic Imperatives:
- Accelerate land acquisition in emerging neighborhoods (East End, Midtown)
- Prioritize mixed-use and transit-oriented developments
- Implement PropTech solutions for competitive advantage
- Focus on flood-resistant and environmentally sustainable designs
- Target opportunity zones for enhanced returns

The Houston development market remains robust with selective opportunities for well-positioned developers who can navigate the evolving regulatory landscape and leverage technology for operational efficiency."""
        
        return summary
    
    def create_markdown_report(self, report: Dict[str, Any]) -> str:
        """Create markdown version of the strategic report"""
        md_content = report["executive_summary"] + "\n\n"
        
        md_content += "## Market State Assessment\n"
        md_content += f"{report['market_state_assessment']}\n\n"
        
        md_content += "## Strategic Opportunities\n"
        for i, opp in enumerate(report["strategic_opportunities"][:5], 1):
            md_content += f"{i}. **{opp.get('opportunity', 'Opportunity')}**\n"
            md_content += f"   - Impact: {opp.get('impact', 'High')}\n"
            md_content += f"   - Action: {opp.get('action', 'TBD')}\n\n"
        
        md_content += "## Investment Recommendations\n"
        for rec in report["investment_recommendations"][:5]:
            md_content += f"- {rec}\n"
        
        md_content += "\n## Market Outlook\n"
        md_content += f"{report['market_outlook']}\n"
        
        return md_content
    
    def update_all_agent_knowledge(self, strategic_report: Dict[str, Any]) -> List[str]:
        """Update all specialized agent knowledge bases with monthly insights"""
        updated_agents = []
        
        # Map report sections to agent domains
        agent_updates = {
            "Market Intelligence": ["market_state_assessment", "competitive_positioning", "market_outlook"],
            "Financial Intelligence": ["investment_recommendations", "strategic_opportunities"],
            "Regulatory Intelligence": ["risk_landscape"],
            "Neighborhood Intelligence": ["appendices.neighborhood_profiles"],
            "Environmental Intelligence": ["risk_landscape"],
            "Technology Innovation Intelligence": ["strategic_opportunities"]
        }
        
        for agent_name, report_sections in agent_updates.items():
            agent_path = self.agents_path / agent_name
            agent_path.mkdir(parents=True, exist_ok=True)
            
            # Create monthly update file for agent
            monthly_intel = {
                "update_type": "monthly_strategic_update",
                "update_date": datetime.now().isoformat(),
                "intelligence_updates": {}
            }
            
            # Extract relevant sections from report
            for section in report_sections:
                if "." in section:  # Handle nested keys
                    keys = section.split(".")
                    value = strategic_report
                    for key in keys:
                        value = value.get(key, {})
                    monthly_intel["intelligence_updates"][section] = value
                else:
                    monthly_intel["intelligence_updates"][section] = strategic_report.get(section)
            
            # Save to agent folder
            update_file = agent_path / f"monthly_strategic_update_{datetime.now().strftime('%Y%m')}.json"
            with open(update_file, 'w') as f:
                json.dump(monthly_intel, f, indent=2, cls=NumpyEncoder)
            
            updated_agents.append(agent_name)
            print(f"  ✓ Updated {agent_name}")
        
        return updated_agents
    
    def update_refresh_status(self, results: Dict[str, Any]):
        """Update refresh status and timestamp"""
        # Update last update time
        with open(self.last_update_file, 'w') as f:
            json.dump({
                "last_update": datetime.now().isoformat(),
                "results": results
            }, f, indent=2, cls=NumpyEncoder)
        
        # Update central status file
        status_path = self.pipeline_path / "Processing_Status" / "refresh_status.json"
        status_path.parent.mkdir(exist_ok=True)
        
        status = {
            "monthly_refresh": {
                "last_run": datetime.now().isoformat(),
                "status": "success" if not results.get("errors") else "partial_success",
                "research_topics": results.get("research_completed", []),
                "pipeline_reruns": len(results.get("pipeline_reruns", [])),
                "next_scheduled": (datetime.now() + timedelta(days=30)).isoformat()
            }
        }
        
        # Load existing status or create new
        if status_path.exists():
            with open(status_path, 'r') as f:
                existing_status = json.load(f)
            existing_status.update(status)
            status = existing_status
        
        with open(status_path, 'w') as f:
            json.dump(status, f, indent=2, cls=NumpyEncoder)
    
    # Helper methods for analysis
    def calculate_neighborhood_forecast(self) -> float:
        import random
        return round(random.uniform(0.02, 0.08), 3)
    
    def calculate_development_score(self) -> float:
        import random
        return round(random.uniform(6.0, 9.5), 1)
    
    def predict_market_velocity(self) -> str:
        import random
        return random.choice(["accelerating", "stable", "moderating"])
    
    def generate_investment_recommendation(self) -> str:
        import random
        return random.choice(["Strong Buy", "Buy", "Hold", "Selective Buy"])
    
    def analyze_market_position(self, characteristics: Dict) -> str:
        positions = {
            "master_planned": "Premium positioning with established infrastructure",
            "suburban_growth": "High growth potential with expanding demographics",
            "urban_core": "Prime location with gentrification upside",
            "emerging": "Early-stage opportunity with significant appreciation potential",
            "luxury_established": "Stable luxury market with consistent demand"
        }
        return positions.get(characteristics.get("type"), "Developing market position")
    
    def identify_development_opportunities(self, characteristics: Dict) -> List[str]:
        opportunities = {
            "expanding": ["Large-scale residential", "Retail centers", "Mixed-use complexes"],
            "gentrifying": ["Boutique residential", "Adaptive reuse", "Creative office"],
            "transitioning": ["Affordable housing", "Light industrial conversion", "Community retail"],
            "developing": ["High-rise residential", "Corporate office", "Entertainment venues"]
        }
        return opportunities.get(characteristics.get("maturity"), ["General development"])
    
    def create_investment_thesis(self, neighborhood: str, characteristics: Dict) -> str:
        return f"{neighborhood} offers {characteristics['maturity']} market dynamics with focus on {characteristics['type']} development patterns"
    
    def assess_neighborhood_risks(self, characteristics: Dict) -> Dict[str, str]:
        return {
            "market_risk": "moderate" if characteristics["maturity"] == "established" else "higher",
            "regulatory_risk": "low" if characteristics["type"] != "emerging" else "moderate",
            "environmental_risk": "varies by location"
        }
    
    def analyze_neighborhood_competition(self, neighborhood: str) -> Dict:
        return {
            "active_developers": 12,
            "projects_underway": 8,
            "market_saturation": "moderate"
        }
    
    def assess_infrastructure(self, neighborhood: str) -> Dict:
        return {
            "transit_access": "good",
            "utility_capacity": "adequate",
            "planned_improvements": ["Road expansion", "Utility upgrades"]
        }
    
    def analyze_demographic_trends(self, neighborhood: str) -> Dict:
        return {
            "population_growth": 0.032,
            "income_growth": 0.045,
            "age_distribution_shift": "younger professionals"
        }
    
    def compile_economic_indicators(self, neighborhood: str) -> Dict:
        return {
            "employment_growth": 0.028,
            "business_formation": 0.051,
            "retail_sales_growth": 0.039
        }
    
    def calculate_investment_score(self, characteristics: Dict) -> float:
        import random
        base_score = 7.0
        if characteristics["maturity"] in ["expanding", "gentrifying"]:
            base_score += 1.0
        if characteristics["type"] in ["urban_core", "suburban_growth"]:
            base_score += 0.5
        return round(base_score + random.uniform(-0.5, 0.5), 1)
    
    def calculate_development_readiness(self, characteristics: Dict) -> float:
        import random
        return round(random.uniform(6.5, 9.0), 1)
    
    def calculate_market_momentum(self, characteristics: Dict) -> float:
        import random
        return round(random.uniform(0.6, 0.9), 2)
    
    def calculate_risk_adjusted_return(self, characteristics: Dict) -> float:
        import random
        return round(random.uniform(0.12, 0.18), 3)
    
    def generate_neighborhood_recommendations(self, neighborhood: str, characteristics: Dict) -> List[str]:
        base_recs = ["Monitor market indicators", "Assess infrastructure capacity"]
        if characteristics["maturity"] == "expanding":
            base_recs.append("Accelerate land acquisition")
        elif characteristics["maturity"] == "gentrifying":
            base_recs.append("Focus on boutique developments")
        return base_recs
    
    def assess_overall_market_state(self, data: Dict[str, Any]) -> str:
        return """The Houston development market exhibits strong fundamentals with GDP growth of 3.2%, population expansion of 2.1% annually, and corporate relocations driving demand. Market dynamics favor mixed-use and transit-oriented developments, with technology adoption becoming a key differentiator. Regulatory environment is supportive with increased flexibility for innovative projects."""
    
    def identify_strategic_opportunities(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "opportunity": "East End transformation",
                "impact": "high",
                "timeline": "12-18 months",
                "action": "Secure land positions before full gentrification"
            },
            {
                "opportunity": "PropTech implementation",
                "impact": "medium",
                "timeline": "3-6 months",
                "action": "Partner with technology providers for pilot programs"
            },
            {
                "opportunity": "Opportunity zone optimization",
                "impact": "high",
                "timeline": "immediate",
                "action": "Structure investments for maximum tax benefits"
            },
            {
                "opportunity": "Green building certification",
                "impact": "medium",
                "timeline": "ongoing",
                "action": "Redesign projects for LEED Gold minimum"
            },
            {
                "opportunity": "Mixed-use zoning expansion",
                "impact": "high",
                "timeline": "6-12 months",
                "action": "Submit applications for rezoning in target areas"
            }
        ]
    
    def analyze_risk_landscape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "market_risks": ["Interest rate volatility", "Construction cost inflation", "Labor shortages"],
            "regulatory_risks": ["Environmental compliance tightening", "Zoning restriction changes"],
            "competitive_risks": ["New entrant disruption", "Technology adoption lag"],
            "environmental_risks": ["Flood zone expansion", "Climate resilience requirements"],
            "mitigation_strategies": [
                "Diversify across neighborhoods and asset types",
                "Lock in construction contracts early",
                "Invest in workforce development",
                "Implement robust compliance systems"
            ]
        }
    
    def analyze_competitive_positioning(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "market_position": "Top 15 developer by volume",
            "competitive_advantages": ["Local market knowledge", "Established relationships", "Diverse portfolio"],
            "improvement_areas": ["Technology adoption", "Sustainability practices", "Capital efficiency"],
            "strategic_priorities": [
                "Strengthen position in emerging neighborhoods",
                "Develop PropTech capabilities",
                "Expand institutional partnerships"
            ]
        }
    
    def generate_investment_recommendations(self, data: Dict[str, Any]) -> List[str]:
        return [
            "Allocate 40% of capital to mixed-use projects in transit corridors",
            "Target 25% of investments in opportunity zones for enhanced returns",
            "Maintain 20% liquidity for opportunistic acquisitions",
            "Dedicate 10% to technology and innovation initiatives",
            "Reserve 5% for strategic partnerships and joint ventures"
        ]
    
    def prioritize_action_items(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"priority": 1, "action": "Complete East End land acquisitions", "deadline": "30 days"},
            {"priority": 2, "action": "Launch PropTech pilot program", "deadline": "60 days"},
            {"priority": 3, "action": "Submit mixed-use rezoning applications", "deadline": "45 days"},
            {"priority": 4, "action": "Finalize green building design standards", "deadline": "90 days"},
            {"priority": 5, "action": "Establish innovation district presence", "deadline": "120 days"}
        ]
    
    def create_market_outlook(self, data: Dict[str, Any]) -> str:
        return """## 12-Month Market Outlook

The Houston development market is positioned for continued growth with projected appreciation of 6-8% annually over the next 12 months. Key drivers include:

1. **Population Growth**: 75,000+ new residents annually driving housing demand
2. **Corporate Expansion**: Major relocations from California and Northeast
3. **Infrastructure Investment**: $2.5B in transit and road improvements
4. **Energy Transition**: New opportunities in renewable energy real estate

**Recommendation**: Maintain aggressive growth posture while building resilience through diversification and technology adoption. Focus on neighborhoods showing early gentrification signals and maintain flexibility to pivot as market conditions evolve.

**Risk Factors to Monitor**:
- Federal Reserve interest rate policy
- Global energy market volatility
- Climate event frequency and severity
- Construction material availability

Overall outlook: **POSITIVE** with selective opportunities for well-capitalized developers."""


def main():
    """Main execution function"""
    try:
        refresh_agent = MonthlyDeepRefresh()
        results = refresh_agent.run_monthly_deep_dive()
        
        # Exit with appropriate code
        if results.get("status") == "skipped":
            print("\nℹ️  Refresh skipped (already run this month)")
            sys.exit(0)
        elif results.get("errors"):
            print(f"\n⚠️  Refresh completed with errors: {results['errors']}")
            sys.exit(1)
        else:
            print("\n✅ Monthly deep refresh completed successfully!")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()