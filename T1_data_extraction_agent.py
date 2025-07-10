#!/usr/bin/env python3
"""
T1 Data Extraction Agent
Houston Development Intelligence Platform
Extracts and processes raw data from Data Processing folders
"""

import pandas as pd
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import re
from typing import Dict, List, Any, Optional
import traceback
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle numpy types"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        return super(NumpyEncoder, self).default(obj)

class T1DataExtractionAgent:
    def __init__(self, data_processing_path: str = "./Data Processing"):
        self.data_processing_path = Path(data_processing_path)
        self.output_base = Path("./Processing_Pipeline/T1_Extracted_Data")
        self.status_file = Path("./Processing_Pipeline/Processing_Status/t1_status.json")
        self.extracted_data = {}
        self.progress_tracker = RealTimeProgressTracker()
        
        # Domain mapping for output organization
        self.domain_mapping = {
            "Houston Development Market": "market_intelligence",
            "Competitive Analysis": "market_intelligence",
            "Economic and Demographic": "financial_intelligence",
            "Environmental and Risk": "environmental_intelligence",
            "Financing and Investment": "financial_intelligence",
            "Legal and Title": "regulatory_intelligence",
            "Neighborhood-Level Market": "neighborhood_intelligence",
            "Real-Time Houston Development Pipeline": "market_intelligence",
            "Technology and Innovation": "technology_intelligence",
            "Zoning and Regulatory": "regulatory_intelligence",
            "land acquisition": "market_intelligence",
            "lending rate": "financial_intelligence",
            "development regulations": "regulatory_intelligence",
            "ROI in Katy": "neighborhood_intelligence",
            "STEM education": "technology_intelligence",
            "flood": "environmental_intelligence"
        }
        
    def determine_domain(self, folder_name: str) -> str:
        """Determine which intelligence domain a folder belongs to"""
        folder_lower = folder_name.lower()
        
        for key, domain in self.domain_mapping.items():
            if key.lower() in folder_lower:
                return domain
        
        # Default fallback
        return "market_intelligence"
    
    def scan_all_folders(self):
        """Scan all Data Processing folders and extract content"""
        # Get priority order
        prioritizer = ProcessingPrioritizer()
        all_folders = [f for f in self.data_processing_path.iterdir() if f.is_dir()]
        ordered_folders = prioritizer.get_processing_order([f.name for f in all_folders])
        
        # Count total files for progress tracking
        total_files = sum(len(list(f.iterdir())) for f in all_folders if f.is_dir())
        self.progress_tracker.total_files = total_files
        
        print(f"🚀 Starting T1 Data Extraction")
        print(f"📁 Found {len(ordered_folders)} folders with {total_files} total files")
        print(f"⚡ Processing in business impact priority order")
        print("━" * 50)
        
        # Process folders in priority order
        for folder_name in ordered_folders:
            folder_path = self.data_processing_path / folder_name
            if folder_path.exists() and folder_path.is_dir():
                print(f"\n📂 Processing: {folder_name}")
                folder_data = self.extract_folder_content(folder_path, folder_name)
                
                # Determine domain and save immediately
                domain = self.determine_domain(folder_name)
                self.save_domain_data(domain, folder_name, folder_data)
                
                # Update status for T2 monitoring
                self.update_extraction_status(domain, folder_name)
        
        print("\n✅ T1 Data Extraction Complete!")
        return self.extracted_data
    
    def extract_folder_content(self, folder_path: Path, folder_name: str) -> Dict:
        """Extract content from a specific folder"""
        folder_data = {
            'metadata': {
                'folder_name': folder_name,
                'extraction_timestamp': datetime.now().isoformat(),
                'file_count': 0,
                'extraction_success_rate': 0
            },
            'csv_data': {},
            'chart_insights': {},
            'script_outputs': {},
            'report_content': {}
        }
        
        files_processed = 0
        files_success = 0
        
        for file in folder_path.iterdir():
            if file.is_file():
                files_processed += 1
                try:
                    if file.suffix == '.csv':
                        data = self.extract_csv_data(file)
                        if data and 'error' not in data:
                            folder_data['csv_data'][file.name] = data
                            files_success += 1
                    elif file.suffix == '.png':
                        data = self.extract_chart_data(file)
                        if data:
                            folder_data['chart_insights'][file.name] = data
                            files_success += 1
                    elif file.suffix == '.py':
                        data = self.extract_script_insights(file)
                        if data:
                            folder_data['script_outputs'][file.name] = data
                            files_success += 1
                    elif file.suffix == '.md':
                        data = self.extract_markdown_content(file)
                        if data:
                            folder_data['report_content'][file.name] = data
                            files_success += 1
                    
                    self.progress_tracker.update_progress(file, "success")
                    
                except Exception as e:
                    print(f"  ⚠️  Error processing {file.name}: {str(e)}")
                    self.progress_tracker.update_progress(file, "error")
        
        folder_data['metadata']['file_count'] = files_processed
        folder_data['metadata']['extraction_success_rate'] = (
            files_success / files_processed if files_processed > 0 else 0
        )
        
        return folder_data
    
    def extract_csv_data(self, file_path: Path) -> Optional[Dict]:
        """Extract and summarize CSV data"""
        try:
            # Check if file has content
            if file_path.stat().st_size == 0:
                return {
                    'status': 'empty_file',
                    'requires_manual_review': True,
                    'file_path': str(file_path)
                }
            
            df = pd.read_csv(file_path)
            
            # Generate comprehensive summary
            summary = {
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'data_types': df.dtypes.astype(str).to_dict(),
                'null_counts': df.isnull().sum().to_dict(),
                'summary_stats': {}
            }
            
            # Add numeric summaries
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                summary['summary_stats'] = df[numeric_cols].describe().to_dict()
            
            # Sample data (first 5 rows)
            summary['sample_data'] = df.head().to_dict('records')
            
            # Extract key insights based on column names
            summary['key_metrics'] = self.extract_key_metrics(df)
            
            return summary
            
        except Exception as e:
            return {'error': str(e), 'traceback': traceback.format_exc()}
    
    def extract_key_metrics(self, df: pd.DataFrame) -> Dict:
        """Extract key metrics from dataframe based on column patterns"""
        metrics = {}
        
        # Look for common patterns
        for col in df.columns:
            col_lower = col.lower()
            
            # Growth rates
            if 'growth' in col_lower or 'change' in col_lower:
                if df[col].dtype in ['float64', 'int64']:
                    metrics[f"{col}_avg"] = df[col].mean()
                    metrics[f"{col}_max"] = df[col].max()
            
            # Prices/Values
            elif 'price' in col_lower or 'value' in col_lower or '$' in col:
                if df[col].dtype in ['float64', 'int64']:
                    metrics[f"{col}_median"] = df[col].median()
                    metrics[f"{col}_range"] = [df[col].min(), df[col].max()]
            
            # Counts/Permits
            elif 'permit' in col_lower or 'count' in col_lower:
                if df[col].dtype in ['float64', 'int64']:
                    metrics[f"{col}_total"] = df[col].sum()
        
        return metrics
    
    def extract_chart_data(self, file_path: Path) -> Optional[Dict]:
        """Extract insights from chart images"""
        try:
            # For now, analyze filename and size
            # In production, would use OCR here
            return {
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'chart_type': self.infer_chart_type(file_path.name),
                'insights': self.analyze_chart_filename(file_path.name),
                'requires_ocr': True,
                'ocr_placeholder': "Chart data extraction pending OCR implementation"
            }
        except Exception as e:
            return {'error': str(e)}
    
    def infer_chart_type(self, filename: str) -> str:
        """Infer chart type from filename"""
        filename_lower = filename.lower()
        
        if 'pie' in filename_lower:
            return 'pie_chart'
        elif 'scatter' in filename_lower:
            return 'scatter_plot'
        elif 'timeline' in filename_lower:
            return 'timeline'
        elif 'bar' in filename_lower or 'chart' in filename_lower:
            return 'bar_chart'
        else:
            return 'unknown'
    
    def analyze_chart_filename(self, filename: str) -> Dict:
        """Extract insights from chart filename"""
        insights = {}
        filename_lower = filename.lower()
        
        # Extract location information
        locations = ['houston', 'katy', 'harris_county', 'sugar_land', 'woodlands']
        for loc in locations:
            if loc in filename_lower:
                insights['location'] = loc
                break
        
        # Extract topic
        topics = ['development', 'price', 'growth', 'investment', 'permit', 'lending']
        for topic in topics:
            if topic in filename_lower:
                insights['topic'] = topic
                break
        
        # Extract year if present
        year_match = re.search(r'20\d{2}', filename)
        if year_match:
            insights['year'] = year_match.group()
        
        return insights
    
    def extract_script_insights(self, file_path: Path) -> Optional[Dict]:
        """Extract insights from Python scripts"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            if not content.strip():
                return {
                    'status': 'empty_file',
                    'file_path': str(file_path)
                }
            
            return {
                'imports': self.extract_imports(content),
                'functions': self.extract_functions(content),
                'data_sources': self.extract_data_sources(content),
                'visualizations': self.extract_visualizations(content),
                'analysis_methods': self.identify_analysis_methods(content)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        import_pattern = r'^(?:from\s+[\w.]+\s+)?import\s+[\w\s,.*]+$'
        imports = re.findall(import_pattern, content, re.MULTILINE)
        return imports
    
    def extract_functions(self, content: str) -> List[str]:
        """Extract function definitions"""
        function_pattern = r'^def\s+(\w+)\s*\('
        functions = re.findall(function_pattern, content, re.MULTILINE)
        return functions
    
    def extract_data_sources(self, content: str) -> List[str]:
        """Extract data file references"""
        # Look for CSV file references
        csv_pattern = r'["\']([^"\']*\.csv)["\']'
        csv_files = re.findall(csv_pattern, content)
        return list(set(csv_files))
    
    def extract_visualizations(self, content: str) -> Dict:
        """Extract visualization details"""
        viz_info = {
            'chart_types': [],
            'color_scheme': [],
            'titles': []
        }
        
        # Plotly chart types
        chart_patterns = [
            (r'go\.Bar', 'bar_chart'),
            (r'go\.Scatter', 'scatter_plot'),
            (r'go\.Pie', 'pie_chart'),
            (r'px\.bar', 'bar_chart'),
            (r'px\.scatter', 'scatter_plot')
        ]
        
        for pattern, chart_type in chart_patterns:
            if re.search(pattern, content):
                viz_info['chart_types'].append(chart_type)
        
        # Extract colors
        color_pattern = r'#[0-9A-Fa-f]{6}'
        colors = re.findall(color_pattern, content)
        viz_info['color_scheme'] = list(set(colors))
        
        # Extract titles
        title_pattern = r'title\s*=\s*["\']([^"\']+)["\']'
        titles = re.findall(title_pattern, content)
        viz_info['titles'] = titles
        
        return viz_info
    
    def identify_analysis_methods(self, content: str) -> List[str]:
        """Identify analysis methods used"""
        methods = []
        
        analysis_patterns = {
            'groupby': 'aggregation_analysis',
            'mean()': 'statistical_summary',
            'sum()': 'totaling',
            'sort_values': 'ranking_analysis',
            'merge': 'data_joining',
            'pivot': 'pivot_analysis'
        }
        
        for pattern, method in analysis_patterns.items():
            if pattern in content:
                methods.append(method)
        
        return list(set(methods))
    
    def extract_markdown_content(self, file_path: Path) -> Optional[Dict]:
        """Extract structured content from markdown files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return {
                    'status': 'empty_file',
                    'file_path': str(file_path)
                }
            
            return {
                'sections': self.parse_markdown_sections(content),
                'key_insights': self.extract_key_insights(content),
                'data_references': self.extract_data_references(content),
                'recommendations': self.extract_recommendations(content)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def parse_markdown_sections(self, content: str) -> Dict:
        """Parse markdown into sections"""
        sections = {}
        
        # Split by headers
        header_pattern = r'^(#{1,3})\s+(.+)$'
        
        current_section = "introduction"
        current_content = []
        
        for line in content.split('\n'):
            header_match = re.match(header_pattern, line)
            if header_match:
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                level = len(header_match.group(1))
                current_section = header_match.group(2).lower().replace(' ', '_')
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def extract_key_insights(self, content: str) -> List[str]:
        """Extract key insights from markdown"""
        insights = []
        
        # Look for bullet points with key information
        bullet_pattern = r'^\s*[-*]\s+(.+)$'
        bullets = re.findall(bullet_pattern, content, re.MULTILINE)
        
        # Filter for insights (containing numbers or percentages)
        for bullet in bullets:
            if re.search(r'\d+%?|\$[\d,]+', bullet):
                insights.append(bullet.strip())
        
        return insights[:10]  # Top 10 insights
    
    def extract_data_references(self, content: str) -> List[str]:
        """Extract data source references"""
        # Look for footnote references
        footnote_pattern = r'\[\^(\d+)\]'
        footnotes = re.findall(footnote_pattern, content)
        
        # Look for source citations
        source_pattern = r'(?:Source|Data):\s*([^\n]+)'
        sources = re.findall(source_pattern, content, re.IGNORECASE)
        
        return {
            'footnotes': list(set(footnotes)),
            'sources': sources
        }
    
    def extract_recommendations(self, content: str) -> List[str]:
        """Extract recommendations from content"""
        recommendations = []
        
        # Look for recommendation patterns
        rec_patterns = [
            r'(?:recommend|suggest|should|consider)\s+([^.!?]+[.!?])',
            r'(?:opportunity|potential)\s+(?:for|to)\s+([^.!?]+[.!?])'
        ]
        
        for pattern in rec_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            recommendations.extend(matches)
        
        return recommendations[:5]  # Top 5 recommendations
    
    def save_domain_data(self, domain: str, folder_name: str, data: Dict):
        """Save extracted data to domain-specific output folder"""
        domain_path = self.output_base / domain
        domain_path.mkdir(parents=True, exist_ok=True)
        
        # Create sanitized filename
        safe_filename = re.sub(r'[^\w\s-]', '', folder_name)
        safe_filename = re.sub(r'[-\s]+', '_', safe_filename)
        
        # Save each data type
        for data_type in ['csv_data', 'chart_insights', 'script_outputs', 'report_content']:
            if data[data_type]:
                type_path = domain_path / data_type
                type_path.mkdir(exist_ok=True)
                
                output_file = type_path / f"{safe_filename}.json"
                with open(output_file, 'w') as f:
                    json.dump({
                        'metadata': data['metadata'],
                        'data': data[data_type]
                    }, f, indent=2, cls=NumpyEncoder)
                
                print(f"  ✅ Saved {data_type} to {domain}/{data_type}")
    
    def update_extraction_status(self, domain: str, folder_name: str):
        """Update status file for T2 monitoring"""
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        
        status = {
            "session": "T1_Data_Extraction",
            "timestamp": datetime.now().isoformat(),
            "latest_completion": {
                "domain": domain,
                "folder": folder_name,
                "completed_at": datetime.now().isoformat()
            },
            "progress": self.progress_tracker.get_progress_stats(),
            "domains_with_data": self.get_completed_domains()
        }
        
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2, cls=NumpyEncoder)
    
    def get_completed_domains(self) -> List[str]:
        """Get list of domains with extracted data"""
        completed = []
        for domain_dir in self.output_base.iterdir():
            if domain_dir.is_dir() and any(domain_dir.iterdir()):
                completed.append(domain_dir.name)
        return completed


