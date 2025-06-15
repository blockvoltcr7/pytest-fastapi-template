#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
TEST_FILE="tests/ai-tests/gemini/test_gemini_podcast_gen.py"
ALLURE_RESULTS_DIR="allure-results"

cd "$PROJECT_ROOT"

# Check dependencies
missing_deps=()
if ! command -v pytest &> /dev/null; then
    missing_deps+=("pytest")
fi
if ! command -v allure &> /dev/null; then
    missing_deps+=("allure")
fi
if [ ${#missing_deps[@]} -ne 0 ]; then
    echo -e "${RED}Error: Missing required dependencies: ${missing_deps[*]}${NC}"
    exit 1
fi

# Clean previous reports
rm -rf "$ALLURE_RESULTS_DIR"/ .pytest_cache/ tests/allure-results/
mkdir -p "$ALLURE_RESULTS_DIR"

# Run pytest
echo -e "${YELLOW}🚀 Running Gemini Podcast AI tests...${NC}"
pytest --alluredir="$ALLURE_RESULTS_DIR" --tb=short --capture=no --show-capture=all "$TEST_FILE"
TEST_EXIT_CODE=$?

# Show result
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ All Gemini podcast tests passed!${NC}"
else
    echo -e "${RED}❌ Some Gemini podcast tests failed (exit code: $TEST_EXIT_CODE)${NC}"
fi

# Generate and launch Allure report
if [ -d "$ALLURE_RESULTS_DIR" ] && [ "$(ls -A $ALLURE_RESULTS_DIR)" ]; then
    echo -e "${YELLOW}📊 Generating Allure report...${NC}"
    allure serve "$ALLURE_RESULTS_DIR"
else
    echo -e "${YELLOW}⚠️  No test results found for Allure report${NC}"
fi
