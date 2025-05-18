# Docker Guide for Baby Podcast GenAI Project

This guide provides comprehensive instructions for containerizing and deploying the Baby Podcast GenAI project using Docker and Google Cloud.

## Table of Contents
- [Project Overview](#project-overview)
- [Docker Configuration](#docker-configuration)
- [Local Development](#local-development)
- [Deployment to Google Cloud](#deployment-to-google-cloud)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)

## Project Overview

The Baby Podcast GenAI project is a Python-based application focused on testing APIs using pytest and Allure reporting. 

## Docker Configuration

The project has been containerized using the following Docker files:

- **Dockerfile**: Defines the main container image, installing dependencies with UV
- **docker-compose.yml**: Orchestrates the application and Allure reporting containers
- **.dockerignore**: Excludes unnecessary files from the Docker build context
- **cloudbuild.yaml**: Defines Google Cloud Build configuration for automated builds and deployments

### Key Features of Our Docker Setup

- **Python-Based**: Uses Python 3.11 slim image for a smaller footprint
- **UV Package Management**: Uses UV for dependency management
- **Volume Mounting**: Preserves test reports between runs
- **Integrated Reporting**: Includes Allure reporting server for test results visualization
- **Cloud-Ready**: Configured for Google Cloud deployment

## Local Development

### Prerequisites

- Docker and Docker Compose installed on your local machine
- Git (to clone the repository)

### Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd baby-podcast-genai
   ```

2. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

3. View the Allure reports at `http://localhost:5050`

### Running Tests

The default Docker configuration runs all tests automatically. To run specific tests:

```bash
# Run a specific test file
docker-compose run app pytest tests/test_api_example.py --alluredir=allure-results

# Run tests with a specific marker
docker-compose run app pytest -m api --alluredir=allure-results
```

### Developing with Docker

For interactive development:

```bash
# Start an interactive shell in the container
docker-compose run --rm app /bin/bash

# Run tests manually from within the container
pytest tests/test_api_example.py --alluredir=allure-results
```

## Deployment to Google Cloud

### Prerequisites

- Google Cloud account with billing enabled
- Google Cloud CLI (`gcloud`) installed and configured
- Docker configured to work with Google Container Registry

### Deployment Steps

1. **Set up Google Cloud project**:
   ```bash
   gcloud projects create baby-podcast-genai --name="Baby Podcast GenAI"
   gcloud config set project baby-podcast-genai
   ```

2. **Enable required APIs**:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **Deploy using Cloud Build**:
   ```bash
   gcloud builds submit --config=cloudbuild.yaml .
   ```

4. **Access your deployed application**:
   The deployment URL will be displayed in the Cloud Build logs, or you can find it with:
   ```bash
   gcloud run services describe baby-podcast-genai --region=us-central1 --format='value(status.url)'
   ```

### CI/CD Integration

For continuous integration:

1. Connect your GitHub repository to Cloud Build:
   ```bash
   gcloud builds triggers create github \
     --repo-name=baby-podcast-genai \
     --repo-owner=YOUR_GITHUB_USERNAME \
     --branch-pattern=main \
     --build-config=cloudbuild.yaml
   ```

2. Each push to the main branch will trigger a build and deployment.

## Configuration Options

### Environment Variables

You can customize the Docker runtime with these environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `PYTHONUNBUFFERED` | Ensures Python output is sent straight to container logs | 1 |
| `CHECK_RESULTS_EVERY_SECONDS` | How often Allure checks for new results | 3 |
| `KEEP_HISTORY` | Whether Allure maintains report history | 1 |

### Custom Test Commands

To run custom test commands, modify the `command` section in `docker-compose.yml` or override at runtime:

```bash
docker-compose run app pytest -v --alluredir=allure-results tests/
```

## Troubleshooting

### Common Issues

1. **"Port already in use" error**:
   Change the port mapping in `docker-compose.yml`:
   ```yaml
   ports:
     - "5051:5050"  # Change 5050 to a different port
   ```

2. **Missing test results**:
   Ensure volume mounts are correct in `docker-compose.yml` and that the allure-results directory has write permissions.

3. **Dependency issues**:
   If new dependencies are added, rebuild the Docker image:
   ```bash
   docker-compose build --no-cache
   ```

### Logs and Debugging

To check container logs:
```bash
# View logs for all services
docker-compose logs

# View logs for a specific service
docker-compose logs app
docker-compose logs allure
```

For more detailed troubleshooting, access the container:
```bash
docker-compose exec app /bin/bash
``` 