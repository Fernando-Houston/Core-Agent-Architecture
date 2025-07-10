# Houston Intelligence Platform - Deployment Guide

## 🚂 Railway Deployment

### Prerequisites
1. Create account at [railway.app](https://railway.app)
2. Install Railway CLI: `npm install -g @railway/cli`

### Deployment Steps

1. **Initialize Railway Project**
```bash
cd "/Users/fernandox/Desktop/Core Agent Architecture"
railway login
railway init
```

2. **Set Environment Variables**
```bash
railway variables set PERPLEXITY_API_KEY=your-api-key-here
railway variables set FLASK_ENV=production
railway variables set PORT=5000
```

3. **Deploy**
```bash
railway up
```

Your API will be available at: `https://your-app.railway.app`

## 💰 Data Source Costs

### Free Data Sources
- **Houston Open Data Portal**: permits, demographics, city planning
- **HCAD**: Property assessments and ownership
- **Census API**: Population and economic data
- **OpenStreetMap**: Geographic data

### Paid Data Sources (Optional)
- **MLS Access**: $100-500/month for agent access
- **CoStar**: $300-1500/month for commercial data
- **Perplexity API**: $20/month for 1000 requests

## 🔗 Perplexity API Setup

1. **Get API Key**
   - Sign up at [perplexity.ai](https://perplexity.ai)
   - Navigate to API settings
   - Generate API key

2. **Add to Environment**
```bash
export PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxxx"
```

3. **Test Integration**
```python
from perplexity_integration import PerplexityClient

client = PerplexityClient()
result = client.get_daily_updates()
print(result)
```

## 📊 Free Real-Time Data Integration

### Houston Open Data
```python
# Free permit data
import requests

def get_houston_permits():
    url = "https://data.houstontx.gov/resource/building-permits.json"
    params = {
        "$limit": 100,
        "$order": "issued_date DESC"
    }
    response = requests.get(url, params=params)
    return response.json()
```

### HCAD Property Data
```python
# Free property assessments
def get_property_data(address):
    # HCAD provides free property data
    # Implementation depends on their current API
    pass
```

## 🚀 Production Checklist

- [ ] Deploy to Railway
- [ ] Set up custom domain
- [ ] Configure SSL certificate (Railway provides free SSL)
- [ ] Set environment variables
- [ ] Test all endpoints
- [ ] Set up monitoring (Railway provides basic monitoring)
- [ ] Configure backup strategy
- [ ] Document API for website team

## 🔧 Monitoring Setup

Railway provides:
- Deployment logs
- Resource usage metrics
- Crash reporting
- Automatic restarts

For advanced monitoring, consider:
- Sentry for error tracking (free tier available)
- Google Analytics for API usage
- Custom logging to track queries

---

**Estimated Monthly Costs:**
- Railway Hosting: $0-20 (free tier available)
- Perplexity API: $20 (optional)
- Data Sources: $0 (using free sources)
- **Total: $0-40/month**