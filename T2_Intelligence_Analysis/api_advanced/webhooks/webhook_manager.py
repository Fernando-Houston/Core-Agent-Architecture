"""
Webhook Notification System for Houston Intelligence Platform
Manages webhook subscriptions and sends notifications on data updates
"""

import asyncio
import json
import logging
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
import aiohttp
from aiohttp import ClientTimeout
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from pydantic import BaseModel, HttpUrl, Field
import redis.asyncio as redis
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import uuid


# Webhook Event Types
class WebhookEventType(Enum):
    """Types of webhook events"""
    ANALYSIS_COMPLETE = "analysis.complete"
    DOMAIN_UPDATE = "domain.update"
    CROSS_DOMAIN_INSIGHT = "cross_domain.insight"
    RISK_ALERT = "risk.alert"
    OPPORTUNITY_ALERT = "opportunity.alert"
    BATCH_COMPLETE = "batch.complete"
    THRESHOLD_EXCEEDED = "threshold.exceeded"
    MARKET_CHANGE = "market.change"
    CUSTOM = "custom"


# Database Models
Base = declarative_base()


class WebhookSubscription(Base):
    """Webhook subscription model"""
    __tablename__ = "webhook_subscriptions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    events = Column(JSON, nullable=False)  # List of event types
    domains = Column(JSON, nullable=True)  # Optional domain filter
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_triggered = Column(DateTime, nullable=True)
    failure_count = Column(Integer, default=0)
    extra_metadata = Column(JSON, nullable=True)


# Pydantic Models
class WebhookConfig(BaseModel):
    """Webhook configuration"""
    url: HttpUrl
    events: List[WebhookEventType]
    domains: Optional[List[str]] = None
    secret: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Optional[Dict[str, Any]] = None


class WebhookEvent(BaseModel):
    """Webhook event payload"""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: WebhookEventType
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    domain: Optional[str] = None
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class WebhookDelivery(BaseModel):
    """Webhook delivery record"""
    delivery_id: str
    subscription_id: str
    event_id: str
    url: str
    status: str  # pending, success, failed
    attempts: int = 0
    last_attempt: Optional[str] = None
    response_code: Optional[int] = None
    error: Optional[str] = None


@dataclass
class WebhookQueueItem:
    """Item in webhook delivery queue"""
    subscription: WebhookSubscription
    event: WebhookEvent
    retry_count: int = 0
    next_retry: datetime = field(default_factory=datetime.now)


