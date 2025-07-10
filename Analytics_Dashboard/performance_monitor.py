#!/usr/bin/env python3
"""
Real-time Performance Monitoring System for Houston Intelligence Platform
Monitors API performance, system health, and generates alerts
"""

import json
import time
import threading
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import deque, defaultdict
import statistics
import sys

# Add path for analytics backend
sys.path.append(str(Path(__file__).parent))
from analytics_backend import AnalyticsEngine, PerformanceMetric


class PerformanceMonitor:
    """Real-time performance monitoring with alerts"""
    
    def __init__(self, analytics_engine: AnalyticsEngine):
        self.analytics = analytics_engine
        
        # Performance thresholds
        self.thresholds = {
            'response_time_ms': {
                'warning': 500,
                'critical': 1000
            },
            'error_rate_percent': {
                'warning': 5,
                'critical': 10
            },
            'throughput_per_minute': {
                'warning': 10,  # Less than 10 calls/min
                'critical': 5   # Less than 5 calls/min
            }
        }
        
        # Real-time metrics storage (last 5 minutes)
        self.metrics_window = defaultdict(lambda: deque(maxlen=300))  # 5 min @ 1 sample/sec
        
        # Alert history
        self.alerts = deque(maxlen=100)
        
        # Monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect current metrics
                self._collect_metrics()
                
                # Check for alerts
                self._check_alerts()
                
                # Sleep for 1 second
                time.sleep(1)
                
            except Exception as e:
                self.analytics.logger.error(f"Monitor error: {e}")
                time.sleep(5)
                
    def _collect_metrics(self):
        """Collect current performance metrics"""
        # Get recent calls from last minute
        recent_calls = self.analytics.db.get_recent_calls(hours=0.0167)  # 1 minute
        
        if not recent_calls:
            # No calls in last minute
            self.metrics_window['calls_per_minute'].append(0)
            self.metrics_window['avg_response_time'].append(0)
            self.metrics_window['error_rate'].append(0)
            return
            
        # Calculate metrics
        calls_count = len(recent_calls)
        response_times = [c['response_time_ms'] for c in recent_calls]
        error_count = sum(1 for c in recent_calls if c['status_code'] >= 400)
        
        # Store metrics
        self.metrics_window['calls_per_minute'].append(calls_count)
        self.metrics_window['avg_response_time'].append(
            statistics.mean(response_times) if response_times else 0
        )
        self.metrics_window['error_rate'].append(
            (error_count / calls_count * 100) if calls_count > 0 else 0
        )
        
        # Track by endpoint
        endpoint_metrics = defaultdict(lambda: {'count': 0, 'time': 0, 'errors': 0})
        for call in recent_calls:
            endpoint = call['endpoint']
            endpoint_metrics[endpoint]['count'] += 1
            endpoint_metrics[endpoint]['time'] += call['response_time_ms']
            if call['status_code'] >= 400:
                endpoint_metrics[endpoint]['errors'] += 1
                
        for endpoint, data in endpoint_metrics.items():
            key = f"endpoint_{endpoint}_rpm"
            self.metrics_window[key].append(data['count'])
            
    def _check_alerts(self):
        """Check metrics against thresholds and generate alerts"""
        timestamp = datetime.now()
        
        # Check average response time
        if self.metrics_window['avg_response_time']:
            avg_response = statistics.mean(list(self.metrics_window['avg_response_time'])[-60:])
            if avg_response > self.thresholds['response_time_ms']['critical']:
                self._create_alert('critical', 'response_time', avg_response, timestamp)
            elif avg_response > self.thresholds['response_time_ms']['warning']:
                self._create_alert('warning', 'response_time', avg_response, timestamp)
                
        # Check error rate
        if self.metrics_window['error_rate']:
            error_rate = statistics.mean(list(self.metrics_window['error_rate'])[-60:])
            if error_rate > self.thresholds['error_rate_percent']['critical']:
                self._create_alert('critical', 'error_rate', error_rate, timestamp)
            elif error_rate > self.thresholds['error_rate_percent']['warning']:
                self._create_alert('warning', 'error_rate', error_rate, timestamp)
                
        # Check throughput
        if self.metrics_window['calls_per_minute']:
            throughput = statistics.mean(list(self.metrics_window['calls_per_minute'])[-5:])
            if throughput < self.thresholds['throughput_per_minute']['critical']:
                self._create_alert('critical', 'low_throughput', throughput, timestamp)
            elif throughput < self.thresholds['throughput_per_minute']['warning']:
                self._create_alert('warning', 'low_throughput', throughput, timestamp)
                
    def _create_alert(self, severity: str, alert_type: str, value: float, timestamp: datetime):
        """Create and store an alert"""
        alert = {
            'timestamp': timestamp.isoformat(),
            'severity': severity,
            'type': alert_type,
            'value': value,
            'message': self._format_alert_message(alert_type, value, severity)
        }
        
        # Check if similar alert was recently created (within 5 minutes)
        recent_alerts = [a for a in self.alerts if 
                        datetime.fromisoformat(a['timestamp']) > timestamp - timedelta(minutes=5)]
        
        similar_exists = any(a['type'] == alert_type and a['severity'] == severity 
                           for a in recent_alerts)
        
        if not similar_exists:
            self.alerts.append(alert)
            self.analytics.logger.warning(f"ALERT: {alert['message']}")
            
    def _format_alert_message(self, alert_type: str, value: float, severity: str) -> str:
        """Format alert message"""
        messages = {
            'response_time': f"Average response time is {value:.0f}ms ({severity})",
            'error_rate': f"Error rate is {value:.1f}% ({severity})",
            'low_throughput': f"API throughput is {value:.1f} calls/minute ({severity})"
        }
        return messages.get(alert_type, f"Unknown alert: {alert_type}")
        
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get current real-time metrics"""
        metrics = {}
        
        # Current values
        for metric_name in ['calls_per_minute', 'avg_response_time', 'error_rate']:
            if self.metrics_window[metric_name]:
                current = list(self.metrics_window[metric_name])[-1]
                avg_1min = statistics.mean(list(self.metrics_window[metric_name])[-60:])
                avg_5min = statistics.mean(list(self.metrics_window[metric_name]))
                
                metrics[metric_name] = {
                    'current': round(current, 2),
                    'avg_1min': round(avg_1min, 2),
                    'avg_5min': round(avg_5min, 2),
                    'trend': self._calculate_trend(self.metrics_window[metric_name])
                }
            else:
                metrics[metric_name] = {
                    'current': 0,
                    'avg_1min': 0,
                    'avg_5min': 0,
                    'trend': 'stable'
                }
                
        # System health score (0-100)
        metrics['health_score'] = self._calculate_health_score()
        
        # Recent alerts
        metrics['recent_alerts'] = list(self.alerts)[-10:]  # Last 10 alerts
        
        # Endpoint-specific metrics
        endpoint_metrics = {}
        for key, values in self.metrics_window.items():
            if key.startswith('endpoint_') and key.endswith('_rpm'):
                endpoint = key.replace('endpoint_', '').replace('_rpm', '')
                if values:
                    endpoint_metrics[endpoint] = {
                        'current_rpm': list(values)[-1],
                        'avg_rpm': round(statistics.mean(values), 2)
                    }
                    
        metrics['endpoints'] = endpoint_metrics
        
        return metrics
        
    def _calculate_trend(self, values: deque) -> str:
        """Calculate trend direction"""
        if len(values) < 10:
            return 'stable'
            
        recent = list(values)[-10:]
        older = list(values)[-20:-10] if len(values) >= 20 else recent
        
        recent_avg = statistics.mean(recent)
        older_avg = statistics.mean(older)
        
        if recent_avg > older_avg * 1.1:
            return 'increasing'
        elif recent_avg < older_avg * 0.9:
            return 'decreasing'
        else:
            return 'stable'
            
    def _calculate_health_score(self) -> int:
        """Calculate overall system health score (0-100)"""
        score = 100
        
        # Deduct for response time
        if self.metrics_window['avg_response_time']:
            avg_response = statistics.mean(list(self.metrics_window['avg_response_time'])[-60:])
            if avg_response > 1000:
                score -= 30
            elif avg_response > 500:
                score -= 15
            elif avg_response > 200:
                score -= 5
                
        # Deduct for error rate
        if self.metrics_window['error_rate']:
            error_rate = statistics.mean(list(self.metrics_window['error_rate'])[-60:])
            if error_rate > 10:
                score -= 30
            elif error_rate > 5:
                score -= 15
            elif error_rate > 2:
                score -= 5
                
        # Deduct for low throughput
        if self.metrics_window['calls_per_minute']:
            throughput = statistics.mean(list(self.metrics_window['calls_per_minute'])[-5:])
            if throughput < 5:
                score -= 20
            elif throughput < 10:
                score -= 10
                
        # Deduct for recent critical alerts
        critical_alerts = sum(1 for a in self.alerts 
                            if a['severity'] == 'critical' and
                            datetime.fromisoformat(a['timestamp']) > 
                            datetime.now() - timedelta(minutes=5))
        score -= critical_alerts * 10
        
        return max(0, score)
        
    def get_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate performance report"""
        conn = sqlite3.connect(self.analytics.db.db_path)
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        # Get performance metrics from database
        cursor.execute('''
            SELECT 
                metric_type,
                AVG(value) as avg_value,
                MIN(value) as min_value,
                MAX(value) as max_value,
                COUNT(*) as data_points
            FROM performance_metrics
            WHERE timestamp > ?
            GROUP BY metric_type
        ''', (since,))
        
        metrics_summary = {}
        for row in cursor.fetchall():
            metrics_summary[row[0]] = {
                'average': round(row[1], 2),
                'min': round(row[2], 2),
                'max': round(row[3], 2),
                'data_points': row[4]
            }
            
        # Get hourly breakdown
        cursor.execute('''
            SELECT 
                strftime('%Y-%m-%d %H:00', timestamp) as hour,
                metric_type,
                AVG(value) as avg_value
            FROM performance_metrics
            WHERE timestamp > ?
            GROUP BY hour, metric_type
            ORDER BY hour
        ''', (since,))
        
        hourly_data = defaultdict(dict)
        for row in cursor.fetchall():
            hourly_data[row[0]][row[1]] = round(row[2], 2)
            
        # Get endpoint performance
        cursor.execute('''
            SELECT 
                endpoint,
                COUNT(*) as calls,
                AVG(response_time_ms) as avg_response,
                SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as errors,
                MIN(response_time_ms) as min_response,
                MAX(response_time_ms) as max_response,
                AVG(response_time_ms * response_time_ms) - AVG(response_time_ms) * AVG(response_time_ms) as variance
            FROM api_calls
            WHERE timestamp > ?
            GROUP BY endpoint
            ORDER BY calls DESC
        ''', (since,))
        
        endpoint_performance = []
        for row in cursor.fetchall():
            std_dev = row[6]**0.5 if row[6] > 0 else 0
            endpoint_performance.append({
                'endpoint': row[0],
                'total_calls': row[1],
                'avg_response_time': round(row[2], 2),
                'error_count': row[3],
                'error_rate': round((row[3] / row[1] * 100), 2) if row[1] > 0 else 0,
                'min_response_time': round(row[4], 2),
                'max_response_time': round(row[5], 2),
                'std_deviation': round(std_dev, 2)
            })
            
        conn.close()
        
        # Calculate uptime
        total_minutes = hours * 60
        healthy_minutes = sum(1 for _ in range(total_minutes) 
                            if self._was_healthy_at(datetime.now() - timedelta(minutes=_)))
        uptime_percent = (healthy_minutes / total_minutes * 100) if total_minutes > 0 else 100
        
        return {
            'report_period_hours': hours,
            'generated_at': datetime.now().isoformat(),
            'metrics_summary': metrics_summary,
            'hourly_breakdown': dict(hourly_data),
            'endpoint_performance': endpoint_performance,
            'system_uptime_percent': round(uptime_percent, 2),
            'total_alerts': len([a for a in self.alerts 
                               if datetime.fromisoformat(a['timestamp']) > 
                               datetime.now() - timedelta(hours=hours)]),
            'current_health_score': self._calculate_health_score()
        }
        
    def _was_healthy_at(self, timestamp: datetime) -> bool:
        """Check if system was healthy at given timestamp"""
        # Simple check: no critical alerts within 1 minute of timestamp
        critical_alerts = [a for a in self.alerts 
                         if a['severity'] == 'critical' and
                         abs((datetime.fromisoformat(a['timestamp']) - timestamp).total_seconds()) < 60]
        return len(critical_alerts) == 0
        
    def stop(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)


