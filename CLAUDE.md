# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based GenAI API template designed for building AI-powered web services. It integrates multiple AI providers (OpenAI, Google Gemini, ElevenLabs) with comprehensive testing and deployment capabilities.

## Essential Commands

### Development Server
```bash
# Start development server (recommended)
uv run uvicorn app.main:app --reload

# Alternative with activated venv
source .venv/bin/activate && uvicorn app.main:app --reload
```

### Testing
```bash
# Run all tests with Allure reporting (Allure enabled by default in pytest.ini)
uv run pytest -v

# Run specific test file
uv run pytest tests/demo/test_hello.py -v

# Run tests by marker
uv run pytest -m api -v
uv run pytest -m integration -v
uv run pytest -m slow -v

# Generate and serve Allure report
allure serve allure-results

# Use convenience test runner (recommended)
./test_runner.sh all                              # Run all tests
./test_runner.sh file tests/demo/test_hello.py    # Run specific file
./test_runner.sh group "API Tests"                # Run by feature group
./test_runner.sh list-files                       # List available test files
./test_runner.sh list-groups                      # List available test groups
```

### Dependency Management
Always use `uv` for package management, never `pip`:
```bash
# Install dependencies
uv sync

# Add new dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Update dependencies
uv sync --upgrade
```

## Architecture

### Core Structure
- **app/api/v1/**: Versioned API endpoints with routers
- **app/core/**: Configuration (Pydantic settings), security, and dependencies
- **app/models/**: Pydantic data models for request/response validation
- **app/services/**: Business logic and AI integrations (image, voice, TTS streaming)
- **app/agents/**: CrewAI agent implementations for content creation
- **app/tools/**: AI tools and utilities for agent workflows
- **tests/**: Comprehensive test suite with Allure reporting and environment configs

### Key Integrations
- **OpenAI**: GPT models and image generation
- **Google Gemini**: Text-to-speech and language models 
- **CrewAI**: Multi-agent AI orchestration for content workflows
- **ElevenLabs**: Voice synthesis and audio generation
- **ChromaDB/LanceDB**: Vector storage for embeddings
- **FastAPI**: Modern async web framework with automatic API docs

### Configuration Management
- Uses Pydantic settings with `.env` file support
- Environment-specific test configurations (dev/uat/prod)
- API keys managed through environment variables
- Automatic directory creation for output files (images, audio)

## Development Guidelines

### Dependency Management
- Always use `uv` commands, never `pip`
- Update `pyproject.toml` when adding dependencies
- Commit both `pyproject.toml` and `uv.lock`

### Testing Requirements
- All new features must have corresponding tests
- Use pytest with Allure annotations (configured in pytest.ini):
  ```python
  @allure.epic("Core Functionality")
  @allure.feature("Feature Name")
  class TestFeatureName:
      @allure.story("Test Scenario")
      @allure.severity(allure.severity_level.CRITICAL)
      def test_something(self):
          with allure.step("Step description"):
              # test code
  ```
- Use appropriate markers: `@pytest.mark.api`, `@pytest.mark.integration`, `@pytest.mark.slow`
- Test organization: ai-tests/, demo/, endpoints/, with specialized test runners
- Environment configs available for dev/uat/prod testing scenarios
- Include response attachments and logging for debugging API responses

### Pydantic V2 Best Practices
- Use `Optional[bool]` instead of `bool` for API fields that might return null
- Use `model_validate_json()` for JSON validation
- Add logging with `allure.attach()` for debugging API responses
- Use `Field(default_factory=list)` for default collections
- Implement custom validation with `@field_validator` decorator

### AI Service Integration
- Store API keys in environment variables
- Add proper error handling for external API calls
- Include response logging for debugging
- Test both success and error scenarios

## API Endpoints

Main endpoints:
- `GET /` - Root endpoint 
- `GET /health` - Health check
- `GET /api/v1/hello` - Basic hello world endpoint
- `POST /api/v1/crewai` - CrewAI agent execution
- `POST /api/v1/content-crew` - Content creation crew workflows
- `POST /api/v1/gemini/podcast` - Multi-speaker TTS generation
- `POST /api/v1/auth` - Authentication
- `GET /api/v1/users` - User management
- Automatic API documentation available at `/docs` and `/redoc`

## Environment Setup

Required for AI features:
```bash
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here  
ELEVENLABS_API_KEY=your_key_here
```

## Project-Specific Best Practices

### Dependency Management
- **ALWAYS** use `uv` commands, never `pip` directly
- Use `uv sync` for installing dependencies from lock file
- Use `uv add package-name` for adding new dependencies
- Commit both `pyproject.toml` and `uv.lock` files

### Pydantic V2 Guidelines  
- Use `Optional[bool]` instead of `bool` for fields that might return null
- Use `Field(default_factory=list)` for default collections
- Add `allure.attach()` for debugging API responses during testing
- Use `@field_validator` decorator for custom validation

### Testing Standards
- Use the convenience test runner: `./test_runner.sh`
- Organize tests by category: ai-tests/, demo/, endpoints/
- Include proper Allure annotations for reporting
- Test both success and error scenarios for AI integrations

## Deployment

The project supports multiple deployment platforms:
- **Render**: Uses `render.yaml` configuration
- **Railway**: Uses `railway.json` configuration
- **Docker**: Multi-stage builds with UV support

Always run tests before deployment:
```bash
uv run pytest && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```
