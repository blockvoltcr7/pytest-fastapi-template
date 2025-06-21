# Test Runners - User Guide 🚀

This directory contains improved shell scripts for running tests with enhanced user experience, better error handling, and comprehensive Allure reporting. These scripts make it easy to run tests in different configurations and environments.

## 🌟 Super Quick Start (Recommended)

We've created a convenience script in the project root for the easiest possible experience:

```bash
# From project root directory, use the convenience script:
./test_runner.sh all                              # Run all tests (dev)
./test_runner.sh file tests/test_hello.py         # Run specific file
./test_runner.sh group "API Endpoints"            # Run by feature group
./test_runner.sh list-files                       # See available files
./test_runner.sh list-groups                      # See available groups
./test_runner.sh help                             # Get help

# All options work the same way:
./test_runner.sh all -e uat -k "smoke" -s         # UAT, smoke tests, skip report
```

## Quick Start 🏃‍♂️

### Prerequisites

---

## Gemini Podcast Test Runner 🗣️☕

A dedicated script is provided for running the Gemini podcast AI tests and generating an Allure report automatically.

**Script location:** `tests/utils/test_runners/run_gemini_podcast_tests.sh`

### Usage

```bash
# From the project root, run:
./tests/utils/test_runners/run_gemini_podcast_tests.sh
```

- This will:
  - Clean previous Allure and pytest results
  - Run only the Gemini podcast test suite
  - Generate and open the Allure report in your browser

> **Tip:** If you get a permission error, run:
> ```bash
> chmod +x tests/utils/test_runners/run_gemini_podcast_tests.sh
> ```

---

1. **Install Dependencies**:
   ```bash
   # Install Python testing dependencies
   uv pip add pytest allure-pytest

   # Install Allure CLI (choose one):
   # macOS:
   brew install allure

   # Other platforms:
   # Download from: https://github.com/allure-framework/allure2/releases
   ```

2. **Navigate to Project Root**:
   ```bash
   cd /path/to/your/project  # Must have pytest.ini and tests/ directory
   ```

### Basic Usage

All scripts **must be run from the project root directory** and will automatically default to the `dev` environment:

```bash
# Option 1: Use convenience script (RECOMMENDED)
./test_runner.sh all
./test_runner.sh file tests/test_hello.py
./test_runner.sh group "API Endpoints"

# Option 2: Use direct scripts
./tests/utils/test_runners/run_all_tests.sh
./tests/utils/test_runners/run_by_file.sh -f tests/test_hello.py
./tests/utils/test_runners/run_by_group.sh -g "API Endpoints"
```

## Available Scripts 📋

### 1. `run_all_tests.sh` - Run All Tests

Runs all tests in the project with comprehensive reporting.

**Basic Syntax:**
```bash
./tests/utils/test_runners/run_all_tests.sh [OPTIONS] [PYTEST_ARGS...]
# OR
./test_runner.sh all [OPTIONS] [PYTEST_ARGS...]
```

**Options:**
- `-e <env>`: Environment (dev/uat/prod) [default: dev]
- `-h, --help`: Show help message
- `-s, --skip`: Skip opening Allure report automatically
- `-q, --quiet`: Run with minimal output

**Examples:**
```bash
# Simple - run all tests in dev
./test_runner.sh all

# Different environment
./test_runner.sh all -e uat

# Run only smoke tests
./test_runner.sh all -k "smoke"

# Verbose output, skip report
./test_runner.sh all -v -s

# Stop after first failure
./test_runner.sh all --maxfail=1

# Quiet mode for CI/CD
./test_runner.sh all -q
```

### 2. `run_by_file.sh` - Run Specific Test File

Runs tests from a specific test file.

**Basic Syntax:**
```bash
./tests/utils/test_runners/run_by_file.sh -f <test_file> [OPTIONS] [PYTEST_ARGS...]
# OR
./test_runner.sh file <test_file> [OPTIONS] [PYTEST_ARGS...]
```

**Required:**
- `-f <file>`: Path to test file (required for direct script)
- `<test_file>`: Test file path (for convenience script)

**Options:**
- `-e <env>`: Environment (dev/uat/prod) [default: dev]
- `-h, --help`: Show help message
- `-s, --skip`: Skip opening Allure report automatically
- `-q, --quiet`: Run with minimal output
- `-l, --list`: List available test files

