#!/usr/bin/env python3
"""
Perplexity Response Parsers
Convert Perplexity AI responses into structured data
"""

import re
import json
from typing import Dict, List, Optional
from datetime import datetime

class PerplexityParser:
    """Parse Perplexity responses into structured data"""
    
    @staticmethod
    def parse_permits(content: str) -> List[Dict]:
        """Extract permit information from Perplexity response"""
        permits = []
        
        # Look for permit patterns in the response
        # Example: "123 Main St - $2.5M commercial development"
        permit_pattern = r'(\d+\s+[\w\s]+(?:St|Ave|Rd|Blvd|Dr|Ln|Way))\s*[-–]\s*\$?([\d.,]+)(?:M|K)?\s*(\w+)'
        
        matches = re.findall(permit_pattern, content)
        
        for i, match in enumerate(matches):
            address, value_str, permit_type = match
            
            # Convert value string to number
            value = value_str.replace(',', '')
            if 'M' in content[content.find(value_str):content.find(value_str)+10]:
                value = float(value) * 1000000
            elif 'K' in content[content.find(value_str):content.find(value_str)+10]:
                value = float(value) * 1000
            else:
                value = float(value)
            
            permits.append({
                "permit_number": f"2025-{str(i+1).zfill(6)}",
                "address": address.strip(),
                "type": permit_type.lower(),
                "value": value,
                "issued_date": datetime.now().strftime("%Y-%m-%d"),
                "source": "Perplexity AI",
                "confidence": 0.8
            })
        
        return permits
    
    @staticmethod
    def parse_market_data(content: str) -> Dict:
        """Extract market statistics from Perplexity response"""
        market_data = {
            "median_price": None,
            "inventory": None,
            "days_on_market": None,
            "price_trend": None,
            "key_insights": []
        }
        
        # Extract median price
        price_pattern = r'median\s+(?:home\s+)?price[:\s]+\$?([\d,]+)'
        price_match = re.search(price_pattern, content, re.IGNORECASE)
        if price_match:
            market_data["median_price"] = int(price_match.group(1).replace(',', ''))
        
        # Extract inventory
        inventory_pattern = r'(\d+)\s+(?:homes?|properties)\s+(?:for sale|available|on market)'
        inventory_match = re.search(inventory_pattern, content, re.IGNORECASE)
        if inventory_match:
            market_data["inventory"] = int(inventory_match.group(1))
        
        # Extract days on market
        dom_pattern = r'(\d+)\s+days?\s+on\s+market'
        dom_match = re.search(dom_pattern, content, re.IGNORECASE)
        if dom_match:
            market_data["days_on_market"] = int(dom_match.group(1))
        
        # Determine price trend
        if 'increase' in content.lower() or 'up' in content.lower():
            market_data["price_trend"] = "increasing"
        elif 'decrease' in content.lower() or 'down' in content.lower():
            market_data["price_trend"] = "decreasing"
        else:
            market_data["price_trend"] = "stable"
        
        # Extract key insights (sentences with important info)
        sentences = content.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in ['growth', 'demand', 'inventory', 'trend', 'forecast']):
                market_data["key_insights"].append(sentence.strip())
        
        return market_data
    
    @staticmethod
    def parse_developments(content: str) -> List[Dict]:
        """Extract development project information"""
        developments = []
        
        # Look for development patterns
        # Example: "East River mixed-use project by Hines"
        dev_pattern = r'([A-Z][\w\s]+?)\s+(?:mixed-use|residential|commercial|retail)\s+(?:project|development)(?:\s+by\s+([\w\s]+))?'
        
        matches = re.findall(dev_pattern, content)
        
        for project_name, developer in matches:
            developments.append({
                "name": project_name.strip(),
                "developer": developer.strip() if developer else "Unknown",
                "type": "mixed-use" if "mixed-use" in content else "commercial",
                "status": "announced",
                "source": "Perplexity AI",
                "announcement_date": datetime.now().strftime("%Y-%m-%d")
            })
        
        return developments
    
    @staticmethod
    def parse_investment_opportunities(content: str) -> List[Dict]:
        """Extract investment opportunities"""
        opportunities = []
        
        # Extract areas mentioned with investment potential
        area_pattern = r'([\w\s]+)\s+(?:offers?|shows?|has)\s+(?:strong|high|good)\s+(?:investment|ROI|return)'
        
        matches = re.findall(area_pattern, content, re.IGNORECASE)
        
        for area in matches:
            opportunities.append({
                "location": area.strip(),
                "type": "investment_opportunity",
                "potential": "high",
                "source": "Perplexity AI",
                "identified_date": datetime.now().strftime("%Y-%m-%d")
            })
        
        return opportunities

# Testing functions
if __name__ == "__main__":
    # Test permit parsing
    test_permit_content = """
    Recent permits issued in Houston:
    - 123 Main Street - $2.5M commercial development
    - 456 Westheimer Rd - $1.2M residential project
    - 789 Memorial Drive - $5M mixed-use development
    """
    
    parser = PerplexityParser()
    permits = parser.parse_permits(test_permit_content)
    print("Parsed Permits:", json.dumps(permits, indent=2))
    
    # Test market parsing
    test_market_content = """
    Houston Heights market update: The median home price is $485,000, 
    up 5% from last year. Currently 156 homes for sale with average 
    45 days on market. Demand remains strong with multiple offers common.
    """
    
    market_data = parser.parse_market_data(test_market_content)
    print("\nParsed Market Data:", json.dumps(market_data, indent=2))
