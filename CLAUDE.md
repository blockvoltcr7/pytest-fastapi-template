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
# Run all tests with Allure reporting
uv run pytest --alluredir=allure-results -v

# Run specific test file
uv run pytest tests/test_hello.py -v

# Run tests by marker
uv run pytest -m api -v

# Generate and serve Allure report
allure serve allure-results
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
- **app/api/v1/**: Versioned API endpoints
- **app/core/**: Configuration and security
- **app/models/**: Pydantic data models
- **app/services/**: Business logic and AI integrations
- **app/agents/**: CrewAI agent implementations
- **app/tools/**: AI tools and utilities
- **tests/**: Comprehensive test suite with Allure reporting

### Key Integrations
- **OpenAI**: GPT models and image generation
- **Google Gemini**: Text-to-speech and language models
- **CrewAI**: Multi-agent AI orchestration
- **ElevenLabs**: Voice synthesis
- **ChromaDB/LanceDB**: Vector storage

## Development Guidelines

### Dependency Management
- Always use `uv` commands, never `pip`
- Update `pyproject.toml` when adding dependencies
- Commit both `pyproject.toml` and `uv.lock`

### Testing Requirements
- All new features must have corresponding tests
- Use pytest with Allure annotations:
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
- `GET /health` - Health check
- `GET /api/v1/hello` - Basic endpoint
- `POST /api/v1/crewai` - CrewAI agent execution
- `POST /api/v1/gemini/podcast` - Multi-speaker TTS generation
- `POST /api/v1/auth` - Authentication
- `GET /api/v1/users` - User management

## Environment Setup

Required for AI features:
```bash
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```

## Deployment

The project supports multiple deployment platforms:
- **Render**: Uses `render.yaml` configuration
- **Railway**: Uses `railway.json` configuration
- **Docker**: Multi-stage builds with UV support

Always run tests before deployment:
```bash
uv run pytest && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```
