"""
Batch Processing System for Houston Intelligence API
Handles multiple queries efficiently with parallel processing
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import aiofiles
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import uuid
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np


class BatchStatus(Enum):
    """Batch job status"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class QueryType(Enum):
    """Types of batch queries"""
    DOMAIN_ANALYSIS = "domain_analysis"
    CROSS_DOMAIN = "cross_domain"
    COMPARATIVE = "comparative"
    HISTORICAL = "historical"
    PREDICTIVE = "predictive"
    CUSTOM = "custom"


class BatchQuery(BaseModel):
    """Individual query in a batch"""
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_type: QueryType
    domain: Optional[str] = None
    parameters: Dict[str, Any] = {}
    priority: int = 5  # 1-10, higher is more important


class BatchRequest(BaseModel):
    """Batch processing request"""
    batch_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    queries: List[BatchQuery]
    callback_url: Optional[str] = None
    parallel_execution: bool = True
    max_parallel: int = 10
    timeout_seconds: int = 300
    return_partial_results: bool = True


class BatchResult(BaseModel):
    """Result of a batch query"""
    query_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: int = 0
    confidence_score: Optional[float] = None


class BatchResponse(BaseModel):
    """Batch processing response"""
    batch_id: str
    status: BatchStatus
    total_queries: int
    completed_queries: int
    failed_queries: int
    results: List[BatchResult]
    start_time: str
    end_time: Optional[str] = None
    total_execution_time_ms: int = 0


@dataclass
class BatchJob:
    """Internal batch job representation"""
    batch_id: str
    request: BatchRequest
    status: BatchStatus
    results: Dict[str, BatchResult]
    start_time: datetime
    end_time: Optional[datetime] = None
    progress: float = 0.0


