#!/bin/bash
#
# Houston Intelligence Platform - Automation Setup Script
# Sets up cron jobs for automated data refresh
#

echo "🚀 Houston Intelligence Platform - Automation Setup"
echo "=================================================="

# Get the current directory (where the scripts are located)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create logs directory
LOGS_DIR="$SCRIPT_DIR/automation_logs"
mkdir -p "$LOGS_DIR"

echo "📁 Script directory: $SCRIPT_DIR"
echo "📝 Logs directory: $LOGS_DIR"

# Function to add cron job
add_cron_job() {
    local schedule="$1"
    local script="$2"
    local description="$3"
    
    # Create the cron job entry
    local cron_entry="$schedule cd $SCRIPT_DIR && /usr/bin/python3 $script >> $LOGS_DIR/${script%.py}.log 2>&1"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "$script"; then
        echo "⚠️  Cron job for $script already exists. Skipping..."
    else
        # Add the cron job
        (crontab -l 2>/dev/null; echo "# $description"; echo "$cron_entry") | crontab -
        echo "✅ Added cron job: $description"
        echo "   Schedule: $schedule"
        echo "   Script: $script"
    fi
}

# Function to setup launchd (macOS alternative to cron)
setup_launchd() {
    local plist_name="$1"
    local script="$2"
    local calendar_interval="$3"
    
    local plist_file="$HOME/Library/LaunchAgents/com.houstonintelligence.$plist_name.plist"
    
    cat > "$plist_file" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.houstonintelligence.$plist_name</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$SCRIPT_DIR/$script</string>
    </array>
    <key>StartCalendarInterval</key>
    $calendar_interval
    <key>StandardOutPath</key>
    <string>$LOGS_DIR/${script%.py}.log</string>
    <key>StandardErrorPath</key>
    <string>$LOGS_DIR/${script%.py}_error.log</string>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
</dict>
</plist>
EOF
    
    launchctl load "$plist_file" 2>/dev/null
    echo "✅ Setup launchd job: $plist_name"
}

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🖥️  Detected macOS - using launchd for scheduling"
    USE_LAUNCHD=true
else
    echo "🐧 Detected Linux - using cron for scheduling"
    USE_LAUNCHD=false
fi

echo ""
echo "📅 Setting up automated refresh schedules..."
echo ""

if [ "$USE_LAUNCHD" = true ]; then
    # macOS launchd setup
    
    # Daily refresh at 6 AM
    setup_launchd "daily" "daily_refresh_agent.py" "
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>"
    
    # Weekly refresh on Sundays at 4 AM
    setup_launchd "weekly" "weekly_refresh_agent.py" "
    <dict>
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>4</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>"
    
    # Monthly refresh on 1st at 2 AM
    setup_launchd "monthly" "monthly_refresh_agent.py" "
    <dict>
        <key>Day</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>"
    
else
    # Linux cron setup
    
    # Daily refresh at 6 AM
    add_cron_job "0 6 * * *" "daily_refresh_agent.py" "Houston Intelligence Daily Refresh (6 AM)"
    
    # Weekly refresh on Sundays at 4 AM
    add_cron_job "0 4 * * 0" "weekly_refresh_agent.py" "Houston Intelligence Weekly Refresh (Sundays 4 AM)"
    
    # Monthly refresh on 1st at 2 AM
    add_cron_job "0 2 1 * *" "monthly_refresh_agent.py" "Houston Intelligence Monthly Deep Refresh (1st of month, 2 AM)"
fi

echo ""
echo "📊 Current scheduled jobs:"
echo ""

if [ "$USE_LAUNCHD" = true ]; then
    launchctl list | grep houstonintelligence
else
    crontab -l | grep -E "(daily|weekly|monthly)_refresh_agent.py" || echo "No cron jobs found"
fi

echo ""
echo "🔧 Useful commands:"
echo ""

if [ "$USE_LAUNCHD" = true ]; then
    echo "View all jobs:     launchctl list | grep houstonintelligence"
    echo "Stop a job:        launchctl unload ~/Library/LaunchAgents/com.houstonintelligence.*.plist"
    echo "Start a job:       launchctl load ~/Library/LaunchAgents/com.houstonintelligence.*.plist"
    echo "Remove a job:      rm ~/Library/LaunchAgents/com.houstonintelligence.*.plist"
else
    echo "View all cron jobs:  crontab -l"
    echo "Edit cron jobs:      crontab -e"
    echo "Remove all jobs:     crontab -r"
fi

echo ""
echo "📁 Log files location: $LOGS_DIR"
echo ""
echo "✅ Automation setup complete!"
echo ""
echo "To test the refresh agents manually:"
echo "  python3 daily_refresh_agent.py"
echo "  python3 weekly_refresh_agent.py"
echo "  python3 monthly_refresh_agent.py"
echo ""