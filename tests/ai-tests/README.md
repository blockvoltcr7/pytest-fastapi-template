# AI Tests

This directory contains tests for AI service integrations including OpenAI and ElevenLabs.

## Setup Requirements

### Environment Variables

The AI tests require API keys to be configured. **Important**: These tests load environment variables from a `.env` file in the project root, not from system environment variables.

1. **Create a `.env` file** in the project root:
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys** to the `.env` file:
   ```bash
   # OpenAI Configuration
   OPENAI_API_KEY=your_actual_openai_api_key_here
   
   # ElevenLabs Configuration (if using)
   ELEVENLABS_API_KEY=your_actual_elevenlabs_api_key_here
   ```

3. **Verify the setup** by running a simple test:
   ```bash
   pytest tests/ai-tests/test_openai_integration.py::TestOpenAIIntegration::test_openai_response -v
   ```

### Security Notes

- The `.env` file is automatically excluded from Git (listed in `.gitignore`)
- Never commit actual API keys to version control
- Use `.env.example` as a template for required environment variables

## Running AI Tests

```bash
# Run all AI tests
pytest ./tests/ai-tests/ -v

# Run specific AI test file
pytest ./tests/ai-tests/test_openai_integration.py -v

# Run with Allure reporting
pytest ./tests/ai-tests/ --alluredir=allure-results -v
```

## Test Coverage

- **OpenAI Integration**: Basic API response testing
- **OpenAI Image Generation**: Image creation with various parameters
- **ElevenLabs Integration**: Voice synthesis testing (if configured)

## Troubleshooting

**Error: "OPENAI_API_KEY not found in environment variables"**
- Ensure you have created a `.env` file in the project root
- Verify your API key is correctly set in the `.env` file
- Check that the `.env` file is not accidentally committed to Git 