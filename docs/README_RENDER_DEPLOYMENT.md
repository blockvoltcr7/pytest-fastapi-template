# FastAPI Deployment to Render.com 🚀

This guide provides the **easiest and fastest way** to deploy your FastAPI application to [Render.com](https://render.com/).

## 📋 Pre-deployment Checklist

✅ FastAPI application configured in `app/main.py`
✅ Dependencies listed in `requirements.txt` (generated from `pyproject.toml`)
✅ `render.yaml` configuration file created
✅ Health check endpoint added (`/health`)
✅ All tests passing with pytest

## 📦 Package Management Note

This project uses **UV package manager** for local development but includes a `requirements.txt` file for cloud deployment compatibility:

- **Local Development**: Use `uv sync` and `uv run` commands
- **Cloud Deployment**: Render uses `pip install -r requirements.txt`
- **Sync Process**: Run `uv pip freeze > requirements.txt` to update deployment dependencies

## 📝 Prerequisite: Create a Render.com Account

Before you can deploy your FastAPI application, you need to have a [Render.com](https://render.com/) account.

1. **Sign Up or Log In**
   - Go to [https://render.com](https://render.com)
   - Click **"Sign Up"** (or **"Log In"** if you already have an account)
   - You can sign up using your email or with your GitHub account for easier integration

2. **Verify Your Email**
   - If you signed up with email, check your inbox for a verification email from Render and follow the instructions

Once your account is set up, you can proceed with the deployment steps below.


## 🌟 Deployment Options

### Option 1: Quick Deploy (Recommended for beginners)

1. **Push to GitHub**
If you have made changes to your code base
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [https://render.com](https://render.com)
   - Click **"New"** → **"Web Service"**
   - Connect your GitHub repository
   - Configure with these settings:

   | Setting | Value |
   |---------|-------|
   | **Language** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | **Plan** | Free (for testing) |
   | **Health Check Path** | `/health` |

3. **Deploy!**
   - Click **"Create Web Service"**
   - Wait 2-3 minutes for deployment
   - Your API will be live at `https://your-app-name.onrender.com`

### Option 2: Infrastructure as Code (Recommended for production)

Your repo includes a `render.yaml` file that Render will automatically detect:

```yaml
services:
  - type: web
    name: genai-fastapi
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: ENVIRONMENT
        value: production
```

Simply connect your repo and Render will use this configuration automatically.

## 🧪 Testing Your Deployment

Once deployed, test these endpoints:

1. **Root endpoint**: `https://pytest-fastapi-template.onrender.com/`
   - Expected: `{"message": "GenAI API"}`

2. **Health check**: `https://pytest-fastapi-template.onrender.com/health`
   - Expected: `{"status": "healthy", "message": "API is running successfully"}`

3. **API Documentation**: `https://pytest-fastapi-template.onrender.com/docs`
   - Interactive Swagger UI

4. **API v1 endpoints**: `https://pytest-fastapi-template.onrender.com/api/v1/hello`
   - Your custom endpoints

## 🔧 Advanced Configuration

### Health Check Path
- Set to `/health` for automatic monitoring
- Render pings this endpoint to ensure your service is healthy
- Returns `{"status": "healthy", "message": "API is running successfully"}`

### Auto-Deploy Settings
- Set to "On Commit" for automatic deployments
- Every push to main branch triggers a new deployment
- No manual intervention needed

### Environment Variables
- Set in Render dashboard or `render.yaml`
- Secure way to manage API keys and secrets
- Production environment automatically set

## ⚠️ Important Notes

### Free Tier Limitations
- **Sleep Mode**: Apps sleep after 15 minutes of inactivity
- **Cold Start**: First request after sleep takes 30+ seconds
- **Build Time**: Limited build minutes per month

### Production Recommendations
- **Upgrade to Paid Plan**: For 24/7 availability and better performance
- **Environment Variables**: Set production secrets in Render dashboard
- **Custom Domain**: Add your own domain for professional appearance
- **Monitoring**: Enable health checks and notifications

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   - Make sure to use `pip` (not `uv`) in the build command
   - Check that `requirements.txt` is up to date
   - Verify Python version compatibility
   - Check build logs in Render dashboard

2. **App Won't Start**
   - Verify start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Check that `app.main:app` matches your file structure
   - Review app logs in Render dashboard

3. **404 Errors**
   - Verify your API routes are correctly configured
   - Check that `/api/v1/` prefix is properly set up
   - Test locally first

### Debug Commands
```bash
# Check if dependencies install correctly
pip install -r requirements.txt

# Test the exact start command Render uses
PORT=8000 uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Run tests to ensure everything works
pytest
```

## 🎯 Next Steps

After successful deployment:

1. **Monitor Performance**: Check response times and uptime
2. **Set Up CI/CD**: Configure automatic deployments on git push
3. **Add Environment Variables**: Configure production settings
4. **Scale Up**: Upgrade to paid plan for production workloads
5. **Custom Domain**: Add your own domain name
6. **Database**: Add Render PostgreSQL for data persistence

## 📚 Resources

- [Render FastAPI Documentation](https://render.com/docs/deploy-fastapi)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Render Blog: FastAPI Deployment](https://render.com/blog)

---

**Deployment Status**: ✅ Ready for deployment
**Estimated Deploy Time**: 2-3 minutes
**Expected URL**: `https://your-app-name.onrender.com`

Happy deploying! 🎉
