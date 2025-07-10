"""
Integrated Houston Intelligence API
Combines WebSocket, Batch Processing, GraphQL, and Webhooks with T2 Intelligence
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

# Import our modules
from websocket.websocket_server import HoustonIntelligenceWebSocket, IntelligenceUpdate, UpdateType
from batch.batch_processor import BatchProcessor, BatchRequest, BatchResponse
from houston_graphql.graphql_api import schema as graphql_schema, IntelligenceDataService
from webhooks.webhook_manager import WebhookManager, EventMonitor, WebhookConfig, WebhookEvent, WebhookEventType
from strawberry.fastapi import GraphQLRouter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("IntegratedAPI")


class IntegratedIntelligenceAPI:
    """Main integrated API combining all advanced features"""
    
    def __init__(self):
        # Initialize components
        self.websocket_server = HoustonIntelligenceWebSocket()
        self.batch_processor = BatchProcessor()
        self.webhook_manager = WebhookManager()
        self.event_monitor = EventMonitor(self.webhook_manager)
        self.intelligence_service = IntelligenceDataService()
        
        # Shared state
        self.active_connections: Dict[str, WebSocket] = {}
        self.analysis_cache: Dict[str, Any] = {}
        
    async def initialize(self):
        """Initialize all components"""
        logger.info("Initializing Integrated Houston Intelligence API...")
        
        # Initialize webhook manager
        await self.webhook_manager.initialize()
        
        # Start event monitoring
        await self.event_monitor.start_monitoring()
        
        # Start background tasks
        asyncio.create_task(self._sync_updates())
        asyncio.create_task(self._monitor_t2_outputs())
        
        logger.info("Integrated API initialized successfully")
    
    async def shutdown(self):
        """Shutdown all components"""
        logger.info("Shutting down Integrated API...")
        await self.event_monitor.stop_monitoring()
    
    async def _sync_updates(self):
        """Sync updates between different components"""
        while True:
            try:
                # Check for new T2 analysis results
                analysis_dir = Path("/Users/fernandox/Desktop/Core Agent Architecture/shared_state/t2_analysis")
                
                for file_path in analysis_dir.glob("*_analysis_*.json"):
                    file_key = file_path.name
                    mtime = file_path.stat().st_mtime
                    
                    # Check if file is new or updated
                    if file_key not in self.analysis_cache or self.analysis_cache[file_key].get("mtime", 0) < mtime:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        self.analysis_cache[file_key] = {
                            "data": data,
                            "mtime": mtime,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # Create update for WebSocket
                        update = IntelligenceUpdate(
                            update_type=UpdateType.ANALYSIS_COMPLETE,
                            domain=data.get("domain", "unknown"),
                            timestamp=data.get("timestamp", datetime.now().isoformat()),
                            data={
                                "confidence_score": data.get("confidence_score", 0),
                                "key_findings": data.get("key_findings", [])[:3]
                            },
                            confidence=data.get("confidence_score", 0)
                        )
                        
                        # Queue for WebSocket broadcast
                        await self.websocket_server.update_queue.put(update)
                        
                        # Trigger webhook event
                        webhook_event = WebhookEvent(
                            event_type=WebhookEventType.ANALYSIS_COMPLETE,
                            domain=data.get("domain"),
                            data={
                                "domain": data.get("domain"),
                                "confidence_score": data.get("confidence_score"),
                                "key_findings": data.get("key_findings", [])[:3]
                            }
                        )
                        await self.webhook_manager.trigger_event(webhook_event)
                        
            except Exception as e:
                logger.error(f"Error in sync updates: {e}")
            
            await asyncio.sleep(5)
    
    async def _monitor_t2_outputs(self):
        """Monitor T2 outputs for batch job completion"""
        while True:
            try:
                # Check for completed batch jobs
                for batch_id, job in self.batch_processor.jobs.items():
                    if job.status.value == "completed" and not job.request.callback_url:
                        # Trigger webhook for batch completion
                        webhook_event = WebhookEvent(
                            event_type=WebhookEventType.BATCH_COMPLETE,
                            data={
                                "batch_id": batch_id,
                                "total_queries": len(job.request.queries),
                                "completed": len([r for r in job.results.values() if r.status == "completed"]),
                                "failed": len([r for r in job.results.values() if r.status == "failed"])
                            }
                        )
                        await self.webhook_manager.trigger_event(webhook_event)
                        
                        # Remove from active jobs after notification
                        del self.batch_processor.jobs[batch_id]
                        
            except Exception as e:
                logger.error(f"Error monitoring batch jobs: {e}")
            
            await asyncio.sleep(10)


# Create integrated API instance
integrated_api = IntegratedIntelligenceAPI()

# FastAPI app with lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await integrated_api.initialize()
    yield
    # Shutdown
    await integrated_api.shutdown()

app = FastAPI(
    title="Houston Intelligence Platform - Integrated API",
    description="Advanced API with WebSocket, Batch Processing, GraphQL, and Webhooks",
    version="2.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate user from token"""
    # In production, validate JWT token
    return {"user_id": "demo_user", "role": "analyst"}


