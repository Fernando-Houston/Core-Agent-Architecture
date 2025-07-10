#!/usr/bin/env python3
"""
Houston AI Enhancer - FREE Hugging Face Models Integration
Provides advanced AI capabilities for Houston Development Intelligence Platform
"""

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from transformers import Conversation
import logging
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import hashlib
from functools import lru_cache
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HoustonAIEnhancer:
    """FREE Hugging Face models for Houston development intelligence"""
    
    def __init__(self, use_gpu: bool = False, lazy_load: bool = True):
        """
        Initialize AI enhancer with FREE models
        
        Args:
            use_gpu: Use GPU if available (default: False for Railway compatibility)
            lazy_load: Load models only when needed to save memory
        """
        self.device = 0 if use_gpu and torch.cuda.is_available() else -1
        self.models = {}
        self.lazy_load = lazy_load
        self._model_configs = {
            'sentiment': {
                'model': 'ProsusAI/finbert',
                'task': 'sentiment-analysis',
                'description': 'Financial sentiment analysis for market news'
            },
            'summarizer': {
                'model': 'facebook/bart-large-cnn',
                'task': 'summarization',
                'description': 'Document summarization for reports'
            },
            'conversational': {
                'model': 'microsoft/DialoGPT-medium',
                'task': 'conversational',
                'description': 'Conversational AI for property queries'
            }
        }
        
        if not lazy_load:
            self._load_all_models()
        
        logger.info(f"🤖 Houston AI Enhancer initialized (GPU: {use_gpu and torch.cuda.is_available()}, Lazy Load: {lazy_load})")
    
    def _load_model(self, model_type: str):
        """Load a specific model on demand"""
        if model_type not in self.models and model_type in self._model_configs:
            try:
                config = self._model_configs[model_type]
                logger.info(f"Loading {model_type} model: {config['model']}...")
                
                self.models[model_type] = pipeline(
                    config['task'],
                    model=config['model'],
                    device=self.device
                )
                
                logger.info(f"✅ {model_type} model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load {model_type} model: {str(e)}")
                raise
    
    def _load_all_models(self):
        """Load all models at initialization"""
        for model_type in self._model_configs:
            self._load_model(model_type)
    
    @lru_cache(maxsize=100)
    def analyze_market_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze Houston market sentiment from news/reports using FinBERT
        
        Args:
            text: Market news or report text
            
        Returns:
            Dict with sentiment analysis results
        """
        try:
            # Load model if needed
            if 'sentiment' not in self.models:
                self._load_model('sentiment')
            
            # Truncate text if too long (BERT has 512 token limit)
            if len(text) > 500:
                text = text[:500] + "..."
            
            # Analyze sentiment
            results = self.models['sentiment'](text)
            
            # FinBERT returns: positive, negative, neutral
            sentiment_map = {
                'positive': 'BULLISH',
                'negative': 'BEARISH',
                'neutral': 'NEUTRAL'
            }
            
            result = results[0]
            
            return {
                'sentiment': sentiment_map.get(result['label'].lower(), result['label']),
                'confidence': round(result['score'], 3),
                'raw_label': result['label'],
                'text_preview': text[:100] + "..." if len(text) > 100 else text,
                'analysis_type': 'financial_sentiment',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return {
                'error': str(e),
                'sentiment': 'UNKNOWN',
                'confidence': 0.0
            }
    
    def analyze_batch_sentiment(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze sentiment for multiple texts efficiently"""
        return [self.analyze_market_sentiment(text) for text in texts]
    
    def summarize_report(self, text: str, max_length: int = 150, min_length: int = 30) -> Dict[str, Any]:
        """
        Summarize lengthy Houston development reports using BART
        
        Args:
            text: Long report text
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            Dict with summary and metadata
        """
        try:
            # Load model if needed
            if 'summarizer' not in self.models:
                self._load_model('summarizer')
            
            # Check if text is long enough for summarization
            word_count = len(text.split())
            if word_count < 50:
                return {
                    'summary': text,
                    'method': 'original_too_short',
                    'original_word_count': word_count,
                    'summary_word_count': word_count,
                    'compression_ratio': 1.0,
                    'timestamp': datetime.now().isoformat()
                }
            
            # BART has a max input length, so truncate if needed
            max_input_length = 1024
            if len(text) > max_input_length * 4:  # Rough char to token ratio
                text = text[:max_input_length * 4]
                logger.warning("Text truncated for summarization")
            
            # Generate summary
            result = self.models['summarizer'](
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )
            
            summary = result[0]['summary_text']
            
            return {
                'summary': summary,
                'method': 'bart_large_cnn',
                'original_word_count': word_count,
                'summary_word_count': len(summary.split()),
                'compression_ratio': round(len(summary) / len(text), 3),
                'key_points': self._extract_key_points(summary),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            # Fallback to simple extraction
            sentences = text.split('. ')[:3]
            fallback_summary = '. '.join(sentences) + '.'
            
            return {
                'summary': fallback_summary,
                'method': 'fallback_extraction',
                'error': str(e),
                'original_word_count': len(text.split()),
                'summary_word_count': len(fallback_summary.split())
            }
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text"""
        # Simple extraction - can be enhanced
        sentences = text.split('. ')
        key_points = []
        
        keywords = ['increase', 'decrease', 'growth', 'development', 'investment', 
                   'opportunity', 'risk', 'trend', 'market', 'price']
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                key_points.append(sentence.strip())
        
        return key_points[:5]  # Top 5 key points
    
    def generate_property_response(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate intelligent responses about Houston properties using DialoGPT
        Enhanced with context awareness
        
        Args:
            user_input: User's question
            context: Additional context (location, property type, etc.)
            
        Returns:
            Dict with AI response and metadata
        """
        try:
            # Load model if needed
            if 'conversational' not in self.models:
                self._load_model('conversational')
            
            # Enhance input with Houston context
            enhanced_input = self._enhance_with_context(user_input, context)
            
            # Create conversation
            conversation = Conversation(enhanced_input)
            
            # Generate response
            result = self.models['conversational'](conversation)
            
            # Extract response
            response_text = result.generated_responses[-1] if result.generated_responses else "I can help you with Houston real estate information. Could you please be more specific?"
            
            # Post-process response to ensure Houston relevance
            enhanced_response = self._enhance_response_quality(response_text, user_input, context)
            
            return {
                'user_query': user_input,
                'ai_response': enhanced_response,
                'confidence': 0.85,  # Simplified confidence
                'context_used': context is not None,
                'response_type': 'conversational_ai',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Conversational AI error: {str(e)}")
            # Fallback to template-based response
            return self._generate_fallback_response(user_input, context)
    
    def _enhance_with_context(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Enhance user input with Houston-specific context"""
        enhanced = user_input
        
        if context:
            if 'location' in context:
                enhanced = f"In {context['location']}, Houston: {user_input}"
            elif 'property_type' in context:
                enhanced = f"Regarding {context['property_type']} properties in Houston: {user_input}"
        
        # Add Houston context if not mentioned
        if 'houston' not in user_input.lower():
            enhanced = f"Houston real estate: {enhanced}"
        
        return enhanced
    
    def _enhance_response_quality(self, response: str, query: str, context: Dict[str, Any] = None) -> str:
        """Enhance AI response to be more Houston-specific and helpful"""
        # If response is too generic, make it Houston-specific
        if 'houston' not in response.lower():
            response = response.replace('area', 'Houston area')
            response = response.replace('market', 'Houston market')
        
        # Add helpful suffix if response is too short
        if len(response.split()) < 20:
            response += " I can provide more specific information about Houston neighborhoods, market trends, or development opportunities if you'd like."
        
        return response
    
    def _generate_fallback_response(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate fallback response when AI fails"""
        query_lower = user_input.lower()
        
        # Detect query type and generate appropriate response
        if any(word in query_lower for word in ['buy', 'purchase', 'invest']):
            response = "For buying property in Houston, I recommend checking areas like The Heights, Montrose, or Sugar Land. Each offers unique investment opportunities. Would you like specific neighborhood analysis?"
        elif any(word in query_lower for word in ['market', 'trend', 'price']):
            response = "Houston's real estate market shows strong growth in areas like Katy and The Woodlands. The market is influenced by energy sector performance and population growth. What specific area interests you?"
        elif any(word in query_lower for word in ['develop', 'build', 'construct']):
            response = "Houston offers excellent development opportunities with business-friendly regulations. Popular areas for development include the Energy Corridor and East End. What type of development are you considering?"
        else:
            response = "I can help with Houston real estate information including market trends, investment opportunities, neighborhood analysis, and development potential. What specific information would you like?"
        
        return {
            'user_query': user_input,
            'ai_response': response,
            'confidence': 0.7,
            'context_used': context is not None,
            'response_type': 'fallback_template',
            'timestamp': datetime.now().isoformat()
        }
    
    def enhance_knowledge_search(self, query: str, knowledge_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Enhance knowledge base search results with AI understanding
        
        Args:
            query: User's search query
            knowledge_results: Results from knowledge base search
            
        Returns:
            Enhanced results with AI analysis
        """
        if not knowledge_results:
            return {
                'enhanced': False,
                'message': 'No knowledge base results to enhance'
            }
        
        # Analyze sentiment of the query
        query_sentiment = self.analyze_market_sentiment(query)
        
        # Summarize if we have multiple results
        combined_text = '\n'.join([
            f"{r.get('title', '')}: {r.get('summary', r.get('insight', ''))}" 
            for r in knowledge_results[:5]
        ])
        
        if len(combined_text) > 100:
            summary = self.summarize_report(combined_text, max_length=200)
        else:
            summary = {'summary': combined_text}
        
        return {
            'enhanced': True,
            'query_analysis': {
                'sentiment': query_sentiment,
                'intent': self._detect_query_intent(query)
            },
            'ai_summary': summary['summary'],
            'key_insights': self._extract_insights(knowledge_results),
            'confidence_score': self._calculate_confidence(knowledge_results),
            'timestamp': datetime.now().isoformat()
        }
    
    def _detect_query_intent(self, query: str) -> str:
        """Detect the intent behind a query"""
        query_lower = query.lower()
        
        intents = {
            'investment': ['invest', 'buy', 'purchase', 'roi', 'return'],
            'market_analysis': ['market', 'trend', 'price', 'analysis'],
            'development': ['develop', 'build', 'construct', 'zone'],
            'research': ['information', 'data', 'tell me', 'what is'],
            'comparison': ['compare', 'versus', 'better', 'best'],
            'risk': ['risk', 'flood', 'environmental', 'concern']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return 'general_inquiry'
    
    def _extract_insights(self, results: List[Dict[str, Any]]) -> List[str]:
        """Extract key insights from knowledge results"""
        insights = []
        
        for result in results[:5]:
            # Look for insight fields
            if 'insight' in result:
                insights.append(result['insight'])
            elif 'key_finding' in result:
                insights.append(result['key_finding'])
            elif 'summary' in result and len(result['summary']) < 200:
                insights.append(result['summary'])
        
        return insights[:3]  # Top 3 insights
    
    def _calculate_confidence(self, results: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence score"""
        if not results:
            return 0.0
        
        # Average relevance scores if available
        scores = [r.get('relevance_score', 0.5) for r in results[:5]]
        avg_score = sum(scores) / len(scores)
        
        # Boost confidence if we have multiple good results
        if len(results) >= 3 and avg_score > 0.7:
            avg_score = min(avg_score * 1.2, 1.0)
        
        return round(avg_score, 2)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        info = {
            'loaded_models': list(self.models.keys()),
            'available_models': list(self._model_configs.keys()),
            'lazy_load': self.lazy_load,
            'device': 'GPU' if self.device == 0 else 'CPU'
        }
        
        for model_type, config in self._model_configs.items():
            info[f'{model_type}_info'] = {
                'loaded': model_type in self.models,
                'model_name': config['model'],
                'description': config['description']
            }
        
        return info


def test_ai_enhancer():
    """Test the AI enhancer with Houston-specific examples"""
    print("🧪 Testing Houston AI Enhancer...")
    print("="*60)
    
    enhancer = HoustonAIEnhancer(use_gpu=False, lazy_load=True)
    
    # Test 1: Sentiment Analysis
    print("\n1️⃣ Testing Market Sentiment Analysis...")
    market_news = "Houston real estate market sees record growth with new developments in the Energy Corridor bringing massive investment opportunities"
    sentiment = enhancer.analyze_market_sentiment(market_news)
    print(f"Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']})")
    
    # Test 2: Report Summarization  
    print("\n2️⃣ Testing Report Summarization...")
    long_report = """
    The Houston real estate market continues to demonstrate remarkable resilience and growth 
    potential across multiple sectors. In the residential segment, we're seeing unprecedented 
    demand in areas like The Heights and Montrose, with property values increasing by 15-20% 
    year-over-year. The commercial sector, particularly in the Energy Corridor and Downtown 
    districts, is experiencing a renaissance with several mixed-use developments breaking ground. 
    
    Key factors driving this growth include Houston's business-friendly environment, no state 
    income tax, and continued population influx from other major metropolitan areas. The city's 
    diversification beyond energy into healthcare, technology, and aerospace has created a more 
    stable economic foundation. Infrastructure improvements, including the expansion of Metro 
    rail lines and highway upgrades, are making previously overlooked neighborhoods attractive 
    for development.
    
    However, investors should remain cognizant of potential challenges including flood risk 
    in certain areas, the need for careful due diligence on environmental factors, and the 
    importance of understanding local zoning regulations which can vary significantly across 
    Houston's vast geographic area.
    """
    summary = enhancer.summarize_report(long_report)
    print(f"Summary: {summary['summary']}")
    print(f"Compression ratio: {summary['compression_ratio']}")
    
    # Test 3: Conversational AI
    print("\n3️⃣ Testing Conversational AI...")
    response = enhancer.generate_property_response(
        "What are the best areas to invest in Houston?",
        context={'property_type': 'residential'}
    )
    print(f"User: {response['user_query']}")
    print(f"AI: {response['ai_response']}")
    
    # Test 4: Model Info
    print("\n4️⃣ Model Information:")
    info = enhancer.get_model_info()
    print(f"Loaded models: {info['loaded_models']}")
    print(f"Device: {info['device']}")
    
    print("\n✅ Houston AI Enhancer tests completed!")


if __name__ == "__main__":
    test_ai_enhancer()