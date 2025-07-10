# Fix for Replicate API Timeout Issue

## Problem Summary
The Replicate API is timing out even though:
- REPLICATE_API_TOKEN is added to Railway
- Payment method is on file at Replicate
- $5 credit is available

The issue is that the current implementation doesn't properly handle:
1. Token validation
2. API timeouts
3. Long-running model predictions

## Root Causes

### 1. **No Timeout Configuration**
The original `replicate.run()` calls don't specify any timeout, causing requests to hang indefinitely.

### 2. **Token Initialization Issue**
The code sets the environment variable with a potentially None value:
```python
self.api_token = api_token or os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = self.api_token  # Could be None!
```

### 3. **Streamlit Timeout Too Short**
The Streamlit interface has a 10-second timeout, but Replicate models can take 30-60 seconds.

## Solution

### Step 1: Replace the Replicate AI Enhancer

Replace `replicate_ai_enhancer.py` with the fixed version (`replicate_ai_enhancer_fixed.py`) that includes:

- Proper token validation
- Timeout handling with model-specific limits
- Retry logic
- Better error messages

```bash
# Backup the original
cp replicate_ai_enhancer.py replicate_ai_enhancer_backup.py

# Replace with fixed version
cp replicate_ai_enhancer_fixed.py replicate_ai_enhancer.py
```

### Step 2: Update Streamlit Chat Interface

The `houston_intelligence_chat.py` has been updated to:
- Increase timeout to 60 seconds for query endpoint
- Show better error messages
- Display loading message indicating potential wait time

### Step 3: Verify Environment Variables in Railway

1. Go to Railway dashboard
2. Check that `REPLICATE_API_TOKEN` is set correctly
3. Ensure `USE_REPLICATE=true` is set
4. Redeploy the service

### Step 4: Test the Fix

Test with a simple query first:
```
"What is the current market trend in Houston?"
```

Then test with a more complex query:
```
"Analyze investment opportunities in Houston Heights under $500k"
```

## Key Changes Made

### 1. Token Validation
```python
if not self.api_token:
    raise ValueError("REPLICATE_API_TOKEN not found")
```

### 2. Timeout Implementation
```python
# Model-specific timeouts
self.timeouts = {
    'llama2_70b': 60,      # 1 minute for large model
    'blip2': 30,           # 30 seconds for image analysis
    'stable_diffusion': 45, # 45 seconds for image generation
    'mistral': 30          # 30 seconds for smaller model
}
```

### 3. Polling with Timeout
```python
# Poll for completion with timeout
start_time = time.time()
while prediction.status not in ["succeeded", "failed", "canceled"]:
    if time.time() - start_time > timeout:
        # Cancel and raise timeout error
        raise TimeoutError(f"Model timed out after {timeout} seconds")
    time.sleep(1)
    prediction = self.client.predictions.get(prediction.id)
```

### 4. Better Error Handling
```python
except TimeoutError as e:
    return {
        'status': 'error',
        'error': 'Analysis timed out. Please try a simpler query.',
        'fallback_response': self._generate_fallback_response(query)
    }
```

## Monitoring

After deployment, monitor for:
1. Successful Replicate API calls in logs
2. Response times for different models
3. Any timeout errors with specific models

## Cost Considerations

With proper timeout handling, costs remain low:
- Llama 2 70B: ~$0.0016 per query
- Mistral 7B: ~$0.0002 per query
- BLIP-2: ~$0.00025 per question
- Stable Diffusion: ~$0.0025 per image

## Fallback Behavior

If Replicate continues to fail:
1. The system will use fallback responses
2. Knowledge base search will still work
3. Basic functionality remains available

## Next Steps

1. Deploy the fixed code to Railway
2. Monitor the logs for successful Replicate initialization
3. Test with various query types
4. Adjust timeouts if needed based on actual response times