**Examples:**
```bash
# Run specific test file (convenience script)
./test_runner.sh file tests/test_hello.py

# Run specific test file (direct script)
./tests/utils/test_runners/run_by_file.sh -f tests/test_hello.py

# Different environment
./test_runner.sh file tests/test_fastapi_endpoints.py -e uat

# AI tests
./test_runner.sh file tests/ai-tests/test_openai_integration.py

# List available test files
./test_runner.sh list-files

# Run with pytest verbose mode
./test_runner.sh file tests/test_hello.py -v
```

### 3. `run_by_group.sh` - Run Tests by Feature Group

Runs tests by Allure feature group (based on `@allure.feature` decorators).

**Basic Syntax:**
```bash
./tests/utils/test_runners/run_by_group.sh -g <group_name> [OPTIONS] [PYTEST_ARGS...]
# OR
./test_runner.sh group <group_name> [OPTIONS] [PYTEST_ARGS...]
```

**Required:**
- `-g <group>`: Allure feature group name (required for direct script)
- `<group_name>`: Group name (for convenience script)

**Options:**
- `-e <env>`: Environment (dev/uat/prod) [default: dev]
- `-h, --help`: Show help message
- `-s, --skip`: Skip opening Allure report automatically
- `-q, --quiet`: Run with minimal output
- `-l, --list`: List available test groups/features

**Examples:**
```bash
# Run API endpoint tests (convenience script)
./test_runner.sh group "API Endpoints"

# Run API endpoint tests (direct script)
./tests/utils/test_runners/run_by_group.sh -g "API Endpoints"

# Run OpenAI tests in UAT
./test_runner.sh group "OpenAI API" -e uat

# List available groups
./test_runner.sh list-groups

# Run FastAPI tests
./test_runner.sh group "FastAPI Application"
```

## Available Test Markers 🏷️

Use these markers with the `-k` option to filter tests:

- `api` - API integration tests
- `integration` - Integration tests
- `smoke` - Quick smoke tests
- `slow` - Slower running tests

**Examples:**
```bash
# Run only API tests
./tests/utils/test_runners/run_all_tests.sh -k "api"

# Run smoke tests in UAT
./tests/utils/test_runners/run_all_tests.sh -e uat -k "smoke"

# Exclude slow tests
./tests/utils/test_runners/run_all_tests.sh -k "not slow"
```

## Environment Configuration 🌍

### Available Environments

- **dev** (default) - Development environment
- **uat** - User Acceptance Testing environment
- **prod** - Production environment

### Environment Setup

The scripts automatically set the `TEST_ENV` environment variable for your tests. Make sure your test configuration can read this value.

**Example in conftest.py:**
```python
import os
test_env = os.getenv('TEST_ENV', 'dev')
```

## Advanced Usage 🔧

### Combining Options

```bash
# Run API tests in UAT with verbose output, skip report
./tests/utils/test_runners/run_all_tests.sh -e uat -k "api" -v -s

# Run specific file in prod with custom pytest options
./tests/utils/test_runners/run_by_file.sh -f tests/test_hello.py -e prod --tb=line

# Quiet mode for CI pipelines
./tests/utils/test_runners/run_all_tests.sh -q -e uat --junitxml=results.xml
```

### Custom Pytest Arguments

All additional arguments are passed directly to pytest:

```bash
# Custom output format
./tests/utils/test_runners/run_all_tests.sh --tb=short

# Stop on first failure
./tests/utils/test_runners/run_all_tests.sh --maxfail=1

# Run with coverage
./tests/utils/test_runners/run_all_tests.sh --cov=app

# Custom markers
./tests/utils/test_runners/run_all_tests.sh -m "not slow"
```

## Getting Help 📚

### Built-in Help

Each script has built-in help:

```bash
./tests/utils/test_runners/run_all_tests.sh --help
./tests/utils/test_runners/run_by_file.sh --help
./tests/utils/test_runners/run_by_group.sh --help
```

### Discovery Commands

```bash
# List all test files
./tests/utils/test_runners/run_by_file.sh -l

# List all feature groups
./tests/utils/test_runners/run_by_group.sh -l
```

## Troubleshooting 🔍

### Common Issues

