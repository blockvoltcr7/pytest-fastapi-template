# AI Integration Tests

This folder contains tests for AI-related functionality in the Baby Podcast GenAI application.

## Contents

- `test_openai_integration.py`: Tests for OpenAI API integration

## Running Tests

From the project root directory:

```bash
# Run all AI tests
pytest tests/ai-tests/ --alluredir=allure-results

# Run specific test
pytest tests/ai-tests/test_openai_integration.py --alluredir=allure-results
```

## Requirements

These tests require:
1. An OpenAI API key set as environment variable `OPENAI_API_KEY`
2. An ElevenLabs API key set as environment variable `ELEVENLABS_API_KEY`
3. The virtual environment activated and all dependencies installed

## Test Details

The OpenAI integration test verifies that the application can:
1. Initialize an OpenAI client
2. Send requests to the OpenAI API
3. Receive and process responses properly 