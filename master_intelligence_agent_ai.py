#!/usr/bin/env python3
"""
AI-Enhanced Master Intelligence Agent
Combines knowledge base with Hugging Face AI models for superior intelligence
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
from houston_ai_enhancer import HoustonAIEnhancer
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
    COMPREHENSIVE_ANALYSIS = "comprehensive_analysis"

class AIEnhancedMasterAgent:
    """Master Intelligence Agent enhanced with Hugging Face AI models"""
    
    def __init__(self):
        self.base_path = Path(".")
        self.agents_path = self.base_path / "6 Specialized Agents"
        
        # Initialize all components
        self.knowledge_loader = KnowledgeBaseLoader()
        self.ai_enhancer = HoustonAIEnhancer(use_gpu=False, lazy_load=True)
        self.perplexity = PerplexityClient()
        self.houston_data = HoustonDataAPI()
        
        # Agent registry (same as before)
        self.agent_registry = {
            "market_intelligence": self.agents_path / "Market Intelligence Agent",
            "neighborhood_intelligence": self.agents_path / "Neighborhood Intelligence Agent",
            "financial_intelligence": self.agents_path / "Financial Intelligence Agent",
            "environmental_intelligence": self.agents_path / "Environmental Intelligence Agent",
            "regulatory_intelligence": self.agents_path / "Regulatory Intelligence Agent",
            "technology_intelligence": self.agents_path / "Technology & Innovation Intelligence Agent"
        }
        
        logger.info("🚀 AI-Enhanced Master Intelligence Agent initialized")
    
    def analyze_query(self, user_query: str) -> Dict[str, Any]:
        """
        Analyze user query with AI enhancement
        """
        start_time = datetime.now()
        
        # Step 1: AI-powered query understanding
        ai_query_analysis = self.ai_enhancer.generate_property_response(
            user_query,
            context={'source': 'master_agent'}
        )
        
        # Step 2: Search knowledge base
        knowledge_results = self._search_all_knowledge_bases(user_query)
        
        # Step 3: Enhance knowledge with AI
        if knowledge_results:
            enhanced_knowledge = self.ai_enhancer.enhance_knowledge_search(
                user_query, 
                knowledge_results
            )
        else:
            enhanced_knowledge = None
        
        # Step 4: Get real-time data
        real_time_data = self._get_real_time_data(user_query)
        
        # Step 5: Analyze market sentiment if relevant
        sentiment_analysis = None
        if any(word in user_query.lower() for word in ['market', 'trend', 'investment', 'growth']):
            sentiment_analysis = self._analyze_market_sentiment(user_query, knowledge_results)
        
        # Step 6: Generate comprehensive response
        response = self._generate_ai_response(
            user_query=user_query,
            ai_analysis=ai_query_analysis,
            knowledge_results=knowledge_results,
            enhanced_knowledge=enhanced_knowledge,
            real_time_data=real_time_data,
            sentiment_analysis=sentiment_analysis
        )
        
        # Add performance metrics
        response['processing_time'] = (datetime.now() - start_time).total_seconds()
        response['ai_enhanced'] = True
        
        return response
    
    def _search_all_knowledge_bases(self, query: str) -> List[Dict[str, Any]]:
        """Search all knowledge bases and compile results"""
        all_results = []
        
        for agent_name in self.agent_registry.keys():
            try:
                # Use the fallback search method that works
                results = self.knowledge_loader.search_knowledge_fallback(agent_name, query, top_k=3)
                for result in results:
                    result['source_agent'] = agent_name
                    all_results.append(result)
            except Exception as e:
                logger.error(f"Error searching {agent_name}: {str(e)}")
        
        # Sort by relevance score
        all_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return all_results[:10]  # Top 10 results
    
    def _get_real_time_data(self, query: str) -> Dict[str, Any]:
        """Get real-time data from Perplexity and Houston APIs"""
        real_time = {}
        
        try:
            # Perplexity search
            if hasattr(self.perplexity, 'search_houston_real_estate'):
                perplexity_results = self.perplexity.search_houston_real_estate(query)
                if perplexity_results.get('success'):
                    real_time['perplexity'] = perplexity_results
            
            # Houston data if permits mentioned
            if 'permit' in query.lower():
                permits = self.houston_data.get_building_permits(days_back=7, limit=5)
                if permits:
                    real_time['recent_permits'] = permits
                    
        except Exception as e:
            logger.error(f"Error getting real-time data: {str(e)}")
        
        return real_time
    
    def _analyze_market_sentiment(self, query: str, knowledge_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze market sentiment from query and results"""
        sentiments = []
        
        # Analyze query sentiment
        query_sentiment = self.ai_enhancer.analyze_market_sentiment(query)
        sentiments.append(query_sentiment)
        
        # Analyze top knowledge results
        for result in knowledge_results[:3]:
            text = result.get('summary', result.get('insight', ''))
            if text and len(text) > 50:
                sentiment = self.ai_enhancer.analyze_market_sentiment(text)
                sentiments.append(sentiment)
        
        # Aggregate sentiments
        if sentiments:
            sentiment_counts = {'BULLISH': 0, 'BEARISH': 0, 'NEUTRAL': 0}
            total_confidence = 0
            
            for s in sentiments:
                if 'sentiment' in s:
                    sentiment_counts[s['sentiment']] = sentiment_counts.get(s['sentiment'], 0) + 1
                    total_confidence += s.get('confidence', 0)
            
            # Determine overall sentiment
            overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)
            avg_confidence = total_confidence / len(sentiments) if sentiments else 0
            
            return {
                'overall_sentiment': overall_sentiment,
                'confidence': round(avg_confidence, 2),
                'sentiment_distribution': sentiment_counts,
                'samples_analyzed': len(sentiments)
            }
        
        return None
    
    def _generate_ai_response(self, **kwargs) -> Dict[str, Any]:
        """Generate comprehensive AI-enhanced response"""
        user_query = kwargs.get('user_query', '')
        ai_analysis = kwargs.get('ai_analysis', {})
        knowledge_results = kwargs.get('knowledge_results', [])
        enhanced_knowledge = kwargs.get('enhanced_knowledge', {})
        real_time_data = kwargs.get('real_time_data', {})
        sentiment_analysis = kwargs.get('sentiment_analysis', {})
        
        # Build executive summary using AI
        summary_parts = []
        
        # Add AI response
        if ai_analysis and 'ai_response' in ai_analysis:
            summary_parts.append(ai_analysis['ai_response'])
        
        # Add enhanced knowledge summary
        if enhanced_knowledge and enhanced_knowledge.get('enhanced'):
            summary_parts.append(enhanced_knowledge.get('ai_summary', ''))
        
        # Combine and summarize if needed
        if len(summary_parts) > 1:
            combined_text = ' '.join(summary_parts)
            if len(combined_text) > 300:
                summary_result = self.ai_enhancer.summarize_report(combined_text, max_length=200)
                executive_summary = summary_result['summary']
            else:
                executive_summary = combined_text
        else:
            executive_summary = summary_parts[0] if summary_parts else "I can help you with Houston real estate intelligence. Please provide more specific details."
        
        # Extract key insights
        key_insights = []
        
        # From enhanced knowledge
        if enhanced_knowledge and 'key_insights' in enhanced_knowledge:
            key_insights.extend(enhanced_knowledge['key_insights'])
        
        # From knowledge results
        for result in knowledge_results[:5]:
            if 'insight' in result:
                key_insights.append(f"[{result['source_agent']}] {result['insight']}")
            elif 'title' in result:
                key_insights.append(f"[{result['source_agent']}] {result['title']}")
        
        # Build data highlights
        data_highlights = []
        
        # From real-time data
        if 'recent_permits' in real_time_data:
            for permit in real_time_data['recent_permits'][:3]:
                data_highlights.append({
                    'type': 'Recent Permit',
                    'value': f"{permit.get('project_name', 'N/A')} - ${permit.get('project_value', 0):,.0f}",
                    'source': 'Houston Open Data'
                })
        
        # From knowledge results
        for result in knowledge_results[:5]:
            if 'metrics' in result:
                for metric, value in list(result['metrics'].items())[:2]:
                    data_highlights.append({
                        'type': metric,
                        'value': str(value),
                        'source': result.get('source_agent', 'Knowledge Base')
                    })
        
        # Build response
        response = {
            'query': user_query,
            'executive_summary': executive_summary,
            'key_insights': key_insights[:10],
            'data_highlights': data_highlights[:10],
            'sentiment_analysis': sentiment_analysis,
            'confidence_score': self._calculate_confidence(knowledge_results, enhanced_knowledge),
            'sources': self._list_sources(knowledge_results, real_time_data),
            'ai_enhancements': {
                'query_understanding': True,
                'sentiment_analysis': sentiment_analysis is not None,
                'summarization': len(summary_parts) > 1,
                'knowledge_enhancement': enhanced_knowledge is not None
            },
            'recommendations': self._generate_recommendations(user_query, knowledge_results, sentiment_analysis),
            'next_steps': self._suggest_next_steps(user_query, knowledge_results),
            'timestamp': datetime.now().isoformat()
        }
        
        return response
    
    def _calculate_confidence(self, knowledge_results: List[Dict], enhanced_knowledge: Dict) -> float:
        """Calculate overall confidence score"""
        scores = []
        
        # Knowledge result scores
        for result in knowledge_results[:5]:
            scores.append(result.get('relevance_score', 0.5))
        
        # Enhanced knowledge confidence
        if enhanced_knowledge and 'confidence_score' in enhanced_knowledge:
            scores.append(enhanced_knowledge['confidence_score'])
        
        # AI analysis confidence (default high for Hugging Face models)
        scores.append(0.85)
        
        return round(sum(scores) / len(scores) if scores else 0.5, 2)
    
    def _list_sources(self, knowledge_results: List[Dict], real_time_data: Dict) -> List[str]:
        """List all data sources used"""
        sources = set()
        
        # Knowledge base sources
        for result in knowledge_results:
            if 'source_agent' in result:
                sources.add(f"{result['source_agent'].replace('_', ' ').title()}")
        
        # Real-time sources
        if 'perplexity' in real_time_data:
            sources.add("Perplexity AI Real-Time Search")
        if 'recent_permits' in real_time_data:
            sources.add("Houston Open Data Portal")
        
        # AI models
        sources.add("FinBERT Financial Sentiment Analysis")
        sources.add("BART Summarization Model")
        sources.add("DialoGPT Conversational AI")
        
        return list(sources)
    
    def _generate_recommendations(self, query: str, knowledge_results: List[Dict], sentiment: Dict) -> List[str]:
        """Generate AI-powered recommendations"""
        recommendations = []
        
        # Based on sentiment
        if sentiment and sentiment.get('overall_sentiment') == 'BULLISH':
            recommendations.append("Market sentiment is positive - consider accelerating investment timelines")
        elif sentiment and sentiment.get('overall_sentiment') == 'BEARISH':
            recommendations.append("Market sentiment suggests caution - focus on thorough due diligence")
        
        # Based on query intent
        query_lower = query.lower()
        if 'invest' in query_lower or 'buy' in query_lower:
            recommendations.append("Review specific property listings in high-growth areas identified")
            recommendations.append("Consult with local real estate professionals for detailed market analysis")
        elif 'develop' in query_lower:
            recommendations.append("Schedule meetings with Houston planning department for specific requirements")
            recommendations.append("Analyze infrastructure plans for your target areas")
        
        # Based on knowledge results
        if len(knowledge_results) > 5:
            recommendations.append("Multiple relevant insights found - consider deep-dive analysis on top opportunities")
        
        return recommendations[:5]
    
    def _suggest_next_steps(self, query: str, knowledge_results: List[Dict]) -> List[str]:
        """Suggest concrete next steps"""
        steps = []
        
        if knowledge_results:
            steps.append("Review detailed reports for properties/areas of interest")
            steps.append("Set up alerts for new opportunities matching your criteria")
            steps.append("Schedule property viewings or site visits")
        else:
            steps.append("Refine your search with specific neighborhoods or property types")
            steps.append("Explore our example queries for better results")
        
        steps.append("Use our AI chat for follow-up questions")
        
        return steps[:4]


