#!/usr/bin/env python3
"""
Simple T2 Monitoring Script
Checks for new T2 completions and processes them
"""

import json
import time
from pathlib import Path
from datetime import datetime


def check_t2_status():
    """Check T2 processing status"""
    base_path = Path("/Users/fernandox/Desktop/Core Agent Architecture")
    status_file = base_path / "Processing_Status" / "t2_processing_status.json"
    
    if not status_file.exists():
        print("No T2 status file found")
        return None
        
    with open(status_file, 'r') as f:
        status = json.load(f)
    
    # Find unprocessed files
    unprocessed = []
    for file_info in status.get('completed_files', []):
        if not file_info.get('processed_by_t3', False):
            unprocessed.append(file_info)
    
    return unprocessed


def monitor_loop():
    """Main monitoring loop"""
    print("Starting T2 monitoring...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            # Check for new files
            unprocessed = check_t2_status()
            
            if unprocessed:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Found {len(unprocessed)} unprocessed T2 files:")
                for file_info in unprocessed:
                    print(f"  - {file_info['path']}")
                print("\nT3 engine will process these files...")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No new T2 completions")
            
            # Wait before next check
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    monitor_loop()