class BatchProcessor:
    """Handles batch processing of intelligence queries"""
    
    def __init__(self, max_workers: int = 20):
        self.max_workers = max_workers
        self.jobs: Dict[str, BatchJob] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.process_executor = ProcessPoolExecutor(max_workers=4)  # For CPU-intensive tasks
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("BatchProcessor")
        
        # Load analyzers (in production, these would be the actual T2 analyzers)
        self.analyzers = self._initialize_analyzers()
    
    def _initialize_analyzers(self) -> Dict[str, Any]:
        """Initialize domain analyzers"""
        # Placeholder - in production, load actual analyzers
        return {
            "market": "MarketAnalyzer",
            "neighborhood": "NeighborhoodAnalyzer",
            "financial": "FinancialAnalyzer",
            "environmental": "EnvironmentalAnalyzer",
            "regulatory": "RegulatoryAnalyzer",
            "technology": "TechnologyAnalyzer"
        }
    
    async def submit_batch(self, request: BatchRequest) -> BatchResponse:
        """Submit a batch job for processing"""
        # Create batch job
        job = BatchJob(
            batch_id=request.batch_id,
            request=request,
            status=BatchStatus.QUEUED,
            results={},
            start_time=datetime.now()
        )
        
        self.jobs[request.batch_id] = job
        
        # Start processing in background
        asyncio.create_task(self._process_batch(job))
        
        # Return initial response
        return self._create_batch_response(job)
    
    async def _process_batch(self, job: BatchJob):
        """Process a batch job"""
        try:
            job.status = BatchStatus.PROCESSING
            
            if job.request.parallel_execution:
                # Process queries in parallel
                await self._process_parallel(job)
            else:
                # Process queries sequentially
                await self._process_sequential(job)
            
            # Update final status
            failed_count = sum(1 for r in job.results.values() if r.status == "failed")
            if failed_count == 0:
                job.status = BatchStatus.COMPLETED
            elif failed_count == len(job.request.queries):
                job.status = BatchStatus.FAILED
            else:
                job.status = BatchStatus.PARTIAL
            
            job.end_time = datetime.now()
            
            # Send callback if provided
            if job.request.callback_url:
                await self._send_callback(job)
                
        except Exception as e:
            self.logger.error(f"Batch processing error: {e}")
            job.status = BatchStatus.FAILED
            job.end_time = datetime.now()
    
    async def _process_parallel(self, job: BatchJob):
        """Process queries in parallel"""
        semaphore = asyncio.Semaphore(job.request.max_parallel)
        
        async def process_with_semaphore(query: BatchQuery):
            async with semaphore:
                return await self._process_single_query(query)
        
        # Create tasks for all queries
        tasks = []
        for query in job.request.queries:
            task = asyncio.create_task(process_with_semaphore(query))
            tasks.append((query.query_id, task))
        
        # Wait for all tasks with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*[task for _, task in tasks], return_exceptions=True),
                timeout=job.request.timeout_seconds
            )
            
            # Store results
            for (query_id, _), result in zip(tasks, results):
                if isinstance(result, Exception):
                    job.results[query_id] = BatchResult(
                        query_id=query_id,
                        status="failed",
                        error=str(result)
                    )
                else:
                    job.results[query_id] = result
                    
        except asyncio.TimeoutError:
            # Handle timeout
            for query_id, task in tasks:
                if query_id not in job.results:
                    task.cancel()
                    job.results[query_id] = BatchResult(
                        query_id=query_id,
                        status="failed",
                        error="Query timeout"
                    )
    
    async def _process_sequential(self, job: BatchJob):
        """Process queries sequentially"""
        for query in job.request.queries:
            try:
                result = await asyncio.wait_for(
                    self._process_single_query(query),
                    timeout=job.request.timeout_seconds / len(job.request.queries)
                )
                job.results[query.query_id] = result
            except asyncio.TimeoutError:
                job.results[query.query_id] = BatchResult(
                    query_id=query.query_id,
                    status="failed",
                    error="Query timeout"
                )
            except Exception as e:
                job.results[query.query_id] = BatchResult(
                    query_id=query.query_id,
                    status="failed",
                    error=str(e)
                )
            
            # Update progress
            job.progress = len(job.results) / len(job.request.queries)
    
    async def _process_single_query(self, query: BatchQuery) -> BatchResult:
        """Process a single query"""
        start_time = datetime.now()
        
        try:
            # Route query to appropriate processor
            if query.query_type == QueryType.DOMAIN_ANALYSIS:
                result = await self._process_domain_analysis(query)
            elif query.query_type == QueryType.CROSS_DOMAIN:
                result = await self._process_cross_domain(query)
            elif query.query_type == QueryType.COMPARATIVE:
                result = await self._process_comparative(query)
            elif query.query_type == QueryType.HISTORICAL:
                result = await self._process_historical(query)
            elif query.query_type == QueryType.PREDICTIVE:
                result = await self._process_predictive(query)
            else:
                result = await self._process_custom(query)
            
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return BatchResult(
                query_id=query.query_id,
                status="completed",
                result=result,
                execution_time_ms=execution_time,
                confidence_score=result.get("confidence_score", 0.9)
            )
            
        except Exception as e:
            self.logger.error(f"Query processing error: {e}")
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return BatchResult(
                query_id=query.query_id,
                status="failed",
                error=str(e),
                execution_time_ms=execution_time
            )
    
    async def _process_domain_analysis(self, query: BatchQuery) -> Dict[str, Any]:
        """Process domain-specific analysis query"""
        domain = query.domain or "market"
        params = query.parameters
        
        # Simulate analysis (in production, call actual analyzer)
        await asyncio.sleep(0.5)  # Simulate processing time
        
        return {
            "domain": domain,
            "analysis_type": "comprehensive",
            "confidence_score": 0.92,
            "key_findings": [
                f"{domain.title()} showing strong growth indicators",
                f"Investment opportunities identified in {params.get('location', 'multiple areas')}",
                "Risk factors remain manageable"
            ],
            "metrics": {
                "growth_rate": 12.5,
                "roi_projection": 18.3,
                "risk_score": 3.2
            },
            "recommendations": [
                f"Focus on {domain} opportunities in Q1",
                "Monitor regulatory changes",
                "Diversify portfolio exposure"
            ]
        }
    
    async def _process_cross_domain(self, query: BatchQuery) -> Dict[str, Any]:
        """Process cross-domain analysis query"""
        domains = query.parameters.get("domains", ["market", "financial"])
        
        # Simulate cross-domain analysis
        await asyncio.sleep(0.8)
        
        return {
            "analysis_type": "cross_domain",
            "domains_analyzed": domains,
            "confidence_score": 0.89,
            "synergies": [
                {
                    "domains": domains[:2],
                    "synergy_score": 85,
                    "opportunity": "Combined strategy shows 25% higher returns"
                }
            ],
            "integrated_insights": [
                "Market conditions align with financial projections",
                "Technology adoption enhances ROI potential",
                "Environmental compliance creates competitive advantage"
            ]
        }
    
    async def _process_comparative(self, query: BatchQuery) -> Dict[str, Any]:
        """Process comparative analysis query"""
        locations = query.parameters.get("locations", ["EaDo", "Midtown", "Heights"])
        metrics = query.parameters.get("metrics", ["roi", "growth", "risk"])
        
        # Simulate comparative analysis
        await asyncio.sleep(0.6)
        
        comparison_data = {}
        for location in locations:
            comparison_data[location] = {
                metric: round(np.random.uniform(5, 25), 2) for metric in metrics
            }
        
        return {
            "analysis_type": "comparative",
            "locations": locations,
            "metrics": metrics,
            "confidence_score": 0.91,
            "comparison_data": comparison_data,
            "rankings": {
                metric: sorted(locations, key=lambda x: comparison_data[x][metric], reverse=True)
                for metric in metrics
            },
            "insights": [
                f"{locations[0]} leads in overall performance",
                "Significant variation in risk profiles observed",
                "Growth potential highest in emerging areas"
            ]
        }
    
    async def _process_historical(self, query: BatchQuery) -> Dict[str, Any]:
        """Process historical trend analysis"""
        time_period = query.parameters.get("time_period", "1_year")
        metrics = query.parameters.get("metrics", ["price", "volume", "velocity"])
        
        # Simulate historical analysis
        await asyncio.sleep(0.7)
        
        return {
            "analysis_type": "historical",
            "time_period": time_period,
            "confidence_score": 0.88,
            "trends": {
                metric: {
                    "direction": "increasing" if np.random.random() > 0.5 else "decreasing",
                    "change_percentage": round(np.random.uniform(-10, 20), 2),
                    "volatility": round(np.random.uniform(5, 25), 2)
                }
                for metric in metrics
            },
            "patterns_identified": [
                "Seasonal fluctuations in Q4",
                "Correlation with interest rate changes",
                "Growth acceleration in tech corridors"
            ]
        }
    
    async def _process_predictive(self, query: BatchQuery) -> Dict[str, Any]:
        """Process predictive analysis query"""
        horizon = query.parameters.get("horizon", "6_months")
        scenarios = query.parameters.get("scenarios", ["base", "optimistic", "pessimistic"])
        
        # Simulate predictive analysis using ML (placeholder)
        await asyncio.sleep(1.0)
        
        predictions = {}
        for scenario in scenarios:
            multiplier = {"optimistic": 1.2, "pessimistic": 0.8, "base": 1.0}[scenario]
            predictions[scenario] = {
                "roi_projection": round(15 * multiplier, 2),
                "price_change": round(8 * multiplier, 2),
                "risk_level": "low" if scenario == "optimistic" else "high" if scenario == "pessimistic" else "medium"
            }
        
        return {
            "analysis_type": "predictive",
            "horizon": horizon,
            "confidence_score": 0.85,
            "predictions": predictions,
            "key_drivers": [
                "Interest rate environment",
                "Population growth trends",
                "Infrastructure investments"
            ],
            "recommendations": [
                "Prepare for multiple scenarios",
                "Focus on resilient asset classes",
                "Maintain liquidity for opportunities"
            ]
        }
    
    async def _process_custom(self, query: BatchQuery) -> Dict[str, Any]:
        """Process custom analysis query"""
        # Custom query processing based on parameters
        await asyncio.sleep(0.5)
        
        return {
            "analysis_type": "custom",
            "query_parameters": query.parameters,
            "confidence_score": 0.87,
            "results": {
                "status": "completed",
                "custom_metrics": query.parameters
            }
        }
    
    async def get_batch_status(self, batch_id: str) -> BatchResponse:
        """Get status of a batch job"""
        job = self.jobs.get(batch_id)
        if not job:
            raise ValueError(f"Batch job {batch_id} not found")
        
        return self._create_batch_response(job)
    
    def _create_batch_response(self, job: BatchJob) -> BatchResponse:
        """Create batch response from job"""
        completed = len([r for r in job.results.values() if r.status == "completed"])
        failed = len([r for r in job.results.values() if r.status == "failed"])
        
        total_time = 0
        if job.end_time:
            total_time = int((job.end_time - job.start_time).total_seconds() * 1000)
        
        return BatchResponse(
            batch_id=job.batch_id,
            status=job.status,
            total_queries=len(job.request.queries),
            completed_queries=completed,
            failed_queries=failed,
            results=list(job.results.values()),
            start_time=job.start_time.isoformat(),
            end_time=job.end_time.isoformat() if job.end_time else None,
            total_execution_time_ms=total_time
        )
    
    async def _send_callback(self, job: BatchJob):
        """Send callback notification when batch completes"""
        try:
            import aiohttp
            
            response = self._create_batch_response(job)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    job.request.callback_url,
                    json=response.dict(),
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        self.logger.warning(f"Callback failed with status {resp.status}")
                        
        except Exception as e:
            self.logger.error(f"Failed to send callback: {e}")
    
    async def export_batch_results(self, batch_id: str, format: str = "json") -> Union[Dict, bytes]:
        """Export batch results in various formats"""
        job = self.jobs.get(batch_id)
        if not job:
            raise ValueError(f"Batch job {batch_id} not found")
        
        response = self._create_batch_response(job)
        
        if format == "json":
            return response.dict()
        
        elif format == "csv":
            # Convert to CSV
            rows = []
            for result in response.results:
                row = {
                    "query_id": result.query_id,
                    "status": result.status,
                    "confidence_score": result.confidence_score,
                    "execution_time_ms": result.execution_time_ms,
                    "error": result.error or ""
                }
                if result.result:
                    # Flatten result data
                    for key, value in result.result.items():
                        if isinstance(value, (str, int, float, bool)):
                            row[f"result_{key}"] = value
                rows.append(row)
            
            df = pd.DataFrame(rows)
            return df.to_csv(index=False).encode()
        
        elif format == "excel":
            # Convert to Excel
            import io
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Summary sheet
                summary_df = pd.DataFrame([{
                    "Batch ID": response.batch_id,
                    "Status": response.status.value,
                    "Total Queries": response.total_queries,
                    "Completed": response.completed_queries,
                    "Failed": response.failed_queries,
                    "Total Time (ms)": response.total_execution_time_ms
                }])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Results sheet
                results_data = []
                for result in response.results:
                    results_data.append({
                        "Query ID": result.query_id,
                        "Status": result.status,
                        "Confidence": result.confidence_score,
                        "Time (ms)": result.execution_time_ms,
                        "Error": result.error or ""
                    })
                
                results_df = pd.DataFrame(results_data)
                results_df.to_excel(writer, sheet_name='Results', index=False)
            
            output.seek(0)
            return output.read()
        
        else:
            raise ValueError(f"Unsupported format: {format}")


