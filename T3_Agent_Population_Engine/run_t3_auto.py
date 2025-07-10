#!/usr/bin/env python3
"""
Automatic T3 Processing Script
Runs T3 processing without user interaction
"""

import sys
sys.path.append('/Users/fernandox/Desktop/Core Agent Architecture/T3_Agent_Population_Engine')

from t3_chunked_processor import T3ChunkedProcessor
from pathlib import Path

def main():
    print("T3 Automatic Processing")
    print("======================\n")
    
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    processor = T3ChunkedProcessor(base_path, chunk_size=5)
    
    # Check current status
    checkpoint = processor.load_checkpoint()
    pending = processor.get_pending_files()
    
    print(f"Current Status:")
    print(f"  Processed files: {len(checkpoint['processed_files'])}")
    print(f"  Pending files: {len(pending)}")
    
    if pending:
        print(f"\nPending files to process:")
        for f in pending:
            print(f"  - {f.name}")
    
    # Process all pending files
    print("\nStarting automatic processing...\n")
    processor.process_all_pending()
    
    print("\nProcessing complete!")
    
    # Show final status
    from t3_status_monitor import display_status
    display_status(Path(base_path))

if __name__ == "__main__":
    main()
