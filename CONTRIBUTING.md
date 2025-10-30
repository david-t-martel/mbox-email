# Contributing to Mail Parser

First off, thank you for considering contributing to Mail Parser! It's people like you that make this tool better for everyone.

## Code of Conduct

Be respectful, inclusive, and professional. We're all here to make email management better!

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include:

- **Clear title** describing the problem
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **System information** (OS, Python version, UV version)
- **Log files** if applicable (sanitize personal data!)
- **mbox file size** and email count

**Example:**
```
Title: Dashboard fails to load with 100K+ emails

Environment:
- OS: macOS 13.5
- Python: 3.11.5
- UV: 0.4.10
- Emails: 150,000
- mbox size: 8GB

Steps:
1. Run parser on 150K emails
2. Open index.html
3. Browser becomes unresponsive

Expected: Dashboard loads with pagination
Actual: Browser freezes after 30 seconds
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting:

- **Use a clear title**
- **Provide detailed description** of the suggested enhancement
- **Explain why** this would be useful
- **List examples** of how it would work

### Pull Requests

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

#### Pull Request Guidelines

- Follow existing code style (PEP 8 for Python)
- Write clear commit messages
- Update README.md if needed
- Add yourself to CONTRIBUTORS.md
- Include examples in docstrings
- Test on multiple platforms if possible

## Development Setup

### Quick Setup (Recommended)

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/mail_parser.git
cd mail_parser

# Run automated setup script (installs everything)
./scripts/setup.sh
```

The setup script will:
- Install UV and Rust if needed
- Create Python virtual environment
- Install all Python dependencies
- Build Rust extension with maturin
- Install pre-commit hooks
- Verify installation

### Manual Setup

If you prefer manual setup:

```bash
# 1. Create virtual environment
uv venv
source .venv/bin/activate  # or .venv/Scripts/activate on Windows

# 2. Install Python dependencies
uv pip install -e ".[dev]"

# 3. Install development tools
uv pip install pre-commit pytest pytest-cov black ruff mypy isort maturin

# 4. Build Rust extension
cd mail_parser_rust
maturin develop --release
cd ..

# 5. Install pre-commit hooks
uv run pre-commit install
```

### Verifying Your Setup

```bash
# Run all tests
./scripts/test.sh

# Run linters
./scripts/lint.sh

# Build everything
./scripts/build.sh
```

## Project Structure

```
mail_parser/
├── mail_parser/           # Python package
│   ├── core/              # Core parsing logic
│   ├── renderers/         # HTML generation
│   ├── organizers/        # File organization
│   ├── api/               # Gmail API integration
│   ├── analysis/          # Statistics and analytics
│   ├── indexing/          # Database and search
│   ├── dashboard/         # Web dashboard
│   └── cli.py             # CLI interface
├── mail_parser_rust/      # Rust extension (PyO3)
│   ├── src/
│   │   ├── lib.rs         # PyO3 bindings
│   │   ├── parser.rs      # Fast email parsing
│   │   └── utils.rs       # Utilities
│   ├── Cargo.toml         # Rust dependencies
│   └── benches/           # Performance benchmarks
├── scripts/               # Development scripts
│   ├── setup.sh           # Initial setup
│   ├── test.sh            # Run all tests
│   ├── lint.sh            # Run all linters
│   ├── build.sh           # Build packages
│   └── clean.sh           # Clean artifacts
├── .github/workflows/     # CI/CD pipelines
│   ├── ci.yml             # Main CI pipeline
│   ├── rust-ci.yml        # Rust-specific CI
│   └── release.yml        # Release automation
├── config/                # Configuration templates
├── tests/                 # Unit tests
└── docs/                  # Documentation
```

## Coding Conventions

### Python Style

We enforce code quality with automated tools. All Python code must:

- Follow **PEP 8** (enforced by `black` and `ruff`)
- Use **type hints** for all function signatures
- Include **Google-style docstrings** for public functions
- Pass **mypy** type checking
- Pass **bandit** security checks

