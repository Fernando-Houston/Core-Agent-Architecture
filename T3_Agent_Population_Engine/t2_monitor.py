#!/usr/bin/env python3
"""
Advanced T2 Completion Monitor
Real-time monitoring system for T2 analysis completions with intelligent processing
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from collections import defaultdict


class T2CompletionHandler(FileSystemEventHandler):
    """Handles file system events for T2 completions"""
    
    def __init__(self, callback_func):
        self.callback_func = callback_func
        self.processed_files = set()
        
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            file_hash = self._get_file_hash(event.src_path)
            if file_hash not in self.processed_files:
                self.processed_files.add(file_hash)
                self.callback_func(event.src_path)
                
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            # Check if file content actually changed
            file_hash = self._get_file_hash(event.src_path)
            if file_hash not in self.processed_files:
                self.processed_files.add(file_hash)
                self.callback_func(event.src_path)
                
    def _get_file_hash(self, file_path: str) -> str:
        """Get hash of file content to detect real changes"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""


class T2CompletionMonitor:
    """Advanced monitoring system for T2 analysis completions"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.t2_output_path = self.base_path / "T2_Intelligence_Output"
        self.status_path = self.base_path / "Processing_Status"
        self.monitor_log_path = self.status_path / "t2_monitor.log"
        
        # Setup logging
        self.setup_logging()
        
        # Processing queue
        self.processing_queue = []
        self.processing_stats = defaultdict(int)
        
        # Intelligence type patterns
        self.intelligence_patterns = {
            "neighborhood": {
                "patterns": ["neighborhood", "area", "district", "location"],
                "required_fields": ["investment_score", "development_opportunities", "price_trajectory"]
            },
            "financial": {
                "patterns": ["financial", "investment", "roi", "financing"],
                "required_fields": ["roi_model", "financing_options", "risk_matrix"]
            },
            "market": {
                "patterns": ["market", "competitive", "pricing", "forecast"],
                "required_fields": ["market_analysis", "competitor_data", "price_trends"]
            },
            "environmental": {
                "patterns": ["environmental", "flood", "risk", "sustainability"],
                "required_fields": ["risk_assessment", "mitigation_strategies", "compliance"]
            },
            "regulatory": {
                "patterns": ["regulatory", "zoning", "permit", "compliance"],
                "required_fields": ["regulations", "requirements", "approval_process"]
            },
            "technology": {
                "patterns": ["technology", "innovation", "smart", "digital"],
                "required_fields": ["tech_features", "innovation_metrics", "implementation"]
            }
        }
        
    def setup_logging(self):
        """Configure advanced logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.monitor_log_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('T2Monitor')
        
    def start_file_system_monitoring(self):
        """Start real-time file system monitoring"""
        event_handler = T2CompletionHandler(self.process_new_t2_file)
        observer = Observer()
        observer.schedule(event_handler, str(self.t2_output_path), recursive=True)
        observer.start()
        self.logger.info(f"Started file system monitoring on {self.t2_output_path}")
        return observer
        
    def process_new_t2_file(self, file_path: str):
        """Process newly detected T2 file"""
        self.logger.info(f"New T2 file detected: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                t2_data = json.load(f)
                
            # Validate and classify the intelligence
            intelligence_type = self.classify_intelligence(t2_data)
            
            # Add to processing queue with metadata
            queue_item = {
                "file_path": file_path,
                "detected_at": datetime.now().isoformat(),
                "intelligence_type": intelligence_type,
                "priority": self.calculate_priority(t2_data, intelligence_type),
                "data": t2_data
            }
            
            self.processing_queue.append(queue_item)
            self.processing_stats[intelligence_type] += 1
            
            # Update status file
            self.update_monitoring_status(queue_item)
            
            self.logger.info(f"Added to queue: {intelligence_type} intelligence (priority: {queue_item['priority']})")
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            
    def classify_intelligence(self, t2_data: Dict[str, Any]) -> str:
        """Classify the type of intelligence based on content"""
        # Check insights for patterns
        content_text = json.dumps(t2_data).lower()
        
        scores = {}
        for intel_type, config in self.intelligence_patterns.items():
            score = sum(1 for pattern in config['patterns'] if pattern in content_text)
            scores[intel_type] = score
            
        # Return type with highest score
        return max(scores, key=scores.get) if scores else "general"
        
    def calculate_priority(self, t2_data: Dict[str, Any], intelligence_type: str) -> int:
        """Calculate processing priority (1-10, 10 being highest)"""
        priority = 5  # Default priority
        
        # Boost priority for certain types
        priority_boost = {
            "financial": 2,
            "neighborhood": 2,
            "regulatory": 1,
            "environmental": 1
        }
        
        priority += priority_boost.get(intelligence_type, 0)
        
        # Boost for high confidence scores
        insights = t2_data.get('insights', [])
        if insights:
            avg_confidence = sum(i.get('confidence_score', 0.5) for i in insights) / len(insights)
            if avg_confidence > 0.8:
                priority += 2
                
        # Boost for cross-domain intelligence
        domains = set()
        for insight in insights:
            domains.add(insight.get('domain', ''))
        if len(domains) > 2:
            priority += 1
            
        return min(priority, 10)  # Cap at 10
        
    def update_monitoring_status(self, queue_item: Dict[str, Any]):
        """Update the monitoring status file"""
        status_file = self.status_path / "t2_monitoring_status.json"
        
        try:
            if status_file.exists():
                with open(status_file, 'r') as f:
                    status = json.load(f)
            else:
                status = {
                    "last_updated": datetime.now().isoformat(),
                    "queue": [],
                    "processed": [],
                    "stats": {}
                }
                
            # Add to queue
            status['queue'].append({
                "file": os.path.basename(queue_item['file_path']),
                "type": queue_item['intelligence_type'],
                "priority": queue_item['priority'],
                "detected_at": queue_item['detected_at']
            })
            
            # Update stats
            status['stats'] = dict(self.processing_stats)
            status['last_updated'] = datetime.now().isoformat()
            
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error updating status: {str(e)}")
            
    def get_priority_queue(self) -> List[Dict[str, Any]]:
        """Get processing queue sorted by priority"""
        return sorted(self.processing_queue, key=lambda x: x['priority'], reverse=True)
        
    def process_neighborhood_intelligence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Special processing for neighborhood intelligence"""
        processed = {
            "investment_scores": {},
            "development_rankings": [],
            "price_trajectories": {},
            "infrastructure_impacts": {}
        }
        
        for insight in data.get('insights', []):
            if 'neighborhood' in insight.get('domain', ''):
                area = insight.get('geographic_scope', ['Unknown'])[0]
                
                # Calculate investment score
                metrics = insight.get('content', {}).get('metrics', {})
                investment_score = self._calculate_investment_score(metrics)
                processed['investment_scores'][area] = investment_score
                
                # Extract development opportunities
                if 'development' in insight.get('tags', []):
                    processed['development_rankings'].append({
                        "area": area,
                        "opportunity": insight.get('title'),
                        "score": investment_score,
                        "factors": insight.get('content', {}).get('key_findings', [])
                    })
                    
        return processed
        
    def _calculate_investment_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate investment score based on metrics"""
        score = 0.0
        
        # Factors that increase score
        score += metrics.get('growth_rate', 0) * 10
        score += metrics.get('demand_index', 0) * 5
        score += (100 - metrics.get('vacancy_rate', 100)) * 0.5
        
        # Factors that decrease score
        score -= metrics.get('risk_level', 0) * 5
        score -= metrics.get('competition_level', 0) * 2
        
        return round(max(0, min(100, score)), 2)
        
    def process_financial_intelligence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Special processing for financial intelligence"""
        processed = {
            "roi_models": {},
            "financing_comparisons": [],
            "tax_strategies": [],
            "risk_matrices": {}
        }
        
        for insight in data.get('insights', []):
            if 'financial' in insight.get('domain', '') or 'investment' in insight.get('tags', []):
                # Extract ROI models
                if 'roi' in insight.get('tags', []):
                    processed['roi_models'][insight.get('title')] = {
                        "expected_return": insight.get('content', {}).get('metrics', {}).get('roi_percentage', 0),
                        "payback_period": insight.get('content', {}).get('metrics', {}).get('payback_period', 'N/A'),
                        "risk_level": insight.get('content', {}).get('metrics', {}).get('risk_level', 'Medium')
                    }
                    
        return processed
        
    def create_cross_domain_alerts(self) -> List[Dict[str, Any]]:
        """Create alerts for important cross-domain patterns"""
        alerts = []
        
        # Analyze queue for patterns
        queue_by_type = defaultdict(list)
        for item in self.processing_queue:
            queue_by_type[item['intelligence_type']].append(item)
            
        # Check for critical combinations
        if queue_by_type['environmental'] and queue_by_type['financial']:
            alerts.append({
                "type": "risk_impact",
                "message": "Environmental risks detected with financial implications",
                "priority": "high",
                "action": "Cross-reference flood risk areas with investment opportunities"
            })
            
        if queue_by_type['regulatory'] and queue_by_type['market']:
            alerts.append({
                "type": "opportunity",
                "message": "Regulatory changes creating market opportunities",
                "priority": "medium",
                "action": "Analyze zoning changes for development potential"
            })
            
        return alerts
        
    def generate_monitoring_report(self) -> Dict[str, Any]:
        """Generate comprehensive monitoring report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "queue_size": len(self.processing_queue),
            "priority_items": len([q for q in self.processing_queue if q['priority'] >= 8]),
            "intelligence_distribution": dict(self.processing_stats),
            "cross_domain_alerts": self.create_cross_domain_alerts(),
            "processing_recommendations": self._generate_recommendations()
        }
        
    def _generate_recommendations(self) -> List[str]:
        """Generate processing recommendations"""
        recommendations = []
        
        if self.processing_stats['neighborhood'] > 5:
            recommendations.append("High neighborhood intelligence volume - consider batch processing")
            
        if self.processing_stats['financial'] > 3 and self.processing_stats['environmental'] > 2:
            recommendations.append("Financial-Environmental correlation detected - prioritize cross-domain mapping")
            
        return recommendations


if __name__ == "__main__":
    # Initialize monitor
    monitor = T2CompletionMonitor("/Users/fernandox/Desktop/Core Agent Architecture")
    
    # Start monitoring
    observer = monitor.start_file_system_monitoring()
    
    print("T2 Completion Monitor running. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(5)
            
            # Generate periodic reports
            if len(monitor.processing_queue) > 0:
                report = monitor.generate_monitoring_report()
                print(f"\nMonitoring Report: {report['timestamp']}")
                print(f"Queue Size: {report['queue_size']}")
                print(f"Priority Items: {report['priority_items']}")
                
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoring stopped.")
    
    observer.join()
