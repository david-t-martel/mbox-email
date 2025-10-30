#!/usr/bin/env bash
# Run all linters (Python + Rust)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${GREEN}=== Running All Linters ===${NC}"

# Parse command line arguments
FIX=false
PYTHON_ONLY=false
RUST_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --fix|-f)
            FIX=true
            shift
            ;;
        --python)
            PYTHON_ONLY=true
            shift
            ;;
        --rust)
            RUST_ONLY=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --fix, -f      Auto-fix issues where possible"
            echo "  --python       Run only Python linters"
            echo "  --rust         Run only Rust linters"
            echo "  --help, -h     Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

FAILED=0

# ==========================================
# Python Linting
# ==========================================
if [ "$RUST_ONLY" = false ]; then
    echo -e "\n${YELLOW}Running Python linters...${NC}"

    # Black (formatting)
    echo -e "\n${YELLOW}Black (code formatting)...${NC}"
    if [ "$FIX" = true ]; then
        if uv run black mail_parser/; then
            echo -e "${GREEN}✓${NC} Black formatting applied"
        else
            echo -e "${RED}✗${NC} Black formatting failed"
            FAILED=1
        fi
    else
        if uv run black --check --diff mail_parser/; then
            echo -e "${GREEN}✓${NC} Black formatting check passed"
        else
            echo -e "${RED}✗${NC} Black formatting check failed (run with --fix)"
            FAILED=1
        fi
    fi

    # isort (import sorting)
    echo -e "\n${YELLOW}isort (import sorting)...${NC}"
    if [ "$FIX" = true ]; then
        if uv run isort mail_parser/; then
            echo -e "${GREEN}✓${NC} isort applied"
        else
            echo -e "${RED}✗${NC} isort failed"
            FAILED=1
        fi
    else
        if uv run isort --check-only --diff mail_parser/; then
            echo -e "${GREEN}✓${NC} isort check passed"
        else
            echo -e "${RED}✗${NC} isort check failed (run with --fix)"
            FAILED=1
        fi
    fi

    # Ruff (linting)
    echo -e "\n${YELLOW}Ruff (linting)...${NC}"
    if [ "$FIX" = true ]; then
        if uv run ruff check mail_parser/ --fix; then
            echo -e "${GREEN}✓${NC} Ruff linting with fixes applied"
        else
            echo -e "${RED}✗${NC} Ruff linting failed"
            FAILED=1
        fi
    else
        if uv run ruff check mail_parser/; then
            echo -e "${GREEN}✓${NC} Ruff linting passed"
        else
            echo -e "${RED}✗${NC} Ruff linting failed (run with --fix)"
            FAILED=1
        fi
    fi

    # mypy (type checking)
    echo -e "\n${YELLOW}mypy (type checking)...${NC}"
    if uv run mypy mail_parser/ --ignore-missing-imports; then
        echo -e "${GREEN}✓${NC} mypy type checking passed"
    else
        echo -e "${YELLOW}⚠${NC} mypy type checking found issues"
        # Don't fail on mypy errors
    fi

    # bandit (security)
    echo -e "\n${YELLOW}bandit (security linting)...${NC}"
    if uv run bandit -c pyproject.toml -r mail_parser/; then
        echo -e "${GREEN}✓${NC} bandit security check passed"
    else
        echo -e "${YELLOW}⚠${NC} bandit found security issues"
        # Don't fail on bandit warnings
    fi

    # pydocstyle (docstrings)
    echo -e "\n${YELLOW}pydocstyle (docstring checks)...${NC}"
    if uv run pydocstyle mail_parser/ --convention=google --add-ignore=D100,D104,D105,D107; then
        echo -e "${GREEN}✓${NC} pydocstyle check passed"
    else
        echo -e "${YELLOW}⚠${NC} pydocstyle found issues"
        # Don't fail on docstring issues
    fi
fi

# ==========================================
# Rust Linting
# ==========================================
if [ "$PYTHON_ONLY" = false ]; then
    echo -e "\n${YELLOW}Running Rust linters...${NC}"

    cd mail_parser_rust

    # rustfmt (formatting)
    echo -e "\n${YELLOW}rustfmt (code formatting)...${NC}"
    if [ "$FIX" = true ]; then
        if cargo fmt; then
            echo -e "${GREEN}✓${NC} rustfmt formatting applied"
        else
            echo -e "${RED}✗${NC} rustfmt formatting failed"
            FAILED=1
        fi
    else
        if cargo fmt -- --check; then
            echo -e "${GREEN}✓${NC} rustfmt formatting check passed"
        else
            echo -e "${RED}✗${NC} rustfmt formatting check failed (run with --fix)"
            FAILED=1
        fi
    fi

    # clippy (linting)
    echo -e "\n${YELLOW}clippy (linting)...${NC}"
    if [ "$FIX" = true ]; then
        if cargo clippy --fix --allow-dirty --allow-staged -- -D warnings; then
            echo -e "${GREEN}✓${NC} clippy linting with fixes applied"
        else
            echo -e "${RED}✗${NC} clippy linting failed"
            FAILED=1
        fi
    else
        if cargo clippy -- -D warnings; then
            echo -e "${GREEN}✓${NC} clippy linting passed"
        else
            echo -e "${RED}✗${NC} clippy linting failed (run with --fix)"
            FAILED=1
        fi
    fi

    # cargo check (compilation)
    echo -e "\n${YELLOW}cargo check (compilation)...${NC}"
    if cargo check; then
        echo -e "${GREEN}✓${NC} cargo check passed"
    else
        echo -e "${RED}✗${NC} cargo check failed"
        FAILED=1
    fi

    # cargo audit (security)
    echo -e "\n${YELLOW}cargo audit (security)...${NC}"
    if command -v cargo-audit &> /dev/null; then
        if cargo audit; then
            echo -e "${GREEN}✓${NC} cargo audit passed"
        else
            echo -e "${YELLOW}⚠${NC} cargo audit found vulnerabilities"
            # Don't fail on audit warnings
        fi
    else
        echo -e "${YELLOW}⚠${NC} cargo-audit not installed (cargo install cargo-audit)"
    fi

    cd "$PROJECT_ROOT"
fi

# ==========================================
# Summary
# ==========================================
echo ""
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}=== All Linters Passed! ===${NC}"
    exit 0
else
    echo -e "${RED}=== Some Linters Failed ===${NC}"
    echo -e "Run with ${YELLOW}--fix${NC} to auto-fix some issues"
    exit 1
fi
