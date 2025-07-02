# Railway CLI Commands Reference

A comprehensive guide to Railway CLI commands for managing your deployments.

## Installation

### Install Railway CLI
```bash
# Using Homebrew (macOS)
brew install railway

# Using npm (macOS, Linux, Windows) - Requires Node.js >=16
npm i -g @railway/cli

# Using Shell Script (macOS, Linux, Windows via WSL)
bash <(curl -fsSL cli.new)

# Using Scoop (Windows)
# Ensure Scoop is installed (https://scoop.sh/)
scoop install railway

# Using Yarn (Alternative to npm)
yarn global add @railway/cli

# Pre-built Binaries
# Download directly from GitHub: https://github.com/railwayapp/cli/releases

# From Source
# Clone the repo and build: https://github.com/railwayapp/cli
```

### Verify Installation
```bash
railway --version
```

## Authentication

### Login to Railway
```bash
# Login via browser (opens railway.com authentication page)
railway login

# Manual login for environments without a browser (e.g., SSH)
railway login --browserless

# Check login status
railway whoami
```

### Token-based Authentication (for CI/CD or non-interactive environments)

Railway CLI can be authenticated using tokens by setting environment variables:

- **`RAILWAY_TOKEN` (Project Token):**
  - Scoped to a specific project and environment.
  - Allows project-level actions like `railway up`, `railway redeploy`, `railway logs`.
  - Cannot perform actions like `railway init`, `railway whoami`, `railway link`.
  - Example: `RAILWAY_TOKEN=your_project_token railway up`

- **`RAILWAY_API_TOKEN` (Account or Team Token):**
  - **Personal Account Token:** Allows all CLI actions across all workspaces.
  - **Team Token:** Allows actions on projects within the scoped workspace (cannot run `railway whoami` or `railway link` to other workspaces).
  - Example: `RAILWAY_API_TOKEN=your_api_token railway init`

*Note: `RAILWAY_TOKEN` takes precedence if both are set.*

### Logout
```bash
railway logout
```

## Project Management

### Create New Project
```bash
# Interactively prompts for project name and team
railway init

# Specify project name (team selection will be prompted if not clear)
railway init --name <your-project-name>
```

### Link to Existing Project
```bash
# Interactive selection of team, project, and environment
railway link

# Link to specific project ID and optionally environment
railway link --project <project-id>
railway link --project <project-id> --environment <environment-name>

# Link to a specific team, project, and environment
railway link --team <team-id-or-personal> --project <project-id> --environment <environment-name>
```

### List Projects
```bash
railway list
```

### Unlink Project
```bash
# Disconnects the current directory from the linked Railway project
railway unlink
```

### Project Status and Information
```bash
# Show current linked project, environment, service, and user status
railway status
```

## Environment Management

Projects can have multiple environments (e.g., production, staging). By default, CLI commands target the linked environment.

### Link/Switch Environment
```bash
# Interactively select an environment to link for the current project
railway environment

# Link to a specific environment by name
railway environment <environment-name>
```

### Create New Environment
```bash
# Interactively create a new environment
railway environment new

# Create a new environment with a specific name
railway environment new <new-environment-name>

# Duplicate an existing environment to a new one
railway environment new <new-environment-name> --duplicate <source-environment-name>
# Optionally override service variables when duplicating
railway environment new <new-env> --duplicate <source-env> --service-variable "<service-name-or-id>=MY_VAR=new_value"
```

### Delete Environment
```bash
# Interactively delete an environment
railway environment delete

# Delete a specific environment by name
railway environment delete <environment-name>

# Skip confirmation dialog
railway environment delete <environment-name> --yes
```

## Service Management

Services are the individual components of your project, like a backend API, a database, or a frontend application.

### Add Service (Databases, From Repo, From Docker Image)
```bash
# Interactively add a new service (e.g., PostgreSQL, MySQL, Redis, MongoDB) or link to an existing one
railway add

# Add a specific database service (e.g., postgres, mysql, redis, mongo)
railway add --database postgres

# Add a service from a Git repository
railway add --repo https://github.com/user/repo.git

# Add a service from a Docker image
railway add --image mydockerimage:latest

# Add a service and set initial environment variables
railway add --database redis --service my-cache --variables "CACHE_PORT=6379" "MAX_MEMORY=256mb"
# For service specific variables when adding a template based service (e.g. from `railway deploy -t <template>`)
# railway deploy -t postgres -v "Backend.POSTGRES_USER=admin"
```

### Select/Link Service
```bash
# Interactively select a service within the current project and environment to link to the current directory
railway service

# Link to a specific service by name or ID
railway service <service-name-or-id>
```

### Unlink Service
```bash
# Unlinks a service from the current directory context (project link remains)
railway unlink --service
```

### Service Information
```bash
# View the currently linked service via `railway status`
railway status
```

## Deployment Commands

### Deploy Project/Service (from local directory)
```bash
# Deploy the linked project/service from the current or specified directory
# Streams build and deployment logs by default.
railway up

# Deploy from a specific path (project root is still deployed if in subdirectory)
railway up ./my-app-subdirectory

# Detach from logs after starting the deployment
railway up --detach

# CI mode: Only stream build logs and exit after completion
railway up --ci

# Deploy to a specific service (if multiple services and not linked)
railway up --service <service-name-or-id>

# Deploy to a specific environment
railway up --environment <environment-name>

# Do not ignore paths from .gitignore
railway up --no-gitignore

# Enable verbose output for debugging
railway up --verbose
```

### Deploy Template
```bash
# Provision a template (e.g., a predefined stack or service) into your project
railway deploy --template <template-code>

# Deploy a template and set template-specific variables
# To specify a variable for a single service within the template, prefix with "{service}."
railway deploy --template <template-code> --variable "MY_VAR=value" --variable "MyServiceInTemplate.PORT=8080"
```

### Check Deployment Status
```bash
# Show overall project and deployment status
railway status

# Show recent deployments for the linked project/environment
# (The old `railway deployments` command functionality is covered by status and logs)
# For specific deployment history, refer to the Railway dashboard.
```

### Redeploy Last Successful Deployment
```bash
# Redeploy the currently deployed version of a service
railway redeploy

# Redeploy a specific service
railway redeploy --service <service-name-or-id>

# Skip confirmation
railway redeploy --yes
```

### Remove Last Deployment (Rollback alternative)
```bash
# Remove the most recent deployment for the linked service
# This can act as a form of rollback if the previous deployment becomes active.
railway down

# Skip confirmation
railway down --yes
```

### Rollback Deployment (Legacy - use `railway down` or `redeploy`)
*The `railway rollback <deployment-id>` command is not prominent in recent CLI versions.
Prefer using `railway down` to remove a bad deployment or `railway redeploy` to re-trigger a known good one. Check the Railway dashboard for specific deployment history and rollback options.*

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
