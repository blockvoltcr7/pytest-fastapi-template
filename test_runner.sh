#!/bin/bash

# Test Runner Convenience Script
# This script provides easy access to all test runners from the project root

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Usage function
show_usage() {
    echo -e "${CYAN}Test Runner Convenience Script${NC}"
    echo ""
    echo -e "${YELLOW}Usage: $0 <command> [options...]${NC}"
    echo ""
    echo -e "${YELLOW}Available Commands:${NC}"
    echo "  all                Run all tests"
    echo "  file <test_file>   Run specific test file"
    echo "  group <group_name> Run tests by feature group"
    echo "  list-files         List available test files"
    echo "  list-groups        List available test groups"
    echo "  help               Show this help message"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./test_runner.sh all                              # Run all tests"
    echo "  ./test_runner.sh all -e uat                       # Run all tests in UAT"
    echo "  ./test_runner.sh all -k \"smoke\"                  # Run smoke tests"
    echo "  ./test_runner.sh file tests/test_hello.py         # Run specific file"
    echo "  ./test_runner.sh group \"API Endpoints\"           # Run API tests"
    echo "  ./test_runner.sh list-files                       # List test files"
    echo "  ./test_runner.sh list-groups                      # List test groups"
    echo ""
    echo -e "${YELLOW}Options (passed to underlying scripts):${NC}"
    echo "  -e <env>    Environment (dev/uat/prod) [default: dev]"
    echo "  -s, --skip  Skip opening Allure report"
    echo "  -q, --quiet Run with minimal output"
    echo "  -k <expr>   Only run tests matching the given expression"
    echo "  -h, --help  Show help for specific runner"
    echo ""
    echo -e "${YELLOW}Note:${NC} This script automatically runs from the project root."
}

# Check if we're in the project root
if [ ! -f "pytest.ini" ] || [ ! -d "tests" ]; then
    echo -e "${RED}Error: This script must be run from the project root directory.${NC}"
    echo -e "${YELLOW}Current directory: $(pwd)${NC}"
    echo -e "${YELLOW}Expected files: pytest.ini, tests/ directory${NC}"
    exit 1
fi

# Check if command is provided
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
    all)
        echo -e "${GREEN}🚀 Running all tests...${NC}"
        exec ./tests/utils/test_runners/run_all_tests.sh "$@"
        ;;
    file)
        if [ $# -eq 0 ]; then
            echo -e "${RED}Error: Please provide a test file path${NC}"
            echo "Usage: $0 file <test_file> [options...]"
            echo "Example: $0 file tests/test_hello.py"
            exit 1
        fi
        TEST_FILE="$1"
        shift
        echo -e "${GREEN}🚀 Running test file: $TEST_FILE${NC}"
        exec ./tests/utils/test_runners/run_by_file.sh -f "$TEST_FILE" "$@"
        ;;
    group)
        if [ $# -eq 0 ]; then
            echo -e "${RED}Error: Please provide a group name${NC}"
            echo "Usage: $0 group <group_name> [options...]"
            echo "Example: $0 group \"API Endpoints\""
            exit 1
        fi
        GROUP_NAME="$1"
        shift
        echo -e "${GREEN}🚀 Running test group: $GROUP_NAME${NC}"
        exec ./tests/utils/test_runners/run_by_group.sh -g "$GROUP_NAME" "$@"
        ;;
    list-files)
        echo -e "${GREEN}📋 Listing available test files...${NC}"
        exec ./tests/utils/test_runners/run_by_file.sh -l
        ;;
    list-groups)
        echo -e "${GREEN}📋 Listing available test groups...${NC}"
        exec ./tests/utils/test_runners/run_by_group.sh -l
        ;;
    help|--help|-h)
        show_usage
        exit 0
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$COMMAND'${NC}"
        echo ""
        show_usage
        exit 1
        ;;
esac 