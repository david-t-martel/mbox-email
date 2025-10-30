# Development Scripts

This directory contains automation scripts for development workflow.

## Available Scripts

### setup.sh
**Initial project setup**

```bash
./scripts/setup.sh
```

**What it does:**
- Checks and installs prerequisites (Python, UV, Rust)
- Creates Python virtual environment
- Installs Python dependencies
- Builds Rust extension with maturin
- Installs pre-commit hooks
- Verifies installation
- Creates necessary directories

**When to use:**
- First time setting up the project
- After cloning the repository
- After major dependency changes

---

### test.sh
**Run all tests (Python + Rust)**

```bash
# Run all tests
./scripts/test.sh

# Run with coverage reports
./scripts/test.sh --coverage

# Run in parallel (faster)
./scripts/test.sh --parallel

# Run only Python tests
./scripts/test.sh --python

# Run only Rust tests
./scripts/test.sh --rust

# Verbose output
./scripts/test.sh --verbose
```

**What it does:**
- Runs pytest for Python tests
- Runs cargo test for Rust tests
- Generates coverage reports (if requested)
- Runs doc tests for Rust

**When to use:**
- Before committing changes
- After implementing new features
- When fixing bugs
- During development

---

### lint.sh
**Run all linters and formatters**

```bash
# Check code quality
./scripts/lint.sh

# Auto-fix issues
./scripts/lint.sh --fix

# Lint only Python
./scripts/lint.sh --python

# Lint only Rust
./scripts/lint.sh --rust
```

**What it does:**

**Python:**
- Black (code formatting)
- isort (import sorting)
- Ruff (linting)
- mypy (type checking)
- bandit (security)
- pydocstyle (docstrings)

**Rust:**
- rustfmt (code formatting)
- clippy (linting)
- cargo check (compilation)
- cargo audit (security)

**When to use:**
- Before committing (pre-commit hooks run automatically)
- When you want to manually check code quality
- To auto-fix formatting issues
- After adding new code

---

### build.sh
**Build Python package and Rust extension**

```bash
# Build in development mode
./scripts/build.sh

# Build in release mode (optimized)
./scripts/build.sh --release

# Clean before building
./scripts/build.sh --clean

# Build and install
./scripts/build.sh --install
```

**What it does:**
- Builds Rust extension with maturin
- Builds Python package (sdist + wheel)
- Optionally installs packages
- Verifies builds

**When to use:**
- Before creating a release
- When testing package distribution
- After modifying Rust code
- When preparing for deployment

---

### clean.sh
**Clean build artifacts and temporary files**

```bash
# Clean build artifacts (keeps venv)
./scripts/clean.sh

# Deep clean (removes venv too)
./scripts/clean.sh --deep

# Clean only cache files
./scripts/clean.sh --cache
```

**What it does:**
- Removes Python build artifacts
- Removes Rust build artifacts
- Removes test/coverage reports
- Removes cache files
- Optionally removes virtual environment

**When to use:**
- When build artifacts are corrupted
- Before creating a fresh build
- To free up disk space
- When switching between branches

---

## Script Options Summary

| Script | Common Options |
|--------|----------------|
| setup.sh | (no options) |
| test.sh | `--coverage`, `--parallel`, `--python`, `--rust`, `--verbose` |
| lint.sh | `--fix`, `--python`, `--rust` |
| build.sh | `--release`, `--clean`, `--install` |
| clean.sh | `--deep`, `--cache` |

## Development Workflow

### First-time Setup
```bash
git clone https://github.com/YOUR_USERNAME/mail_parser.git
cd mail_parser
./scripts/setup.sh
```

### Daily Development
```bash
# Make changes to code...

# Check code quality
./scripts/lint.sh --fix

# Run tests
./scripts/test.sh

# Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: Add new feature"
```

### Before Release
```bash
# Clean everything
./scripts/clean.sh --deep

# Fresh setup
./scripts/setup.sh

# Run all tests with coverage
./scripts/test.sh --coverage

# Lint everything
./scripts/lint.sh

# Build release packages
./scripts/build.sh --release
```

### Troubleshooting

**Problem: Scripts won't execute**
```bash
chmod +x scripts/*.sh
```

**Problem: Dependencies out of sync**
```bash
./scripts/clean.sh --deep
./scripts/setup.sh
```

**Problem: Rust extension won't build**
```bash
cd mail_parser_rust
cargo clean
cd ..
./scripts/build.sh --clean --release
```

**Problem: Tests failing**
```bash
./scripts/test.sh --verbose
# Check error messages
```

## Cross-Platform Notes

### Linux/macOS
Scripts work out of the box:
```bash
./scripts/setup.sh
```

### Windows (WSL)
Scripts work in WSL Ubuntu:
```bash
./scripts/setup.sh
```

### Windows (PowerShell)
Use Git Bash or WSL. Native PowerShell support coming soon.

## CI/CD Integration

These scripts are used by GitHub Actions workflows:

- **ci.yml** - Uses test.sh, lint.sh
- **rust-ci.yml** - Uses test.sh --rust, lint.sh --rust
- **release.yml** - Uses build.sh --release

## Contributing

When adding new scripts:
1. Make them executable: `chmod +x scripts/new-script.sh`
2. Add help text with `--help` flag
3. Use colored output (see existing scripts)
4. Update this README
5. Test on Linux, macOS, and WSL
