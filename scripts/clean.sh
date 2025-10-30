#!/usr/bin/env bash
# Clean build artifacts and temporary files

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${GREEN}=== Cleaning Build Artifacts ===${NC}"

# Parse command line arguments
DEEP_CLEAN=false
CACHE_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --deep|-d)
            DEEP_CLEAN=true
            shift
            ;;
        --cache|-c)
            CACHE_ONLY=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --deep, -d     Deep clean (removes venv, all caches)"
            echo "  --cache, -c    Clean only cache files"
            echo "  --help, -h     Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# ==========================================
# Python Artifacts
# ==========================================
if [ "$CACHE_ONLY" = false ]; then
    echo -e "\n${YELLOW}Cleaning Python artifacts...${NC}"

    # Remove build directories
    rm -rf build/ dist/ *.egg-info/
    echo -e "${GREEN}✓${NC} Removed build directories"

    # Remove compiled Python files
    find . -type f -name '*.pyc' -delete
    find . -type f -name '*.pyo' -delete
    find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Removed compiled Python files"
fi

# ==========================================
# Rust Artifacts
# ==========================================
if [ "$CACHE_ONLY" = false ]; then
    echo -e "\n${YELLOW}Cleaning Rust artifacts...${NC}"

    cd mail_parser_rust

    # Clean Rust build artifacts
    cargo clean
    echo -e "${GREEN}✓${NC} Removed Rust build artifacts"

    # Remove wheels
    rm -rf target/wheels/
    echo -e "${GREEN}✓${NC} Removed Rust wheels"

    cd "$PROJECT_ROOT"
fi

# ==========================================
# Test and Coverage Artifacts
# ==========================================
if [ "$CACHE_ONLY" = false ]; then
    echo -e "\n${YELLOW}Cleaning test artifacts...${NC}"

    # Python coverage
    rm -rf htmlcov/
    rm -f .coverage coverage.xml
    rm -rf .pytest_cache/
    echo -e "${GREEN}✓${NC} Removed Python test artifacts"

    # Rust coverage
    rm -rf mail_parser_rust/target/llvm-cov/
    rm -f mail_parser_rust/lcov.info
    echo -e "${GREEN}✓${NC} Removed Rust test artifacts"
fi

# ==========================================
# Cache Files
# ==========================================
echo -e "\n${YELLOW}Cleaning cache files...${NC}"

# Python caches
rm -rf .mypy_cache/
rm -rf .ruff_cache/
rm -rf .hypothesis/
echo -e "${GREEN}✓${NC} Removed Python cache files"

# Rust caches (keep registry, clean incremental builds)
if [ "$DEEP_CLEAN" = true ]; then
    rm -rf ~/.cargo/registry/cache/
    rm -rf ~/.cargo/git/checkouts/
    echo -e "${GREEN}✓${NC} Removed Cargo caches"
fi

# UV cache
if [ "$DEEP_CLEAN" = true ]; then
    rm -rf ~/.cache/uv/
    echo -e "${GREEN}✓${NC} Removed UV cache"
fi

# ==========================================
# Logs and Temporary Files
# ==========================================
if [ "$CACHE_ONLY" = false ]; then
    echo -e "\n${YELLOW}Cleaning logs and temporary files...${NC}"

    # Remove log files
    rm -f *.log
    rm -rf logs/*.log 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Removed log files"

    # Remove temporary test outputs
    rm -rf test_output/
    rm -rf tmp/ temp/ .tmp/
    echo -e "${GREEN}✓${NC} Removed temporary files"

    # IDE and editor artifacts
    rm -rf .vscode/.ropeproject/
    rm -f .DS_Store
    echo -e "${GREEN}✓${NC} Removed IDE artifacts"
fi

# ==========================================
# Virtual Environment (Deep Clean Only)
# ==========================================
if [ "$DEEP_CLEAN" = true ]; then
    echo -e "\n${YELLOW}Deep clean: Removing virtual environment...${NC}"

    rm -rf .venv/
    echo -e "${GREEN}✓${NC} Removed virtual environment"

    echo -e "\n${YELLOW}Note: Run ./scripts/setup.sh to recreate the environment${NC}"
fi

# ==========================================
# Summary
# ==========================================
echo -e "\n${GREEN}=== Clean Complete! ===${NC}"

if [ "$DEEP_CLEAN" = true ]; then
    echo -e "\nDeep clean completed. You may want to run:"
    echo -e "  ${YELLOW}./scripts/setup.sh${NC} - To recreate the development environment"
elif [ "$CACHE_ONLY" = true ]; then
    echo -e "\nCache files cleaned."
else
    echo -e "\nBuild artifacts cleaned. Virtual environment preserved."
    echo -e "For a complete clean, run: ${YELLOW}$0 --deep${NC}"
fi
