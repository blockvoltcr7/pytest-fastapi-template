# Railway Deployment Details

## Accessing Your Deployed Application

Your FastAPI application is successfully deployed on Railway! Here's how to find and access all your endpoints.



## Finding Your App URL

### Method 1: Railway CLI (Recommended)
```bash
# Link to your service (if not already linked)
railway service

# Get the domain URL
railway domain
```

**Your current app URL:** `https://pytest-fast-api-template-production.up.railway.app`

### Method 2: Railway Dashboard
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Select your `pytest-fast-api-template` project
3. Click on your service
4. Look for the **"Domains"** section or **"Public URL"**

## Available Endpoints

### Core Application Endpoints

1. **Root Endpoint**
   ```
   GET https://pytest-fast-api-template-production.up.railway.app/
   ```
   Returns welcome message

2. **Health Check**
   ```
   GET https://pytest-fast-api-template-production.up.railway.app/health
   ```
   Returns application health status

3. **Items API**
   ```
   GET https://pytest-fast-api-template-production.up.railway.app/items/
   GET https://pytest-fast-api-template-production.up.railway.app/items/{item_id}
   POST https://pytest-fast-api-template-production.up.railway.app/items/
   ```

### API Documentation

4. **Swagger UI (Interactive API Documentation)**
   ```
   https://pytest-fast-api-template-production.up.railway.app/docs
   ```
   - Interactive API testing interface
   - Try out endpoints directly in the browser

5. **ReDoc (Alternative API Documentation)**
   ```
   https://pytest-fast-api-template-production.up.railway.app/redoc
   ```
   - Clean, readable API documentation

### OpenAPI Schema

6. **OpenAPI JSON Schema**
   ```
   GET https://pytest-fast-api-template-production.up.railway.app/openapi.json
   ```
   - Raw OpenAPI specification in JSON format

## Testing Your Deployment

### Using cURL
```bash
# Test health endpoint
curl https://pytest-fast-api-template-production.up.railway.app/health

# Test root endpoint
curl https://pytest-fast-api-template-production.up.railway.app/

# Test items endpoint
curl https://pytest-fast-api-template-production.up.railway.app/items/

# Test specific item
curl https://pytest-fast-api-template-production.up.railway.app/items/1
```

### Using HTTPie
```bash
# Install HTTPie if not installed
pip install httpie

# Test endpoints
http GET https://pytest-fast-api-template-production.up.railway.app/health
http GET https://pytest-fast-api-template-production.up.railway.app/items/
```

### Using Python Requests
```python
import requests

base_url = "https://pytest-fast-api-template-production.up.railway.app"

# Test health
response = requests.get(f"{base_url}/health")
print(response.json())

# Test items
response = requests.get(f"{base_url}/items/")
print(response.json())
```

## Monitoring Your Application

### Railway Dashboard
- View real-time logs in the Railway dashboard
- Monitor deployment status and health checks
- Check resource usage and metrics

### Health Check Monitoring
Railway automatically monitors your `/health` endpoint for application health.

## Custom Domain (Optional)

To use your own domain:

1. In Railway Dashboard, go to your service
2. Navigate to "Domains" section
3. Click "Add Domain"
4. Enter your custom domain
5. Configure DNS records as instructed

## Environment Variables

Current configuration:
- `PORT`: Automatically set by Railway (usually 8080)
- Application runs on `0.0.0.0:${PORT}`

## Deployment Information

- **Platform**: Railway.app
- **Runtime**: Python 3.11
- **Framework**: FastAPI with Uvicorn
- **Build Method**: Docker
- **Health Check**: `/health` endpoint
- **Auto-deploy**: Enabled (deploys on git push)

## Troubleshooting

### If endpoints are not accessible:
1. Check Railway dashboard for deployment status
2. Review deploy logs for errors
3. Verify health check is passing
4. Check if service is properly started

### Common Issues:
- **503 Service Unavailable**: Application may be starting up (wait 1-2 minutes)
- **404 Not Found**: Check if the endpoint path is correct
- **Deployment failed**: Review build logs in Railway dashboard

## Next Steps

1. **Test all endpoints** using the Swagger UI at `/docs`
2. **Set up monitoring** for production usage
3. **Configure custom domain** if needed
4. **Set up CI/CD** for automated testing before deployment

---

*Last updated: May 2025*
*Deployment URL: https://pytest-fast-api-template-production.up.railway.app*
