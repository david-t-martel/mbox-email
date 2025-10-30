# Installation Guide for mail_parser_rust

This guide explains how to build and install the `mail_parser_rust` extension.

## Prerequisites

### Required
- **Rust** 1.70 or later ([install from rustup.rs](https://rustup.rs))
- **Python** 3.10 or later
- **maturin** (Python package for building Rust extensions)

### Verify Installation
```bash
# Check Rust version
rustc --version  # Should be 1.70+

# Check Python version
python --version  # Should be 3.10+

# Install maturin if not already installed
uv pip install maturin
```

## Installation Methods

### Method 1: Development Install (Recommended for Development)

This creates a symlink to the built extension, allowing changes to be immediately reflected:

```bash
cd mail_parser_rust/

# Build and install in one step
maturin develop --release

# Or use the Makefile
make install
```

To install to the parent project's venv:
```bash
make install-parent
```

### Method 2: Build Wheel and Install

Build a wheel package that can be distributed:

```bash
cd mail_parser_rust/

# Build the wheel
maturin build --release

# Install the wheel
uv pip install target/wheels/mail_parser_rust-*.whl
```

### Method 3: Install from Parent Project

From the parent `mail_parser` directory:

```bash
# Install the main package with Rust extension support
uv pip install -e .[build]

# Then build and install the Rust extension
cd mail_parser_rust/
maturin develop --release
```

### Method 4: Using the Build Script

The included build script provides a convenient wrapper:

```bash
cd mail_parser_rust/

# Build, test, and install
./build.sh --test --clippy --install-parent

# Just build
./build.sh

# Build dev version (faster compilation, no optimizations)
./build.sh --dev
```

## Verification

After installation, verify the extension works:

```python
# Python shell
import mail_parser_rust

# Check version
print(mail_parser_rust.__version__)

# Test a function
emails = mail_parser_rust.extract_emails_fast("Contact: john@example.com")
print(emails)  # ['john@example.com']
```

## Integration with mail_parser

The main `mail_parser` package automatically detects and uses the Rust extension if available:

```python
from mail_parser import EmailParser

# The parser will automatically use Rust functions when available
parser = EmailParser()
# Now 10-100x faster!
```

## Troubleshooting

### Rust Not Found
```
Error: Rust/Cargo not found
```
**Solution**: Install Rust from https://rustup.rs

### Wrong Python Version
```
Error: requires-python >=3.10
```
**Solution**: Upgrade Python or create a venv with Python 3.10+

### Build Fails with Linking Errors
**On Linux**: Install build essentials
```bash
sudo apt-get install build-essential
```

**On WSL**: Make sure you're using native Linux Rust, not Windows Rust
```bash
# Check Rust path
which rustc  # Should be /home/user/.cargo/bin/rustc, not /mnt/c/...
```

**On macOS**: Install Xcode Command Line Tools
```bash
xcode-select --install
```

### Extension Not Found After Install
```python
ModuleNotFoundError: No module named 'mail_parser_rust'
```

**Solution**: Make sure you're in the correct Python environment
```bash
# Activate the parent project's venv
source ../.venv/bin/activate

# Reinstall
cd mail_parser_rust/
maturin develop --release
```

### Performance Not as Expected

Make sure you built with the `--release` flag:
```bash
# NOT THIS (debug build, very slow)
maturin develop

# THIS (optimized build, full speed)
maturin develop --release
```

## Advanced Options

### Cross-Compilation

Build for a different target:
```bash
# Install target
rustup target add x86_64-pc-windows-gnu

# Build for Windows from Linux
maturin build --release --target x86_64-pc-windows-gnu
```

### Custom Build Configuration

The extension respects these environment variables:

```bash
# Use custom Python
export PYTHON_SYS_EXECUTABLE=/usr/bin/python3.11
maturin develop --release

# Enable additional optimizations
export RUSTFLAGS="-C target-cpu=native"
maturin develop --release
```

### Build with Debug Symbols

For profiling or debugging:
```bash
# Build with debug symbols but release optimizations
cargo build --profile release-with-debug
```

## Uninstallation

```bash
# Uninstall the extension
uv pip uninstall mail_parser_rust

# Clean build artifacts
cd mail_parser_rust/
make clean
```

## Development Workflow

Recommended workflow for development:

```bash
# 1. Make changes to src/lib.rs

# 2. Run checks
make check  # Runs clippy, fmt, and tests

# 3. Build and install
make dev-install  # Runs check, build, and install-parent

# 4. Test in parent project
cd ..
uv run python -m pytest -xvs tests/
```

## Performance Tips

1. **Always use --release**: Debug builds are 10-100x slower
2. **Enable LTO**: Already enabled in Cargo.toml for release builds
3. **Use native CPU features**: Set `RUSTFLAGS="-C target-cpu=native"`
4. **Profile before optimizing**: Use `cargo bench` to find bottlenecks

## Getting Help

- Check the [README.md](README.md) for project overview
- Review the [Rust source code](src/lib.rs) for API documentation
- Open an issue on GitHub for bugs or feature requests
