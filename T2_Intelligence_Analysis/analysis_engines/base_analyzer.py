"""
Base Intelligence Analyzer - Foundation for all domain analyzers
"""

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from dataclasses import dataclass, asdict


@dataclass
class AnalysisResult:
    """Structured analysis result"""
    domain: str
    timestamp: str
    confidence_score: float
    key_findings: List[str]
    insights: Dict[str, Any]
    risks: List[Dict[str, Any]]
    opportunities: List[Dict[str, Any]]
    recommendations: List[str]
    metrics: Dict[str, float]
    data_quality_score: float


class BaseIntelligenceAnalyzer(ABC):
    """Base class for all intelligence analyzers"""
    
    def __init__(self, domain: str, config: Dict[str, Any]):
        self.domain = domain
        self.config = config
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup domain-specific logger"""
        logger = logging.getLogger(f"T2.{self.domain}")
        logger.setLevel(logging.INFO)
        return logger
    
    def analyze(self, extracted_data_path: str) -> AnalysisResult:
        """Main analysis pipeline"""
        self.logger.info(f"Starting analysis for {self.domain}")
        
        try:
            # Load extracted data
            data = self._load_extracted_data(extracted_data_path)
            
            # Validate data quality
            quality_score = self._assess_data_quality(data)
            
            # Perform domain-specific analysis
            raw_insights = self._perform_analysis(data)
            
            # Generate insights
            key_findings = self._extract_key_findings(raw_insights)
            risks = self._identify_risks(raw_insights)
            opportunities = self._identify_opportunities(raw_insights)
            recommendations = self._generate_recommendations(raw_insights, risks, opportunities)
            
            # Calculate confidence
            confidence = self._calculate_confidence(quality_score, raw_insights)
            
            # Package results
            result = AnalysisResult(
                domain=self.domain,
                timestamp=datetime.now().isoformat(),
                confidence_score=confidence,
                key_findings=key_findings,
                insights=raw_insights,
                risks=risks,
                opportunities=opportunities,
                recommendations=recommendations,
                metrics=self._extract_metrics(raw_insights),
                data_quality_score=quality_score
            )
            
            self.logger.info(f"Analysis completed with confidence: {confidence:.2f}")
            return result
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise
    
    def _load_extracted_data(self, path: str) -> Dict[str, Any]:
        """Load T1 extracted data"""
        with open(path, 'r') as f:
            return json.load(f)
    
    def _assess_data_quality(self, data: Dict[str, Any]) -> float:
        """Assess quality of extracted data"""
        quality_factors = []
        
        # Check completeness
        if data.get("files_processed", 0) > 0:
            quality_factors.append(1.0)
        
        # Check data volume
        total_data_points = sum(len(v) if isinstance(v, list) else 1 
                               for v in data.get("aggregated_data", {}).values())
        if total_data_points >= self.config.get("min_data_points", 10):
            quality_factors.append(1.0)
        else:
            quality_factors.append(total_data_points / self.config.get("min_data_points", 10))
        
        # Check extraction success rate
        if "extraction_stats" in data:
            success_rate = data["extraction_stats"].get("success_rate", 0)
            quality_factors.append(success_rate)
        
        return np.mean(quality_factors) if quality_factors else 0.0
    
    def _calculate_confidence(self, quality_score: float, insights: Dict[str, Any]) -> float:
        """Calculate overall confidence in analysis"""
        # Base confidence on data quality
        confidence = quality_score * 0.6
        
        # Adjust based on insight consistency
        if insights:
            # Add confidence if multiple indicators align
            confidence += 0.4
        
        return min(confidence, 1.0)
    
    @abstractmethod
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform domain-specific analysis - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _extract_key_findings(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key findings - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _identify_risks(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify domain-specific risks - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _identify_opportunities(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify opportunities - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _generate_recommendations(self, insights: Dict[str, Any], 
                                risks: List[Dict], 
                                opportunities: List[Dict]) -> List[str]:
        """Generate actionable recommendations - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _extract_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics - must be implemented by subclasses"""
        pass
    
    def save_results(self, result: AnalysisResult, output_path: str):
        """Save analysis results"""
        output_file = Path(output_path) / f"{self.domain}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(asdict(result), f, indent=2)
        
        self.logger.info(f"Results saved to {output_file}")
        return str(output_file)