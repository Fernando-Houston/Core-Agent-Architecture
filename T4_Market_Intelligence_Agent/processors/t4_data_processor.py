"""
T4 Data Processor
Extracts quantitative metrics and market intelligence from markdown reports
"""

import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from T4_Market_Intelligence_Agent.config.t4_config import T4_CONFIG, REPORT_TO_DOMAIN_MAPPING


class T4DataProcessor:
    """Process markdown reports to extract financial metrics and market intelligence"""
    
    def __init__(self):
        self.config = T4_CONFIG
        self.financial_patterns = self.config["financial_patterns"]
        self.processed_reports = set()
        
    def process_markdown_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract intelligence from a markdown report"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate unique ID for this intelligence
            intelligence_id = self._generate_intelligence_id(file_path)
            
            # Determine report category
            report_category = self._determine_report_category(file_path)
            
            # Extract various types of data
            financial_metrics = self._extract_financial_metrics(content)
            market_data = self._extract_market_data(content)
            investment_opportunities = self._identify_opportunities(content)
            risk_factors = self._extract_risk_factors(content)
            demographic_data = self._extract_demographic_trends(content)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(
                financial_metrics, market_data, investment_opportunities
            )
            
            # Structure the output
            processed_data = {
                "intelligence_id": intelligence_id,
                "source_file": str(file_path),
                "report_category": report_category,
                "report_sources": [file_path.stem],
                "market_metrics": {
                    "financial_indicators": financial_metrics,
                    "investment_opportunities": investment_opportunities,
                    "market_forecasts": market_data.get("forecasts", {}),
                    "risk_factors": risk_factors
                },
                "quantitative_data": {
                    "cap_rates": financial_metrics.get("cap_rates", {}),
                    "roi_projections": financial_metrics.get("roi", {}),
                    "cost_estimates": financial_metrics.get("construction_costs", {}),
                    "demographic_trends": demographic_data
                },
                "actionable_insights": self._generate_insights(
                    financial_metrics, market_data, investment_opportunities
                ),
                "confidence_score": confidence_score,
                "data_vintage": "2024-2025",
                "timestamp": datetime.now().isoformat(),
                "processing_metadata": {
                    "processor": "T4-Data-Processor",
                    "version": self.config["version"],
                    "extraction_patterns_used": list(self.financial_patterns.keys())
                }
            }
            
            return processed_data
            
        except Exception as e:
            return {
                "error": f"Failed to process {file_path}: {str(e)}",
                "file": str(file_path),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_intelligence_id(self, file_path: Path) -> str:
        """Generate unique ID for intelligence report"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_hash = hashlib.md5(str(file_path).encode()).hexdigest()[:5]
        return f"t4-{date_str}-{file_hash}"
    
    def _determine_report_category(self, file_path: Path) -> str:
        """Determine which category the report belongs to"""
        file_name = file_path.stem.lower()
        
        for category in self.config["data_sources"]["report_categories"]:
            if category.lower().replace(" ", "-") in file_name:
                return category
        
        # Try to match based on parent directory
        parent_dir = file_path.parent.name.lower()
        for category in self.config["data_sources"]["report_categories"]:
            if category.lower().replace(" ", "-") in parent_dir:
                return category
                
        return "General Market Intelligence"
    
    def _extract_financial_metrics(self, content: str) -> Dict[str, Any]:
        """Extract financial metrics using regex patterns"""
        metrics = {}
        
        # Extract cap rates
        cap_rates = []
        for match in re.finditer(self.financial_patterns["cap_rate"], content, re.IGNORECASE):
            rate = float(match.group(1))
            # Find context around the match
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end].strip()
            cap_rates.append({
                "rate": rate,
                "context": context
            })
        if cap_rates:
            metrics["cap_rates"] = cap_rates
        
        # Extract ROI figures
        roi_data = []
        for match in re.finditer(self.financial_patterns["roi"], content, re.IGNORECASE):
            roi = float(match.group(1))
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end].strip()
            roi_data.append({
                "roi_percentage": roi,
                "context": context
            })
        if roi_data:
            metrics["roi"] = roi_data
        
        # Extract construction costs
        construction_costs = []
        for match in re.finditer(self.financial_patterns["construction_cost"], content, re.IGNORECASE):
            amount = float(match.group(1))
            # Check if million or billion
            if "billion" in match.group(0).lower() or "B" in match.group(0):
                amount *= 1000  # Convert to millions
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end].strip()
            construction_costs.append({
                "amount_millions": amount,
                "context": context
            })
        if construction_costs:
            metrics["construction_costs"] = construction_costs
        
        # Extract SOFR + spread rates
        loan_rates = []
        for match in re.finditer(self.financial_patterns["loan_rate"], content, re.IGNORECASE):
            spread = float(match.group(1))
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end].strip()
            loan_rates.append({
                "sofr_spread": spread,
                "context": context
            })
        if loan_rates:
            metrics["loan_rates"] = loan_rates
        
        return metrics
    
    def _extract_market_data(self, content: str) -> Dict[str, Any]:
        """Extract market trends and forecasts"""
        market_data = {"forecasts": {}}
        
        # Look for supply/demand metrics
        supply_pattern = r"(\d+,?\d*)\s*(?:units?|sf|square feet)\s*(?:of\s+)?(?:new\s+)?supply"
        for match in re.finditer(supply_pattern, content, re.IGNORECASE):
            amount = match.group(1).replace(",", "")
            market_data["new_supply"] = int(amount)
        
        # Look for absorption rates
        absorption_pattern = r"(\d+\.?\d*)\s*%?\s*absorption"
        for match in re.finditer(absorption_pattern, content, re.IGNORECASE):
            rate = float(match.group(1))
            market_data["absorption_rate"] = rate
        
        # Look for vacancy rates
        vacancy_pattern = r"(\d+\.?\d*)\s*%?\s*vacanc"
        for match in re.finditer(vacancy_pattern, content, re.IGNORECASE):
            rate = float(match.group(1))
            market_data["vacancy_rate"] = rate
        
        # Extract year-over-year growth
        yoy_pattern = r"(\d+\.?\d*)\s*%?\s*(?:year-over-year|yoy|y/y)"
        for match in re.finditer(yoy_pattern, content, re.IGNORECASE):
            growth = float(match.group(1))
            market_data["yoy_growth"] = growth
        
        # Look for market forecasts
        forecast_patterns = [
            r"forecast.*?(\d{4}).*?(\d+\.?\d*)\s*%",
            r"project.*?(\d{4}).*?(\d+\.?\d*)\s*%",
            r"expect.*?(\d{4}).*?(\d+\.?\d*)\s*%"
        ]
        
        for pattern in forecast_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                year = match.group(1)
                value = float(match.group(2))
                if "forecasts" not in market_data:
                    market_data["forecasts"] = {}
                market_data["forecasts"][year] = value
        
        return market_data
    
    def _identify_opportunities(self, content: str) -> List[Dict[str, Any]]:
        """Identify investment opportunities from the content"""
        opportunities = []
        
        # Opportunity keywords
        opportunity_keywords = [
            "opportunity", "undervalued", "emerging", "growth potential",
            "high return", "attractive investment", "favorable", "upside"
        ]
        
        # Find sentences containing opportunity keywords
        sentences = content.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for keyword in opportunity_keywords:
                if keyword in sentence_lower:
                    # Extract any numbers in the sentence
                    numbers = re.findall(r'\d+\.?\d*', sentence)
                    opportunities.append({
                        "description": sentence.strip(),
                        "keyword": keyword,
                        "quantitative_metrics": numbers
                    })
                    break
        
        # Look for specific opportunity zones
        oz_pattern = r"opportunity zone[s]?.*?(\w+(?:\s+\w+)*)"
        for match in re.finditer(oz_pattern, content, re.IGNORECASE):
            location = match.group(1)
            opportunities.append({
                "type": "opportunity_zone",
                "location": location,
                "description": match.group(0)
            })
        
        return opportunities[:10]  # Limit to top 10 opportunities
    
    def _extract_risk_factors(self, content: str) -> List[Dict[str, str]]:
        """Extract risk factors mentioned in the report"""
        risk_factors = []
        
        risk_keywords = [
            "risk", "challenge", "concern", "threat", "headwind",
            "uncertainty", "volatility", "exposure"
        ]
        
        sentences = content.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for keyword in risk_keywords:
                if keyword in sentence_lower:
                    risk_factors.append({
                        "type": keyword,
                        "description": sentence.strip()
                    })
                    break
        
        # Deduplicate similar risks
        unique_risks = []
        seen_descriptions = set()
        for risk in risk_factors:
            desc_lower = risk["description"].lower()
            if desc_lower not in seen_descriptions:
                seen_descriptions.add(desc_lower)
                unique_risks.append(risk)
        
        return unique_risks[:10]  # Limit to top 10 risks
    
    def _extract_demographic_trends(self, content: str) -> Dict[str, Any]:
        """Extract demographic and population trends"""
        demographics = {}
        
        # Population growth
        pop_pattern = r"population.*?(\d+\.?\d*)\s*%?\s*(?:growth|increase)"
        for match in re.finditer(pop_pattern, content, re.IGNORECASE):
            growth = float(match.group(1))
            demographics["population_growth"] = growth
        
        # Age demographics
        age_patterns = [
            r"millennials?.*?(\d+\.?\d*)\s*%",
            r"gen\s*z.*?(\d+\.?\d*)\s*%",
            r"baby\s*boomers?.*?(\d+\.?\d*)\s*%"
        ]
        
        for i, pattern in enumerate(age_patterns):
            generation = ["millennials", "gen_z", "baby_boomers"][i]
            for match in re.finditer(pattern, content, re.IGNORECASE):
                percentage = float(match.group(1))
                if "age_distribution" not in demographics:
                    demographics["age_distribution"] = {}
                demographics["age_distribution"][generation] = percentage
        
        # Income levels
        income_pattern = r"(?:median|average)\s*(?:household\s*)?income.*?\$(\d+,?\d*)"
        for match in re.finditer(income_pattern, content, re.IGNORECASE):
            income = int(match.group(1).replace(",", ""))
            demographics["median_income"] = income
        
        # Employment
        employment_pattern = r"(?:unemployment|employment).*?(\d+\.?\d*)\s*%"
        for match in re.finditer(employment_pattern, content, re.IGNORECASE):
            rate = float(match.group(1))
            if "unemployment" in match.group(0).lower():
                demographics["unemployment_rate"] = rate
            else:
                demographics["employment_rate"] = rate
        
        return demographics
    
    def _generate_insights(self, financial_metrics: Dict, market_data: Dict, 
                          opportunities: List) -> List[str]:
        """Generate actionable insights from extracted data"""
        insights = []
        
        # Cap rate insights
        if "cap_rates" in financial_metrics:
            avg_cap = sum(cr["rate"] for cr in financial_metrics["cap_rates"]) / len(financial_metrics["cap_rates"])
            if avg_cap > 7:
                insights.append(f"High cap rates averaging {avg_cap:.1f}% indicate value-add opportunities")
            elif avg_cap < 5:
                insights.append(f"Compressed cap rates at {avg_cap:.1f}% suggest strong institutional demand")
        
        # Construction cost insights
        if "construction_costs" in financial_metrics:
            total_costs = sum(cc["amount_millions"] for cc in financial_metrics["construction_costs"])
            insights.append(f"${total_costs:.0f}M in tracked construction projects indicates robust development pipeline")
        
        # Market dynamics
        if "absorption_rate" in market_data and "vacancy_rate" in market_data:
            if market_data["absorption_rate"] > 90 and market_data["vacancy_rate"] < 5:
                insights.append("Strong absorption with low vacancy creates favorable rent growth conditions")
        
        # Opportunity insights
        if opportunities:
            oz_opps = [o for o in opportunities if o.get("type") == "opportunity_zone"]
            if oz_opps:
                insights.append(f"{len(oz_opps)} Opportunity Zone locations identified for tax-advantaged investment")
        
        # Loan market insights
        if "loan_rates" in financial_metrics:
            avg_spread = sum(lr["sofr_spread"] for lr in financial_metrics["loan_rates"]) / len(financial_metrics["loan_rates"])
            insights.append(f"Construction loans pricing at SOFR+{avg_spread:.0f}bps reflects current lending environment")
        
        return insights[:5]  # Return top 5 insights
    
    def _calculate_confidence(self, financial_metrics: Dict, market_data: Dict, 
                            opportunities: List) -> float:
        """Calculate confidence score based on data quality and quantity"""
        score_components = []
        
        # Financial metrics completeness
        financial_keys = ["cap_rates", "roi", "construction_costs", "loan_rates"]
        financial_score = sum(1 for key in financial_keys if key in financial_metrics) / len(financial_keys)
        score_components.append(financial_score)
        
        # Market data completeness
        market_keys = ["absorption_rate", "vacancy_rate", "yoy_growth", "forecasts"]
        market_score = sum(1 for key in market_keys if key in market_data) / len(market_keys)
        score_components.append(market_score)
        
        # Opportunities identified
        opp_score = min(len(opportunities) / 5, 1.0)  # Max score at 5 opportunities
        score_components.append(opp_score)
        
        # Calculate weighted average
        if score_components:
            base_score = sum(score_components) / len(score_components)
            # Boost for 2024-2025 data vintage
            confidence = min(base_score * 1.1, 0.99)
            return round(confidence, 2)
        
        return 0.85  # Default confidence
    
    def process_directory(self, directory_path: Path) -> List[Dict[str, Any]]:
        """Process all markdown files in a directory"""
        results = []
        
        markdown_files = []
        for ext in self.config["processing"]["markdown_extensions"]:
            markdown_files.extend(directory_path.rglob(f"*{ext}"))
        
        for file_path in markdown_files:
            if file_path.stat().st_size > self.config["processing"]["max_file_size_mb"] * 1024 * 1024:
                print(f"Skipping large file: {file_path}")
                continue
                
            print(f"Processing: {file_path}")
            result = self.process_markdown_file(file_path)
            results.append(result)
            self.processed_reports.add(str(file_path))
        
        return results