#!/usr/bin/env python3
"""
Analytics Backend System for Houston Intelligence Platform
Tracks API usage, performance metrics, and user patterns
"""

import json
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import threading
import queue
import logging
from dataclasses import dataclass, asdict
import statistics


@dataclass
class APICall:
    """Represents a single API call"""
    timestamp: str
    endpoint: str
    method: str
    agent: str
    response_time_ms: float
    status_code: int
    user_id: str
    query_params: Dict[str, Any]
    error: Optional[str] = None
    request_size: int = 0
    response_size: int = 0


@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    timestamp: str
    metric_type: str  # response_time, error_rate, throughput
    value: float
    endpoint: str
    agent: str


class AnalyticsDatabase:
    """SQLite database for analytics storage"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # API calls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                method TEXT NOT NULL,
                agent TEXT NOT NULL,
                response_time_ms REAL NOT NULL,
                status_code INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                query_params TEXT,
                error TEXT,
                request_size INTEGER,
                response_size INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                value REAL NOT NULL,
                endpoint TEXT,
                agent TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_start TEXT NOT NULL,
                session_end TEXT,
                total_calls INTEGER DEFAULT 0,
                agents_accessed TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_calls_timestamp ON api_calls(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_calls_endpoint ON api_calls(endpoint)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_calls_user ON api_calls(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_timestamp ON performance_metrics(timestamp)')
        
        conn.commit()
        conn.close()
        
    def insert_api_call(self, api_call: APICall):
        """Insert API call record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_calls 
            (timestamp, endpoint, method, agent, response_time_ms, status_code, 
             user_id, query_params, error, request_size, response_size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            api_call.timestamp,
            api_call.endpoint,
            api_call.method,
            api_call.agent,
            api_call.response_time_ms,
            api_call.status_code,
            api_call.user_id,
            json.dumps(api_call.query_params),
            api_call.error,
            api_call.request_size,
            api_call.response_size
        ))
        
        conn.commit()
        conn.close()
        
    def insert_performance_metric(self, metric: PerformanceMetric):
        """Insert performance metric"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_metrics 
            (timestamp, metric_type, value, endpoint, agent)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            metric.timestamp,
            metric.metric_type,
            metric.value,
            metric.endpoint,
            metric.agent
        ))
        
        conn.commit()
        conn.close()
        
    def get_recent_calls(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent API calls"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        cursor.execute('''
            SELECT * FROM api_calls 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC
        ''', (since,))
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results


class AnalyticsEngine:
    """Main analytics engine for tracking and monitoring"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.analytics_path = self.base_path / "Analytics_Dashboard"
        self.analytics_path.mkdir(exist_ok=True)
        
        # Initialize database
        self.db = AnalyticsDatabase(str(self.analytics_path / "analytics.db"))
        
        # In-memory caches for real-time metrics
        self.recent_calls = queue.Queue(maxsize=1000)
        self.endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'errors': 0,
            'last_called': None
        })
        
        # Setup logging
        self.setup_logging()
        
        # Start background processing
        self.processing_thread = threading.Thread(target=self._process_metrics, daemon=True)
        self.processing_thread.start()
        
    def setup_logging(self):
        """Setup logging system"""
        log_file = self.analytics_path / "analytics.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AnalyticsEngine')
        
    def track_api_call(self, 
                      endpoint: str,
                      method: str,
                      agent: str,
                      response_time_ms: float,
                      status_code: int,
                      user_id: str,
                      query_params: Dict[str, Any] = None,
                      error: str = None,
                      request_size: int = 0,
                      response_size: int = 0):
        """Track an API call"""
        
        api_call = APICall(
            timestamp=datetime.now().isoformat(),
            endpoint=endpoint,
            method=method,
            agent=agent,
            response_time_ms=response_time_ms,
            status_code=status_code,
            user_id=user_id,
            query_params=query_params or {},
            error=error,
            request_size=request_size,
            response_size=response_size
        )
        
        # Store in database
        self.db.insert_api_call(api_call)
        
        # Update in-memory stats
        self._update_endpoint_stats(api_call)
        
        # Add to recent calls queue
        try:
            self.recent_calls.put_nowait(api_call)
        except queue.Full:
            # Remove oldest and add new
            self.recent_calls.get()
            self.recent_calls.put_nowait(api_call)
            
        # Log the call
        if status_code >= 400:
            self.logger.error(f"API Error: {endpoint} - {status_code} - {error}")
        else:
            self.logger.info(f"API Call: {endpoint} - {response_time_ms}ms")
            
    def _update_endpoint_stats(self, api_call: APICall):
        """Update in-memory endpoint statistics"""
        stats = self.endpoint_stats[api_call.endpoint]
        stats['count'] += 1
        stats['total_time'] += api_call.response_time_ms
        stats['last_called'] = api_call.timestamp
        
        if api_call.status_code >= 400:
            stats['errors'] += 1
            
    def _process_metrics(self):
        """Background thread to process and aggregate metrics"""
        while True:
            try:
                # Calculate and store performance metrics every minute
                self._calculate_performance_metrics()
                time.sleep(60)  # Run every minute
            except Exception as e:
                self.logger.error(f"Error processing metrics: {e}")
                time.sleep(60)
                
    def _calculate_performance_metrics(self):
        """Calculate and store performance metrics"""
        # Get recent calls from last 5 minutes
        recent_calls = self.db.get_recent_calls(hours=0.083)  # 5 minutes
        
        if not recent_calls:
            return
            
        # Group by endpoint
        endpoint_groups = defaultdict(list)
        for call in recent_calls:
            endpoint_groups[call['endpoint']].append(call)
            
        # Calculate metrics for each endpoint
        for endpoint, calls in endpoint_groups.items():
            # Average response time
            response_times = [c['response_time_ms'] for c in calls]
            avg_response_time = statistics.mean(response_times)
            
            # Error rate
            error_count = sum(1 for c in calls if c['status_code'] >= 400)
            error_rate = (error_count / len(calls)) * 100
            
            # Throughput (calls per minute)
            throughput = len(calls) / 5  # 5-minute window
            
            # Store metrics
            timestamp = datetime.now().isoformat()
            
            self.db.insert_performance_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type='avg_response_time',
                value=avg_response_time,
                endpoint=endpoint,
                agent=calls[0]['agent']
            ))
            
            self.db.insert_performance_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type='error_rate',
                value=error_rate,
                endpoint=endpoint,
                agent=calls[0]['agent']
            ))
            
            self.db.insert_performance_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type='throughput',
                value=throughput,
                endpoint=endpoint,
                agent=calls[0]['agent']
            ))
            
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get current dashboard statistics"""
        conn = sqlite3.connect(str(self.analytics_path / "analytics.db"))
        cursor = conn.cursor()
        
        # Total API calls (last 24 hours)
        since_24h = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute(
            'SELECT COUNT(*) FROM api_calls WHERE timestamp > ?',
            (since_24h,)
        )
        total_calls_24h = cursor.fetchone()[0]
        
        # Average response time (last 24 hours)
        cursor.execute(
            'SELECT AVG(response_time_ms) FROM api_calls WHERE timestamp > ?',
            (since_24h,)
        )
        avg_response_time = cursor.fetchone()[0] or 0
        
        # Error rate (last 24 hours)
        cursor.execute(
            'SELECT COUNT(*) FROM api_calls WHERE timestamp > ? AND status_code >= 400',
            (since_24h,)
        )
        error_count = cursor.fetchone()[0]
        error_rate = (error_count / total_calls_24h * 100) if total_calls_24h > 0 else 0
        
        # Popular endpoints
        cursor.execute('''
            SELECT endpoint, COUNT(*) as count 
            FROM api_calls 
            WHERE timestamp > ?
            GROUP BY endpoint 
            ORDER BY count DESC 
            LIMIT 10
        ''', (since_24h,))
        popular_endpoints = [{'endpoint': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Active users
        cursor.execute(
            'SELECT COUNT(DISTINCT user_id) FROM api_calls WHERE timestamp > ?',
            (since_24h,)
        )
        active_users = cursor.fetchone()[0]
        
        # Calls by agent
        cursor.execute('''
            SELECT agent, COUNT(*) as count 
            FROM api_calls 
            WHERE timestamp > ?
            GROUP BY agent 
            ORDER BY count DESC
        ''', (since_24h,))
        calls_by_agent = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Hourly call distribution
        cursor.execute('''
            SELECT 
                strftime('%H', timestamp) as hour,
                COUNT(*) as count
            FROM api_calls
            WHERE timestamp > ?
            GROUP BY hour
            ORDER BY hour
        ''', (since_24h,))
        hourly_distribution = [{'hour': int(row[0]), 'count': row[1]} for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'summary': {
                'total_calls_24h': total_calls_24h,
                'avg_response_time_ms': round(avg_response_time, 2),
                'error_rate_percent': round(error_rate, 2),
                'active_users': active_users
            },
            'popular_endpoints': popular_endpoints,
            'calls_by_agent': calls_by_agent,
            'hourly_distribution': hourly_distribution,
            'real_time_stats': self._get_real_time_stats()
        }
        
    def _get_real_time_stats(self) -> Dict[str, Any]:
        """Get real-time statistics from memory"""
        # Convert queue to list for processing
        recent_calls_list = list(self.recent_calls.queue)
        
        if not recent_calls_list:
            return {
                'calls_last_minute': 0,
                'avg_response_last_minute': 0,
                'active_endpoints': 0
            }
            
        # Calls in last minute
        one_minute_ago = (datetime.now() - timedelta(minutes=1)).isoformat()
        calls_last_minute = [
            c for c in recent_calls_list 
            if c.timestamp > one_minute_ago
        ]
        
        # Average response time for last minute
        if calls_last_minute:
            avg_response = statistics.mean([c.response_time_ms for c in calls_last_minute])
        else:
            avg_response = 0
            
        # Active endpoints
        active_endpoints = len(set(c.endpoint for c in calls_last_minute))
        
        return {
            'calls_last_minute': len(calls_last_minute),
            'avg_response_last_minute': round(avg_response, 2),
            'active_endpoints': active_endpoints
        }
        
    def get_endpoint_analytics(self, endpoint: str, hours: int = 24) -> Dict[str, Any]:
        """Get detailed analytics for a specific endpoint"""
        conn = sqlite3.connect(str(self.analytics_path / "analytics.db"))
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        # Get all calls for this endpoint
        cursor.execute('''
            SELECT * FROM api_calls 
            WHERE endpoint = ? AND timestamp > ?
            ORDER BY timestamp DESC
        ''', (endpoint, since))
        
        calls = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        calls_data = [dict(zip(columns, row)) for row in calls]
        
        if not calls_data:
            return {'error': 'No data found for endpoint'}
            
        # Calculate statistics
        response_times = [c['response_time_ms'] for c in calls_data]
        status_codes = [c['status_code'] for c in calls_data]
        
        # Response time percentiles
        sorted_times = sorted(response_times)
        p50 = sorted_times[len(sorted_times)//2]
        p95 = sorted_times[int(len(sorted_times)*0.95)] if len(sorted_times) > 20 else max(sorted_times)
        p99 = sorted_times[int(len(sorted_times)*0.99)] if len(sorted_times) > 100 else max(sorted_times)
        
        # Status code distribution
        status_distribution = Counter(status_codes)
        
        # User distribution
        user_distribution = Counter(c['user_id'] for c in calls_data)
        
        # Time series data (hourly)
        hourly_data = defaultdict(lambda: {'count': 0, 'total_time': 0, 'errors': 0})
        for call in calls_data:
            hour = call['timestamp'][:13]  # YYYY-MM-DDTHH
            hourly_data[hour]['count'] += 1
            hourly_data[hour]['total_time'] += call['response_time_ms']
            if call['status_code'] >= 400:
                hourly_data[hour]['errors'] += 1
                
        # Convert to list
        time_series = []
        for hour, data in sorted(hourly_data.items()):
            time_series.append({
                'hour': hour,
                'count': data['count'],
                'avg_response_time': data['total_time'] / data['count'],
                'error_count': data['errors']
            })
            
        conn.close()
        
        return {
            'endpoint': endpoint,
            'total_calls': len(calls_data),
            'time_period_hours': hours,
            'response_times': {
                'mean': statistics.mean(response_times),
                'median': statistics.median(response_times),
                'p95': p95,
                'p99': p99,
                'min': min(response_times),
                'max': max(response_times)
            },
            'status_codes': dict(status_distribution),
            'unique_users': len(user_distribution),
            'top_users': user_distribution.most_common(10),
            'time_series': time_series
        }
        
    def get_user_analytics(self, user_id: str, hours: int = 24) -> Dict[str, Any]:
        """Get analytics for a specific user"""
        conn = sqlite3.connect(str(self.analytics_path / "analytics.db"))
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        # Get user's API calls
        cursor.execute('''
            SELECT * FROM api_calls 
            WHERE user_id = ? AND timestamp > ?
            ORDER BY timestamp DESC
        ''', (user_id, since))
        
        calls = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        calls_data = [dict(zip(columns, row)) for row in calls]
        
        if not calls_data:
            return {'error': 'No data found for user'}
            
        # Endpoints used
        endpoint_usage = Counter(c['endpoint'] for c in calls_data)
        
        # Agents accessed
        agent_usage = Counter(c['agent'] for c in calls_data)
        
        # Calculate session info
        sessions = self._calculate_user_sessions(calls_data)
        
        # Error analysis
        errors = [c for c in calls_data if c['status_code'] >= 400]
        
        conn.close()
        
        return {
            'user_id': user_id,
            'total_calls': len(calls_data),
            'time_period_hours': hours,
            'endpoints_used': dict(endpoint_usage),
            'agents_accessed': dict(agent_usage),
            'sessions': sessions,
            'error_count': len(errors),
            'error_rate': (len(errors) / len(calls_data) * 100) if calls_data else 0,
            'avg_response_time': statistics.mean([c['response_time_ms'] for c in calls_data]),
            'last_activity': calls_data[0]['timestamp'] if calls_data else None
        }
        
    def _calculate_user_sessions(self, calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate user sessions from API calls"""
        if not calls:
            return []
            
        # Sort by timestamp
        sorted_calls = sorted(calls, key=lambda x: x['timestamp'])
        
        sessions = []
        current_session = {
            'start': sorted_calls[0]['timestamp'],
            'end': sorted_calls[0]['timestamp'],
            'calls': 1,
            'endpoints': {sorted_calls[0]['endpoint']}
        }
        
        # Session timeout: 30 minutes
        session_timeout = timedelta(minutes=30)
        
        for i in range(1, len(sorted_calls)):
            call_time = datetime.fromisoformat(sorted_calls[i]['timestamp'])
            prev_time = datetime.fromisoformat(sorted_calls[i-1]['timestamp'])
            
            if call_time - prev_time > session_timeout:
                # New session
                current_session['endpoints'] = list(current_session['endpoints'])
                sessions.append(current_session)
                
                current_session = {
                    'start': sorted_calls[i]['timestamp'],
                    'end': sorted_calls[i]['timestamp'],
                    'calls': 1,
                    'endpoints': {sorted_calls[i]['endpoint']}
                }
            else:
                # Continue session
                current_session['end'] = sorted_calls[i]['timestamp']
                current_session['calls'] += 1
                current_session['endpoints'].add(sorted_calls[i]['endpoint'])
                
        # Add last session
        current_session['endpoints'] = list(current_session['endpoints'])
        sessions.append(current_session)
        
        return sessions
        
    def generate_usage_report(self, period_days: int = 7) -> Dict[str, Any]:
        """Generate comprehensive usage report"""
        conn = sqlite3.connect(str(self.analytics_path / "analytics.db"))
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(days=period_days)).isoformat()
        
        # Total calls
        cursor.execute(
            'SELECT COUNT(*) FROM api_calls WHERE timestamp > ?',
            (since,)
        )
        total_calls = cursor.fetchone()[0]
        
        # Daily breakdown
        cursor.execute('''
            SELECT 
                date(timestamp) as day,
                COUNT(*) as calls,
                AVG(response_time_ms) as avg_response,
                SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as errors
            FROM api_calls
            WHERE timestamp > ?
            GROUP BY day
            ORDER BY day
        ''', (since,))
        
        daily_stats = []
        for row in cursor.fetchall():
            daily_stats.append({
                'date': row[0],
                'calls': row[1],
                'avg_response_time': round(row[2], 2),
                'errors': row[3],
                'error_rate': round((row[3] / row[1] * 100), 2) if row[1] > 0 else 0
            })
            
        # Agent usage
        cursor.execute('''
            SELECT 
                agent,
                COUNT(*) as calls,
                AVG(response_time_ms) as avg_response,
                COUNT(DISTINCT user_id) as unique_users
            FROM api_calls
            WHERE timestamp > ?
            GROUP BY agent
            ORDER BY calls DESC
        ''', (since,))
        
        agent_stats = []
        for row in cursor.fetchall():
            agent_stats.append({
                'agent': row[0],
                'calls': row[1],
                'avg_response_time': round(row[2], 2),
                'unique_users': row[3]
            })
            
        # Top endpoints
        cursor.execute('''
            SELECT 
                endpoint,
                COUNT(*) as calls,
                AVG(response_time_ms) as avg_response
            FROM api_calls
            WHERE timestamp > ?
            GROUP BY endpoint
            ORDER BY calls DESC
            LIMIT 20
        ''', (since,))
        
        top_endpoints = []
        for row in cursor.fetchall():
            top_endpoints.append({
                'endpoint': row[0],
                'calls': row[1],
                'avg_response_time': round(row[2], 2)
            })
            
        # User activity
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT user_id) as total_users,
                AVG(user_calls) as avg_calls_per_user,
                MAX(user_calls) as max_calls_per_user
            FROM (
                SELECT user_id, COUNT(*) as user_calls
                FROM api_calls
                WHERE timestamp > ?
                GROUP BY user_id
            )
        ''', (since,))
        
        user_stats = cursor.fetchone()
        
        # Performance trends
        cursor.execute('''
            SELECT 
                metric_type,
                AVG(value) as avg_value,
                MIN(value) as min_value,
                MAX(value) as max_value
            FROM performance_metrics
            WHERE timestamp > ?
            GROUP BY metric_type
        ''', (since,))
        
        performance_trends = {}
        for row in cursor.fetchall():
            performance_trends[row[0]] = {
                'average': round(row[1], 2),
                'min': round(row[2], 2),
                'max': round(row[3], 2)
            }
            
        conn.close()
        
        return {
            'report_period_days': period_days,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_calls': total_calls,
                'total_users': user_stats[0],
                'avg_calls_per_user': round(user_stats[1], 2) if user_stats[1] else 0,
                'max_calls_per_user': user_stats[2]
            },
            'daily_statistics': daily_stats,
            'agent_usage': agent_stats,
            'top_endpoints': top_endpoints,
            'performance_trends': performance_trends
        }


if __name__ == "__main__":
    # Example usage
    analytics = AnalyticsEngine("/Users/fernandox/Desktop/Core Agent Architecture")
    
    print("Analytics Engine initialized")
    print("Database created at: Analytics_Dashboard/analytics.db")
    print("Logging to: Analytics_Dashboard/analytics.log")
