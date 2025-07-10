#!/usr/bin/env python3
"""
Perplexity AI Integration for Houston Intelligence Platform
Handles real-time data queries and research
"""

import os
import requests
import json
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PerplexityClient:
    """Client for Perplexity AI API integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def search_houston_data(self, query: str, data_type: str) -> Dict:
        """
        Search for Houston real estate data using Perplexity
        
        Args:
            query: Search query
            data_type: Type of data (permits, market, developments, etc.)
        """
        # Construct focused query for Houston real estate
        focused_query = f"Houston Texas real estate {data_type}: {query} (current 2025 data)"
        
        payload = {
            "model": "pplx-70b-online",  # Online model for real-time data
            "messages": [
                {
                    "role": "system",
                    "content": "You are a Houston real estate data analyst. Provide specific, current data with sources."
                },
                {
                    "role": "user",
                    "content": focused_query
                }
            ],
            "temperature": 0.2,  # Lower temperature for factual data
            "return_citations": True  # Get sources
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'content': data['choices'][0]['message']['content'],
                    'citations': data.get('citations', [])
                }
            else:
                logger.error(f"Perplexity API error: {response.status_code}")
                return {
                    'success': False,
                    'error': f"API error: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Perplexity request failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_daily_updates(self) -> Dict:
        """Get daily Houston real estate updates"""
        queries = [
            "new building permits issued Houston today",
            "Houston real estate market news today",
            "new development announcements Houston",
            "Houston zoning changes this week"
        ]
        
        updates = {}
        for query in queries:
            result = self.search_houston_data(query, "daily update")
            if result['success']:
                updates[query] = result['content']
        
        return updates
    
    def research_property(self, address: str) -> Dict:
        """Research specific property information"""
        query = f"property information and history for {address}"
        return self.search_houston_data(query, "property research")
    
    def analyze_market_trends(self, area: str) -> Dict:
        """Analyze market trends for specific area"""
        query = f"{area} real estate market trends, prices, inventory 2025"
        return self.search_houston_data(query, "market analysis")


    def search_houston_real_estate(self, query: str) -> Dict:
        """
        Search Houston real estate data (wrapper for compatibility)
        This method was referenced in master_intelligence_agent.py
        """
        return self.search_houston_data(query, "real estate")

# Integration with daily refresh agent
def integrate_with_refresh_agents():
    """
    Integrate Perplexity API with existing refresh agents
    """
    client = PerplexityClient()
    
    # Example integration code
    daily_updates = client.get_daily_updates()
    
    # Save updates to agent knowledge bases
    for topic, content in daily_updates.items():
        # Process and structure the data
        structured_data = {
            "source": "perplexity_ai",
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "content": content,
            "data_type": "real_time_update"
        }
        
        # Save to appropriate agent folder
        # (Integration with existing agent structure)
        
    return daily_updates

# Example usage
if __name__ == "__main__":
    # Test the integration
    client = PerplexityClient()
    
    # Test market search
    result = client.analyze_market_trends("Houston Heights")
    if result['success']:
        print("Market Analysis:", result['content'][:500] + "...")
    
    # Test property research
    property_result = client.research_property("123 Main St, Houston, TX")
    if property_result['success']:
        print("\nProperty Research:", property_result['content'][:500] + "...")