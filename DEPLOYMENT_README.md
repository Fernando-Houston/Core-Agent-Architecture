# Houston Intelligence Platform - Deployment

## 🚀 Railway Deployment

### Prerequisites
- GitHub repository connected
- Railway account
- Perplexity API key

### Deployment Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

2. **Create Railway Project**
- Go to [railway.app](https://railway.app)
- New Project → Deploy from GitHub repo
- Select `Core-Agent-Architecture`

3. **Set Environment Variables in Railway**
```
PERPLEXITY_API_KEY=your-perplexity-api-key-here
SECRET_KEY=generate-a-random-secret-key
PORT=8080
```

4. **Deploy**
- Railway will auto-deploy on push
- Get your URL: `https://your-app.railway.app`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| PERPLEXITY_API_KEY | Your Perplexity API key | Yes |
| SECRET_KEY | Flask secret key | Yes |
| PORT | Port number (Railway sets this) | Auto |
| CENSUS_API_KEY | US Census API key | No |

### Testing Deployment

```bash
# Health check
curl https://your-app.railway.app/health

# Test query
curl -X POST https://your-app.railway.app/api/v1/query   -H "Content-Type: application/json"   -d '{"query": "Houston market trends"}'
```

### Monitoring

Railway provides:
- Deployment logs
- Resource metrics
- Crash alerts
- Auto-restart on failure

### Troubleshooting

1. **Module not found**: Check requirements.txt
2. **Port issues**: Let Railway set PORT
3. **API errors**: Verify env variables
4. **Memory issues**: Upgrade Railway plan

## 🔒 Security Notes

- Never commit .env file
- Use Railway's env variables
- Rotate API keys regularly
- Enable HTTPS (Railway provides)