class WebhookManager:
    """Manages webhook subscriptions and deliveries"""
    
    def __init__(
        self,
        database_url: str = "sqlite:///webhooks.db",
        redis_url: str = "redis://localhost:6379",
        max_retries: int = 3,
        timeout_seconds: int = 30
    ):
        self.database_url = database_url
        self.redis_url = redis_url
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        
        # Setup database
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("WebhookManager")
        
        # Delivery queue
        self.delivery_queue: asyncio.Queue = asyncio.Queue()
        self.active_deliveries: Set[str] = set()
        
        # Redis for caching and rate limiting
        self.redis_client: Optional[redis.Redis] = None
    
    async def initialize(self):
        """Initialize webhook manager"""
        # Connect to Redis
        try:
            self.redis_client = await redis.from_url(self.redis_url)
            await self.redis_client.ping()
            self.logger.info("Connected to Redis")
        except Exception as e:
            self.logger.warning(f"Redis connection failed: {e}. Using in-memory fallback.")
            self.redis_client = None
        
        # Start delivery workers
        for i in range(5):  # 5 concurrent delivery workers
            asyncio.create_task(self._delivery_worker(i))
        
        self.logger.info("Webhook manager initialized")
    
    async def subscribe(self, config: WebhookConfig) -> str:
        """Create a new webhook subscription"""
        with self.SessionLocal() as session:
            subscription = WebhookSubscription(
                url=str(config.url),
                secret=config.secret,
                events=[e.value for e in config.events],
                domains=config.domains,
                extra_metadata=config.metadata
            )
            
            session.add(subscription)
            session.commit()
            
            self.logger.info(f"Created webhook subscription: {subscription.id}")
            return subscription.id
    
    async def unsubscribe(self, subscription_id: str) -> bool:
        """Remove a webhook subscription"""
        with self.SessionLocal() as session:
            subscription = session.query(WebhookSubscription).filter_by(
                id=subscription_id
            ).first()
            
            if subscription:
                subscription.active = False
                session.commit()
                self.logger.info(f"Deactivated webhook subscription: {subscription_id}")
                return True
            
            return False
    
    async def list_subscriptions(
        self,
        active_only: bool = True,
        event_type: Optional[WebhookEventType] = None
    ) -> List[Dict[str, Any]]:
        """List webhook subscriptions"""
        with self.SessionLocal() as session:
            query = session.query(WebhookSubscription)
            
            if active_only:
                query = query.filter_by(active=True)
            
            subscriptions = query.all()
            
            results = []
            for sub in subscriptions:
                if event_type and event_type.value not in sub.events:
                    continue
                
                results.append({
                    "id": sub.id,
                    "url": sub.url,
                    "events": sub.events,
                    "domains": sub.domains,
                    "active": sub.active,
                    "created_at": sub.created_at.isoformat(),
                    "last_triggered": sub.last_triggered.isoformat() if sub.last_triggered else None,
                    "failure_count": sub.failure_count
                })
            
            return results
    
    async def trigger_event(self, event: WebhookEvent):
        """Trigger webhook event for all matching subscriptions"""
        with self.SessionLocal() as session:
            # Find matching subscriptions
            subscriptions = session.query(WebhookSubscription).filter_by(
                active=True
            ).all()
            
            triggered_count = 0
            
            for subscription in subscriptions:
                # Check if subscription matches event
                if event.event_type.value not in subscription.events:
                    continue
                
                # Check domain filter
                if subscription.domains and event.domain:
                    if event.domain not in subscription.domains:
                        continue
                
                # Queue for delivery
                queue_item = WebhookQueueItem(
                    subscription=subscription,
                    event=event
                )
                
                await self.delivery_queue.put(queue_item)
                triggered_count += 1
            
            self.logger.info(
                f"Triggered {triggered_count} webhooks for event {event.event_type.value}"
            )
    
    async def _delivery_worker(self, worker_id: int):
        """Worker to process webhook deliveries"""
        self.logger.info(f"Delivery worker {worker_id} started")
        
        while True:
            try:
                # Get item from queue
                item: WebhookQueueItem = await self.delivery_queue.get()
                
                # Check if we should wait before retry
                if item.next_retry > datetime.now():
                    wait_time = (item.next_retry - datetime.now()).total_seconds()
                    await asyncio.sleep(wait_time)
                
                # Deliver webhook
                success = await self._deliver_webhook(item)
                
                if not success and item.retry_count < self.max_retries:
                    # Schedule retry with exponential backoff
                    item.retry_count += 1
                    item.next_retry = datetime.now() + timedelta(
                        seconds=2 ** item.retry_count * 10
                    )
                    await self.delivery_queue.put(item)
                elif not success:
                    # Max retries exceeded
                    await self._handle_delivery_failure(item)
                
            except Exception as e:
                self.logger.error(f"Delivery worker {worker_id} error: {e}")
                await asyncio.sleep(1)
    
    async def _deliver_webhook(self, item: WebhookQueueItem) -> bool:
        """Deliver a single webhook"""
        subscription = item.subscription
        event = item.event
        
        # Prepare payload
        payload = {
            "event": event.dict(),
            "subscription_id": subscription.id,
            "delivery_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate signature
        signature = self._generate_signature(
            json.dumps(payload, sort_keys=True),
            subscription.secret
        )
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
            "X-Webhook-Event": event.event_type.value,
            "X-Webhook-Delivery-ID": payload["delivery_id"]
        }
        
        # Attempt delivery
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    subscription.url,
                    json=payload,
                    headers=headers,
                    timeout=ClientTimeout(total=self.timeout_seconds)
                ) as response:
                    success = 200 <= response.status < 300
                    
                    if success:
                        self.logger.info(
                            f"Successfully delivered webhook to {subscription.url}"
                        )
                        await self._update_subscription_success(subscription.id)
                    else:
                        self.logger.warning(
                            f"Webhook delivery failed with status {response.status}"
                        )
                        await self._update_subscription_failure(subscription.id)
                    
                    # Store delivery record
                    await self._store_delivery_record(
                        payload["delivery_id"],
                        subscription.id,
                        event.event_id,
                        response.status,
                        success
                    )
                    
                    return success
                    
        except asyncio.TimeoutError:
            self.logger.error(f"Webhook delivery timeout for {subscription.url}")
            await self._update_subscription_failure(subscription.id)
            return False
        except Exception as e:
            self.logger.error(f"Webhook delivery error: {e}")
            await self._update_subscription_failure(subscription.id)
            return False
    
    def _generate_signature(self, payload: str, secret: str) -> str:
        """Generate HMAC signature for webhook payload"""
        return hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    async def _update_subscription_success(self, subscription_id: str):
        """Update subscription after successful delivery"""
        with self.SessionLocal() as session:
            subscription = session.query(WebhookSubscription).filter_by(
                id=subscription_id
            ).first()
            
            if subscription:
                subscription.last_triggered = datetime.utcnow()
                subscription.failure_count = 0
                session.commit()
    
    async def _update_subscription_failure(self, subscription_id: str):
        """Update subscription after failed delivery"""
        with self.SessionLocal() as session:
            subscription = session.query(WebhookSubscription).filter_by(
                id=subscription_id
            ).first()
            
            if subscription:
                subscription.failure_count += 1
                
                # Disable subscription after too many failures
                if subscription.failure_count >= 10:
                    subscription.active = False
                    self.logger.warning(
                        f"Disabled subscription {subscription_id} due to repeated failures"
                    )
                
                session.commit()
    
    async def _handle_delivery_failure(self, item: WebhookQueueItem):
        """Handle final delivery failure"""
        self.logger.error(
            f"Webhook delivery failed after {self.max_retries} retries: "
            f"{item.subscription.url}"
        )
        
        # Could send email notification, store in dead letter queue, etc.
    
    async def _store_delivery_record(
        self,
        delivery_id: str,
        subscription_id: str,
        event_id: str,
        status_code: int,
        success: bool
    ):
        """Store webhook delivery record"""
        if self.redis_client:
            # Store in Redis with TTL
            key = f"webhook:delivery:{delivery_id}"
            record = {
                "delivery_id": delivery_id,
                "subscription_id": subscription_id,
                "event_id": event_id,
                "status_code": status_code,
                "success": success,
                "timestamp": datetime.now().isoformat()
            }
            
            await self.redis_client.setex(
                key,
                86400 * 7,  # 7 days TTL
                json.dumps(record)
            )
    
    async def get_delivery_history(
        self,
        subscription_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get webhook delivery history"""
        if not self.redis_client:
            return []
        
        # Scan for delivery records
        history = []
        pattern = f"webhook:delivery:*"
        
        async for key in self.redis_client.scan_iter(match=pattern, count=1000):
            record_data = await self.redis_client.get(key)
            if record_data:
                record = json.loads(record_data)
                
                if subscription_id and record["subscription_id"] != subscription_id:
                    continue
                
                history.append(record)
                
                if len(history) >= limit:
                    break
        
        # Sort by timestamp
        history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return history[:limit]
    
    async def test_webhook(self, subscription_id: str) -> Dict[str, Any]:
        """Send test webhook to verify configuration"""
        with self.SessionLocal() as session:
            subscription = session.query(WebhookSubscription).filter_by(
                id=subscription_id,
                active=True
            ).first()
            
            if not subscription:
                raise ValueError("Subscription not found or inactive")
            
            # Create test event
            test_event = WebhookEvent(
                event_type=WebhookEventType.CUSTOM,
                data={
                    "test": True,
                    "message": "This is a test webhook delivery",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            # Deliver immediately
            item = WebhookQueueItem(
                subscription=subscription,
                event=test_event
            )
            
            success = await self._deliver_webhook(item)
            
            return {
                "success": success,
                "subscription_id": subscription_id,
                "url": subscription.url,
                "event": test_event.dict()
            }


# Event Monitoring Service
class EventMonitor:
    """Monitors T2 analysis outputs and triggers webhook events"""
    
    def __init__(self, webhook_manager: WebhookManager):
        self.webhook_manager = webhook_manager
        self.monitored_files: Dict[str, float] = {}
        self.running = False
        
    async def start_monitoring(self):
        """Start monitoring for events"""
        self.running = True
        
        # Monitor different sources
        asyncio.create_task(self._monitor_analysis_files())
        asyncio.create_task(self._monitor_thresholds())
        asyncio.create_task(self._monitor_batch_jobs())
        
        logging.info("Event monitoring started")
    
    async def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
    
    async def _monitor_analysis_files(self):
        """Monitor T2 analysis output files"""
        analysis_dir = Path("/Users/fernandox/Desktop/Core Agent Architecture/shared_state/t2_analysis")
        
        while self.running:
            try:
                # Check for new or updated files
                for file_path in analysis_dir.glob("*_analysis_*.json"):
                    mtime = file_path.stat().st_mtime
                    
                    if (file_path.name not in self.monitored_files or 
                        mtime > self.monitored_files[file_path.name]):
                        
                        self.monitored_files[file_path.name] = mtime
                        
                        # Read analysis data
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        # Trigger analysis complete event
                        event = WebhookEvent(
                            event_type=WebhookEventType.ANALYSIS_COMPLETE,
                            domain=data.get("domain"),
                            data={
                                "domain": data.get("domain"),
                                "confidence_score": data.get("confidence_score"),
                                "key_findings": data.get("key_findings", [])[:3],
                                "timestamp": data.get("timestamp")
                            }
                        )
                        
                        await self.webhook_manager.trigger_event(event)
                        
                        # Check for alerts
                        await self._check_for_alerts(data)
                
            except Exception as e:
                logging.error(f"Error monitoring analysis files: {e}")
            
            await asyncio.sleep(10)  # Check every 10 seconds
    
    async def _check_for_alerts(self, analysis_data: Dict[str, Any]):
        """Check for risk and opportunity alerts"""
        domain = analysis_data.get("domain")
        
        # Check risks
        for risk in analysis_data.get("risks", []):
            if risk.get("severity") in ["high", "critical"]:
                event = WebhookEvent(
                    event_type=WebhookEventType.RISK_ALERT,
                    domain=domain,
                    data={
                        "risk": risk,
                        "domain": domain,
                        "severity": risk.get("severity"),
                        "confidence": analysis_data.get("confidence_score")
                    }
                )
                await self.webhook_manager.trigger_event(event)
        
        # Check opportunities
        for opportunity in analysis_data.get("opportunities", []):
            if opportunity.get("potential") == "high":
                event = WebhookEvent(
                    event_type=WebhookEventType.OPPORTUNITY_ALERT,
                    domain=domain,
                    data={
                        "opportunity": opportunity,
                        "domain": domain,
                        "potential": opportunity.get("potential"),
                        "confidence": analysis_data.get("confidence_score")
                    }
                )
                await self.webhook_manager.trigger_event(event)
    
    async def _monitor_thresholds(self):
        """Monitor for threshold breaches"""
        # Example thresholds
        thresholds = {
            "avg_price_per_sqft": {"max": 400, "min": 200},
            "roi": {"min": 15},
            "risk_score": {"max": 7}
        }
        
        while self.running:
            # Check current metrics against thresholds
            # This would read from actual analysis results
            await asyncio.sleep(60)  # Check every minute
    
    async def _monitor_batch_jobs(self):
        """Monitor batch processing completion"""
        # Would integrate with batch processor
        while self.running:
            await asyncio.sleep(30)


# FastAPI Application
app = FastAPI(title="Houston Intelligence Webhook API")

# Global webhook manager
webhook_manager = WebhookManager()
event_monitor = EventMonitor(webhook_manager)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await webhook_manager.initialize()
    await event_monitor.start_monitoring()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await event_monitor.stop_monitoring()


@app.post("/webhooks/subscribe")
async def subscribe_webhook(config: WebhookConfig) -> Dict[str, str]:
    """Subscribe to webhook notifications"""
    subscription_id = await webhook_manager.subscribe(config)
    return {"subscription_id": subscription_id}


@app.delete("/webhooks/{subscription_id}")
async def unsubscribe_webhook(subscription_id: str):
    """Unsubscribe from webhook notifications"""
    success = await webhook_manager.unsubscribe(subscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"status": "unsubscribed"}


@app.get("/webhooks")
async def list_webhooks(
    active_only: bool = True,
    event_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """List webhook subscriptions"""
    event_type_enum = WebhookEventType(event_type) if event_type else None
    return await webhook_manager.list_subscriptions(active_only, event_type_enum)


@app.post("/webhooks/{subscription_id}/test")
async def test_webhook(subscription_id: str):
    """Send test webhook"""
    try:
        result = await webhook_manager.test_webhook(subscription_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/webhooks/{subscription_id}/history")
async def get_webhook_history(subscription_id: str, limit: int = 100):
    """Get webhook delivery history"""
    return await webhook_manager.get_delivery_history(subscription_id, limit)


@app.post("/webhooks/trigger")
async def trigger_webhook_event(event: WebhookEvent):
    """Manually trigger a webhook event"""
    await webhook_manager.trigger_event(event)
    return {"status": "triggered"}


# Webhook receiver endpoint for testing
@app.post("/webhook-receiver")
async def receive_webhook(
    payload: Dict[str, Any],
    x_webhook_signature: Optional[str] = Header(None),
    x_webhook_event: Optional[str] = Header(None)
):
    """Example webhook receiver endpoint"""
    logging.info(f"Received webhook: {x_webhook_event}")
    logging.info(f"Payload: {json.dumps(payload, indent=2)}")
    
    # Verify signature if needed
    # ...
    
    return {"status": "received"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)