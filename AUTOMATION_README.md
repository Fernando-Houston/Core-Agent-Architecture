# Houston Intelligence Platform - Automated Data Refresh System

## 🔄 Overview

This automated refresh system keeps your Houston Development Intelligence Platform current with the latest market data. The system includes three refresh cycles:

1. **Daily Refresh** - Real-time data updates (permits, listings, news)
2. **Weekly Refresh** - Market analysis and competitive intelligence
3. **Monthly Refresh** - Deep analysis and comprehensive research

## 📋 Components

### Refresh Agents
- `daily_refresh_agent.py` - Updates construction permits, MLS listings, zoning changes
- `weekly_refresh_agent.py` - Analyzes market trends, competitive landscape, neighborhoods
- `monthly_refresh_agent.py` - Comprehensive research, forecasts, strategic reports

### Automation Setup
- `setup_automation.sh` - Configures scheduled execution (cron/launchd)

## 🚀 Quick Start

### 1. Initial Setup
```bash
# Make setup script executable
chmod +x setup_automation.sh

# Run automation setup
./setup_automation.sh
```

### 2. Manual Testing
Test each refresh agent manually before enabling automation:

```bash
# Test daily refresh
python3 daily_refresh_agent.py

# Test weekly refresh
python3 weekly_refresh_agent.py

# Test monthly refresh
python3 monthly_refresh_agent.py
```

### 3. Check Schedule
```bash
# On macOS
launchctl list | grep houstonintelligence

# On Linux
crontab -l
```

## 📅 Default Schedule

| Refresh Type | Schedule | Time | Purpose |
|-------------|----------|------|---------|
| Daily | Every day | 6:00 AM | Real-time data updates |
| Weekly | Sundays | 4:00 AM | Market analysis |
| Monthly | 1st of month | 2:00 AM | Deep intelligence refresh |

## 📁 Data Structure

### Daily Updates
```
6 Specialized Agents/
├── Market Intelligence/
│   └── daily_updates_construction_permits.json
├── Neighborhood Intelligence/
│   └── daily_updates_mls_listings.json
└── Regulatory Intelligence/
    └── daily_updates_zoning_changes.json
```

### Weekly Reports
```
Processing_Pipeline/
├── Weekly_Reports/
│   └── weekly_report_YYYYMMDD.json
└── Processing_Status/
    └── refresh_status.json
```

### Monthly Analysis
```
Processing_Pipeline/
├── Monthly_Forecasts/
│   └── market_forecasts_YYYYMM.json
├── Strategic_Reports/
│   ├── monthly_strategic_report_YYYYMM.json
│   └── monthly_strategic_report_YYYYMM.md
└── Monthly_Backups/
    └── backup_YYYYMMDD_HHMMSS/
```

## 🔍 Monitoring

### Log Files
All refresh activities are logged:
```
automation_logs/
├── daily_refresh_agent.log
├── weekly_refresh_agent.log
└── monthly_refresh_agent.log
```

### View Logs
```bash
# View latest daily refresh
tail -n 50 automation_logs/daily_refresh_agent.log

# Monitor weekly refresh in real-time
tail -f automation_logs/weekly_refresh_agent.log
```

### Check Status
```bash
# View last refresh status
cat Processing_Pipeline/Processing_Status/refresh_status.json | python3 -m json.tool
```

## 🛠️ Customization

### Change Schedule

#### macOS (launchd)
Edit the plist files:
```bash
# Edit daily schedule
nano ~/Library/LaunchAgents/com.houstonintelligence.daily.plist

# Reload after editing
launchctl unload ~/Library/LaunchAgents/com.houstonintelligence.daily.plist
launchctl load ~/Library/LaunchAgents/com.houstonintelligence.daily.plist
```

#### Linux (cron)
```bash
# Edit cron jobs
crontab -e
```

### Modify Refresh Targets

Edit the refresh agents to change what data is collected:

```python
# In daily_refresh_agent.py
self.daily_update_targets = {
    "construction_permits": {
        "queries": [
            # Add your custom queries here
        ]
    }
}
```

## 🔌 Integration with Perplexity AI

Currently, the refresh agents use simulated data. To integrate with real data sources:

1. **Add Perplexity API Key**
   ```python
   # Create .env file
   PERPLEXITY_API_KEY=your_api_key_here
   ```

2. **Update Query Methods**
   ```python
   # Replace simulate_intelligence_query with:
   def query_perplexity(self, query):
       response = perplexity_client.query(query)
       return self.parse_perplexity_response(response)
   ```

## 🚨 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x setup_automation.sh
   chmod +x *.py
   ```

2. **Python Module Not Found**
   ```bash
   pip3 install pandas numpy
   ```

3. **Cron Job Not Running**
   - Check if cron service is running
   - Verify python3 path: `which python3`
   - Check log files for errors

4. **Disk Space Issues**
   - Monthly backups accumulate over time
   - Set up backup rotation:
   ```bash
   # Keep only last 3 months of backups
   find Processing_Pipeline/Monthly_Backups -mtime +90 -type d -exec rm -rf {} +
   ```

## 📊 Performance Optimization

### Parallel Processing
The monthly refresh can be resource-intensive. To optimize:

1. **Limit Concurrent Operations**
   ```python
   # In monthly_refresh_agent.py
   self.max_workers = 4  # Adjust based on system
   ```

2. **Schedule During Low Usage**
   - Default: 2 AM on the 1st
   - Adjust based on your server load

### Memory Management
- Daily: ~100MB memory usage
- Weekly: ~500MB memory usage
- Monthly: ~2GB memory usage (with backups)

## 🔒 Security

1. **API Keys**: Never commit API keys to version control
2. **File Permissions**: Ensure only authorized users can modify scripts
3. **Log Rotation**: Implement log rotation to prevent disk fill:
   ```bash
   # Add to crontab
   0 0 * * 0 find automation_logs -name "*.log" -mtime +30 -delete
   ```

## 📈 Success Metrics

Monitor these KPIs to ensure system health:

- Daily refresh success rate: >95%
- Weekly analysis completion: 100%
- Monthly backup success: 100%
- Average refresh duration:
  - Daily: <5 minutes
  - Weekly: <30 minutes
  - Monthly: <2 hours

## 🆘 Support

If you encounter issues:

1. Check the log files first
2. Verify all dependencies are installed
3. Ensure sufficient disk space (minimum 10GB recommended)
4. Test manual execution before automation

---

**Remember**: The quality of your intelligence platform depends on regular, reliable data updates. Monitor the system regularly and adjust schedules based on your business needs.