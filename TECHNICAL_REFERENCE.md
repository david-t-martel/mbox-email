# 🔧 Gmail Parser Technical Reference

Comprehensive technical documentation for developers, system administrators, and technical contributors.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Performance Characteristics](#performance-characteristics)
3. [Development Setup](#development-setup)
4. [Deployment and CI/CD](#deployment-and-cicd)
5. [Core Components](#core-components)
6. [Optimization Details](#optimization-details)
7. [API Reference](#api-reference)
8. [Database Schema](#database-schema)
9. [Testing Framework](#testing-framework)
10. [Contributing Guidelines](#contributing-guidelines)
11. [Security Architecture](#security-architecture)
12. [Monitoring and Observability](#monitoring-and-observability)
13. [Troubleshooting Guide](#troubleshooting-guide)
14. [Performance Tuning](#performance-tuning)
15. [Development Quick Reference](#development-quick-reference)

---

## Architecture Overview

### System Design

Gmail Parser is a high-performance email parsing system built with a hybrid Python/Rust architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Dashboard (FastAPI)                 │
│                          Port 8080                          │
├─────────────────────────────────────────────────────────────┤
│                    API Layer (Python)                       │
│              FastAPI + Pydantic + async/await              │
├─────────────────────────────────────────────────────────────┤
│                 Business Logic Layer                        │
│         ┌──────────────┬──────────────────────┐           │
│         │ Python Core  │   Rust Extensions    │           │
│         │              │   (via PyO3)         │           │
│         └──────────────┴──────────────────────┘           │
├─────────────────────────────────────────────────────────────┤
│                    Data Layer                               │
│         ┌──────────────┬──────────────────────┐           │
│         │   SQLite     │   In-Memory Cache    │           │
│         │   (FTS5)     │   (Rust HashMap)     │           │
│         └──────────────┴──────────────────────┘           │
├─────────────────────────────────────────────────────────────┤
│                 Storage & File System                       │
│                   .mbox files / JSON                        │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Framework** | FastAPI | REST API, WebSocket support |
| **Frontend** | HTML5 + Alpine.js | Reactive UI without build step |
| **Database** | SQLite with FTS5 | Full-text search, ACID compliance |
| **Parser Core** | Python (stdlib) | Email parsing, MIME handling |
| **Performance Layer** | Rust (PyO3) | Header parsing, parallel processing |
| **Caching** | Rust HashMap | Sub-microsecond lookups |
| **Task Queue** | Python asyncio | Concurrent operations |
| **Web Server** | Uvicorn | ASGI server, production-ready |
| **Build System** | Maturin | Rust/Python integration |

### Key Design Decisions

1. **Hybrid Architecture**: Python for flexibility, Rust for performance-critical paths
2. **SQLite FTS5**: Enables instant full-text search without external dependencies
3. **Zero-copy Parsing**: Rust extensions use memory-mapped files for large mbox files
4. **Async Everything**: Full async/await stack for maximum concurrency
5. **Progressive Enhancement**: Works without JavaScript, enhanced with Alpine.js

---

## Performance Characteristics

### Benchmarks

| Metric | Performance | Details |
|--------|------------|---------|
| **Parse Speed** | 1,044 emails/sec | Single-threaded Python |
| **Parse Speed (Rust)** | 52,630 emails/sec | Multi-threaded Rust |
| **Search Latency** | < 10ms | 17,000 emails, any query |
| **Memory Usage** | 45MB base | +2.6MB per 1000 emails |
| **Startup Time** | 95ms | Time to first response |
| **Index Size** | ~10% of mbox | Compressed FTS5 index |

### Performance by Operation

```python
# Operation timing benchmarks (17,492 emails)
{
    "initial_parse": "16.76 seconds",      # 1,044 emails/sec
    "rust_parse": "0.332 seconds",         # 52,630 emails/sec
    "full_text_search": "8.3ms",          # Any query
    "exact_match": "0.9ms",                # Indexed field
    "thread_reconstruction": "12ms",       # 50-email thread
    "export_csv": "890ms",                 # 5,000 emails
    "statistics_calculation": "45ms",      # All metrics
}
```

### Resource Requirements

- **Minimum**: 2GB RAM, 2 CPU cores, 1GB free disk
- **Recommended**: 4GB RAM, 4 CPU cores, 5GB free disk
- **Large Archives** (100k+ emails): 8GB RAM, 8 CPU cores, 20GB free disk

---

## Development Setup

### Prerequisites

```bash
# System requirements
Python >= 3.8
Rust >= 1.70
Node.js >= 16 (for frontend tooling)
SQLite >= 3.35.0 (with FTS5 support)

# Python dependencies
uv >= 0.1.0  # Fast Python package manager
poetry >= 1.0 (optional, for dependency management)
```

### Quick Setup

```bash
# Clone repository
git clone https://github.com/auricleinc/mail_parser.git
cd mail_parser

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .
uv pip install -r requirements-dev.txt

# Build Rust extensions
maturin develop --release

# Run tests
pytest tests/ -v --cov=mail_parser --cov-report=html

# Start development server
uvicorn mail_parser.api.main:app --reload --port 8080
```

### Project Structure

```
mail_parser/
├── src/                      # Rust source code
│   ├── lib.rs               # Rust library entry point
│   ├── parser.rs            # High-performance email parser
│   ├── cache.rs             # In-memory caching layer
│   └── parallel.rs          # Parallel processing utilities
├── mail_parser/             # Python package
│   ├── __init__.py
│   ├── parser.py            # Main parser interface
│   ├── models.py            # Pydantic models
│   ├── database.py          # SQLite/FTS5 operations
│   ├── api/                 # FastAPI application
│   │   ├── main.py         # API entry point
│   │   ├── routes.py       # API endpoints
│   │   └── websocket.py    # Real-time updates
│   ├── rust_ext/           # Rust extension bindings
│   └── web/                # Frontend assets
├── tests/                   # Test suite
├── benchmarks/             # Performance benchmarks
├── scripts/                # Utility scripts
├── Cargo.toml             # Rust dependencies
├── pyproject.toml         # Python project config
└── Makefile               # Build automation
```

### Development Commands

```makefile
# Makefile targets
make dev        # Start development environment
make test       # Run all tests
make bench      # Run benchmarks
make build      # Build production release
make clean      # Clean build artifacts
make docs       # Generate documentation
make lint       # Run linters and formatters
make profile    # Run performance profiling
```

---

## Deployment and CI/CD

### Production Deployment

#### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim AS builder

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Build Rust extensions
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release

# Python stage
FROM python:3.11-slim
WORKDIR /app

# Copy Rust artifacts
COPY --from=builder /app/target/release/*.so ./

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY mail_parser ./mail_parser
COPY web ./web

# Run application
CMD ["uvicorn", "mail_parser.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### SystemD Service

```ini
# /etc/systemd/system/gmail-parser.service
[Unit]
Description=Gmail Parser Service
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/gmail-parser
Environment="PATH=/opt/gmail-parser/venv/bin"
ExecStart=/opt/gmail-parser/venv/bin/uvicorn mail_parser.api.main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
        rust-version: [stable, nightly]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Setup Rust
      uses: actions-rs/toolchain@v1
      with:
        toolchain: ${{ matrix.rust-version }}
    
    - name: Install dependencies
      run: |
        pip install uv
        uv pip install -e .
        uv pip install -r requirements-dev.txt
    
    - name: Build Rust extensions
      run: maturin develop
    
    - name: Run tests
      run: |
        pytest tests/ --cov=mail_parser --cov-report=xml
        cargo test
    
    - name: Run benchmarks
      run: |
        python benchmarks/run_benchmarks.py
        cargo bench
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        # Deployment script here
        echo "Deploying to production..."
```

---

## Core Components

### Email Parser

```python
# mail_parser/parser.py
class EmailParser:
    """High-performance email parser with Rust acceleration."""
    
    def __init__(self, use_rust: bool = True):
        self.use_rust = use_rust
        if use_rust:
            from mail_parser.rust_ext import RustParser
            self._rust_parser = RustParser()
    
    def parse_mbox(self, file_path: str) -> List[Email]:
        """Parse mbox file into Email objects."""
        if self.use_rust:
            # Use Rust for 50x speed improvement
            return self._rust_parser.parse_parallel(file_path)
        else:
            # Fallback to pure Python
            return self._parse_python(file_path)
    
    def parse_headers_only(self, file_path: str) -> List[Dict]:
        """Fast header-only parsing for initial scan."""
        # Rust implementation: 100x faster than full parse
        return self._rust_parser.scan_headers(file_path)
```

### Database Layer

```python
# mail_parser/database.py
class EmailDatabase:
    """SQLite FTS5 database for email storage and search."""
    
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_fts5()
    
    def _init_fts5(self):
        """Initialize FTS5 virtual table for full-text search."""
        self.conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS emails_fts USING fts5(
                message_id UNINDEXED,
                subject,
                from_addr,
                to_addr,
                cc_addr,
                date UNINDEXED,
                body,
                thread_id UNINDEXED,
                tokenize = 'porter unicode61'
            )
        """)
    
    def search(self, query: str, limit: int = 100) -> List[Email]:
        """Full-text search with relevance ranking."""
        sql = """
            SELECT *, rank
            FROM emails_fts
            WHERE emails_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """
        return self.execute(sql, (query, limit))
```

### Rust Extensions

```rust
// src/parser.rs
use pyo3::prelude::*;
use rayon::prelude::*;
use memmap2::MmapOptions;

#[pyfunction]
pub fn parse_parallel(file_path: &str) -> PyResult<Vec<Email>> {
    let file = std::fs::File::open(file_path)?;
    let mmap = unsafe { MmapOptions::new().map(&file)? };
    
    // Split on "From " boundaries
    let chunks = split_mbox(&mmap);
    
    // Parse in parallel using all CPU cores
    let emails: Vec<Email> = chunks
        .par_iter()
        .filter_map(|chunk| parse_email(chunk).ok())
        .collect();
    
    Ok(emails)
}

#[pyfunction]
pub fn scan_headers(file_path: &str) -> PyResult<Vec<HashMap<String, String>>> {
    // Ultra-fast header-only parsing
    // Skips body parsing for 100x speedup
    let file = std::fs::File::open(file_path)?;
    let reader = BufReader::new(file);
    
    let mut headers = Vec::new();
    let mut current = HashMap::new();
    
    for line in reader.lines() {
        let line = line?;
        if line.starts_with("From ") {
            if !current.is_empty() {
                headers.push(current.clone());
                current.clear();
            }
        } else if let Some((key, value)) = parse_header_line(&line) {
            current.insert(key, value);
        }
    }
    
    Ok(headers)
}
```

---

## Optimization Details

### Performance Optimizations Implemented

#### 1. Rust Header Parser (50x speedup)
```rust
// Before: Python regex parsing - 20 emails/sec
// After: Rust SIMD parsing - 1,000 emails/sec

pub fn parse_headers_simd(data: &[u8]) -> Headers {
    // Use SIMD instructions to find line boundaries
    let newlines = find_newlines_simd(data);
    
    // Parse headers in parallel
    newlines.par_windows(2)
        .filter_map(|w| parse_header_between(data, w[0], w[1]))
        .collect()
}
```

#### 2. Parallel Processing (10x speedup)
```python
# Before: Sequential processing
for email in emails:
    process_email(email)  # 1,000 emails = 10 seconds

# After: Parallel processing with thread pool
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_email, emails)  # 1,000 emails = 1 second
```

#### 3. Memory-Mapped Files (5x speedup for large files)
```rust
// Instead of reading entire file into memory
let contents = fs::read_to_string(path)?;  // Uses 2x file size in RAM

// Use memory-mapped file
let mmap = unsafe { MmapOptions::new().map(&file)? };  // Zero-copy access
```

#### 4. SQLite FTS5 Optimization
```sql
-- Optimized FTS5 configuration
CREATE VIRTUAL TABLE emails_fts USING fts5(
    subject,
    body,
    from_addr,
    to_addr,
    -- Optimize for common queries
    prefix='2 3 4',
    tokenize='porter unicode61 remove_diacritics 1',
    content='emails',
    content_rowid='id'
);

-- Create covering index for common queries
CREATE INDEX idx_emails_date ON emails(date DESC);
CREATE INDEX idx_emails_thread ON emails(thread_id, date);
```

#### 5. Lazy Loading and Streaming
```python
# Before: Load all emails into memory
emails = parser.parse_all()  # Uses GB of RAM

# After: Stream emails on-demand
for email in parser.stream_emails():  # Constant memory usage
    yield process_email(email)
```

#### 6. Caching Layer
```rust
// LRU cache for frequently accessed emails
pub struct EmailCache {
    cache: LruCache<String, Email>,
    stats: CacheStats,
}

impl EmailCache {
    pub fn get(&mut self, message_id: &str) -> Option<&Email> {
        self.stats.requests += 1;
        if let Some(email) = self.cache.get(message_id) {
            self.stats.hits += 1;
            Some(email)
        } else {
            None
        }
    }
}
```

### Memory Optimization

```python
# Memory usage optimization strategies

# 1. Use generators instead of lists
def process_emails(mbox_path):
    # Bad: Loads all into memory
    # emails = list(parse_mbox(mbox_path))
    
    # Good: Stream processing
    for email in parse_mbox_generator(mbox_path):
        yield process_email(email)

# 2. Clear caches periodically
@periodic_task(seconds=300)
def clear_caches():
    email_cache.clear_old_entries()
    gc.collect()  # Force garbage collection

# 3. Use slots for memory efficiency
class Email:
    __slots__ = ['message_id', 'subject', 'from_addr', 'to_addr', 
                 'date', 'body', 'attachments', 'thread_id']
```

---

## API Reference

### REST API Endpoints

```python
# FastAPI route definitions

@app.get("/api/emails")
async def list_emails(
    page: int = 1,
    per_page: int = 20,
    sort: str = "date",
    order: str = "desc"
) -> EmailListResponse:
    """List emails with pagination."""

@app.get("/api/emails/{message_id}")
async def get_email(message_id: str) -> EmailResponse:
    """Get single email by message ID."""

@app.get("/api/search")
async def search_emails(
    q: str,
    from_addr: Optional[str] = None,
    to_addr: Optional[str] = None,
    after: Optional[datetime] = None,
    before: Optional[datetime] = None,
    has_attachment: Optional[bool] = None,
    limit: int = 100
) -> SearchResponse:
    """Full-text search with filters."""

@app.post("/api/parse")
async def parse_mbox(
    file: UploadFile,
    background: bool = False
) -> ParseResponse:
    """Upload and parse mbox file."""

@app.get("/api/stats")
async def get_statistics() -> StatsResponse:
    """Get email statistics and analytics."""

@app.ws("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates during parsing."""
```

### WebSocket Protocol

```javascript
// WebSocket client example
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'parse_progress':
            updateProgressBar(data.progress, data.total);
            break;
        case 'parse_complete':
            showSuccess(data.emails_parsed);
            break;
        case 'error':
            showError(data.message);
            break;
    }
};

// Send commands
ws.send(JSON.stringify({
    command: 'start_parse',
    file_path: '/path/to/mbox'
}));
```

### Python SDK

```python
# Client library usage
from mail_parser import MailParserClient

# Initialize client
client = MailParserClient(
    base_url="http://localhost:8080",
    api_key="optional-api-key"
)

# Parse mbox file
result = client.parse_mbox("/path/to/emails.mbox")
print(f"Parsed {result.email_count} emails in {result.duration}s")

# Search emails
results = client.search(
    query="invoice",
    from_addr="accounting@company.com",
    after=datetime(2024, 1, 1)
)

for email in results:
    print(f"{email.subject} - {email.from_addr}")

# Stream emails for processing
for email in client.stream_emails():
    if "important" in email.subject.lower():
        process_important_email(email)
```

---

## Database Schema

### Core Tables

```sql
-- Main emails table
CREATE TABLE emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT UNIQUE NOT NULL,
    thread_id TEXT,
    subject TEXT,
    from_addr TEXT,
    from_name TEXT,
    to_addr TEXT,
    cc_addr TEXT,
    bcc_addr TEXT,
    date DATETIME,
    body TEXT,
    html_body TEXT,
    headers JSON,
    attachments JSON,
    size INTEGER,
    flags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- FTS5 virtual table for search
CREATE VIRTUAL TABLE emails_fts USING fts5(
    message_id UNINDEXED,
    subject,
    from_addr,
    to_addr,
    cc_addr,
    body,
    tokenize = 'porter unicode61'
);

-- Attachments table
CREATE TABLE attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id INTEGER REFERENCES emails(id),
    filename TEXT,
    content_type TEXT,
    size INTEGER,
    content BLOB,
    checksum TEXT
);

-- Threads table for conversation grouping
CREATE TABLE threads (
    id TEXT PRIMARY KEY,
    subject TEXT,
    participants JSON,
    message_count INTEGER,
    first_date DATETIME,
    last_date DATETIME,
    updated_at DATETIME
);

-- Search history and saved searches
CREATE TABLE searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    filters JSON,
    result_count INTEGER,
    execution_time REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- User tags and labels
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    color TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_tags (
    email_id INTEGER REFERENCES emails(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (email_id, tag_id)
);

-- Performance indices
CREATE INDEX idx_emails_date ON emails(date DESC);
CREATE INDEX idx_emails_from ON emails(from_addr);
CREATE INDEX idx_emails_thread ON emails(thread_id, date);
CREATE INDEX idx_attachments_email ON attachments(email_id);
CREATE INDEX idx_email_tags_email ON email_tags(email_id);
CREATE INDEX idx_email_tags_tag ON email_tags(tag_id);
```

### Database Optimization

```sql
-- Analyze and optimize periodically
ANALYZE;
VACUUM;

-- FTS5 optimization
INSERT INTO emails_fts(emails_fts) VALUES('optimize');

-- Query optimization hints
EXPLAIN QUERY PLAN
SELECT * FROM emails e
JOIN emails_fts f ON e.message_id = f.message_id
WHERE f.emails_fts MATCH 'invoice'
ORDER BY e.date DESC
LIMIT 100;
```

---

## Testing Framework

### Test Structure

```python
# tests/test_parser.py
import pytest
from mail_parser import EmailParser

class TestEmailParser:
    @pytest.fixture
    def parser(self):
        return EmailParser(use_rust=True)
    
    @pytest.fixture
    def sample_mbox(self, tmp_path):
        """Create sample mbox for testing."""
        mbox_file = tmp_path / "test.mbox"
        mbox_file.write_text(SAMPLE_MBOX_DATA)
        return str(mbox_file)
    
    def test_parse_single_email(self, parser, sample_mbox):
        emails = parser.parse_mbox(sample_mbox)
        assert len(emails) == 1
        assert emails[0].subject == "Test Email"
    
    @pytest.mark.benchmark
    def test_parse_performance(self, parser, large_mbox, benchmark):
        """Benchmark parsing performance."""
        result = benchmark(parser.parse_mbox, large_mbox)
        assert len(result) > 1000
        assert benchmark.stats['mean'] < 1.0  # Should parse in < 1 second
    
    @pytest.mark.asyncio
    async def test_async_parsing(self, parser, sample_mbox):
        """Test async parsing capabilities."""
        emails = await parser.parse_async(sample_mbox)
        assert len(emails) > 0
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from mail_parser.api.main import app

class TestAPI:
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_search_endpoint(self, client, populated_db):
        response = client.get("/api/search?q=invoice")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0
    
    def test_parse_upload(self, client, sample_mbox_file):
        with open(sample_mbox_file, "rb") as f:
            response = client.post(
                "/api/parse",
                files={"file": f}
            )
        assert response.status_code == 200
        assert response.json()["status"] == "success"
```

### Benchmarking

```python
# benchmarks/run_benchmarks.py
import time
from mail_parser import EmailParser

def benchmark_parsing():
    """Benchmark email parsing performance."""
    parser = EmailParser(use_rust=True)
    
    # Test different file sizes
    for size in ['small', 'medium', 'large']:
        mbox_path = f"benchmarks/data/{size}.mbox"
        
        start = time.perf_counter()
        emails = parser.parse_mbox(mbox_path)
        duration = time.perf_counter() - start
        
        emails_per_sec = len(emails) / duration
        print(f"{size}: {emails_per_sec:.0f} emails/sec")

def benchmark_search():
    """Benchmark search performance."""
    # ... search benchmarks
```

---

## Contributing Guidelines

### Development Process

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/mail_parser.git
   cd mail_parser
   git remote add upstream https://github.com/auricleinc/mail_parser.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write code following style guides
   - Add tests for new functionality
   - Update documentation

4. **Run Tests**
   ```bash
   make test
   make lint
   ```

5. **Submit Pull Request**
   - Clear description of changes
   - Reference any related issues
   - Ensure CI passes

### Code Style

#### Python Style
```python
# Follow PEP 8 with these additions:
# - Line length: 88 characters (Black default)
# - Use type hints for all functions
# - Docstrings for all public APIs

from typing import List, Optional

def parse_email(content: str, strict: bool = False) -> Optional[Email]:
    """Parse email content into Email object.
    
    Args:
        content: Raw email content as string
        strict: Whether to raise on parsing errors
        
    Returns:
        Parsed Email object or None if parsing fails
        
    Raises:
        ParseError: If strict=True and parsing fails
    """
```

#### Rust Style
```rust
// Follow Rust style guide with:
// - Use clippy for linting
// - Document all public items
// - Prefer iterators over loops

/// Parse email headers from raw bytes.
///
/// # Arguments
/// * `data` - Raw email data as bytes
///
/// # Returns
/// Parsed headers as HashMap
///
/// # Example
/// ```
/// let headers = parse_headers(b"From: test@example.com\r\n");
/// ```
pub fn parse_headers(data: &[u8]) -> HashMap<String, String> {
    // Implementation
}
```

### Testing Requirements

- Minimum 80% code coverage
- All new features must have tests
- Performance benchmarks for optimization PRs
- Integration tests for API changes

---

## Security Architecture

### Security Measures

1. **Input Validation**
   ```python
   # Validate all user inputs
   def validate_mbox_file(file_path: str):
       # Check file exists and is readable
       if not os.path.exists(file_path):
           raise ValueError("File not found")
       
       # Check file size limits
       if os.path.getsize(file_path) > MAX_FILE_SIZE:
           raise ValueError("File too large")
       
       # Verify mbox format
       with open(file_path, 'rb') as f:
           magic = f.read(5)
           if magic != b'From ':
               raise ValueError("Invalid mbox format")
   ```

2. **SQL Injection Prevention**
   ```python
   # Always use parameterized queries
   def search_emails(query: str):
       # Safe: uses parameter binding
       cursor.execute(
           "SELECT * FROM emails WHERE body MATCH ?",
           (query,)
       )
       
       # Never: string concatenation
       # cursor.execute(f"SELECT * FROM emails WHERE body MATCH '{query}'")
   ```

3. **Rate Limiting**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.get("/api/search")
   @limiter.limit("100/minute")
   async def search_emails(q: str):
       # Rate limited to 100 requests per minute
   ```

4. **Authentication (Optional)**
   ```python
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   @app.get("/api/emails")
   async def list_emails(credentials: HTTPAuthorizationCredentials = Depends(security)):
       # Verify token
       if not verify_token(credentials.credentials):
           raise HTTPException(status_code=401)
   ```

---

## Monitoring and Observability

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
parse_counter = Counter('emails_parsed_total', 'Total emails parsed')
search_duration = Histogram('search_duration_seconds', 'Search duration')
active_sessions = Gauge('active_sessions', 'Number of active sessions')

# Instrument code
@track_metrics
async def search_emails(query: str):
    with search_duration.time():
        results = await db.search(query)
    return results
```

### Logging

```python
import structlog

logger = structlog.get_logger()

# Structured logging with context
logger.info(
    "email_parsed",
    message_id=email.message_id,
    size=len(email.body),
    attachments=len(email.attachments),
    parse_time=duration
)

# Log aggregation queries
SELECT 
    COUNT(*) as total_parsed,
    AVG(parse_time) as avg_time,
    MAX(parse_time) as max_time
FROM logs
WHERE event = 'email_parsed'
AND timestamp > NOW() - INTERVAL '1 hour';
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    checks = {
        "database": check_database_connection(),
        "disk_space": check_disk_space(),
        "memory": check_memory_usage(),
        "rust_extension": check_rust_extension(),
    }
    
    status = "healthy" if all(checks.values()) else "unhealthy"
    return {
        "status": status,
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }
```

---

## Troubleshooting Guide

### Common Issues

#### High Memory Usage
```python
# Problem: Memory grows unbounded during parsing
# Solution: Use streaming parser
parser = EmailParser(streaming=True, batch_size=100)
for batch in parser.parse_mbox_batches(file_path):
    process_batch(batch)
    gc.collect()  # Force garbage collection between batches
```

#### Slow Search Performance
```sql
-- Problem: FTS5 queries are slow
-- Solution: Optimize FTS5 table
INSERT INTO emails_fts(emails_fts) VALUES('optimize');

-- Rebuild FTS index if corrupted
INSERT INTO emails_fts(emails_fts) VALUES('rebuild');

-- Check query plan
EXPLAIN QUERY PLAN SELECT * FROM emails_fts WHERE emails_fts MATCH 'query';
```

#### Parsing Failures
```python
# Problem: Some emails fail to parse
# Solution: Use error recovery mode
parser = EmailParser(
    strict=False,  # Don't fail on errors
    error_handler=log_error,  # Log errors for analysis
    encoding_fallback=['utf-8', 'latin-1', 'cp1252']  # Try multiple encodings
)
```

#### Database Lock Errors
```python
# Problem: "database is locked" errors
# Solution: Use WAL mode and connection pooling
conn = sqlite3.connect(
    db_path,
    isolation_level=None,  # Autocommit mode
    check_same_thread=False  # Allow multi-threading
)
conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
conn.execute("PRAGMA busy_timeout=5000")  # 5 second timeout
```

---

## Performance Tuning

### System-Level Tuning

```bash
# Linux kernel parameters for better performance
sudo sysctl -w vm.dirty_ratio=80
sudo sysctl -w vm.dirty_background_ratio=50
sudo sysctl -w vm.swappiness=10

# Increase file descriptor limits
ulimit -n 65536

# CPU governor for consistent performance
sudo cpupower frequency-set -g performance
```

### Database Tuning

```sql
-- SQLite performance settings
PRAGMA page_size = 32768;          -- Larger pages for better I/O
PRAGMA cache_size = -64000;         -- 64MB cache
PRAGMA temp_store = MEMORY;         -- Use RAM for temp tables
PRAGMA mmap_size = 30000000000;     -- 30GB memory-mapped I/O
PRAGMA synchronous = NORMAL;        -- Faster writes
PRAGMA journal_mode = WAL;          -- Write-ahead logging
PRAGMA wal_autocheckpoint = 10000;  -- Less frequent checkpoints
```

### Python Optimization

```python
# Use PyPy for 2-5x speedup (pure Python code)
# Install: pypy3 -m pip install -r requirements.txt

# Profile-guided optimization
import cProfile
import pstats

def profile_code():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run your code
    parse_large_mbox()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 time consumers
```

### Rust Optimization

```toml
# Cargo.toml optimization settings
[profile.release]
opt-level = 3          # Maximum optimization
lto = true            # Link-time optimization
codegen-units = 1     # Single codegen unit
panic = "abort"       # Smaller binary
strip = true          # Strip symbols

[dependencies]
rayon = "1.7"         # Parallel processing
mimalloc = "0.1"      # Fast allocator
ahash = "0.8"         # Faster HashMap
```

---

## Development Quick Reference

### Essential Commands

```bash
# Development
make dev                    # Start dev server with hot reload
make test                   # Run all tests
make bench                  # Run benchmarks
make lint                   # Lint Python and Rust code
make format                 # Auto-format code
make clean                  # Clean build artifacts

# Database
sqlite3 emails.db ".schema"              # Show schema
sqlite3 emails.db "VACUUM"               # Optimize database
sqlite3 emails.db ".backup backup.db"    # Backup database

# Debugging
python -m pdb mail_parser/parser.py      # Python debugger
RUST_BACKTRACE=1 cargo run              # Rust stack traces
python -m cProfile -s cumtime script.py  # Profile Python
cargo flamegraph                        # Profile Rust

# Git workflow
git checkout -b feature/my-feature       # Create feature branch
git commit -am "feat: add new feature"   # Conventional commit
git push origin feature/my-feature       # Push branch
gh pr create                             # Create PR with GitHub CLI
```

### Configuration Files

```yaml
# config.yaml - Application configuration
database:
  path: "./emails.db"
  pool_size: 10
  timeout: 5.0

parser:
  use_rust: true
  batch_size: 1000
  max_workers: 8

api:
  host: "0.0.0.0"
  port: 8080
  cors_origins: ["*"]
  rate_limit: 100  # requests per minute

cache:
  size: 10000
  ttl: 3600
```

### Environment Variables

```bash
# .env file
DATABASE_URL=sqlite:///./emails.db
RUST_LOG=debug
PYTHON_LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=10737418240  # 10GB
SECRET_KEY=your-secret-key-here
API_KEY=optional-api-key
WORKERS=4
```

### Quick Debugging

```python
# Debug helpers in mail_parser/debug.py

def inspect_email(email):
    """Pretty-print email for debugging."""
    from pprint import pprint
    import json
    
    print(f"Message ID: {email.message_id}")
    print(f"Subject: {email.subject}")
    print(f"From: {email.from_addr}")
    print(f"Date: {email.date}")
    print(f"Attachments: {len(email.attachments)}")
    print("Headers:")
    pprint(json.loads(email.headers))
    print(f"Body preview: {email.body[:200]}...")

def time_operation(func):
    """Decorator to time operations."""
    import time
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"{func.__name__} took {duration:.3f}s")
        return result
    return wrapper

# Memory profiling
from memory_profiler import profile

@profile
def memory_intensive_operation():
    # Your code here
    pass
```

---

## Appendix

### File Format Specifications

#### MBOX Format
```
From sender@example.com Sat Jan 1 00:00:00 2000
From: sender@example.com
To: recipient@example.com
Subject: Example Email
Date: Sat, 1 Jan 2000 00:00:00 +0000
Message-ID: <unique-id@example.com>

Email body text here...

From sender2@example.com Sun Jan 2 00:00:00 2000
...next email...
```

### Performance Benchmarks Raw Data

```json
{
  "system": {
    "cpu": "Intel i7-9700K @ 3.6GHz",
    "ram": "32GB DDR4",
    "disk": "NVMe SSD",
    "os": "Ubuntu 22.04"
  },
  "benchmarks": {
    "parse_python": {
      "emails_per_second": 1044,
      "memory_usage_mb": 145,
      "cpu_usage_percent": 25
    },
    "parse_rust": {
      "emails_per_second": 52630,
      "memory_usage_mb": 89,
      "cpu_usage_percent": 95
    },
    "search_fts5": {
      "queries_per_second": 120,
      "p50_latency_ms": 8.3,
      "p99_latency_ms": 15.2
    }
  }
}
```

### Version History

- **v2.0.0** - Rust extensions, 50x performance improvement
- **v1.5.0** - Added FTS5 full-text search
- **v1.0.0** - Initial Python implementation
- **v0.9.0** - Beta release with basic parsing

---

*Technical Reference v2.0 - Last updated December 2024*
*For user documentation, see [USER_GUIDE.md](USER_GUIDE.md)*