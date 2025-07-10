#!/usr/bin/env python3
"""
API Tracker Middleware for Houston Intelligence Platform
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
        
    def disable(self):
        """Disable tracking temporarily"""
        self.enabled = False
        
    def enable(self):
        """Enable tracking"""
        self.enabled = True


class MockAPIEndpoints:
    """Mock API endpoints for demonstration"""
    
    def __init__(self, tracker: APITracker):
        self.tracker = tracker
        
    def market_query(self, query: str, user_id: str = "anonymous", filters: Dict = None):
        """Market intelligence query endpoint"""
        wrapped = self.tracker.track_call(
            endpoint="/api/v1/agents/market/query",
            method="POST",
            agent="Market_Intelligence"
        )(self._market_query_impl)
        return wrapped(query=query, user_id=user_id, filters=filters)
        
    def _market_query_impl(self, query: str, user_id: str = "anonymous", filters: Dict = None):
        """Market intelligence query implementation"""
        # Simulate processing
        time.sleep(0.1)  # 100ms processing
        
        return {
            "status": "success",
            "results": [
                {
                    "title": "Houston Market Forecast",
                    "insight": "Residential prices expected to increase 3-5%",
                    "confidence": 0.85
                }
            ],
            "query": query
        }
        
    def neighborhood_analysis(self, area: str, user_id: str = "anonymous"):
        """Neighborhood analysis endpoint"""
        # Simulate processing
        time.sleep(0.05)  # 50ms processing
        
        if area.lower() == "error":
            raise ValueError("Invalid area specified")
            
        return {
            "status": "success",
            "area": area,
            "investment_score": 85,
            "growth_rate": 12.5,
            "demographics": {
                "population": 45000,
                "median_income": 95000
            }
        }
        
    @track(endpoint="/api/v1/agents/financial/roi", method="POST", agent="Financial_Intelligence")
    def calculate_roi(self, investment: float, property_type: str, user_id: str = "anonymous"):
        """ROI calculation endpoint"""
        # Simulate complex calculation
        time.sleep(0.2)  # 200ms processing
        
        roi = 15.5  # Simplified calculation
        
        return {
            "status": "success",
            "investment": investment,
            "property_type": property_type,
            "projected_roi": roi,
            "break_even_months": 36
        }
        
    @track(endpoint="/api/v1/agents/environmental/risk", method="GET", agent="Environmental_Intelligence")
    def environmental_risk(self, location: str, user_id: str = "anonymous"):
        """Environmental risk assessment endpoint"""
        # Simulate processing
        time.sleep(0.08)  # 80ms
        
        return {
            "status": "success",
            "location": location,
            "flood_risk": "moderate",
            "air_quality_index": 45,
            "environmental_score": 7.5
        }
        
    @track(endpoint="/api/v1/agents/regulatory/zoning", method="GET", agent="Regulatory_Intelligence")
    def zoning_info(self, address: str, user_id: str = "anonymous"):
        """Zoning information endpoint"""
        # Simulate database lookup
        time.sleep(0.06)  # 60ms
        
        return {
            "status": "success",
            "address": address,
            "zoning": "MU-1",
            "permitted_uses": ["residential", "commercial", "mixed-use"],
            "height_limit": "65 feet"
        }
        
    @track(endpoint="/api/v1/agents/technology/innovation", method="GET", agent="Technology_Innovation")
    def innovation_metrics(self, district: str, user_id: str = "anonymous"):
        """Innovation district metrics endpoint"""
        # Simulate processing
        time.sleep(0.07)  # 70ms
        
        return {
            "status": "success",
            "district": district,
            "startup_density": 125,
            "tech_employment": 15000,
            "innovation_score": 8.8
        }
        
    @track(endpoint="/api/v1/search", method="POST", agent="Master_Intelligence")
    def unified_search(self, query: str, user_id: str = "anonymous", limit: int = 10):
        """Unified search across all agents"""
        # Simulate complex multi-agent search
        time.sleep(0.3)  # 300ms
        
        return {
            "status": "success",
            "query": query,
            "total_results": 42,
            "results": [
                {
                    "agent": "Market_Intelligence",
                    "title": "Market opportunity in Heights",
                    "relevance": 0.95
                },
                {
                    "agent": "Financial_Intelligence",
                    "title": "ROI projections for mixed-use",
                    "relevance": 0.87
                }
            ][:limit]
        }


def simulate_api_traffic(analytics_engine: AnalyticsEngine, duration_seconds: int = 60):
    """Simulate API traffic for testing"""
    import random
    
    # Initialize tracker and endpoints
    tracker = APITracker(analytics_engine)
    api = MockAPIEndpoints(tracker)
    
    # User pool
    users = [f"user_{i}" for i in range(1, 21)]  # 20 users
    
    # Neighborhoods
    neighborhoods = ["Houston Heights", "Montrose", "River Oaks", "Midtown", "The Woodlands"]
    
    # Districts
    districts = ["Ion District", "TMC", "Energy Corridor"]
    
    print(f"Simulating API traffic for {duration_seconds} seconds...")
    start_time = time.time()
    call_count = 0
    
    while time.time() - start_time < duration_seconds:
        # Random user
        user = random.choice(users)
        
        # Random endpoint with weighted probability
        endpoint_choice = random.choices(
            ['market', 'neighborhood', 'financial', 'environmental', 'regulatory', 'technology', 'search'],
            weights=[25, 20, 15, 10, 10, 10, 10],  # Market queries most common
            k=1
        )[0]
        
        try:
            if endpoint_choice == 'market':
                api.market_query(
                    query=f"market trends {random.choice(neighborhoods)}",
                    user_id=user
                )
            elif endpoint_choice == 'neighborhood':
                # Occasionally trigger an error
                area = "error" if random.random() < 0.05 else random.choice(neighborhoods)
                api.neighborhood_analysis(area=area, user_id=user)
            elif endpoint_choice == 'financial':
                api.calculate_roi(
                    investment=random.randint(100000, 1000000),
                    property_type=random.choice(["residential", "commercial", "mixed-use"]),
                    user_id=user
                )
            elif endpoint_choice == 'environmental':
                api.environmental_risk(
                    location=random.choice(neighborhoods),
                    user_id=user
                )
            elif endpoint_choice == 'regulatory':
                api.zoning_info(
                    address=f"{random.randint(100, 9999)} Main St",
                    user_id=user
                )
            elif endpoint_choice == 'technology':
                api.innovation_metrics(
                    district=random.choice(districts),
                    user_id=user
                )
            else:  # search
                api.unified_search(
                    query=f"development opportunities {random.choice(neighborhoods)}",
                    user_id=user,
                    limit=random.choice([5, 10, 20])
                )
                
            call_count += 1
            
        except Exception as e:
            # Errors are tracked by the decorator
            pass
            
        # Variable traffic rate
        sleep_time = random.uniform(0.1, 0.5)  # 2-10 requests per second
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
