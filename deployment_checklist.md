# 🚀 Deployment Checklist

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
