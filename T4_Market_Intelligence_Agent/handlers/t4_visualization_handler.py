"""
T4 Visualization Handler
Processes chart scripts and generated visualizations from market reports
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from T4_Market_Intelligence_Agent.config.t4_config import T4_CONFIG


class T4VisualizationHandler:
    """Process and catalog chart visualizations and their data"""
    
    def __init__(self):
        self.config = T4_CONFIG
        self.processed_charts = set()
        self.chart_metadata = {}
        
    def process_chart_file(self, file_path: Path, associated_report: Optional[str] = None) -> Dict[str, Any]:
        """Process a chart/visualization file"""
        try:
            chart_id = self._generate_chart_id(file_path)
            
            # Extract metadata from filename and path
            chart_type = self._determine_chart_type(file_path)
            chart_category = self._determine_chart_category(file_path)
            
            # Process based on file type
            if file_path.suffix in ['.png', '.jpg', '.jpeg']:
                chart_data = self._process_image_chart(file_path)
            elif file_path.suffix == '.py':
                chart_data = self._process_python_script(file_path)
            else:
                chart_data = {"type": "unknown", "file": str(file_path)}
            
            # Create metadata entry
            metadata = {
                "chart_id": chart_id,
                "file_path": str(file_path),
                "file_name": file_path.name,
                "chart_type": chart_type,
                "category": chart_category,
                "associated_report": associated_report,
                "data_sources": chart_data.get("data_sources", []),
                "key_metrics": chart_data.get("key_metrics", []),
                "visualization_insights": self._extract_chart_insights(file_path, chart_data),
                "timestamp": datetime.now().isoformat(),
                "processing_metadata": {
                    "handler": "T4-Visualization-Handler",
                    "version": self.config["version"]
                }
            }
            
            self.chart_metadata[chart_id] = metadata
            return metadata
            
        except Exception as e:
            return {
                "error": f"Failed to process chart {file_path}: {str(e)}",
                "file": str(file_path),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_chart_id(self, file_path: Path) -> str:
        """Generate unique ID for chart"""
        file_hash = hashlib.md5(str(file_path).encode()).hexdigest()[:8]
        return f"t4-chart-{file_hash}"
    
    def _determine_chart_type(self, file_path: Path) -> str:
        """Determine the type of chart from filename"""
        filename_lower = file_path.stem.lower()
        
        chart_types = {
            "bar": ["bar", "column"],
            "line": ["line", "trend", "time_series", "timeseries"],
            "pie": ["pie", "donut"],
            "scatter": ["scatter", "correlation"],
            "heatmap": ["heatmap", "heat_map"],
            "map": ["map", "geographic", "spatial"],
            "area": ["area", "stacked"],
            "box": ["box", "boxplot"],
            "histogram": ["histogram", "distribution"]
        }
        
        for chart_type, keywords in chart_types.items():
            for keyword in keywords:
                if keyword in filename_lower:
                    return chart_type
        
        # Try to infer from content patterns in filename
        if "comparison" in filename_lower:
            return "bar"
        elif "growth" in filename_lower or "forecast" in filename_lower:
            return "line"
        elif "breakdown" in filename_lower or "composition" in filename_lower:
            return "pie"
        
        return "general"
    
    def _determine_chart_category(self, file_path: Path) -> str:
        """Determine the business category of the chart"""
        path_str = str(file_path).lower()
        
        categories = {
            "financial": ["finance", "financial", "cost", "price", "revenue", "profit", "cap_rate", "roi"],
            "market": ["market", "supply", "demand", "absorption", "vacancy", "inventory"],
            "demographic": ["demographic", "population", "age", "income", "employment"],
            "geographic": ["map", "location", "neighborhood", "district", "zone"],
            "construction": ["construction", "development", "pipeline", "delivery"],
            "investment": ["investment", "capital", "fund", "allocation"],
            "climate": ["climate", "resilient", "flood", "environmental", "green"],
            "infrastructure": ["infrastructure", "utility", "power", "water", "transportation"]
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in path_str:
                    return category
        
        return "general"
    
    def _process_image_chart(self, file_path: Path) -> Dict[str, Any]:
        """Extract information from image filename and context"""
        chart_data = {
            "type": "image_visualization",
            "format": file_path.suffix[1:]  # Remove the dot
        }
        
        # Extract metrics from filename
        filename = file_path.stem
        
        # Look for years
        years = re.findall(r'20\d{2}', filename)
        if years:
            chart_data["time_period"] = years
        
        # Look for percentages
        percentages = re.findall(r'(\d+\.?\d*)\s*%', filename)
        if percentages:
            chart_data["percentage_values"] = [float(p) for p in percentages]
        
        # Look for dollar amounts
        dollars = re.findall(r'\$(\d+\.?\d*)\s*([MBK])?', filename)
        if dollars:
            chart_data["dollar_values"] = []
            for amount, unit in dollars:
                value = float(amount)
                if unit == 'K':
                    value *= 1000
                elif unit == 'M':
                    value *= 1000000
                elif unit == 'B':
                    value *= 1000000000
                chart_data["dollar_values"].append(value)
        
        # Extract key metrics based on common patterns
        key_metrics = []
        
        # Common metric patterns in filenames
        metric_patterns = {
            "growth_rate": r"growth.*?(\d+\.?\d*)\s*%",
            "market_share": r"share.*?(\d+\.?\d*)\s*%",
            "occupancy": r"occupancy.*?(\d+\.?\d*)\s*%",
            "cap_rate": r"cap.*?rate.*?(\d+\.?\d*)\s*%"
        }
        
        for metric_name, pattern in metric_patterns.items():
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                key_metrics.append({
                    "metric": metric_name,
                    "value": float(match.group(1))
                })
        
        if key_metrics:
            chart_data["key_metrics"] = key_metrics
        
        return chart_data
    
    def _process_python_script(self, file_path: Path) -> Dict[str, Any]:
        """Extract data sources and visualization details from Python scripts"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            chart_data = {
                "type": "python_visualization_script",
                "libraries": self._extract_libraries(content),
                "data_sources": self._extract_data_sources(content),
                "chart_configurations": self._extract_chart_config(content)
            }
            
            # Extract metrics from the code
            key_metrics = []
            
            # Look for variable assignments with numeric values
            numeric_assignments = re.findall(r'(\w+)\s*=\s*(\d+\.?\d*)', content)
            for var_name, value in numeric_assignments:
                if any(keyword in var_name.lower() for keyword in ['rate', 'price', 'cost', 'return', 'growth']):
                    key_metrics.append({
                        "metric": var_name,
                        "value": float(value)
                    })
            
            # Look for DataFrame operations that might indicate metrics
            df_operations = re.findall(r'df\[[\'"]([\w\s]+)[\'"]\]', content)
            chart_data["dataframe_columns"] = list(set(df_operations))
            
            if key_metrics:
                chart_data["key_metrics"] = key_metrics
            
            return chart_data
            
        except Exception as e:
            return {"type": "python_script", "error": str(e)}
    
    def _extract_libraries(self, content: str) -> List[str]:
        """Extract imported libraries from Python script"""
        libraries = []
        
        # Standard import patterns
        import_patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)\s+import',
            r'import\s+(\w+)\s+as\s+\w+'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            libraries.extend(matches)
        
        # Filter for visualization libraries
        viz_libraries = ['matplotlib', 'seaborn', 'plotly', 'bokeh', 'altair', 'pandas', 'numpy']
        return list(set([lib for lib in libraries if lib in viz_libraries]))
    
    def _extract_data_sources(self, content: str) -> List[str]:
        """Extract data source references from Python script"""
        data_sources = []
        
        # Look for file reads
        file_patterns = [
            r'read_csv\([\'"]([^\'\"]+)[\'"]',
            r'read_excel\([\'"]([^\'\"]+)[\'"]',
            r'open\([\'"]([^\'\"]+)[\'"]',
            r'load\([\'"]([^\'\"]+)[\'"]'
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            data_sources.extend(matches)
        
        # Look for API endpoints
        api_pattern = r'(?:url|endpoint)\s*=\s*[\'"]([^\'\"]+)[\'"]'
        api_matches = re.findall(api_pattern, content)
        data_sources.extend(api_matches)
        
        return list(set(data_sources))
    
    def _extract_chart_config(self, content: str) -> Dict[str, Any]:
        """Extract chart configuration from Python script"""
        config = {}
        
        # Extract chart titles
        title_patterns = [
            r'title\s*=\s*[\'"]([^\'\"]+)[\'"]',
            r'\.title\([\'"]([^\'\"]+)[\'"]',
            r'suptitle\([\'"]([^\'\"]+)[\'"]'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, content)
            if match:
                config["title"] = match.group(1)
                break
        
        # Extract axis labels
        xlabel_match = re.search(r'xlabel\([\'"]([^\'\"]+)[\'"]', content)
        ylabel_match = re.search(r'ylabel\([\'"]([^\'\"]+)[\'"]', content)
        
        if xlabel_match:
            config["x_axis"] = xlabel_match.group(1)
        if ylabel_match:
            config["y_axis"] = ylabel_match.group(1)
        
        # Extract chart type from function calls
        chart_functions = {
            "bar": r'\.bar\(',
            "line": r'\.plot\(',
            "scatter": r'\.scatter\(',
            "pie": r'\.pie\(',
            "heatmap": r'\.heatmap\(',
            "histogram": r'\.hist\('
        }
        
        for chart_type, pattern in chart_functions.items():
            if re.search(pattern, content):
                config["chart_type"] = chart_type
                break
        
        return config
    
    def _extract_chart_insights(self, file_path: Path, chart_data: Dict) -> List[str]:
        """Generate insights from chart metadata"""
        insights = []
        
        # Insights based on chart type
        chart_type = chart_data.get("chart_type") or self._determine_chart_type(file_path)
        
        if chart_type == "line" and "time_period" in chart_data:
            years = chart_data["time_period"]
            if len(years) >= 2:
                insights.append(f"Time series analysis covering {min(years)} to {max(years)}")
        
        if chart_type == "bar" and "dataframe_columns" in chart_data:
            insights.append(f"Comparative analysis across {len(chart_data['dataframe_columns'])} metrics")
        
        # Insights from key metrics
        if "key_metrics" in chart_data:
            for metric in chart_data["key_metrics"]:
                if "rate" in metric["metric"].lower():
                    insights.append(f"{metric['metric']}: {metric['value']}%")
                else:
                    insights.append(f"{metric['metric']}: {metric['value']}")
        
        # Insights from dollar values
        if "dollar_values" in chart_data:
            total_value = sum(chart_data["dollar_values"])
            if total_value > 1000000000:
                insights.append(f"Total tracked value: ${total_value/1000000000:.1f}B")
            elif total_value > 1000000:
                insights.append(f"Total tracked value: ${total_value/1000000:.1f}M")
        
        # Category-specific insights
        category = self._determine_chart_category(file_path)
        if category == "financial":
            insights.append("Financial performance visualization")
        elif category == "market":
            insights.append("Market dynamics visualization")
        elif category == "demographic":
            insights.append("Population and demographic trends")
        
        return insights[:5]  # Limit to 5 insights
    
    def process_visualization_directory(self, directory_path: Path, 
                                      report_associations: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Process all visualizations in a directory"""
        results = []
        
        # Find all chart files
        chart_extensions = ['.png', '.jpg', '.jpeg', '.py']
        chart_files = []
        
        for ext in chart_extensions:
            chart_files.extend(directory_path.rglob(f"*{ext}"))
        
        for file_path in chart_files:
            # Skip if already processed
            if str(file_path) in self.processed_charts:
                continue
            
            # Determine associated report if provided
            associated_report = None
            if report_associations:
                # Try to match based on directory or filename similarity
                for report, report_path in report_associations.items():
                    if file_path.parent.name in report_path or report in str(file_path):
                        associated_report = report
                        break
            
            print(f"Processing visualization: {file_path}")
            result = self.process_chart_file(file_path, associated_report)
            results.append(result)
            self.processed_charts.add(str(file_path))
        
        return results
    
    def generate_visualization_catalog(self) -> Dict[str, Any]:
        """Generate a catalog of all processed visualizations"""
        catalog = {
            "catalog_id": f"t4-viz-catalog-{datetime.now().strftime('%Y%m%d')}",
            "total_visualizations": len(self.chart_metadata),
            "visualizations_by_type": {},
            "visualizations_by_category": {},
            "key_insights": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Group by type
        for chart_id, metadata in self.chart_metadata.items():
            chart_type = metadata.get("chart_type", "unknown")
            if chart_type not in catalog["visualizations_by_type"]:
                catalog["visualizations_by_type"][chart_type] = []
            catalog["visualizations_by_type"][chart_type].append(chart_id)
        
        # Group by category
        for chart_id, metadata in self.chart_metadata.items():
            category = metadata.get("category", "general")
            if category not in catalog["visualizations_by_category"]:
                catalog["visualizations_by_category"][category] = []
            catalog["visualizations_by_category"][category].append(chart_id)
        
        # Extract key insights
        all_insights = []
        for metadata in self.chart_metadata.values():
            all_insights.extend(metadata.get("visualization_insights", []))
        
        # Deduplicate and select top insights
        unique_insights = list(set(all_insights))
        catalog["key_insights"] = unique_insights[:20]
        
        # Add detailed metadata
        catalog["visualization_details"] = self.chart_metadata
        
        return catalog