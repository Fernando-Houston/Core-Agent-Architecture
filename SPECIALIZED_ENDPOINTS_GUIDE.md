# Houston Intelligence Platform - Specialized Endpoints Guide

## 🎯 Purpose-Built Endpoints

The specialized endpoints provide targeted access to specific intelligence domains within the Houston real estate market.

## 📋 Available Endpoints

### 1. Active Developments
```http
GET /api/v1/developments/active
```
Returns all active development projects with details on type, location, developer, and estimated values.

**Example Response:**
```json
{
  "developments": [{
    "name": "East River Mixed-Use",
    "type": "mixed-use",
    "location": "Downtown Houston",
    "developer": "Hines",
    "estimated_value": "$500M",
    "completion_date": "2026-Q2"
  }]
}
```

### 2. Neighborhood Analysis
```http
GET /api/v1/neighborhoods/{neighborhood_name}
```
Get comprehensive analysis for specific neighborhoods.

**Example:**
```bash
curl http://localhost:5000/api/v1/neighborhoods/Houston%20Heights
```

### 3. Recent Permits
```http
GET /api/v1/permits/recent?type=residential&area=Sugar%20Land&limit=20
```
Filter recent building permits by type and area.

**Query Parameters:**
- `type`: residential, commercial, industrial, or all
- `area`: specific area or neighborhood
- `limit`: max results (default: 50)

### 4. Market Trends
```http
GET /api/v1/market/trends
```
Current market trends and projections for residential, commercial, and industrial sectors.

### 5. Investment Opportunities
```http
POST /api/v1/opportunities/investment
```
Find opportunities matching specific investment criteria.

**Request Body:**
```json
{
  "budget_min": 1000000,
  "budget_max": 5000000,
  "property_types": ["mixed-use", "residential"],
  "areas": ["Downtown", "Midtown"],
  "min_roi": 15
}
```

### 6. Risk Assessment
```http
POST /api/v1/risks/assessment
```
Assess environmental, regulatory, and market risks for a location.

**Request Body:**
```json
{
  "location": "Sugar Land",
  "project_type": "residential"
}
```

### 7. Top Developers
```http
GET /api/v1/developers/top?limit=10
```
Get top developers by permit activity and market share.

### 8. Technology Innovations
```http
GET /api/v1/technology/innovations
```
Discover PropTech and construction technology opportunities.

## 🚀 Quick Examples

### Find High-ROI Investments
```bash
curl -X POST http://localhost:5000/api/v1/opportunities/investment \
  -H "Content-Type: application/json" \
  -d '{
    "budget_max": 10000000,
    "min_roi": 20,
    "property_types": ["mixed-use"]
  }'
```

### Check Flood Risk
```bash
curl -X POST http://localhost:5000/api/v1/risks/assessment \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Houston Heights",
    "project_type": "residential"
  }'
```

### Track Market Activity
```bash
# Get recent commercial permits
curl "http://localhost:5000/api/v1/permits/recent?type=commercial&limit=10"

# Check market trends
curl http://localhost:5000/api/v1/market/trends
```

## 📊 Response Formats

All endpoints return consistent JSON responses:

```json
{
  "status": "success|error",
  "timestamp": "2025-01-10T12:00:00Z",
  "data": {
    // Endpoint-specific data
  }
}
```

## 🔧 Integration Example

```javascript
// JavaScript/React example
async function findInvestments() {
  const response = await fetch('/api/v1/opportunities/investment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      budget_min: 2000000,
      budget_max: 8000000,
      areas: ['Midtown', 'River Oaks'],
      min_roi: 18
    })
  });
  
  const data = await response.json();
  return data.opportunities;
}
```

## 🛡️ Rate Limits

- General endpoints: 200/day, 50/hour
- Search endpoints: 20/minute
- Query endpoints: 10/minute

## 📈 Performance Tips

1. **Use specific filters** to reduce response size
2. **Cache responses** for data that doesn't change frequently
3. **Batch similar requests** when possible
4. **Monitor rate limits** in response headers

## 🆘 Troubleshooting

- **Empty results**: Check if agents have been populated with data
- **500 errors**: Verify knowledge files exist in agent folders
- **Rate limits**: Implement exponential backoff
- **CORS issues**: Ensure origin is whitelisted

---

These specialized endpoints provide direct access to Houston real estate intelligence without needing to craft complex queries.