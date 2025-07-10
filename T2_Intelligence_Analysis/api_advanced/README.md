# Houston Intelligence Platform - Advanced API Features

## Overview

The Houston Intelligence Platform now includes advanced API capabilities that enable real-time updates, batch processing, flexible querying, and automated notifications. These features work seamlessly with the T2 Intelligence Analysis Engine to provide a comprehensive development intelligence solution.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Houston Intelligence Platform              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  WebSocket  │  │    Batch     │  │    GraphQL      │  │
│  │  Real-time  │  │  Processing  │  │   Flexible      │  │
│  │   Updates   │  │   Engine     │  │   Queries       │  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬────────┘  │
│         │                 │                    │           │
│         └─────────────────┴────────────────────┘          │
│                           │                                │
│                    ┌──────┴───────┐                       │
│                    │  Integrated  │                       │
│                    │     API      │                       │
│                    └──────┬───────┘                       │
│                           │                                │
│         ┌─────────────────┴────────────────────┐          │
│         │                                       │          │
│    ┌────┴─────┐                        ┌───────┴──────┐   │
│    │ Webhook  │                        │      T2      │   │
│    │ Manager  │◄───────────────────────┤ Intelligence │   │
│    └──────────┘                        │   Engine     │   │
│                                        └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Features

### 1. WebSocket Real-time Updates

**Purpose**: Provides real-time intelligence updates to connected clients as new analysis completes.

**Key Features**:
- Real-time push notifications
- Channel-based subscriptions
- Automatic reconnection support
- Low-latency updates

**Connection URL**: `ws://localhost:8000/ws`

**Example Usage**:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
    // Subscribe to channels
    ws.send(JSON.stringify({
        type: 'subscribe',
        channels: ['market', 'financial', 'alerts']
    }));
};

ws.onmessage = (event) => {
    const update = JSON.parse(event.data);
    console.log('Intelligence Update:', update);
};
```

**Update Types**:
- `analysis_complete`: New domain analysis completed
- `domain_update`: Domain-specific update
- `risk_alert`: High-severity risk detected
- `opportunity_alert`: High-potential opportunity identified
- `metric_change`: Key metric changed
- `cross_domain_insight`: Cross-domain connection identified

### 2. Batch Processing API

**Purpose**: Process multiple intelligence queries efficiently with parallel execution.

**Key Features**:
- Parallel query execution
- Progress tracking
- Partial results support
- Multiple export formats (JSON, CSV, Excel)
- File upload support

**Endpoints**:
- `POST /batch/submit` - Submit batch queries
- `GET /batch/{batch_id}/status` - Check batch status
- `GET /batch/{batch_id}/export?format=csv` - Export results

**Example Batch Request**:
```json
{
    "queries": [
        {
            "query_type": "domain_analysis",
            "domain": "market",
            "priority": 10
        },
        {
            "query_type": "comparative",
            "parameters": {
                "locations": ["EaDo", "Midtown", "Heights"],
                "metrics": ["roi", "growth", "risk"]
            }
        },
        {
            "query_type": "predictive",
            "domain": "financial",
            "parameters": {
                "horizon": "6_months",
                "scenarios": ["base", "optimistic", "pessimistic"]
            }
        }
    ],
    "parallel_execution": true,
    "max_parallel": 10,
    "callback_url": "https://your-server.com/batch-complete"
}
```

**Query Types**:
- `domain_analysis`: Comprehensive domain analysis
- `cross_domain`: Cross-domain insights
- `comparative`: Compare multiple locations/metrics
- `historical`: Historical trend analysis
- `predictive`: Predictive analytics
- `custom`: Custom queries

### 3. GraphQL API

**Purpose**: Flexible querying with exactly the data you need.

**Key Features**:
- Single endpoint for all queries
- Nested data fetching
- Type safety
- Real-time subscriptions
- Introspection support

**Endpoint**: `/graphql`

**Example Queries**:

```graphql
# Get market snapshot
query MarketSnapshot {
    marketSnapshot {
        overallConfidence
        marketSentiment
        topOpportunities {
            type
            potential
            description
            expectedRoi
        }
        criticalRisks {
            type
            severity
            mitigation
        }
    }
}

# Get specific domain analysis
query DomainAnalysis($domain: String!) {
    domainAnalysis(domain: $domain) {
        confidenceScore
        keyFindings {
            finding
            importance
        }
        opportunities {
            type
            description
            action
        }
    }
}

# Search opportunities
query SearchOpportunities($minRoi: Float) {
    searchOpportunities(minRoi: $minRoi) {
        type
        location
        expectedRoi
        action
    }
}

