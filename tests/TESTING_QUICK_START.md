# Testing Quick Start Guide ⚡

This is the fastest way to get started with testing in this project.

## Prerequisites 📋

1. **Install dependencies**:
   ```bash
   uv pip install pytest allure-pytest
   brew install allure  # macOS (or see alternatives below)
   ```

2. **Make sure you're in the project root** (where `pytest.ini` exists)

## Super Quick Commands 🚀

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

### Running Tests - Two Main Ways

You can run tests in two main ways:

1. **By Suite** (using Allure suites):
   ```bash
   ./test_runner.sh group "smoke_tests"     # Run smoke test suite
   ./test_runner.sh group "regression"      # Run regression test suite
   ```

2. **By Test Marker** (using pytest markers):
   ```bash
   ./test_runner.sh all -k "smoke"          # Run tests marked as smoke
   ./test_runner.sh all -k "api"            # Run tests marked as API
   ./test_runner.sh all -k "not slow"       # Skip slow tests
   ./test_runner.sh all -k "smoke and api"  # Combine markers
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

## Pro Tips 💡

- **Default environment is `dev`** - safe for development
- **Allure reports open automatically** - use `-s` to skip
- **All pytest options work** - just add them at the end
- **Use tab completion** - scripts support standard bash completion
- **Choose the right approach**:
  - Use `group` for running test suites (e.g., "smoke_tests")
  - Use `-k` for flexible test selection by markers (e.g., smoke, api)
  - Combine both for maximum flexibility

## Quick Reference 🎯

```bash
# Most common commands
./test_runner.sh group "smoke_tests"       # Run smoke tests by suite
./test_runner.sh all -k "smoke"            # Run smoke tests by marker
./test_runner.sh all -k "api and not slow" # Complex marker selection
./test_runner.sh list-groups               # See available suites
```

## Need More Help? 📖

- **Detailed documentation**: `tests/utils/test_runners/README.md`
- **Script help**: `./test_runner.sh help`
- **Individual script help**: `./tests/utils/test_runners/run_all_tests.sh --help`

---

**Remember**: Always run from the project root directory! 🎯 