**Code formatting is automatic:**
```bash
# Auto-format code
./scripts/lint.sh --fix

# Or run individual formatters
uv run black mail_parser/
uv run isort mail_parser/
uv run ruff check mail_parser/ --fix
```

**Example well-formatted code:**
```python
from typing import Any
from datetime import datetime

def generate_filename(
    metadata: dict[str, Any],
    email_index: int,
    extension: str = 'html'
) -> str:
    """Generate human-readable filename for email.

    Args:
        metadata: Email metadata dictionary containing date, from, subject
        email_index: Unique email index number (0-based)
        extension: File extension without dot (default: html)

    Returns:
        Sanitized filename string in format YYYYMMDD_HHMM_sender_subject_NNNNNN.ext

    Raises:
        ValueError: If metadata is missing required fields

    Example:
        >>> metadata = {
        ...     'date': datetime(2025, 10, 28, 14, 44),
        ...     'subject': 'Meeting Notes'
        ... }
        >>> generate_filename(metadata, 123)
        '20251028_1444_sender_meeting_notes_000123.html'
    """
    # Implementation...
```

### Rust Style

All Rust code must:

- Follow **rustfmt** formatting (automatic)
- Pass **clippy** lints with no warnings
- Include **documentation comments** for public APIs
- Pass **cargo audit** security checks

**Rust formatting is automatic:**
```bash
# Auto-format Rust code
cd mail_parser_rust
cargo fmt

# Run clippy with auto-fixes
cargo clippy --fix --allow-dirty
```

**Example Rust code:**
```rust
/// Parse email headers efficiently using memory-mapped files.
///
/// This function uses SIMD-optimized regex and memory mapping
/// for 10-100x faster parsing than Python's email.parser.
///
/// # Arguments
///
/// * `file_path` - Path to the email file or mbox
/// * `offset` - Byte offset to start parsing
///
/// # Returns
///
/// Parsed email metadata as a Python dict
///
/// # Example
///
/// ```python
/// from mail_parser_rust import parse_email_fast
/// metadata = parse_email_fast("email.eml", 0)
/// print(metadata['subject'])
/// ```
#[pyfunction]
pub fn parse_email_fast(file_path: &str, offset: usize) -> PyResult<PyObject> {
    // Implementation...
}
```

### Pre-commit Hooks

All commits automatically run pre-commit hooks that:

1. **Format code** (black, rustfmt)
2. **Sort imports** (isort)
3. **Lint code** (ruff, clippy)
4. **Check types** (mypy)
5. **Scan for secrets** (detect-secrets)
6. **Validate files** (trailing whitespace, YAML, TOML)

**If pre-commit fails:**
```bash
# Pre-commit auto-fixes most issues
git add -u
git commit -m "Your message"
# Hooks run and fix issues

# Manually fix remaining issues
./scripts/lint.sh --fix

# Commit fixed code
git add -u
git commit -m "Your message"
```

### Commit Messages

Use clear, descriptive commit messages following conventional commits:

```
type(scope): Brief description (50 chars max)

Detailed explanation of what changed and why.
Include motivation and context.

- Bullet points for multiple changes
- Reference issues: Fixes #123
- Break lines at 72 characters

Example: feat(rust): Add SIMD-optimized email parsing
```

**Commit types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Build process, dependencies
- `ci`: CI/CD changes

## Areas for Contribution

### High Priority

- [ ] **Tests!** - Unit tests, integration tests
- [ ] **Performance optimization** - Faster parsing
- [ ] **Export formats** - PST, EML, etc.
- [ ] **Advanced search** - Regex, date ranges
- [ ] **Email threading** - Better conversation detection

### Medium Priority

- [ ] **Themes** - Dashboard color schemes
- [ ] **Plugins** - Extensible architecture
- [ ] **Cloud storage** - S3, Google Drive integration
- [ ] **Mobile app** - React Native viewer
- [ ] **Encryption** - PGP support

### Documentation

- [ ] Video tutorials
- [ ] More examples
- [ ] Troubleshooting guide
- [ ] Performance tuning guide
- [ ] API documentation

## Testing

### Running Tests

```bash
# Run all tests (Python + Rust)
./scripts/test.sh