def demo_performance_monitoring(analytics_engine: AnalyticsEngine):
    """Demonstrate performance monitoring"""
    monitor = PerformanceMonitor(analytics_engine)
    
    print("Performance Monitor started...")
    print("Monitoring real-time metrics...")
    
    # Let it collect some data
    time.sleep(5)
    
    # Show real-time metrics
    for _ in range(10):
        metrics = monitor.get_real_time_metrics()
        
        print(f"\n{'='*60}")
        print(f"Real-time Metrics - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        print(f"Health Score: {metrics['health_score']}/100")
        print(f"\nCalls/minute: {metrics['calls_per_minute']['current']} "
              f"(avg: {metrics['calls_per_minute']['avg_1min']}) "
              f"[{metrics['calls_per_minute']['trend']}]")
        
        print(f"Response time: {metrics['avg_response_time']['current']}ms "
              f"(avg: {metrics['avg_response_time']['avg_1min']}ms) "
              f"[{metrics['avg_response_time']['trend']}]")
        
        print(f"Error rate: {metrics['error_rate']['current']}% "
              f"(avg: {metrics['error_rate']['avg_1min']}%) "
              f"[{metrics['error_rate']['trend']}]")
        
        if metrics['recent_alerts']:
            print(f"\nRecent Alerts:")
            for alert in metrics['recent_alerts'][-3:]:
                print(f"  [{alert['severity'].upper()}] {alert['message']}")
                
        time.sleep(3)
        
    # Generate performance report
    print(f"\n{'='*60}")
    print("24-Hour Performance Report")
    print(f"{'='*60}")
    
    report = monitor.get_performance_report(24)
    
    print(f"System Uptime: {report['system_uptime_percent']}%")
    print(f"Total Alerts: {report['total_alerts']}")
    print(f"Current Health: {report['current_health_score']}/100")
    
    print(f"\nTop Endpoints by Volume:")
    for ep in report['endpoint_performance'][:5]:
        print(f"  {ep['endpoint']}: {ep['total_calls']} calls, "
              f"{ep['avg_response_time']}ms avg, "
              f"{ep['error_rate']}% errors")
        
    monitor.stop()
    print("\nMonitor stopped.")


if __name__ == "__main__":
    # Initialize analytics engine
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    analytics = AnalyticsEngine(base_path)
    
    # Run demo
    demo_performance_monitoring(analytics)