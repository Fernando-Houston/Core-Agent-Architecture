#!/usr/bin/env python3
"""
HCAD Property Search via Perplexity AI
Since HCAD doesn't have a public API, we use Perplexity to search public records
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from perplexity_integration import PerplexityClient
import json
import logging

logger = logging.getLogger(__name__)

class HCADPerplexitySearch:
    """Search HCAD property data using Perplexity AI"""
    
    def __init__(self):
        self.client = PerplexityClient()
        
    def search_property(self, address: str) -> Dict:
        """
        Search for property information using Perplexity
        HCAD data is public record and searchable
        """
        # Create specific query for HCAD data
        query = f"""
        HCAD Harris County Appraisal District property information for {address}:
        - Owner name
        - Appraised value
        - Property type
        - Year built
        - Square footage
        - Lot size
        - Tax assessment
        - Last sale date and price
        Search hcad.org public records
        """
        
        logger.info(f"Searching HCAD data for: {address}")
        
        result = self.client.search_houston_data(query, "property_records")
        
        if result['success']:
            # Parse property data from response
            property_data = self._parse_property_data(result['content'], address)
            property_data['citations'] = result.get('citations', [])
            property_data['search_timestamp'] = datetime.now().isoformat()
            return property_data
        else:
            logger.error(f"Failed to search property: {result.get('error')}")
            return {
                "error": "Unable to retrieve property data",
                "address": address
            }
    
    def search_owner_properties(self, owner_name: str) -> List[Dict]:
        """
        Search for all properties owned by a person/entity
        """
        query = f"""
        HCAD Harris County properties owned by {owner_name}:
        - List all properties
        - Addresses
        - Property types
        - Appraised values
        - Account numbers
        Search hcad.org public ownership records Houston Texas
        """
        
        result = self.client.search_houston_data(query, "ownership_search")
        
        if result['success']:
            properties = self._parse_ownership_data(result['content'], owner_name)
            return properties
        else:
            return []
    
    def get_neighborhood_comps(self, address: str, radius_miles: float = 0.5) -> List[Dict]:
        """
        Get comparable properties in the neighborhood
        """
        query = f"""
        HCAD comparable properties near {address} within {radius_miles} miles:
        - Similar properties sold recently
        - Sale prices
        - Square footage
        - Year built
        - Property characteristics
        Search hcad.org and Houston MLS public records
        """
        
        result = self.client.search_houston_data(query, "comparable_properties")
        
        if result['success']:
            comps = self._parse_comp_data(result['content'])
            return comps
        else:
            return []
    
    def get_tax_history(self, address: str) -> Dict:
        """
        Get property tax history
        """
        query = f"""
        HCAD property tax history for {address}:
        - Tax assessments last 5 years
        - Appraised values
        - Exemptions
        - Tax rates
        - Payment status
        Search hcad.org tax records
        """
        
        result = self.client.search_houston_data(query, "tax_history")
        
        if result['success']:
            tax_data = self._parse_tax_data(result['content'])
            return tax_data
        else:
            return {"error": "Unable to retrieve tax history"}
    
    def _parse_property_data(self, content: str, address: str) -> Dict:
        """Parse property information from Perplexity response"""
        import re
        
        property_info = {
            "address": address,
            "owner": None,
            "appraised_value": None,
            "property_type": None,
            "year_built": None,
            "square_footage": None,
            "lot_size": None,
            "last_sale": None,
            "account_number": None,
            "legal_description": None,
            "source": "HCAD via Perplexity AI"
        }
        
        # Extract owner name
        owner_pattern = r'owner[:\s]+([A-Z][A-Z\s&,\.]+?)(?:\n|\.)'
        owner_match = re.search(owner_pattern, content, re.IGNORECASE)
        if owner_match:
            property_info["owner"] = owner_match.group(1).strip()
        
        # Extract appraised value
        value_pattern = r'appraised\s+(?:value|at)[:\s]+\$?([\d,]+)'
        value_match = re.search(value_pattern, content, re.IGNORECASE)
        if value_match:
            property_info["appraised_value"] = int(value_match.group(1).replace(',', ''))
        
        # Extract year built
        year_pattern = r'(?:year\s+built|built\s+in)[:\s]+(\d{4})'
        year_match = re.search(year_pattern, content, re.IGNORECASE)
        if year_match:
            property_info["year_built"] = int(year_match.group(1))
        
        # Extract square footage
        sqft_pattern = r'(\d+[\d,]*)\s*(?:sq\.?\s*ft\.?|square\s+feet)'
        sqft_match = re.search(sqft_pattern, content, re.IGNORECASE)
        if sqft_match:
            property_info["square_footage"] = int(sqft_match.group(1).replace(',', ''))
        
        # Extract property type
        type_pattern = r'property\s+type[:\s]+([^\n\.]+)'
        type_match = re.search(type_pattern, content, re.IGNORECASE)
        if type_match:
            property_info["property_type"] = type_match.group(1).strip()
        
        # Add full response for reference
        property_info["full_response"] = content
        
        return property_info
    
    def _parse_ownership_data(self, content: str, owner_name: str) -> List[Dict]:
        """Parse multiple properties from ownership search"""
        properties = []
        
        # Split by common property separators
        property_blocks = re.split(r'\n\d+\.|Property \d+:|•', content)
        
        for block in property_blocks:
            if len(block.strip()) > 20:  # Skip empty blocks
                prop = self._parse_property_data(block, "")
                if prop.get("address") or any(word in block.lower() for word in ['street', 'drive', 'lane', 'road']):
                    prop["owner"] = owner_name
                    properties.append(prop)
        
        return properties
    
    def _parse_comp_data(self, content: str) -> List[Dict]:
        """Parse comparable properties"""
        comps = []
        
        # Look for property listings in the content
        # This is a simplified parser - enhance based on actual response patterns
        property_blocks = content.split('\n\n')
        
        for block in property_blocks:
            if '$' in block and any(word in block.lower() for word in ['sold', 'sale', 'price']):
                comp = {
                    "description": block.strip(),
                    "source": "HCAD/MLS via Perplexity"
                }
                
                # Extract price
                price_match = re.search(r'\$?([\d,]+)', block)
                if price_match:
                    comp["sale_price"] = int(price_match.group(1).replace(',', ''))
                
                comps.append(comp)
        
        return comps
    
    def _parse_tax_data(self, content: str) -> Dict:
        """Parse tax history data"""
        tax_history = {
            "years": [],
            "current_exemptions": [],
            "tax_rate": None,
            "source": "HCAD via Perplexity"
        }
        
        # Extract years and values
        year_pattern = r'(\d{4})[:\s]+\$?([\d,]+)'
        year_matches = re.findall(year_pattern, content)
        
        for year, value in year_matches:
            tax_history["years"].append({
                "year": int(year),
                "assessed_value": int(value.replace(',', ''))
            })
        
        # Extract exemptions
        if 'homestead' in content.lower():
            tax_history["current_exemptions"].append("Homestead")
        if 'senior' in content.lower() or 'over 65' in content.lower():
            tax_history["current_exemptions"].append("Senior/Over 65")
        
        return tax_history

# Integration with the main system
class HCADDataEnhancer:
    """Enhance property data with HCAD information via Perplexity"""
    
    def __init__(self):
        self.hcad_search = HCADPerplexitySearch()
        self.cache = {}  # Simple in-memory cache
        
    def enhance_permit_with_property_data(self, permit: Dict) -> Dict:
        """
        Enhance a building permit with HCAD property data
        """
        address = permit.get('address', '')
        
        # Check cache first
        if address in self.cache:
            permit['property_data'] = self.cache[address]
            return permit
        
        # Search HCAD data
        property_data = self.hcad_search.search_property(address)
        
        if not property_data.get('error'):
            # Cache the result
            self.cache[address] = property_data
            
            # Enhance permit with property data
            permit['property_data'] = property_data
            permit['owner'] = property_data.get('owner')
            permit['appraised_value'] = property_data.get('appraised_value')
            permit['property_type'] = property_data.get('property_type')
        
        return permit
    
    def find_development_opportunities(self, target_area: str) -> List[Dict]:
        """
        Find development opportunities by analyzing HCAD data
        """
        opportunities = []
        
        # Search for undervalued properties
        query = f"""
        Find development opportunities in {target_area} Houston using HCAD data:
        - Vacant lots
        - Old properties with low improvement value
        - Large lots in areas with new development
        - Properties with tax delinquencies
        - Estate sales or distressed properties
        """
        
        result = self.hcad_search.client.search_houston_data(
            query, 
            "development_opportunities"
        )
        
        if result['success']:
            # Parse opportunities from response
            opps = self._parse_opportunities(result['content'])
            opportunities.extend(opps)
        
        return opportunities
    
    def _parse_opportunities(self, content: str) -> List[Dict]:
        """Parse development opportunities from content"""
        opportunities = []
        
        # Look for opportunity indicators
        if 'vacant' in content.lower():
            opportunities.append({
                "type": "vacant_lot",
                "description": "Vacant lots identified in area",
                "action": "Research zoning and development potential"
            })
        
        if 'tax delinquen' in content.lower():
            opportunities.append({
                "type": "tax_delinquent",
                "description": "Properties with tax issues",
                "action": "Contact owner or monitor for tax sale"
            })
        
        return opportunities

# Example usage and testing
if __name__ == "__main__":
    print("🏢 HCAD Property Search via Perplexity AI")
    print("="*50)
    
    # Initialize searcher
    searcher = HCADPerplexitySearch()
    
    # Test property search
    test_address = "1000 Main St, Houston, TX"
    print(f"\n🔍 Searching for: {test_address}")
    
    property_data = searcher.search_property(test_address)
    
    if not property_data.get('error'):
        print(f"✅ Found property data:")
        print(f"  Owner: {property_data.get('owner', 'N/A')}")
        print(f"  Appraised Value: ${property_data.get('appraised_value', 0):,}")
        print(f"  Year Built: {property_data.get('year_built', 'N/A')}")
        print(f"  Square Footage: {property_data.get('square_footage', 'N/A')}")
    else:
        print(f"❌ Error: {property_data.get('error')}")
    
    # Test owner search
    print(f"\n🔍 Searching properties owned by: DR HORTON")
    owner_properties = searcher.search_owner_properties("DR HORTON")
    print(f"✅ Found {len(owner_properties)} properties")
    
    # Test comparable search
    print(f"\n🔍 Searching for comps near: {test_address}")
    comps = searcher.get_neighborhood_comps(test_address)
    print(f"✅ Found {len(comps)} comparable properties")
    
    print("\n✨ HCAD search via Perplexity complete!")