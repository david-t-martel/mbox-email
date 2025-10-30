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

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/mbox-email.git
cd mbox-email

# Install in development mode
uv pip install -e ".[dev]"

# Run tests (if you add them)
uv run pytest
```

## Project Structure

```
mail_parser/
├── mail_parser/
│   ├── core/              # Core parsing logic
│   ├── renderers/         # HTML generation
│   ├── organizers/        # File organization
│   ├── api/               # Gmail API integration
│   ├── analysis/          # Statistics and analytics
│   ├── indexing/          # Database and search
│   ├── dashboard/         # Web dashboard
│   └── cli.py             # CLI interface
├── config/
├── tests/                 # Unit tests (to be added)
└── docs/                  # Documentation
```

## Coding Conventions

### Python Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions focused and small
- Use descriptive variable names

**Example:**
```python
def generate_filename(
    metadata: dict[str, Any],
    email_index: int,
    extension: str = 'html'
) -> str:
    """
    Generate human-readable filename for email.

    Args:
        metadata: Email metadata dictionary
        email_index: Unique email index number
        extension: File extension (default: html)

    Returns:
        Sanitized filename string

    Example:
        >>> metadata = {'date': datetime(...), 'subject': 'Test'}
        >>> generate_filename(metadata, 123)
        '20251028_1444_sender_test_000123.html'
    """
    # Implementation...
```

### Commit Messages

Use clear, descriptive commit messages:

```
Add support for Maildir format

- Implement Maildir parser class
- Add tests for Maildir parsing
- Update documentation with Maildir examples
```

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

When adding features, please add tests:

```python
# tests/test_filename_generator.py
import pytest
from mail_parser.core.filename_generator import FilenameGenerator

def test_sanitize_filename():
    """Test filename sanitization."""
    gen = FilenameGenerator()
    result = gen.sanitize_for_filename('Test: Email/Subject')
    assert result == 'Test_Email_Subject'

def test_generate_filename():
    """Test filename generation."""
    metadata = {
        'date': datetime(2025, 10, 28, 14, 44),
        'from': {'name': 'John Doe', 'email': 'john@example.com'},
        'subject': 'Meeting Notes'
    }
    result = FilenameGenerator().generate_filename(metadata, 123)
    assert result.startswith('20251028_1444_')
    assert '_000123.html' in result
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
