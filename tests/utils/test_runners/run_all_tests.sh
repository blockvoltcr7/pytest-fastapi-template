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
    echo -e "${CYAN}Usage: $0 [OPTIONS] [PYTEST_ARGS...]${NC}"
    echo ""
    echo -e "${YELLOW}Options:${NC}"
    echo "  -e <env>     Environment (dev/uat/prod) [default: dev]"
    echo "  -h, --help   Show this help message"
    echo "  -s, --skip   Skip opening Allure report automatically"
    echo "  -q, --quiet  Run with minimal output"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./run_all_tests.sh                    # Run all tests in dev environment"
    echo "  ./run_all_tests.sh -e uat             # Run all tests in UAT environment"
    echo "  ./run_all_tests.sh -k \"smoke\"        # Run only smoke tests"
    echo "  ./run_all_tests.sh -v -s              # Verbose output, skip Allure report"
    echo "  ./run_all_tests.sh --maxfail=1        # Stop after first failure"
    echo ""
    echo -e "${YELLOW}Available test markers:${NC}"
    echo "  api, integration, smoke, slow"
    echo ""
    echo -e "${YELLOW}Note:${NC} Run this script from the project root directory."
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
        echo "  ./tests/utils/test_runners/run_all_tests.sh"
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

while [[ $# -gt 0 ]]; do
    case $1 in
        -e)
            ENV="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
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

# Check if we're in the right directory
check_project_root

# Check dependencies
check_dependencies

# Display banner
if [ "$QUIET_MODE" = false ]; then
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                    RUNNING ALL TESTS                    ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Environment:${NC}     ${YELLOW}$ENV${NC}"
    echo -e "${GREEN}Test Directory:${NC}  ${YELLOW}$(pwd)/tests${NC}"
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
)

# Add quiet mode args if specified
if [ "$QUIET_MODE" = true ]; then
    PYTEST_ARGS+=("-q")
else
    PYTEST_ARGS+=("-v")
fi

# Run tests
if [ "$QUIET_MODE" = false ]; then
    echo -e "${YELLOW}🚀 Running tests...${NC}"
fi

# Export environment variable for tests
export TEST_ENV=$ENV

# Run pytest with all arguments
pytest "${PYTEST_ARGS[@]}" "$@"
TEST_EXIT_CODE=$?

# Check test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    if [ "$QUIET_MODE" = false ]; then
        echo -e "${GREEN}✅ All tests passed successfully!${NC}"
    fi
else
    echo -e "${RED}❌ Some tests failed (exit code: $TEST_EXIT_CODE)${NC}"
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