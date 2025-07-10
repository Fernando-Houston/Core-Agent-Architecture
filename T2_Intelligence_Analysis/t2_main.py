#!/usr/bin/env python3
"""
T2 Intelligence Analysis Engine - Main orchestrator
Monitors T1 completions and generates sophisticated market intelligence
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add to Python path
sys.path.append(str(Path(__file__).parent))

from monitoring.t1_monitor import T1Monitor
from config.analysis_config import DOMAIN_CONFIG, SHARED_STATE_PATH, T2_OUTPUTS_PATH
from analysis_engines.market_intelligence.market_analyzer import MarketIntelligenceAnalyzer
from analysis_engines.neighborhood_intelligence.neighborhood_analyzer import NeighborhoodIntelligenceAnalyzer
from analysis_engines.financial_intelligence.financial_analyzer import FinancialIntelligenceAnalyzer
from analysis_engines.environmental_intelligence.environmental_analyzer import EnvironmentalIntelligenceAnalyzer
from analysis_engines.regulatory_intelligence.regulatory_analyzer import RegulatoryIntelligenceAnalyzer
from analysis_engines.technology_intelligence.technology_analyzer import TechnologyIntelligenceAnalyzer


class T2IntelligenceEngine:
    """Main T2 Intelligence Analysis Engine"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_directories()
        self.monitor = T1Monitor(SHARED_STATE_PATH)
        self.analyzers = self.initialize_analyzers()
        self.processing_stats = {
            "domains_processed": 0,
            "analysis_completed": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat()
        }
        
    def setup_logging(self):
        """Setup main logger"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "t2_main.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("T2.Main")
        
    def setup_directories(self):
        """Ensure all directories exist"""
        Path(T2_OUTPUTS_PATH).mkdir(parents=True, exist_ok=True)
        
    def initialize_analyzers(self) -> Dict[str, Any]:
        """Initialize domain analyzers"""
        analyzers = {}
        
        # Initialize all available analyzers
        analyzers["market_intelligence"] = MarketIntelligenceAnalyzer(
            DOMAIN_CONFIG["market_intelligence"]
        )
        
        analyzers["neighborhood_intelligence"] = NeighborhoodIntelligenceAnalyzer(
            DOMAIN_CONFIG["neighborhood_intelligence"]
        )
        
        analyzers["financial_intelligence"] = FinancialIntelligenceAnalyzer(
            DOMAIN_CONFIG["financial_intelligence"]
        )
        
        analyzers["environmental_intelligence"] = EnvironmentalIntelligenceAnalyzer(
            DOMAIN_CONFIG["environmental_intelligence"]
        )
        
        analyzers["regulatory_intelligence"] = RegulatoryIntelligenceAnalyzer(
            DOMAIN_CONFIG["regulatory_intelligence"]
        )
        
        analyzers["technology_intelligence"] = TechnologyIntelligenceAnalyzer(
            DOMAIN_CONFIG["technology_intelligence"]
        )
        
        self.logger.info(f"Initialized {len(analyzers)} domain analyzers")
        return analyzers
    
    def process_domain(self, domain_info: Dict[str, Any]) -> Optional[str]:
        """Process a single domain's extracted data"""
        domain = domain_info["domain"]
        self.logger.info(f"Processing domain: {domain} (Priority: {domain_info['priority']})")
        
        try:
            # Get appropriate analyzer
            analyzer = self.analyzers.get(domain)
            if not analyzer:
                self.logger.warning(f"No analyzer available for domain: {domain}")
                return None
            
            # Load extracted data
            input_file = domain_info["output_file"]
            if not Path(input_file).exists():
                self.logger.error(f"Input file not found: {input_file}")
                return None
            
            # Perform analysis
            result = analyzer.analyze(input_file)
            
            # Save results
            output_file = analyzer.save_results(result, T2_OUTPUTS_PATH)
            
            # Update stats
            self.processing_stats["analysis_completed"] += 1
            
            # Queue for T3
            self.queue_for_t3(domain, output_file, result)
            
            self.logger.info(f"Successfully analyzed {domain}. Confidence: {result.confidence_score:.2f}")
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error processing {domain}: {e}")
            self.processing_stats["errors"] += 1
            return None
    
    def queue_for_t3(self, domain: str, output_file: str, result: Any):
        """Queue analysis results for T3 agent population"""
        t3_queue_file = Path(SHARED_STATE_PATH) / "t3_agent_queue" / f"{domain}_ready.json"
        t3_queue_file.parent.mkdir(exist_ok=True)
        
        queue_entry = {
            "domain": domain,
            "analysis_file": output_file,
            "timestamp": datetime.now().isoformat(),
            "confidence": result.confidence_score,
            "key_metrics": result.metrics,
            "priority": DOMAIN_CONFIG.get(domain, {}).get("priority", "medium"),
            "status": "ready_for_agent_population"
        }
        
        with open(t3_queue_file, 'w') as f:
            json.dump(queue_entry, f, indent=2)
        
        self.logger.info(f"Queued {domain} for T3 agent population")
    
    def update_status(self):
        """Update T2 status for monitoring"""
        status_file = Path(SHARED_STATE_PATH) / "t2_analysis_status.json"
        
        status = {
            "engine": "T2_Intelligence_Analysis",
            "status": "running",
            "stats": self.processing_stats,
            "domains_ready": list(self.analyzers.keys()),
            "last_update": datetime.now().isoformat()
        }
        
        with open(status_file, 'w') as f:
            json.dump(status, f, indent=2)
    
    def run(self):
        """Main processing loop"""
        self.logger.info("Starting T2 Intelligence Analysis Engine")
        self.logger.info(f"Monitoring T1 extractions at: {SHARED_STATE_PATH}")
        
        # Start monitoring
        self.monitor.start()
        
        try:
            while True:
                # Check for completed extractions
                next_domain = self.monitor.get_next_for_analysis()
                
                if next_domain:
                    self.processing_stats["domains_processed"] += 1
                    self.process_domain(next_domain)
                    self.update_status()
                else:
                    # No new domains, wait
                    time.sleep(5)
                
                # Periodic status update
                if self.processing_stats["domains_processed"] % 5 == 0:
                    self.log_progress()
                    
        except KeyboardInterrupt:
            self.logger.info("Shutting down T2 Engine...")
        finally:
            self.monitor.stop()
            self.final_report()
    
    def log_progress(self):
        """Log current progress"""
        self.logger.info(
            f"Progress: Processed {self.processing_stats['domains_processed']} domains, "
            f"Completed {self.processing_stats['analysis_completed']} analyses, "
            f"Errors: {self.processing_stats['errors']}"
        )
    
    def final_report(self):
        """Generate final report"""
        runtime = (datetime.now() - datetime.fromisoformat(self.processing_stats["start_time"])).total_seconds() / 60
        
        self.logger.info("=" * 50)
        self.logger.info("T2 Intelligence Analysis Engine - Final Report")
        self.logger.info(f"Runtime: {runtime:.1f} minutes")
        self.logger.info(f"Domains Processed: {self.processing_stats['domains_processed']}")
        self.logger.info(f"Analyses Completed: {self.processing_stats['analysis_completed']}")
        self.logger.info(f"Errors: {self.processing_stats['errors']}")
        self.logger.info(f"Success Rate: {(self.processing_stats['analysis_completed'] / max(self.processing_stats['domains_processed'], 1) * 100):.1f}%")
        self.logger.info("=" * 50)


if __name__ == "__main__":
    engine = T2IntelligenceEngine()
    engine.run()