#!/usr/bin/env python3
"""
API Tracker Middleware for Houston Intelligence Platform (Simplified)
Tracks all API calls and integrates with analytics backend
"""

import time
import json
import sys
import functools
from datetime import datetime
from typing import Dict, Any, Callable, Optional
import traceback
import uuid
from pathlib import Path
import random

# Add path for analytics backend
sys.path.append(str(Path(__file__).parent))
from analytics_backend import AnalyticsEngine


class APITracker:
    """Middleware for tracking API calls"""
    
    def __init__(self, analytics_engine: AnalyticsEngine):
        self.analytics = analytics_engine
        self.enabled = True
        
    def track_call(self, 
                   endpoint: str,
                   method: str = "GET",
                   agent: str = "unknown") -> Callable:
        """Decorator to track API calls"""
        
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enabled:
                    return func(*args, **kwargs)
                    
                # Generate request ID
                request_id = str(uuid.uuid4())[:8]
                
                # Extract user ID from kwargs or use default
                user_id = kwargs.get('user_id', 'anonymous')
                
                # Extract query parameters
                query_params = {
                    k: v for k, v in kwargs.items() 
                    if k not in ['user_id', 'request_body']
                }
                
                # Calculate request size
                request_size = len(json.dumps(kwargs)) if kwargs else 0
                
                # Start timing
                start_time = time.time()
                status_code = 200
                error_msg = None
                response_size = 0
                
                try:
                    # Execute the actual function
                    result = func(*args, **kwargs)
                    
                    # Calculate response size
                    if isinstance(result, dict):
                        response_size = len(json.dumps(result))
                    elif isinstance(result, str):
                        response_size = len(result)
                        
                    return result
                    
                except Exception as e:
                    # Track errors
                    status_code = 500
                    error_msg = str(e)
                    
                    # Log full traceback
                    self.analytics.logger.error(
                        f"API Error in {endpoint}: {traceback.format_exc()}"
                    )
                    
                    # Re-raise the exception
                    raise
                    
                finally:
                    # Calculate response time
                    response_time_ms = (time.time() - start_time) * 1000
                    
                    # Track the API call
                    self.analytics.track_api_call(
                        endpoint=endpoint,
                        method=method,
                        agent=agent,
                        response_time_ms=response_time_ms,
                        status_code=status_code,
                        user_id=user_id,
                        query_params=query_params,
                        error=error_msg,
                        request_size=request_size,
                        response_size=response_size
                    )
                    
            return wrapper
        return decorator


