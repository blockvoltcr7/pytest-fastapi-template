#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default environment
DEFAULT_ENV="dev"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Usage function
show_usage() {
    echo -e "${CYAN}Usage: $0 -f <test_file> [OPTIONS] [PYTEST_ARGS...]${NC}"
    echo ""
    echo -e "${YELLOW}Required:${NC}"
    echo "  -f <file>    Path to test file (required)"
    echo ""
    echo -e "${YELLOW}Options:${NC}"
    echo "  -e <env>     Environment (dev/uat/prod) [default: dev]"
    echo "  -h, --help   Show this help message"
    echo "  -s, --skip   Skip opening Allure report automatically"
    echo "  -q, --quiet  Run with minimal output"
    echo "  -l, --list   List available test files"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./run_by_file.sh -f tests/test_hello.py"
    echo "  ./run_by_file.sh -f tests/test_fastapi_endpoints.py -e uat"
    echo "  ./run_by_file.sh -f tests/ai-tests/test_openai_integration.py -v"
    echo "  ./run_by_file.sh -l                           # List available test files"
    echo ""
    echo -e "${YELLOW}Note:${NC} Run this script from the project root directory."
}

# List available test files
list_test_files() {
    echo -e "${CYAN}Available test files:${NC}"
    echo ""
    
    if [ -d "tests" ]; then
        # Find all test files and organize them
        find tests -name "test_*.py" -type f | sort | while read -r file; do
            # Get relative path from tests directory
            rel_path="${file#tests/}"
            dir_name=$(dirname "$rel_path")
            
            if [ "$dir_name" = "." ]; then
                echo -e "  ${GREEN}├── ${file}${NC}"
            else
                echo -e "  ${GREEN}├── ${file}${NC} ${YELLOW}(${dir_name})${NC}"
            fi
        done
    else
        echo -e "${RED}Error: tests directory not found${NC}"
    fi
    echo ""
}

# Check if script is run from project root
check_project_root() {
    if [ ! -f "pytest.ini" ] || [ ! -d "tests" ]; then
        echo -e "${RED}Error: This script must be run from the project root directory.${NC}"
        echo -e "${YELLOW}Current directory: $(pwd)${NC}"
        echo -e "${YELLOW}Expected files: pytest.ini, tests/ directory${NC}"
        echo ""
        echo -e "${CYAN}Solution:${NC}"
        echo "  cd $PROJECT_ROOT"
        echo "  ./tests/utils/test_runners/run_by_file.sh -f <test_file>"
        exit 1
    fi
}

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    if ! command -v pytest &> /dev/null; then
        missing_deps+=("pytest")
    fi
    
    if ! command -v allure &> /dev/null; then
        missing_deps+=("allure")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${RED}Error: Missing required dependencies: ${missing_deps[*]}${NC}"
        echo ""
        echo -e "${YELLOW}To install missing dependencies:${NC}"
        for dep in "${missing_deps[@]}"; do
            case $dep in
                pytest)
                    echo "  uv pip install pytest allure-pytest"
                    ;;
                allure)
                    echo "  # Install Allure CLI: https://docs.qameta.io/allure/#_installing_a_commandline"
                    echo "  # macOS: brew install allure"
                    echo "  # Other: Download from https://github.com/allure-framework/allure2/releases"
                    ;;
            esac
        done
        exit 1
    fi
}

# Parse command line arguments
SKIP_ALLURE=false
QUIET_MODE=false
TEST_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -f)
            TEST_FILE="$2"
            shift 2
            ;;
        -e)
            ENV="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        -l|--list)
            check_project_root
            list_test_files
            exit 0
            ;;
        -s|--skip)
            SKIP_ALLURE=true
            shift
            ;;
        -q|--quiet)
            QUIET_MODE=true
            shift
            ;;
        -*)
            # Pass unknown options to pytest
            break
            ;;
        *)
            # Pass positional arguments to pytest
            break
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
    echo -e "${RED}Error: Please provide a test file path using -f option${NC}"
    echo ""
    show_usage
    exit 1
fi

# Check if we're in the right directory
check_project_root

# Check dependencies
check_dependencies

# Verify file exists
if [ ! -f "$TEST_FILE" ]; then
    echo -e "${RED}Error: Test file not found: $TEST_FILE${NC}"
    echo ""
    echo -e "${YELLOW}Available test files:${NC}"
    list_test_files
    exit 1
fi

# Display banner
if [ "$QUIET_MODE" = false ]; then
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                   RUNNING FILE TESTS                    ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Environment:${NC}     ${YELLOW}$ENV${NC}"
    echo -e "${GREEN}Test File:${NC}       ${YELLOW}$TEST_FILE${NC}"
    echo -e "${GREEN}Allure Results:${NC}  ${YELLOW}$(pwd)/allure-results${NC}"
    echo ""
fi

# Clean previous results
if [ "$QUIET_MODE" = false ]; then
    echo -e "${YELLOW}🧹 Cleaning previous test results...${NC}"
fi
rm -rf allure-results/ .pytest_cache/ tests/allure-results/

# Create allure-results directory
mkdir -p allure-results

# Prepare pytest arguments
PYTEST_ARGS=(
    "--alluredir=allure-results"
    "--tb=short"
    "--capture=no"
    "--show-capture=all"
    "$TEST_FILE"
)

# Add quiet mode args if specified
if [ "$QUIET_MODE" = true ]; then
    PYTEST_ARGS+=("-q")
else
    PYTEST_ARGS+=("-v")
fi

# Run tests
if [ "$QUIET_MODE" = false ]; then
    echo -e "${YELLOW}🚀 Running tests from file: $(basename "$TEST_FILE")...${NC}"
fi

# Export environment variable for tests
export TEST_ENV=$ENV

# Run pytest with all arguments
pytest "${PYTEST_ARGS[@]}" "$@"
TEST_EXIT_CODE=$?

# Check test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    if [ "$QUIET_MODE" = false ]; then
        echo -e "${GREEN}✅ All tests in file passed successfully!${NC}"
    fi
else
    echo -e "${RED}❌ Some tests in file failed (exit code: $TEST_EXIT_CODE)${NC}"
fi

# Generate and serve Allure report
if [ "$SKIP_ALLURE" = false ]; then
    if [ "$QUIET_MODE" = false ]; then
        echo -e "${YELLOW}📊 Generating Allure report...${NC}"
    fi
    
    # Check if we have test results
    if [ -d "allure-results" ] && [ "$(ls -A allure-results)" ]; then
        allure serve allure-results
    else
        echo -e "${YELLOW}⚠️  No test results found for Allure report${NC}"
    fi
else
    if [ "$QUIET_MODE" = false ]; then
        echo -e "${CYAN}📋 Allure report skipped. To view results later, run:${NC}"
        echo -e "   ${YELLOW}allure serve allure-results${NC}"
    fi
fi

exit $TEST_EXIT_CODE 