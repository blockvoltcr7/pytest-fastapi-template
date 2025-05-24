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
    echo -e "${CYAN}Usage: $0 -g <group_name> [OPTIONS] [PYTEST_ARGS...]${NC}"
    echo ""
    echo -e "${YELLOW}Required:${NC}"
    echo "  -g <group>   Allure feature group name (required)"
    echo ""
    echo -e "${YELLOW}Options:${NC}"
    echo "  -e <env>     Environment (dev/uat/prod) [default: dev]"
    echo "  -h, --help   Show this help message"
    echo "  -s, --skip   Skip opening Allure report automatically"
    echo "  -q, --quiet  Run with minimal output"
    echo "  -l, --list   List available test groups/features"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./run_by_group.sh -g \"API Endpoints\""
    echo "  ./run_by_group.sh -g \"OpenAI API\" -e uat"
    echo "  ./run_by_group.sh -g \"FastAPI Application\" -v"
    echo "  ./run_by_group.sh -l                         # List available groups"
    echo ""
    echo -e "${YELLOW}Note:${NC} Run this script from the project root directory."
}

# List available test groups
list_test_groups() {
    echo -e "${CYAN}Scanning for available test groups/suites:${NC}"
    echo ""
    
    if [ -d "tests" ]; then
        # Find all test files and extract @allure.suite annotations
        local suites=()
        
        while IFS= read -r file; do
            if [ -f "$file" ]; then
                # Extract suite names from @allure.suite() annotations
                while IFS= read -r line; do
                    if [[ $line =~ @allure\.suite\([\"\'](.*)[\"\']\) ]]; then
                        suite="${BASH_REMATCH[1]}"
                        if [[ ! " ${suites[@]} " =~ " $suite " ]]; then
                            suites+=("$suite")
                        fi
                    fi
                done < "$file"
            fi
        done < <(find tests -name "test_*.py" -type f)
        
        if [ ${#suites[@]} -eq 0 ]; then
            echo -e "${YELLOW}⚠️  No @allure.suite annotations found in test files${NC}"
            echo -e "${CYAN}Make sure your test files have @allure.suite decorators like:${NC}"
            echo -e "  ${GREEN}@allure.suite(\"smoke_tests\")${NC}"
        else
            echo -e "${GREEN}Found the following test suites:${NC}"
            echo ""
            for suite in "${suites[@]}"; do
                echo -e "  ${GREEN}├── \"${suite}\"${NC}"
            done
        fi
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
        echo "  ./tests/utils/test_runners/run_by_group.sh -g <group_name>"
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
GROUP_NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -g)
            GROUP_NAME="$2"
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
            list_test_groups
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

# Check if group name is provided
if [ -z "$GROUP_NAME" ]; then
    echo -e "${RED}Error: Please provide a group name using -g option${NC}"
    echo ""
    show_usage
    echo ""
    echo -e "${CYAN}To see available groups, run:${NC}"
    echo -e "  ${YELLOW}./run_by_group.sh -l${NC}"
    exit 1
fi

# Check if we're in the right directory
check_project_root

# Check dependencies
check_dependencies

# Display banner
if [ "$QUIET_MODE" = false ]; then
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                  RUNNING GROUP TESTS                    ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Environment:${NC}     ${YELLOW}$ENV${NC}"
    echo -e "${GREEN}Test Group:${NC}      ${YELLOW}\"$GROUP_NAME\"${NC}"
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
    "--allure-label=suite=$GROUP_NAME"
)

# Add quiet mode args if specified
if [ "$QUIET_MODE" = true ]; then
    PYTEST_ARGS+=("-q")
else
    PYTEST_ARGS+=("-v")
fi

# Run tests
if [ "$QUIET_MODE" = false ]; then
    echo -e "${YELLOW}🚀 Running tests for group: \"$GROUP_NAME\"...${NC}"
fi

# Export environment variable for tests
export TEST_ENV=$ENV

# Run pytest with all arguments
pytest "${PYTEST_ARGS[@]}" "$@"
TEST_EXIT_CODE=$?

# Check test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    if [ "$QUIET_MODE" = false ]; then
        echo -e "${GREEN}✅ All tests in group passed successfully!${NC}"
    fi
else
    echo -e "${RED}❌ Some tests in group failed (exit code: $TEST_EXIT_CODE)${NC}"
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
        echo -e "${CYAN}This might mean no tests matched the group \"$GROUP_NAME\"${NC}"
        echo -e "${CYAN}To see available groups, run: ./run_by_group.sh -l${NC}"
    fi
else
    if [ "$QUIET_MODE" = false ]; then
        echo -e "${CYAN}📋 Allure report skipped. To view results later, run:${NC}"
        echo -e "   ${YELLOW}allure serve allure-results${NC}"
    fi
fi

exit $TEST_EXIT_CODE 