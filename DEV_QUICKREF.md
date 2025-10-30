# Developer Quick Reference

Quick commands for common development tasks.

## First Time Setup
```bash
./scripts/setup.sh
```

## Daily Development

### Code Quality
```bash
# Auto-format code
./scripts/lint.sh --fix

# Check code quality
./scripts/lint.sh
```

### Testing
```bash
# Run all tests
./scripts/test.sh

# Run with coverage
./scripts/test.sh --coverage

# Run tests in parallel
./scripts/test.sh --parallel

# Run only Python tests
./scripts/test.sh --python

# Run only Rust tests
./scripts/test.sh --rust
```

### Building
```bash
# Development build
./scripts/build.sh

# Release build (optimized)
./scripts/build.sh --release

# Build and install
./scripts/build.sh --install
```

### Cleaning
```bash
# Clean build artifacts
./scripts/clean.sh

# Deep clean (including venv)
./scripts/clean.sh --deep
```

## Pre-commit Hooks

### Install
```bash
uv run pre-commit install
```

### Run Manually
```bash
# Run on all files
uv run pre-commit run --all-files

# Run on staged files
uv run pre-commit run
```

### Update Hooks
```bash
uv run pre-commit autoupdate
```

## Python Development

### Formatting
```bash
uv run black mail_parser/
uv run isort mail_parser/
```

### Linting
```bash
uv run ruff check mail_parser/
uv run ruff check mail_parser/ --fix
```

### Type Checking
```bash
uv run mypy mail_parser/
```

### Security
```bash
uv run bandit -r mail_parser/
```

### Testing
```bash
uv run pytest
uv run pytest -v
uv run pytest --cov=mail_parser
uv run pytest -n auto  # parallel
```

## Rust Development

### Formatting
```bash
cd mail_parser_rust
cargo fmt
cargo fmt -- --check
```

### Linting
```bash
cd mail_parser_rust
cargo clippy
cargo clippy --fix --allow-dirty
```

### Testing
```bash
cd mail_parser_rust
cargo test
cargo test --verbose
```

### Building
```bash
cd mail_parser_rust
maturin develop          # development
maturin develop --release  # optimized
maturin build --release  # wheel
```

### Security
```bash
cd mail_parser_rust
cargo audit
cargo outdated
```

## Git Workflow

### Feature Branch
```bash
git checkout -b feature/my-feature
# Make changes
./scripts/lint.sh --fix
./scripts/test.sh
git add .
git commit -m "feat: Add my feature"
git push origin feature/my-feature
```

### Commit Message Format
```
type(scope): Brief description

Detailed explanation

- Bullet points
- More details

Fixes #123
```

**Types:** feat, fix, docs, style, refactor, perf, test, chore, ci

### Before Merging
```bash
# Sync with main
git fetch origin
git rebase origin/main

# Run all checks
./scripts/lint.sh
./scripts/test.sh --coverage

# Push
git push origin feature/my-feature --force-with-lease
```

## Troubleshooting

### Pre-commit Failing
```bash
./scripts/lint.sh --fix
git add -u
git commit -m "Your message"
```

### Rust Build Issues
```bash
cd mail_parser_rust
cargo clean
cd ..
./scripts/build.sh --clean --release
```

### Test Failures
```bash
./scripts/test.sh --verbose
```

### Dependency Issues
```bash
./scripts/clean.sh --deep
./scripts/setup.sh
```

### Can't Execute Scripts
```bash
chmod +x scripts/*.sh
```

## Environment

### Activate Virtual Environment
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Check Environment
```bash
which python
which uv
which cargo
python --version
uv --version
cargo --version
```

### Install Missing Tools
```bash
# UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Maturin
uv pip install maturin
```

## Performance

### Profile Python
```bash
uv run python -m cProfile -o profile.stats mail_parser/cli.py
uv run python -m pstats profile.stats
```

### Profile Rust
```bash
cd mail_parser_rust
cargo build --release
perf record --call-graph=dwarf ./target/release/mail_parser_rust
perf report
```

### Benchmarks
```bash
cd mail_parser_rust
cargo bench
```

## CI/CD

### Check CI Locally
```bash
# Run what CI runs
./scripts/lint.sh
./scripts/test.sh --coverage
./scripts/build.sh --release
```

### View CI Status
- GitHub Actions tab in repository
- Check README badges

### Re-run Failed CI
- Go to Actions tab
- Click failed workflow
- Click "Re-run jobs"

## Release

### Create Release
```bash
# Update version in pyproject.toml and Cargo.toml
# Commit version bump
git commit -m "chore: Bump version to 1.1.0"
git tag v1.1.0
git push origin v1.1.0
# CI automatically publishes to PyPI
```

### Test Release
```bash
# Build locally
./scripts/build.sh --release

# Test wheel
pip install dist/*.whl
python -c "import mail_parser; print('OK')"
```

## Documentation

### Build Docs
```bash
# If using Sphinx
cd docs
make html
open _build/html/index.html
```

### Update Docs
- README.md - Main documentation
- CONTRIBUTING.md - Developer guide
- scripts/README.md - Script documentation
- Docstrings in code

## Useful Commands

### Find TODOs
```bash
rg "TODO|FIXME|XXX|HACK" --type py --type rust
```

### Count Lines of Code
```bash
# Python
find mail_parser -name "*.py" | xargs wc -l

# Rust
find mail_parser_rust/src -name "*.rs" | xargs wc -l
```

### Check Coverage
```bash
./scripts/test.sh --coverage
open htmlcov/index.html
```

### Update Dependencies
```bash
# Python
uv pip list --outdated
uv pip install --upgrade <package>

# Rust
cd mail_parser_rust
cargo update
```

## Quick Links

- **Repository:** https://github.com/auricleinc/mail_parser
- **Issues:** https://github.com/auricleinc/mail_parser/issues
- **CI:** https://github.com/auricleinc/mail_parser/actions
- **Coverage:** https://codecov.io/gh/auricleinc/mail_parser

---

**Tip:** Bookmark this file for quick access to common commands!
