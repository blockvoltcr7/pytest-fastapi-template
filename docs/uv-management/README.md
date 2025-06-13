# UV Package Manager Guide

This guide covers the complete workflow for using `uv` package manager with this FastAPI project template.

## What is UV?

UV is a fast, modern Python package manager and build backend that combines the functionality of pip, pip-tools, and virtualenv into a single tool. It provides:

- **Fast package resolution and installation**
- **Reliable dependency management with lock files**
- **Built-in virtual environment management**
- **Project-based configuration with pyproject.toml**

## Installation

### Install UV

Choose one of these methods:

```bash
# Recommended: Install via pipx
pipx install uv

# Alternative: Install via pip
pip install uv

# macOS: Install via Homebrew
brew install uv

# Windows: Install via winget
winget install --id=astral-sh.uv  -e
```

Verify installation:
```bash
uv --version
```

## Project Setup Workflow

### 1. Initialize Project (First Time Setup)

When setting up this project for the first time:

```bash
# Clone the repository
git clone <repository-url>
cd pytest-fastapi-template

# Sync dependencies from pyproject.toml and uv.lock
uv sync

# This automatically:
# - Creates a virtual environment (.venv)
# - Installs all dependencies
# - Sets up the project in editable mode
```

### 2. Activate Virtual Environment

```bash
# Activate the virtual environment
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate     # Windows

# Verify activation (prompt should show (pytest-fastapi-template))
which python  # Should point to .venv/bin/python
```

### 3. Run Commands in Virtual Environment

Option 1 - With activated environment:
```bash
source .venv/bin/activate
uvicorn app.main:app --reload
pytest
```

Option 2 - Using `uv run` (recommended):
```bash
# Run commands directly without activating
uv run uvicorn app.main:app --reload
uv run pytest
uv run python -m app.main
```

## Dependency Management

### Adding New Dependencies

```bash
# Add a runtime dependency
uv add fastapi uvicorn pydantic

# Add a development dependency
uv add --dev pytest pytest-html allure-pytest

# Add with version constraints
uv add "fastapi>=0.100.0,<1.0.0"

# Add from specific source
uv add "git+https://github.com/user/repo.git"
```

### Removing Dependencies

```bash
# Remove a dependency
uv remove requests

# Remove a development dependency
uv remove --dev pytest-mock
```

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv add "fastapi@latest"

# Update all dev dependencies
uv sync --upgrade --dev
```

### Lock File Management

```bash
# Generate/update lock file (done automatically with uv add/remove)
uv lock

# Sync environment to match lock file exactly
uv sync

# Install only production dependencies
uv sync --no-dev
```

## Development Workflow

### Daily Development

```bash
# Start development server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app

# Run linting (if configured)
uv run ruff check .
uv run mypy .
```

### Environment Management

```bash
# Create a new virtual environment
uv venv

# Use specific Python version
uv venv --python 3.11

# Remove virtual environment
rm -rf .venv

# Recreate environment
uv venv && uv sync
```

## Project Configuration (pyproject.toml)

This project uses `pyproject.toml` for configuration:

```toml
[project]
name = "pytest-fastapi-template"
version = "0.1.0"
description = "FastAPI template with pytest testing"
requires-python = ">=3.9"
dependencies = [
    "fastapi>=0.115.12",
    "uvicorn>=0.34.2",
    # ... other dependencies
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["app"]
```

## Troubleshooting

### Common Issues

**1. `uv sync` fails with resolution errors**
```bash
# Clear cache and retry
uv cache clean
uv sync

# Or recreate environment
rm -rf .venv uv.lock
uv sync
```

**2. Wrong Python version**
```bash
# Check current Python
uv run python --version

# Recreate with specific version
rm -rf .venv
uv venv --python 3.11
uv sync
```

**3. Import errors**
```bash
# Ensure project is installed in editable mode
uv sync

# Verify installation
uv run python -c "import app; print('Success')"
```

**4. Lock file conflicts**
```bash
# Reset lock file
rm uv.lock
uv lock
uv sync
```

## Advanced Usage

### Multiple Environments

```bash
# Create environment for different Python version
uv venv --python 3.11 .venv-py311
uv venv --python 3.12 .venv-py312

# Activate specific environment
source .venv-py311/bin/activate
```

### Scripts and Tools

```bash
# Run arbitrary commands
uv run python -c "print('Hello from uv!')"

# Run module
uv run -m pytest

# Run with environment variables
uv run --env DEBUG=1 uvicorn app.main:app --reload
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Set up Python and uv
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'

- name: Install uv
  run: pip install uv

- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest
```

## Best Practices

1. **Always use `uv sync`** after cloning or pulling changes
2. **Use `uv run`** for running commands to avoid activation issues
3. **Commit both `pyproject.toml` and `uv.lock`** to version control
4. **Use `uv add`** instead of editing pyproject.toml manually
5. **Keep dependencies minimal** - only add what you actually need
6. **Use version constraints** for critical dependencies
7. **Regular updates** - run `uv sync --upgrade` periodically

## Comparison with Other Tools

| Task | pip/venv | poetry | uv |
|------|----------|--------|----|
| Create venv | `python -m venv .venv` | `poetry install` | `uv sync` |
| Install deps | `pip install -r requirements.txt` | `poetry install` | `uv sync` |
| Add dependency | Edit requirements.txt + `pip install` | `poetry add package` | `uv add package` |
| Run command | `source .venv/bin/activate && python` | `poetry run python` | `uv run python` |
| Update deps | `pip install --upgrade` | `poetry update` | `uv sync --upgrade` |

## Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)
- [pyproject.toml Specification](https://peps.python.org/pep-0621/)