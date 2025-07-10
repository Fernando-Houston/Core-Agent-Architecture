#!/usr/bin/env python3
"""
Master Intelligence Agent with Replicate AI Integration
Uses cloud-based AI models for superior intelligence without local installation
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re
from dataclasses import dataclass
from enum import Enum
from knowledge_base_loader import KnowledgeBaseLoader
from replicate_ai_enhancer import ReplicateAIEnhancer
from perplexity_integration import PerplexityClient
from houston_data_enhanced import HoustonDataAPI
import logging

logger = logging.getLogger(__name__)

class QueryIntent(Enum):
    """Types of queries the master agent can handle"""
    MARKET_ANALYSIS = "market_analysis"
    NEIGHBORHOOD_ASSESSMENT = "neighborhood_assessment"
    INVESTMENT_OPPORTUNITY = "investment_opportunity"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    RISK_ASSESSMENT = "risk_assessment"
    DEVELOPMENT_FEASIBILITY = "development_feasibility"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    PROPERTY_VISUALIZATION = "property_visualization"
    IMAGE_ANALYSIS = "image_analysis"
    COMPREHENSIVE_ANALYSIS = "comprehensive_analysis"

class ReplicateEnhancedMasterAgent:
    """Master Intelligence Agent enhanced with Replicate AI"""
    
    def __init__(self):
        self.base_path = Path(".")
        self.agents_path = self.base_path / "6 Specialized Agents"
        
        # Initialize all components
        self.knowledge_loader = KnowledgeBaseLoader()
        self.replicate_ai = ReplicateAIEnhancer()
        self.perplexity = PerplexityClient()
        self.houston_data = HoustonDataAPI()
        
        # Agent registry
        self.agent_registry = {
            "market_intelligence": self.agents_path / "Market Intelligence Agent",
            "neighborhood_intelligence": self.agents_path / "Neighborhood Intelligence Agent",
            "financial_intelligence": self.agents_path / "Financial Intelligence Agent",
            "environmental_intelligence": self.agents_path / "Environmental Intelligence Agent",
            "regulatory_intelligence": self.agents_path / "Regulatory Intelligence Agent",
            "technology_intelligence": self.agents_path / "Technology & Innovation Intelligence Agent"
        }
        
        # Enhanced intent patterns
        self.intent_patterns = {
            QueryIntent.MARKET_ANALYSIS: [r"market", r"trend", r"analysis", r"growth"],
            QueryIntent.INVESTMENT_OPPORTUNITY: [r"invest", r"buy", r"roi", r"opportunity"],
            QueryIntent.PROPERTY_VISUALIZATION: [r"visualiz", r"render", r"show.*develop", r"what.*look"],
            QueryIntent.IMAGE_ANALYSIS: [r"photo", r"image", r"picture", r"analyze.*property"],
        }
        
        logger.info("🚀 Replicate-Enhanced Master Intelligence Agent initialized")
    
    def analyze_query(self, user_query: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze user query with Replicate AI enhancement
        
        Args:
            user_query: User's question
            image_url: Optional property image to analyze
        """
        start_time = datetime.now()
        
        # Determine query intent
        intent = self._determine_intent(user_query)
        
        # Extract context
        context = self._extract_context(user_query)
        
        # Route to appropriate handler
        if image_url and intent == QueryIntent.IMAGE_ANALYSIS:
            response = self._handle_image_analysis(user_query, image_url)
        elif intent == QueryIntent.PROPERTY_VISUALIZATION:
            response = self._handle_visualization_request(user_query, context)
        elif intent == QueryIntent.INVESTMENT_OPPORTUNITY:
            response = self._handle_investment_analysis(user_query, context)
        else:
            response = self._handle_general_query(user_query, context, intent)
        
        # Add metadata
        response['processing_time'] = (datetime.now() - start_time).total_seconds()
        response['ai_provider'] = 'replicate'
        response['intent'] = intent.value
        
        return response
    
    def _handle_general_query(self, query: str, context: Dict[str, Any], intent: QueryIntent) -> Dict[str, Any]:
        """Handle general market/intelligence queries"""
        
        # Step 1: Search knowledge base
        knowledge_results = self._search_knowledge_bases(query)
        
        # Step 2: Get real-time data
        real_time_data = self._get_real_time_data(query)
        
        # Step 3: Use Replicate AI for sophisticated analysis
        ai_analysis = self.replicate_ai.analyze_market_intelligence(query, context)
        
        # Step 4: Synthesize response
        if ai_analysis['status'] == 'success':
            executive_summary = ai_analysis['response']
            insights = ai_analysis.get('insights', [])
            confidence = ai_analysis.get('confidence', 0.85)
        else:
            # Fallback to knowledge base
            executive_summary = self._generate_fallback_summary(query, knowledge_results)
            insights = self._extract_insights_from_knowledge(knowledge_results)
            confidence = 0.7
        
        return {
            'query': query,
            'executive_summary': executive_summary,
            'key_insights': insights,
            'knowledge_base_results': len(knowledge_results),
            'real_time_data': bool(real_time_data),
            'confidence_score': confidence,
            'sources': self._list_sources(knowledge_results, real_time_data, ai_analysis),
            'ai_cost_estimate': ai_analysis.get('cost_estimate', 0),
            'timestamp': datetime.now().isoformat()
        }
    
    def _handle_investment_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle investment opportunity analysis"""
        
        # Extract property details from query
        property_data = self._extract_property_details(query, context)
        
        # Get market context
        market_data = self._get_market_context(property_data.get('location'))
        
        # Use Replicate AI for investment analysis
        investment_analysis = self.replicate_ai.analyze_investment_opportunity(
            property_data, 
            market_data
        )
        
        # Search for similar investments in knowledge base
        similar_investments = self._search_similar_investments(property_data)
        
        return {
            'query': query,
            'analysis_type': 'investment_opportunity',
            'property_details': property_data,
            'ai_analysis': investment_analysis,
            'recommendation': investment_analysis.get('recommendation', 'NEUTRAL'),
            'metrics': investment_analysis.get('metrics', {}),
            'similar_investments': similar_investments[:3],
            'market_context': market_data,
            'confidence_score': 0.9 if investment_analysis['status'] == 'success' else 0.6,
            'ai_cost_estimate': investment_analysis.get('cost_estimate', 0),
            'timestamp': datetime.now().isoformat()
        }
    
    def _handle_image_analysis(self, query: str, image_url: str) -> Dict[str, Any]:
        """Handle property image analysis"""
        
        # Define questions based on query
        questions = self._generate_image_questions(query)
        
        # Analyze image with BLIP-2
        image_analysis = self.replicate_ai.analyze_property_image(image_url, questions)
        
        # Get relevant knowledge based on image analysis
        if image_analysis['status'] == 'success':
            property_type = image_analysis['analysis'].get('What type of property is this?', '')
            relevant_knowledge = self._search_knowledge_bases(f"{property_type} Houston")
        else:
            relevant_knowledge = []
        
        return {
            'query': query,
            'analysis_type': 'image_analysis',
            'image_url': image_url,
            'ai_analysis': image_analysis,
            'property_insights': image_analysis.get('summary', ''),
            'related_knowledge': relevant_knowledge[:3],
            'confidence_score': 0.9 if image_analysis['status'] == 'success' else 0.5,
            'ai_cost_estimate': image_analysis.get('cost_estimate', 0),
            'timestamp': datetime.now().isoformat()
        }
    
    def _handle_visualization_request(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle development visualization requests"""
        
        # Extract visualization details
        property_data = self._extract_property_details(query, context)
        
        # Generate visualization with Stable Diffusion
        visualization = self.replicate_ai.generate_development_visualization(query, property_data)
        
        # Get relevant development examples
        similar_developments = self._search_knowledge_bases(f"development {property_data.get('location', 'Houston')}")
        
        return {
            'query': query,
            'analysis_type': 'property_visualization',
            'visualization': visualization,
            'property_context': property_data,
            'similar_developments': similar_developments[:3],
            'confidence_score': 0.95 if visualization['status'] == 'success' else 0.5,
            'ai_cost_estimate': visualization.get('cost_estimate', 0),
            'timestamp': datetime.now().isoformat()
        }
    
    def _determine_intent(self, query: str) -> QueryIntent:
        """Determine query intent"""
        query_lower = query.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        # Default intents based on keywords
        if any(word in query_lower for word in ['invest', 'buy', 'roi', 'return']):
            return QueryIntent.INVESTMENT_OPPORTUNITY
        elif any(word in query_lower for word in ['market', 'trend', 'analysis']):
            return QueryIntent.MARKET_ANALYSIS
        elif any(word in query_lower for word in ['visual', 'render', 'look like']):
            return QueryIntent.PROPERTY_VISUALIZATION
        
        return QueryIntent.COMPREHENSIVE_ANALYSIS
    
    def _extract_context(self, query: str) -> Dict[str, Any]:
        """Extract context from query"""
        context = {}
        
        # Extract location
        locations = ['katy', 'woodlands', 'sugar land', 'heights', 'river oaks', 
                    'midtown', 'downtown', 'energy corridor', 'galleria']
        for location in locations:
            if location in query.lower():
                context['location'] = location.title()
                break
        
        # Extract price/budget
        price_match = re.search(r'\$?([\d,]+)(?:k|K|m|M)?', query)
        if price_match:
            value = price_match.group(1).replace(',', '')
            multiplier = 1
            if 'k' in query.lower()[price_match.end()-1:price_match.end()]:
                multiplier = 1000
            elif 'm' in query.lower()[price_match.end()-1:price_match.end()]:
                multiplier = 1000000
            context['budget'] = int(value) * multiplier
        
        # Extract property type
        property_types = ['residential', 'commercial', 'multifamily', 'land', 'office', 'retail']
        for prop_type in property_types:
            if prop_type in query.lower():
                context['property_type'] = prop_type
                break
        
        return context
    
    def _extract_property_details(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract property details from query and context"""
        details = {
            'query_text': query,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add context
        details.update(context)
        
        # Extract additional details from query
        if 'acre' in query.lower():
            acre_match = re.search(r'(\d+(?:\.\d+)?)\s*acre', query.lower())
            if acre_match:
                details['size'] = f"{acre_match.group(1)} acres"
        
        return details
    
    def _search_knowledge_bases(self, query: str) -> List[Dict[str, Any]]:
        """Search all knowledge bases"""
        all_results = []
        
        for agent_name in self.agent_registry.keys():
            try:
                results = self.knowledge_loader.search_knowledge_fallback(agent_name, query, top_k=3)
                for result in results:
                    result['source_agent'] = agent_name
                    all_results.append(result)
            except Exception as e:
                logger.error(f"Error searching {agent_name}: {str(e)}")
        
        all_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return all_results[:10]
    
    def _search_similar_investments(self, property_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for similar investment opportunities"""
        search_query = f"{property_data.get('property_type', '')} {property_data.get('location', 'Houston')} investment"
        return self._search_knowledge_bases(search_query)
    
    def _get_real_time_data(self, query: str) -> Dict[str, Any]:
        """Get real-time data from APIs"""
        real_time = {}
        
        try:
            # Houston permits if mentioned
            if 'permit' in query.lower():
                permits = self.houston_data.get_building_permits(days_back=7, limit=5)
                if permits:
                    real_time['recent_permits'] = permits
            
            # Perplexity search
            if hasattr(self.perplexity, 'search_houston_real_estate'):
                perplexity_results = self.perplexity.search_houston_real_estate(query)
                if perplexity_results.get('success'):
                    real_time['perplexity'] = perplexity_results
                    
        except Exception as e:
            logger.error(f"Error getting real-time data: {str(e)}")
        
        return real_time
    
    def _get_market_context(self, location: Optional[str]) -> Dict[str, Any]:
        """Get market context for location"""
        market_context = {
            'houston_average_price': 350000,
            'annual_appreciation': 0.05,
            'rental_yield': 0.065
        }
        
        if location:
            # Search for location-specific data
            location_data = self._search_knowledge_bases(f"{location} market data")
            if location_data:
                market_context['location_insights'] = location_data[:2]
        
        return market_context
    
    def _generate_image_questions(self, query: str) -> List[str]:
        """Generate relevant questions for image analysis"""
        base_questions = [
            "What type of property is this?",
            "What is the condition of the property?",
            "What are the key features visible?"
        ]
        
        # Add query-specific questions
        if 'damage' in query.lower() or 'issue' in query.lower():
            base_questions.append("Are there any visible damages or issues?")
        if 'renovate' in query.lower():
            base_questions.append("What renovations might be needed?")
        if 'value' in query.lower():
            base_questions.append("What quality indicators are visible?")
        
        return base_questions
    
    def _generate_fallback_summary(self, query: str, knowledge_results: List[Dict[str, Any]]) -> str:
        """Generate summary when AI is unavailable"""
        if knowledge_results:
            top_result = knowledge_results[0]
            return f"Based on Houston market data: {top_result.get('summary', top_result.get('insight', 'Limited data available'))}"
        return f"I can help with your query about {query}. Please provide more specific details for better analysis."
    
    def _extract_insights_from_knowledge(self, knowledge_results: List[Dict[str, Any]]) -> List[str]:
        """Extract insights from knowledge base results"""
        insights = []
        
        for result in knowledge_results[:5]:
            if 'insight' in result:
                insights.append(f"[{result['source_agent']}] {result['insight']}")
            elif 'title' in result:
                insights.append(f"[{result['source_agent']}] {result['title']}")
        
        return insights
    
    def _list_sources(self, knowledge_results: List[Dict[str, Any]], real_time_data: Dict[str, Any], ai_analysis: Dict[str, Any]) -> List[str]:
        """List all data sources used"""
        sources = set()
        
        # Knowledge base sources
        for result in knowledge_results:
            if 'source_agent' in result:
                sources.add(result['source_agent'].replace('_', ' ').title())
        
        # Real-time sources
        if real_time_data:
            if 'recent_permits' in real_time_data:
                sources.add("Houston Open Data Portal")
            if 'perplexity' in real_time_data:
                sources.add("Perplexity AI Search")
        
        # AI model used
        if ai_analysis and ai_analysis.get('status') == 'success':
            model = ai_analysis.get('model', 'Replicate AI')
            sources.add(f"Replicate AI ({model})")
        
        return list(sources)
    
    def estimate_monthly_costs(self, usage_estimate: Dict[str, int]) -> Dict[str, float]:
        """Estimate monthly AI costs"""
        return self.replicate_ai.estimate_cost(
            list(usage_estimate.keys()) * max(usage_estimate.values())
        )


def test_replicate_master_agent():
    """Test the Replicate-enhanced master agent"""
    print("🧪 Testing Replicate-Enhanced Master Intelligence Agent...")
    print("="*60)
    
    agent = ReplicateEnhancedMasterAgent()
    
    # Test query
    test_query = "What are the best investment opportunities in Houston Heights under $500k?"
    print(f"\nQuery: {test_query}")
    print("-"*60)
    
    # Analyze
    response = agent.analyze_query(test_query)
    
    # Display results
    print(f"\n📊 Executive Summary:")
    print(response.get('executive_summary', 'No summary available')[:300] + "...")
    
    print(f"\n💡 Key Insights:")
    for i, insight in enumerate(response.get('key_insights', [])[:3], 1):
        print(f"{i}. {insight}")
    
    print(f"\n💰 AI Cost: ${response.get('ai_cost_estimate', 0):.4f}")
    print(f"⏱️ Processing Time: {response.get('processing_time', 0):.2f} seconds")
    
    print("\n✅ Replicate-Enhanced Master Agent ready!")


if __name__ == "__main__":
    test_replicate_master_agent()