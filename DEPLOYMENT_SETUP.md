# Deployment Setup - Mail Parser

This document describes the complete pre-commit and CI/CD setup for the Mail Parser project.

## What Was Created

### Pre-commit Hooks Configuration
**File:** `.pre-commit-config.yaml`

Comprehensive pre-commit hooks covering:

#### Python Checks
- **black** - Code formatting (auto-fix)
- **isort** - Import sorting (auto-fix)
- **ruff** - Fast linting with auto-fix
- **mypy** - Type checking
- **bandit** - Security scanning
- **pydocstyle** - Docstring validation

#### Rust Checks
- **rustfmt** - Code formatting (auto-fix)
- **clippy** - Linting with warnings as errors
- **cargo audit** - Security vulnerability scanning

#### General Checks
- Trailing whitespace removal
- End-of-file fixing
- YAML/TOML/JSON validation
- Large file detection
- Secret detection (detect-secrets)
- Markdown linting (markdownlint)

#### Custom Local Hooks
- Sensitive file protection
- Python dependency sync check
- Rust tests execution
- Python smoke tests

### GitHub Actions Workflows

#### 1. ci.yml - Main CI Pipeline
**Runs on:** Push to main/develop, Pull Requests

**Jobs:**
- **python-quality** - Linting, type checking, security
- **python-tests** - Multi-version testing (3.10, 3.11, 3.12) on Linux/Windows/macOS
- **integration-tests** - Python + Rust integration
- **pre-commit** - Pre-commit hooks validation
- **build-check** - Package building and verification

**Features:**
- Code coverage with Codecov
- Parallel testing
- Cached dependencies
- Multi-platform support

#### 2. rust-ci.yml - Rust-Specific CI
**Runs on:** Push/PR affecting Rust code

**Jobs:**
- **rust-quality** - rustfmt, clippy, cargo audit
- **rust-tests** - Multi-platform testing (stable + nightly)
- **rust-coverage** - Coverage with cargo-llvm-cov
- **benchmarks** - Performance benchmarking
- **build-pyo3** - PyO3 extension building (all platforms, all Python versions)
- **dependency-audit** - Security and outdated dependency checks

#### 3. release.yml - Release Automation
**Runs on:** Version tags (v*.*.*), releases, manual trigger

**Jobs:**
- **build-wheels** - Multi-platform wheel building with maturin
- **build-sdist** - Source distribution building
- **test-wheels** - Wheel installation and testing
- **publish-pypi** - PyPI publication
- **publish-test-pypi** - Test PyPI publication
- **create-release** - GitHub release creation
- **build-docs** - Documentation building and deployment

**Features:**
- manylinux wheel support
- Cross-platform wheels (Linux/Windows/macOS)
- Multi-Python version support (3.10, 3.11, 3.12)
- Automated PyPI publishing
- GitHub Pages documentation

### Development Scripts

All scripts in `scripts/` directory with full documentation.

#### setup.sh
- Automated development environment setup
- Prerequisites checking and installation
- Virtual environment creation
- Dependency installation
- Rust extension building
- Pre-commit hooks installation
- Installation verification

#### test.sh
- Run all tests (Python + Rust)
- Coverage report generation
- Parallel test execution
- Selective testing (Python-only, Rust-only)
- Verbose mode

#### lint.sh
- Run all linters
- Auto-fix mode
- Selective linting (Python-only, Rust-only)
- Security checks
- Type checking

#### build.sh
- Build Python package
- Build Rust extension
- Release mode (optimized)
- Clean build support
- Automatic installation
- Build verification

#### clean.sh
- Clean build artifacts
- Remove cache files
- Deep clean (including venv)
- Cache-only clean
- Cross-platform support

### Configuration Files

#### .gitignore (Updated)
Added Rust-specific ignores:
- Rust build artifacts (`target/`)
- Cargo.lock (for library crates)
- Rust incremental compilation files
- Maturin build artifacts
- Coverage reports (Python + Rust)
- Pre-commit artifacts

#### .secrets.baseline
Initial baseline for detect-secrets hook to avoid false positives.

#### .codecov.yml
Codecov configuration:
- Coverage targets (80% Python, 70% Rust)
- Flag-based reporting
- Comment configuration
- Ignore patterns

#### pyproject.toml (Enhanced)
Added configurations for:
- **[tool.bandit]** - Security linter settings
- **[tool.pydocstyle]** - Docstring conventions

Already had comprehensive configs for:
- black, ruff, isort, mypy, pytest, coverage

### Documentation Updates

#### CONTRIBUTING.md (Major Update)
New sections:
- **Quick Setup** - Automated setup instructions
- **Manual Setup** - Step-by-step manual process
- **Project Structure** - Updated with Rust and scripts
- **Python Style** - Automated tooling documentation
- **Rust Style** - Rust conventions and tools
- **Pre-commit Hooks** - How they work and troubleshooting
- **Commit Messages** - Conventional commits format
- **Testing** - Running tests, writing tests (Python + Rust)
- **Coverage Requirements** - Minimum coverage standards
- **Integration Tests** - Python-Rust interface testing

