#!/usr/bin/env bash
# Build script for mail_parser_rust extension

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${GREEN}=== Building mail_parser_rust extension ===${NC}"

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo -e "${RED}Error: Rust/Cargo not found. Install from https://rustup.rs${NC}"
    exit 1
fi

# Check if maturin is installed
if ! command -v maturin &> /dev/null; then
    echo -e "${YELLOW}Installing maturin...${NC}"
    uv pip install maturin
fi

# Parse arguments
BUILD_MODE="release"
INSTALL_TO_PARENT="false"
RUN_TESTS="false"
RUN_CLIPPY="false"
AUTO_FIX="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --dev)
            BUILD_MODE="dev"
            shift
            ;;
        --install-parent)
            INSTALL_TO_PARENT="true"
            shift
            ;;
        --test)
            RUN_TESTS="true"
            shift
            ;;
        --clippy)
            RUN_CLIPPY="true"
            shift
            ;;
        --fix)
            AUTO_FIX="true"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--dev] [--install-parent] [--test] [--clippy] [--fix]"
            exit 1
            ;;
    esac
done

cd "$SCRIPT_DIR"

# Run clippy if requested
if [[ "$RUN_CLIPPY" == "true" ]]; then
    echo -e "${YELLOW}Running clippy...${NC}"
    if [[ "$AUTO_FIX" == "true" ]]; then
        cargo clippy --fix --allow-dirty --allow-staged
    else
        cargo clippy -- -D warnings
    fi
fi

# Run tests if requested
if [[ "$RUN_TESTS" == "true" ]]; then
    echo -e "${YELLOW}Running tests...${NC}"
    cargo test --all-features
fi

# Format check
echo -e "${YELLOW}Checking formatting...${NC}"
if [[ "$AUTO_FIX" == "true" ]]; then
    cargo fmt
else
    cargo fmt -- --check
fi

# Build with maturin
echo -e "${YELLOW}Building extension with maturin...${NC}"
if [[ "$BUILD_MODE" == "release" ]]; then
    maturin build --release
else
    maturin build
fi

echo -e "${GREEN}Build complete!${NC}"

# Install to parent project if requested
if [[ "$INSTALL_TO_PARENT" == "true" ]]; then
    echo -e "${YELLOW}Installing to parent project venv...${NC}"

    # Find the parent project's venv
    if [[ -d "$PROJECT_ROOT/.venv" ]]; then
        PARENT_VENV="$PROJECT_ROOT/.venv"
        echo -e "${GREEN}Found parent venv at: $PARENT_VENV${NC}"

        # Install using maturin develop (creates symlink for development)
        source "$PARENT_VENV/bin/activate"
        maturin develop --release

        echo -e "${GREEN}Extension installed to parent project!${NC}"
    else
        echo -e "${RED}Warning: Parent venv not found at $PROJECT_ROOT/.venv${NC}"
        echo -e "${YELLOW}You may need to manually install with: maturin develop${NC}"
    fi
fi

# Print usage instructions
echo ""
echo -e "${GREEN}=== Build Summary ===${NC}"
echo "Build mode: $BUILD_MODE"
echo "Extension location: $SCRIPT_DIR/target/$BUILD_MODE/"
echo ""
echo -e "${YELLOW}To install for development:${NC}"
echo "  cd $SCRIPT_DIR && maturin develop --release"
echo ""
echo -e "${YELLOW}To build a wheel:${NC}"
echo "  cd $SCRIPT_DIR && maturin build --release"
echo ""
echo -e "${YELLOW}To install from parent project:${NC}"
echo "  uv pip install -e ./mail_parser_rust"
