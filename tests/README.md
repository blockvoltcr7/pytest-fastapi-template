# Test Automation Framework

This directory contains the test automation framework for the FastAPI template project. The framework is designed to be easy to use, maintainable, and compatible with both human users and LLMs.

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

## Environment Configuration

The framework supports three environments:
- `dev`: Local development environment
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

3. **Run tests** (server must be running first):
   ```bash
   ./tests/utils/test_runners/run_all_tests.sh
   ```

### For Other Environments:

- **UAT**: Tests will use the configured UAT server URL
- **Production**: Tests will use the configured production server URL
- Server availability is verified by the test framework during execution

### Why This Approach?

- **No conflicts**: Avoids port conflicts and server startup issues
- **Realistic testing**: Tests run against the actual server as users would interact with it
- **Faster execution**: No time spent starting/stopping servers for each test run
- **Flexibility**: Can test against local, remote, or containerized servers

## Running Tests

### Using Test Runner Scripts

The framework provides three main test runner scripts with environment support:

1. Run All Tests:
```bash
# Run all tests in dev environment (default)
./tests/utils/test_runners/run_all_tests.sh

# Run all tests in specific environment
./tests/utils/test_runners/run_all_tests.sh -e uat
```

2. Run Tests by Group/Feature:
```bash
# Run group tests in dev environment
./tests/utils/test_runners/run_by_group.sh -g "API Tests"

# Run group tests in specific environment
./tests/utils/test_runners/run_by_group.sh -g "API Tests" -e prod
```

3. Run Tests by File:
```bash
# Run specific file in dev environment
./tests/utils/test_runners/run_by_file.sh -f tests/api/v1/test_hello.py

# Run specific file in specific environment
./tests/utils/test_runners/run_by_file.sh -f tests/api/v1/test_hello.py -e uat
```

### Additional Options

You can pass additional pytest options to any runner script after the main arguments:

```bash
# Run with specific marker and environment
./tests/utils/test_runners/run_all_tests.sh -e prod -k "test_specific_function"
```

## Allure Reporting

All test runners automatically generate and serve Allure reports. The reports include:
- Test execution results
- Test steps and attachments
- Test grouping by features
- Test duration and trends
- Failure analysis
- Environment information

## Test Organization

### 1. Test Files

- Name test files with prefix `test_`
- Use descriptive names: `test_user_authentication.py`
- Group related tests in classes: `TestUserAuthentication`

### 2. Test Cases

- Use descriptive test names: `test_login_with_valid_credentials`
- Include docstrings explaining test purpose
- Use Allure decorators for organization:
  ```python
  @allure.epic("Authentication")
  @allure.feature("User Login")
  @allure.story("Valid Credentials")
  def test_login_with_valid_credentials():
      """Test user login with valid username and password."""
  ```

### 3. Fixtures

- Define reusable fixtures in `conftest.py`
- Use appropriate scope (function, class, module, session)
- Document fixture purpose and usage

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

## Environment-Specific Testing

### 1. Configuration Access

Access environment configuration in tests:
```python
from tests.config.config_loader import config

def test_api_endpoint():
    base_url = config.API_BASE_URL
    endpoint = config.API_HELLO_ENDPOINT
```

### 2. Environment Variables

- `TEST_ENV`: Set by test runners, determines which environment config to load
- Default environment: `dev`
- Valid environments: `dev`, `uat`, `prod`

## For LLM Users

When writing or modifying tests, follow these guidelines:

1. **Test Structure**
   ```python
   @allure.epic("Feature Area")
   @allure.feature("Specific Feature")
   class TestFeature:
       @allure.story("Test Scenario")
       @allure.severity(allure.severity_level.NORMAL)
       def test_specific_scenario(self):
           with allure.step("First step description"):
               # Test code
               pass
   ```

2. **Adding New Tests**
   - Place in appropriate directory based on test type
   - Follow existing naming conventions
   - Include all necessary imports
   - Add proper Allure decorators
   - Consider environment-specific requirements

3. **Using Fixtures**
   - Import fixtures from conftest.py
   - Document fixture requirements in test docstring
   - Create new fixtures in conftest.py if needed

4. **Error Handling**
   - Include appropriate try-except blocks
   - Add error details to Allure report
   - Use pytest.raises for expected exceptions

## Continuous Integration

The framework is designed to work with CI/CD pipelines:
- Generates JUnit XML reports
- Produces Allure reports
- Supports parallel test execution
- Configurable test selection and filtering
- Environment-specific test execution 