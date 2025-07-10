#!/usr/bin/env python3
"""
Houston Intelligence Platform - Analytics Dashboard Demo
Demonstrates the complete analytics and monitoring system
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add path for analytics modules
sys.path.append(str(Path(__file__).parent))
from analytics_backend import AnalyticsEngine
from api_tracker_v2 import simulate_api_traffic
from performance_monitor import PerformanceMonitor
from dashboard_generator import DashboardGenerator
from report_generator import ReportGenerator


def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")


def main():
    """Run complete analytics demo"""
    print_section("HOUSTON INTELLIGENCE PLATFORM - ANALYTICS DEMO")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize analytics engine
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    analytics = AnalyticsEngine(base_path)
    
    print("\n✓ Analytics engine initialized")
    print(f"  Database: {analytics.analytics_path}/analytics.db")
    print(f"  Logging: {analytics.analytics_path}/analytics.log")
    
    # Step 1: Simulate API traffic
    print_section("STEP 1: SIMULATING API TRAFFIC")
    print("Generating realistic API traffic patterns...")
    simulate_api_traffic(analytics, duration_seconds=30)
    
    # Step 2: Performance monitoring
    print_section("STEP 2: PERFORMANCE MONITORING")
    monitor = PerformanceMonitor(analytics)
    print("Performance monitor started...")
    
    # Let it collect some metrics
    time.sleep(5)
    
    # Show real-time metrics
    metrics = monitor.get_real_time_metrics()
    print(f"\nSystem Health Score: {metrics['health_score']}/100")
    print(f"Current Throughput: {metrics['calls_per_minute']['current']} calls/minute")
    print(f"Average Response Time: {metrics['avg_response_time']['current']}ms")
    print(f"Error Rate: {metrics['error_rate']['current']}%")
    
    if metrics['recent_alerts']:
        print(f"\nRecent Alerts: {len(metrics['recent_alerts'])}")
        for alert in metrics['recent_alerts'][-3:]:
            print(f"  [{alert['severity'].upper()}] {alert['message']}")
    
    # Step 3: Generate dashboards
    print_section("STEP 3: GENERATING DASHBOARDS")
    dashboard_gen = DashboardGenerator(analytics)
    
    # Main dashboard
    main_dash = dashboard_gen.generate_main_dashboard()
    print(f"✓ Main dashboard: {main_dash}")
    
    # Performance report
    perf_dash = dashboard_gen.generate_performance_report(24)
    print(f"✓ Performance report: {perf_dash}")
    
    # Usage report
    usage_dash = dashboard_gen.generate_usage_report(7)
    print(f"✓ Usage report: {usage_dash}")
    
    # Step 4: Generate reports
    print_section("STEP 4: GENERATING ANALYTICS REPORTS")
    report_gen = ReportGenerator(analytics)
    
    # Daily report
    daily = report_gen.generate_daily_report()
    print(f"✓ Daily report generated")
    print(f"  Total calls: {daily['summary']['total_api_calls']}")
    print(f"  Active users: {daily['summary']['unique_users']}")
    print(f"  Health score: {daily['summary']['health_score']}/100")
    
    # Performance analysis
    perf = report_gen.generate_performance_report(24)
    print(f"\n✓ Performance analysis generated")
    print(f"  System uptime: {perf['system_health']['uptime_percent']}%")
    print(f"  Total alerts: {perf['system_health']['total_alerts']}")
    
    # Step 5: Show analytics insights
    print_section("STEP 5: ANALYTICS INSIGHTS")
    
    # Get dashboard stats
    stats = analytics.get_dashboard_stats()
    
    print("\nAgent Usage Distribution:")
    for agent, calls in stats['calls_by_agent'].items():
        percentage = (calls / stats['summary']['total_calls_24h'] * 100) if stats['summary']['total_calls_24h'] > 0 else 0
        print(f"  {agent}: {calls} calls ({percentage:.1f}%)")
    
    print("\nTop 5 Endpoints:")
    for i, endpoint in enumerate(stats['popular_endpoints'][:5], 1):
        print(f"  {i}. {endpoint['endpoint']}: {endpoint['count']} calls")
    
    print("\nHourly Activity Pattern:")
    peak_hour = max(stats['hourly_distribution'], key=lambda x: x['count'])
    print(f"  Peak hour: {peak_hour['hour']}:00 with {peak_hour['count']} calls")
    
    # Step 6: Schedule automated reports
    print_section("STEP 6: SCHEDULING AUTOMATED REPORTS")
    report_gen.schedule_reports()
    print("✓ Automatic report generation scheduled:")
    print("  - Daily reports at 2:00 AM")
    print("  - Weekly reports on Mondays at 3:00 AM") 
    print("  - Monthly reports on 1st of month at 4:00 AM")
    
    # Summary
    print_section("ANALYTICS SYSTEM SUMMARY")
    print("✓ Complete analytics infrastructure deployed:")
    print("  1. Real-time API call tracking")
    print("  2. Performance monitoring with alerts")
    print("  3. Interactive HTML dashboards")
    print("  4. Automated report generation")
    print("  5. Historical data analysis")
    print("  6. User and endpoint analytics")
    
    print(f"\n📊 Dashboard files: {analytics.analytics_path}/dashboards/")
    print(f"📄 Report files: {analytics.analytics_path}/reports/")
    print(f"💾 Database: {analytics.analytics_path}/analytics.db")
    print(f"📝 Logs: {analytics.analytics_path}/analytics.log")
    
    print("\n✅ Analytics system ready for production use!")
    print("\nNote: Dashboards auto-refresh every 30 seconds when opened in browser")
    
    # Cleanup
    monitor.stop()
    dashboard_gen.stop()
    report_gen.stop()
    
    print_section("DEMO COMPLETE")
    print("The analytics system continues running in the background.")
    print("Open the HTML dashboard files to view live analytics.")


if __name__ == "__main__":
    main()