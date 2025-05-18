# Docker Quick Reference for Baby Podcast GenAI

## Common Docker Commands

### Building and Running

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode (background)
docker-compose up -d

# Stop all services
docker-compose down

# Rebuild without using cache
docker-compose build --no-cache
```

### Running Tests

```bash
# Run all tests
docker-compose run app pytest

# Run specific test file
docker-compose run app pytest tests/test_api_example.py

# Run with specific marker
docker-compose run app pytest -m api

# Run with increased verbosity
docker-compose run app pytest -v
```

### Container Management

```bash
# List running containers
docker-compose ps

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs app

# Follow logs (continuous)
docker-compose logs -f

# Access container shell
docker-compose exec app bash

# Run one-off command
docker-compose run --rm app python -c "print('Hello')"
```

### Volume Management

```bash
# Clear allure results
sudo rm -rf allure-results/*

# Inspect volumes
docker volume ls
```

### Google Cloud Commands

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/baby-podcast-genai

# Deploy to Cloud Run
gcloud run deploy baby-podcast-genai \
  --image gcr.io/PROJECT_ID/baby-podcast-genai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Environment Variables

Common environment variables used in the project:

| Variable | Purpose | Where to Set |
|----------|---------|-------------|
| API_BASE_URL | Base URL for API tests | docker-compose.yml or .env |
| PYTHONUNBUFFERED | Force Python output unbuffering | docker-compose.yml |
| CHECK_RESULTS_EVERY_SECONDS | Allure refresh rate | docker-compose.yml |

## Container Specs

The Baby Podcast GenAI project uses two main containers:

1. **app** - Python application container  
   Base: python:3.11-slim  
   Primary purpose: Run tests and generate reports

2. **allure** - Allure reporting server  
   Base: frankescobar/allure-docker-service  
   Primary purpose: Display test results

## Volume Mount Reference

| Path in Container | Path on Host | Purpose |
|-------------------|--------------|---------|
| /app/allure-results | ./allure-results | Store Allure test reports |

## Port Mapping

| Container Port | Host Port | Service |
|----------------|-----------|---------|
| 5050 | 5050 | Allure report server | 