# Subscribe to updates
subscription IntelligenceUpdates {
    intelligenceUpdates(domains: ["market", "financial"]) {
        updateType
        domain
        timestamp
        data
    }
}
```

### 4. Webhook Notifications

**Purpose**: Push notifications to your servers when events occur.

**Key Features**:
- Event-based notifications
- Secure webhook delivery (HMAC signatures)
- Retry logic with exponential backoff
- Delivery history tracking
- Multiple event subscriptions

**Endpoints**:
- `POST /webhooks/subscribe` - Create webhook subscription
- `GET /webhooks` - List subscriptions
- `DELETE /webhooks/{id}` - Remove subscription
- `POST /webhooks/{id}/test` - Test webhook

**Event Types**:
- `analysis.complete` - Analysis completed for a domain
- `domain.update` - Domain data updated
- `cross_domain.insight` - New cross-domain insight
- `risk.alert` - High-severity risk detected
- `opportunity.alert` - High-potential opportunity
- `batch.complete` - Batch processing completed
- `threshold.exceeded` - Metric threshold exceeded

**Example Webhook Subscription**:
```json
{
    "url": "https://your-server.com/webhook",
    "events": ["analysis.complete", "risk.alert", "opportunity.alert"],
    "domains": ["market", "financial"],
    "secret": "your-webhook-secret"
}
```

**Webhook Payload Example**:
```json
{
    "event": {
        "event_id": "evt_123",
        "event_type": "risk.alert",
        "timestamp": "2025-01-10T10:30:00Z",
        "domain": "environmental",
        "data": {
            "risk": {
                "type": "flood_risk",
                "severity": "high",
                "description": "5 areas in high flood risk zones",
                "mitigation": "Require elevation and enhanced drainage"
            },
            "confidence": 0.92
        }
    },
    "subscription_id": "sub_456",
    "delivery_id": "del_789",
    "timestamp": "2025-01-10T10:30:01Z"
}
```

## Running the Integrated API

### 1. Start the Integrated Server

```bash
cd /Users/fernandox/Desktop/Core\ Agent\ Architecture/T2_Intelligence_Analysis/api_advanced
python integrated_api.py
```

This starts a single server on port 8000 that includes:
- REST API endpoints
- WebSocket server
- GraphQL endpoint
- Batch processing
- Webhook management

### 2. Access Points

- **REST API**: `http://localhost:8000/api/*`
- **WebSocket**: `ws://localhost:8000/ws`
- **GraphQL Playground**: `http://localhost:8000/graphql`
- **API Documentation**: `http://localhost:8000/docs`
- **Demo WebSocket Client**: `http://localhost:8000/demo`

### 3. Authentication

All endpoints require Bearer token authentication:
```
Authorization: Bearer your-api-token
```

## Integration with T2 Intelligence

The advanced API features are fully integrated with the T2 Intelligence Analysis Engine:

1. **Automatic Updates**: When T2 completes analysis, updates are automatically:
   - Broadcast via WebSocket
   - Sent to webhook subscribers
   - Available through GraphQL queries

2. **Batch Processing**: Batch queries can trigger new T2 analyses and aggregate results

3. **Cross-Domain Insights**: The API exposes T2's cross-domain analysis capabilities

4. **Real-time Monitoring**: All T2 outputs are monitored for changes and alerts

## Example Client Applications

### Python WebSocket Client

```python
import asyncio
import websockets
import json

async def houston_client():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        # Subscribe to updates
        await websocket.send(json.dumps({
            "type": "subscribe",
            "channels": ["market", "alerts"]
        }))
        
        # Listen for updates
        async for message in websocket:
            update = json.loads(message)
            print(f"Update: {update}")

asyncio.run(houston_client())
```

### GraphQL Client (Python)

```python
import requests

query = """
    query {
        marketSnapshot {
            overallConfidence
            topOpportunities {
                description
                expectedRoi
            }
        }
    }
"""

response = requests.post(
    "http://localhost:8000/graphql",
    json={"query": query},
    headers={"Authorization": "Bearer your-token"}
)

data = response.json()
print(data)
```

### Webhook Receiver (Flask)

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "your-webhook-secret"

@app.route("/webhook", methods=["POST"])
def receive_webhook():
    # Verify signature
    signature = request.headers.get("X-Webhook-Signature")
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        request.data,
        hashlib.sha256
    ).hexdigest()
    
    if signature != expected:
        return "Unauthorized", 401
    
    # Process webhook
    data = request.json
    event_type = data["event"]["event_type"]
    
    if event_type == "risk.alert":
        # Handle risk alert
        print(f"Risk Alert: {data['event']['data']}")
    
    return "OK", 200
```

## Performance Considerations

1. **WebSocket Connections**: Supports 1000+ concurrent connections
2. **Batch Processing**: Can handle 100+ queries in parallel
3. **Webhook Delivery**: Processes 1000+ webhooks/minute
4. **GraphQL**: Optimized resolvers with caching

## Security Best Practices

1. **Authentication**: Always use Bearer tokens in production
2. **HTTPS**: Deploy behind HTTPS in production
3. **Webhook Signatures**: Verify HMAC signatures on webhook receipts
4. **Rate Limiting**: Implement rate limiting for public APIs
5. **CORS**: Configure CORS appropriately for your domains

## Monitoring and Debugging

1. **Health Check**: `GET /api/status`
2. **Metrics**: Monitor active connections, queue sizes, processing times
3. **Logs**: Check application logs for errors and performance data
4. **Webhook History**: `GET /webhooks/{id}/history`

## Next Steps

1. Deploy to production environment
2. Set up monitoring and alerting
3. Configure auto-scaling for high load
4. Implement additional security measures
5. Create SDKs for common languages

---

The Houston Intelligence Platform's advanced API features provide a comprehensive toolkit for building sophisticated real estate intelligence applications with real-time capabilities, efficient batch processing, flexible querying, and automated notifications.