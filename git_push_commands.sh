#!/bin/bash
# Git Push Commands for Houston Intelligence Platform

echo "🚀 Pushing Houston Intelligence Platform to GitHub..."

# Make sure we're in the right directory
cd "/Users/fernandox/Desktop/Core Agent Architecture"

# Check current status
echo "📊 Current Git Status:"
git status

# Check remote
echo -e "\n🔗 Remote Repository:"
git remote -v

# Push to GitHub
echo -e "\n📤 Pushing to GitHub..."
git push -u origin main

echo -e "\n✅ Push complete! Your repository should now be live at:"
echo "https://github.com/Fernando-Houston/Core-Agent-Architecture"