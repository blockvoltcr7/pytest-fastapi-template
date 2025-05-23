# Docker Configuration Guide for GenAI Project

This document outlines the steps to configure your GenAI project with Docker.

## Initial Setup

1. **Copy Docker Files to Project Root**

   Make sure these files are in your project root:
   - `Dockerfile`
   - `docker-compose.yml`
   - `.dockerignore`
   - `cloudbuild.yaml` (for Google Cloud deployment)

2. **Install Docker Prerequisites**

   Ensure you have Docker and Docker Compose installed:
   ```bash
   # Check installations
   docker --version
   docker-compose --version
   ```

## Project Configuration

### 1. Configure Environment Variables

Create a `.env` file in your project root (optional but recommended):

```bash
# API configuration
API_BASE_URL=https://httpbin.org

# Test configuration
ALLURE_RESULTS_DIR=./allure-results
```

### 2. Custom Test Configuration

Modify `pytest.ini` if you need special test configurations:

```ini
[pytest]
# Enable Allure reporting by default
addopts = --alluredir=allure-results

# Add any other test configuration needed
```

### 3. Update Docker Image Configuration (if needed)

If you need to customize the Docker image, modify the `Dockerfile`:

```dockerfile
# Use a different Python version
FROM python:3.9-slim

# Add additional system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Rest of Dockerfile remains the same
```

### 4. Configure Volume Mounts (if needed)

Modify volume mounts in `docker-compose.yml` if you need to persist additional data:

```yaml
volumes:
  - ./allure-results:/app/allure-results
  - ./custom-data:/app/custom-data
```

## Working with Secrets

For handling secrets and credentials:

1. **Local Development**

   Use environment variables in `docker-compose.yml`:
   ```yaml
   environment:
     - API_KEY=${API_KEY}
   ```

2. **Google Cloud Deployment**

   Set up secrets in Google Cloud Secret Manager:
   ```bash
   # Create a secret
   echo -n "your-api-key" | gcloud secrets create api-key --data-file=-
   
   # Reference in Cloud Run
   gcloud run deploy pytest-fast-api-template \
     --image=gcr.io/PROJECT_ID/pytest-fast-api-template \
     --update-secrets=API_KEY=api-key:latest
   ```

## Custom Extensions

### Adding Custom Python Packages

1. **Update requirements.in**:
   ```
   # Add your package
   your-new-package
   ```

2. **Compile requirements.txt**:
   ```bash
   # Using UV (preferred as per project standards)
   uv pip compile requirements.in
   ```

3. **Rebuild Docker image**:
   ```bash
   docker-compose build --no-cache
   ```

### Adding System Dependencies

If your project requires system packages (e.g., ffmpeg):

1. **Update Dockerfile**:
   ```dockerfile
   # Add after FROM line
   RUN apt-get update && apt-get install -y \
       ffmpeg \
       && rm -rf /var/lib/apt/lists/*
   ```

2. **Rebuild Docker image**:
   ```bash
   docker-compose build --no-cache
   ```

## Google Cloud Configuration

### Setting Up Cloud Run

1. **Configure your service**:
   ```bash
   gcloud run services update pytest-fast-api-template \
     --memory=512Mi \
     --cpu=1 \
     --timeout=300 \
     --concurrency=80
   ```

2. **Set up a custom domain** (optional):
   ```bash
   gcloud beta run domain-mappings create \
     --service=pytest-fast-api-template \
     --domain=api.example.com
   ```

### Cost Optimization

To optimize costs when running on Google Cloud:

1. **Use CPU always allocated** only if necessary:
   ```bash
   gcloud run services update pytest-fast-api-template --no-cpu-always-allocated
   ```

2. **Set minimum instances to 0** for serverless scaling:
   ```bash
   gcloud run services update pytest-fast-api-template --min-instances=0
   ```

## Verification and Validation

After configuration, verify your setup:

```bash
# Check Docker configuration
docker-compose config

# Run tests locally
docker-compose up --build

# Verify Allure reports
# Open http://localhost:5050 in your browser
``` 