def simulate_api_traffic(analytics_engine: AnalyticsEngine, duration_seconds: int = 60):
    """Simulate API traffic for testing"""
    
    # Initialize tracker
    tracker = APITracker(analytics_engine)
    
    # Create tracked endpoint functions
    @tracker.track_call("/api/v1/agents/market/query", "POST", "Market_Intelligence")
    def market_query(query: str, user_id: str = "anonymous"):
        time.sleep(0.1)  # Simulate processing
        return {
            "status": "success",
            "results": [{"title": "Houston Market Forecast", "confidence": 0.85}],
            "query": query
        }
    
    @tracker.track_call("/api/v1/agents/neighborhood/analysis", "GET", "Neighborhood_Intelligence")
    def neighborhood_analysis(area: str, user_id: str = "anonymous"):
        time.sleep(0.05)  # Simulate processing
        if area.lower() == "error":
            raise ValueError("Invalid area specified")
        return {
            "status": "success",
            "area": area,
            "investment_score": 85
        }
    
    @tracker.track_call("/api/v1/agents/financial/roi", "POST", "Financial_Intelligence")
    def calculate_roi(investment: float, property_type: str, user_id: str = "anonymous"):
        time.sleep(0.2)  # Simulate processing
        return {
            "status": "success",
            "projected_roi": 15.5,
            "break_even_months": 36
        }
    
    @tracker.track_call("/api/v1/agents/environmental/risk", "GET", "Environmental_Intelligence")
    def environmental_risk(location: str, user_id: str = "anonymous"):
        time.sleep(0.08)  # Simulate processing
        return {
            "status": "success",
            "flood_risk": "moderate",
            "environmental_score": 7.5
        }
    
    @tracker.track_call("/api/v1/agents/regulatory/zoning", "GET", "Regulatory_Intelligence")
    def zoning_info(address: str, user_id: str = "anonymous"):
        time.sleep(0.06)  # Simulate processing
        return {
            "status": "success",
            "zoning": "MU-1",
            "permitted_uses": ["residential", "commercial"]
        }
    
    @tracker.track_call("/api/v1/agents/technology/innovation", "GET", "Technology_Innovation")
    def innovation_metrics(district: str, user_id: str = "anonymous"):
        time.sleep(0.07)  # Simulate processing
        return {
            "status": "success",
            "innovation_score": 8.8,
            "startup_density": 125
        }
    
    @tracker.track_call("/api/v1/search", "POST", "Master_Intelligence")
    def unified_search(query: str, user_id: str = "anonymous", limit: int = 10):
        time.sleep(0.3)  # Simulate processing
        return {
            "status": "success",
            "total_results": 42,
            "results": [
                {"agent": "Market_Intelligence", "relevance": 0.95},
                {"agent": "Financial_Intelligence", "relevance": 0.87}
            ][:limit]
        }
    
    # Data for simulation
    users = [f"user_{i}" for i in range(1, 21)]
    neighborhoods = ["Houston Heights", "Montrose", "River Oaks", "Midtown", "The Woodlands"]
    districts = ["Ion District", "TMC", "Energy Corridor"]
    
    print(f"Simulating API traffic for {duration_seconds} seconds...")
    start_time = time.time()
    call_count = 0
    
    while time.time() - start_time < duration_seconds:
        # Random user
        user = random.choice(users)
        
        # Random endpoint
        endpoint_choice = random.choices(
            ['market', 'neighborhood', 'financial', 'environmental', 'regulatory', 'technology', 'search'],
            weights=[25, 20, 15, 10, 10, 10, 10],
            k=1
        )[0]
        
        try:
            if endpoint_choice == 'market':
                market_query(
                    query=f"market trends {random.choice(neighborhoods)}",
                    user_id=user
                )
            elif endpoint_choice == 'neighborhood':
                area = "error" if random.random() < 0.05 else random.choice(neighborhoods)
                neighborhood_analysis(area=area, user_id=user)
            elif endpoint_choice == 'financial':
                calculate_roi(
                    investment=random.randint(100000, 1000000),
                    property_type=random.choice(["residential", "commercial", "mixed-use"]),
                    user_id=user
                )
            elif endpoint_choice == 'environmental':
                environmental_risk(
                    location=random.choice(neighborhoods),
                    user_id=user
                )
            elif endpoint_choice == 'regulatory':
                zoning_info(
                    address=f"{random.randint(100, 9999)} Main St",
                    user_id=user
                )
            elif endpoint_choice == 'technology':
                innovation_metrics(
                    district=random.choice(districts),
                    user_id=user
                )
            else:  # search
                unified_search(
                    query=f"development opportunities {random.choice(neighborhoods)}",
                    user_id=user,
                    limit=random.choice([5, 10, 20])
                )
                
            call_count += 1
            
        except Exception as e:
            # Errors are tracked by the decorator
            pass
            
        # Variable traffic rate
        sleep_time = random.uniform(0.1, 0.5)
        time.sleep(sleep_time)
        
    print(f"\nSimulation complete!")
    print(f"Total API calls: {call_count}")
    print(f"Average rate: {call_count/duration_seconds:.1f} calls/second")
    
    # Show current stats
    stats = analytics_engine.get_dashboard_stats()
    print(f"\nDashboard Stats:")
    print(f"  Total calls (24h): {stats['summary']['total_calls_24h']}")
    print(f"  Avg response time: {stats['summary']['avg_response_time_ms']}ms")
    print(f"  Error rate: {stats['summary']['error_rate_percent']}%")
    print(f"  Active users: {stats['summary']['active_users']}")


if __name__ == "__main__":
    # Example usage
    base_path = "/Users/fernandox/Desktop/Core Agent Architecture"
    analytics = AnalyticsEngine(base_path)
    
    # Run simulation
    simulate_api_traffic(analytics, duration_seconds=30)