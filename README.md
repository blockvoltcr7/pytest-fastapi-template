# FastAPI Allure Pytest Template

This repository provides a quick start template for building APIs with FastAPI, testing with Pytest, and generating beautiful test reports using Allure. The goal is to enable developers to quickly create and deploy APIs to platforms like Render or Railway.

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
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

## Running the Application

To run the FastAPI application locally:

```bash
uvicorn app.main:app --reload
```

The application will typically be available at `http://127.0.0.1:8000`.

## Running Tests

This project uses Pytest for testing and Allure for reporting.

You can run tests directly with pytest, or use the provided shell scripts for more control over test execution and environment selection.

### Using Test Runner Scripts

Shell scripts are available in `tests/utils/test_runners/` to help you:
- Run all tests
- Run tests by group/feature
- Run tests by file
- Specify the environment to test against (dev, uat, prod)

**Examples:**

Run all tests in the default (dev) environment:
```bash
./tests/utils/test_runners/run_all_tests.sh
```

Run all tests in a specific environment:
```bash
./tests/utils/test_runners/run_all_tests.sh -e dev
```

Run tests by group:
```bash
./tests/utils/test_runners/run_by_group.sh -g "API Tests"
```

Run a specific test file:
```bash
./tests/utils/test_runners/run_by_file.sh -f tests/api/v1/test_hello.py
```

You can also pass additional pytest options to these scripts as needed.

For more details on test organization, environment configuration, and advanced usage, see [`tests/README.md`](tests/README.md).

1.  **Run Pytest tests and generate Allure results (direct):**
    ```bash
    pytest --alluredir=allure-results -v -s
    ```

2.  **Serve the Allure report:**
    ```bash
    allure serve allure-results
    ```
    This will open the report in your web browser.

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