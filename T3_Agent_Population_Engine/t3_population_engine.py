#!/usr/bin/env python3
"""
T3 Agent Population Engine
Knowledge Architecture System for Houston Development Intelligence Platform

Transforms T2 intelligence insights into structured AI agent knowledge bases
"""

import json
import os
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import time
from dataclasses import dataclass, asdict
from collections import defaultdict
import re


@dataclass
class IntelligenceRecord:
    """Structured intelligence record for agent knowledge bases"""
    id: str
    timestamp: str
    source_file: str
    domain: str
    category: str
    subcategory: str
    title: str
    content: Dict[str, Any]
    tags: List[str]
    relationships: List[str]
    confidence_score: float
    data_points: List[Dict[str, Any]]
    geographic_scope: List[str]
    temporal_relevance: str
    cross_references: List[str]


class T3PopulationEngine:
    """Main engine for populating agent knowledge bases"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.agents_path = self.base_path / "6 Specialized Agents"
        self.t2_output_path = self.base_path / "T2_Intelligence_Output"
        self.knowledge_base_path = self.base_path / "Agent_Knowledge_Bases"
        self.status_path = self.base_path / "Processing_Status"
        
        # Create necessary directories
        self.knowledge_base_path.mkdir(exist_ok=True)
        self.status_path.mkdir(exist_ok=True)
        
        # Initialize logging
        self.setup_logging()
        
        # Agent configurations
        self.agent_configs = {
            "Market Intelligence": {
                "domains": ["competitive_analysis", "market_forecasts", "pricing_trends", "development_pipeline"],
                "schema_version": "1.0",
                "intelligence_types": ["market_metrics", "competitor_profiles", "trend_analysis", "opportunity_mapping"]
            },
            "Neighborhood Intelligence": {
                "domains": ["houston_heights", "katy_area", "sugar_land", "the_woodlands", "other_neighborhoods"],
                "schema_version": "1.0",
                "intelligence_types": ["demographic_insights", "development_patterns", "growth_indicators", "community_profiles"]
            },
            "Financial Intelligence": {
                "domains": ["financing_options", "investment_analysis", "lending_trends", "tax_implications"],
                "schema_version": "1.0",
                "intelligence_types": ["roi_analysis", "funding_sources", "market_valuations", "financial_forecasts"]
            },
            "Environmental Intelligence": {
                "domains": ["air_quality", "coastal_protection", "environmental_regulations", "flood_risk_data"],
                "schema_version": "1.0",
                "intelligence_types": ["risk_assessments", "compliance_requirements", "mitigation_strategies", "environmental_impacts"]
            },
            "Regulatory Intelligence": {
                "domains": ["compliance_tracking", "permit_requirements", "planning_commission", "zoning_data"],
                "schema_version": "1.0",
                "intelligence_types": ["regulatory_updates", "compliance_checklists", "approval_processes", "zoning_changes"]
            },
            "Technology & Innovation Intelligence": {
                "domains": ["Innovation_districts", "development_technologies", "investment_flows", "smart_city_initiatives"],
                "schema_version": "1.0",
                "intelligence_types": ["tech_trends", "innovation_metrics", "smart_solutions", "digital_infrastructure"]
            }
        }
        
        # Cross-domain mappings
        self.cross_domain_mappings = defaultdict(list)
        
        # Processing statistics
        self.stats = {
            "files_processed": 0,
            "records_created": 0,
            "agents_populated": 0,
            "cross_references": 0,
            "start_time": datetime.datetime.now().isoformat()
        }
    
    def setup_logging(self):
        """Configure logging for the engine"""
        log_file = self.status_path / f"t3_engine_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('T3PopulationEngine')
        self.logger.info("T3 Agent Population Engine initialized")
    
    def monitor_t2_completions(self) -> List[Path]:
        """Monitor T2 output directory for completed analysis files"""
        if not self.t2_output_path.exists():
            self.t2_output_path.mkdir(exist_ok=True)
            
        completed_files = []
        status_file = self.status_path / "t2_processing_status.json"
        
        if status_file.exists():
            with open(status_file, 'r') as f:
                status_data = json.load(f)
                
            for file_info in status_data.get('completed_files', []):
                file_path = Path(file_info['path'])
                if file_path.exists() and file_info.get('processed_by_t3', False) == False:
                    completed_files.append(file_path)
        
        self.logger.info(f"Found {len(completed_files)} new T2 completions to process")
        return completed_files
    
    def generate_record_id(self, content: Dict[str, Any]) -> str:
        """Generate unique ID for intelligence record"""
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.md5(content_str.encode()).hexdigest()[:12]
    
    def extract_intelligence_from_t2(self, file_path: Path) -> List[IntelligenceRecord]:
        """Extract and structure intelligence from T2 analysis files"""
        records = []
        
        try:
            with open(file_path, 'r') as f:
                t2_data = json.load(f)
            
            # Process each intelligence insight
            for insight in t2_data.get('insights', []):
                record = IntelligenceRecord(
                    id=self.generate_record_id(insight),
                    timestamp=datetime.datetime.now().isoformat(),
                    source_file=str(file_path),
                    domain=insight.get('domain', 'general'),
                    category=insight.get('category', 'uncategorized'),
                    subcategory=insight.get('subcategory', ''),
                    title=insight.get('title', 'Untitled'),
                    content=insight.get('content', {}),
                    tags=insight.get('tags', []),
                    relationships=insight.get('relationships', []),
                    confidence_score=insight.get('confidence_score', 0.8),
                    data_points=insight.get('data_points', []),
                    geographic_scope=insight.get('geographic_scope', ['Houston']),
                    temporal_relevance=insight.get('temporal_relevance', '2024-2025'),
                    cross_references=[]
                )
                records.append(record)
                
        except Exception as e:
            self.logger.error(f"Error processing T2 file {file_path}: {str(e)}")
            
        return records
    
    def determine_agent_assignment(self, record: IntelligenceRecord) -> List[str]:
        """Determine which agents should receive this intelligence"""
        assigned_agents = []
        
        # Primary assignment based on domain
        for agent_name, config in self.agent_configs.items():
            if record.domain in config['domains']:
                assigned_agents.append(agent_name)
                
        # Secondary assignment based on tags and content
        content_text = json.dumps(record.content).lower()
        
        # Market Intelligence keywords
        if any(keyword in content_text for keyword in ['market', 'price', 'competitive', 'forecast']):
            if "Market Intelligence" not in assigned_agents:
                assigned_agents.append("Market Intelligence")
                
        # Financial Intelligence keywords
        if any(keyword in content_text for keyword in ['investment', 'roi', 'financing', 'tax']):
            if "Financial Intelligence" not in assigned_agents:
                assigned_agents.append("Financial Intelligence")
                
        # Environmental Intelligence keywords
        if any(keyword in content_text for keyword in ['flood', 'environmental', 'risk', 'coastal']):
            if "Environmental Intelligence" not in assigned_agents:
                assigned_agents.append("Environmental Intelligence")
                
        # Regulatory Intelligence keywords
        if any(keyword in content_text for keyword in ['zoning', 'permit', 'regulation', 'compliance']):
            if "Regulatory Intelligence" not in assigned_agents:
                assigned_agents.append("Regulatory Intelligence")
                
        # Technology Intelligence keywords
        if any(keyword in content_text for keyword in ['innovation', 'technology', 'smart', 'digital']):
            if "Technology & Innovation Intelligence" not in assigned_agents:
                assigned_agents.append("Technology & Innovation Intelligence")
                
        return assigned_agents if assigned_agents else ["Market Intelligence"]  # Default assignment
    
    def create_cross_references(self, records: List[IntelligenceRecord]):
        """Create cross-references between related intelligence records"""
        for i, record1 in enumerate(records):
            for j, record2 in enumerate(records[i+1:], i+1):
                # Check for common tags
                common_tags = set(record1.tags) & set(record2.tags)
                if len(common_tags) >= 2:
                    record1.cross_references.append(record2.id)
                    record2.cross_references.append(record1.id)
                    self.stats['cross_references'] += 1
                    
                # Check for geographic overlap
                common_geo = set(record1.geographic_scope) & set(record2.geographic_scope)
                if common_geo and record1.domain != record2.domain:
                    record1.cross_references.append(record2.id)
                    record2.cross_references.append(record1.id)
                    self.stats['cross_references'] += 1
    
    def populate_agent_knowledge_base(self, agent_name: str, records: List[IntelligenceRecord]):
        """Populate specific agent's knowledge base with structured intelligence"""
        agent_kb_path = self.knowledge_base_path / agent_name.replace(' ', '_')
        agent_kb_path.mkdir(exist_ok=True)
        
        # Group records by category
        categorized_records = defaultdict(list)
        for record in records:
            categorized_records[record.category].append(record)
        
        # Create knowledge base files
        for category, category_records in categorized_records.items():
            kb_file = agent_kb_path / f"{category}_knowledge.json"
            
            # Load existing knowledge if file exists
            existing_knowledge = {}
            if kb_file.exists():
                with open(kb_file, 'r') as f:
                    existing_knowledge = json.load(f)
            
            # Update with new records
            for record in category_records:
                existing_knowledge[record.id] = asdict(record)
            
            # Save updated knowledge base
            with open(kb_file, 'w') as f:
                json.dump(existing_knowledge, f, indent=2)
            
            self.logger.info(f"Updated {agent_name} - {category}: {len(category_records)} new records")
        
        # Create agent metadata
        metadata = {
            "agent_name": agent_name,
            "last_updated": datetime.datetime.now().isoformat(),
            "total_records": sum(len(recs) for recs in categorized_records.values()),
            "categories": list(categorized_records.keys()),
            "schema_version": self.agent_configs[agent_name]['schema_version']
        }
        
        with open(agent_kb_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def generate_intelligence_index(self):
        """Generate master index of all intelligence records"""
        index = {
            "generated_at": datetime.datetime.now().isoformat(),
            "total_records": self.stats['records_created'],
            "agents": {},
            "cross_domain_mappings": dict(self.cross_domain_mappings),
            "geographic_index": defaultdict(list),
            "temporal_index": defaultdict(list),
            "tag_index": defaultdict(list)
        }
        
        # Build comprehensive index
        for agent_name in self.agent_configs.keys():
            agent_kb_path = self.knowledge_base_path / agent_name.replace(' ', '_')
            if agent_kb_path.exists():
                agent_records = []
                for kb_file in agent_kb_path.glob("*_knowledge.json"):
                    with open(kb_file, 'r') as f:
                        records = json.load(f)
                        agent_records.extend(records.keys())
                        
                        # Build auxiliary indexes
                        for record_id, record_data in records.items():
                            for geo in record_data.get('geographic_scope', []):
                                index['geographic_index'][geo].append(record_id)
                            
                            index['temporal_index'][record_data.get('temporal_relevance', 'unknown')].append(record_id)
                            
                            for tag in record_data.get('tags', []):
                                index['tag_index'][tag].append(record_id)
                
                index['agents'][agent_name] = {
                    "record_count": len(agent_records),
                    "record_ids": agent_records
                }
        
        # Save master index
        with open(self.knowledge_base_path / "master_index.json", 'w') as f:
            json.dump(index, f, indent=2)
        
        self.logger.info("Generated master intelligence index")
    
    def process_t2_completions(self):
        """Main processing loop for T2 completions"""
        self.logger.info("Starting T2 completion processing")
        
        # Get new T2 files
        t2_files = self.monitor_t2_completions()
        
        if not t2_files:
            self.logger.info("No new T2 completions to process")
            return
        
        all_records = []
        
        # Process each T2 file
        for t2_file in t2_files:
            self.logger.info(f"Processing T2 file: {t2_file}")
            
            # Extract intelligence records
            records = self.extract_intelligence_from_t2(t2_file)
            all_records.extend(records)
            
            self.stats['files_processed'] += 1
            self.stats['records_created'] += len(records)
            
            # Mark file as processed
            self.mark_t2_file_processed(t2_file)
        
        # Create cross-references
        self.create_cross_references(all_records)
        
        # Assign and populate agents
        agent_assignments = defaultdict(list)
        for record in all_records:
            assigned_agents = self.determine_agent_assignment(record)
            for agent in assigned_agents:
                agent_assignments[agent].append(record)
                
                # Track cross-domain mappings
                if len(assigned_agents) > 1:
                    for other_agent in assigned_agents:
                        if other_agent != agent:
                            self.cross_domain_mappings[agent].append({
                                "record_id": record.id,
                                "shared_with": other_agent,
                                "reason": "multi-domain relevance"
                            })
        
        # Populate each agent's knowledge base
        for agent_name, records in agent_assignments.items():
            self.populate_agent_knowledge_base(agent_name, records)
            self.stats['agents_populated'] += 1
        
        # Generate master index
        self.generate_intelligence_index()
        
        # Update processing statistics
        self.update_processing_stats()
        
        self.logger.info(f"Processing complete. Created {self.stats['records_created']} records across {self.stats['agents_populated']} agents")
    
    def mark_t2_file_processed(self, file_path: Path):
        """Mark T2 file as processed by T3"""
        status_file = self.status_path / "t2_processing_status.json"
        
        if status_file.exists():
            with open(status_file, 'r') as f:
                status_data = json.load(f)
            
            for file_info in status_data.get('completed_files', []):
                if file_info['path'] == str(file_path):
                    file_info['processed_by_t3'] = True
                    file_info['t3_timestamp'] = datetime.datetime.now().isoformat()
            
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
    
    def update_processing_stats(self):
        """Update processing statistics"""
        self.stats['end_time'] = datetime.datetime.now().isoformat()
        stats_file = self.status_path / f"t3_stats_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        self.logger.info(f"Processing statistics saved to {stats_file}")
    
    def continuous_monitoring(self, check_interval: int = 30):
        """Continuously monitor for T2 completions"""
        self.logger.info(f"Starting continuous monitoring (check every {check_interval} seconds)")
        
        while True:
            try:
                self.process_t2_completions()
                self.logger.info(f"Waiting {check_interval} seconds before next check...")
                time.sleep(check_interval)
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(check_interval)


if __name__ == "__main__":
    # Initialize T3 Population Engine
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    engine = T3PopulationEngine(base_path)
    
    # Start continuous monitoring
    engine.continuous_monitoring(check_interval=30)
