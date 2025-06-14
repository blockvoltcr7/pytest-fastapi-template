#!/bin/bash

# Colors for output
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Starting FastAPI server for integration tests..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &>/dev/null &
SERVER_PID=$!

# Ensure server is killed on exit
trap 'kill $SERVER_PID 2>/dev/null' EXIT

sleep 3 # Give server time to start

echo "Running integration tests..."
# Run pytest and capture the output and exit code
# Ensure we are running from the project root
top_dir="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

cd "$top_dir"

# Run smoke tests directly using pytest
TEST_OUTPUT=$(uv run pytest -m smoke tests/endpoints/test_fastapi_endpoints.py -v 2>&1)
TEST_RESULT=$?

# Always print the test output
echo "$TEST_OUTPUT"

# Check if tests failed
if [ $TEST_RESULT -ne 0 ]; then
  echo -e "${YELLOW}Warning: Pytest tests failed. This will not block the commit.${NC}"
else
  echo -e "${GREEN}Pytest tests passed.${NC}"
fi

# Stop the server
kill $SERVER_PID
exit $TEST_RESULT
