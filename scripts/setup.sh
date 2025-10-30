#!/usr/bin/env bash
# Setup script for Mail Parser development environment
# Works cross-platform: Linux, macOS, Windows WSL

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${GREEN}=== Mail Parser Development Setup ===${NC}"
echo "Project root: $PROJECT_ROOT"

# ==========================================
# Check Prerequisites
# ==========================================
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION"

# Check UV
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}Installing UV package manager...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi
echo -e "${GREEN}✓${NC} UV installed"

# Check Rust
if ! command -v cargo &> /dev/null; then
    echo -e "${YELLOW}Installing Rust...${NC}"
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
fi
RUST_VERSION=$(rustc --version | awk '{print $2}')
echo -e "${GREEN}✓${NC} Rust $RUST_VERSION"

# ==========================================
# Python Environment Setup
# ==========================================
echo -e "\n${YELLOW}Setting up Python environment...${NC}"

# Create virtual environment
if [ ! -d ".venv" ]; then
    uv venv
    echo -e "${GREEN}✓${NC} Created virtual environment"
else
    echo -e "${GREEN}✓${NC} Virtual environment exists"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
uv pip install -e ".[dev]"
echo -e "${GREEN}✓${NC} Python dependencies installed"

# Install development tools
echo "Installing development tools..."
uv pip install \
    pre-commit \
    pytest \
    pytest-cov \
    pytest-xdist \
    black \
    ruff \
    mypy \
    isort \
    bandit[toml] \
    pydocstyle \
    maturin
echo -e "${GREEN}✓${NC} Development tools installed"

# ==========================================
# Rust Environment Setup
# ==========================================
echo -e "\n${YELLOW}Setting up Rust environment...${NC}"

cd mail_parser_rust

# Install Rust components
rustup component add rustfmt clippy

# Install cargo tools
if ! command -v cargo-audit &> /dev/null; then
    cargo install cargo-audit
fi

if ! command -v cargo-llvm-cov &> /dev/null; then
    cargo install cargo-llvm-cov
fi

echo -e "${GREEN}✓${NC} Rust components installed"

# Build Rust extension
echo "Building Rust extension..."
maturin develop --release
echo -e "${GREEN}✓${NC} Rust extension built"

cd "$PROJECT_ROOT"

# ==========================================
# Pre-commit Hooks Setup
# ==========================================
echo -e "\n${YELLOW}Setting up pre-commit hooks...${NC}"

# Create .secrets.baseline if it doesn't exist
if [ ! -f ".secrets.baseline" ]; then
    echo '{}' > .secrets.baseline
    echo -e "${GREEN}✓${NC} Created .secrets.baseline"
fi

# Install pre-commit hooks
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
echo -e "${GREEN}✓${NC} Pre-commit hooks installed"

# Run pre-commit on all files (first time)
echo "Running pre-commit on all files (this may take a while)..."
uv run pre-commit run --all-files || echo -e "${YELLOW}Some pre-commit checks failed. Please fix them before committing.${NC}"

# ==========================================
# Git Configuration
# ==========================================
echo -e "\n${YELLOW}Configuring Git...${NC}"

# Check if this is a git repository
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}WARNING: Not a git repository. Run 'git init' if needed.${NC}"
else
    # Set git config for this repo
    git config core.autocrlf input  # Normalize line endings
    git config pull.rebase true     # Use rebase for pulls
    echo -e "${GREEN}✓${NC} Git configured"
fi

# ==========================================
# Create necessary directories
# ==========================================
echo -e "\n${YELLOW}Creating project directories...${NC}"

mkdir -p output
mkdir -p test_output
mkdir -p logs

echo -e "${GREEN}✓${NC} Directories created"

# ==========================================
# Verify Installation
# ==========================================
echo -e "\n${YELLOW}Verifying installation...${NC}"

# Test Python import
if uv run python -c "import mail_parser; print('Python package OK')" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Python package import successful"
else
    echo -e "${YELLOW}⚠${NC} Python package import failed (may need to run tests)"
fi

# Test Rust extension
if uv run python -c "import mail_parser_rust; print('Rust extension OK')" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Rust extension import successful"
else
    echo -e "${YELLOW}⚠${NC} Rust extension import failed"
fi

# ==========================================
# Summary
# ==========================================
echo -e "\n${GREEN}=== Setup Complete! ===${NC}"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo "  2. Run tests:"
echo "     ${YELLOW}./scripts/test.sh${NC}"
echo ""
echo "  3. Run linters:"
echo "     ${YELLOW}./scripts/lint.sh${NC}"
echo ""
echo "  4. Build the project:"
echo "     ${YELLOW}./scripts/build.sh${NC}"
echo ""
echo "  5. Before committing, pre-commit hooks will run automatically"
echo ""
echo -e "For more information, see ${YELLOW}CONTRIBUTING.md${NC}"
