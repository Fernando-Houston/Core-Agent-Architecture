#!/usr/bin/env python3
"""
T1 Extraction Monitor - Monitors T1's completion status and triggers analysis
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import threading
import queue

class T1Monitor:
    def __init__(self, shared_state_path: str, check_interval: int = 5):
        self.shared_state_path = Path(shared_state_path)
        self.check_interval = check_interval
        self.running = False
        self.analysis_queue = queue.Queue()
        self.processed_domains = set()
        
        # Setup logging
        log_path = Path(__file__).parent.parent / "logs"
        log_path.mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path / "t1_monitor.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("T1Monitor")
        
    def read_extraction_status(self) -> Optional[Dict]:
        """Read T1's extraction status file"""
        status_file = self.shared_state_path / "t1_extraction_status.json"
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error reading status file: {e}")
        return None
    
    def check_for_completions(self) -> List[Dict]:
        """Check for newly completed extractions"""
        status = self.read_extraction_status()
        if not status:
            return []
        
        new_completions = []
        for domain, info in status.get("domains", {}).items():
            if (info.get("status") == "completed" and 
                domain not in self.processed_domains and
                info.get("output_file")):
                
                new_completions.append({
                    "domain": domain,
                    "priority": info.get("priority", "medium"),
                    "completed_at": info.get("completed_at"),
                    "output_file": info.get("output_file"),
                    "stats": info.get("stats", {})
                })
                self.processed_domains.add(domain)
                
        return new_completions
    
    def monitor_loop(self):
        """Main monitoring loop"""
        self.logger.info("Starting T1 extraction monitoring...")
        
        while self.running:
            try:
                # Check for new completions
                new_completions = self.check_for_completions()
                
                # Sort by priority (high -> medium -> low)
                priority_order = {"high": 0, "medium": 1, "low": 2}
                new_completions.sort(key=lambda x: priority_order.get(x["priority"], 3))
                
                # Queue for analysis
                for completion in new_completions:
                    self.logger.info(f"New extraction completed: {completion['domain']} "
                                   f"(Priority: {completion['priority']})")
                    self.analysis_queue.put(completion)
                
                # Log current status
                status = self.read_extraction_status()
                if status:
                    total = len(status.get("domains", {}))
                    completed = len(self.processed_domains)
                    self.logger.info(f"Progress: {completed}/{total} domains processed")
                
            except Exception as e:
                self.logger.error(f"Monitor error: {e}")
            
            time.sleep(self.check_interval)
    
    def start(self):
        """Start monitoring"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.start()
        self.logger.info("T1 Monitor started")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
        self.logger.info("T1 Monitor stopped")
    
    def get_next_for_analysis(self) -> Optional[Dict]:
        """Get next domain ready for analysis"""
        try:
            return self.analysis_queue.get_nowait()
        except queue.Empty:
            return None


if __name__ == "__main__":
    # Test monitor
    shared_state = "/Users/fernandox/Desktop/Core Agent Architecture/shared_state"
    monitor = T1Monitor(shared_state)
    
    try:
        monitor.start()
        # Keep running
        while True:
            time.sleep(10)
            next_domain = monitor.get_next_for_analysis()
            if next_domain:
                print(f"Ready for analysis: {next_domain}")
    except KeyboardInterrupt:
        monitor.stop()