# FastAPI endpoints for batch processing
app = FastAPI(title="Houston Intelligence Batch API")

# Global batch processor
batch_processor = BatchProcessor()


@app.post("/batch/submit", response_model=BatchResponse)
async def submit_batch(request: BatchRequest):
    """Submit a batch of queries for processing"""
    return await batch_processor.submit_batch(request)


@app.get("/batch/{batch_id}/status", response_model=BatchResponse)
async def get_batch_status(batch_id: str):
    """Get status of a batch job"""
    try:
        return await batch_processor.get_batch_status(batch_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/batch/{batch_id}/export")
async def export_batch_results(batch_id: str, format: str = "json"):
    """Export batch results in various formats"""
    try:
        result = await batch_processor.export_batch_results(batch_id, format)
        
        if format == "json":
            return JSONResponse(content=result)
        elif format == "csv":
            return StreamingResponse(
                io.BytesIO(result),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=batch_{batch_id}.csv"}
            )
        elif format == "excel":
            return StreamingResponse(
                io.BytesIO(result),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename=batch_{batch_id}.xlsx"}
            )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/batch/upload")
async def upload_batch_file(file: UploadFile = File(...)):
    """Upload a CSV/Excel file with batch queries"""
    content = await file.read()
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Convert dataframe to batch queries
        queries = []
        for _, row in df.iterrows():
            query = BatchQuery(
                query_type=QueryType(row.get('query_type', 'domain_analysis')),
                domain=row.get('domain'),
                parameters=row.to_dict()
            )
            queries.append(query)
        
        # Create and submit batch request
        batch_request = BatchRequest(queries=queries)
        return await batch_processor.submit_batch(batch_request)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)