class ProcessingPrioritizer:
    """Prioritize folder processing based on business impact"""
    
    def __init__(self):
        self.priority_order = [
            # Tier 1: Core Business Intelligence
            "Houston Development Market_ Competitive Analysis",
            "Neighborhood-Level Market Intelligence", 
            "Real-Time Houston Development Pipeline Research",
            
            # Tier 2: Financial & Investment
            "Financing and Investment Intelligence",
            "Economic and Demographic Intelligence _Houston population growth projections by",
            
            # Tier 3: Regulatory & Environmental
            "Zoning and Regulatory Intelligence",
            "Environmental and Risk Intelligence",
            
            # Tier 4: Strategic Intelligence
            "Technology and Innovation District Intelligence _Houston innovation distri",
            "Legal and Title Intelligence",
            
            # Tier 5: Research Questions
            "How are land acquisition strategies shaping Houston_s top developers_ growth plans",
            "How do lending rate trends impact commercial real estate projects in Harris County",
            "What are the key differences between Houston_s development regulations a",
            "What are the key indicators of development ROI in Katy Heights",
            "What role does STEM education play in Houston's economic expansion",
            "What technological advancements are being used to improve Harris County flood",
            "How might the district_s partnerships with companies like Chevron and Microsoft shape local economic growth"
        ]
    
    def get_processing_order(self, available_folders: List[str]) -> List[str]:
        """Return folders in business impact priority order"""
        ordered_folders = []
        
        # Match folders to priority order (partial matching)
        for priority_folder in self.priority_order:
            for folder in available_folders:
                if priority_folder.lower() in folder.lower() or folder.lower() in priority_folder.lower():
                    if folder not in ordered_folders:
                        ordered_folders.append(folder)
        
        # Add any remaining folders
        remaining = [f for f in available_folders if f not in ordered_folders]
        ordered_folders.extend(sorted(remaining))
        
        return ordered_folders


