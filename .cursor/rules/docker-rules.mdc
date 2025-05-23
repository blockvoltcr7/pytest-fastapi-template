---
description: 
globs: 
alwaysApply: false
---

# Docker Rules for GenAI Project

## Core Principles
- Always use the existing Docker setup files (Dockerfile, docker-compose.yml) as foundation
- Maintain separation between development, testing, and production environments
- Follow UV package management workflows for Python dependencies
- Preserve volume mounts for test results and reporting

## Container Structure
- Use python:3.11-slim as the base image
- Keep the /app working directory pattern
- Maintain the allure-results volume mounting
- Do not change service names without updating all references

## Dependency Management
- Always use `uv` for package management, never direct pip commands
- Any new package should be added to requirements.in first
- After modifying requirements.in, run `uv pip compile requirements.in`
- Rebuild images after dependency changes with `docker-compose build --no-cache`

## Testing Workflow
- Preserve the pytest and Allure reporting integration
- Maintain volume mapping between containers for test results
- Always include the `--alluredir=allure-results` flag with pytest commands
- Keep environment variable `PYTHONUNBUFFERED=1` to ensure logs are visible

## Dockerfile Modifications
- Maintain the build stages sequence (working dir, dependencies, code copy)
- Keep image size minimal - don't install unnecessary packages
- Always use multi-stage builds for production deployments
- Use specific version tags for base images, not 'latest'

## Security Rules
- Never hardcode credentials in Docker files
- Use environment variables or secrets management for sensitive data
- Validate no credentials are leaked in the Docker build context
- Scan images for vulnerabilities before deployment

## Google Cloud Integration
- Preserve the Cloud Run configuration in cloudbuild.yaml
- Always specify container regions and resource constraints
- Maintain proper image tagging with `$COMMIT_SHA` for versioning
- Follow least-privilege principle for service accounts

## Performance Optimization
- Keep the .dockerignore file updated to minimize build context
- Use layer caching efficiently (order dependencies before code)
- Optimize container resource allocation for Cloud Run
- Consider using Alpine-based images when appropriate

## Development Workflow
- Use docker-compose for local development and testing
- Run tests inside containers to ensure environment consistency
- Use named volumes for persistent data when appropriate
- Document all environment variables needed for container operation