1. **"Must be run from project root"**
   ```bash
   # ❌ Wrong
   cd tests/utils/test_runners
   ./run_all_tests.sh

   # ✅ Correct
   cd /path/to/project/root
   ./tests/utils/test_runners/run_all_tests.sh
   ```

2. **Missing dependencies**
   ```bash
   # Install missing dependencies
   uv pip install pytest allure-pytest
   brew install allure  # macOS
   ```

3. **No test results found**
   - Check if tests actually ran
   - Verify test file paths are correct
   - Use list commands to see available tests/groups

4. **Environment errors**
   - Only use: dev, uat, prod
   - Check if your config supports the environment

### Debug Mode

Run with verbose pytest output for debugging:

```bash
./tests/utils/test_runners/run_all_tests.sh -vv --tb=long
```

## Features ✨

### Enhanced User Experience

- 🎨 **Colorful output** with clear status indicators
- 📊 **Progress banners** showing what's running
- ✅ **Success/failure feedback** with exit codes
- 🔍 **Discovery commands** to find tests and groups
- 📋 **Comprehensive help** for each script

### Error Handling

- ✋ **Dependency checking** (pytest, allure)
- 📁 **Directory validation** (must run from project root)
- 🔧 **Missing file detection** with helpful suggestions
- 🚫 **Invalid environment handling**

### Flexibility

- 🌍 **Multi-environment support** (dev/uat/prod)
- 🎯 **Multiple run modes** (all/file/group)
- 🔇 **Quiet mode** for automation
- ⏭️ **Skip report option** for faster execution
- 🔄 **Pass-through pytest arguments**

### Allure Integration

- 📊 **Automatic report generation**
- 🧹 **Clean previous results**
- 🌐 **Interactive report serving**
- 📎 **Rich test attachments**

## Notes 📝

- Scripts automatically clean previous test results before running
- Allure reports open automatically in your browser (unless skipped)
- All scripts support passing additional pytest arguments
- Default environment is always `dev` for safety
- Scripts validate dependencies and provide installation instructions
- Exit codes match pytest exit codes for CI/CD integration

## Test Organization 📋

Tests are organized using Allure decorators and pytest markers:

```python
@allure.epic("Core API")              # Top-level grouping
@allure.feature("API Tests")          # Feature being tested
@allure.suite("smoke_tests")          # Test suite grouping
@allure.story("Root Endpoint")        # Individual test story
@pytest.mark.api                      # API test marker
@pytest.mark.smoke                    # Smoke test marker
def test_example():
    pass
```

### Test Suites

Use test suites to group related tests together:

```bash
# Run smoke test suite
./test_runner.sh group "smoke_tests"

# Run regression test suite
./test_runner.sh group "regression"

# Run performance test suite
./test_runner.sh group "performance"
```

### Test Markers

Use pytest markers for more flexible test filtering:

```bash
# Run tests by marker
./test_runner.sh all -k "smoke"
./test_runner.sh all -k "api"
./test_runner.sh all -k "not slow"

# Combine markers
./test_runner.sh all -k "smoke and not slow"
```

### Allure Organization

Allure decorators serve different purposes:

- `@allure.epic()` - Top-level grouping (e.g., "Core API")
- `@allure.feature()` - Feature being tested (e.g., "API Tests", "User Authentication")
- `@allure.suite()` - Test suite grouping (e.g., "smoke_tests", "regression")
- `@allure.story()` - Individual test story (e.g., "Root Endpoint")
- `@allure.severity()` - Test importance level

You can run tests at different levels of the hierarchy:

```bash
# Run by epic
./run_by_group.sh -g "Core API"

# Run by feature
./run_by_group.sh -g "API Tests"

# Run by suite
./run_by_group.sh -g "smoke_tests"

# Run by pytest marker
./run_all_tests.sh -k "smoke"
```

### Test Decorators

Tests should use the following Allure decorators for proper organization:

```python
@allure.epic("Core API")              # Top-level grouping
@allure.feature("API Tests")          # Feature grouping
@allure.suite("smoke_tests")          # Suite grouping
@allure.story("Root Endpoint")        # Individual test story
@pytest.mark.api                      # Pytest marker for API tests
@pytest.mark.smoke                    # Pytest marker for smoke tests
def test_example():
    pass
```
