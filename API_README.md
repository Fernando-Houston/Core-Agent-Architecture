# Houston Intelligence Platform API

A RESTful API for accessing the Houston Development Intelligence system.

## Features

- **Natural Language Queries**: Process complex questions about Houston development
- **Multi-Agent Intelligence**: Access insights from 6 specialized agents
- **Real-time Data**: Get latest market intelligence and development updates
- **Search Capabilities**: Search across all intelligence data
- **Rate Limiting**: Protect against abuse with configurable limits
- **Caching**: Optimize performance with intelligent caching
- **CORS Support**: Enable web frontend integration

## Installation

1. Install required dependencies:
```bash
pip3 install flask flask-cors flask-limiter flask-caching
```

2. Run the API server:
```bash
python3 houston_intelligence_api.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```
Returns server health status.

### Query Intelligence
```
POST /api/v1/query
Content-Type: application/json

{
  "query": "What are the best investment opportunities in Houston?",
  "context": {
    "budget": "5-10M",
    "type": "mixed-use"
  }
}
```
Process natural language queries through the Master Intelligence Agent.

### List Agents
```
GET /api/v1/agents
```
Get list of all available intelligence agents and their capabilities.

### Agent Details
```
GET /api/v1/agent/{agent_name}
```
Get detailed information about a specific agent.

### Latest Insights
```
GET /api/v1/insights/latest
```
Retrieve the most recent insights across all agents.

### Search Intelligence
```
POST /api/v1/search
Content-Type: application/json

{
  "keywords": ["permits", "residential", "2025"],
  "filters": {
    "agents": ["market_intelligence", "regulatory_intelligence"]
  }
}
```
Search across all intelligence data with optional filters.

### Platform Statistics
```
GET /api/v1/stats
```
Get platform metrics and statistics.

## Rate Limits

- Default: 200 requests per day, 50 per hour
- Query endpoint: 10 requests per minute
- Search endpoint: 20 requests per minute

## Response Format

All responses follow this structure:
```json
{
  "status": "success|error",
  "timestamp": "2025-01-10T12:00:00Z",
  "data": {...}
}
```

## Error Handling

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Missing or invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

## Example Usage

### Python
```python
import requests

# Query the intelligence platform
response = requests.post('http://localhost:5000/api/v1/query', 
    json={
        'query': 'What are the top developers in Houston?'
    }
)
data = response.json()
print(data['response'])
```

### JavaScript
```javascript
fetch('http://localhost:5000/api/v1/query', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        query: 'Show me population growth trends'
    })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## Production Deployment

For production deployment:

1. Use a production WSGI server:
```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 houston_intelligence_api:app
```

2. Set up reverse proxy with nginx:
```nginx
server {
    listen 80;
    server_name api.houston-intelligence.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Enable HTTPS with SSL certificates

4. Configure environment variables:
```bash
export FLASK_ENV=production
export API_KEY=your-secret-key
```

## Security Considerations

- API keys for authentication (implement as needed)
- Rate limiting to prevent abuse
- Input validation on all endpoints
- CORS configured for specific domains
- Logging for audit trails

## Performance Optimization

- Response caching (5-60 minutes based on endpoint)
- Database connection pooling
- Asynchronous processing for heavy queries
- CDN for static assets

## Monitoring

The API logs all requests with:
- Request method and path
- Client IP address
- Response status code
- Processing duration

Use these logs for monitoring and debugging.