# Run with coverage
./scripts/test.sh --coverage

# Run in parallel (faster)
./scripts/test.sh --parallel

# Run only Python tests
./scripts/test.sh --python

# Run only Rust tests
./scripts/test.sh --rust
```

### Writing Python Tests

All new features must include tests. We use `pytest`:

```python
# tests/test_filename_generator.py
import pytest
from datetime import datetime
from mail_parser.core.filename_generator import FilenameGenerator


class TestFilenameGenerator:
    """Test suite for FilenameGenerator."""

    def test_sanitize_filename(self):
        """Test filename sanitization removes special characters."""
        gen = FilenameGenerator()
        result = gen.sanitize_for_filename('Test: Email/Subject')
        assert result == 'Test_Email_Subject'

    def test_generate_filename(self):
        """Test filename generation with full metadata."""
        metadata = {
            'date': datetime(2025, 10, 28, 14, 44),
            'from': {'name': 'John Doe', 'email': 'john@example.com'},
            'subject': 'Meeting Notes'
        }
        gen = FilenameGenerator()
        result = gen.generate_filename(metadata, 123)

        assert result.startswith('20251028_1444_')
        assert '_000123.html' in result
        assert 'meeting_notes' in result.lower()

    @pytest.mark.parametrize("subject,expected", [
        ("Simple Subject", "simple_subject"),
        ("Subject: With/Special*Chars", "subject_with_special_chars"),
        ("", "no_subject"),
    ])
    def test_sanitize_parametrized(self, subject, expected):
        """Test sanitization with multiple inputs."""
        gen = FilenameGenerator()
        result = gen.sanitize_for_filename(subject)
        assert expected in result.lower()
```

### Writing Rust Tests

Rust tests use the built-in test framework:

```rust
// mail_parser_rust/src/parser.rs

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_email_header() {
        let email = b"From: test@example.com\r\n\
                      Subject: Test Email\r\n\
                      \r\n\
                      Body content";

        let result = parse_email_header(email).unwrap();
        assert_eq!(result.from, "test@example.com");
        assert_eq!(result.subject, "Test Email");
    }

    #[test]
    fn test_parse_invalid_email() {
        let email = b"Invalid email content";
        let result = parse_email_header(email);
        assert!(result.is_err());
    }
}

// Benchmarks (in benches/email_parsing.rs)
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn benchmark_parse_email(c: &mut Criterion) {
    let email = b"From: test@example.com\r\nSubject: Test\r\n\r\nBody";

    c.bench_function("parse_email_fast", |b| {
        b.iter(|| parse_email_header(black_box(email)))
    });
}

criterion_group!(benches, benchmark_parse_email);
criterion_main!(benches);
```

### Coverage Requirements

- **Minimum 80% coverage** for Python code
- **Minimum 70% coverage** for Rust code
- All public APIs must have tests
- Edge cases and error paths must be tested

### Integration Tests

Test the Python-Rust interface:

```python
# tests/test_integration.py
import pytest
import mail_parser_rust


@pytest.mark.integration
class TestRustIntegration:
    """Test Python-Rust integration."""

    def test_rust_parser_available(self):
        """Verify Rust extension is importable."""
        assert hasattr(mail_parser_rust, 'parse_email_fast')

    def test_rust_parser_performance(self):
        """Verify Rust parser is faster than Python."""
        import timeit

        # Compare Python vs Rust parsing
        python_time = timeit.timeit(
            'parse_email_python(sample)',
            globals={'parse_email_python': ..., 'sample': ...},
            number=1000
        )

        rust_time = timeit.timeit(
            'parse_email_fast(sample)',
            globals={'parse_email_fast': mail_parser_rust.parse_email_fast, 'sample': ...},
            number=1000
        )

        # Rust should be at least 10x faster
        assert rust_time < python_time / 10
```

## Questions?

- Open an issue with the `question` label
- Email: david.martel@auricleinc.com
- Read the docs: README.md, QUICK_START.md

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in commit history

Thank you for making Mail Parser better! 🎉
