# Perplexity API Integration Guide

## 🚀 Quick Start

### 1. Get Your API Key
1. Go to [https://www.perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Sign up or login
3. Generate an API key (starts with `pplx-`)
4. Cost: $5/1000 requests or $20/month unlimited

### 2. Set Environment Variable
```bash
# Add to your shell profile (.bashrc, .zshrc, etc)
export PERPLEXITY_API_KEY="pplx-your-key-here"

# Or set it temporarily
export PERPLEXITY_API_KEY="pplx-1234567890abcdef"
```

### 3. Install Required Package
```bash
pip3 install requests
```

### 4. Test Your Integration
```bash
cd "/Users/fernandox/Desktop/Core Agent Architecture"
python3 test_perplexity.py
```

## 📝 API Key Format
- Starts with: `pplx-`
- Length: ~50 characters
- Example: `pplx-1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`

## 🔧 Integration Points

### Daily Refresh Agent
The daily agent will use Perplexity to get:
- Latest building permits
- New MLS listings
- Zoning changes
- Development announcements

### Weekly Refresh Agent
The weekly agent will use Perplexity for:
- Market trend analysis
- Competitive intelligence
- Neighborhood rankings
- Investment opportunities

### Monthly Refresh Agent
The monthly agent will use Perplexity for:
- Deep market research
- Long-term projections
- Comprehensive area analysis
- Strategic insights

## 💰 Cost Analysis

### Option 1: Pay-as-you-go
- $5 per 1000 requests
- Good for testing
- ~200 requests/day = $1/day

### Option 2: Pro Plan (Recommended)
- $20/month unlimited
- Best value for production
- Includes all models

## 🧪 Test Queries

### Permits & Development
```
"Houston building permits issued this week over $1 million"
"Major development projects announced Houston 2025"
"Houston zoning changes approved January 2025"
```

### Market Intelligence
```
"Houston Heights real estate market analysis median price inventory"
"Top Houston neighborhoods for investment 2025 ROI"
"Houston commercial real estate vacancy rates by area"
```

### Property Research
```
"Property history and ownership 123 Main St Houston TX"
"Recent home sales River Oaks Houston price per square foot"
"Houston luxury home market trends 2025"
```

## ⚡ Performance Tips

1. **Cache Responses**: Same query within 24 hours? Use cached data
2. **Batch Queries**: Combine related questions
3. **Specific Queries**: More specific = better results
4. **Include Timeframe**: Always specify "2025" or "current"

## 🔍 Response Format

Perplexity returns:
```json
{
  "choices": [{
    "message": {
      "content": "Based on current data..."
    }
  }],
  "citations": [
    {"title": "Source 1", "url": "..."},
    {"title": "Source 2", "url": "..."}
  ]
}
```

## 🚨 Common Issues

### "Invalid API Key"
- Check the key starts with `pplx-`
- Ensure no extra spaces
- Verify key is active in your account

### "Rate Limit Exceeded"
- Pro plan: Should not happen
- Free tier: Wait 60 seconds
- Consider upgrading to Pro

### "No Results Found"
- Make query more specific
- Add "Houston Texas" to query
- Include year "2025"

## 📊 Integration Status

- ✅ Client class implemented
- ✅ Search function ready
- ✅ Daily updates function
- ✅ Market analysis function
- ⏳ Needs: API key configuration
- ⏳ Needs: Response parsing for structured data