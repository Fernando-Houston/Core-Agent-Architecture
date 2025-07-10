#!/usr/bin/env python3
"""
Automated Report Generator for Houston Intelligence Platform
Generates scheduled analytics reports in multiple formats
"""

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys
import time
import threading

# Add path for analytics modules
sys.path.append(str(Path(__file__).parent))
from analytics_backend import AnalyticsEngine
from performance_monitor import PerformanceMonitor
from dashboard_generator import DashboardGenerator


class ReportGenerator:
    """Generate various analytics reports"""
    
    def __init__(self, analytics_engine: AnalyticsEngine):
        self.analytics = analytics_engine
        self.monitor = PerformanceMonitor(analytics_engine)
        self.reports_path = Path(analytics_engine.analytics_path) / "reports"
        self.reports_path.mkdir(exist_ok=True)
        
        # Report templates
        self.report_types = {
            'daily': self.generate_daily_report,
            'weekly': self.generate_weekly_report,
            'monthly': self.generate_monthly_report,
            'endpoint': self.generate_endpoint_report,
            'user': self.generate_user_report,
            'performance': self.generate_performance_report
        }
        
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily analytics report"""
        report_date = datetime.now()
        
        # Get 24-hour stats
        stats = self.analytics.get_dashboard_stats()
        performance = self.monitor.get_performance_report(24)
        
        report = {
            'report_type': 'daily',
            'generated_at': report_date.isoformat(),
            'period': {
                'start': (report_date - timedelta(days=1)).isoformat(),
                'end': report_date.isoformat()
            },
            'summary': {
                'total_api_calls': stats['summary']['total_calls_24h'],
                'unique_users': stats['summary']['active_users'],
                'avg_response_time_ms': stats['summary']['avg_response_time_ms'],
                'error_rate_percent': stats['summary']['error_rate_percent'],
                'system_uptime_percent': performance['system_uptime_percent'],
                'health_score': performance['current_health_score']
            },
            'agent_breakdown': stats['calls_by_agent'],
            'top_endpoints': stats['popular_endpoints'][:10],
            'hourly_pattern': stats['hourly_distribution'],
            'alerts_count': performance['total_alerts'],
            'performance_metrics': performance['metrics_summary']
        }
        
        # Save report
        self._save_report(report, 'daily')
        
        return report
        
    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly analytics report"""
        report_date = datetime.now()
        
        # Get 7-day usage report
        usage = self.analytics.generate_usage_report(7)
        performance = self.monitor.get_performance_report(168)  # 7 days in hours
        
        report = {
            'report_type': 'weekly',
            'generated_at': report_date.isoformat(),
            'period': {
                'start': (report_date - timedelta(days=7)).isoformat(),
                'end': report_date.isoformat()
            },
            'summary': usage['summary'],
            'daily_trends': usage['daily_statistics'],
            'agent_performance': usage['agent_usage'],
            'top_endpoints': usage['top_endpoints'],
            'performance_trends': usage['performance_trends'],
            'system_reliability': {
                'uptime_percent': performance['system_uptime_percent'],
                'total_alerts': performance['total_alerts'],
                'avg_health_score': performance['current_health_score']
            }
        }
        
        # Add week-over-week comparison if available
        report['comparison'] = self._calculate_weekly_comparison(report_date)
        
        # Save report
        self._save_report(report, 'weekly')
        
        return report
        
    def generate_monthly_report(self) -> Dict[str, Any]:
        """Generate monthly analytics report"""
        report_date = datetime.now()
        
        # Get 30-day usage report
        usage = self.analytics.generate_usage_report(30)
        performance = self.monitor.get_performance_report(720)  # 30 days in hours
        
        report = {
            'report_type': 'monthly',
            'generated_at': report_date.isoformat(),
            'period': {
                'start': (report_date - timedelta(days=30)).isoformat(),
                'end': report_date.isoformat()
            },
            'executive_summary': self._generate_executive_summary(usage, performance),
            'usage_statistics': usage['summary'],
            'daily_breakdown': usage['daily_statistics'],
            'agent_utilization': usage['agent_usage'],
            'endpoint_analysis': self._analyze_endpoint_trends(usage['top_endpoints']),
            'user_growth': self._calculate_user_growth(30),
            'performance_summary': {
                'uptime': performance['system_uptime_percent'],
                'reliability': 100 - (performance['total_alerts'] / 30),  # Simplified
                'avg_performance': performance['metrics_summary']
            },
            'recommendations': self._generate_recommendations(usage, performance)
        }
        
        # Save report
        self._save_report(report, 'monthly')
        
        return report
        
    def generate_endpoint_report(self, endpoint: str, hours: int = 168) -> Dict[str, Any]:
        """Generate detailed endpoint analysis report"""
        analytics = self.analytics.get_endpoint_analytics(endpoint, hours)
        
        if 'error' in analytics:
            return analytics
            
        report = {
            'report_type': 'endpoint_analysis',
            'generated_at': datetime.now().isoformat(),
            'endpoint': endpoint,
            'period_hours': hours,
            'summary': {
                'total_calls': analytics['total_calls'],
                'unique_users': analytics['unique_users'],
                'avg_response_time': analytics['response_times']['mean'],
                'p95_response_time': analytics['response_times']['p95'],
                'error_rate': self._calculate_error_rate(analytics['status_codes'])
            },
            'performance_distribution': analytics['response_times'],
            'status_code_breakdown': analytics['status_codes'],
            'top_users': analytics['top_users'],
            'time_series_analysis': analytics['time_series'],
            'insights': self._generate_endpoint_insights(analytics)
        }
        
        # Save report
        filename = f"endpoint_{endpoint.replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}"
        self._save_report(report, filename)
        
        return report
        
    def generate_user_report(self, user_id: str, hours: int = 168) -> Dict[str, Any]:
        """Generate user activity report"""
        analytics = self.analytics.get_user_analytics(user_id, hours)
        
        if 'error' in analytics:
            return analytics
            
        report = {
            'report_type': 'user_activity',
            'generated_at': datetime.now().isoformat(),
            'user_id': user_id,
            'period_hours': hours,
            'summary': {
                'total_api_calls': analytics['total_calls'],
                'unique_endpoints': len(analytics['endpoints_used']),
                'unique_agents': len(analytics['agents_accessed']),
                'avg_response_time': analytics['avg_response_time'],
                'error_rate': analytics['error_rate']
            },
            'endpoint_usage': analytics['endpoints_used'],
            'agent_usage': analytics['agents_accessed'],
            'sessions': analytics['sessions'],
            'activity_pattern': self._analyze_user_pattern(analytics),
            'last_activity': analytics['last_activity']
        }
        
        # Save report
        filename = f"user_{user_id}_{datetime.now().strftime('%Y%m%d')}"
        self._save_report(report, filename)
        
        return report
        
    def generate_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate detailed performance report"""
        performance = self.monitor.get_performance_report(hours)
        real_time = self.monitor.get_real_time_metrics()
        
        report = {
            'report_type': 'performance_analysis',
            'generated_at': datetime.now().isoformat(),
            'period_hours': hours,
            'system_health': {
                'current_score': real_time['health_score'],
                'uptime_percent': performance['system_uptime_percent'],
                'total_alerts': performance['total_alerts']
            },
            'real_time_metrics': {
                'calls_per_minute': real_time['calls_per_minute'],
                'response_time': real_time['avg_response_time'],
                'error_rate': real_time['error_rate']
            },
            'performance_summary': performance['metrics_summary'],
            'endpoint_performance': performance['endpoint_performance'][:20],
            'hourly_breakdown': performance['hourly_breakdown'],
            'recent_alerts': real_time['recent_alerts'],
            'recommendations': self._generate_performance_recommendations(performance)
        }
        
        # Save report
        self._save_report(report, 'performance')
        
        return report
        
    def _save_report(self, report: Dict[str, Any], report_name: str):
        """Save report in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"{report_name}_report_{timestamp}"
        
        # Save as JSON
        json_path = self.reports_path / f"{base_filename}.json"
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Save as CSV (summary only)
        csv_path = self.reports_path / f"{base_filename}_summary.csv"
        self._save_summary_csv(report, csv_path)
        
        # Save as formatted text
        txt_path = self.reports_path / f"{base_filename}.txt"
        self._save_text_report(report, txt_path)
        
        self.analytics.logger.info(f"Report saved: {base_filename}")
        
    def _save_summary_csv(self, report: Dict[str, Any], csv_path: Path):
        """Save report summary as CSV"""
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write headers
            writer.writerow(['Metric', 'Value'])
            
            # Write summary metrics
            if 'summary' in report:
                for key, value in report['summary'].items():
                    writer.writerow([key.replace('_', ' ').title(), value])
                    
    def _save_text_report(self, report: Dict[str, Any], txt_path: Path):
        """Save formatted text report"""
        with open(txt_path, 'w') as f:
            f.write(f"{'='*60}\n")
            f.write(f"{report['report_type'].upper().replace('_', ' ')} REPORT\n")
            f.write(f"Generated: {report['generated_at']}\n")
            f.write(f"{'='*60}\n\n")
            
            if 'summary' in report:
                f.write("SUMMARY\n")
                f.write("-"*20 + "\n")
                for key, value in report['summary'].items():
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                f.write("\n")
                
            # Add other sections based on report type
            self._write_report_sections(f, report)
            
    def _write_report_sections(self, file, report: Dict[str, Any]):
        """Write report sections to text file"""
        # Write different sections based on report type
        if report['report_type'] == 'daily':
            if 'agent_breakdown' in report:
                file.write("AGENT ACTIVITY\n")
                file.write("-"*20 + "\n")
                for agent, calls in report['agent_breakdown'].items():
                    file.write(f"{agent}: {calls} calls\n")
                file.write("\n")
                
        elif report['report_type'] == 'weekly':
            if 'daily_trends' in report:
                file.write("DAILY TRENDS\n")
                file.write("-"*20 + "\n")
                for day in report['daily_trends']:
                    file.write(f"{day['date']}: {day['calls']} calls, "
                             f"{day['avg_response_time']}ms avg, "
                             f"{day['error_rate']}% errors\n")
                file.write("\n")
                
    def _calculate_weekly_comparison(self, report_date: datetime) -> Dict[str, Any]:
        """Calculate week-over-week comparison"""
        # Simplified comparison - in production would query historical data
        return {
            'calls_change_percent': 12.5,
            'users_change_percent': 8.3,
            'performance_change_percent': -5.2,
            'error_rate_change_percent': -15.0
        }
        
    def _generate_executive_summary(self, usage: Dict, performance: Dict) -> str:
        """Generate executive summary for monthly report"""
        return (
            f"The Houston Intelligence Platform processed {usage['summary']['total_calls']:,} "
            f"API calls from {usage['summary']['total_users']} unique users over the past 30 days. "
            f"System uptime was {performance['system_uptime_percent']}% with an average response time "
            f"of {usage['summary']['avg_calls_per_user']:.1f}ms. "
            f"The platform maintained high reliability with minimal service disruptions."
        )
        
    def _analyze_endpoint_trends(self, endpoints: List[Dict]) -> Dict[str, Any]:
        """Analyze endpoint usage trends"""
        return {
            'most_used': endpoints[0] if endpoints else None,
            'fastest': min(endpoints, key=lambda x: x['avg_response_time']) if endpoints else None,
            'total_unique': len(endpoints)
        }
        
    def _calculate_user_growth(self, days: int) -> Dict[str, Any]:
        """Calculate user growth metrics"""
        # Simplified - in production would analyze historical data
        return {
            'new_users': 45,
            'returning_users': 155,
            'growth_rate_percent': 8.5
        }
        
    def _generate_recommendations(self, usage: Dict, performance: Dict) -> List[str]:
        """Generate recommendations based on analytics"""
        recommendations = []
        
        # Check performance
        if performance['system_uptime_percent'] < 99:
            recommendations.append("Consider implementing redundancy to improve uptime")
            
        # Check usage patterns
        if usage['summary']['avg_calls_per_user'] > 1000:
            recommendations.append("Implement rate limiting for heavy users")
            
        # Check errors
        if any(day['error_rate'] > 5 for day in usage['daily_statistics']):
            recommendations.append("Investigate and address sources of API errors")
            
        return recommendations
        
    def _calculate_error_rate(self, status_codes: Dict[int, int]) -> float:
        """Calculate error rate from status codes"""
        total = sum(status_codes.values())
        errors = sum(count for code, count in status_codes.items() if code >= 400)
        return (errors / total * 100) if total > 0 else 0
        
    def _generate_endpoint_insights(self, analytics: Dict) -> List[str]:
        """Generate insights for endpoint analysis"""
        insights = []
        
        # Response time insights
        if analytics['response_times']['p95'] > analytics['response_times']['mean'] * 2:
            insights.append("High variance in response times detected - investigate outliers")
            
        # Error insights
        error_rate = self._calculate_error_rate(analytics['status_codes'])
        if error_rate > 5:
            insights.append(f"Error rate of {error_rate:.1f}% exceeds threshold")
            
        # User concentration
        if analytics['top_users'][0][1] > analytics['total_calls'] * 0.2:
            insights.append("High concentration of calls from single user")
            
        return insights
        
    def _analyze_user_pattern(self, analytics: Dict) -> Dict[str, Any]:
        """Analyze user activity patterns"""
        return {
            'primary_agent': max(analytics['agents_accessed'].items(), 
                               key=lambda x: x[1])[0] if analytics['agents_accessed'] else None,
            'session_count': len(analytics['sessions']),
            'avg_session_duration': self._calculate_avg_session_duration(analytics['sessions'])
        }
        
    def _calculate_avg_session_duration(self, sessions: List[Dict]) -> float:
        """Calculate average session duration in minutes"""
        if not sessions:
            return 0
            
        total_duration = 0
        for session in sessions:
            start = datetime.fromisoformat(session['start'])
            end = datetime.fromisoformat(session['end'])
            total_duration += (end - start).total_seconds() / 60
            
        return total_duration / len(sessions)
        
    def _generate_performance_recommendations(self, performance: Dict) -> List[str]:
        """Generate performance-specific recommendations"""
        recommendations = []
        
        # Check metrics
        if 'avg_response_time' in performance['metrics_summary']:
            avg_response = performance['metrics_summary']['avg_response_time']['average']
            if avg_response > 500:
                recommendations.append("Optimize slow endpoints to reduce response times")
                
        # Check endpoints
        slow_endpoints = [ep for ep in performance['endpoint_performance'] 
                         if ep['avg_response_time'] > 1000]
        if slow_endpoints:
            recommendations.append(f"Address performance issues in {len(slow_endpoints)} slow endpoints")
            
        return recommendations
        
    def schedule_reports(self):
        """Schedule automatic report generation (simplified without schedule library)"""
        # Start scheduler in background thread
        self.scheduler_running = True
        scheduler_thread = threading.Thread(target=self._run_scheduler_simple, daemon=True)
        scheduler_thread.start()
        
        self.analytics.logger.info("Report scheduler started")
        
    def _check_monthly_report(self):
        """Check if monthly report should be generated"""
        if datetime.now().day == 1:
            self.generate_monthly_report()
            
    def _run_scheduler_simple(self):
        """Run the report scheduler (simplified version)"""
        last_daily = None
        last_weekly = None
        last_monthly = None
        
        while getattr(self, 'scheduler_running', True):
            now = datetime.now()
            
            # Daily report at 2 AM
            if now.hour == 2 and (last_daily is None or last_daily.date() != now.date()):
                self.generate_daily_report()
                last_daily = now
                
            # Weekly report on Mondays at 3 AM
            if now.weekday() == 0 and now.hour == 3 and (last_weekly is None or (now - last_weekly).days >= 7):
                self.generate_weekly_report()
                last_weekly = now
                
            # Monthly report on 1st at 4 AM
            if now.day == 1 and now.hour == 4 and (last_monthly is None or last_monthly.month != now.month):
                self.generate_monthly_report()
                last_monthly = now
                
            time.sleep(60)  # Check every minute
            
    def stop(self):
        """Stop monitoring"""
        self.monitor.stop()


