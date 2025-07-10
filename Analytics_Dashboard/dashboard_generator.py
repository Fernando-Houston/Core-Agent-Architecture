#!/usr/bin/env python3
"""
Dashboard HTML Generator for Houston Intelligence Platform
Creates interactive HTML dashboards with real-time analytics
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add path for analytics modules
sys.path.append(str(Path(__file__).parent))
from analytics_backend import AnalyticsEngine
from performance_monitor import PerformanceMonitor


class DashboardGenerator:
    """Generate HTML dashboards with analytics data"""
    
    def __init__(self, analytics_engine: AnalyticsEngine):
        self.analytics = analytics_engine
        self.monitor = PerformanceMonitor(analytics_engine)
        self.output_path = Path(analytics_engine.analytics_path) / "dashboards"
        self.output_path.mkdir(exist_ok=True)
        
    def generate_main_dashboard(self) -> str:
        """Generate main analytics dashboard"""
        # Get data
        stats = self.analytics.get_dashboard_stats()
        real_time = self.monitor.get_real_time_metrics()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Houston Intelligence Platform - Analytics Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px 0;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
            margin: 10px 0;
        }}
        
        .metric-label {{
            color: #7f8c8d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-change {{
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .trend-up {{
            color: #27ae60;
        }}
        
        .trend-down {{
            color: #e74c3c;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }}
        
        .chart-container {{
            height: 300px;
            margin: 20px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }}
        
        tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .health-score {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .health-good {{
            background-color: #d4edda;
            color: #155724;
        }}
        
        .health-warning {{
            background-color: #fff3cd;
            color: #856404;
        }}
        
        .health-critical {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        
        .alert-item {{
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 4px solid;
        }}
        
        .alert-warning {{
            background-color: #fff3cd;
            border-color: #ffc107;
            color: #856404;
        }}
        
        .alert-critical {{
            background-color: #f8d7da;
            border-color: #dc3545;
            color: #721c24;
        }}
        
        .timestamp {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        .agent-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 500;
            margin: 2px;
        }}
        
        .agent-market {{ background-color: #e3f2fd; color: #1565c0; }}
        .agent-neighborhood {{ background-color: #f3e5f5; color: #6a1b9a; }}
        .agent-financial {{ background-color: #e8f5e9; color: #2e7d32; }}
        .agent-environmental {{ background-color: #fff8e1; color: #f57c00; }}
        .agent-regulatory {{ background-color: #fce4ec; color: #c2185b; }}
        .agent-technology {{ background-color: #e0f2f1; color: #00695c; }}
        
        @media (max-width: 768px) {{
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
            
            header h1 {{
                font-size: 1.8em;
            }}
            
            .metric-value {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Houston Intelligence Platform</h1>
            <p>Real-time Analytics Dashboard</p>
            <p class="timestamp">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </header>
    
    <div class="container">
        <!-- Key Metrics -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total API Calls (24h)</div>
                <div class="metric-value">{stats['summary']['total_calls_24h']:,}</div>
                <div class="metric-change trend-up">↑ Active</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Average Response Time</div>
                <div class="metric-value">{stats['summary']['avg_response_time_ms']:.0f}ms</div>
                <div class="metric-change {self._get_trend_class(real_time['avg_response_time']['trend'])}">
                    {self._get_trend_icon(real_time['avg_response_time']['trend'])} {real_time['avg_response_time']['trend']}
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Error Rate</div>
                <div class="metric-value">{stats['summary']['error_rate_percent']:.1f}%</div>
                <div class="metric-change {self._get_trend_class(real_time['error_rate']['trend'])}">
                    {self._get_trend_icon(real_time['error_rate']['trend'])} {real_time['error_rate']['trend']}
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Active Users</div>
                <div class="metric-value">{stats['summary']['active_users']:,}</div>
                <div class="metric-change trend-up">↑ Growing</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">System Health</div>
                <div class="metric-value">
                    <span class="{self._get_health_class(real_time['health_score'])} health-score">
                        {real_time['health_score']}/100
                    </span>
                </div>
                <div class="metric-change">{self._get_health_status(real_time['health_score'])}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Current Throughput</div>
                <div class="metric-value">{real_time['calls_per_minute']['current']}</div>
                <div class="metric-change">calls/minute</div>
            </div>
        </div>
        
        <!-- Agent Activity -->
        <div class="section">
            <h2>Agent Activity Distribution</h2>
            <div class="metrics-grid">
                {self._generate_agent_cards(stats['calls_by_agent'])}
            </div>
        </div>
        
        <!-- Top Endpoints -->
        <div class="section">
            <h2>Popular Endpoints</h2>
            <table>
                <thead>
                    <tr>
                        <th>Endpoint</th>
                        <th>Calls (24h)</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_endpoint_rows(stats['popular_endpoints'], stats['summary']['total_calls_24h'])}
                </tbody>
            </table>
        </div>
        
        <!-- Recent Alerts -->
        <div class="section">
            <h2>Recent Alerts</h2>
            {self._generate_alerts(real_time['recent_alerts'])}
        </div>
        
        <!-- Real-time Metrics -->
        <div class="section">
            <h2>Real-time Performance Metrics</h2>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Current</th>
                        <th>1-min Avg</th>
                        <th>5-min Avg</th>
                        <th>Trend</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Calls per Minute</td>
                        <td>{real_time['calls_per_minute']['current']}</td>
                        <td>{real_time['calls_per_minute']['avg_1min']}</td>
                        <td>{real_time['calls_per_minute']['avg_5min']}</td>
                        <td class="{self._get_trend_class(real_time['calls_per_minute']['trend'])}">
                            {self._get_trend_icon(real_time['calls_per_minute']['trend'])} {real_time['calls_per_minute']['trend']}
                        </td>
                    </tr>
                    <tr>
                        <td>Response Time (ms)</td>
                        <td>{real_time['avg_response_time']['current']}</td>
                        <td>{real_time['avg_response_time']['avg_1min']}</td>
                        <td>{real_time['avg_response_time']['avg_5min']}</td>
                        <td class="{self._get_trend_class(real_time['avg_response_time']['trend'])}">
                            {self._get_trend_icon(real_time['avg_response_time']['trend'])} {real_time['avg_response_time']['trend']}
                        </td>
                    </tr>
                    <tr>
                        <td>Error Rate (%)</td>
                        <td>{real_time['error_rate']['current']}</td>
                        <td>{real_time['error_rate']['avg_1min']}</td>
                        <td>{real_time['error_rate']['avg_5min']}</td>
                        <td class="{self._get_trend_class(real_time['error_rate']['trend'])}">
                            {self._get_trend_icon(real_time['error_rate']['trend'])} {real_time['error_rate']['trend']}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => {{
            window.location.reload();
        }}, 30000);
    </script>
</body>
</html>
"""
        
        # Save dashboard
        dashboard_path = self.output_path / "main_dashboard.html"
        with open(dashboard_path, 'w') as f:
            f.write(html)
            
        return str(dashboard_path)
        
    def generate_performance_report(self, hours: int = 24) -> str:
        """Generate detailed performance report"""
        report = self.monitor.get_performance_report(hours)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Report - Houston Intelligence Platform</title>
    <style>
        {self._get_base_styles()}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .summary-item {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .summary-label {{
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        
        .summary-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .performance-table {{
            overflow-x: auto;
        }}
        
        .metric-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .metric-response {{ background-color: #e3f2fd; color: #1565c0; }}
        .metric-error {{ background-color: #ffebee; color: #c62828; }}
        .metric-throughput {{ background-color: #e8f5e9; color: #2e7d32; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Performance Report</h1>
            <p>Houston Intelligence Platform - {hours} Hour Analysis</p>
            <p class="timestamp">Generated: {report['generated_at']}</p>
        </div>
    </header>
    
    <div class="container">
        <!-- Summary -->
        <div class="section">
            <h2>Performance Summary</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-label">System Uptime</div>
                    <div class="summary-value">{report['system_uptime_percent']}%</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Total Alerts</div>
                    <div class="summary-value">{report['total_alerts']}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Health Score</div>
                    <div class="summary-value">{report['current_health_score']}/100</div>
                </div>
            </div>
        </div>
        
        <!-- Metrics Summary -->
        <div class="section">
            <h2>Metrics Overview</h2>
            <table>
                <thead>
                    <tr>
                        <th>Metric Type</th>
                        <th>Average</th>
                        <th>Minimum</th>
                        <th>Maximum</th>
                        <th>Data Points</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_metrics_rows(report['metrics_summary'])}
                </tbody>
            </table>
        </div>
        
        <!-- Endpoint Performance -->
        <div class="section">
            <h2>Endpoint Performance Analysis</h2>
            <div class="performance-table">
                <table>
                    <thead>
                        <tr>
                            <th>Endpoint</th>
                            <th>Total Calls</th>
                            <th>Avg Response</th>
                            <th>Min/Max</th>
                            <th>Std Dev</th>
                            <th>Error Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        {self._generate_endpoint_performance_rows(report['endpoint_performance'])}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        # Save report
        report_path = self.output_path / f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_path, 'w') as f:
            f.write(html)
            
        return str(report_path)
        
    def generate_usage_report(self, days: int = 7) -> str:
        """Generate usage analytics report"""
        report = self.analytics.generate_usage_report(days)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Usage Report - Houston Intelligence Platform</title>
    <style>
        {self._get_base_styles()}
        
        .usage-summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        
        .usage-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .usage-stat {{
            text-align: center;
        }}
        
        .usage-number {{
            font-size: 2em;
            font-weight: bold;
        }}
        
        .usage-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .daily-chart {{
            overflow-x: auto;
        }}
        
        .bar {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 5px 10px;
            margin: 2px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Usage Analytics Report</h1>
            <p>Houston Intelligence Platform - {days} Day Analysis</p>
            <p class="timestamp">Generated: {report['generated_at']}</p>
        </div>
    </header>
    
    <div class="container">
        <!-- Usage Summary -->
        <div class="usage-summary">
            <h2>Usage Summary</h2>
            <div class="usage-grid">
                <div class="usage-stat">
                    <div class="usage-number">{report['summary']['total_calls']:,}</div>
                    <div class="usage-label">Total API Calls</div>
                </div>
                <div class="usage-stat">
                    <div class="usage-number">{report['summary']['total_users']}</div>
                    <div class="usage-label">Active Users</div>
                </div>
                <div class="usage-stat">
                    <div class="usage-number">{report['summary']['avg_calls_per_user']:.1f}</div>
                    <div class="usage-label">Avg Calls/User</div>
                </div>
                <div class="usage-stat">
                    <div class="usage-number">{report['summary']['max_calls_per_user']}</div>
                    <div class="usage-label">Max Calls/User</div>
                </div>
            </div>
        </div>
        
        <!-- Daily Statistics -->
        <div class="section">
            <h2>Daily Usage Trends</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Total Calls</th>
                        <th>Avg Response Time</th>
                        <th>Errors</th>
                        <th>Error Rate</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_daily_stats_rows(report['daily_statistics'])}
                </tbody>
            </table>
        </div>
        
        <!-- Agent Usage -->
        <div class="section">
            <h2>Agent Usage Statistics</h2>
            <table>
                <thead>
                    <tr>
                        <th>Agent</th>
                        <th>Total Calls</th>
                        <th>Avg Response Time</th>
                        <th>Unique Users</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_agent_usage_rows(report['agent_usage'])}
                </tbody>
            </table>
        </div>
        
        <!-- Top Endpoints -->
        <div class="section">
            <h2>Most Used Endpoints</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Endpoint</th>
                        <th>Total Calls</th>
                        <th>Avg Response Time</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_top_endpoints_rows(report['top_endpoints'])}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
        
        # Save report
        report_path = self.output_path / f"usage_report_{days}days_{datetime.now().strftime('%Y%m%d')}.html"
        with open(report_path, 'w') as f:
            f.write(html)
            
        return str(report_path)
        
    def _get_base_styles(self) -> str:
        """Get base CSS styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px 0;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .section {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }
        
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        
        tr:hover {
            background-color: #f8f9fa;
        }
        
        .timestamp {
            color: #95a5a6;
            font-size: 0.9em;
        }
        """
        
    def _get_trend_class(self, trend: str) -> str:
        """Get CSS class for trend"""
        if trend == 'increasing':
            return 'trend-up'
        elif trend == 'decreasing':
            return 'trend-down'
        return ''
        
    def _get_trend_icon(self, trend: str) -> str:
        """Get icon for trend"""
        if trend == 'increasing':
            return '↑'
        elif trend == 'decreasing':
            return '↓'
        return '→'
        
    def _get_health_class(self, score: int) -> str:
        """Get CSS class for health score"""
        if score >= 80:
            return 'health-good'
        elif score >= 60:
            return 'health-warning'
        return 'health-critical'
        
    def _get_health_status(self, score: int) -> str:
        """Get health status text"""
        if score >= 80:
            return 'Healthy'
        elif score >= 60:
            return 'Warning'
        return 'Critical'
        
    def _generate_agent_cards(self, agent_calls: Dict[str, int]) -> str:
        """Generate agent activity cards"""
        cards = []
        for agent, calls in agent_calls.items():
            agent_class = f"agent-{agent.split('_')[0].lower()}"
            cards.append(f"""
                <div class="metric-card">
                    <div class="metric-label">{agent.replace('_', ' ')}</div>
                    <div class="metric-value">{calls:,}</div>
                    <div class="metric-change">
                        <span class="agent-badge {agent_class}">{agent.split('_')[0]}</span>
                    </div>
                </div>
            """)
        return '\n'.join(cards)
        
    def _generate_endpoint_rows(self, endpoints: List[Dict], total: int) -> str:
        """Generate endpoint table rows"""
        rows = []
        for ep in endpoints:
            percentage = (ep['count'] / total * 100) if total > 0 else 0
            rows.append(f"""
                <tr>
                    <td>{ep['endpoint']}</td>
                    <td>{ep['count']:,}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """)
        return '\n'.join(rows)
        
    def _generate_alerts(self, alerts: List[Dict]) -> str:
        """Generate alert items"""
        if not alerts:
            return '<p style="color: #7f8c8d;">No recent alerts</p>'
            
        alert_items = []
        for alert in alerts[:5]:  # Show last 5
            alert_class = f"alert-{alert['severity']}"
            timestamp = datetime.fromisoformat(alert['timestamp']).strftime('%H:%M:%S')
            alert_items.append(f"""
                <div class="alert-item {alert_class}">
                    <strong>[{alert['severity'].upper()}]</strong> {alert['message']}
                    <span class="timestamp" style="float: right;">{timestamp}</span>
                </div>
            """)
        return '\n'.join(alert_items)
        
    def _generate_metrics_rows(self, metrics: Dict) -> str:
        """Generate metrics table rows"""
        rows = []
        metric_names = {
            'avg_response_time': ('Average Response Time', 'ms', 'metric-response'),
            'error_rate': ('Error Rate', '%', 'metric-error'),
            'throughput': ('Throughput', 'calls/min', 'metric-throughput')
        }
        
        for metric_type, data in metrics.items():
            if metric_type in metric_names:
                name, unit, badge_class = metric_names[metric_type]
                rows.append(f"""
                    <tr>
                        <td><span class="metric-badge {badge_class}">{name}</span></td>
                        <td>{data['average']} {unit}</td>
                        <td>{data['min']} {unit}</td>
                        <td>{data['max']} {unit}</td>
                        <td>{data['data_points']}</td>
                    </tr>
                """)
        return '\n'.join(rows)
        
    def _generate_endpoint_performance_rows(self, endpoints: List[Dict]) -> str:
        """Generate endpoint performance rows"""
        rows = []
        for ep in endpoints[:10]:  # Top 10
            error_class = 'trend-down' if ep['error_rate'] > 5 else ''
            rows.append(f"""
                <tr>
                    <td>{ep['endpoint']}</td>
                    <td>{ep['total_calls']:,}</td>
                    <td>{ep['avg_response_time']}ms</td>
                    <td>{ep['min_response_time']}/{ep['max_response_time']}ms</td>
                    <td>{ep['std_deviation']}ms</td>
                    <td class="{error_class}">{ep['error_rate']}%</td>
                </tr>
            """)
        return '\n'.join(rows)
        
    def _generate_daily_stats_rows(self, daily_stats: List[Dict]) -> str:
        """Generate daily statistics rows"""
        rows = []
        for day in daily_stats:
            error_class = 'trend-down' if day['error_rate'] > 5 else ''
            rows.append(f"""
                <tr>
                    <td>{day['date']}</td>
                    <td>{day['calls']:,}</td>
                    <td>{day['avg_response_time']}ms</td>
                    <td>{day['errors']}</td>
                    <td class="{error_class}">{day['error_rate']}%</td>
                </tr>
            """)
        return '\n'.join(rows)
        
    def _generate_agent_usage_rows(self, agent_stats: List[Dict]) -> str:
        """Generate agent usage rows"""
        rows = []
        for agent in agent_stats:
            agent_class = f"agent-{agent['agent'].split('_')[0].lower()}"
            rows.append(f"""
                <tr>
                    <td><span class="agent-badge {agent_class}">{agent['agent'].replace('_', ' ')}</span></td>
                    <td>{agent['calls']:,}</td>
                    <td>{agent['avg_response_time']}ms</td>
                    <td>{agent['unique_users']}</td>
                </tr>
            """)
        return '\n'.join(rows)
        
    def _generate_top_endpoints_rows(self, endpoints: List[Dict]) -> str:
        """Generate top endpoints rows"""
        rows = []
        for i, ep in enumerate(endpoints[:10], 1):
            rows.append(f"""
                <tr>
                    <td>#{i}</td>
                    <td>{ep['endpoint']}</td>
                    <td>{ep['calls']:,}</td>
                    <td>{ep['avg_response_time']}ms</td>
                </tr>
            """)
        return '\n'.join(rows)
        
    def stop(self):
        """Stop monitoring"""
        self.monitor.stop()


def demo_dashboards():
    """Demo dashboard generation"""
    # Initialize
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    analytics = AnalyticsEngine(base_path)
    generator = DashboardGenerator(analytics)
    
    print("Generating dashboards...")
    
    # Generate main dashboard
    main_path = generator.generate_main_dashboard()
    print(f"✓ Main dashboard: {main_path}")
    
    # Generate performance report
    perf_path = generator.generate_performance_report(24)
    print(f"✓ Performance report: {perf_path}")
    
    # Generate usage report
    usage_path = generator.generate_usage_report(7)
    print(f"✓ Usage report: {usage_path}")
    
    print("\nDashboards generated successfully!")
    print("Open the HTML files in a browser to view the dashboards.")
    
    # Stop monitoring
    generator.stop()


if __name__ == "__main__":
    demo_dashboards()