#!/usr/bin/env bash
# Run all tests (Python + Rust)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${GREEN}=== Running All Tests ===${NC}"

# Parse command line arguments
COVERAGE=false
VERBOSE=false
PARALLEL=false
RUST_ONLY=false
PYTHON_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage|-c)
            COVERAGE=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --parallel|-p)
            PARALLEL=true
            shift
            ;;
        --rust)
            RUST_ONLY=true
            shift
            ;;
        --python)
            PYTHON_ONLY=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --coverage, -c    Generate coverage reports"
            echo "  --verbose, -v     Verbose output"
            echo "  --parallel, -p    Run tests in parallel"
            echo "  --rust            Run only Rust tests"
            echo "  --python          Run only Python tests"
            echo "  --help, -h        Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# ==========================================
# Python Tests
# ==========================================
if [ "$RUST_ONLY" = false ]; then
    echo -e "\n${YELLOW}Running Python tests...${NC}"

    PYTEST_ARGS=()

    if [ "$VERBOSE" = true ]; then
        PYTEST_ARGS+=("-v")
    else
        PYTEST_ARGS+=("-q")
    fi

    if [ "$PARALLEL" = true ]; then
        PYTEST_ARGS+=("-n" "auto")
    fi

    if [ "$COVERAGE" = true ]; then
        PYTEST_ARGS+=("--cov=mail_parser" "--cov-report=html" "--cov-report=term" "--cov-report=xml")
    fi

    # Run pytest
    if uv run pytest tests/ "${PYTEST_ARGS[@]}"; then
        echo -e "${GREEN}✓${NC} Python tests passed"
    else
        echo -e "${RED}✗${NC} Python tests failed"
        exit 1
    fi

    if [ "$COVERAGE" = true ]; then
        echo -e "\n${GREEN}Coverage report generated in htmlcov/index.html${NC}"
    fi
fi

# ==========================================
# Rust Tests
# ==========================================
if [ "$PYTHON_ONLY" = false ]; then
    echo -e "\n${YELLOW}Running Rust tests...${NC}"

    cd mail_parser_rust

    CARGO_TEST_ARGS=()

    if [ "$VERBOSE" = true ]; then
        CARGO_TEST_ARGS+=("--verbose")
    fi

    # Run cargo test
    if cargo test "${CARGO_TEST_ARGS[@]}"; then
        echo -e "${GREEN}✓${NC} Rust tests passed"
    else
        echo -e "${RED}✗${NC} Rust tests failed"
        cd "$PROJECT_ROOT"
        exit 1
    fi

    # Run doc tests
    if cargo test --doc; then
        echo -e "${GREEN}✓${NC} Rust doc tests passed"
    else
        echo -e "${RED}✗${NC} Rust doc tests failed"
        cd "$PROJECT_ROOT"
        exit 1
    fi

    # Generate coverage if requested
    if [ "$COVERAGE" = true ]; then
        echo -e "\n${YELLOW}Generating Rust coverage...${NC}"
        if command -v cargo-llvm-cov &> /dev/null; then
            cargo llvm-cov --html --open
            echo -e "${GREEN}✓${NC} Rust coverage report generated"
        else
            echo -e "${YELLOW}⚠${NC} cargo-llvm-cov not installed. Run: cargo install cargo-llvm-cov"
        fi
    fi

    cd "$PROJECT_ROOT"
fi

# ==========================================
# Summary
# ==========================================
echo -e "\n${GREEN}=== All Tests Passed! ===${NC}"

if [ "$COVERAGE" = true ]; then
    echo ""
    echo "Coverage reports:"
    echo "  Python: ${YELLOW}htmlcov/index.html${NC}"
    echo "  Rust:   ${YELLOW}mail_parser_rust/target/llvm-cov/html/index.html${NC}"
fi
