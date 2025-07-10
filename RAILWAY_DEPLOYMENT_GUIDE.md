# Railway Pro Deployment Guide for ML Applications

## Problem Summary
The build is failing during pip install of torch/transformers packages on Railway Pro (32GB RAM, 100GB disk).

## Solution Options

### Option 1: Use Nixpacks with CPU-Only PyTorch (Recommended)

1. **Created Files:**
   - `nixpacks.toml` - Configures build process with increased timeouts
   - `.python-version` - Specifies Python 3.11
   - `requirements-railway.txt` - Uses CPU-only PyTorch to reduce package size

2. **To Deploy:**
   ```bash
   # Update railway.json to use the new requirements file
   # In railway.json, add:
   "build": {
     "builder": "NIXPACKS",
     "buildCommand": "pip install -r requirements-railway.txt"
   }
   ```

3. **Key Changes:**
   - Uses PyTorch CPU version (much smaller: ~200MB vs ~2GB)
   - Increased pip timeout to 1000 seconds
   - Specified Python 3.11 for consistency

### Option 2: Use Railpack (Beta)

1. **Enable in Railway Dashboard:**
   - Go to your service settings
   - Enable "Railpack (Beta)" builder
   - Railpack offers 77% smaller Python images

2. **Benefits:**
   - Better caching
   - Smaller image sizes
   - More reliable builds

### Option 3: Use Docker (Most Control)

1. **Created File:**
   - `Dockerfile.railway` - Multi-stage build optimized for ML packages

2. **To Deploy:**
   ```bash
   # In railway.json, change:
   "build": {
     "builder": "DOCKERFILE",
     "dockerfilePath": "./Dockerfile.railway"
   }
   ```

3. **Benefits:**
   - Full control over build process
   - Better layer caching
   - Can install system dependencies

## Build Failure Root Causes

1. **Package Size**: Full PyTorch with CUDA is ~2GB, causing memory issues during installation
2. **Build Timeouts**: Default pip timeout may be too short for large packages
3. **Missing System Dependencies**: Some ML packages need gcc/g++ for compilation

## Best Practices for Railway ML Deployments

1. **Use CPU-Only Versions**: Unless you have GPU access, CPU versions are smaller and sufficient
2. **Increase Timeouts**: Set pip timeout to at least 1000 seconds
3. **Use Specific Versions**: Lock all package versions to avoid surprises
4. **Consider Lighter Alternatives**:
   - Use `sentence-transformers` instead of full `transformers` if only doing embeddings
   - Use `onnxruntime` for inference-only workloads

## Environment Variables to Set in Railway

```bash
NIXPACKS_PYTHON_VERSION=3.11
PIP_DEFAULT_TIMEOUT=1000
PIP_NO_CACHE_DIR=1
PYTHONUNBUFFERED=1
```

## Testing Locally

Before deploying, test the build locally:

```bash
# Test with nixpacks
npx nixpacks build . --name test-build

# Or test with Docker
docker build -f Dockerfile.railway -t test-build .
```

## Monitoring Build Logs

Watch for these in Railway build logs:
- "Collecting torch" - Should show CPU version
- Memory usage warnings
- Timeout errors

## If Build Still Fails

1. **Check Build Logs**: Look for specific error messages
2. **Try Smaller Models**: Use distilled models like `distilbert-base-uncased`
3. **Split Dependencies**: Install core deps first, then ML packages
4. **Contact Railway Support**: With Pro plan, you have priority support

## Alternative Approaches

If Railway continues to have issues:
1. Pre-build Docker images and push to registry
2. Use Railway's container image deployment
3. Consider using model APIs instead of local inference