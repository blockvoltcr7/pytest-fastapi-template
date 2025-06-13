# FastAPI Deployment to Railway.com 🚄

This guide provides the **complete deployment strategy** for your FastAPI application to [Railway.com](https://railway.com/) - a modern cloud platform with superior developer experience.

## 🎯 Why Railway Over Other Platforms?

✅ **No Sleep Mode**: Unlike Render's free tier, Railway doesn't force apps to sleep
✅ **Superior UX**: Users consistently report the best deployment experience
✅ **Multiple Options**: Different deployment methods with Docker support
✅ **Auto-Detection**: Automatically detects and configures your app
✅ **Built-in Networking**: Easy service-to-service communication
✅ **Better Performance**: Faster deployments and more reliable infrastructure

## 🚀 Getting Started with Railway

### 1. Create Railway Account
1. Visit [Railway.app](https://railway.app)
2. Click "Login" or "Sign Up"
3. Authenticate with GitHub (recommended)
4. Complete any required verification steps

### 2. Create New Project
1. Click "New Project" in Railway dashboard
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will automatically detect your configuration

## 📋 Pre-deployment Checklist

✅ FastAPI application configured in `app/main.py`
✅ Dependencies listed in `requirements.txt` (generated from `pyproject.toml`)
✅ `railway.json` configuration file created
✅ Health check endpoint added (`/health`)
✅ Railway-optimized `Dockerfile.railway` ready

## 📦 Package Management Note

This project uses **UV package manager** for local development but includes a `requirements.txt` file for cloud deployment compatibility:

- **Local Development**: Use `uv sync` and `uv run` commands
- **Cloud Deployment**: Railway/Docker uses `pip install -r requirements.txt`
- **Sync Process**: Run `uv pip freeze > requirements.txt` to update deployment dependencies

## ⚙️ Required Configuration Files

### 1. railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.railway"
  },
  "deploy": {
    "startCommand": null,
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Dockerfile.railway
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install dependencies using standard pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
COPY . .

# Create directory for allure results
RUN mkdir -p allure-results

# Expose port
EXPOSE 8000

# Set environment variable with a default value
ENV PORT=8000

# Run the FastAPI application with proper PORT variable expansion
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 🔑 Important Configuration Notes

### PORT Handling
- Railway automatically injects a `PORT` environment variable
- The Dockerfile sets a default `PORT=8000` as fallback
- Use simple `CMD` format instead of shell form for proper variable expansion
- Avoid using `${PORT:-8000}` syntax as it can cause issues

### Health Check
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}
```

## 🚀 Deployment Process

1. **Prepare Repository**
   ```bash
   git add .
   git commit -m "Configure Railway deployment"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to Railway Dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Wait for initial deployment (2-3 minutes)

3. **Monitor Deployment**
   - Watch build logs in Railway dashboard
   - Check for successful health check responses
   - Verify PORT environment variable handling

4. **Configure Domain**
   - Go to Settings → Networking
   - Click "Generate Domain"
   - Your API will be available at `https://your-app-name.up.railway.app`

## 🧪 Testing Your Deployment

1. **Health Check**
   ```bash
   curl https://your-app-name.up.railway.app/health
   # Expected: {"status": "healthy", "message": "API is running successfully"}
   ```

2. **API Documentation**
   - Visit `https://your-app-name.up.railway.app/docs`
   - Test endpoints through Swagger UI

## 🚨 Troubleshooting Common Issues

### 1. PORT Configuration Issues
If you see errors like `Invalid value for '--port': '$PORT' is not a valid integer`:
- Verify `Dockerfile.railway` uses the correct CMD format
- Ensure PORT environment variable is properly set
- Check Railway dashboard for environment variables

### 2. Health Check Failures
- Verify `/health` endpoint exists and returns correct response
- Check health check timeout in `railway.json`
- Review application logs for startup errors

### 3. Build Failures
- Ensure all dependencies are in `requirements.txt`
- Use standard `pip` instead of `uv`
- Check build logs for specific error messages

## 📊 Monitoring and Logs

1. **View Logs**
   - Railway Dashboard → Your Project → Logs
   - Filter by service or deployment
   - Search for specific error messages

2. **Monitor Health**
   - Check deployment status
   - Review health check responses
   - Monitor resource usage

## 🔧 Advanced Configuration

### Environment Variables
- Set in Railway dashboard under Variables tab
- Supports `.env` file upload
- Automatically injected into containers

### Custom Domains
- Add domains in Settings → Networking
- Automatic SSL certificate provisioning
- Update DNS records as instructed

### Scaling
- Configure resources in project settings
- Set auto-scaling rules
- Monitor performance metrics

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

## 🆘 Getting Help

- Join [Railway Discord](https://discord.gg/railway)
- Check [Railway Status Page](https://status.railway.app/)
- Review [Common Issues](https://docs.railway.app/troubleshoot)

---

**Deployment Status**: ✅ Railway-Ready
**Estimated Deploy Time**: 2-3 minutes
**Support**: [Railway Support](https://railway.app/support)

**All aboard the Railway! 🚄✨**
