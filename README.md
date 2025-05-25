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
├── requirements.in       # Main dependencies file for uv
├── requirements.lock     # Lock file for dependencies
├── requirements.txt      # Pinned dependencies generated from requirements.in
```

## Getting Started

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (Python package installer and virtual environment manager)
- Docker (optional, for containerized development and deployment)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/pytest-fast-api-template.git
    cd pytest-fast-api-template
    ```

2.  **Create and activate a virtual environment using uv:**
    ```bash
    uv venv
    source .venv/bin/activate  # On Unix/macOS
    # .venv\Scripts\activate    # On Windows
    ```

3.  **Install dependencies using uv:**
    ```bash
    uv pip install -r requirements.txt
    ```
    *Note: `requirements.txt` is generated from `requirements.in`. If you add new dependencies, add them to `requirements.in` and then run `uv pip compile requirements.in` to update `requirements.txt`.*

4.  **Set up environment variables (optional, for AI tests):**
    ```bash
    # Copy the example environment file
    cp .env.example .env
    
    # Edit .env and add your API keys
    # OPENAI_API_KEY=your_openai_api_key_here
    # ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
    ```
    *Note: The `.env` file is excluded from Git for security. Only add it if you plan to run AI integration tests.*

## Running the Application

To run the FastAPI application locally:

1. **Ensure your virtual environment is activated:**
   ```bash
   source .venv/bin/activate  # On Unix/macOS
   # .venv\Scripts\activate    # On Windows
   ```
   *You'll know the virtual environment is active when you see `(pytest-fastapi-template)` at the beginning of your terminal prompt.*

2. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

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
source .venv/bin/activate
uvicorn app.main:app --reload
```

### 🌟 Recommended: Use the Convenience Script

The easiest way to run tests is with our convenience script from the project root:

```bash
# Install testing dependencies first
uv pip install pytest allure-pytest
brew install allure  # macOS (or see alternatives in TESTING_QUICK_START.md)

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
   # Ensure virtual environment is activated first
   source .venv/bin/activate  # On Unix/macOS
   # .venv\Scripts\activate    # On Windows
   
   # Run all tests
   pytest -v -s
   ```

2. **Run tests with Allure reporting:**
   ```bash
   # Run tests and generate Allure results
   pytest --alluredir=allure-results -v -s
   
   # Serve the Allure report (opens in browser)
   allure serve allure-results
   ```

3. **Run specific tests:**
   ```bash
   # Run a specific test file
   pytest tests/test_fastapi_endpoints.py -v
   
   # Run a specific test method
   pytest tests/test_fastapi_endpoints.py::TestFastAPIEndpoints::test_root_endpoint -v
   
   # Run tests with specific markers
   pytest -m api -v
   
   # Run tests with keyword matching
   pytest -k "test_hello" -v
   ```

4. **Environment-specific testing:**
   ```bash
   # Run tests against a specific environment
   TEST_ENV=dev pytest --alluredir=allure-results -v
   TEST_ENV=uat pytest --alluredir=allure-results -v
   ```

## Troubleshooting

### Common Issues

**1. `ModuleNotFoundError: No module named 'fastapi'`**
- **Cause**: Virtual environment is not activated
- **Solution**: Run `source .venv/bin/activate` (Unix/macOS) or `.venv\Scripts\activate` (Windows)
- **Verification**: Your terminal prompt should show `(pytest-fastapi-template)` at the beginning

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
- **Cause**: Virtual environment not activated or dependencies not installed
- **Solution**: 
  ```bash
  source .venv/bin/activate
  uv pip install -r requirements.txt
  ```

**4. Tests fail with connection errors**
- **Cause**: FastAPI server is not running
- **Solution**: Start the server before running tests:
  ```bash
  # In one terminal
  source .venv/bin/activate
  uvicorn app.main:app --reload
  
  # In another terminal
  source .venv/bin/activate
  pytest --alluredir=allure-results -v -s
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

This template is designed for easy deployment to cloud platforms.

### Render

Refer to the `README_RENDER_DEPLOYMENT.md` file and `render.yaml` for detailed instructions on deploying to Render.

Key files:
- `render.yaml`
- `README_RENDER_DEPLOYMENT.md`
- `Dockerfile` (or rely on Render's native Python support)

### Railway

Refer to the `README_RAILWAY_DEPLOYMENT.md`, `README_RAILWAY_DEPLOYMENT_DETAILS.md`, and `RAILWAY_CLI_COMMANDS.md` files for comprehensive guidance on deploying to Railway.

Key files:
- `railway.json` / `railway-simple.json`
- `Dockerfile.railway`
- `deploy-railway.sh`
- `README_RAILWAY_DEPLOYMENT.md`
- `README_RAILWAY_DEPLOYMENT_DETAILS.md`
- `RAILWAY_CLI_COMMANDS.md`

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