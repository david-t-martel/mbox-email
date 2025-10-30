# Quick Reference Card

## 🚀 Essential Commands

### Build & Install
```bash
make dev-install        # Check + build + install to parent (recommended)
make build-release      # Build optimized version
make install-parent     # Install to parent project's venv
maturin develop --release  # Direct build and install
```

### Code Quality
```bash
make check              # Run all checks (clippy + fmt + tests)
make fix                # Auto-fix clippy warnings and format code
make test               # Run Rust tests
cargo fmt               # Format code
cargo clippy            # Run linter
```

### Benchmarking
```bash
make bench              # Run all benchmarks
cargo bench             # Alternative
# View results: open target/criterion/report/index.html
```

### Utilities
```bash
make clean              # Clean build artifacts
make info               # Show extension information
make help               # Show all available targets
```

## 📦 File Locations

| File | Location |
|------|----------|
| Rust source | `src/lib.rs` |
| Build config | `.cargo/config.toml` |
| Dependencies | `Cargo.toml` |
| Python metadata | `pyproject.toml` |
| Formatting | `rustfmt.toml` |
| Linting | `clippy.toml` |
| Benchmarks | `benches/email_parsing.rs` |

## 🐍 Python Usage

```python
import mail_parser_rust

# Check version
print(mail_parser_rust.__version__)

# Fast message counting
count = mail_parser_rust.count_messages_fast("emails.mbox")

# Encoding detection
encoding = mail_parser_rust.detect_encoding_fast(email_bytes)

# Extract emails
emails = mail_parser_rust.extract_emails_fast(text)

# Extract URLs
urls = mail_parser_rust.extract_urls_fast(text)

# Regex operations
matches = mail_parser_rust.regex_findall_fast(r"\d+", text)
result = mail_parser_rust.regex_replace_fast(r"\d+", "NUM", text)

# Utilities
clean = mail_parser_rust.sanitize_filename_fast(filename)
decoded = mail_parser_rust.decode_fast(bytes, "utf-8")
```

## ⚡ Performance Tips

1. **Always use --release**: `maturin develop --release`
2. **Native CPU optimizations**: `export RUSTFLAGS="-C target-cpu=native"`
3. **Profile first**: `cargo bench` before optimizing
4. **Check binary size**: `make info`

## 🔍 Troubleshooting

### Build fails
```bash
# Clean and rebuild
make clean
cargo clean
make dev-install
```

### Extension not found
```bash
# Verify installation
python -c "import mail_parser_rust; print(mail_parser_rust.__version__)"

# Reinstall
cd mail_parser_rust/
source ../.venv/bin/activate
maturin develop --release
```

### Slow performance
```bash
# Make sure you built with --release
maturin develop --release  # NOT just 'maturin develop'
```

## 📊 Performance Expectations

| Operation | Python | Rust | Speedup |
|-----------|--------|------|---------|
| Count messages | 2.5s | 0.05s | **50x** |
| Encoding detect | 100ms | 1ms | **100x** |
| Email extract | 50ms | 5ms | **10x** |
| Regex findall | 200ms | 4ms | **50x** |

## 🔧 Development Workflow

1. Edit `src/lib.rs`
2. Run `make fix` (auto-fix)
3. Run `make check` (verify)
4. Run `make dev-install` (build + install)
5. Test in parent project

## 📚 Documentation

- [README.md](README.md) - Full documentation
- [INSTALL.md](INSTALL.md) - Installation guide
- [SETUP_SUMMARY.md](SETUP_SUMMARY.md) - Configuration details

## 🎯 Cargo Aliases (from .cargo/config.toml)

```bash
cargo build-fast        # Quick release build (thin LTO)
cargo build-opt         # Maximum optimization (fat LTO)
cargo install-dev       # Build and install to Python
cargo test-all          # Run all tests with output
cargo bench-all         # Run all benchmarks
cargo fix               # Auto-fix clippy warnings
```

## ⚙️ Environment Variables

```bash
# Use specific Python
export PYTHON_SYS_EXECUTABLE=/usr/bin/python3.11

# CPU-specific optimizations
export RUSTFLAGS="-C target-cpu=native"

# Faster linking (Linux)
export RUSTFLAGS="-C link-arg=-fuse-ld=lld"
```

## ✅ Pre-commit Checklist

Before committing changes:

```bash
make fix        # Auto-fix issues
make check      # Verify quality
make test       # Run tests
make bench      # Check performance (optional)
```

---

**Quick Help**: Run `make help` or see [README.md](README.md) for full documentation.
