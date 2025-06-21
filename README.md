# FastAPI Allure Pytest Template

This repository provides a quick start template for building APIs with FastAPI, testing with Pytest, and generating beautiful test reports using Allure. The goal is to enable developers to quickly create and deploy APIs to platforms like Render or Railway.

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
  - [Render](#render)
  - [Railway](#railway)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

The project is organized as follows:

```
.
├── app/                  # Main application code (FastAPI)
├── tests/                # Pytest tests
├── .github/              # GitHub Actions workflows (if any)
├── .venv/                # Virtual environment
├── allure-results/       # Allure test results
├── output/               # General output directory
├── docs/                 # Project documentation
├── .dockerignore         # Specifies intentionally untracked files that Docker should ignore
├── .gitignore            # Specifies intentionally untracked files that Git should ignore
├── cloudbuild.yaml       # Google Cloud Build configuration
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Dockerfile for building the application image
├── Dockerfile.railway    # Dockerfile specific to Railway deployment
├── Dockerfile.original   # Original Dockerfile (backup or alternative)
├── deploy-railway.sh     # Script for deploying to Railway
├── deploy.sh             # General deployment script
├── get-pip.py            # Script to install pip
├── pytest.ini            # Pytest configuration
├── railway-simple.json   # Simplified Railway configuration
├── railway.json          # Railway configuration
├── README_RAILWAY_DEPLOYMENT.md # Detailed Railway deployment instructions
├── README_RAILWAY_DEPLOYMENT_DETAILS.md # Additional Railway deployment details
├── RAILWAY_CLI_COMMANDS.md # Railway CLI commands
├── README_RENDER_DEPLOYMENT.md # Detailed Render deployment instructions
├── render.yaml           # Render configuration
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock               # Lock file for exact dependency versions
```

## Getting Started

### Prerequisites

- Python 3.11+ (matches the pinned dependency set)
- [uv](https://docs.astral.sh/uv/) (Python package installer and virtual environment manager)
- Docker (optional, for containerized development and deployment)

#### Install UV

Choose one of these methods:
```bash
# Recommended: Install via pipx
pipx install uv

# Alternative: Install via pip
pip install uv

# macOS: Install via Homebrew
brew install uv

# Windows: Install via winget
winget install --id=astral-sh.uv -e
```

Verify installation:
```bash
uv --version
```

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/pytest-fastapi-template.git
    cd pytest-fastapi-template
    ```

2.  **Install dependencies and set up virtual environment (one command!):**
    ```bash
    uv sync
    ```

    This single command:
    - Creates a virtual environment in `.venv/`
    - Installs all dependencies from `pyproject.toml` and `uv.lock`
    - Sets up the project in editable mode
    - No need to manually create or activate the virtual environment!

3.  **Set up environment variables (optional, for AI tests):**
    ```bash
    # Copy the example environment file (if it exists)
    cp .env.example .env

    # Edit .env and add your API keys
    # OPENAI_API_KEY=your_openai_api_key_here
    # ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
    ```
    *Note: The `.env` file is excluded from Git for security. Only add it if you plan to run AI integration tests.*

#### Alternative: Manual Virtual Environment Setup

If you prefer to manage the virtual environment manually:
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Unix/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
uv sync
```

## Running the Application

To run the FastAPI application locally:

**Option 1 - Using `uv run` (Recommended):**
```bash
# Run directly without activating virtual environment
uv run uvicorn app.main:app --reload
```

**Option 2 - With activated virtual environment:**
```bash
# Activate virtual environment
source .venv/bin/activate  # Unix/macOS
# .venv\Scripts\activate    # Windows

# Start the server
uvicorn app.main:app --reload
```

*Note: `uv run` automatically uses the project's virtual environment, so you don't need to manually activate it.*

The application will be available at `http://127.0.0.1:8000`.

**Available endpoints:**
- Health check: `http://127.0.0.1:8000/health`
- API documentation: `http://127.0.0.1:8000/docs`
- Hello World: `http://127.0.0.1:8000/api/v1/hello`

**Note:** If you get a `ModuleNotFoundError: No module named 'fastapi'` error, it means your virtual environment is not activated. Make sure to run `source .venv/bin/activate` first.

## Running Tests

This project uses Pytest for testing and Allure for reporting with **enhanced test runners** for the best developer experience.

**Important**: Before running tests, ensure the FastAPI server is running:
```bash
# Start the server in a separate terminal
uv run uvicorn app.main:app --reload

# Or with activated environment:
# source .venv/bin/activate
# uvicorn app.main:app --reload
```

### 🌟 Recommended: Use the Convenience Script

The easiest way to run tests is with our convenience script from the project root:

```bash
# Testing dependencies are already installed via uv sync
# Install allure for report generation
brew install allure  # macOS
# or follow allure installation guide for other platforms

# Super simple test commands (defaults to dev environment)
./test_runner.sh all                              # Run all tests
./test_runner.sh file tests/test_hello.py         # Run specific file
./test_runner.sh group "API Tests"                # Run by feature group
./test_runner.sh group "smoke_tests"              # Run smoke tests
./test_runner.sh list-files                       # See available files
./test_runner.sh list-groups                      # See available groups

# With options
./test_runner.sh all -e uat                       # Different environment
./test_runner.sh all -k "smoke"                   # Run smoke tests by marker
./test_runner.sh all -q                           # Quiet mode

# Or run tests directly with uv
uv run pytest                                     # Run all tests
uv run pytest tests/test_hello.py                # Run specific file
uv run pytest --alluredir=allure-results -v     # Generate allure reports
```

### Test Organization

Tests are organized using Allure decorators in a hierarchical structure:

```
Core API (epic)
└── API Tests (feature)
    └── smoke_tests (suite)
        ├── Root Endpoint (story)
        ├── Hello World Endpoint (story)
        └── Basic Testing (story)
```

You can run tests at any level:
```bash
./test_runner.sh group "Core API"        # Run all Core API tests
./test_runner.sh group "API Tests"       # Run all API tests
./test_runner.sh group "smoke_tests"     # Run smoke tests
```

**👉 For detailed instructions, see [TESTING_QUICK_START.md](TESTING_QUICK_START.md)**

### Advanced: Use Test Runner Scripts Directly

For more control, use the enhanced test runner scripts:

```bash
# Run all tests
./tests/utils/test_runners/run_all_tests.sh

# Run specific test file
./tests/utils/test_runners/run_by_file.sh -f tests/test_hello.py

# Run tests by feature group
./tests/utils/test_runners/run_by_group.sh -g "API Endpoints"

# All scripts support these options:
# -e <env>     Environment (dev/uat/prod) [default: dev]
# -s, --skip   Skip opening Allure report automatically
# -q, --quiet  Run with minimal output
# -h, --help   Show help

# List available tests/groups
./tests/utils/test_runners/run_by_file.sh -l      # List test files
./tests/utils/test_runners/run_by_group.sh -l     # List feature groups
```

**👉 For comprehensive documentation, see [tests/utils/test_runners/README.md](tests/utils/test_runners/README.md)**

### Direct Pytest Commands

For maximum flexibility, you can run tests directly with pytest:

1. **Basic test execution:**
   ```bash
   # Option 1: Using uv run (recommended)
   uv run pytest -v -s

   # Option 2: With activated virtual environment
   source .venv/bin/activate  # Unix/macOS
   # .venv\Scripts\activate    # Windows
   pytest -v -s
   ```

2. **Run tests with Allure reporting:**
   ```bash
   # Run tests and generate Allure results
   uv run pytest --alluredir=allure-results -v -s

   # Serve the Allure report (opens in browser)
   allure serve allure-results
   ```

3. **Run specific tests:**
   ```bash
   # Run a specific test file
   uv run pytest tests/test_fastapi_endpoints.py -v

   # Run a specific test method
   uv run pytest tests/test_fastapi_endpoints.py::TestFastAPIEndpoints::test_root_endpoint -v

   # Run tests with specific markers
   uv run pytest -m api -v

   # Run tests with keyword matching
   uv run pytest -k "test_hello" -v
   ```

4. **Environment-specific testing:**
   ```bash
   # Run tests against a specific environment
   uv run --env TEST_ENV=dev pytest --alluredir=allure-results -v
   uv run --env TEST_ENV=uat pytest --alluredir=allure-results -v
   ```

## Troubleshooting

### Common Issues

**1. `ModuleNotFoundError: No module named 'fastapi'`**
- **Cause**: Dependencies not installed or virtual environment not set up
- **Solution**:
  ```bash
  # Reinstall dependencies
  uv sync

  # Or use uv run to run commands
  uv run uvicorn app.main:app --reload
  ```
- **Verification**: `uv run python -c "import fastapi; print('FastAPI installed')"` should work

**2. `ERROR: [Errno 48] Address already in use`**
- **Cause**: Another instance of the server is already running on port 8000
- **Solution**: Kill the existing process or use a different port:
  ```bash
  # Find and kill the process
  lsof -ti:8000 | xargs kill -9

  # Or run on a different port
  uvicorn app.main:app --reload --port 8001
  ```

**3. Import errors in tests**
- **Cause**: Dependencies not installed or virtual environment not set up properly
- **Solution**:
  ```bash
  # Reinstall all dependencies
  uv sync

  # Verify installation
  uv run python -c "import app; print('App module available')"
  ```

**4. Tests fail with connection errors**
- **Cause**: FastAPI server is not running
- **Solution**: Start the server before running tests:
  ```bash
  # In one terminal
  uv run uvicorn app.main:app --reload

  # In another terminal
  uv run pytest --alluredir=allure-results -v -s
  ```

**5. AI tests fail with "OPENAI_API_KEY not found" error**
- **Cause**: Environment variables not properly loaded from .env file
- **Solution**: Ensure .env file is set up correctly:
  ```bash
  # Copy the example file and add your API keys
  cp .env.example .env
  # Edit .env file and add: OPENAI_API_KEY=your_actual_api_key_here

  # Test that environment loading works
  pytest tests/ai-tests/test_openai_integration.py -v
  ```

## Deployment

This template is designed for easy deployment to cloud platforms with full UV support.

### Quick Deploy Checklist

Before deploying to any platform:

1. **Ensure your code is production-ready:**
   ```bash
   # Run all tests
   uv run pytest

   # Verify the app starts correctly
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Update dependencies and lock file:**
   ```bash
   # Add any production dependencies
   uv add gunicorn  # For production WSGI server

   # Ensure lock file is up to date
   uv lock
   ```

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

### Render Deployment

Render now supports UV natively for faster builds.

**Option 1: Using UV (Recommended)**

1. **Create `render.yaml` configuration:**
   ```yaml
   services:
     - type: web
       name: fastapi-app
       env: python
       region: oregon
       plan: free
       buildCommand: |
         pip install uv
         uv sync --no-dev
       startCommand: uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: PYTHON_VERSION
           value: 3.11
   ```

2. **Deploy to Render:**
   - Connect your GitHub repository to Render
   - Render will automatically use the `render.yaml` configuration
   - Build time is significantly faster with UV

**Option 2: Using Dockerfile**

Update your Dockerfile to use UV:
```dockerfile
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY . /app
WORKDIR /app

# Install dependencies with UV
RUN uv sync --no-dev

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Railway Deployment

Railway also supports UV for faster, more reliable deployments.

1. **Update `railway.json` for UV:**
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS",
       "buildCommand": "pip install uv && uv sync --no-dev"
     },
     "deploy": {
       "startCommand": "uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

2. **Deploy using Railway CLI:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login to Railway
   railway login

   # Deploy the project
   railway up
   ```

3. **Or deploy via GitHub integration:**
   - Connect your repository to Railway
   - Railway will automatically detect the configuration
   - Builds are faster and more reliable with UV

### Docker Deployment (General)

For containerized deployments on any platform:

```dockerfile
# Use Python 3.11 slim base image
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy project configuration
COPY pyproject.toml uv.lock ./

# Install dependencies (production only)
RUN uv sync --frozen --no-dev

# Copy application code
COPY ./app ./app

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

Set these environment variables in your deployment platform:

```bash
# Required
PORT=8000                    # Port for the application
PYTHON_ENV=production        # Environment setting

# Optional (if using AI features)
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here

# Database (if you add database support)
DATABASE_URL=your_db_url_here
```

### Performance Optimization

For production deployments:

1. **Add production dependencies:**
   ```bash
   # Add production server
   uv add gunicorn

   # Add performance monitoring (optional)
   uv add prometheus-client
   ```

2. **Use production ASGI server:**
   ```bash
   # Instead of uvicorn directly, use gunicorn with uvicorn workers
   uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Update start command in deployment configs:**
   ```yaml
   # render.yaml
   startCommand: uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

### Monitoring and Logging

Add monitoring to your deployed application:

```python
# In app/main.py
import logging
from fastapi import FastAPI
from prometheus_client import Counter, generate_latest

app = FastAPI()

# Metrics
request_counter = Counter('http_requests_total', 'Total HTTP requests')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    request_counter.inc()
    response = await call_next(request)
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Platform-Specific Documentation

For detailed platform-specific instructions, refer to:

- **Render**: `README_RENDER_DEPLOYMENT.md`
- **Railway**: `README_RAILWAY_DEPLOYMENT.md` and `RAILWAY_CLI_COMMANDS.md`
- **UV Management**: `docs/uv-management/README.md`

All deployment methods now use UV for faster, more reliable builds and dependency resolution.

## Dependency Management Best Practices

### Adding New Dependencies

When adding new packages to the project:

```bash
# Add runtime dependency
uv add requests

# Add development dependency (for testing, linting, etc.)
uv add --dev black ruff mypy

# Add with version constraints
uv add "fastapi>=0.100.0,<1.0.0"

# Add from Git repository
uv add "git+https://github.com/user/repo.git"
```

### Updating Dependencies

```bash
# Update all dependencies to latest compatible versions
uv sync --upgrade

# Update specific dependency
uv add "fastapi@latest"

# Check for outdated packages
uv tree --outdated
```

### Managing Development vs Production

```bash
# Install all dependencies (dev + production)
uv sync

# Install only production dependencies
uv sync --no-dev

# Add development-only dependencies
uv add --dev pytest pytest-cov black ruff
```

### Version Control

Always commit both files:
- `pyproject.toml` - Contains dependency specifications
- `uv.lock` - Contains exact versions for reproducible builds

```bash
git add pyproject.toml uv.lock
git commit -m "Update dependencies"
```

### Troubleshooting Dependencies

```bash
# Clear UV cache if experiencing issues
uv cache clean

# Recreate lock file
rm uv.lock
uv lock

# Reinstall all dependencies
rm -rf .venv
uv sync
```

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to the project's coding standards and that all tests pass.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (if one exists, otherwise specify your chosen license).
