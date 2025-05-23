#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default environment
DEFAULT_ENV="dev"

# Parse command line arguments
while getopts "e:" opt; do
  case $opt in
    e) ENV="$OPTARG"
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

echo -e "${GREEN}Running All Tests in ${YELLOW}$ENV${GREEN} Environment${NC}"

# Clean previous results
echo -e "${YELLOW}Cleaning previous test results...${NC}"
rm -rf allure-results/ .pytest_cache/

# Run tests with all markers
echo -e "${YELLOW}Running tests...${NC}"
TEST_ENV=$ENV pytest \
    --alluredir=allure-results \
    -v \
    --capture=no \
    --show-capture=all \
    "${@:$OPTIND}"

# Generate and serve Allure report
echo -e "${YELLOW}Generating Allure report...${NC}"
allure serve allure-results 