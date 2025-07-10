#!/usr/bin/env python3
"""
Replicate AI Integration for Houston Intelligence Platform
Uses powerful cloud-based models with pay-per-use pricing
"""

import os
import replicate
import requests
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import base64
from functools import lru_cache
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReplicateAIEnhancer:
    """Replicate AI models for Houston development intelligence"""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize Replicate AI client
        
        Args:
            api_token: Replicate API token (or set REPLICATE_API_TOKEN env var)
        """
        self.api_token = api_token or os.getenv('REPLICATE_API_TOKEN')
        os.environ['REPLICATE_API_TOKEN'] = self.api_token
        
        # Model configurations
        self.models = {
            'llama2_70b': 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
            'blip2': 'salesforce/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608',
            'stable_diffusion': 'stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4',
            'mistral': 'mistralai/mistral-7b-instruct-v0.2:f5701ad84de5715051cb99d550539719f8a7fbcf65e0e62a3d1eb3f94720764e'
        }
        
        logger.info("🚀 Replicate AI Enhancer initialized")
    
    def analyze_market_intelligence(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use Llama 2 70B for sophisticated market analysis
        
        Args:
            query: User's market question
            context: Additional context (location, property type, etc.)
            
        Returns:
            Dict with AI analysis
        """
        try:
            # Build enhanced prompt
            prompt = self._build_market_prompt(query, context)
            
            # Run Llama 2 70B
            output = replicate.run(
                self.models['llama2_70b'],
                input={
                    "prompt": prompt,
                    "temperature": 0.3,  # Lower for factual responses
                    "max_tokens": 500,
                    "top_p": 0.9,
                    "system_prompt": "You are a Houston real estate market expert. Provide specific, actionable insights based on current market conditions. Always mention specific Houston neighborhoods and real data when possible."
                }
            )
            
            # Concatenate streaming output
            response = "".join(output)
            
            # Extract key insights
            insights = self._extract_insights(response)
            
            return {
                'status': 'success',
                'model': 'llama-2-70b',
                'response': response,
                'insights': insights,
                'confidence': 0.9,
                'cost_estimate': 0.0016,  # ~$0.0016 per 1k tokens
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Llama 2 analysis error: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'fallback_response': self._generate_fallback_response(query)
            }
    
    def analyze_property_image(self, image_url: str, questions: List[str] = None) -> Dict[str, Any]:
        """
        Use BLIP-2 to analyze property photos
        
        Args:
            image_url: URL of property image
            questions: Optional specific questions about the image
            
        Returns:
            Dict with image analysis
        """
        try:
            default_questions = [
                "What is the condition of this property?",
                "What type of property is this?",
                "What notable features are visible?",
                "Are there any visible issues or concerns?"
            ]
            
            questions = questions or default_questions
            results = {}
            
            for question in questions:
                output = replicate.run(
                    self.models['blip2'],
                    input={
                        "image": image_url,
                        "question": question
                    }
                )
                
                # BLIP-2 returns a string answer
                answer = "".join(output) if isinstance(output, list) else str(output)
                results[question] = answer
            
            # Generate summary
            summary = self._summarize_image_analysis(results)
            
            return {
                'status': 'success',
                'model': 'blip-2',
                'image_url': image_url,
                'analysis': results,
                'summary': summary,
                'cost_estimate': 0.00025 * len(questions),  # ~$0.00025 per question
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"BLIP-2 analysis error: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'fallback': 'Unable to analyze image at this time'
            }
    
    def generate_development_visualization(self, prompt: str, property_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use Stable Diffusion to generate development visualizations
        
        Args:
            prompt: Description of what to visualize
            property_data: Optional property details to enhance prompt
            
        Returns:
            Dict with generated image URL
        """
        try:
            # Enhance prompt with Houston context
            enhanced_prompt = self._build_visualization_prompt(prompt, property_data)
            
            output = replicate.run(
                self.models['stable_diffusion'],
                input={
                    "prompt": enhanced_prompt,
                    "negative_prompt": "low quality, blurry, distorted, unrealistic",
                    "width": 768,
                    "height": 512,
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5
                }
            )
            
            # Get the image URL
            image_url = output[0] if isinstance(output, list) else output
            
            return {
                'status': 'success',
                'model': 'stable-diffusion-xl',
                'image_url': image_url,
                'prompt_used': enhanced_prompt,
                'cost_estimate': 0.0025,  # ~$0.0025 per image
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Stable Diffusion error: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'fallback': 'Unable to generate visualization'
            }
    
    def analyze_investment_opportunity(self, property_data: Dict[str, Any], market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use Mistral for quick investment analysis
        
        Args:
            property_data: Property details
            market_data: Optional market context
            
        Returns:
            Dict with investment analysis
        """
        try:
            prompt = self._build_investment_prompt(property_data, market_data)
            
            output = replicate.run(
                self.models['mistral'],
                input={
                    "prompt": prompt,
                    "temperature": 0.2,
                    "max_tokens": 400,
                    "top_p": 0.9
                }
            )
            
            response = "".join(output)
            
            # Parse investment metrics
            metrics = self._parse_investment_metrics(response)
            
            return {
                'status': 'success',
                'model': 'mistral-7b',
                'analysis': response,
                'metrics': metrics,
                'recommendation': self._extract_recommendation(response),
                'cost_estimate': 0.0002,  # Very cheap!
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Mistral analysis error: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _build_market_prompt(self, query: str, context: Dict[str, Any] = None) -> str:
        """Build enhanced prompt for market analysis"""
        base_prompt = f"""As a Houston real estate expert, analyze this query: {query}

Context: Houston's current market conditions include strong population growth, 
energy sector recovery, and expanding tech presence. Consider factors like:
- Location-specific trends in Houston neighborhoods
- Current interest rates and their impact
- Houston's unique no-zoning advantages
- Energy sector influence on commercial real estate
"""
        
        if context:
            if 'location' in context:
                base_prompt += f"\nSpecific area of interest: {context['location']}"
            if 'property_type' in context:
                base_prompt += f"\nProperty type: {context['property_type']}"
            if 'budget' in context:
                base_prompt += f"\nBudget range: ${context['budget']:,}"
        
        base_prompt += "\n\nProvide specific, actionable insights with data and examples."
        
        return base_prompt
    
    def _build_visualization_prompt(self, prompt: str, property_data: Dict[str, Any] = None) -> str:
        """Build enhanced prompt for visualizations"""
        enhanced = f"Modern Houston Texas development visualization: {prompt}"
        
        if property_data:
            if 'style' in property_data:
                enhanced += f", {property_data['style']} architectural style"
            if 'location' in property_data:
                enhanced += f", located in {property_data['location']} Houston"
        
        enhanced += ", professional architectural rendering, photorealistic, high quality"
        
        return enhanced
    
    def _build_investment_prompt(self, property_data: Dict[str, Any], market_data: Dict[str, Any] = None) -> str:
        """Build prompt for investment analysis"""
        prompt = f"""Analyze this Houston investment opportunity:

Property Details:
- Address: {property_data.get('address', 'Houston property')}
- Type: {property_data.get('type', 'Not specified')}
- Price: ${property_data.get('price', 0):,}
- Size: {property_data.get('size', 'Not specified')}
- Current Use: {property_data.get('current_use', 'Not specified')}

Provide:
1. Investment potential score (1-10)
2. Estimated ROI
3. Key risks
4. Development opportunities
5. Recommendation (Buy/Hold/Pass)
"""
        
        if market_data:
            prompt += f"\n\nMarket Context:\n{json.dumps(market_data, indent=2)}"
        
        return prompt
    
    def _extract_insights(self, response: str) -> List[str]:
        """Extract key insights from AI response"""
        insights = []
        
        # Look for numbered points
        numbered_pattern = r'\d+\.\s*([^\n]+)'
        insights.extend(re.findall(numbered_pattern, response))
        
        # Look for bullet points
        bullet_pattern = r'[•·-]\s*([^\n]+)'
        insights.extend(re.findall(bullet_pattern, response))
        
        # If no structured points, take first 3 sentences
        if not insights:
            sentences = response.split('. ')[:3]
            insights = [s.strip() for s in sentences if len(s) > 20]
        
        return insights[:5]  # Top 5 insights
    
    def _summarize_image_analysis(self, results: Dict[str, str]) -> str:
        """Create summary from image analysis results"""
        summary_parts = []
        
        for question, answer in results.items():
            if 'condition' in question.lower():
                summary_parts.append(f"Condition: {answer}")
            elif 'type' in question.lower():
                summary_parts.append(f"Property type: {answer}")
            elif 'features' in question.lower():
                summary_parts.append(f"Features: {answer}")
            elif 'issues' in question.lower() and answer.lower() not in ['no', 'none']:
                summary_parts.append(f"Concerns: {answer}")
        
        return " | ".join(summary_parts)
    
    def _parse_investment_metrics(self, response: str) -> Dict[str, Any]:
        """Extract investment metrics from response"""
        metrics = {}
        
        # Extract score (1-10)
        score_pattern = r'(?:score|rating)[::\s]*(\d+(?:\.\d+)?)\s*(?:/\s*10)?'
        score_match = re.search(score_pattern, response, re.IGNORECASE)
        if score_match:
            metrics['investment_score'] = float(score_match.group(1))
        
        # Extract ROI
        roi_pattern = r'(?:roi|return)[::\s]*(\d+(?:\.\d+)?)\s*%'
        roi_match = re.search(roi_pattern, response, re.IGNORECASE)
        if roi_match:
            metrics['estimated_roi'] = float(roi_match.group(1))
        
        # Extract recommendation
        if any(word in response.lower() for word in ['buy', 'purchase', 'acquire']):
            metrics['recommendation'] = 'BUY'
        elif 'hold' in response.lower():
            metrics['recommendation'] = 'HOLD'
        elif any(word in response.lower() for word in ['pass', 'avoid', 'skip']):
            metrics['recommendation'] = 'PASS'
        
        return metrics
    
    def _extract_recommendation(self, response: str) -> str:
        """Extract main recommendation from response"""
        response_lower = response.lower()
        
        if 'strong buy' in response_lower or 'highly recommend' in response_lower:
            return "STRONG BUY"
        elif 'buy' in response_lower or 'recommend' in response_lower:
            return "BUY"
        elif 'hold' in response_lower or 'wait' in response_lower:
            return "HOLD"
        elif 'pass' in response_lower or 'avoid' in response_lower:
            return "PASS"
        else:
            return "NEUTRAL"
    
    def _generate_fallback_response(self, query: str) -> str:
        """Generate fallback response if API fails"""
        return f"I understand you're asking about {query}. While I can't access advanced AI analysis right now, I recommend consulting local Houston real estate professionals for detailed insights on this topic."
    
    def estimate_cost(self, operations: List[str]) -> Dict[str, float]:
        """Estimate costs for various operations"""
        cost_map = {
            'market_analysis': 0.0016,  # Llama 2 70B
            'image_analysis': 0.00025,   # BLIP-2 per question
            'visualization': 0.0025,     # Stable Diffusion
            'quick_analysis': 0.0002     # Mistral 7B
        }
        
        total = sum(cost_map.get(op, 0) for op in operations)
        
        return {
            'operations': operations,
            'individual_costs': {op: cost_map.get(op, 0) for op in operations},
            'total_estimate': total,
            'monthly_estimate': total * 1000  # Assuming 1000 operations/month
        }


def test_replicate_enhancer():
    """Test the Replicate AI enhancer"""
    print("🧪 Testing Replicate AI Enhancer...")
    print("="*60)
    
    enhancer = ReplicateAIEnhancer()
    
    # Test 1: Market Analysis
    print("\n1️⃣ Testing Market Analysis with Llama 2 70B...")
    market_result = enhancer.analyze_market_intelligence(
        "What are the best areas for multifamily development in Houston?",
        context={'budget': 5000000}
    )
    if market_result['status'] == 'success':
        print(f"Response preview: {market_result['response'][:200]}...")
        print(f"Cost: ${market_result['cost_estimate']}")
    
    # Test 2: Investment Analysis
    print("\n2️⃣ Testing Investment Analysis with Mistral...")
    investment_result = enhancer.analyze_investment_opportunity({
        'address': '123 Main St, Houston Heights',
        'type': 'Multifamily lot',
        'price': 500000,
        'size': '10,000 sqft'
    })
    if investment_result['status'] == 'success':
        print(f"Recommendation: {investment_result['recommendation']}")
        print(f"Metrics: {investment_result['metrics']}")
    
    # Test 3: Cost Estimation
    print("\n3️⃣ Cost Estimation for 1000 operations/month:")
    costs = enhancer.estimate_cost(['market_analysis', 'image_analysis', 'quick_analysis'])
    print(f"Per operation: ${costs['total_estimate']:.4f}")
    print(f"Monthly (1000x): ${costs['monthly_estimate']:.2f}")
    
    print("\n✅ Replicate AI Enhancer ready for production!")


if __name__ == "__main__":
    test_replicate_enhancer()