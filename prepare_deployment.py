#!/usr/bin/env python3
"""
Prepare Houston Intelligence Platform for Railway Deployment
Sets up environment variables and configuration
"""

import os
import json
from pathlib import Path

def update_api_with_env():
    """Update API to use environment variables"""
    api_update = '''
# Add this at the top of houston_intelligence_api.py after imports:
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Update the Flask app configuration:
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# The Perplexity client already uses os.getenv('PERPLEXITY_API_KEY')
'''
    
    print("📝 Update houston_intelligence_api.py:")
    print(api_update)

def create_railway_config():
    """Create railway.toml for deployment configuration"""
    config = '''[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn houston_intelligence_api:app --bind 0.0.0.0:$PORT"
restartPolicyType = "on-failure"
restartPolicyMaxRetries = 10

[variables]
FLASK_ENV = "production"
'''
    
    with open('railway.toml', 'w') as f:
        f.write(config)
    
    print("✅ Created railway.toml")

def create_github_workflow():
    """Create GitHub Actions workflow for auto-deploy"""
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow = '''name: Deploy to Railway

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install Railway
      run: npm i -g @railway/cli
    
    - name: Deploy to Railway
      run: railway up
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
'''
    
    workflow_path = workflow_dir / 'deploy.yml'
    with open(workflow_path, 'w') as f:
        f.write(workflow)
    
    print(f"✅ Created GitHub workflow: {workflow_path}")

def create_readme_deployment():
    """Create deployment instructions"""
    readme = '''# Houston Intelligence Platform - Deployment

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
curl -X POST https://your-app.railway.app/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Houston market trends"}'
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
'''
    
    with open('DEPLOYMENT_README.md', 'w') as f:
        f.write(readme)
    
    print("✅ Created DEPLOYMENT_README.md")

def check_requirements():
    """Verify requirements.txt has all dependencies"""
    required_packages = [
        'flask',
        'flask-cors', 
        'flask-limiter',
        'flask-caching',
        'gunicorn',
        'requests',
        'pandas',
        'python-dotenv'
    ]
    
    print("\n📦 Add python-dotenv to requirements.txt:")
    print("python-dotenv>=0.19.0")
    
    print("\n✅ Current requirements should include:")
    for pkg in required_packages:
        print(f"  - {pkg}")

def create_deployment_checklist():
    """Create a deployment checklist"""
    checklist = '''# 🚀 Deployment Checklist

## Before Pushing to GitHub

- [ ] API key removed from code (using env vars)
- [ ] .env file in .gitignore
- [ ] requirements.txt updated
- [ ] All imports working
- [ ] Test scripts removed from deployment

## GitHub Setup

- [ ] Create repository: https://github.com/Fernando-Houston/Core-Agent-Architecture
- [ ] Add .gitignore
- [ ] Don't commit .env file
- [ ] Push all code

## Railway Setup

- [ ] Connect GitHub repo
- [ ] Add environment variables:
  - [ ] PERPLEXITY_API_KEY
  - [ ] SECRET_KEY
  - [ ] Any other secrets
- [ ] Deploy

## Post-Deployment

- [ ] Test health endpoint
- [ ] Test API queries
- [ ] Monitor logs
- [ ] Set up domain (optional)
- [ ] Enable monitoring

## Files to Deploy

✅ Core Files:
- houston_intelligence_api.py
- houston_intelligence_endpoints.py
- master_intelligence_agent.py
- perplexity_integration.py
- perplexity_parsers.py
- perplexity_data_replacement.py
- All refresh agents
- All agent folders with knowledge

✅ Configuration:
- requirements.txt
- railway.toml
- Procfile
- .gitignore

❌ Don't Deploy:
- .env (use Railway env vars)
- Test files (optional)
- Local data files
- API keys in any file
'''
    
    with open('deployment_checklist.md', 'w') as f:
        f.write(checklist)
    
    print("✅ Created deployment_checklist.md")

def main():
    print("🚀 Preparing Houston Intelligence Platform for Deployment")
    print("="*60)
    
    # Create configurations
    create_railway_config()
    create_github_workflow()
    create_readme_deployment()
    create_deployment_checklist()
    
    # Show update instructions
    print("\n📝 Required Updates:")
    update_api_with_env()
    check_requirements()
    
    print("\n✅ Deployment Preparation Complete!")
    print("\n🎯 Next Steps:")
    print("1. Wait for T2 to complete")
    print("2. Update houston_intelligence_api.py with dotenv")
    print("3. Add python-dotenv to requirements.txt")
    print("4. Git init and push to GitHub:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git remote add origin https://github.com/Fernando-Houston/Core-Agent-Architecture.git")
    print("   git push -u origin main")
    print("\n5. Deploy on Railway with your Perplexity API key!")

if __name__ == "__main__":
    main()