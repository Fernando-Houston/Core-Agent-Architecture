#!/bin/bash
# Automated push script for Houston Intelligence Platform

echo "🚀 Automated GitHub Push for Houston Intelligence Platform"
echo "======================================================="

# Navigate to project directory
cd "/Users/fernandox/Desktop/Core Agent Architecture"

# Set up the remote URL with token embedded (temporary for this push)
echo "📡 Configuring authenticated remote..."
git remote set-url origin https://Fernando-Houston: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@github.com/Fernando-Houston/Core-Agent-Architecture.git

# Check current status
echo -e "\n📊 Repository Status:"
git status --short

# Push to GitHub
echo -e "\n📤 Pushing to GitHub..."
git push -u origin main

# Reset the URL to remove the token (for security)
echo -e "\n🔒 Securing remote URL..."
git remote set-url origin https://github.com/Fernando-Houston/Core-Agent-Architecture.git

echo -e "\n✅ Push complete!"
echo "🌐 Repository URL: https://github.com/Fernando-Houston/Core-Agent-Architecture"
echo "🚀 Ready for Railway deployment!"
echo ""
echo "⚠️  IMPORTANT: Delete this script after use for security!"