#### scripts/README.md (New)
Complete documentation for all development scripts:
- Script descriptions
- Usage examples
- Options summary
- Development workflows
- Troubleshooting guide
- Cross-platform notes

## How to Use

### Initial Setup
```bash
# Clone repository
git clone https://github.com/auricleinc/mail_parser.git
cd mail_parser

# Run automated setup
./scripts/setup.sh
```

### Development Workflow
```bash
# Make changes to code...

# Auto-format and lint
./scripts/lint.sh --fix

# Run tests
./scripts/test.sh

# Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: Add awesome feature"

# Push (CI runs automatically)
git push origin feature-branch
```

### Release Workflow
```bash
# Update version in pyproject.toml and Cargo.toml
# Commit version bump
git commit -m "chore: Bump version to 1.1.0"

# Create and push tag
git tag v1.1.0
git push origin v1.1.0

# GitHub Actions will:
# 1. Run all tests
# 2. Build wheels for all platforms
# 3. Publish to PyPI
# 4. Create GitHub release
# 5. Deploy documentation
```

## CI/CD Features

### Automated Quality Gates
✅ Code formatting (black, rustfmt)
✅ Import sorting (isort)
✅ Linting (ruff, clippy)
✅ Type checking (mypy)
✅ Security scanning (bandit, cargo audit)
✅ Secret detection
✅ Test execution (pytest, cargo test)
✅ Coverage reporting (Codecov)
✅ Multi-platform testing
✅ Multi-Python version testing

### Deployment Automation
✅ Wheel building (manylinux, Windows, macOS)
✅ PyPI publishing (automatic on release)
✅ GitHub releases (automatic with artifacts)
✅ Documentation deployment (GitHub Pages)
✅ Test PyPI support (for testing)

### Performance Features
✅ Dependency caching (UV, Cargo)
✅ Parallel testing
✅ Incremental builds
✅ Benchmark tracking

## Environment Variables Needed

### For GitHub Actions

#### PyPI Publishing (Required for releases)
```bash
PYPI_TOKEN=<your-pypi-token>
TEST_PYPI_TOKEN=<your-test-pypi-token>
```

#### Code Coverage (Optional but recommended)
```bash
CODECOV_TOKEN=<your-codecov-token>
```

### Setting Secrets in GitHub
1. Go to repository Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `PYPI_TOKEN`
   - `TEST_PYPI_TOKEN`
   - `CODECOV_TOKEN`

## Pre-commit Hook Bypass (NOT RECOMMENDED)

If you absolutely must bypass pre-commit hooks:
```bash
# NOT RECOMMENDED - only for emergencies
git commit --no-verify -m "Emergency fix"
```

**Warning:** CI will still run all checks and may fail.

## Troubleshooting

### Pre-commit hooks failing
```bash
# Auto-fix most issues
./scripts/lint.sh --fix

# Re-run pre-commit
git add -u
git commit -m "Your message"
```

### Rust extension build failing
```bash
# Clean and rebuild
cd mail_parser_rust
cargo clean
cd ..
./scripts/build.sh --clean --release
```

### Tests failing in CI but passing locally
```bash
# Run tests exactly as CI does
./scripts/test.sh --coverage --verbose

# Check multiple Python versions
uv run --python 3.10 pytest
uv run --python 3.11 pytest
uv run --python 3.12 pytest
```

### GitHub Actions workflow not triggering
- Check branch protection rules
- Verify workflow files are in `.github/workflows/`
- Check YAML syntax with `yamllint`
- Review GitHub Actions logs

## Production-Ready Features

### Zero-Downtime Deployment
- manylinux wheels ensure broad Linux compatibility
- Windows and macOS wheels included
- Automatic wheel testing before publication

### Monitoring
- Code coverage tracking
- Security vulnerability scanning
- Dependency update checks
- Performance benchmarking

### Quality Assurance
- Multi-platform testing
- Multi-Python version support
- Integration testing
- Strict linting and type checking

### Security
- Secret detection in commits
- Security linting (bandit, cargo audit)
- Dependency vulnerability scanning
- No secrets in repository

## Next Steps

1. **Set up GitHub Secrets** for PyPI and Codecov
2. **Enable branch protection** on main branch
3. **Configure Codecov** integration
4. **Test release workflow** with Test PyPI
5. **Add more tests** to improve coverage
6. **Create first release** when ready

## Support

- **Issues:** https://github.com/auricleinc/mail_parser/issues
- **Documentation:** CONTRIBUTING.md, scripts/README.md
- **Email:** david.martel@auricleinc.com

---

**Generated:** 2025-10-30
**Version:** 1.0.0
**Status:** Production-ready ✅
