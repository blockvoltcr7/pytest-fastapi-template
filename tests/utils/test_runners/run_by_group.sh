#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default environment
DEFAULT_ENV="dev"

# Parse command line arguments
while getopts "e:g:" opt; do
  case $opt in
    e) ENV="$OPTARG"
       ;;
    g) GROUP_NAME="$OPTARG"
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

# Check if group name is provided
if [ -z "$GROUP_NAME" ]; then
    echo -e "${RED}Error: Please provide a group name${NC}"
    echo "Usage: $0 -g <group_name> [-e <environment>]"
    echo "Example: $0 -g 'API Tests' -e dev"
    exit 1
fi

echo -e "${GREEN}Running Tests for Group: ${YELLOW}$GROUP_NAME${NC} in ${YELLOW}$ENV${GREEN} Environment${NC}"

# Clean previous results
echo -e "${YELLOW}Cleaning previous test results...${NC}"
rm -rf allure-results/ .pytest_cache/

# Run tests with specific allure group
echo -e "${YELLOW}Running tests...${NC}"
TEST_ENV=$ENV pytest \
    --alluredir=allure-results \
    -v \
    --capture=no \
    --show-capture=all \
    --allure-features="$GROUP_NAME" \
    "${@:$OPTIND}"

# Generate and serve Allure report
echo -e "${YELLOW}Generating Allure report...${NC}"
allure serve allure-results 