#!/bin/bash

echo "🚄 FastAPI Deployment to Railway.com"
echo "===================================="

echo "📋 Pre-deployment checklist:"
echo "✅ FastAPI app configured"
echo "✅ Requirements.txt ready"
echo "✅ railway.json configured"
echo "✅ Health check endpoint added"
echo "✅ Dockerfile.railway optimized"

echo ""
echo "🚀 Railway Deployment Options:"
echo ""
echo "Option 1: One-Click Template (Fastest - 30 seconds)"
echo "  1. Visit: https://railway.app/template/fastapi"
echo "  2. Click 'Deploy on Railway'"
echo "  3. Connect GitHub account"
echo "  4. Done! ✨"

echo ""
echo "Option 2: GitHub Repository Deploy (Recommended)"
echo "  1. Push code to GitHub:"
echo "     git add ."
echo "     git commit -m 'Deploy to Railway'"
echo "     git push origin main"
echo "  2. Visit: https://railway.app"
echo "  3. Click 'New Project' > 'Deploy from GitHub repo'"
echo "  4. Select your repository"
echo "  5. Click 'Deploy Now'"

echo ""
echo "Option 3: Railway CLI (Developer-friendly)"
echo "  1. Install CLI: npm install -g @railway/cli"
echo "  2. Login: railway login"
echo "  3. Initialize: railway init"
echo "  4. Deploy: railway up"

echo ""
echo "Option 4: Docker Deployment"
echo "  - Railway automatically detects Dockerfile.railway"
echo "  - Uses optimized container build"
echo "  - Built-in health checks"

echo ""
echo "🧪 Post-deployment testing:"
echo "1. Root: https://your-app-name.up.railway.app/"
echo "2. Health: https://your-app-name.up.railway.app/health"
echo "3. Docs: https://your-app-name.up.railway.app/docs"
echo "4. API: https://your-app-name.up.railway.app/api/v1/"

echo ""
echo "🎯 Railway Advantages:"
echo "✅ No sleep mode (unlike Render free tier)"
echo "✅ Faster cold starts (~1s vs 30s+)"
echo "✅ Superior developer experience"
echo "✅ Built-in monitoring and logs"
echo "✅ Auto-scaling and load balancing"
echo "✅ One-click database integration"

echo ""
echo "🚄 All aboard the Railway! ✨"

# Check if railway CLI is installed
if command -v railway &> /dev/null; then
    echo ""
    echo "🔧 Railway CLI detected! Want to deploy now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "🚀 Deploying to Railway..."
        railway login
        railway init
        railway up
        echo "✅ Deployment initiated!"
    fi
else
    echo ""
    echo "💡 Tip: Install Railway CLI for fastest deployment:"
    echo "   npm install -g @railway/cli"
fi 