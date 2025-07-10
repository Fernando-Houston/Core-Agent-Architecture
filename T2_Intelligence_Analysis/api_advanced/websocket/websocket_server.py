"""
WebSocket Real-time Update System for Houston Intelligence API
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, List, Any, Optional
from pathlib import Path
import websockets
from websockets.server import WebSocketServerProtocol
import aiofiles
from dataclasses import dataclass, asdict
from enum import Enum


class UpdateType(Enum):
    """Types of real-time updates"""
    ANALYSIS_COMPLETE = "analysis_complete"
    DOMAIN_UPDATE = "domain_update"
    CROSS_DOMAIN_INSIGHT = "cross_domain_insight"
    RISK_ALERT = "risk_alert"
    OPPORTUNITY_ALERT = "opportunity_alert"
    METRIC_CHANGE = "metric_change"
    STATUS_UPDATE = "status_update"


@dataclass
class IntelligenceUpdate:
    """Structure for real-time intelligence updates"""
    update_type: UpdateType
    domain: str
    timestamp: str
    data: Dict[str, Any]
    priority: str = "normal"
    confidence: float = 0.0


class SubscriptionManager:
    """Manages client subscriptions to different update types"""
    
    def __init__(self):
        self.subscriptions: Dict[str, Set[WebSocketServerProtocol]] = {
            "all": set(),
            "market": set(),
            "neighborhood": set(),
            "financial": set(),
            "environmental": set(),
            "regulatory": set(),
            "technology": set(),
            "alerts": set(),
            "insights": set()
        }
        self.client_subscriptions: Dict[WebSocketServerProtocol, Set[str]] = {}
    
    def subscribe(self, client: WebSocketServerProtocol, channels: List[str]):
        """Subscribe client to channels"""
        if client not in self.client_subscriptions:
            self.client_subscriptions[client] = set()
        
        for channel in channels:
            if channel in self.subscriptions:
                self.subscriptions[channel].add(client)
                self.client_subscriptions[client].add(channel)
                logging.info(f"Client {client.remote_address} subscribed to {channel}")
    
    def unsubscribe(self, client: WebSocketServerProtocol, channels: Optional[List[str]] = None):
        """Unsubscribe client from channels"""
        if channels is None:
            channels = list(self.client_subscriptions.get(client, []))
        
        for channel in channels:
            if channel in self.subscriptions:
                self.subscriptions[channel].discard(client)
                if client in self.client_subscriptions:
                    self.client_subscriptions[client].discard(channel)
    
    def remove_client(self, client: WebSocketServerProtocol):
        """Remove client from all subscriptions"""
        for channel in self.subscriptions.values():
            channel.discard(client)
        self.client_subscriptions.pop(client, None)
    
    def get_subscribers(self, channels: List[str]) -> Set[WebSocketServerProtocol]:
        """Get all subscribers for given channels"""
        subscribers = set()
        for channel in channels:
            subscribers.update(self.subscriptions.get(channel, set()))
        return subscribers


class HoustonIntelligenceWebSocket:
    """WebSocket server for Houston Intelligence real-time updates"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.subscription_manager = SubscriptionManager()
        self.connected_clients: Set[WebSocketServerProtocol] = set()
        self.update_queue: asyncio.Queue = asyncio.Queue()
        self.file_watchers: Dict[str, asyncio.Task] = {}
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("WebSocketServer")
    
    async def register_client(self, websocket: WebSocketServerProtocol):
        """Register new client connection"""
        self.connected_clients.add(websocket)
        self.logger.info(f"Client connected: {websocket.remote_address}")
        
        # Send welcome message
        welcome = {
            "type": "connection",
            "status": "connected",
            "timestamp": datetime.now().isoformat(),
            "available_channels": list(self.subscription_manager.subscriptions.keys()),
            "server_version": "2.0"
        }
        await websocket.send(json.dumps(welcome))
    
    async def unregister_client(self, websocket: WebSocketServerProtocol):
        """Unregister client connection"""
        self.connected_clients.discard(websocket)
        self.subscription_manager.remove_client(websocket)
        self.logger.info(f"Client disconnected: {websocket.remote_address}")
    
    async def handle_client_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming client messages"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "subscribe":
                channels = data.get("channels", [])
                self.subscription_manager.subscribe(websocket, channels)
                await websocket.send(json.dumps({
                    "type": "subscription_confirmed",
                    "channels": channels,
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message_type == "unsubscribe":
                channels = data.get("channels", [])
                self.subscription_manager.unsubscribe(websocket, channels)
                await websocket.send(json.dumps({
                    "type": "unsubscription_confirmed",
                    "channels": channels,
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message_type == "ping":
                await websocket.send(json.dumps({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message_type == "query":
                # Handle real-time queries
                await self.handle_query(websocket, data)
            
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Invalid JSON format",
                "timestamp": datetime.now().isoformat()
            }))
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
            await websocket.send(json.dumps({
                "type": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }))
    
    async def handle_query(self, websocket: WebSocketServerProtocol, query_data: Dict[str, Any]):
        """Handle real-time intelligence queries"""
        query_type = query_data.get("query_type")
        domain = query_data.get("domain")
        
        if query_type == "latest_insights":
            # Get latest insights for domain
            insights = await self.get_latest_insights(domain)
            await websocket.send(json.dumps({
                "type": "query_response",
                "query_type": query_type,
                "domain": domain,
                "data": insights,
                "timestamp": datetime.now().isoformat()
            }))
        
        elif query_type == "risk_status":
            # Get current risk status
            risks = await self.get_risk_status(domain)
            await websocket.send(json.dumps({
                "type": "query_response",
                "query_type": query_type,
                "domain": domain,
                "data": risks,
                "timestamp": datetime.now().isoformat()
            }))
    
    async def client_handler(self, websocket: WebSocketServerProtocol, path: str):
        """Handle client connections"""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                await self.handle_client_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    async def broadcast_update(self, update: IntelligenceUpdate):
        """Broadcast update to relevant subscribers"""
        # Determine channels for this update
        channels = ["all", update.domain]
        
        if update.update_type in [UpdateType.RISK_ALERT, UpdateType.OPPORTUNITY_ALERT]:
            channels.append("alerts")
        
        if update.update_type == UpdateType.CROSS_DOMAIN_INSIGHT:
            channels.append("insights")
        
        # Get subscribers
        subscribers = self.subscription_manager.get_subscribers(channels)
        
        if subscribers:
            message = json.dumps({
                "type": "intelligence_update",
                "update_type": update.update_type.value,
                "domain": update.domain,
                "timestamp": update.timestamp,
                "priority": update.priority,
                "confidence": update.confidence,
                "data": update.data
            })
            
            # Broadcast to all subscribers
            disconnected = set()
            for client in subscribers:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(client)
            
            # Clean up disconnected clients
            for client in disconnected:
                await self.unregister_client(client)
    
    async def update_processor(self):
        """Process updates from queue and broadcast"""
        while True:
            try:
                update = await self.update_queue.get()
                await self.broadcast_update(update)
            except Exception as e:
                self.logger.error(f"Error processing update: {e}")
            await asyncio.sleep(0.1)
    
    async def watch_analysis_outputs(self):
        """Watch T2 analysis outputs for updates"""
        analysis_dir = Path("/Users/fernandox/Desktop/Core Agent Architecture/shared_state/t2_analysis")
        last_modified = {}
        
        while True:
            try:
                # Check for new or modified files
                for file_path in analysis_dir.glob("*_analysis_*.json"):
                    mtime = file_path.stat().st_mtime
                    
                    if file_path.name not in last_modified or mtime > last_modified[file_path.name]:
                        last_modified[file_path.name] = mtime
                        
                        # Read and process update
                        async with aiofiles.open(file_path, 'r') as f:
                            content = await f.read()
                            data = json.loads(content)
                        
                        # Create update
                        domain = data.get("domain", "unknown")
                        update = IntelligenceUpdate(
                            update_type=UpdateType.ANALYSIS_COMPLETE,
                            domain=domain,
                            timestamp=data.get("timestamp", datetime.now().isoformat()),
                            data={
                                "confidence_score": data.get("confidence_score", 0),
                                "key_findings": data.get("key_findings", [])[:3],
                                "top_opportunity": data.get("opportunities", [{}])[0] if data.get("opportunities") else None,
                                "metrics": data.get("metrics", {})
                            },
                            confidence=data.get("confidence_score", 0)
                        )
                        
                        await self.update_queue.put(update)
                        
                        # Check for alerts
                        await self.check_for_alerts(data)
                
            except Exception as e:
                self.logger.error(f"Error watching files: {e}")
            
            await asyncio.sleep(5)  # Check every 5 seconds
    
    async def check_for_alerts(self, analysis_data: Dict[str, Any]):
        """Check analysis data for risk/opportunity alerts"""
        domain = analysis_data.get("domain", "unknown")
        
        # Check for high-severity risks
        risks = analysis_data.get("risks", [])
        for risk in risks:
            if risk.get("severity") in ["high", "critical"]:
                alert = IntelligenceUpdate(
                    update_type=UpdateType.RISK_ALERT,
                    domain=domain,
                    timestamp=datetime.now().isoformat(),
                    data=risk,
                    priority="high",
                    confidence=analysis_data.get("confidence_score", 0)
                )
                await self.update_queue.put(alert)
        
        # Check for high-potential opportunities
        opportunities = analysis_data.get("opportunities", [])
        for opp in opportunities:
            if opp.get("potential") == "high":
                alert = IntelligenceUpdate(
                    update_type=UpdateType.OPPORTUNITY_ALERT,
                    domain=domain,
                    timestamp=datetime.now().isoformat(),
                    data=opp,
                    priority="high",
                    confidence=analysis_data.get("confidence_score", 0)
                )
                await self.update_queue.put(alert)
    
    async def simulate_real_time_updates(self):
        """Simulate real-time updates for testing"""
        domains = ["market", "neighborhood", "financial", "environmental", "regulatory", "technology"]
        
        while True:
            # Simulate metric changes
            domain = domains[int(datetime.now().timestamp()) % len(domains)]
            
            update = IntelligenceUpdate(
                update_type=UpdateType.METRIC_CHANGE,
                domain=domain,
                timestamp=datetime.now().isoformat(),
                data={
                    "metric": "market_activity",
                    "previous_value": 100,
                    "current_value": 100 + (hash(datetime.now().isoformat()) % 20 - 10),
                    "change_percentage": (hash(datetime.now().isoformat()) % 20 - 10) / 100
                },
                confidence=0.95
            )
            
            await self.update_queue.put(update)
            await asyncio.sleep(30)  # Update every 30 seconds
    
    async def get_latest_insights(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """Get latest insights for domain"""
        # In production, this would query the actual analysis results
        return {
            "domain": domain or "all",
            "latest_update": datetime.now().isoformat(),
            "insights": [
                f"Latest insight for {domain or 'all domains'}",
                "Market conditions remain favorable",
                "New opportunities identified"
            ]
        }
    
    async def get_risk_status(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """Get current risk status"""
        return {
            "domain": domain or "all",
            "risk_level": "medium",
            "active_risks": 3,
            "mitigated_risks": 5,
            "risk_trend": "decreasing"
        }
    
    async def start_server(self):
        """Start WebSocket server"""
        self.logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
        
        # Start background tasks
        asyncio.create_task(self.update_processor())
        asyncio.create_task(self.watch_analysis_outputs())
        asyncio.create_task(self.simulate_real_time_updates())
        
        # Start WebSocket server
        async with websockets.serve(self.client_handler, self.host, self.port):
            self.logger.info("WebSocket server started successfully")
            await asyncio.Future()  # Run forever


# WebSocket client example
class HoustonIntelligenceClient:
    """Example WebSocket client for testing"""
    
    def __init__(self, uri: str = "ws://localhost:8765"):
        self.uri = uri
    
    async def connect_and_subscribe(self):
        """Connect to server and subscribe to updates"""
        async with websockets.connect(self.uri) as websocket:
            print("Connected to Houston Intelligence WebSocket")
            
            # Subscribe to channels
            await websocket.send(json.dumps({
                "type": "subscribe",
                "channels": ["all", "alerts", "market", "financial"]
            }))
            
            # Listen for updates
            async for message in websocket:
                data = json.loads(message)
                print(f"Received: {data.get('type')} - {data.get('domain', 'N/A')}")
                
                if data.get("type") == "intelligence_update":
                    print(f"  Update Type: {data.get('update_type')}")
                    print(f"  Confidence: {data.get('confidence', 0):.2%}")
                    print(f"  Data: {json.dumps(data.get('data', {}), indent=2)}")


if __name__ == "__main__":
    # Start server
    server = HoustonIntelligenceWebSocket()
    asyncio.run(server.start_server())