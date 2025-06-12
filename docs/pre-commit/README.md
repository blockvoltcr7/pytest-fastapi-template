# Pre-commit Configuration

This project uses [pre-commit](https://pre-commit.com/) to automatically run essential checks before each commit. The configuration is optimized for speed while ensuring core functionality works.

## What is Pre-commit?

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. It automatically runs configured tools on your staged files before you commit them to git.

## Current Setup

Our minimal pre-commit configuration is defined in `.pre-commit-config.yaml` and includes these fast, essential hooks:

### Essential Checks

1. **Basic File Checks** (< 1 second)
   - `trailing-whitespace`: Removes trailing whitespace
   - `end-of-file-fixer`: Ensures files end with a newline
   - `check-yaml`: Validates YAML file syntax
   - `check-merge-conflict`: Checks for merge conflict markers

2. **Smoke Test** (~5 seconds)
   - **pytest-smoke-test**: Runs a critical API test
     - Starts the FastAPI application on port 8000
     - Runs `test_root_endpoint` from `tests/test_fastapi_endpoints.py`
     - Verifies the core API functionality works
     - Automatically shuts down the server after testing

## What Happens Now

With pre-commit installed, the following occurs automatically:

### On Every Commit Attempt

1. **File Checks**: Basic file formatting checks run quickly
2. **API Test**: The application starts, runs a smoke test, then shuts down
3. **Commit Blocking**: If any check fails, the commit is blocked
4. **Total Time**: ~6 seconds for all checks

### Typical Workflow

```bash
# Make changes to your code
git add .

# Attempt to commit
git commit -m "Your commit message"

# Pre-commit runs automatically:
# ✓ Trailing whitespace fixed
# ✓ End of file fixed
# ✓ YAML files validated
# ✓ Merge conflict markers checked
# ✓ Starting FastAPI server...
# ✓ Running smoke test on root endpoint
# ✓ Server shut down
# ✓ All checks passed!

# If files were modified, stage them again
git add .
git commit -m "Your commit message"
```

## Manual Execution

You can run pre-commit hooks manually without committing:

```bash
# Run all hooks
uv run pre-commit run --all-files

# Run only smoke test
uv run pre-commit run pytest-smoke-test

# Run only file checks
uv run pre-commit run trailing-whitespace
```

## Installation Details

Pre-commit is included in our `pyproject.toml` dependencies and installed via:

```bash
uv sync  # Installs pre-commit
uv run pre-commit install  # Sets up git hooks
```

## Benefits

1. **Speed**: Minimal checks complete in ~6 seconds
2. **Essential Coverage**: Catches critical API failures before commit
3. **File Quality**: Ensures clean, consistent file formatting
4. **Automation**: Prevents broken code from being committed

## Bypassing Pre-commit (Not Recommended)

In rare cases, you can bypass pre-commit hooks:

```bash
git commit --no-verify -m "Emergency commit"
```

**Note**: This should only be used in emergency situations.

## Why This Minimal Setup?

This configuration prioritizes:
- **Speed**: Total runtime ~6 seconds vs. 30+ seconds with full linting
- **Core Functionality**: Smoke test ensures the API actually works
- **Essential Hygiene**: Basic file checks prevent common issues
- **Developer Experience**: Fast feedback loop encourages regular commits

## Troubleshooting

### Common Issues

1. **Smoke Test Fails**: Check if port 8000 is already in use
2. **Server Won't Start**: Verify dependencies with `uv sync`
3. **Files Modified**: Stage the modified files and commit again

### Getting Help

- Check the pre-commit documentation: https://pre-commit.com/
- Use `uv run pre-commit run --help` for command options
