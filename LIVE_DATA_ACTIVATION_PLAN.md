# Live Data Activation Plan - Houston Intelligence Platform

## ✅ What We Already Have

1. **Perplexity Integration** (`perplexity_integration.py`)
   - API client ready
   - Search functions implemented
   - Just needs API key

2. **Data Aggregator** (`perplexity_data_replacement.py`)
   - MLS alternative searches
   - Commercial data searches
   - Development intelligence
   - Investment opportunities

3. **Refresh Agents** (daily, weekly, monthly)
   - Currently using simulated data
   - Ready to connect to live sources

4. **API Infrastructure**
   - All endpoints built
   - Rate limiting configured
   - Caching enabled

## 🚀 Activation Steps

### Step 1: Install Dependencies
```bash
pip3 install requests pandas flask flask-cors flask-limiter flask-caching
```

### Step 2: Set API Keys
```bash
# Required (get from perplexity.ai)
export PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxxx"

# Optional (free from census.gov)
export CENSUS_API_KEY="your-census-key"
```

### Step 3: Update Refresh Agents

#### Update `daily_refresh_agent.py`:
Replace the `fetch_permits()` function with:
```python
def fetch_permits(self):
    """Fetch latest building permits using Perplexity"""
    from perplexity_integration import PerplexityClient
    
    self.log("Fetching building permits via Perplexity...")
    
    client = PerplexityClient()
    result = client.search_houston_data(
        "Houston building permits issued this week major projects addresses values",
        "permits"
    )
    
    if result['success']:
        # Extract permit data from response
        content = result['content']
        # Parse content to extract permits
        # Return structured permit list
        return self.parse_permit_content(content)
    
    return []
```

#### Update `weekly_refresh_agent.py`:
Replace market analysis simulation with:
```python
def analyze_market_trends(self):
    """Analyze market trends using Perplexity"""
    from perplexity_data_replacement import PerplexityDataAggregator
    
    aggregator = PerplexityDataAggregator()
    
    # Get MLS alternative data
    neighborhoods = ["Houston Heights", "Montrose", "River Oaks"]
    market_data = {}
    
    for area in neighborhoods:
        market_data[area] = aggregator.get_mls_alternative_data(area)
    
    return market_data
```

### Step 4: Test Live Data

Create `test_live_data.py`:
```python
#!/usr/bin/env python3
from perplexity_integration import PerplexityClient
from perplexity_data_replacement import PerplexityDataAggregator

# Test Perplexity connection
client = PerplexityClient()
result = client.get_daily_updates()
print("Daily Updates:", result)

# Test data aggregation
aggregator = PerplexityDataAggregator()
heights_data = aggregator.get_mls_alternative_data("Houston Heights")
print("\nHouston Heights Data:", heights_data)

# Test investment opportunities
opps = aggregator.get_investment_opportunities({
    "budget": "5 million",
    "type": "mixed-use"
})
print("\nInvestment Opportunities:", opps)
```

### Step 5: Free API Integration

Add these free Houston data sources:

#### Houston Open Data (No Key Required):
```python
# Building Permits
url = "https://data.houstontx.gov/resource/3tts-58vt.json"

# Code Violations  
url = "https://data.houstontx.gov/resource/azmy-mepx.json"

# 311 Service Requests
url = "https://data.houstontx.gov/resource/nskf-3m7d.json"
```

#### HCAD Property Data:
```python
# Public property records
# Web interface: https://public.hcad.org/
# Can search by address, owner name, account number
```

## 📊 Hybrid Data Flow

```
Free APIs (Houston Open Data, HCAD, Census)
    ↓
Combined with Perplexity AI Enhancement ($20/mo)
    ↓
Structured by Refresh Agents
    ↓
Stored in Agent Knowledge Bases
    ↓
Served via REST API
```

## 🔧 Quick Test Commands

```bash
# 1. Test Perplexity
export PERPLEXITY_API_KEY="your-key"
python3 -c "from perplexity_integration import PerplexityClient; print(PerplexityClient().get_daily_updates())"

# 2. Test Houston Open Data (no key needed)
curl "https://data.houstontx.gov/resource/3tts-58vt.json?\$limit=5"

# 3. Run daily refresh with live data
python3 daily_refresh_agent.py

# 4. Start API server
python3 houston_intelligence_api.py
```

## 💡 Benefits of This Approach

1. **Cost**: $20/month vs $1,800/month
2. **Data Quality**: Real-time from multiple sources
3. **Legal**: All public data, no scraping
4. **Scalable**: Add more sources easily
5. **Reliable**: Multiple fallback options

## 🎯 Next Actions

1. Get Perplexity API key
2. Update refresh agents with live data code
3. Test each data source
4. Run full pipeline test
5. Deploy to Railway

This hybrid approach gives you professional-grade data at 1% of the cost!