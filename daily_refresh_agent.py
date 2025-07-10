#!/usr/bin/env python3
"""
Daily Intelligence Refresh Agent
Houston Development Intelligence Platform
Automatically updates real-time data daily
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from typing import Dict, List, Any, Optional
import requests
import traceback
import sys

# Import the custom encoder from T1 agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from T1_data_extraction_agent import NumpyEncoder

class DailyIntelligenceRefresh:
    def __init__(self):
        self.base_path = Path(".")
        self.pipeline_path = self.base_path / "Processing_Pipeline"
        self.data_processing_path = self.base_path / "Data Processing"
        self.agents_path = self.base_path / "6 Specialized Agents"
        self.status_path = self.pipeline_path / "Processing_Status" / "refresh_status.json"
        
        # Daily update targets
        self.daily_update_targets = {
            "construction_permits": {
                "domain": "market_intelligence",
                "queries": [
                    "Houston construction permits filed yesterday",
                    "Harris County building permits last 24 hours",
                    "Houston commercial construction permits today"
                ]
            },
            "mls_listings": {
                "domain": "neighborhood_intelligence",
                "queries": [
                    "Houston MLS new listings yesterday",
                    "Houston real estate price changes today",
                    "Harris County property listings last 24 hours"
                ]
            },
            "zoning_changes": {
                "domain": "regulatory_intelligence",
                "queries": [
                    "Houston zoning changes yesterday",
                    "Harris County zoning variance applications today",
                    "Houston planning commission decisions this week"
                ]
            },
            "development_news": {
                "domain": "market_intelligence",
                "queries": [
                    "Houston development projects announced today",
                    "Houston real estate development news yesterday",
                    "Harris County commercial development updates"
                ]
            }
        }
        
        # Initialize last update tracking
        self.last_update_file = self.pipeline_path / "last_daily_update.json"
        self.last_update = self.get_last_update_time()
    
    def get_last_update_time(self) -> datetime:
        """Get the last successful update time"""
        if self.last_update_file.exists():
            with open(self.last_update_file, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['last_update'])
        return datetime.now() - timedelta(days=1)  # Default to 1 day ago
    
    def should_run_update(self) -> bool:
        """Check if daily update should run"""
        time_since_update = datetime.now() - self.last_update
        return time_since_update >= timedelta(hours=23)  # Run if 23+ hours since last update
    
    def run_daily_refresh(self) -> Dict[str, Any]:
        """Main daily refresh process"""
        print("🔄 Starting Daily Intelligence Refresh")
        print(f"📅 Current time: {datetime.now()}")
        print(f"📅 Last update: {self.last_update}")
        print("=" * 50)
        
        if not self.should_run_update():
            print("ℹ️  Update already run today. Skipping.")
            return {"status": "skipped", "reason": "already_updated_today"}
        
        refresh_results = {
            "start_time": datetime.now().isoformat(),
            "domains_updated": [],
            "new_data_items": 0,
            "errors": []
        }
        
        try:
            # 1. Gather fresh intelligence
            print("\n📊 Gathering Fresh Intelligence...")
            fresh_data = self.gather_daily_intelligence()
            refresh_results["raw_data_gathered"] = len(fresh_data)
            
            # 2. Process and structure the data
            print("\n🔧 Processing New Data...")
            processed_data = self.process_fresh_data(fresh_data)
            refresh_results["processed_items"] = len(processed_data)
            
            # 3. Update agent knowledge bases
            print("\n🤖 Updating Agent Knowledge Bases...")
            update_results = self.update_agent_intelligence(processed_data)
            refresh_results["domains_updated"] = update_results["domains_updated"]
            refresh_results["new_data_items"] = update_results["total_updates"]
            
            # 4. Regenerate affected insights
            print("\n💡 Regenerating Market Insights...")
            insights_updated = self.refresh_market_insights(processed_data)
            refresh_results["insights_regenerated"] = insights_updated
            
            # 5. Update status and timestamp
            self.update_refresh_status(refresh_results)
            
            print("\n✅ Daily Refresh Complete!")
            print(f"📊 Domains Updated: {len(refresh_results['domains_updated'])}")
            print(f"📈 New Data Items: {refresh_results['new_data_items']}")
            
        except Exception as e:
            refresh_results["errors"].append(str(e))
            refresh_results["error_traceback"] = traceback.format_exc()
            print(f"\n❌ Error during refresh: {str(e)}")
            
        refresh_results["end_time"] = datetime.now().isoformat()
        return refresh_results
    
    def gather_daily_intelligence(self) -> Dict[str, Any]:
        """Gather fresh intelligence data"""
        fresh_data = {}
        
        for target_name, target_config in self.daily_update_targets.items():
            print(f"\n🔍 Gathering {target_name} data...")
            target_data = []
            
            for query in target_config["queries"]:
                # Simulate data gathering (in production, this would call Perplexity API)
                # For now, we'll create sample fresh data
                query_result = self.simulate_intelligence_query(query, target_name)
                if query_result:
                    target_data.append(query_result)
                    print(f"  ✓ Found {len(query_result['items'])} items for: {query}")
            
            fresh_data[target_name] = {
                "domain": target_config["domain"],
                "data": target_data,
                "timestamp": datetime.now().isoformat()
            }
        
        return fresh_data
    
    def simulate_intelligence_query(self, query: str, target_type: str) -> Dict[str, Any]:
        """Simulate intelligence gathering (replace with actual API calls)"""
        # In production, this would call Perplexity AI or other data sources
        
        sample_data = {
            "construction_permits": {
                "items": [
                    {
                        "permit_number": f"HP-2025-{datetime.now().strftime('%m%d')}-001",
                        "address": "1234 Main St, Houston, TX",
                        "type": "Commercial",
                        "value": 2500000,
                        "filed_date": datetime.now().isoformat(),
                        "developer": "Houston Development Corp"
                    },
                    {
                        "permit_number": f"HP-2025-{datetime.now().strftime('%m%d')}-002",
                        "address": "5678 Westheimer Rd, Houston, TX",
                        "type": "Mixed-Use",
                        "value": 4500000,
                        "filed_date": datetime.now().isoformat(),
                        "developer": "Westheimer Properties LLC"
                    }
                ]
            },
            "mls_listings": {
                "items": [
                    {
                        "mls_number": f"MLS-{datetime.now().strftime('%Y%m%d')}-001",
                        "address": "9012 River Oaks Blvd",
                        "price": 850000,
                        "price_change": -25000,
                        "days_on_market": 0,
                        "property_type": "Single Family",
                        "neighborhood": "River Oaks"
                    }
                ]
            },
            "zoning_changes": {
                "items": [
                    {
                        "case_number": f"ZC-2025-{datetime.now().strftime('%m%d')}",
                        "location": "Downtown Houston",
                        "current_zoning": "C-1",
                        "proposed_zoning": "MU-2",
                        "status": "Pending Review",
                        "filed_date": datetime.now().isoformat()
                    }
                ]
            },
            "development_news": {
                "items": [
                    {
                        "project_name": "Houston Innovation District Phase 2",
                        "developer": "Tech Park Developers",
                        "investment": 150000000,
                        "announcement_date": datetime.now().isoformat(),
                        "location": "Midtown Houston",
                        "type": "Mixed-Use Technology Campus"
                    }
                ]
            }
        }
        
        return {
            "query": query,
            "items": sample_data.get(target_type, {}).get("items", []),
            "source": "simulated_data",
            "timestamp": datetime.now().isoformat()
        }
    
    def process_fresh_data(self, fresh_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure fresh data for agent consumption"""
        processed = {}
        
        for target_name, target_data in fresh_data.items():
            domain = target_data["domain"]
            
            if domain not in processed:
                processed[domain] = {}
            
            # Structure data by type
            processed[domain][target_name] = {
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "update_type": "daily_refresh",
                    "data_count": sum(len(d["items"]) for d in target_data["data"])
                },
                "data": []
            }
            
            # Flatten and structure the data items
            for data_batch in target_data["data"]:
                for item in data_batch["items"]:
                    structured_item = {
                        **item,
                        "_metadata": {
                            "query_source": data_batch["query"],
                            "extraction_timestamp": data_batch["timestamp"],
                            "update_cycle": "daily"
                        }
                    }
                    processed[domain][target_name]["data"].append(structured_item)
        
        return processed
    
    def update_agent_intelligence(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update agent knowledge bases with fresh data"""
        update_results = {
            "domains_updated": [],
            "total_updates": 0,
            "updates_by_domain": {}
        }
        
        for domain, domain_data in processed_data.items():
            print(f"\n📝 Updating {domain}...")
            domain_updates = 0
            
            # Create domain path if doesn't exist
            domain_path = self.agents_path / domain.replace("_", " ").title()
            domain_path.mkdir(parents=True, exist_ok=True)
            
            for data_type, type_data in domain_data.items():
                # Create daily update file
                daily_file = domain_path / f"daily_updates_{data_type}.json"
                
                # Load existing daily updates or create new
                if daily_file.exists():
                    with open(daily_file, 'r') as f:
                        existing_data = json.load(f)
                else:
                    existing_data = {
                        "update_history": [],
                        "current_data": []
                    }
                
                # Add new data with timestamp
                update_entry = {
                    "update_timestamp": datetime.now().isoformat(),
                    "data_count": len(type_data["data"]),
                    "data": type_data["data"]
                }
                
                existing_data["update_history"].append(update_entry)
                existing_data["current_data"] = type_data["data"]  # Replace with latest
                
                # Keep only last 30 days of history
                cutoff_date = datetime.now() - timedelta(days=30)
                existing_data["update_history"] = [
                    entry for entry in existing_data["update_history"]
                    if datetime.fromisoformat(entry["update_timestamp"]) > cutoff_date
                ]
                
                # Save updated data
                with open(daily_file, 'w') as f:
                    json.dump(existing_data, f, indent=2, cls=NumpyEncoder)
                
                domain_updates += len(type_data["data"])
                print(f"  ✓ Updated {data_type}: {len(type_data['data'])} items")
            
            update_results["domains_updated"].append(domain)
            update_results["updates_by_domain"][domain] = domain_updates
            update_results["total_updates"] += domain_updates
        
        return update_results
    
    def refresh_market_insights(self, processed_data: Dict[str, Any]) -> int:
        """Regenerate market insights based on fresh data"""
        insights_generated = 0
        
        # Create insights directory
        insights_path = self.pipeline_path / "Daily_Insights"
        insights_path.mkdir(exist_ok=True)
        
        # Generate insights by domain
        for domain, domain_data in processed_data.items():
            domain_insights = []
            
            # Generate insights based on data type
            for data_type, type_data in domain_data.items():
                if data_type == "construction_permits" and type_data["data"]:
                    # Analyze permit trends
                    total_value = sum(item.get("value", 0) for item in type_data["data"])
                    domain_insights.append({
                        "type": "permit_activity",
                        "insight": f"New construction permits totaling ${total_value:,} filed today",
                        "data_points": len(type_data["data"]),
                        "timestamp": datetime.now().isoformat()
                    })
                    
                elif data_type == "mls_listings" and type_data["data"]:
                    # Analyze listing trends
                    price_changes = [item.get("price_change", 0) for item in type_data["data"] if item.get("price_change")]
                    if price_changes:
                        avg_change = sum(price_changes) / len(price_changes)
                        domain_insights.append({
                            "type": "price_movement",
                            "insight": f"Average price change: ${avg_change:,.0f}",
                            "data_points": len(price_changes),
                            "timestamp": datetime.now().isoformat()
                        })
                
                elif data_type == "development_news" and type_data["data"]:
                    # Analyze development announcements
                    total_investment = sum(item.get("investment", 0) for item in type_data["data"])
                    if total_investment > 0:
                        domain_insights.append({
                            "type": "investment_flow",
                            "insight": f"New development investments announced: ${total_investment:,}",
                            "data_points": len(type_data["data"]),
                            "timestamp": datetime.now().isoformat()
                        })
            
            # Save domain insights
            if domain_insights:
                insights_file = insights_path / f"{domain}_daily_insights.json"
                
                # Load existing insights or create new
                if insights_file.exists():
                    with open(insights_file, 'r') as f:
                        all_insights = json.load(f)
                else:
                    all_insights = []
                
                # Add today's insights
                all_insights.extend(domain_insights)
                
                # Keep only last 30 days
                cutoff_date = datetime.now() - timedelta(days=30)
                all_insights = [
                    insight for insight in all_insights
                    if datetime.fromisoformat(insight["timestamp"]) > cutoff_date
                ]
                
                # Save updated insights
                with open(insights_file, 'w') as f:
                    json.dump(all_insights, f, indent=2, cls=NumpyEncoder)
                
                insights_generated += len(domain_insights)
                print(f"  ✓ Generated {len(domain_insights)} insights for {domain}")
        
        return insights_generated
    
    def update_refresh_status(self, results: Dict[str, Any]):
        """Update refresh status and timestamp"""
        # Update last update time
        with open(self.last_update_file, 'w') as f:
            json.dump({
                "last_update": datetime.now().isoformat(),
                "results": results
            }, f, indent=2)
        
        # Update central status file
        self.status_path.parent.mkdir(exist_ok=True)
        
        status = {
            "daily_refresh": {
                "last_run": datetime.now().isoformat(),
                "status": "success" if not results.get("errors") else "partial_success",
                "domains_updated": results.get("domains_updated", []),
                "items_processed": results.get("new_data_items", 0),
                "next_scheduled": (datetime.now() + timedelta(days=1)).isoformat()
            }
        }
        
        # Load existing status or create new
        if self.status_path.exists():
            with open(self.status_path, 'r') as f:
                existing_status = json.load(f)
            existing_status.update(status)
            status = existing_status
        
        with open(self.status_path, 'w') as f:
            json.dump(status, f, indent=2)


def main():
    """Main execution function"""
    try:
        refresh_agent = DailyIntelligenceRefresh()
        results = refresh_agent.run_daily_refresh()
        
        # Exit with appropriate code
        if results.get("status") == "skipped":
            print("\nℹ️  Refresh skipped (already run today)")
            sys.exit(0)
        elif results.get("errors"):
            print(f"\n⚠️  Refresh completed with errors: {results['errors']}")
            sys.exit(1)
        else:
            print("\n✅ Daily refresh completed successfully!")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()