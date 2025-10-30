# Development Setup Guide

This guide covers setting up a development environment for the Mail Parser project using modern Python tooling with UV as the primary package manager.

## Prerequisites

- Python 3.10 or higher
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager (required)
- [Rust](https://rustup.rs/) - Required for building the Rust extension (mail_parser_rust)
- [Maturin](https://github.com/PyO3/maturin) - For building PyO3 extensions

## Quick Start

### 1. Clone and Navigate to Project

```bash
cd /mnt/c/codedev/auricleinc/mail_analysis/mail/mail_parser
```

### 2. Create Virtual Environment with UV

```bash
# UV automatically creates and manages virtual environments
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Linux/macOS
# Or on Windows:
# .venv\Scripts\activate
```

### 3. Install Dependencies

#### Production Dependencies Only

```bash
uv pip install -e .
```

#### Development Dependencies

```bash
# Install with dev and test extras
uv pip install -e ".[dev,test]"

# Or install all optional dependencies
uv pip install -e ".[all]"
```

#### Using Requirements Files

```bash
# Production
uv pip install -r requirements.txt

# Development
uv pip install -r requirements-dev.txt
```

### 4. Build Rust Extension

The project includes a high-performance Rust extension for email parsing:

```bash
cd mail_parser_rust

# Build in development mode
maturin develop

# Or build optimized release version
maturin develop --release

cd ..
```

## Project Structure

```
mail_parser/
├── mail_parser/              # Main Python package
│   ├── __init__.py
│   ├── __main__.py          # Package entry point
│   ├── cli.py               # Click-based CLI
│   ├── core/                # Core parsing logic
│   ├── api/                 # Gmail API integration
│   ├── analysis/            # Statistics and analytics
│   ├── renderers/           # HTML rendering
│   ├── organizers/          # Email organization strategies
│   ├── indexing/            # Database and search
│   └── dashboard/           # Analytics dashboard
├── mail_parser_rust/        # Rust extension (PyO3)
│   ├── Cargo.toml
│   ├── pyproject.toml
│   └── src/
├── tests/                   # Test suite
├── config/                  # Configuration files
├── credentials/             # Gmail API credentials
├── output/                  # Parsed email output
├── pyproject.toml           # Project configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
└── README.md
```

## Development Workflow

### Running the Application

#### Using UV (Recommended)

```bash
# Run as module
uv run python -m mail_parser parse --mbox path/to/mbox --output ./output

# Or use installed CLI command
uv run mail-parser parse --mbox path/to/mbox --output ./output
```

#### Direct CLI Usage

After installation, the CLI is available:

```bash
mail-parser parse --mbox path/to/mbox --output ./output
mbox-parse parse --mbox path/to/mbox --output ./output  # Alternative command
```

### Code Quality Tools

#### Black - Code Formatting

```bash
# Format all Python files
uv run black mail_parser/

# Check without modifying
uv run black --check mail_parser/
```

#### Ruff - Fast Linting

```bash
# Run linter
uv run ruff check mail_parser/

# Auto-fix issues
uv run ruff check --fix mail_parser/

# Format code (alternative to black)
uv run ruff format mail_parser/
```

#### MyPy - Type Checking

```bash
# Run type checker
uv run mypy mail_parser/

# Strict mode
uv run mypy --strict mail_parser/
```

### Testing

#### Running Tests with Pytest

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=mail_parser --cov-report=html

# Run specific test file
uv run pytest tests/test_parser.py

# Run with verbose output
uv run pytest -v

# Run parallel tests (faster)
uv run pytest -n auto
```

#### Test Markers

```bash
# Run only unit tests
uv run pytest -m unit

# Run integration tests
uv run pytest -m integration

# Skip slow tests
uv run pytest -m "not slow"

# Skip Gmail API tests (require credentials)
uv run pytest -m "not gmail_api"
```

#### Coverage Reports

```bash
# Generate HTML coverage report
uv run pytest --cov=mail_parser --cov-report=html
# Open htmlcov/index.html in browser

# Generate terminal report
uv run pytest --cov=mail_parser --cov-report=term-missing

# Generate XML report (for CI)
uv run pytest --cov=mail_parser --cov-report=xml
```

### Pre-commit Quality Checks

Run all quality checks before committing:

```bash
# Format code
uv run black mail_parser/

# Lint and auto-fix
uv run ruff check --fix mail_parser/

# Type check
uv run mypy mail_parser/

# Run tests
uv run pytest
```

## Building and Distribution

### Building Source and Wheel Distributions

```bash
# Build Python package
uv pip install build
uv run python -m build

# Outputs will be in dist/
```

### Building Rust Extension

```bash
cd mail_parser_rust

# Development build
maturin develop

# Release build with optimizations
maturin develop --release

# Build wheel for distribution
maturin build --release

cd ..
```

## Configuration Files

### pyproject.toml

The main configuration file contains:

- **Project metadata**: Name, version, description, authors
- **Dependencies**: Production and optional dependencies (dev, test, docs, build, profile)
- **Build system**: Hatchling configuration
- **Tool configurations**: Black, Ruff, Pytest, MyPy, Coverage
- **Scripts**: CLI entry points (mail-parser, mbox-parse)

### Tool-Specific Configuration

All tools are configured in `pyproject.toml`:

- **[tool.black]**: Line length 100, Python 3.10+
- **[tool.ruff]**: Fast linting with comprehensive rules
- **[tool.pytest.ini_options]**: Test discovery, coverage, markers
- **[tool.mypy]**: Type checking configuration
- **[tool.coverage]**: Coverage measurement and reporting

## Optional Dependencies

Install specific feature sets as needed:

```bash
# Development tools (black, ruff, mypy, ipython, ipdb)
uv pip install -e ".[dev]"

# Testing tools (pytest, coverage, hypothesis)
uv pip install -e ".[test]"

# Documentation tools (sphinx, themes)
uv pip install -e ".[docs]"

# Build tools (maturin for Rust extensions)
uv pip install -e ".[build]"

# Profiling tools (py-spy, memory-profiler, line-profiler)
uv pip install -e ".[profile]"

# All optional dependencies
uv pip install -e ".[all]"
```

## Performance Profiling

### Python Profiling

```bash
# Install profiling tools
uv pip install -e ".[profile]"

# CPU profiling with py-spy
uv run py-spy record -o profile.svg -- python -m mail_parser parse --mbox test.mbox

# Memory profiling
uv run python -m memory_profiler mail_parser/core/mbox_parser.py

# Line profiling
uv run kernprof -l -v mail_parser/core/mbox_parser.py
```

### Rust Extension Profiling

```bash
cd mail_parser_rust

# Build with debug symbols
cargo build --release

# Profile with cargo-flamegraph
cargo flamegraph --bin mail_parser_rust

cd ..
```

## Troubleshooting

### Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e ".[all]"
```

### Rust Extension Build Failures

```bash
# Ensure Rust is installed
rustc --version

# Update Rust toolchain
rustup update

# Clean and rebuild
cd mail_parser_rust
cargo clean
maturin develop --release
cd ..
```

### Dependency Conflicts

```bash
# Regenerate requirements files
uv pip compile pyproject.toml -o requirements.txt
uv pip compile pyproject.toml --extra dev --extra test -o requirements-dev.txt

# Sync with lock file
uv pip sync requirements-dev.txt
```

### UV Not Found

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

## IDE Setup

### VS Code

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests",
    "-v"
  ],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true,
    "source.organizeImports": true
  }
}
```

### PyCharm

1. Set Python interpreter to `.venv/bin/python`
2. Enable pytest as test runner
3. Configure Black as code formatter
4. Enable MyPy for type checking

## Continuous Integration

The project is configured for CI/CD with:

- **GitHub Actions**: Automated testing and linting
- **Coverage reporting**: Coverage.py with HTML/XML reports
- **Multi-platform testing**: Linux, macOS, Windows
- **Python versions**: 3.10, 3.11, 3.12

See `.github/workflows/` for CI configuration.

## Additional Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [Maturin Guide](https://www.maturin.rs/)
- [PyO3 Documentation](https://pyo3.rs/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)

## Getting Help

- Review the [README.md](README.md) for project overview
- Check [QUICK_START.md](QUICK_START.md) for basic usage
- Read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- See [PERFORMANCE_SUMMARY.md](PERFORMANCE_SUMMARY.md) for optimization details

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
