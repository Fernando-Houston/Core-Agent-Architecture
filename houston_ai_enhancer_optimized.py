#!/usr/bin/env python3
"""
Houston AI Enhancer - Optimized for Railway Deployment
Memory-efficient version with lazy loading and caching
"""

import os
import torch
from transformers import pipeline
import logging
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import gc
from functools import lru_cache
import warnings
warnings.filterwarnings('ignore')

# Set memory-efficient settings
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
torch.set_num_threads(1)

logger = logging.getLogger(__name__)

class OptimizedHoustonAIEnhancer:
    """Memory-optimized AI enhancer for Railway deployment"""
    
    def __init__(self):
        """Initialize with minimal memory footprint"""
        self.device = -1  # CPU only for Railway
        self.models = {}
        self.model_loaded = {}
        
        # Model configurations
        self._model_configs = {
            'sentiment': {
                'model': 'ProsusAI/finbert',
                'task': 'sentiment-analysis',
                'max_length': 512
            }
        }
        
        logger.info("🚀 Optimized Houston AI Enhancer initialized for Railway")
    
    def _load_sentiment_model(self):
        """Load sentiment model only when needed"""
        if 'sentiment' not in self.models:
            try:
                logger.info("Loading FinBERT sentiment model...")
                self.models['sentiment'] = pipeline(
                    'sentiment-analysis',
                    model='ProsusAI/finbert',
                    device=self.device,
                    model_kwargs={'torchscript': True}  # Optimize for inference
                )
                self.model_loaded['sentiment'] = True
                logger.info("✅ Sentiment model loaded")
            except Exception as e:
                logger.error(f"Failed to load sentiment model: {e}")
                self.model_loaded['sentiment'] = False
    
    def _unload_model(self, model_type: str):
        """Unload model to free memory"""
        if model_type in self.models:
            del self.models[model_type]
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    
    @lru_cache(maxsize=100)
    def analyze_market_sentiment(self, text: str) -> Dict[str, Any]:
        """Cached sentiment analysis"""
        try:
            # Load model if needed
            self._load_sentiment_model()
            
            if not self.model_loaded.get('sentiment', False):
                return self._fallback_sentiment(text)
            
            # Truncate for BERT limit
            if len(text) > 500:
                text = text[:500] + "..."
            
            # Analyze
            results = self.models['sentiment'](text)
            result = results[0]
            
            # Map FinBERT labels
            sentiment_map = {
                'positive': 'BULLISH',
                'negative': 'BEARISH', 
                'neutral': 'NEUTRAL'
            }
            
            return {
                'sentiment': sentiment_map.get(result['label'].lower(), result['label']),
                'confidence': round(result['score'], 3),
                'method': 'finbert',
                'cached': False
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return self._fallback_sentiment(text)
    
    def _fallback_sentiment(self, text: str) -> Dict[str, Any]:
        """Simple rule-based sentiment fallback"""
        text_lower = text.lower()
        
        bullish_words = ['growth', 'increase', 'opportunity', 'positive', 'strong', 'surge']
        bearish_words = ['decline', 'decrease', 'risk', 'negative', 'weak', 'fall']
        
        bullish_count = sum(1 for word in bullish_words if word in text_lower)
        bearish_count = sum(1 for word in bearish_words if word in text_lower)
        
        if bullish_count > bearish_count:
            sentiment = 'BULLISH'
            confidence = min(0.6 + (bullish_count * 0.1), 0.9)
        elif bearish_count > bullish_count:
            sentiment = 'BEARISH'
            confidence = min(0.6 + (bearish_count * 0.1), 0.9)
        else:
            sentiment = 'NEUTRAL'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'method': 'rule_based',
            'cached': False
        }
    
    def simple_summarize(self, text: str, max_sentences: int = 3) -> Dict[str, Any]:
        """Simple extractive summarization without loading BART"""
        sentences = text.split('. ')
        
        if len(sentences) <= max_sentences:
            return {
                'summary': text,
                'method': 'too_short',
                'sentence_count': len(sentences)
            }
        
        # Score sentences by keyword importance
        keywords = ['houston', 'development', 'investment', 'market', 'growth', 
                   'opportunity', 'property', 'real estate', 'trend', 'price']
        
        scored_sentences = []
        for sentence in sentences:
            score = sum(1 for keyword in keywords if keyword in sentence.lower())
            scored_sentences.append((score, sentence))
        
        # Sort by score and take top sentences
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        summary_sentences = [sent for _, sent in scored_sentences[:max_sentences]]
        
        return {
            'summary': '. '.join(summary_sentences) + '.',
            'method': 'extractive',
            'sentence_count': len(summary_sentences)
        }
    
    def generate_simple_response(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response using templates instead of loading DialoGPT"""
        query_lower = user_input.lower()
        
        # Detect intent and generate appropriate response
        if any(word in query_lower for word in ['buy', 'purchase', 'invest']):
            areas = ['The Heights', 'Montrose', 'Sugar Land', 'Katy', 'The Woodlands']
            response = f"For buying property in Houston, consider these high-growth areas: {', '.join(areas[:3])}. Each offers unique investment opportunities based on your specific needs."
        
        elif any(word in query_lower for word in ['market', 'trend']):
            response = "Houston's real estate market is showing strong momentum with steady population growth and business-friendly policies. Key growth areas include master-planned communities and areas near major employment centers."
        
        elif any(word in query_lower for word in ['develop', 'build']):
            response = "Houston offers excellent development opportunities with relatively permissive zoning laws. Focus on areas with infrastructure improvements and growing populations for best ROI."
        
        elif 'permit' in query_lower:
            response = "Houston building permits can be obtained through the city's online portal. Processing times vary by project type. Consider engaging a local expediter for complex projects."
        
        else:
            response = f"Regarding your question about '{user_input[:50]}...', I can provide specific Houston real estate insights. Please specify if you're interested in investment, development, or market analysis."
        
        # Add context if provided
        if context and 'location' in context:
            response = f"In {context['location']}: {response}"
        
        return {
            'user_query': user_input,
            'ai_response': response,
            'method': 'template_based',
            'confidence': 0.75
        }
    
    def enhance_with_ai(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance data with available AI features"""
        enhanced = data.copy()
        
        # Add sentiment if text is available
        if 'text' in data or 'content' in data:
            text = data.get('text', data.get('content', ''))
            if text and len(text) > 50:
                enhanced['sentiment_analysis'] = self.analyze_market_sentiment(text)
        
        # Add summary if long text
        if 'report' in data or 'description' in data:
            long_text = data.get('report', data.get('description', ''))
            if long_text and len(long_text.split()) > 100:
                enhanced['summary'] = self.simple_summarize(long_text)
        
        return enhanced
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of AI enhancer"""
        return {
            'optimized_for': 'railway',
            'models_loaded': list(self.model_loaded.keys()),
            'memory_efficient': True,
            'features': {
                'sentiment_analysis': 'available',
                'summarization': 'rule_based',
                'conversational': 'template_based'
            }
        }


# Create singleton instance for Railway
_ai_enhancer_instance = None

def get_ai_enhancer() -> OptimizedHoustonAIEnhancer:
    """Get or create AI enhancer instance"""
    global _ai_enhancer_instance
    if _ai_enhancer_instance is None:
        _ai_enhancer_instance = OptimizedHoustonAIEnhancer()
    return _ai_enhancer_instance


# For backward compatibility
HoustonAIEnhancer = OptimizedHoustonAIEnhancer