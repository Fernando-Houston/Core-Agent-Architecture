#!/usr/bin/env python3
"""
T3 Status Monitor
Simple status monitoring for T3 processing
"""

import json
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, Any


def get_agent_stats(base_path: Path) -> Dict[str, Any]:
    """Get statistics for all agents"""
    kb_path = base_path / "Agent_Knowledge_Bases"
    stats = {}
    
    for agent_dir in kb_path.iterdir():
        if agent_dir.is_dir():
            agent_stats = {
                "kb_files": 0,
                "total_records": 0,
                "categories": []
            }
            
            # Count KB files and records
            for kb_file in agent_dir.glob("*_knowledge.json"):
                agent_stats['kb_files'] += 1
                agent_stats['categories'].append(kb_file.stem.replace('_knowledge', ''))
                
                try:
                    with open(kb_file, 'r') as f:
                        knowledge = json.load(f)
                        agent_stats['total_records'] += len(knowledge)
                except:
                    pass
                    
            stats[agent_dir.name] = agent_stats
            
    return stats


def display_status(base_path: Path):
    """Display current T3 status"""
    print("\n" + "="*60)
    print(f"T3 Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Check master index
    master_index = base_path / "Agent_Knowledge_Bases" / "master_index.json"
    if master_index.exists():
        with open(master_index, 'r') as f:
            index = json.load(f)
            print(f"\nTotal Intelligence Records: {index.get('total_records', 0)}")
            print(f"Last Index Update: {index.get('generated_at', 'Unknown')}")
    
    # Get agent statistics
    print("\nAgent Knowledge Bases:")
    print("-"*60)
    
    stats = get_agent_stats(base_path)
    for agent, data in stats.items():
        print(f"\n{agent}:")
        print(f"  Records: {data['total_records']}")
        print(f"  Categories: {', '.join(data['categories']) if data['categories'] else 'None'}")
    
    # Check checkpoint
    checkpoint_file = base_path / "Processing_Status" / "t3_checkpoint.json"
    if checkpoint_file.exists():
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
            print(f"\n\nProcessing Checkpoint:")
            print(f"  Processed Files: {len(checkpoint.get('processed_files', []))}")
            print(f"  Last Update: {checkpoint.get('last_update', 'Unknown')}")
    
    # Check for pending T2 files
    t2_path = base_path / "T2_Intelligence_Output"
    if t2_path.exists():
        t2_files = list(t2_path.glob("*.json"))
        if checkpoint_file.exists():
            processed = set(checkpoint.get('processed_files', []))
            pending = [f for f in t2_files if str(f) not in processed]
            print(f"\n\nT2 Files:")
            print(f"  Total: {len(t2_files)}")
            print(f"  Pending: {len(pending)}")
        else:
            print(f"\n\nT2 Files: {len(t2_files)} found")


def monitor_loop(base_path: Path, interval: int = 30):
    """Continuous monitoring loop"""
    print("Starting T3 Status Monitor")
    print(f"Checking every {interval} seconds")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            display_status(base_path)
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(interval)


if __name__ == "__main__":
    import sys
    
    base_path = Path("/Users/fernandox/Desktop/Core Agent Architecture")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        display_status(base_path)
    else:
        monitor_loop(base_path)
