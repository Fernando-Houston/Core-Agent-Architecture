# Replicate AI Setup for Railway

## 🔑 Environment Variable Required

Add this to your Railway environment variables:

```
REPLICATE_API_TOKEN=your_replicate_api_token_here
```

Note: Your token starts with `r8_` - add it in Railway's environment variables.

## 🚀 Features Enabled

Once you add the token, your Houston Intelligence Platform will have:

### 1. **Llama 2 70B** - Sophisticated Market Analysis
- Complex investment reasoning
- Market trend analysis
- Natural language understanding
- Cost: ~$0.0016 per request

### 2. **BLIP-2** - Property Image Analysis
- Analyze property conditions from photos
- Identify property types and features
- Detect visible issues or concerns
- Cost: ~$0.00025 per question

### 3. **Stable Diffusion** - Development Visualizations
- Generate property development renders
- Visualize "what if" scenarios
- Create marketing materials
- Cost: ~$0.0025 per image

### 4. **Mistral 7B** - Quick Analysis
- Fast investment scoring
- ROI calculations
- Risk assessments
- Cost: ~$0.0002 per request

## 💰 Cost Estimates

- **Per Request**: $0.001 - $0.003
- **1,000 Requests/Month**: ~$2-3
- **10,000 Requests/Month**: ~$20-30

## 📝 Example Queries That Now Work Better

1. "Analyze the investment potential of a $500k property in Houston Heights"
2. "Show me what a modern multifamily development would look like in Midtown"
3. "Analyze this property photo: [image_url]"
4. "Give me sophisticated market analysis for Energy Corridor commercial properties"

## ⚙️ How to Enable in Railway

1. Go to your Railway project
2. Click on Variables
3. Add: `REPLICATE_API_TOKEN` with your token
4. Add: `USE_REPLICATE=true` (optional, defaults to true)
5. Railway will auto-redeploy

Your chat will now provide AI-powered responses instead of "Limited data available"! 🎉