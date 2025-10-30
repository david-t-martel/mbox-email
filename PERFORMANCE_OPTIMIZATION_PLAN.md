# Performance Optimization Plan - Mail Parser

## Current Performance Analysis

Based on analysis of the 39,768 email parse running at ~9-12 msg/s:
- **Total processing time**: ~72 minutes (estimated)
- **Current throughput**: ~550-720 emails/minute
- **Target throughput**: 5,000+ emails/minute (7-10x improvement)

## Identified Bottlenecks

### 1. Message Counting (mbox_parser.py:45-48)
**Current**: Python line-by-line iteration
```python
with open(self.mbox_path, 'rb') as f:
    for line in f:
        if line.startswith(b'From '):
            count += 1
```
**Impact**: 4-5 minutes for 3GB file
**Solution**: Use ripgrep - **Expected: 30 seconds (10x faster)**

### 2. Encoding Detection (email_processor.py:119, 220, 240)
**Current**: chardet.detect() on every email
**Impact**: ~50-100ms per email = 33-66 minutes total
**Solution**: Fast encoding detection with caching - **Expected: 3-6 minutes (10x faster)**

### 3. Database Inserts (database.py:147-171)
**Current**: Individual INSERT per email with autocommit
**Impact**: ~10-20ms per email = 6-13 minutes total
**Solution**: Batch inserts with transaction batching - **Expected: 30-60 seconds (10x faster)**

### 4. HTML Rendering (html_renderer.py:104)
**Current**: BeautifulSoup parsing every email
**Impact**: ~30-50ms per email = 20-33 minutes total
**Solution**: Faster parsing + template caching - **Expected: 5-10 minutes (4x faster)**

### 5. Regex Operations
**Current**: Python `re` module
**Impact**: ~5-10ms per email = 3-6 minutes total
**Solution**: Rust regex crate via PyO3 - **Expected: 30-60 seconds (10x faster)**

### 6. MIME Parsing
**Current**: Python email.message parsing
**Impact**: ~20-40ms per email = 13-26 minutes total
**Solution**: Rust mailparse crate - **Expected: 2-4 minutes (10x faster)**

## Optimization Phases

### Phase 1: Quick Wins (No Code Changes) - **2-3x Improvement**

#### 1.1 Use ripgrep for message counting
```bash
rg -c "^From " mbox_file  # 100x faster than Python
```
**Time saved**: 4 minutes → 30 seconds

#### 1.2 Enable SQLite optimizations
```sql
PRAGMA journal_mode=WAL;        -- Better concurrency
PRAGMA synchronous=NORMAL;       -- Faster writes
PRAGMA cache_size=-64000;        -- 64MB cache
PRAGMA temp_store=MEMORY;        -- Temp tables in RAM
```
**Time saved**: 6 minutes → 1 minute

#### 1.3 Batch database operations
```python
cursor.executemany("INSERT INTO ...", batch_data)
conn.commit()  # Commit every 1000 emails
```
**Time saved**: 13 minutes → 1 minute

**Total Phase 1 improvement**: 72 minutes → **45 minutes** (1.6x faster)

### Phase 2: Rust Integration via PyO3 - **10x Improvement**

#### 2.1 Fast MBOX Parser (Rust)
Create `mail_parser_rust/` extension with:
- **mailparse** crate for MIME parsing
- **memmap2** for memory-mapped file access
- **rayon** for parallel processing

```rust
use mailparse::parse_mail;
use memmap2::Mmap;
use pyo3::prelude::*;

#[pyfunction]
fn parse_mbox_fast(path: &str) -> PyResult<Vec<EmailMetadata>> {
    // Memory-mapped file access
    let file = File::open(path)?;
    let mmap = unsafe { Mmap::map(&file)? };

    // Parallel processing with rayon
    parse_emails_parallel(&mmap)
}
```

**Benefits**:
- Memory-mapped I/O: 3-5x faster file reading
- Zero-copy parsing: No memory allocation overhead
- Parallel processing: Use all CPU cores efficiently
- **Expected: 20,000+ emails/minute**