def test_ai_master_agent():
    """Test the AI-enhanced master agent"""
    print("🧪 Testing AI-Enhanced Master Intelligence Agent...")
    print("="*60)
    
    agent = AIEnhancedMasterAgent()
    
    # Test query
    test_query = "I am interested in buying land in Houston for development"
    print(f"\nQuery: {test_query}")
    print("-"*60)
    
    # Analyze
    response = agent.analyze_query(test_query)
    
    # Display results
    print(f"\n📊 Executive Summary:")
    print(response['executive_summary'])
    
    print(f"\n💡 Key Insights ({len(response['key_insights'])}):")
    for i, insight in enumerate(response['key_insights'][:3], 1):
        print(f"{i}. {insight}")
    
    if response.get('sentiment_analysis'):
        print(f"\n📈 Market Sentiment: {response['sentiment_analysis']['overall_sentiment']} "
              f"(confidence: {response['sentiment_analysis']['confidence']})")
    
    print(f"\n🎯 Confidence Score: {response['confidence_score']}")
    
    print(f"\n✅ AI Enhancements Used:")
    for feature, used in response['ai_enhancements'].items():
        if used:
            print(f"  - {feature.replace('_', ' ').title()}")
    
    print(f"\n⏱️ Processing Time: {response['processing_time']:.2f} seconds")
    
    print("\n✅ AI-Enhanced Master Agent test completed!")


if __name__ == "__main__":
    test_ai_master_agent()