#!/bin/bash
# Push to GitHub with Personal Access Token

echo "🚀 Pushing Houston Intelligence Platform to GitHub..."

cd "/Users/fernandox/Desktop/Core Agent Architecture"

# Configure git to use the token
git config --local credential.helper ""

# Push using the token
echo "📤 Pushing to private repository..."
echo "When prompted:"
echo "  Username: Fernando-Houston"
echo "  Password: [paste your token]"
echo ""

git push -u origin main

echo "✅ Done! Check your repository at:"
echo "https://github.com/Fernando-Houston/Core-Agent-Architecture"