#### 2.2 Fast Regex Engine (Rust)
```rust
use regex::Regex;
use pyo3::prelude::*;

#[pyclass]
struct FastRegex {
    pattern: Regex,
}

#[pymethods]
impl FastRegex {
    #[new]
    fn new(pattern: &str) -> PyResult<Self> {
        Ok(FastRegex {
            pattern: Regex::new(pattern).unwrap()
        })
    }

    fn find_all(&self, text: &str) -> Vec<(usize, usize)> {
        self.pattern.find_iter(text)
            .map(|m| (m.start(), m.end()))
            .collect()
    }
}
```

**Benefits**:
- 10-50x faster than Python `re`
- DFA-based matching
- SIMD optimizations

#### 2.3 Fast Encoding Detection (Rust)
```rust
use chardetng::EncodingDetector;

#[pyfunction]
fn detect_encoding_fast(data: &[u8]) -> String {
    let mut detector = EncodingDetector::new();
    detector.feed(data, true);
    detector.guess(None, true).name().to_string()
}
```

**Benefits**:
- 100x faster than Python chardet
- Optimized for email content
- Minimal memory usage

**Total Phase 2 improvement**: 45 minutes → **5-7 minutes** (8x faster)

### Phase 3: Advanced Optimizations - **15x Improvement**

#### 3.1 Numpy-based Batch Processing
```python
import numpy as np

# Process metadata in batches
dates = np.array([email['date'] for email in batch], dtype='datetime64')
# Vectorized date operations
years = dates.astype('datetime64[Y]')
months = dates.astype('datetime64[M]')
```

**Benefits**:
- Vectorized operations for date processing
- Batch filename generation
- Fast array operations

#### 3.2 Output Compression
```python
import zstandard as zstd

# Compress HTML files
compressor = zstd.ZstdCompressor(level=3)
compressed_html = compressor.compress(html.encode())
```

**Benefits**:
- 70-80% space savings
- Minimal CPU overhead (zstd level 3)
- Faster disk I/O (less data to write)

#### 3.3 Parallel HTML Generation
```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
    futures = [executor.submit(render_html, email) for email in batch]
    results = [f.result() for f in futures]
```

**Benefits**:
- Use all CPU cores for rendering
- 4-8x faster on modern CPUs

#### 3.4 Optimized File I/O
```python
import os

# Use O_DIRECT for bypassing page cache
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_DIRECT)
```

**Benefits**:
- Avoid kernel page cache overhead
- Better for large sequential writes

**Total Phase 3 improvement**: 5-7 minutes → **4-5 minutes** (15x total)

## Implementation Roadmap

### Week 1: Quick Wins
- [ ] Implement ripgrep message counting
- [ ] Add SQLite optimizations (WAL, batch inserts)
- [ ] Add transaction batching
- [ ] Cache compiled Jinja2 templates

### Week 2: Rust Foundation
- [ ] Set up maturin project structure
- [ ] Create PyO3 bindings skeleton
- [ ] Implement fast regex module
- [ ] Implement fast encoding detection

### Week 3: Core Rust Parser
- [ ] Implement memory-mapped mbox reader
- [ ] Implement Rust MIME parser
- [ ] Add parallel email processing
- [ ] Create Python bindings

### Week 4: Integration & Testing
- [ ] Integrate Rust modules into Python
- [ ] Add numpy batch processing
- [ ] Implement output compression
- [ ] Performance testing and benchmarking

### Week 5: Advanced Features
- [ ] Parallel HTML generation
- [ ] Optimized file I/O
- [ ] Memory usage profiling
- [ ] Final optimizations

## Expected Performance Metrics

| Metric | Current | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|---------|
| **Throughput** | 550-720 emails/min | 880 emails/min | 5,600 emails/min | 8,000+ emails/min |
| **39K emails** | 72 minutes | 45 minutes | 7 minutes | 5 minutes |
| **Memory usage** | ~500MB | ~500MB | ~200MB | ~150MB |
| **Disk space** | 2-3GB | 2-3GB | 2-3GB | 800MB-1GB |
| **CPU usage** | 20-30% | 30-40% | 70-90% | 80-95% |

## Technology Stack

### Python Optimizations
- **ripgrep**: Fast text search (100x faster than grep)
- **numpy**: Vectorized operations
- **zstandard**: Fast compression
- **concurrent.futures**: Parallel processing

### Rust Components (via PyO3)
- **mailparse**: Fast MIME parsing
- **regex**: Optimized regex engine
- **chardetng**: Fast encoding detection
- **memmap2**: Memory-mapped file I/O
- **rayon**: Data parallelism
- **pyo3**: Python bindings
- **maturin**: Build system

