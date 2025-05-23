#!/bin/bash

echo "🚀 FastAPI Deployment to Render.com"
echo "=================================="

echo "📋 Pre-deployment checklist:"
echo "✅ FastAPI app configured"
echo "✅ Requirements.txt ready"
echo "✅ render.yaml configured"
echo "✅ Dockerfile updated for production"

echo ""
echo "🧪 Testing locally (optional):"
echo "1. Run: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo "2. Visit: http://localhost:8000"
echo "3. Check API docs: http://localhost:8000/docs"

echo ""
echo "🌐 Deploy to Render:"
echo "1. Push your code to GitHub"
echo "2. Go to https://render.com"
echo "3. Click 'New' > 'Web Service'"
echo "4. Connect your GitHub repository"
echo "5. Use these settings:"
echo "   - Language: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo "   - Plan: Free (for testing)"

echo ""
echo "🔧 Alternative: Use render.yaml (Infrastructure as Code)"
echo "1. Make sure render.yaml is in your repo root"
echo "2. Render will automatically detect and use the configuration"

echo ""
echo "🧪 Post-deployment testing:"
echo "1. Visit your-app-name.onrender.com"
echo "2. Test API docs at your-app-name.onrender.com/docs"
echo "3. Test endpoints at your-app-name.onrender.com/api/v1/"

echo ""
echo "⚠️  Important notes:"
echo "- Free tier may sleep after 15 minutes of inactivity"
echo "- First request after sleep may take 30+ seconds"
echo "- For production, consider paid plans for better performance"

echo ""
echo "Happy deploying! 🎉" 