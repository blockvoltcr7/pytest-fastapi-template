"""
Production environment configuration.
"""

# API Configuration
API_BASE_URL = "https://api.example.com"
API_HELLO_ENDPOINT = "/api/v1/hello"
API_HEALTH_ENDPOINT = "/health"
API_OPENAI_ENDPOINT = "/api/v1/ai/generate"
API_ELEVENLABS_ENDPOINT = "/api/v1/voice/synthesize"

# Database Configuration
DATABASE_URL = "postgresql://user:pass@prod-db.example.com:5432/proddb"
DATABASE_TIMEOUT = 60
DATABASE_POOL_SIZE = 20

# Test Execution
PARALLEL_WORKERS = 1  # Conservative for production testing
RETRY_ATTEMPTS = 5
TIMEOUT = 120

# Logging
LOG_LEVEL = "WARNING"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 