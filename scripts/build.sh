#!/usr/bin/env bash
# Build Python package and Rust extension

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${GREEN}=== Building Mail Parser ===${NC}"

# Parse command line arguments
RELEASE=false
CLEAN=false
INSTALL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --release|-r)
            RELEASE=true
            shift
            ;;
        --clean|-c)
            CLEAN=true
            shift
            ;;
        --install|-i)
            INSTALL=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --release, -r   Build in release mode (optimized)"
            echo "  --clean, -c     Clean build artifacts before building"
            echo "  --install, -i   Install after building"
            echo "  --help, -h      Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# ==========================================
# Clean (if requested)
# ==========================================
if [ "$CLEAN" = true ]; then
    echo -e "\n${YELLOW}Cleaning build artifacts...${NC}"
    ./scripts/clean.sh
    echo -e "${GREEN}✓${NC} Clean complete"
fi

# ==========================================
# Build Rust Extension
# ==========================================
echo -e "\n${YELLOW}Building Rust extension...${NC}"

cd mail_parser_rust

if [ "$RELEASE" = true ]; then
    echo "Building in release mode (optimized)..."
    maturin build --release --strip
else
    echo "Building in development mode..."
    maturin build
fi

echo -e "${GREEN}✓${NC} Rust extension built"

# Install the wheel if requested
if [ "$INSTALL" = true ]; then
    echo -e "\n${YELLOW}Installing Rust extension...${NC}"
    WHEEL_FILE=$(find target/wheels -name "*.whl" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
    if [ -n "$WHEEL_FILE" ]; then
        uv pip install --force-reinstall "$WHEEL_FILE"
        echo -e "${GREEN}✓${NC} Rust extension installed: $WHEEL_FILE"
    else
        echo -e "${RED}✗${NC} No wheel file found"
        exit 1
    fi
fi

cd "$PROJECT_ROOT"

# ==========================================
# Build Python Package
# ==========================================
echo -e "\n${YELLOW}Building Python package...${NC}"

# Clean old distributions
rm -rf dist/*.tar.gz dist/*.whl 2>/dev/null || true

# Build Python package
uv pip install build
uv run python -m build

echo -e "${GREEN}✓${NC} Python package built"

# ==========================================
# Verify Builds
# ==========================================
echo -e "\n${YELLOW}Verifying builds...${NC}"

# Check Python distribution
if [ -n "$(ls -A dist/*.tar.gz 2>/dev/null)" ]; then
    echo -e "${GREEN}✓${NC} Python source distribution created"
    ls -lh dist/*.tar.gz
fi

if [ -n "$(ls -A dist/*.whl 2>/dev/null)" ]; then
    echo -e "${GREEN}✓${NC} Python wheel created"
    ls -lh dist/*.whl
fi

# Check Rust wheels
if [ -n "$(ls -A mail_parser_rust/target/wheels/*.whl 2>/dev/null)" ]; then
    echo -e "${GREEN}✓${NC} Rust extension wheel created"
    ls -lh mail_parser_rust/target/wheels/*.whl
fi

# ==========================================
# Install (if requested)
# ==========================================
if [ "$INSTALL" = true ]; then
    echo -e "\n${YELLOW}Installing packages...${NC}"

    # Install Python package in editable mode
    uv pip install -e .

    echo -e "${GREEN}✓${NC} Packages installed"

    # Verify installation
    echo -e "\n${YELLOW}Verifying installation...${NC}"

    if uv run python -c "import mail_parser; print(f'mail_parser version: {mail_parser.__version__ if hasattr(mail_parser, \"__version__\") else \"unknown\"}')" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} mail_parser import successful"
    else
        echo -e "${RED}✗${NC} mail_parser import failed"
        exit 1
    fi

    if uv run python -c "import mail_parser_rust; print('mail_parser_rust imported successfully')" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} mail_parser_rust import successful"
    else
        echo -e "${YELLOW}⚠${NC} mail_parser_rust import failed (may need separate installation)"
    fi
fi

# ==========================================
# Summary
# ==========================================
echo -e "\n${GREEN}=== Build Complete! ===${NC}"
echo ""
echo "Build artifacts:"
echo "  Python distributions: ${YELLOW}dist/${NC}"
echo "  Rust wheels:          ${YELLOW}mail_parser_rust/target/wheels/${NC}"
echo ""

if [ "$INSTALL" = false ]; then
    echo "To install the packages, run:"
    echo "  ${YELLOW}$0 --install${NC}"
    echo ""
fi

if [ "$RELEASE" = false ]; then
    echo "For optimized builds, run:"
    echo "  ${YELLOW}$0 --release${NC}"
fi