class RealTimeProgressTracker:
    """Track and display real-time progress"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.total_files = 0
        self.processed_files = 0
        self.success_count = 0
        self.error_count = 0
        self.domain_progress = {}
    
    def update_progress(self, file_path: Path, status: str):
        """Update progress for a processed file"""
        self.processed_files += 1
        
        if status == "success":
            self.success_count += 1
        elif status == "error":
            self.error_count += 1
        
        # Display progress every 5 files
        if self.processed_files % 5 == 0:
            self.display_progress()
    
    def display_progress(self):
        """Display current progress"""
        elapsed = datetime.now() - self.start_time
        progress_pct = (self.processed_files / self.total_files) * 100 if self.total_files > 0 else 0
        success_rate = (self.success_count / self.processed_files) * 100 if self.processed_files > 0 else 0
        
        # Calculate ETA
        if self.processed_files > 0:
            avg_time_per_file = elapsed.total_seconds() / self.processed_files
            remaining_files = self.total_files - self.processed_files
            eta_seconds = avg_time_per_file * remaining_files
            eta = timedelta(seconds=int(eta_seconds))
        else:
            eta = "Calculating..."
        
        print(f"\n{'━' * 50}")
        print(f"🔄 T1 Data Extraction Progress")
        print(f"{'━' * 50}")
        print(f"Progress: {progress_pct:.1f}% ({self.processed_files}/{self.total_files} files)")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Errors: {self.error_count}")
        print(f"Elapsed: {elapsed}")
        print(f"ETA: {eta}")
        print(f"{'━' * 50}\n")
    
    def get_progress_stats(self) -> Dict:
        """Get progress statistics"""
        return {
            "progress_percentage": (self.processed_files / self.total_files) * 100 if self.total_files > 0 else 0,
            "files_processed": self.processed_files,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": (self.success_count / self.processed_files) * 100 if self.processed_files > 0 else 0
        }


def main():
    """Main execution function"""
    print("🚀 Houston Development Intelligence Platform")
    print("📊 T1 Data Extraction Agent Starting...")
    print("=" * 50)
    
    # Initialize agent
    agent = T1DataExtractionAgent()
    
    # Check if data processing folder exists
    if not agent.data_processing_path.exists():
        print(f"❌ Error: Data Processing folder not found at {agent.data_processing_path}")
        sys.exit(1)
    
    # Start extraction
    try:
        extracted_data = agent.scan_all_folders()
        
        # Final summary
        print("\n" + "=" * 50)
        print("✅ T1 Data Extraction Complete!")
        print(f"📊 Total Files Processed: {agent.progress_tracker.processed_files}")
        print(f"✅ Success Rate: {agent.progress_tracker.get_progress_stats()['success_rate']:.1f}%")
        print(f"📁 Data saved to: {agent.output_base}")
        print("🚀 Ready for T2 Intelligence Analysis!")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()