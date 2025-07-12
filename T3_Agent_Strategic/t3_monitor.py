#!/usr/bin/env python3
"""
T3 Strategic Monitor - Watches for T2 analyses and processes them
"""

import time
import json
from pathlib import Path
from datetime import datetime, timedelta
import logging
from typing import Set, Dict, Any, List
import threading
import queue

from t3_strategic_agent import T3StrategicAgent


class T3Monitor:
    """Monitors T2 output and triggers T3 strategic processing"""
    
    def __init__(self, base_path: str, check_interval: int = 60):
        self.base_path = Path(base_path)
        self.t2_path = self.base_path / "T2_Analysis_Results"
        self.t3_agent = T3StrategicAgent(base_path)
        self.check_interval = check_interval
        
        # Track processed files
        self.processed_files = self._load_processed_files()
        
        # Processing queue
        self.processing_queue = queue.Queue()
        
        # Setup logging
        self.setup_logging()
        
        # Start monitoring
        self.monitoring = True
        self.monitor_thread = None
        self.processor_thread = None
        
    def setup_logging(self):
        """Setup logging"""
        log_path = self.base_path / "T3_Agent_Strategic" / "t3_monitor.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('T3-Monitor')
        
    def _load_processed_files(self) -> Set[str]:
        """Load list of already processed files"""
        processed_file = self.base_path / "T3_Agent_Strategic" / ".processed_files.json"
        if processed_file.exists():
            try:
                with open(processed_file, 'r') as f:
                    return set(json.load(f))
            except:
                return set()
        return set()
        
    def _save_processed_files(self):
        """Save list of processed files"""
        processed_file = self.base_path / "T3_Agent_Strategic" / ".processed_files.json"
        with open(processed_file, 'w') as f:
            json.dump(list(self.processed_files), f)
            
    def start(self):
        """Start monitoring"""
        self.logger.info("Starting T3 Strategic Monitor")
        
        # Start monitor thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # Start processor thread
        self.processor_thread = threading.Thread(target=self._processor_loop, daemon=True)
        self.processor_thread.start()
        
        self.logger.info(f"Monitoring T2 output directory: {self.t2_path}")
        
    def stop(self):
        """Stop monitoring"""
        self.logger.info("Stopping T3 Monitor")
        self.monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        if self.processor_thread:
            self.processor_thread.join(timeout=5)
            
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Check for new T2 analyses
                new_files = self._check_for_new_files()
                
                if new_files:
                    self.logger.info(f"Found {len(new_files)} new T2 analyses")
                    
                    # Group by time window for batch processing
                    batches = self._group_files_by_time(new_files)
                    
                    for batch in batches:
                        self.processing_queue.put(batch)
                        
                # Sleep before next check
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {e}")
                time.sleep(self.check_interval)
                
    def _check_for_new_files(self) -> List[Path]:
        """Check for new T2 analysis files"""
        new_files = []
        
        if not self.t2_path.exists():
            return new_files
            
        for file in self.t2_path.glob("*.json"):
            if file.name not in self.processed_files:
                # Verify it's a valid T2 analysis
                if self._is_valid_t2_file(file):
                    new_files.append(file)
                    
        return new_files
        
    def _is_valid_t2_file(self, file: Path) -> bool:
        """Check if file is a valid T2 analysis"""
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                # Check for required T2 fields
                return all(key in data for key in ['analysis_id', 'analysis_type', 'confidence_score'])
        except:
            return False
            
    def _group_files_by_time(self, files: List[Path]) -> List[List[str]]:
        """Group files by time window for batch processing"""
        # Group files created within 5 minutes of each other
        time_window = 300  # 5 minutes
        
        # Sort by modification time
        files_with_time = [(f, f.stat().st_mtime) for f in files]
        files_with_time.sort(key=lambda x: x[1])
        
        batches = []
        current_batch = []
        current_window_start = None
        
        for file, mtime in files_with_time:
            if current_window_start is None or mtime - current_window_start <= time_window:
                if current_window_start is None:
                    current_window_start = mtime
                current_batch.append(file.stem)  # Use file stem as analysis ID
            else:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [file.stem]
                current_window_start = mtime
                
        if current_batch:
            batches.append(current_batch)
            
        return batches
        
    def _processor_loop(self):
        """Process T2 analyses from queue"""
        while self.monitoring:
            try:
                # Get batch from queue (timeout to allow checking monitoring flag)
                try:
                    batch = self.processing_queue.get(timeout=5)
                except queue.Empty:
                    continue
                    
                self.logger.info(f"Processing batch of {len(batch)} T2 analyses")
                
                # Process with T3 agent
                try:
                    structure = self.t3_agent.process_t2_analyses(analysis_ids=batch)
                    
                    if structure:
                        self.logger.info(f"Successfully created strategic structure: {structure['structure_id']}")
                        
                        # Mark files as processed
                        for analysis_id in batch:
                            # Find the actual file name
                            for file in self.t2_path.glob(f"*{analysis_id}*.json"):
                                self.processed_files.add(file.name)
                                
                        self._save_processed_files()
                        
                        # Notify about completion
                        self._notify_completion(structure)
                        
                except Exception as e:
                    self.logger.error(f"Error processing batch: {e}")
                    
            except Exception as e:
                self.logger.error(f"Error in processor loop: {e}")
                time.sleep(5)
                
    def _notify_completion(self, structure: Dict[str, Any]):
        """Notify about completed strategic structure"""
        # Log summary
        self.logger.info(f"Strategic Structure Summary:")
        self.logger.info(f"  ID: {structure['structure_id']}")
        self.logger.info(f"  Opportunities: {len(structure['strategic_insights']['opportunities'])}")
        self.logger.info(f"  Risks: {len(structure['strategic_insights']['risks'])}")
        self.logger.info(f"  Recommendations: {len(structure['strategic_insights']['recommendations'])}")
        self.logger.info(f"  Confidence: {structure['confidence_score']:.2%}")
        
        # Save notification
        notification = {
            'timestamp': datetime.now().isoformat(),
            'structure_id': structure['structure_id'],
            'summary': {
                'opportunities': len(structure['strategic_insights']['opportunities']),
                'risks': len(structure['strategic_insights']['risks']),
                'recommendations': len(structure['strategic_insights']['recommendations']),
                'confidence': structure['confidence_score']
            },
            'market_narrative': structure['market_narrative']['summary']
        }
        
        notification_file = self.base_path / "T3_Agent_Strategic" / "notifications" / f"{structure['structure_id']}_notification.json"
        notification_file.parent.mkdir(exist_ok=True)
        
        with open(notification_file, 'w') as f:
            json.dump(notification, f, indent=2)
            
    def get_status(self) -> Dict[str, Any]:
        """Get monitor status"""
        return {
            'monitoring': self.monitoring,
            'processed_files': len(self.processed_files),
            'queue_size': self.processing_queue.qsize(),
            'check_interval': self.check_interval,
            't2_path': str(self.t2_path),
            'last_check': datetime.now().isoformat()
        }
        
    def process_all_pending(self):
        """Process all pending T2 analyses immediately"""
        new_files = self._check_for_new_files()
        
        if not new_files:
            self.logger.info("No pending T2 analyses to process")
            return
            
        self.logger.info(f"Processing {len(new_files)} pending T2 analyses")
        
        # Process all as one batch
        analysis_ids = [f.stem for f in new_files]
        
        try:
            structure = self.t3_agent.process_t2_analyses(analysis_ids=analysis_ids)
            
            if structure:
                # Mark as processed
                for file in new_files:
                    self.processed_files.add(file.name)
                self._save_processed_files()
                
                self._notify_completion(structure)
                
                return structure
                
        except Exception as e:
            self.logger.error(f"Error processing pending analyses: {e}")
            raise


