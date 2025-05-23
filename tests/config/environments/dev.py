"""
Development environment configuration.
"""

# API Configuration
API_BASE_URL = "http://localhost:8080"
API_HELLO_ENDPOINT = "/api/v1/hello"
API_HEALTH_ENDPOINT = "/health"
API_OPENAI_ENDPOINT = "/api/v1/ai/generate"
API_ELEVENLABS_ENDPOINT = "/api/v1/voice/synthesize"

# Database Configuration
DATABASE_URL = "sqlite:///dev_test.db"
DATABASE_TIMEOUT = 30
DATABASE_POOL_SIZE = 5

# Test Execution
PARALLEL_WORKERS = 2
RETRY_ATTEMPTS = 2
TIMEOUT = 30

# Logging
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 