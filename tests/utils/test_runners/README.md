# Test Runners

This directory contains shell scripts for running tests in different configurations and environments. These scripts provide a convenient way to execute tests while ensuring consistent reporting and environment handling.

## Available Runners

### 1. `run_all_tests.sh`

Runs all tests in the project.

```bash
# Basic usage (runs in dev environment)
./run_all_tests.sh

# Run in specific environment
./run_all_tests.sh -e dev

# Options:
# -e <environment>  : Specify environment (dev/uat/prod)
# Additional pytest arguments can be passed after options
```

### 2. `run_by_file.sh`

Runs tests from a specific file.

```bash
# Basic usage (runs in dev environment)
./run_by_file.sh -f tests/api/v1/test_hello.py

# Run in specific environment
./run_by_file.sh -f tests/api/v1/test_hello.py -e prod

# Options:
# -f <file_path>   : Path to test file (required)
# -e <environment> : Specify environment (dev/uat/prod)
# Additional pytest arguments can be passed after options
```

### 3. `run_by_group.sh`

Runs tests by Allure feature group.

```bash
# Basic usage (runs in dev environment)
./run_by_group.sh -g "API Tests"

# Run in specific environment
./run_by_group.sh -g "API Tests" -e uat

# Options:
# -g <group_name>  : Allure feature group name (required)
# -e <environment> : Specify environment (dev/uat/prod)
# Additional pytest arguments can be passed after options
```

## Common Features

All test runners include:

1. **Environment Support**
   - Default environment: `dev`
   - Supported environments: `dev`, `uat`, `prod`
   - Environment validation
   - Environment-specific configuration loading

2. **Allure Reporting**
   - Automatic cleanup of previous results
   - Report generation after test execution
   - Interactive report serving

3. **Error Handling**
   - Input validation
   - Clear error messages
   - Proper exit codes

4. **Additional Options**
   - All pytest arguments are supported
   - Verbose output
   - Test capture settings

## Examples

1. Run all tests in UAT with specific marker:
```bash
./run_all_tests.sh -e uat -k "smoke"
```

2. Run specific file in production with xfail:
```bash
./run_by_file.sh -f tests/api/v1/test_auth.py -e prod -x
```

3. Run API tests in development with verbose output:
```bash
./run_by_group.sh -g "API Tests" -e dev -vv
```

## Environment Variables

The runners set the following environment variables:

- `TEST_ENV`: Current test environment (dev/uat/prod)

## Exit Codes

- 0: Tests executed successfully
- 1: Invalid arguments or configuration
- Other: pytest exit codes

## Notes

1. Always run scripts from the project root directory
2. Ensure proper permissions (`chmod +x`) for execution
3. The scripts automatically clean previous test results
4. Allure must be installed for report generation 