def main():
    """Run T3 Monitor"""
    import sys
    
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
        
    # Create monitor
    monitor = T3Monitor(base_path, check_interval=30)  # Check every 30 seconds
    
    print("\n" + "="*60)
    print("T3 STRATEGIC MONITOR")
    print("="*60)
    
    # Start monitoring
    monitor.start()
    
    print(f"\n✓ Monitoring started")
    print(f"  T2 Path: {monitor.t2_path}")
    print(f"  Check interval: {monitor.check_interval} seconds")
    print(f"  Previously processed: {len(monitor.processed_files)} files")
    
    print("\nMonitor is running. Press Ctrl+C to stop.")
    print("\nCommands:")
    print("  s - Show status")
    print("  p - Process all pending immediately")
    print("  q - Quit")
    
    try:
        while True:
            command = input("\nCommand: ").strip().lower()
            
            if command == 's':
                status = monitor.get_status()
                print(f"\nMonitor Status:")
                print(f"  Active: {status['monitoring']}")
                print(f"  Processed files: {status['processed_files']}")
                print(f"  Queue size: {status['queue_size']}")
                
            elif command == 'p':
                print("\nProcessing all pending analyses...")
                structure = monitor.process_all_pending()
                if structure:
                    print(f"✓ Created structure: {structure['structure_id']}")
                    
            elif command == 'q':
                print("\nStopping monitor...")
                break
                
            else:
                print("Unknown command. Use 's', 'p', or 'q'")
                
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        
    finally:
        monitor.stop()
        print("\n✓ Monitor stopped")
        print("="*60)


if __name__ == "__main__":
    main()