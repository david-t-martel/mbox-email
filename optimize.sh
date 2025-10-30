#!/usr/bin/env bash
#
# Email Parser Optimization Helper Script
# ========================================
#
# This script helps you run performance profiling and benchmarking
# to verify the optimizations described in OPTIMIZATION_SUMMARY.md
#
# Usage:
#   ./optimize.sh profile /path/to/test.mbox 1000
#   ./optimize.sh benchmark /path/to/test.mbox 1000
#   ./optimize.sh index /path/to/large.mbox
#   ./optimize.sh help
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if uv is available
check_uv() {
    if ! command -v uv &> /dev/null; then
        log_error "uv not found. Please install: pip install uv"
        exit 1
    fi
}

# Profile current performance
profile_current() {
    local mbox_path="$1"
    local limit="${2:-1000}"

    log_info "Profiling current performance..."
    log_info "MBOX: $mbox_path"
    log_info "Sample size: $limit emails"

    check_uv

    uv run python profile_performance.py \
        --mbox "$mbox_path" \
        --limit "$limit" \
        --profiler bench \
        --output ./profile_output

    log_success "Profiling complete! Check ./profile_output/ for results"
}

# Benchmark parallel vs sequential
benchmark_parallel() {
    local mbox_path="$1"
    local limit="${2:-1000}"

    log_info "Benchmarking parallel vs sequential processing..."
    log_info "MBOX: $mbox_path"
    log_info "Sample size: $limit emails"
    log_warning "This will take a few minutes..."

    check_uv

    uv run python profile_performance.py \
        --mbox "$mbox_path" \
        --limit "$limit" \
        --benchmark \
        --output ./benchmark_output

    log_success "Benchmark complete! Check output above for speedup results"
}

# Build MBOX index
build_index() {
    local mbox_path="$1"

    log_info "Building MBOX index..."
    log_info "MBOX: $mbox_path"
    log_warning "This is a one-time operation (30-60 seconds for 40K emails)"

    check_uv

    python3 << EOF
import sys
sys.path.insert(0, '.')
from MBOX_INDEXER import MboxIndexer

indexer = MboxIndexer('$mbox_path')
index_path = indexer.build_index()

print(f"\n✅ Index built: {index_path}")

stats = indexer.get_index_statistics()
print(f"""
Index Statistics:
=================
Total emails:     {stats['total_emails']:,}
Total size:       {stats['total_size_mb']:.1f} MB
Avg email size:   {stats['avg_email_size_bytes']:,} bytes
Index file size:  {stats['index_file_size_bytes']:,} bytes
""")
EOF

    log_success "Index built successfully!"
}

# Test index access
test_index() {
    local mbox_path="$1"

    log_info "Testing index-based random access..."

    python3 << EOF
import sys
sys.path.insert(0, '.')
from MBOX_INDEXER import MboxIndexer
import time

indexer = MboxIndexer('$mbox_path')
indexer.load_index()

# Test reading email 100
start = time.time()
message = indexer.read_email_at_index(100)
elapsed = time.time() - start

print(f"\n✅ Read email 100 in {elapsed*1000:.2f}ms")
print(f"   Subject: {message.get('Subject', 'No subject')}")

# Test reading email 10,000
start = time.time()
message = indexer.read_email_at_index(10000)
elapsed = time.time() - start

print(f"\n✅ Read email 10,000 in {elapsed*1000:.2f}ms (no sequential parsing!)")
print(f"   Subject: {message.get('Subject', 'No subject')}")
EOF

    log_success "Index test complete!"
}

# Flamegraph profiling
profile_flamegraph() {
    local mbox_path="$1"
    local limit="${2:-1000}"

    log_info "Generating flamegraph with py-spy..."
    log_warning "This requires py-spy: uv pip install py-spy"

    if ! command -v py-spy &> /dev/null; then
        log_warning "Installing py-spy..."
        uv pip install py-spy
    fi

    uv run python profile_performance.py \
        --mbox "$mbox_path" \
        --limit "$limit" \
        --profiler pyspy \
        --output ./flamegraph_output

    local svg_path="./flamegraph_output/flamegraph.svg"
    if [[ -f "$svg_path" ]]; then
        log_success "Flamegraph generated: $svg_path"
        log_info "Open in browser: file://$(realpath "$svg_path")"
    fi
}

# Show help
show_help() {
    cat << 'EOF'
Email Parser Optimization Helper
=================================

Usage:
  ./optimize.sh <command> <mbox_path> [limit]

Commands:
  profile <mbox> [limit]     - Profile current performance (default: 1000 emails)
  benchmark <mbox> [limit]   - Benchmark parallel vs sequential (default: 1000 emails)
  index <mbox>               - Build MBOX index for fast access
  test-index <mbox>          - Test index-based random access
  flamegraph <mbox> [limit]  - Generate performance flamegraph (requires py-spy)
  help                       - Show this help message

Examples:
  # Profile 1000 emails
  ./optimize.sh profile /path/to/test.mbox 1000

  # Benchmark parallel vs sequential
  ./optimize.sh benchmark /path/to/test.mbox 1000

  # Build index for fast access
  ./optimize.sh index /path/to/large.mbox

  # Test index performance
  ./optimize.sh test-index /path/to/large.mbox

  # Generate flamegraph
  ./optimize.sh flamegraph /path/to/test.mbox 500

Output Locations:
  ./profile_output/       - Profiling results
  ./benchmark_output/     - Benchmark results
  ./flamegraph_output/    - Flamegraph SVG files
  *.mbox.idx             - Index files (same dir as mbox)

Performance Targets:
  Current:     68 minutes for 39,768 emails (~10 emails/sec)
  Target:      5 minutes for 39,768 emails (~132 emails/sec)
  Required:    13.6x speedup

Expected Results After Optimization:
  Phase 1 (Parallel):        9 minutes (7.5x speedup)
  Phase 2 (Hard Links):      6 minutes (11x speedup) ✅ TARGET MET
  Phase 3 (Indexing):        3 minutes (22x speedup)

For detailed optimization guide, see: OPTIMIZATION_SUMMARY.md
EOF
}

# Main script
main() {
    local command="${1:-help}"
    shift || true

    case "$command" in
        profile)
            if [[ $# -lt 1 ]]; then
                log_error "Usage: $0 profile <mbox_path> [limit]"
                exit 1
            fi
            profile_current "$@"
            ;;
        benchmark)
            if [[ $# -lt 1 ]]; then
                log_error "Usage: $0 benchmark <mbox_path> [limit]"
                exit 1
            fi
            benchmark_parallel "$@"
            ;;
        index)
            if [[ $# -lt 1 ]]; then
                log_error "Usage: $0 index <mbox_path>"
                exit 1
            fi
            build_index "$@"
            ;;
        test-index)
            if [[ $# -lt 1 ]]; then
                log_error "Usage: $0 test-index <mbox_path>"
                exit 1
            fi
            test_index "$@"
            ;;
        flamegraph)
            if [[ $# -lt 1 ]]; then
                log_error "Usage: $0 flamegraph <mbox_path> [limit]"
                exit 1
            fi
            profile_flamegraph "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main
main "$@"
