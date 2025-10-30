# Makefile for mail_parser_rust extension
# Provides common development tasks

.PHONY: help build build-release install install-parent test clippy fmt clean check bench

# Default target
help:
	@echo "mail_parser_rust - High-Performance Email Parsing Extension"
	@echo ""
	@echo "Available targets:"
	@echo "  make build          - Build debug version"
	@echo "  make build-release  - Build optimized release version"
	@echo "  make install        - Install to current Python environment"
	@echo "  make install-parent - Install to parent project's venv"
	@echo "  make test           - Run all tests"
	@echo "  make clippy         - Run clippy linter"
	@echo "  make fmt            - Format code with rustfmt"
	@echo "  make check          - Run all checks (clippy + fmt + test)"
	@echo "  make bench          - Run benchmarks"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make fix            - Auto-fix clippy warnings and format"
	@echo ""
	@echo "Development workflow:"
	@echo "  1. make check          # Verify code quality"
	@echo "  2. make build-release  # Build optimized version"
	@echo "  3. make install-parent # Install to parent project"

# Build targets
build:
	@echo "Building debug version..."
	cargo build

build-release:
	@echo "Building release version..."
	cargo build --release
	@echo "Build complete: target/release/libmail_parser_rust.so"

# Install targets
install:
	@echo "Installing to current Python environment..."
	maturin develop --release

install-parent:
	@echo "Installing to parent project venv..."
	@if [ -d "../.venv" ]; then \
		. ../.venv/bin/activate && maturin develop --release; \
		echo "Installed to parent project's venv"; \
	else \
		echo "Error: Parent venv not found at ../.venv"; \
		exit 1; \
	fi

# Testing
test:
	@echo "Running tests..."
	cargo test --all-features -- --nocapture

bench:
	@echo "Running benchmarks..."
	cargo bench --all-features

# Code quality
clippy:
	@echo "Running clippy..."
	cargo clippy --all-features -- -D warnings

fmt:
	@echo "Checking formatting..."
	cargo fmt -- --check

fmt-fix:
	@echo "Formatting code..."
	cargo fmt

fix:
	@echo "Auto-fixing clippy warnings and formatting..."
	cargo clippy --fix --allow-dirty --allow-staged
	cargo fmt

# Comprehensive check
check: clippy fmt test
	@echo "All checks passed!"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	cargo clean
	rm -rf target/
	rm -rf .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete"

# Development helpers
dev-install: check build-release install-parent
	@echo "Development build and install complete!"

# Show compiled extension info
info:
	@echo "Extension Information:"
	@echo "  Name: mail_parser_rust"
	@echo "  Version: $(shell cargo pkgid | cut -d@ -f2)"
	@echo "  Rust version: $(shell rustc --version)"
	@echo "  PyO3 version: 0.25.0"
	@echo ""
	@if [ -f "target/release/libmail_parser_rust.so" ]; then \
		echo "Release build:"; \
		ls -lh target/release/libmail_parser_rust.so; \
	fi