# REST Endpoints
@app.get("/")
async def root():
    """API documentation"""
    return {
        "name": "Houston Intelligence Platform - Integrated API",
        "version": "2.0",
        "endpoints": {
            "websocket": "ws://localhost:8000/ws",
            "graphql": "/graphql",
            "batch": "/batch/*",
            "webhooks": "/webhooks/*",
            "rest": "/api/*"
        },
        "documentation": "/docs"
    }


@app.get("/api/status")
async def api_status():
    """Get API status"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "websocket": "active",
            "batch_processor": "active",
            "graphql": "active",
            "webhooks": "active"
        },
        "active_connections": len(integrated_api.active_connections),
        "cached_analyses": len(integrated_api.analysis_cache),
        "active_batch_jobs": len(integrated_api.batch_processor.jobs)
    }


@app.get("/api/domains/{domain}/latest")
async def get_latest_analysis(domain: str, user=Depends(get_current_user)):
    """Get latest analysis for a domain"""
    analysis = await integrated_api.intelligence_service.get_domain_analysis(domain)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"No analysis found for domain: {domain}")
    
    return {
        "domain": analysis.domain,
        "confidence_score": analysis.confidence_score,
        "timestamp": analysis.timestamp,
        "key_findings": [f.finding for f in analysis.key_findings],
        "opportunities": [
            {
                "type": o.type,
                "potential": o.potential,
                "description": o.description,
                "expected_roi": o.expected_roi
            }
            for o in analysis.opportunities
        ],
        "risks": [
            {
                "type": r.type,
                "severity": r.severity,
                "description": r.description,
                "mitigation": r.mitigation
            }
            for r in analysis.risks
        ]
    }


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    
    # Add to active connections
    connection_id = f"conn_{datetime.now().timestamp()}"
    integrated_api.active_connections[connection_id] = websocket
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat()
        })
        
        # Handle messages
        while True:
            data = await websocket.receive_json()
            
            # Process subscription requests
            if data.get("type") == "subscribe":
                channels = data.get("channels", [])
                await websocket.send_json({
                    "type": "subscription_confirmed",
                    "channels": channels,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Send latest data for subscribed channels
                for channel in channels:
                    if channel in ["market", "financial", "neighborhood", "environmental", "regulatory", "technology"]:
                        analysis = await integrated_api.intelligence_service.get_domain_analysis(channel)
                        if analysis:
                            await websocket.send_json({
                                "type": "initial_data",
                                "channel": channel,
                                "data": {
                                    "confidence_score": analysis.confidence_score,
                                    "key_findings": [f.finding for f in analysis.key_findings[:3]]
                                }
                            })
            
    except WebSocketDisconnect:
        # Remove from active connections
        del integrated_api.active_connections[connection_id]
        logger.info(f"WebSocket client {connection_id} disconnected")


# Batch Processing endpoints
@app.post("/batch/submit", response_model=BatchResponse)
async def submit_batch(request: BatchRequest, user=Depends(get_current_user)):
    """Submit batch processing request"""
    return await integrated_api.batch_processor.submit_batch(request)


@app.get("/batch/{batch_id}/status", response_model=BatchResponse)
async def get_batch_status(batch_id: str, user=Depends(get_current_user)):
    """Get batch job status"""
    try:
        return await integrated_api.batch_processor.get_batch_status(batch_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Batch job not found")


# Webhook endpoints
@app.post("/webhooks/subscribe")
async def subscribe_webhook(config: WebhookConfig, user=Depends(get_current_user)):
    """Subscribe to webhook notifications"""
    subscription_id = await integrated_api.webhook_manager.subscribe(config)
    return {
        "subscription_id": subscription_id,
        "status": "active",
        "events": [e.value for e in config.events]
    }


@app.get("/webhooks")
async def list_webhooks(user=Depends(get_current_user)):
    """List active webhook subscriptions"""
    return await integrated_api.webhook_manager.list_subscriptions()


# GraphQL endpoint
graphql_context = {
    "intelligence_service": integrated_api.intelligence_service
}

graphql_app = GraphQLRouter(
    graphql_schema,
    context_getter=lambda: graphql_context
)

app.include_router(graphql_app, prefix="/graphql")


# Demo WebSocket client page
@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """Demo page for WebSocket testing"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Houston Intelligence WebSocket Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .message { margin: 5px 0; padding: 5px; background: #f0f0f0; }
            .update { background: #e0f0ff; }
            .alert { background: #ffe0e0; }
            button { margin: 5px; }
        </style>
    </head>
    <body>
        <h1>Houston Intelligence Real-Time Updates</h1>
        
        <div>
            <button onclick="connect()">Connect</button>
            <button onclick="disconnect()">Disconnect</button>
            <button onclick="subscribeAll()">Subscribe All</button>
            <button onclick="subscribeAlerts()">Subscribe Alerts Only</button>
        </div>
        
        <div id="status">Disconnected</div>
        <div id="messages"></div>
        
        <script>
            let ws = null;
            
            function connect() {
                ws = new WebSocket('ws://localhost:8000/ws');
                
                ws.onopen = () => {
                    document.getElementById('status').textContent = 'Connected';
                    addMessage('Connected to Houston Intelligence Platform', 'update');
                };
                
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    console.log('Received:', data);
                    
                    const className = data.type.includes('alert') ? 'alert' : 'update';
                    addMessage(`${data.type}: ${JSON.stringify(data.data || {})}`, className);
                };
                
                ws.onclose = () => {
                    document.getElementById('status').textContent = 'Disconnected';
                    addMessage('Disconnected from server', 'message');
                };
            }
            
            function disconnect() {
                if (ws) ws.close();
            }
            
            function subscribeAll() {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'subscribe',
                        channels: ['all', 'market', 'financial', 'neighborhood']
                    }));
                }
            }
            
            function subscribeAlerts() {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'subscribe',
                        channels: ['alerts']
                    }));
                }
            }
            
            function addMessage(text, className = 'message') {
                const messages = document.getElementById('messages');
                const message = document.createElement('div');
                message.className = `message ${className}`;
                message.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
                messages.insertBefore(message, messages.firstChild);
                
                // Keep only last 50 messages
                while (messages.children.length > 50) {
                    messages.removeChild(messages.lastChild);
                }
            }
            
            // Auto-connect on load
            window.onload = () => connect();
        </script>
    </body>
    </html>
    """


# Example usage documentation
@app.get("/api/examples")
async def get_examples():
    """Get API usage examples"""
    return {
        "websocket": {
            "description": "Connect to WebSocket for real-time updates",
            "example": {
                "url": "ws://localhost:8000/ws",
                "subscribe": {
                    "type": "subscribe",
                    "channels": ["market", "financial", "alerts"]
                }
            }
        },
        "batch": {
            "description": "Submit multiple queries for batch processing",
            "example": {
                "url": "POST /batch/submit",
                "body": {
                    "queries": [
                        {
                            "query_type": "domain_analysis",
                            "domain": "market"
                        },
                        {
                            "query_type": "cross_domain",
                            "parameters": {
                                "domains": ["market", "financial"]
                            }
                        }
                    ]
                }
            }
        },
        "graphql": {
            "description": "Flexible queries with GraphQL",
            "example": {
                "url": "/graphql",
                "query": """
                    query {
                        marketSnapshot {
                            overallConfidence
                            marketSentiment
                            topOpportunities {
                                type
                                description
                                expectedRoi
                            }
                        }
                    }
                """
            }
        },
        "webhooks": {
            "description": "Subscribe to push notifications",
            "example": {
                "url": "POST /webhooks/subscribe",
                "body": {
                    "url": "https://your-server.com/webhook",
                    "events": ["analysis.complete", "risk.alert"],
                    "domains": ["market", "financial"]
                }
            }
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["default"],
            },
        }
    )