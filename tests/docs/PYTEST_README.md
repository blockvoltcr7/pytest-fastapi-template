# Test Automation Framework

This directory contains the test automation framework for the FastAPI template project. The framework is designed to be easy to use, maintainable, and compatible with both human users and LLMs.

## Quick Start Commands 🚀

```bash
# Run all tests (dev environment - default)
./test_runner.sh all

# Run specific test file
./test_runner.sh file tests/test_hello.py

# Run tests by suite
./test_runner.sh group "smoke_tests"

# Run tests by marker
./test_runner.sh all -k "smoke"

# See what's available
./test_runner.sh list-files
./test_runner.sh list-groups

# Get help
./test_runner.sh help
```

## Running Tests Without Shell Scripts 🔨

If you prefer not to use the shell scripts, you can run tests directly with pytest commands:

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_hello.py

# Run tests by marker
pytest -v -m "smoke"  # Run smoke tests
pytest -v -m "api"    # Run API tests
pytest -v -m "not slow"  # Skip slow tests

# Run tests with specific name pattern
pytest -k "test_api"  # Run tests with "test_api" in the name

# Run tests with Allure reporting
pytest --alluredir=allure-results

# Generate and serve Allure report
allure serve allure-results

# Set test environment
TEST_ENV=uat pytest  # Run tests against UAT environment
TEST_ENV=prod pytest # Run tests against production environment

# Common pytest options
pytest -v            # Verbose output
pytest -s            # Show print statements
pytest -x            # Stop on first failure
pytest -n auto      # Run tests in parallel
pytest --pdb        # Drop into debugger on failures
```

Note: The shell scripts provide additional convenience features and standardization, but direct pytest commands give you more flexibility and control when needed.

## Common Options 🔧

```bash
# Different environments
./test_runner.sh all -e uat
./test_runner.sh all -e prod

# Skip Allure report (faster for development)
./test_runner.sh all -s

# Quiet mode (less output)
./test_runner.sh all -q

# Run only specific tests
./test_runner.sh all -k "smoke"          # Run tests marked as smoke
./test_runner.sh all -k "api"            # Run tests marked as API
./test_runner.sh all -k "not slow"       # Skip slow tests

# Stop on first failure
./test_runner.sh all --maxfail=1
```

## Directory Structure

```
tests/
├── conftest.py                     # Global fixtures and configurations
├── config/                         # Test configurations
│   ├── environments/              # Environment-specific configs (dev, uat, prod)
│   └── config_loader.py          # Environment configuration loader
├── api/                            # API tests
│   ├── v1/                         # API version-specific tests
├── integration/                    # Integration tests
├── unit/                           # Unit tests
├── e2e/                            # End-to-end tests
└── utils/                          # Test utilities
    ├── test_runners/              # Test runner scripts
    └── helpers/                   # Test helper functions
```

## Test Categories

1. **API Tests** (`api/`): Tests for REST API endpoints
2. **Integration Tests** (`integration/`): Tests for external service integration (OpenAI, ElevenLabs)
3. **Unit Tests** (`unit/`): Tests for individual components and functions
4. **End-to-End Tests** (`e2e/`): Full flow tests simulating real user scenarios

## Test Organization 📚

Tests are organized using a combination of Allure decorators and pytest markers. Each serves a specific purpose:

### Allure Decorators (for reporting and organization)

```python
@allure.epic("Core API")              # Top-level grouping
@allure.feature("API Tests")          # Feature being tested
@allure.suite("smoke_tests")          # Test suite grouping (use with group command)
@allure.story("Root Endpoint")        # Individual test story
@allure.severity(allure.severity_level.CRITICAL)  # Test importance
```

### Pytest Markers (for test selection)

```python
@pytest.mark.api                      # API test marker
@pytest.mark.smoke                    # Smoke test marker
```

### Current Test Suites

Our current test organization:

```
Core API (epic)
└── API Tests (feature)
    └── smoke_tests (suite)  ← Use this with group command
        ├── Root Endpoint (story)
        ├── Hello World Endpoint (story)
        └── Basic Testing (story)
```

## Available Test Files 📄

```
tests/test_hello.py                        # Basic tests
tests/test_fastapi_endpoints.py            # API tests
tests/test_load_dot_env.py                 # Environment tests
tests/ai-tests/test_openai_integration.py  # AI integration
tests/ai-tests/test_openai_image_gen.py    # AI image generation
tests/utils/helpers/test_utils.py          # Utility tests
```

## Environment Configuration

The framework supports three environments:
- `dev`: Local development environment (default)
- `uat`: User Acceptance Testing environment
- `prod`: Production environment

Environment-specific configurations are stored in `tests/config/environments/`.

## Server Setup and Prerequisites

**Important**: The test framework assumes that the FastAPI server is **already running** on the configured port. Tests do not start their own server instance.

### For Development (dev environment):

1. **Start the FastAPI server** before running tests:
   ```bash
   # Ensure virtual environment is activated
   source .venv/bin/activate

   # Start the server on port 8000
   uvicorn app.main:app --reload
   ```

2. **Verify the server is running**:
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"healthy","message":"API is running successfully"}
   ```

### For Other Environments:
- **UAT**: Tests will use the configured UAT server URL
- **Production**: Tests will use the configured production server URL
- Server availability is verified by the test framework during execution

## Allure Reporting

All test runners automatically generate and serve Allure reports. The reports include:
- Test execution results
- Test steps and attachments
- Test grouping by features
- Test duration and trends
- Failure analysis
- Environment information

## Best Practices

1. **Test Independence**
   - Each test should be independent and self-contained
   - Clean up test data after execution
   - Don't rely on test execution order

2. **Test Data Management**
   - Use fixtures for test data
   - Avoid hardcoding test data
   - Use meaningful test data that represents real scenarios

3. **Assertions**
   - Use descriptive assertions
   - Include meaningful error messages
   - Test both positive and negative scenarios

4. **Documentation**
   - Document test purpose and requirements
   - Include examples in docstrings
   - Document any special setup requirements

5. **Maintenance**
   - Keep tests simple and focused
   - Follow DRY (Don't Repeat Yourself) principle
   - Regular cleanup of obsolete tests

## Troubleshooting 🔍

1. **"Must be run from project root"**:
   ```bash
   cd /path/to/project/root  # Where pytest.ini exists
   ./test_runner.sh all
   ```

2. **Missing dependencies**:
   ```bash
   uv pip install pytest allure-pytest

   # Install Allure CLI:
   # macOS: brew install allure
   # Windows: Download from GitHub releases
   # Linux: Use package manager or download from GitHub
   ```

3. **No tests found**:
   ```bash
   ./test_runner.sh list-files    # See available files
   ./test_runner.sh list-groups   # See available suites
   ```

4. **"No tests matched the group"**:
   ```bash
   ./test_runner.sh list-groups   # Check available suite names
   # Make sure you're using the exact suite name, e.g., "smoke_tests"
   ```

## Need More Help? 📖

- **Detailed documentation**: `tests/utils/test_runners/README.md`
- **Script help**: `./test_runner.sh help`
- **Individual script help**: `./tests/utils/test_runners/run_all_tests.sh --help`

---

**Remember**: Always run from the project root directory! 🎯
