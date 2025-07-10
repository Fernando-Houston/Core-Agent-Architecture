#!/usr/bin/env python3
"""
T3 Chunked Processor
Processes T2 intelligence in small chunks to avoid API errors
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from collections import defaultdict


class T3ChunkedProcessor:
    """Processes T2 intelligence in manageable chunks"""
    
    def __init__(self, base_path: str, chunk_size: int = 5):
        self.base_path = Path(base_path)
        self.chunk_size = chunk_size
        self.t2_output_path = self.base_path / "T2_Intelligence_Output"
        self.kb_path = self.base_path / "Agent_Knowledge_Bases"
        self.status_path = self.base_path / "Processing_Status"
        self.checkpoint_file = self.status_path / "t3_checkpoint.json"
        
        # Ensure directories exist
        self.kb_path.mkdir(exist_ok=True)
        self.status_path.mkdir(exist_ok=True)
        
        # Setup simple logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup basic logging"""
        log_file = self.status_path / f"t3_chunked_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('T3Chunked')
        
    def load_checkpoint(self) -> Dict[str, Any]:
        """Load processing checkpoint"""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {
            "processed_files": [],
            "processed_records": {},
            "last_update": None
        }
    
    def save_checkpoint(self, checkpoint: Dict[str, Any]):
        """Save processing checkpoint"""
        checkpoint['last_update'] = datetime.now().isoformat()
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
            
    def get_pending_files(self) -> List[Path]:
        """Get list of T2 files pending processing"""
        checkpoint = self.load_checkpoint()
        processed = set(checkpoint['processed_files'])
        
        pending = []
        if self.t2_output_path.exists():
            for file_path in self.t2_output_path.glob("*.json"):
                if str(file_path) not in processed:
                    pending.append(file_path)
                    
        return pending
    
    def process_file_in_chunks(self, file_path: Path) -> int:
        """Process a single T2 file in chunks"""
        self.logger.info(f"Processing file: {file_path.name}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            insights = data.get('insights', [])
            total_processed = 0
            
            # Process in chunks
            for i in range(0, len(insights), self.chunk_size):
                chunk = insights[i:i + self.chunk_size]
                self.logger.info(f"Processing chunk {i//self.chunk_size + 1} ({len(chunk)} insights)")
                
                # Process each insight in chunk
                for insight in chunk:
                    self.process_single_insight(insight, str(file_path))
                    total_processed += 1
                    
                # Small delay between chunks
                time.sleep(0.5)
                
            # Mark file as processed
            checkpoint = self.load_checkpoint()
            checkpoint['processed_files'].append(str(file_path))
            self.save_checkpoint(checkpoint)
            
            self.logger.info(f"Completed processing {total_processed} insights from {file_path.name}")
            return total_processed
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return 0
    
    def process_single_insight(self, insight: Dict[str, Any], source_file: str):
        """Process a single insight and populate appropriate agents"""
        # Determine which agents should receive this insight
        target_agents = self.determine_target_agents(insight)
        
        # Create knowledge record
        record = self.create_knowledge_record(insight, source_file)
        
        # Save to each target agent's knowledge base
        for agent in target_agents:
            self.save_to_agent_kb(agent, record)
            
    def determine_target_agents(self, insight: Dict[str, Any]) -> List[str]:
        """Determine which agents should receive an insight"""
        domain = insight.get('domain', '')
        tags = insight.get('tags', [])
        
        agents = []
        
        # Domain-based assignment
        domain_map = {
            'market': 'Market_Intelligence',
            'neighborhood': 'Neighborhood_Intelligence',
            'financial': 'Financial_Intelligence',
            'environmental': 'Environmental_Intelligence',
            'regulatory': 'Regulatory_Intelligence',
            'technology': 'Technology_Innovation_Intelligence'
        }
        
        for key, agent in domain_map.items():
            if key in domain.lower():
                agents.append(agent)
                
        # Tag-based assignment
        tag_map = {
            'roi': 'Financial_Intelligence',
            'investment': 'Financial_Intelligence',
            'zoning': 'Regulatory_Intelligence',
            'flood': 'Environmental_Intelligence',
            'innovation': 'Technology_Innovation_Intelligence',
            'development': 'Market_Intelligence'
        }
        
        for tag in tags:
            for key, agent in tag_map.items():
                if key in tag.lower() and agent not in agents:
                    agents.append(agent)
                    
        # Default to Market Intelligence if no match
        if not agents:
            agents.append('Market_Intelligence')
            
        return agents
    
    def create_knowledge_record(self, insight: Dict[str, Any], source_file: str) -> Dict[str, Any]:
        """Create a structured knowledge record"""
        record_id = self.generate_record_id(insight)
        
        return {
            "id": record_id,
            "timestamp": datetime.now().isoformat(),
            "source_file": source_file,
            "domain": insight.get('domain', 'general'),
            "category": insight.get('category', 'uncategorized'),
            "subcategory": insight.get('subcategory', ''),
            "title": insight.get('title', 'Untitled'),
            "content": insight.get('content', {}),
            "tags": insight.get('tags', []),
            "relationships": insight.get('relationships', []),
            "confidence_score": insight.get('confidence_score', 0.8),
            "data_points": insight.get('data_points', []),
            "geographic_scope": insight.get('geographic_scope', ['Houston']),
            "temporal_relevance": insight.get('temporal_relevance', '2024-2025')
        }
    
    def generate_record_id(self, content: Dict[str, Any]) -> str:
        """Generate unique ID for a record"""
        import hashlib
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.md5(content_str.encode()).hexdigest()[:12]
    
    def save_to_agent_kb(self, agent: str, record: Dict[str, Any]):
        """Save record to agent's knowledge base"""
        agent_path = self.kb_path / agent
        agent_path.mkdir(exist_ok=True)
        
        # Determine KB file based on category
        category = record['category'].replace(' ', '_').lower()
        kb_file = agent_path / f"{category}_knowledge.json"
        
        # Load existing knowledge
        knowledge = {}
        if kb_file.exists():
            try:
                with open(kb_file, 'r') as f:
                    knowledge = json.load(f)
            except:
                knowledge = {}
                
        # Add new record
        knowledge[record['id']] = record
        
        # Save updated knowledge
        with open(kb_file, 'w') as f:
            json.dump(knowledge, f, indent=2)
            
        # Update metadata
        self.update_agent_metadata(agent_path, len(knowledge))
        
    def update_agent_metadata(self, agent_path: Path, record_count: int):
        """Update agent metadata file"""
        metadata_file = agent_path / "metadata.json"
        
        metadata = {
            "agent_name": agent_path.name,
            "last_updated": datetime.now().isoformat(),
            "total_records": record_count,
            "schema_version": "1.0"
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    def process_all_pending(self):
        """Process all pending T2 files"""
        pending_files = self.get_pending_files()
        
        if not pending_files:
            self.logger.info("No pending files to process")
            return
            
        self.logger.info(f"Found {len(pending_files)} pending files")
        
        total_insights = 0
        for file_path in pending_files:
            count = self.process_file_in_chunks(file_path)
            total_insights += count
            
            # Longer delay between files
            time.sleep(2)
            
        self.logger.info(f"Processing complete. Total insights processed: {total_insights}")
        
        # Update master index
        self.update_master_index()
        
    def update_master_index(self):
        """Update the master intelligence index"""
        self.logger.info("Updating master index...")
        
        index = {
            "generated_at": datetime.now().isoformat(),
            "agents": {},
            "total_records": 0
        }
        
        # Scan all agent directories
        for agent_dir in self.kb_path.iterdir():
            if agent_dir.is_dir():
                agent_name = agent_dir.name
                record_count = 0
                
                # Count records in all KB files
                for kb_file in agent_dir.glob("*_knowledge.json"):
                    try:
                        with open(kb_file, 'r') as f:
                            knowledge = json.load(f)
                            record_count += len(knowledge)
                    except:
                        pass
                        
                index['agents'][agent_name] = {
                    "record_count": record_count
                }
                index['total_records'] += record_count
                
        # Save master index
        index_file = self.kb_path / "master_index.json"
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
            
        self.logger.info(f"Master index updated. Total records: {index['total_records']}")


def main():
    """Main execution function"""
    print("T3 Chunked Processor - Houston Development Intelligence")
    print("======================================================")
    
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    processor = T3ChunkedProcessor(base_path, chunk_size=5)
    
    while True:
        print("\nOptions:")
        print("1. Process all pending T2 files")
        print("2. Check processing status")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ")
        
        if choice == '1':
            processor.process_all_pending()
        elif choice == '2':
            checkpoint = processor.load_checkpoint()
            pending = processor.get_pending_files()
            print(f"\nProcessed files: {len(checkpoint['processed_files'])}")
            print(f"Pending files: {len(pending)}")
            if checkpoint['last_update']:
                print(f"Last update: {checkpoint['last_update']}")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
