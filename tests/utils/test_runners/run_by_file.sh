#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default environment
DEFAULT_ENV="dev"

# Parse command line arguments
while getopts "e:f:" opt; do
  case $opt in
    e) ENV="$OPTARG"
       ;;
    f) TEST_FILE="$OPTARG"
       ;;
    \?) echo "Invalid option -$OPTARG" >&2
        exit 1
        ;;
  esac
done

# Set environment
ENV=${ENV:-$DEFAULT_ENV}

# Validate environment
case $ENV in
  dev|uat|prod) ;;
  *)
    echo -e "${RED}Error: Invalid environment '$ENV'. Must be one of: dev, uat, prod${NC}"
    exit 1
    ;;
esac

# Check if test file is provided
if [ -z "$TEST_FILE" ]; then
    echo -e "${RED}Error: Please provide a test file path${NC}"
    echo "Usage: $0 -f <test_file_path> [-e <environment>]"
    echo "Example: $0 -f tests/api/v1/test_hello.py -e dev"
    exit 1
fi

# Verify file exists
if [ ! -f "$TEST_FILE" ]; then
    echo -e "${RED}Error: Test file not found: $TEST_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}Running Tests from File: ${YELLOW}$TEST_FILE${NC} in ${YELLOW}$ENV${GREEN} Environment${NC}"

# Clean previous results
echo -e "${YELLOW}Cleaning previous test results...${NC}"
rm -rf allure-results/ .pytest_cache/

# Run tests from specific file
echo -e "${YELLOW}Running tests...${NC}"
TEST_ENV=$ENV pytest \
    --alluredir=allure-results \
    -v \
    --capture=no \
    --show-capture=all \
    "$TEST_FILE" \
    "${@:$OPTIND}"

# Generate and serve Allure report
echo -e "${YELLOW}Generating Allure report...${NC}"
allure serve allure-results 