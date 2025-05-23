# Railway CLI Commands Reference

A comprehensive guide to Railway CLI commands for managing your deployments.

## Installation

### Install Railway CLI
```bash
# Using npm
npm install -g @railway/cli

# Using yarn
yarn global add @railway/cli

# Using Homebrew (macOS)
brew install railway

# Using curl (Linux/macOS)
curl -fsSL https://railway.app/install.sh | sh
```

### Verify Installation
```bash
railway --version
```

## Authentication

### Login to Railway
```bash
# Login via browser
railway login

# Login with token
railway login --token <your-token>

# Check login status
railway whoami
```

### Logout
```bash
railway logout
```

## Project Management

### List Projects
```bash
railway projects
```

### Create New Project
```bash
railway init
```

### Link to Existing Project
```bash
# Interactive selection
railway link

# Link to specific project
railway link <project-id>
```

### Project Information
```bash
# Show current project status
railway status

# Show project details
railway project
```

## Service Management

### List Services
```bash
railway service list
```

### Select/Link Service
```bash
# Interactive service selection
railway service

# Link to specific service
railway service <service-name>
```

### Create New Service
```bash
railway service create
```

### Delete Service
```bash
railway service delete
```

## Deployment Commands

### Deploy Current Directory
```bash
# Deploy using detected buildpack
railway up

# Deploy with specific dockerfile
railway up --dockerfile Dockerfile

# Deploy from specific directory
railway up --path ./my-app

# Deploy with detach (don't stream logs)
railway up --detach
```

### Check Deployment Status
```bash
# Show deployment status
railway status

# Show recent deployments
railway deployments
```

### Rollback Deployment
```bash
# List deployments to find ID
railway deployments

# Rollback to specific deployment
railway rollback <deployment-id>
```

## Domain Management

### List Domains
```bash
railway domain
```

### Add Custom Domain
```bash
railway domain add <your-domain.com>
```

### Remove Domain
```bash
railway domain remove <domain>
```

### Generate Railway Domain
```bash
# This creates the default .up.railway.app domain
railway domain
```

## Environment Variables

### List Environment Variables
```bash
railway vars
```

### Set Environment Variable
```bash
# Set single variable
railway vars set KEY=value

# Set multiple variables
railway vars set KEY1=value1 KEY2=value2

# Set from file
railway vars set --file .env
```

### Remove Environment Variable
```bash
railway vars remove KEY
```

### View Specific Variable
```bash
railway vars get KEY
```

## Logs and Monitoring

### View Application Logs
```bash
# Stream live logs
railway logs

# View last 100 lines
railway logs --tail 100

# View logs for specific service
railway logs --service <service-name>

# View logs for specific deployment
railway logs --deployment <deployment-id>
```

### Open Application in Browser
```bash
railway open
```

## Development Tools

### Run Local Development
```bash
# Run with Railway environment variables
railway run <command>

# Example: Run local server with production env vars
railway run python app/main.py
railway run uvicorn app.main:app --reload

# Run npm/yarn commands with env vars
railway run npm start
railway run yarn dev
```

### Connect to Database
```bash
# Open database shell (if using Railway database)
railway connect <database-service>
```

### Port Forwarding
```bash
# Forward local port to Railway service
railway connect <service-name> --port <local-port>
```

## Configuration Management

### View Configuration
```bash
# Show railway.json content
cat railway.json

# Validate railway.json
railway validate
```

### Generate railway.json
```bash
# Create railway.json with current settings
railway init --template
```

## Useful Workflow Commands

### Complete Deployment Workflow
```bash
# 1. Link to project/service
railway link

# 2. Set environment variables (if needed)
railway vars set NODE_ENV=production

# 3. Deploy
railway up

# 4. Check status
railway status

# 5. View logs
railway logs

# 6. Open in browser
railway open
```

### Development Workflow
```bash
# 1. Run locally with production env vars
railway run uvicorn app.main:app --reload

# 2. Test locally
curl http://localhost:8000/health

# 3. Deploy when ready
railway up

# 4. Check production
railway open
```

### Debugging Workflow
```bash
# 1. Check deployment status
railway status

# 2. View recent logs
railway logs --tail 50

# 3. Check environment variables
railway vars

# 4. Check service configuration
railway service

# 5. View deployments history
railway deployments
```

## Advanced Commands

### Export Environment Variables
```bash
# Export to .env file
railway vars > .env

# Use in shell
eval $(railway vars export)
```

### Service Health Check
```bash
# Check if service is responding
curl $(railway domain)/health
```

### Bulk Operations
```bash
# Deploy multiple services
for service in api frontend; do
  railway service $service
  railway up
done
```

## Troubleshooting Commands

### Common Debugging Steps
```bash
# 1. Verify authentication
railway whoami

# 2. Check project linking
railway status

# 3. Verify service exists
railway service list

# 4. Check recent deployments
railway deployments

# 5. View build/deploy logs
railway logs --deployment <latest-deployment-id>

# 6. Check environment variables
railway vars

# 7. Test domain resolution
nslookup <your-app>.up.railway.app
```

### Performance Monitoring
```bash
# Monitor application response time
while true; do
  curl -w "%{time_total}\n" -o /dev/null -s $(railway domain)/health
  sleep 5
done
```

## Quick Reference

### Essential Commands
```bash
railway login              # Authenticate
railway link               # Link to project
railway service            # Select service
railway up                 # Deploy
railway logs               # View logs
railway domain             # Get/manage domains
railway vars               # Manage env vars
railway status             # Check status
railway open               # Open in browser
```

### Emergency Commands
```bash
railway logs --tail 200    # Recent logs
railway rollback <id>      # Emergency rollback
railway vars set DEBUG=true # Enable debug mode
```

## Configuration Files

### railway.json Structure
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Environment File (.env)
```bash
# Example .env for Railway
NODE_ENV=production
DEBUG=false
PORT=8000
```

---

## Support and Resources

- **Railway Documentation**: https://docs.railway.app
- **Railway CLI GitHub**: https://github.com/railwayapp/cli
- **Community Discord**: https://discord.gg/railway
- **Status Page**: https://status.railway.app

---

*This reference covers Railway CLI v3.x - check `railway --version` for your current version* 