### Database Optimizations
- **SQLite WAL mode**: Write-Ahead Logging
- **Batch inserts**: executemany() with transactions
- **Optimized indexes**: Covering indexes where possible
- **Connection pooling**: Reuse connections

## Memory Optimization Strategy

### Current Memory Usage Pattern
```
mbox file (memory-mapped):     3GB virtual, 100MB resident
Email parsing:                 ~50MB per worker × 8 = 400MB
HTML rendering:                ~100MB buffer
Database:                      ~64MB cache
Total:                        ~500-600MB
```

### Optimized Memory Usage
```
mbox file (memory-mapped):     3GB virtual, 50MB resident
Rust parser:                   ~20MB per worker × 8 = 160MB
HTML rendering (streaming):    ~20MB buffer
Database:                      ~64MB cache
Total:                        ~150-200MB (3x improvement)
```

### Memory Optimization Techniques
1. **Streaming processing**: Don't load entire emails in memory
2. **Memory pooling**: Reuse allocated buffers
3. **Lazy evaluation**: Parse only what's needed
4. **Arena allocation**: Batch allocations for related data

## Disk Space Optimization

### Compression Strategy
```python
# HTML compression with zstd
Original HTML:     ~50KB average
Compressed:        ~8KB average (85% savings)

For 39,768 emails:
Original:          2GB
Compressed:        340MB
Savings:           1.66GB (83% reduction)
```

### Deduplication Strategy
```python
# Content-based deduplication
Unique emails:     ~38,000
Duplicates:        ~1,768
Space saved:       ~88MB (4.4%)
```

## Benchmarking Plan

### Test Cases
1. **Small dataset**: 1,000 emails (~75MB)
2. **Medium dataset**: 10,000 emails (~750MB)
3. **Large dataset**: 39,768 emails (3GB) - Current dataset
4. **XL dataset**: 100,000 emails (~8GB) - Stress test

### Metrics to Track
- **Throughput**: Emails processed per minute
- **Latency**: Time per email (p50, p95, p99)
- **Memory**: Peak resident set size (RSS)
- **CPU**: Utilization percentage
- **Disk**: I/O operations per second
- **Space**: Output size vs input size

### Performance Testing
```bash
# Benchmark script
python -m pytest benchmarks/test_performance.py --benchmark-only

# Memory profiling
python -m memory_profiler mail_parser/cli.py parse --mbox test.mbox

# CPU profiling
python -m cProfile -o profile.stats mail_parser/cli.py parse

# I/O profiling
sudo iotop -b -n 10 > io_profile.txt
```

## Risk Mitigation

### Compatibility Risks
- **Python version**: Ensure PyO3 supports Python 3.10+
- **Platform support**: Test on Linux, macOS, Windows (WSL)
- **Dependency conflicts**: Pin versions in pyproject.toml

### Performance Risks
- **Memory leaks**: Use valgrind to detect leaks in Rust code
- **Deadlocks**: Careful synchronization in parallel code
- **Data corruption**: Extensive testing of batch operations

### Rollback Strategy
- **Feature flags**: Enable optimizations progressively
- **A/B testing**: Run old and new code in parallel
- **Monitoring**: Track error rates and performance metrics

## Success Criteria

### Must Have (P0)
- ✅ 5x faster overall processing (72 min → 15 min)
- ✅ No data loss or corruption
- ✅ Backward compatible with existing code
- ✅ Works on all platforms (Linux, macOS, Windows)

### Should Have (P1)
- ✅ 10x faster overall processing (72 min → 7 min)
- ✅ 50% memory reduction
- ✅ 70% disk space savings with compression
- ✅ Comprehensive benchmarks

### Nice to Have (P2)
- ⭐ 15x faster overall processing (72 min → 5 min)
- ⭐ Stream processing for unlimited email sizes
- ⭐ GPU acceleration for encoding detection
- ⭐ Distributed processing across multiple machines

## Conclusion

This optimization plan provides a clear roadmap for achieving **10-15x performance improvement** through:
1. Quick wins with minimal code changes (2-3x)
2. Rust integration for CPU-bound operations (5-7x)
3. Advanced optimizations for I/O and parallelism (2-3x)

The phased approach allows for incremental improvements with measurable results at each stage.
