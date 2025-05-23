"""
UAT environment configuration.
"""

# API Configuration
API_BASE_URL = "https://api-uat.example.com"
API_HELLO_ENDPOINT = "/api/v1/hello"
API_HEALTH_ENDPOINT = "/health"
API_OPENAI_ENDPOINT = "/api/v1/ai/generate"
API_ELEVENLABS_ENDPOINT = "/api/v1/voice/synthesize"

# Database Configuration
DATABASE_URL = "postgresql://user:pass@uat-db.example.com:5432/testdb"
DATABASE_TIMEOUT = 45
DATABASE_POOL_SIZE = 10

# Test Execution
PARALLEL_WORKERS = 4
RETRY_ATTEMPTS = 3
TIMEOUT = 60

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 