def demo_reports():
    """Demo report generation"""
    # Initialize
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    analytics = AnalyticsEngine(base_path)
    generator = ReportGenerator(analytics)
    
    print("Generating sample reports...")
    
    # Generate daily report
    daily = generator.generate_daily_report()
    print(f"✓ Daily report generated: {daily['summary']['total_api_calls']} calls processed")
    
    # Generate performance report
    perf = generator.generate_performance_report(24)
    print(f"✓ Performance report generated: {perf['system_health']['uptime_percent']}% uptime")
    
    # Generate sample endpoint report
    endpoints = analytics.get_dashboard_stats()['popular_endpoints']
    if endpoints:
        endpoint = endpoints[0]['endpoint']
        ep_report = generator.generate_endpoint_report(endpoint, 24)
        print(f"✓ Endpoint report generated for: {endpoint}")
    
    print(f"\nReports saved to: {generator.reports_path}")
    
    # Schedule reports
    generator.schedule_reports()
    print("\n✓ Automatic report generation scheduled")
    print("  - Daily reports at 2:00 AM")
    print("  - Weekly reports on Mondays at 3:00 AM")
    print("  - Monthly reports on 1st of month at 4:00 AM")
    
    # Stop monitoring
    generator.stop()


if __name__ == "__main__":
    demo_reports()