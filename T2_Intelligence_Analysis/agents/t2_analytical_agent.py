"""
T2 Analytical Agent - Houston Intelligence Platform
Analyzes and enhances raw data extracted by T1 agents
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
import pandas as pd
from collections import defaultdict
import asyncio
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("T2-Analytical-Agent")


@dataclass
class AnalyticalMetrics:
    """Calculated metrics from raw data"""
    calculated_values: Dict[str, float]
    trends: Dict[str, Dict[str, Any]]
    anomalies: List[Dict[str, Any]]
    correlations: Dict[str, float]


@dataclass
class T2Analysis:
    """T2 Agent analysis output"""
    analysis_id: str
    source_data: List[str]
    metrics: AnalyticalMetrics
    insights: List[str]
    confidence_score: float
    timestamp: str
    processing_time_ms: int


class T2AnalyticalAgent:
    """
    T2 Agent - Analytical Intelligence Layer
    Processes raw data from T1 agents and generates analytical insights
    """
    
    def __init__(self):
        self.agent_id = "t2-analytical-001"
        self.t1_data_path = Path("/Users/fernandox/Desktop/Core Agent Architecture/shared_state/t1_extractions")
        self.t2_output_path = Path("/Users/fernandox/Desktop/Core Agent Architecture/shared_state/t2_analysis")
        self.processed_files = set()
        
        # Analytical thresholds
        self.anomaly_thresholds = {
            "price_change_pct": 50,  # 50% price change
            "permit_spike_multiplier": 3,  # 3x normal volume
            "tax_assessment_deviation": 30,  # 30% from median
            "days_on_market_outlier": 180,  # 180+ days
            "growth_rate_extreme": 25  # 25% YoY
        }
        
        # Ensure output directory exists
        self.t2_output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"T2 Analytical Agent initialized: {self.agent_id}")
    
    async def process_t1_data(self, t1_file_path: Path) -> Optional[T2Analysis]:
        """Process a single T1 extraction file"""
        try:
            # Check if already processed
            if t1_file_path.name in self.processed_files:
                logger.debug(f"Already processed: {t1_file_path.name}")
                return None
            
            # Load T1 data
            with open(t1_file_path, 'r') as f:
                t1_data = json.load(f)
            
            # Validate T1 data source
            if not self._validate_t1_source(t1_data):
                logger.warning(f"Invalid T1 data source: {t1_file_path.name}")
                return None
            
            # Generate analysis based on data type
            domain = t1_data.get("domain", "").lower()
            
            if domain == "permits":
                analysis = await self._analyze_permits(t1_data)
            elif domain == "property":
                analysis = await self._analyze_property(t1_data)
            elif domain == "tax":
                analysis = await self._analyze_tax_data(t1_data)
            elif domain == "market":
                analysis = await self._analyze_market_data(t1_data)
            elif domain == "distressed":
                analysis = await self._analyze_distressed_properties(t1_data)
            else:
                analysis = await self._analyze_generic(t1_data)
            
            # Mark as processed
            self.processed_files.add(t1_file_path.name)
            
            # Save analysis
            if analysis:
                await self._save_analysis(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error processing T1 data {t1_file_path}: {e}")
            return None
    
    def _validate_t1_source(self, t1_data: Dict) -> bool:
        """Validate data comes from authorized T1 agent"""
        source = t1_data.get("source", {})
        agent_id = source.get("agent_id", "")
        
        # Check if source is T1 agent
        if not agent_id.startswith("t1-"):
            return False
        
        # Verify required fields
        required_fields = ["extraction_id", "timestamp", "data", "source"]
        return all(field in t1_data for field in required_fields)
    
    async def _analyze_permits(self, t1_data: Dict) -> T2Analysis:
        """Analyze building permit data"""
        start_time = datetime.now()
        
        data = t1_data.get("data", {})
        permits = data.get("permits", [])
        
        # Calculate metrics
        metrics = self._calculate_permit_metrics(permits)
        
        # Identify trends
        trends = self._identify_permit_trends(permits)
        
        # Detect anomalies
        anomalies = self._detect_permit_anomalies(permits, metrics)
        
        # Generate insights
        insights = self._generate_permit_insights(metrics, trends, anomalies)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(len(permits), len(anomalies))
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return T2Analysis(
            analysis_id=self._generate_analysis_id(),
            source_data=[t1_data.get("extraction_id")],
            metrics=AnalyticalMetrics(
                calculated_values=metrics,
                trends=trends,
                anomalies=anomalies,
                correlations={}
            ),
            insights=insights,
            confidence_score=confidence,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time
        )
    
    def _calculate_permit_metrics(self, permits: List[Dict]) -> Dict[str, float]:
        """Calculate permit-related metrics"""
        if not permits:
            return {}
        
        # Group by type
        permit_types = defaultdict(int)
        permit_values = []
        
        for permit in permits:
            permit_type = permit.get("type", "unknown")
            permit_types[permit_type] += 1
            
            value = permit.get("estimated_value", 0)
            if value:
                permit_values.append(value)
        
        # Calculate metrics
        metrics = {
            "total_permits": len(permits),
            "unique_types": len(permit_types),
            "residential_permits": permit_types.get("residential", 0),
            "commercial_permits": permit_types.get("commercial", 0),
            "renovation_permits": permit_types.get("renovation", 0),
            "new_construction_permits": permit_types.get("new_construction", 0)
        }
        
        if permit_values:
            metrics.update({
                "avg_permit_value": np.mean(permit_values),
                "median_permit_value": np.median(permit_values),
                "total_permit_value": sum(permit_values),
                "max_permit_value": max(permit_values),
                "min_permit_value": min(permit_values)
            })
        
        # Calculate percentages
        total = metrics["total_permits"]
        if total > 0:
            for permit_type, count in permit_types.items():
                metrics[f"{permit_type}_percentage"] = (count / total) * 100
        
        return metrics
    
    def _identify_permit_trends(self, permits: List[Dict]) -> Dict[str, Dict]:
        """Identify trends in permit data"""
        if not permits:
            return {}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(permits)
        
        trends = {}
        
        # Monthly trend
        if 'issue_date' in df.columns:
            df['issue_date'] = pd.to_datetime(df['issue_date'], errors='coerce')
            df['month'] = df['issue_date'].dt.to_period('M')
            
            monthly_counts = df.groupby('month').size()
            if len(monthly_counts) > 1:
                # Calculate month-over-month growth
                mom_growth = monthly_counts.pct_change().mean() * 100
                
                trends['monthly_permit_volume'] = {
                    "direction": "increasing" if mom_growth > 0 else "decreasing",
                    "growth_rate": float(mom_growth),
                    "latest_month_count": int(monthly_counts.iloc[-1]),
                    "previous_month_count": int(monthly_counts.iloc[-2]) if len(monthly_counts) > 1 else 0
                }
        
        # Neighborhood concentration
        if 'neighborhood' in df.columns:
            neighborhood_counts = df['neighborhood'].value_counts()
            top_neighborhoods = neighborhood_counts.head(5)
            
            trends['neighborhood_concentration'] = {
                "top_neighborhoods": top_neighborhoods.to_dict(),
                "concentration_ratio": float(top_neighborhoods.sum() / len(df)) * 100
            }
        
        # Permit type trends
        if 'type' in df.columns:
            type_counts = df['type'].value_counts()
            trends['permit_type_distribution'] = type_counts.to_dict()
        
        return trends
    
    def _detect_permit_anomalies(self, permits: List[Dict], metrics: Dict) -> List[Dict]:
        """Detect anomalies in permit data"""
        anomalies = []
        
        if not permits or not metrics:
            return anomalies
        
        # Check for permit volume spikes
        avg_permits = metrics.get("total_permits", 0) / 30  # Daily average
        if avg_permits > 0:
            # Group by date
            daily_counts = defaultdict(int)
            for permit in permits:
                date = permit.get("issue_date", "").split("T")[0]
                if date:
                    daily_counts[date] += 1
            
            # Find spikes
            for date, count in daily_counts.items():
                if count > avg_permits * self.anomaly_thresholds["permit_spike_multiplier"]:
                    anomalies.append({
                        "type": "permit_volume_spike",
                        "date": date,
                        "count": count,
                        "expected": avg_permits,
                        "deviation_multiplier": count / avg_permits
                    })
        
        # Check for high-value permits
        avg_value = metrics.get("avg_permit_value", 0)
        if avg_value > 0:
            for permit in permits:
                value = permit.get("estimated_value", 0)
                if value > avg_value * 5:  # 5x average
                    anomalies.append({
                        "type": "high_value_permit",
                        "permit_id": permit.get("permit_number"),
                        "value": value,
                        "average_value": avg_value,
                        "deviation_multiplier": value / avg_value
                    })
        
        return anomalies
    
    def _generate_permit_insights(self, metrics: Dict, trends: Dict, anomalies: List) -> List[str]:
        """Generate insights from permit analysis"""
        insights = []
        
        # Volume insights
        total_permits = metrics.get("total_permits", 0)
        if total_permits > 0:
            insights.append(f"Analyzed {total_permits} building permits")
            
            # Type distribution
            residential_pct = metrics.get("residential_percentage", 0)
            commercial_pct = metrics.get("commercial_percentage", 0)
            
            if residential_pct > 70:
                insights.append("Strong residential development focus (>70% of permits)")
            elif commercial_pct > 40:
                insights.append("Significant commercial development activity (>40% of permits)")
        
        # Trend insights
        monthly_trend = trends.get("monthly_permit_volume", {})
        if monthly_trend:
            direction = monthly_trend.get("direction")
            growth_rate = monthly_trend.get("growth_rate", 0)
            
            if abs(growth_rate) > self.anomaly_thresholds["growth_rate_extreme"]:
                insights.append(f"Permit volume {direction} rapidly at {abs(growth_rate):.1f}% month-over-month")
        
        # Neighborhood insights
        neighborhood_data = trends.get("neighborhood_concentration", {})
        if neighborhood_data:
            top_neighborhoods = neighborhood_data.get("top_neighborhoods", {})
            if top_neighborhoods:
                top_area = list(top_neighborhoods.keys())[0]
                insights.append(f"Highest permit concentration in {top_area}")
        
        # Anomaly insights
        if anomalies:
            spike_anomalies = [a for a in anomalies if a["type"] == "permit_volume_spike"]
            if spike_anomalies:
                insights.append(f"Detected {len(spike_anomalies)} unusual permit volume spikes")
        
        # Value insights
        avg_value = metrics.get("avg_permit_value", 0)
        if avg_value > 0:
            insights.append(f"Average permit value: ${avg_value:,.0f}")
            
            total_value = metrics.get("total_permit_value", 0)
            if total_value > 1000000:
                insights.append(f"Total development value: ${total_value/1000000:.1f}M")
        
        return insights
    
    async def _analyze_property(self, t1_data: Dict) -> T2Analysis:
        """Analyze property data"""
        start_time = datetime.now()
        
        data = t1_data.get("data", {})
        properties = data.get("properties", [])
        
        # Calculate property metrics
        metrics = self._calculate_property_metrics(properties)
        
        # Identify market trends
        trends = self._identify_property_trends(properties)
        
        # Detect anomalies
        anomalies = self._detect_property_anomalies(properties, metrics)
        
        # Calculate correlations
        correlations = self._calculate_property_correlations(properties)
        
        # Generate insights
        insights = self._generate_property_insights(metrics, trends, anomalies)
        
        confidence = self._calculate_confidence(len(properties), len(anomalies))
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return T2Analysis(
            analysis_id=self._generate_analysis_id(),
            source_data=[t1_data.get("extraction_id")],
            metrics=AnalyticalMetrics(
                calculated_values=metrics,
                trends=trends,
                anomalies=anomalies,
                correlations=correlations
            ),
            insights=insights,
            confidence_score=confidence,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time
        )
    
    def _calculate_property_metrics(self, properties: List[Dict]) -> Dict[str, float]:
        """Calculate property-related metrics"""
        if not properties:
            return {}
        
        prices = []
        sqft_values = []
        days_on_market = []
        year_built = []
        
        for prop in properties:
            price = prop.get("price", 0)
            if price > 0:
                prices.append(price)
            
            sqft = prop.get("square_feet", 0)
            if sqft > 0:
                sqft_values.append(sqft)
                if price > 0:
                    prop["price_per_sqft"] = price / sqft
            
            dom = prop.get("days_on_market", 0)
            if dom > 0:
                days_on_market.append(dom)
            
            year = prop.get("year_built", 0)
            if year > 1900:
                year_built.append(year)
        
        metrics = {
            "total_properties": len(properties),
            "active_listings": len([p for p in properties if p.get("status") == "active"]),
            "sold_properties": len([p for p in properties if p.get("status") == "sold"])
        }
        
        if prices:
            metrics.update({
                "avg_price": np.mean(prices),
                "median_price": np.median(prices),
                "min_price": min(prices),
                "max_price": max(prices),
                "price_std_dev": np.std(prices)
            })
        
        if sqft_values:
            metrics.update({
                "avg_sqft": np.mean(sqft_values),
                "median_sqft": np.median(sqft_values)
            })
            
            # Price per sqft
            price_per_sqft = [p.get("price_per_sqft", 0) for p in properties if p.get("price_per_sqft", 0) > 0]
            if price_per_sqft:
                metrics["avg_price_per_sqft"] = np.mean(price_per_sqft)
        
        if days_on_market:
            metrics.update({
                "avg_days_on_market": np.mean(days_on_market),
                "median_days_on_market": np.median(days_on_market)
            })
        
        if year_built:
            metrics["avg_property_age"] = datetime.now().year - np.mean(year_built)
        
        return metrics
    
    def _identify_property_trends(self, properties: List[Dict]) -> Dict[str, Dict]:
        """Identify property market trends"""
        if not properties:
            return {}
        
        df = pd.DataFrame(properties)
        trends = {}
        
        # Price trends by neighborhood
        if 'neighborhood' in df.columns and 'price' in df.columns:
            neighborhood_prices = df.groupby('neighborhood')['price'].agg(['mean', 'median', 'count'])
            neighborhood_prices = neighborhood_prices[neighborhood_prices['count'] >= 3]  # Min 3 properties
            
            if not neighborhood_prices.empty:
                trends['neighborhood_pricing'] = {
                    "highest_avg_price": neighborhood_prices['mean'].idxmax(),
                    "lowest_avg_price": neighborhood_prices['mean'].idxmin(),
                    "price_range": float(neighborhood_prices['mean'].max() - neighborhood_prices['mean'].min())
                }
        
        # Market velocity
        if 'days_on_market' in df.columns:
            dom_by_type = df.groupby('property_type')['days_on_market'].mean()
            
            trends['market_velocity'] = {
                "fastest_moving_type": dom_by_type.idxmin() if not dom_by_type.empty else None,
                "slowest_moving_type": dom_by_type.idxmax() if not dom_by_type.empty else None,
                "velocity_by_type": dom_by_type.to_dict()
            }
        
        # Price distribution
        if 'price' in df.columns:
            price_quartiles = df['price'].quantile([0.25, 0.5, 0.75])
            
            trends['price_distribution'] = {
                "q1_price": float(price_quartiles.iloc[0]),
                "median_price": float(price_quartiles.iloc[1]),
                "q3_price": float(price_quartiles.iloc[2]),
                "iqr": float(price_quartiles.iloc[2] - price_quartiles.iloc[0])
            }
        
        return trends
    
    def _detect_property_anomalies(self, properties: List[Dict], metrics: Dict) -> List[Dict]:
        """Detect anomalies in property data"""
        anomalies = []
        
        avg_price = metrics.get("avg_price", 0)
        median_dom = metrics.get("median_days_on_market", 0)
        
        for prop in properties:
            # Price anomalies
            price = prop.get("price", 0)
            if price > 0 and avg_price > 0:
                price_deviation = abs(price - avg_price) / avg_price * 100
                
                if price_deviation > self.anomaly_thresholds["price_change_pct"]:
                    anomalies.append({
                        "type": "price_outlier",
                        "property_id": prop.get("property_id"),
                        "price": price,
                        "avg_price": avg_price,
                        "deviation_pct": price_deviation,
                        "direction": "above" if price > avg_price else "below"
                    })
            
            # Days on market anomalies
            dom = prop.get("days_on_market", 0)
            if dom > self.anomaly_thresholds["days_on_market_outlier"]:
                anomalies.append({
                    "type": "stale_listing",
                    "property_id": prop.get("property_id"),
                    "days_on_market": dom,
                    "median_dom": median_dom,
                    "address": prop.get("address")
                })
            
            # Price per sqft anomalies
            price_per_sqft = prop.get("price_per_sqft", 0)
            avg_ppsf = metrics.get("avg_price_per_sqft", 0)
            
            if price_per_sqft > 0 and avg_ppsf > 0:
                ppsf_deviation = abs(price_per_sqft - avg_ppsf) / avg_ppsf * 100
                
                if ppsf_deviation > 40:  # 40% deviation
                    anomalies.append({
                        "type": "price_per_sqft_outlier",
                        "property_id": prop.get("property_id"),
                        "price_per_sqft": price_per_sqft,
                        "avg_price_per_sqft": avg_ppsf,
                        "deviation_pct": ppsf_deviation
                    })
        
        return anomalies
    
    def _calculate_property_correlations(self, properties: List[Dict]) -> Dict[str, float]:
        """Calculate correlations between property features"""
        if len(properties) < 10:  # Need minimum data points
            return {}
        
        # Create DataFrame for correlation analysis
        data_for_corr = []
        
        for prop in properties:
            if all(prop.get(field) for field in ["price", "square_feet", "bedrooms", "year_built"]):
                data_for_corr.append({
                    "price": prop["price"],
                    "sqft": prop["square_feet"],
                    "bedrooms": prop["bedrooms"],
                    "age": datetime.now().year - prop["year_built"],
                    "price_per_sqft": prop["price"] / prop["square_feet"]
                })
        
        if len(data_for_corr) < 10:
            return {}
        
        df = pd.DataFrame(data_for_corr)
        
        correlations = {
            "price_vs_sqft": float(df['price'].corr(df['sqft'])),
            "price_vs_bedrooms": float(df['price'].corr(df['bedrooms'])),
            "price_vs_age": float(df['price'].corr(df['age'])),
            "sqft_vs_bedrooms": float(df['sqft'].corr(df['bedrooms']))
        }
        
        return correlations
    
    def _generate_property_insights(self, metrics: Dict, trends: Dict, anomalies: List) -> List[str]:
        """Generate property market insights"""
        insights = []
        
        # Market overview
        total_props = metrics.get("total_properties", 0)
        if total_props > 0:
            insights.append(f"Analyzed {total_props} properties in the market")
            
            active = metrics.get("active_listings", 0)
            sold = metrics.get("sold_properties", 0)
            
            if active > 0:
                insights.append(f"{active} active listings ({active/total_props*100:.1f}% of inventory)")
        
        # Pricing insights
        avg_price = metrics.get("avg_price", 0)
        median_price = metrics.get("median_price", 0)
        
        if avg_price > 0 and median_price > 0:
            if avg_price > median_price * 1.1:
                insights.append("Market skewed by high-value properties (mean > median by 10%+)")
            
            insights.append(f"Median property price: ${median_price:,.0f}")
        
        # Market velocity
        avg_dom = metrics.get("avg_days_on_market", 0)
        if avg_dom > 0:
            if avg_dom < 30:
                insights.append(f"Fast-moving market with {avg_dom:.0f} average days on market")
            elif avg_dom > 90:
                insights.append(f"Slow market conditions with {avg_dom:.0f} average days on market")
        
        # Neighborhood trends
        neighborhood_data = trends.get("neighborhood_pricing", {})
        if neighborhood_data:
            highest = neighborhood_data.get("highest_avg_price")
            if highest:
                insights.append(f"{highest} commands highest average prices")
        
        # Anomaly summary
        if anomalies:
            outlier_count = len([a for a in anomalies if "outlier" in a["type"]])
            stale_count = len([a for a in anomalies if a["type"] == "stale_listing"])
            
            if outlier_count > 0:
                insights.append(f"Identified {outlier_count} properties with unusual pricing")
            if stale_count > 0:
                insights.append(f"{stale_count} properties showing extended market time (180+ days)")
        
        return insights
    
    async def _analyze_tax_data(self, t1_data: Dict) -> T2Analysis:
        """Analyze tax assessment data"""
        start_time = datetime.now()
        
        data = t1_data.get("data", {})
        assessments = data.get("assessments", [])
        
        # Calculate tax metrics
        metrics = self._calculate_tax_metrics(assessments)
        
        # Identify assessment patterns
        trends = self._identify_tax_trends(assessments)
        
        # Detect anomalies
        anomalies = self._detect_tax_anomalies(assessments, metrics)
        
        # Generate insights
        insights = self._generate_tax_insights(metrics, trends, anomalies)
        
        confidence = self._calculate_confidence(len(assessments), len(anomalies))
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return T2Analysis(
            analysis_id=self._generate_analysis_id(),
            source_data=[t1_data.get("extraction_id")],
            metrics=AnalyticalMetrics(
                calculated_values=metrics,
                trends=trends,
                anomalies=anomalies,
                correlations={}
            ),
            insights=insights,
            confidence_score=confidence,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time
        )
    
    def _calculate_tax_metrics(self, assessments: List[Dict]) -> Dict[str, float]:
        """Calculate tax assessment metrics"""
        if not assessments:
            return {}
        
        assessed_values = []
        tax_amounts = []
        assessment_ratios = []
        
        for assessment in assessments:
            assessed = assessment.get("assessed_value", 0)
            if assessed > 0:
                assessed_values.append(assessed)
            
            tax = assessment.get("tax_amount", 0)
            if tax > 0:
                tax_amounts.append(tax)
            
            # Calculate assessment ratio if market value available
            market_value = assessment.get("market_value", 0)
            if market_value > 0 and assessed > 0:
                ratio = assessed / market_value
                assessment_ratios.append(ratio)
        
        metrics = {
            "total_assessments": len(assessments),
            "total_tax_revenue": sum(tax_amounts)
        }
        
        if assessed_values:
            metrics.update({
                "avg_assessed_value": np.mean(assessed_values),
                "median_assessed_value": np.median(assessed_values),
                "total_assessed_value": sum(assessed_values)
            })
        
        if tax_amounts:
            metrics.update({
                "avg_tax_amount": np.mean(tax_amounts),
                "median_tax_amount": np.median(tax_amounts)
            })
        
        if assessment_ratios:
            metrics["avg_assessment_ratio"] = np.mean(assessment_ratios)
        
        # Calculate effective tax rate
        if assessed_values and tax_amounts:
            total_assessed = sum(assessed_values)
            total_tax = sum(tax_amounts)
            if total_assessed > 0:
                metrics["effective_tax_rate"] = (total_tax / total_assessed) * 100
        
        return metrics
    
    def _identify_tax_trends(self, assessments: List[Dict]) -> Dict[str, Dict]:
        """Identify tax assessment trends"""
        if not assessments:
            return {}
        
        df = pd.DataFrame(assessments)
        trends = {}
        
        # Year-over-year changes
        if 'year' in df.columns and 'assessed_value' in df.columns:
            yearly_assessments = df.groupby('year')['assessed_value'].agg(['mean', 'sum', 'count'])
            
            if len(yearly_assessments) > 1:
                # Calculate YoY growth
                yoy_growth = yearly_assessments['mean'].pct_change().mean() * 100
                
                trends['assessment_growth'] = {
                    "avg_yoy_growth": float(yoy_growth),
                    "latest_year_avg": float(yearly_assessments['mean'].iloc[-1]),
                    "total_growth": float((yearly_assessments['mean'].iloc[-1] / yearly_assessments['mean'].iloc[0] - 1) * 100)
                }
        
        # Assessment distribution by property type
        if 'property_type' in df.columns:
            type_assessments = df.groupby('property_type')['assessed_value'].mean()
            
            trends['assessment_by_type'] = {
                "highest_assessed_type": type_assessments.idxmax() if not type_assessments.empty else None,
                "assessment_values": type_assessments.to_dict()
            }
        
        # Tax burden analysis
        if 'tax_amount' in df.columns and 'assessed_value' in df.columns:
            df['tax_rate'] = df['tax_amount'] / df['assessed_value'] * 100
            
            trends['tax_burden'] = {
                "avg_tax_rate": float(df['tax_rate'].mean()),
                "median_tax_rate": float(df['tax_rate'].median()),
                "tax_rate_std": float(df['tax_rate'].std())
            }
        
        return trends
    
    def _detect_tax_anomalies(self, assessments: List[Dict], metrics: Dict) -> List[Dict]:
        """Detect anomalies in tax assessment data"""
        anomalies = []
        
        median_assessed = metrics.get("median_assessed_value", 0)
        avg_ratio = metrics.get("avg_assessment_ratio", 0)
        
        for assessment in assessments:
            # Assessment value anomalies
            assessed = assessment.get("assessed_value", 0)
            if assessed > 0 and median_assessed > 0:
                deviation = abs(assessed - median_assessed) / median_assessed * 100
                
                if deviation > self.anomaly_thresholds["tax_assessment_deviation"]:
                    anomalies.append({
                        "type": "assessment_outlier",
                        "property_id": assessment.get("property_id"),
                        "assessed_value": assessed,
                        "median_value": median_assessed,
                        "deviation_pct": deviation
                    })
            
            # Assessment ratio anomalies
            market_value = assessment.get("market_value", 0)
            if market_value > 0 and assessed > 0:
                ratio = assessed / market_value
                
                if avg_ratio > 0:
                    ratio_deviation = abs(ratio - avg_ratio) / avg_ratio * 100
                    
                    if ratio_deviation > 25:  # 25% deviation from average ratio
                        anomalies.append({
                            "type": "assessment_ratio_anomaly",
                            "property_id": assessment.get("property_id"),
                            "assessment_ratio": ratio,
                            "avg_ratio": avg_ratio,
                            "deviation_pct": ratio_deviation
                        })
            
            # Year-over-year anomalies
            yoy_change = assessment.get("yoy_change_pct", 0)
            if abs(yoy_change) > self.anomaly_thresholds["growth_rate_extreme"]:
                anomalies.append({
                    "type": "assessment_spike",
                    "property_id": assessment.get("property_id"),
                    "yoy_change": yoy_change,
                    "direction": "increase" if yoy_change > 0 else "decrease"
                })
        
        return anomalies
    
    def _generate_tax_insights(self, metrics: Dict, trends: Dict, anomalies: List) -> List[str]:
        """Generate tax assessment insights"""
        insights = []
        
        # Overview
        total_assessments = metrics.get("total_assessments", 0)
        if total_assessments > 0:
            insights.append(f"Analyzed {total_assessments} tax assessments")
            
            total_revenue = metrics.get("total_tax_revenue", 0)
            if total_revenue > 0:
                insights.append(f"Total tax revenue: ${total_revenue:,.0f}")
        
        # Assessment trends
        growth_data = trends.get("assessment_growth", {})
        if growth_data:
            yoy_growth = growth_data.get("avg_yoy_growth", 0)
            if abs(yoy_growth) > 5:
                direction = "increasing" if yoy_growth > 0 else "decreasing"
                insights.append(f"Assessments {direction} at {abs(yoy_growth):.1f}% year-over-year")
        
        # Tax rate insights
        effective_rate = metrics.get("effective_tax_rate", 0)
        if effective_rate > 0:
            insights.append(f"Effective tax rate: {effective_rate:.2f}%")
        
        # Assessment ratio
        avg_ratio = metrics.get("avg_assessment_ratio", 0)
        if avg_ratio > 0:
            insights.append(f"Properties assessed at {avg_ratio*100:.1f}% of market value on average")
        
        # Anomaly insights
        if anomalies:
            outlier_count = len([a for a in anomalies if a["type"] == "assessment_outlier"])
            spike_count = len([a for a in anomalies if a["type"] == "assessment_spike"])
            
            if outlier_count > 0:
                insights.append(f"{outlier_count} properties with unusual assessment values")
            if spike_count > 0:
                insights.append(f"{spike_count} properties showing significant assessment changes")
        
        return insights
    
    async def _analyze_market_data(self, t1_data: Dict) -> T2Analysis:
        """Analyze market indicators and trends"""
        start_time = datetime.now()
        
        data = t1_data.get("data", {})
        
        # Extract different market data types
        sales_data = data.get("sales", [])
        inventory_data = data.get("inventory", {})
        price_trends = data.get("price_trends", [])
        
        # Calculate comprehensive market metrics
        metrics = self._calculate_market_metrics(sales_data, inventory_data, price_trends)
        
        # Identify market trends
        trends = self._identify_market_trends(sales_data, price_trends)
        
        # Detect market anomalies
        anomalies = self._detect_market_anomalies(sales_data, metrics)
        
        # Generate market insights
        insights = self._generate_market_insights(metrics, trends, anomalies)
        
        confidence = self._calculate_confidence(len(sales_data), len(anomalies))
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return T2Analysis(
            analysis_id=self._generate_analysis_id(),
            source_data=[t1_data.get("extraction_id")],
            metrics=AnalyticalMetrics(
                calculated_values=metrics,
                trends=trends,
                anomalies=anomalies,
                correlations={}
            ),
            insights=insights,
            confidence_score=confidence,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time
        )
    
    def _calculate_market_metrics(self, sales: List[Dict], inventory: Dict, price_trends: List[Dict]) -> Dict[str, float]:
        """Calculate comprehensive market metrics"""
        metrics = {}
        
        # Sales metrics
        if sales:
            sale_prices = [s.get("sale_price", 0) for s in sales if s.get("sale_price", 0) > 0]
            list_prices = [s.get("list_price", 0) for s in sales if s.get("list_price", 0) > 0]
            
            if sale_prices:
                metrics.update({
                    "avg_sale_price": np.mean(sale_prices),
                    "median_sale_price": np.median(sale_prices),
                    "total_sales_volume": sum(sale_prices),
                    "num_sales": len(sale_prices)
                })
            
            # Sale to list ratio
            if sale_prices and list_prices and len(sale_prices) == len(list_prices):
                ratios = [s/l for s, l in zip(sale_prices, list_prices) if l > 0]
                if ratios:
                    metrics["avg_sale_to_list_ratio"] = np.mean(ratios)
        
        # Inventory metrics
        if inventory:
            metrics.update({
                "current_inventory": inventory.get("total_active", 0),
                "new_listings": inventory.get("new_this_week", 0),
                "pending_sales": inventory.get("pending", 0),
                "months_of_inventory": inventory.get("months_supply", 0)
            })
        
        # Price trend metrics
        if price_trends:
            recent_trends = price_trends[-12:]  # Last 12 periods
            prices = [t.get("median_price", 0) for t in recent_trends if t.get("median_price", 0) > 0]
            
            if len(prices) > 1:
                # Calculate price appreciation
                price_change = (prices[-1] - prices[0]) / prices[0] * 100
                metrics["price_appreciation_rate"] = price_change
        
        # Market velocity
        if sales:
            dom_values = [s.get("days_on_market", 0) for s in sales if s.get("days_on_market", 0) > 0]
            if dom_values:
                metrics["market_velocity_days"] = np.mean(dom_values)
        
        return metrics
    
    def _identify_market_trends(self, sales: List[Dict], price_trends: List[Dict]) -> Dict[str, Dict]:
        """Identify market trends and patterns"""
        trends = {}
        
        # Sales volume trend
        if sales:
            df_sales = pd.DataFrame(sales)
            if 'sale_date' in df_sales.columns:
                df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'], errors='coerce')
                df_sales['month'] = df_sales['sale_date'].dt.to_period('M')
                
                monthly_volumes = df_sales.groupby('month').agg({
                    'sale_price': ['count', 'sum', 'mean']
                })
                
                if len(monthly_volumes) > 2:
                    volume_trend = monthly_volumes[('sale_price', 'count')].pct_change().mean() * 100
                    
                    trends['sales_volume_trend'] = {
                        "direction": "increasing" if volume_trend > 0 else "decreasing",
                        "avg_monthly_change": float(volume_trend),
                        "latest_month_sales": int(monthly_volumes[('sale_price', 'count')].iloc[-1])
                    }
        
        # Price momentum
        if price_trends and len(price_trends) > 3:
            recent_prices = [t.get("median_price", 0) for t in price_trends[-6:]]
            if all(p > 0 for p in recent_prices):
                # Calculate momentum (3-month vs 6-month average)
                momentum = (np.mean(recent_prices[-3:]) / np.mean(recent_prices) - 1) * 100
                
                trends['price_momentum'] = {
                    "momentum_indicator": float(momentum),
                    "trend": "accelerating" if momentum > 2 else "decelerating" if momentum < -2 else "stable"
                }
        
        # Seasonal patterns
        if sales and len(sales) > 50:
            df_sales = pd.DataFrame(sales)
            if 'sale_date' in df_sales.columns:
                df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'], errors='coerce')
                df_sales['quarter'] = df_sales['sale_date'].dt.quarter
                
                quarterly_avg = df_sales.groupby('quarter')['sale_price'].mean()
                if len(quarterly_avg) == 4:
                    trends['seasonal_pattern'] = {
                        "strongest_quarter": int(quarterly_avg.idxmax()),
                        "weakest_quarter": int(quarterly_avg.idxmin()),
                        "seasonal_variation": float(quarterly_avg.std() / quarterly_avg.mean() * 100)
                    }
        
        return trends
    
    def _detect_market_anomalies(self, sales: List[Dict], metrics: Dict) -> List[Dict]:
        """Detect market anomalies and unusual patterns"""
        anomalies = []
        
        avg_price = metrics.get("avg_sale_price", 0)
        median_dom = metrics.get("market_velocity_days", 0)
        
        for sale in sales:
            # Rapid sales (much faster than average)
            dom = sale.get("days_on_market", 0)
            if dom > 0 and median_dom > 0 and dom < median_dom * 0.2:
                anomalies.append({
                    "type": "rapid_sale",
                    "property_id": sale.get("property_id"),
                    "days_on_market": dom,
                    "avg_days": median_dom,
                    "speed_factor": median_dom / dom
                })
            
            # Price anomalies
            price = sale.get("sale_price", 0)
            list_price = sale.get("list_price", 0)
            
            if price > 0 and list_price > 0:
                # Over asking price by significant margin
                if price > list_price * 1.1:  # 10% over asking
                    anomalies.append({
                        "type": "over_asking_sale",
                        "property_id": sale.get("property_id"),
                        "sale_price": price,
                        "list_price": list_price,
                        "premium_pct": (price / list_price - 1) * 100
                    })
                
                # Significant price drop
                elif price < list_price * 0.85:  # 15% below asking
                    anomalies.append({
                        "type": "discounted_sale",
                        "property_id": sale.get("property_id"),
                        "sale_price": price,
                        "list_price": list_price,
                        "discount_pct": (1 - price / list_price) * 100
                    })
        
        # Market-wide anomalies
        months_inventory = metrics.get("months_of_inventory", 0)
        if months_inventory > 0:
            if months_inventory < 2:
                anomalies.append({
                    "type": "inventory_shortage",
                    "months_supply": months_inventory,
                    "severity": "critical" if months_inventory < 1 else "high"
                })
            elif months_inventory > 6:
                anomalies.append({
                    "type": "inventory_surplus",
                    "months_supply": months_inventory,
                    "severity": "high" if months_inventory > 9 else "moderate"
                })
        
        return anomalies
    
    def _generate_market_insights(self, metrics: Dict, trends: Dict, anomalies: List) -> List[str]:
        """Generate market analysis insights"""
        insights = []
        
        # Sales volume insights
        num_sales = metrics.get("num_sales", 0)
        if num_sales > 0:
            insights.append(f"Analyzed {num_sales} property sales")
            
            total_volume = metrics.get("total_sales_volume", 0)
            if total_volume > 1000000:
                insights.append(f"Total sales volume: ${total_volume/1000000:.1f}M")
        
        # Price insights
        median_price = metrics.get("median_sale_price", 0)
        if median_price > 0:
            insights.append(f"Median sale price: ${median_price:,.0f}")
            
            appreciation = metrics.get("price_appreciation_rate", 0)
            if abs(appreciation) > 5:
                direction = "appreciated" if appreciation > 0 else "depreciated"
                insights.append(f"Prices {direction} {abs(appreciation):.1f}% over analyzed period")
        
        # Market velocity
        velocity = metrics.get("market_velocity_days", 0)
        if velocity > 0:
            if velocity < 30:
                insights.append(f"Hot market conditions: properties selling in {velocity:.0f} days average")
            elif velocity > 90:
                insights.append(f"Slow market: properties taking {velocity:.0f} days to sell")
        
        # Sale to list ratio
        ratio = metrics.get("avg_sale_to_list_ratio", 0)
        if ratio > 0:
            if ratio > 0.98:
                insights.append(f"Strong seller's market: {ratio*100:.1f}% sale-to-list ratio")
            elif ratio < 0.95:
                insights.append(f"Buyer negotiation power: {ratio*100:.1f}% sale-to-list ratio")
        
        # Inventory insights
        months_inv = metrics.get("months_of_inventory", 0)
        if months_inv > 0:
            if months_inv < 3:
                insights.append(f"Low inventory: {months_inv:.1f} months supply")
            elif months_inv > 6:
                insights.append(f"High inventory: {months_inv:.1f} months supply")
        
        # Trend insights
        volume_trend = trends.get("sales_volume_trend", {})
        if volume_trend:
            direction = volume_trend.get("direction")
            change = volume_trend.get("avg_monthly_change", 0)
            if abs(change) > 10:
                insights.append(f"Sales volume {direction} at {abs(change):.1f}% monthly rate")
        
        # Anomaly insights
        if anomalies:
            rapid_sales = len([a for a in anomalies if a["type"] == "rapid_sale"])
            if rapid_sales > 0:
                insights.append(f"{rapid_sales} properties sold unusually quickly")
            
            over_asking = len([a for a in anomalies if a["type"] == "over_asking_sale"])
            if over_asking > 0:
                insights.append(f"{over_asking} properties sold above asking price")
        
        return insights
    
    async def _analyze_distressed_properties(self, t1_data: Dict) -> T2Analysis:
        """Analyze distressed property indicators"""
        start_time = datetime.now()
        
        data = t1_data.get("data", {})
        properties = data.get("distressed_properties", [])
        
        # Calculate distressed property metrics
        metrics = self._calculate_distressed_metrics(properties)
        
        # Identify distressed property patterns
        trends = self._identify_distressed_trends(properties)
        
        # Detect anomalies
        anomalies = self._detect_distressed_anomalies(properties, metrics)
        
        # Generate insights
        insights = self._generate_distressed_insights(metrics, trends, anomalies)
        
        confidence = self._calculate_confidence(len(properties), len(anomalies))
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return T2Analysis(
            analysis_id=self._generate_analysis_id(),
            source_data=[t1_data.get("extraction_id")],
            metrics=AnalyticalMetrics(
                calculated_values=metrics,
                trends=trends,
                anomalies=anomalies,
                correlations={}
            ),
            insights=insights,
            confidence_score=confidence,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time
        )
    
    def _calculate_distressed_metrics(self, properties: List[Dict]) -> Dict[str, float]:
        """Calculate metrics for distressed properties"""
        if not properties:
            return {}
        
        # Categorize by distress type
        foreclosures = [p for p in properties if p.get("distress_type") == "foreclosure"]
        tax_liens = [p for p in properties if p.get("distress_type") == "tax_lien"]
        abandoned = [p for p in properties if p.get("distress_type") == "abandoned"]
        
        metrics = {
            "total_distressed": len(properties),
            "foreclosures": len(foreclosures),
            "tax_liens": len(tax_liens),
            "abandoned": len(abandoned),
            "foreclosure_rate": len(foreclosures) / len(properties) * 100 if properties else 0,
            "tax_lien_rate": len(tax_liens) / len(properties) * 100 if properties else 0
        }
        
        # Financial metrics
        estimated_values = [p.get("estimated_value", 0) for p in properties if p.get("estimated_value", 0) > 0]
        if estimated_values:
            metrics.update({
                "total_distressed_value": sum(estimated_values),
                "avg_distressed_value": np.mean(estimated_values),
                "median_distressed_value": np.median(estimated_values)
            })
        
        # Days in distress
        days_distressed = [p.get("days_distressed", 0) for p in properties if p.get("days_distressed", 0) > 0]
        if days_distressed:
            metrics["avg_days_distressed"] = np.mean(days_distressed)
        
        return metrics
    
    def _identify_distressed_trends(self, properties: List[Dict]) -> Dict[str, Dict]:
        """Identify trends in distressed properties"""
        if not properties:
            return {}
        
        df = pd.DataFrame(properties)
        trends = {}
        
        # Geographic concentration
        if 'neighborhood' in df.columns:
            neighborhood_counts = df['neighborhood'].value_counts()
            
            trends['geographic_concentration'] = {
                "highest_distress_area": neighborhood_counts.idxmax() if not neighborhood_counts.empty else None,
                "distressed_by_area": neighborhood_counts.head(5).to_dict(),
                "concentration_score": float(neighborhood_counts.iloc[0] / len(df) * 100) if not neighborhood_counts.empty else 0
            }
        
        # Distress type trends
        if 'distress_type' in df.columns:
            type_counts = df['distress_type'].value_counts()
            
            trends['distress_types'] = {
                "primary_type": type_counts.idxmax() if not type_counts.empty else None,
                "type_distribution": type_counts.to_dict()
            }
        
        # Time-based trends
        if 'distress_date' in df.columns:
            df['distress_date'] = pd.to_datetime(df['distress_date'], errors='coerce')
            df['month'] = df['distress_date'].dt.to_period('M')
            
            monthly_counts = df.groupby('month').size()
            if len(monthly_counts) > 1:
                trend_direction = "increasing" if monthly_counts.iloc[-1] > monthly_counts.iloc[0] else "decreasing"
                
                trends['temporal_trend'] = {
                    "direction": trend_direction,
                    "recent_month_count": int(monthly_counts.iloc[-1]),
                    "avg_monthly": float(monthly_counts.mean())
                }
        
        return trends
    
    def _detect_distressed_anomalies(self, properties: List[Dict], metrics: Dict) -> List[Dict]:
        """Detect anomalies in distressed property data"""
        anomalies = []
        
        avg_value = metrics.get("avg_distressed_value", 0)
        avg_days = metrics.get("avg_days_distressed", 0)
        
        for prop in properties:
            # High-value distressed properties
            value = prop.get("estimated_value", 0)
            if value > 0 and avg_value > 0 and value > avg_value * 3:
                anomalies.append({
                    "type": "high_value_distressed",
                    "property_id": prop.get("property_id"),
                    "value": value,
                    "avg_value": avg_value,
                    "multiplier": value / avg_value
                })
            
            # Long-term distressed
            days = prop.get("days_distressed", 0)
            if days > 365:  # Over 1 year
                anomalies.append({
                    "type": "chronic_distress",
                    "property_id": prop.get("property_id"),
                    "days_distressed": days,
                    "years": days / 365
                })
            
            # Multiple distress indicators
            distress_indicators = prop.get("distress_indicators", [])
            if len(distress_indicators) > 2:
                anomalies.append({
                    "type": "multiple_distress_factors",
                    "property_id": prop.get("property_id"),
                    "indicators": distress_indicators,
                    "count": len(distress_indicators)
                })
        
        # Geographic clustering
        neighborhood_counts = defaultdict(int)
        for prop in properties:
            neighborhood = prop.get("neighborhood", "unknown")
            neighborhood_counts[neighborhood] += 1
        
        # Find neighborhoods with high concentration
        total = len(properties)
        for neighborhood, count in neighborhood_counts.items():
            if count > total * 0.2:  # More than 20% in one area
                anomalies.append({
                    "type": "distress_cluster",
                    "neighborhood": neighborhood,
                    "property_count": count,
                    "concentration_pct": count / total * 100
                })
        
        return anomalies
    
    def _generate_distressed_insights(self, metrics: Dict, trends: Dict, anomalies: List) -> List[str]:
        """Generate insights about distressed properties"""
        insights = []
        
        # Overview
        total = metrics.get("total_distressed", 0)
        if total > 0:
            insights.append(f"Identified {total} distressed properties")
            
            # Type breakdown
            foreclosures = metrics.get("foreclosures", 0)
            tax_liens = metrics.get("tax_liens", 0)
            
            if foreclosures > 0:
                insights.append(f"{foreclosures} properties in foreclosure ({metrics.get('foreclosure_rate', 0):.1f}%)")
            if tax_liens > 0:
                insights.append(f"{tax_liens} properties with tax liens ({metrics.get('tax_lien_rate', 0):.1f}%)")
        
        # Value insights
        total_value = metrics.get("total_distressed_value", 0)
        if total_value > 0:
            insights.append(f"Total distressed property value: ${total_value:,.0f}")
        
        # Geographic insights
        geo_data = trends.get("geographic_concentration", {})
        if geo_data:
            top_area = geo_data.get("highest_distress_area")
            concentration = geo_data.get("concentration_score", 0)
            
            if top_area and concentration > 15:
                insights.append(f"{top_area} shows highest distress concentration ({concentration:.1f}%)")
        
        # Temporal trends
        temporal = trends.get("temporal_trend", {})
        if temporal:
            direction = temporal.get("direction")
            insights.append(f"Distressed property count {direction}")
        
        # Duration insights
        avg_days = metrics.get("avg_days_distressed", 0)
        if avg_days > 0:
            insights.append(f"Average time in distress: {avg_days:.0f} days")
        
        # Anomaly insights
        if anomalies:
            clusters = [a for a in anomalies if a["type"] == "distress_cluster"]
            if clusters:
                insights.append(f"{len(clusters)} neighborhoods showing distress clustering")
            
            chronic = len([a for a in anomalies if a["type"] == "chronic_distress"])
            if chronic > 0:
                insights.append(f"{chronic} properties in distress for over 1 year")
        
        return insights
    
    async def _analyze_generic(self, t1_data: Dict) -> T2Analysis:
        """Generic analysis for unspecified data types"""
        start_time = datetime.now()
        
        data = t1_data.get("data", {})
        
        # Basic metrics
        metrics = {
            "record_count": len(data) if isinstance(data, list) else 1,
            "data_completeness": self._calculate_completeness(data)
        }
        
        # Simple trend analysis
        trends = {}
        if isinstance(data, list) and len(data) > 10:
            trends["data_volume"] = {
                "size": len(data),
                "complexity": "high" if len(data) > 100 else "moderate"
            }
        
        anomalies = []
        insights = [f"Processed generic data with {metrics['record_count']} records"]
        
        confidence = 0.7  # Lower confidence for generic analysis
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return T2Analysis(
            analysis_id=self._generate_analysis_id(),
            source_data=[t1_data.get("extraction_id")],
            metrics=AnalyticalMetrics(
                calculated_values=metrics,
                trends=trends,
                anomalies=anomalies,
                correlations={}
            ),
            insights=insights,
            confidence_score=confidence,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time
        )
    
    def _calculate_completeness(self, data: Any) -> float:
        """Calculate data completeness score"""
        if isinstance(data, dict):
            total_fields = len(data)
            filled_fields = sum(1 for v in data.values() if v is not None and v != "")
            return filled_fields / total_fields if total_fields > 0 else 0
        elif isinstance(data, list):
            if not data:
                return 0
            # Sample first few items
            sample = data[:min(10, len(data))]
            scores = [self._calculate_completeness(item) for item in sample]
            return np.mean(scores) if scores else 0
        else:
            return 1.0 if data else 0.0
    
    def _calculate_confidence(self, data_points: int, anomaly_count: int) -> float:
        """Calculate confidence score for analysis"""
        # Base confidence on data volume
        if data_points < 10:
            base_confidence = 0.6
        elif data_points < 50:
            base_confidence = 0.7
        elif data_points < 100:
            base_confidence = 0.8
        else:
            base_confidence = 0.9
        
        # Adjust for anomalies
        if data_points > 0:
            anomaly_ratio = anomaly_count / data_points
            if anomaly_ratio > 0.2:  # More than 20% anomalies
                base_confidence *= 0.8
            elif anomaly_ratio > 0.1:  # More than 10% anomalies
                base_confidence *= 0.9
        
        return min(base_confidence, 0.95)  # Cap at 95%
    
    def _generate_analysis_id(self) -> str:
        """Generate unique analysis ID"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        random_suffix = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:5]
        return f"t2-{timestamp}-{random_suffix}"
    
    async def _save_analysis(self, analysis: T2Analysis):
        """Save analysis results to file"""
        filename = f"{analysis.analysis_id}.json"
        filepath = self.t2_output_path / filename
        
        # Convert to dict
        analysis_dict = {
            "analysis_id": analysis.analysis_id,
            "source_data": analysis.source_data,
            "metrics": {
                "calculated_values": analysis.metrics.calculated_values,
                "trends": analysis.metrics.trends,
                "anomalies": analysis.metrics.anomalies,
                "correlations": analysis.metrics.correlations
            },
            "insights": analysis.insights,
            "confidence_score": analysis.confidence_score,
            "timestamp": analysis.timestamp,
            "processing_time_ms": analysis.processing_time_ms,
            "agent_id": self.agent_id
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(analysis_dict, f, indent=2)
        
        logger.info(f"Saved analysis: {filename}")
    
    async def monitor_t1_extractions(self):
        """Continuously monitor for new T1 extractions"""
        logger.info("Starting T1 extraction monitoring...")
        
        while True:
            try:
                # Check for new T1 files
                t1_files = list(self.t1_data_path.glob("t1-*.json"))
                
                for t1_file in t1_files:
                    if t1_file.name not in self.processed_files:
                        logger.info(f"Processing new T1 extraction: {t1_file.name}")
                        await self.process_t1_data(t1_file)
                
                # Wait before next check
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(30)


# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize T2 agent
        agent = T2AnalyticalAgent()
        
        # Start monitoring for T1 data
        await agent.monitor_t1_extractions()
    
    # Run the agent
    asyncio.run(main())