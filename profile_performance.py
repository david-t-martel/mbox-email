#!/usr/bin/env python3
"""
Performance Profiling Script for Email Parser
==============================================

This script profiles the email parser to identify actual bottlenecks.

Usage:
    # Profile with cProfile
    python profile_performance.py --mbox /path/to/test.mbox --limit 1000 --profiler cprofile

    # Profile with py-spy (live flamegraph)
    python profile_performance.py --mbox /path/to/test.mbox --limit 1000 --profiler pyspy

    # Profile with line_profiler (detailed line-by-line)
    python profile_performance.py --mbox /path/to/test.mbox --limit 100 --profiler line

    # Benchmark parallel vs sequential
    python profile_performance.py --mbox /path/to/test.mbox --limit 1000 --benchmark

Requirements:
    pip install py-spy line_profiler memory_profiler
"""

import argparse
import cProfile
import pstats
import time
import sys
from pathlib import Path
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def profile_with_cprofile(mbox_path: str, limit: int, output_dir: str):
    """Profile using cProfile (built-in)."""
    from mail_parser.cli import MailParserCLI

    print("\n" + "="*70)
    print("PROFILING WITH cProfile")
    print("="*70)

    # Create profiler
    profiler = cProfile.Profile()

    # Run with profiling
    profiler.enable()

    app = MailParserCLI()
    app.config['output']['base_dir'] = output_dir
    app.config['performance']['workers'] = 1  # Sequential for clear profiling
    app.initialize_database()
    app.parse_mbox(mbox_path, limit=limit)

    profiler.disable()

    # Save stats
    stats_file = Path(output_dir) / 'profile_stats.prof'
    profiler.dump_stats(str(stats_file))
    print(f"\n✅ Profile saved to: {stats_file}")

    # Print top functions by cumulative time
    print("\n" + "="*70)
    print("TOP 30 FUNCTIONS BY CUMULATIVE TIME")
    print("="*70)

    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats(30)
    print(stream.getvalue())

    # Print top functions by total time
    print("\n" + "="*70)
    print("TOP 30 FUNCTIONS BY TOTAL TIME")
    print("="*70)

    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs()
    stats.sort_stats('tottime')
    stats.print_stats(30)
    print(stream.getvalue())


def profile_with_pyspy(mbox_path: str, limit: int, output_dir: str):
    """Profile using py-spy (requires separate installation)."""
    import subprocess

    print("\n" + "="*70)
    print("PROFILING WITH py-spy")
    print("="*70)

    output_svg = Path(output_dir) / 'flamegraph.svg'

    # Build command
    cmd = [
        'py-spy', 'record',
        '-o', str(output_svg),
        '--', 'python', '-m', 'mail_parser.cli', 'parse',
        '--mbox', mbox_path,
        '--output', output_dir,
        '--limit', str(limit),
        '--workers', '1',
    ]

    print(f"Running: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Flamegraph saved to: {output_svg}")
        print(f"Open in browser: file://{output_svg.absolute()}")
    except FileNotFoundError:
        print("❌ py-spy not found. Install with: pip install py-spy")
    except subprocess.CalledProcessError as e:
        print(f"❌ py-spy failed: {e}")


def profile_with_line_profiler(mbox_path: str, limit: int, output_dir: str):
    """Profile with line_profiler for line-by-line analysis."""
    print("\n" + "="*70)
    print("PROFILING WITH line_profiler")
    print("="*70)

    try:
        from line_profiler import LineProfiler
    except ImportError:
        print("❌ line_profiler not found. Install with: pip install line_profiler")
        return

    from mail_parser.cli import MailParserCLI
    from mail_parser.core.mbox_parser import MboxParser
    from mail_parser.core.email_processor import EmailProcessor
    from mail_parser.renderers.html_renderer import HtmlRenderer

    # Create profiler
    profiler = LineProfiler()

    # Add functions to profile
    profiler.add_function(MailParserCLI.parse_mbox)
    profiler.add_function(MailParserCLI.process_email)
    profiler.add_function(MboxParser.parse_stream)
    profiler.add_function(EmailProcessor.extract_metadata)
    profiler.add_function(EmailProcessor.extract_body)
    profiler.add_function(HtmlRenderer.render_email)

    # Run with profiling
    app = MailParserCLI()
    app.config['output']['base_dir'] = output_dir
    app.config['performance']['workers'] = 1
    app.initialize_database()

    profiler.enable()
    app.parse_mbox(mbox_path, limit=limit)
    profiler.disable()

    # Print results
    profiler.print_stats()


def benchmark_operations(mbox_path: str, limit: int):
    """Benchmark individual operations to identify bottlenecks."""
    from mail_parser.core.mbox_parser import MboxParser
    from mail_parser.core.email_processor import EmailProcessor
    from mail_parser.core.mime_handler import MimeHandler
    from mail_parser.renderers.html_renderer import HtmlRenderer

    print("\n" + "="*70)
    print("BENCHMARKING INDIVIDUAL OPERATIONS")
    print("="*70)

    parser = MboxParser(mbox_path)
    renderer = HtmlRenderer()

    timings = {
        'parse': [],
        'metadata': [],
        'body': [],
        'attachments': [],
        'render': [],
        'total': [],
    }

    print(f"\nProcessing {limit} emails...\n")

    for idx, message in parser.parse_stream(show_progress=True):
        if idx >= limit:
            break

        t_start = time.time()

        # Time metadata extraction
        t0 = time.time()
        metadata = EmailProcessor.extract_metadata(message)
        timings['metadata'].append(time.time() - t0)

        # Time body extraction
        t0 = time.time()
        body = EmailProcessor.extract_body(message)
        timings['body'].append(time.time() - t0)

        # Time attachment extraction
        t0 = time.time()
        attachments = MimeHandler.extract_attachments(message)
        timings['attachments'].append(time.time() - t0)

        # Time HTML rendering
        t0 = time.time()
        html = renderer.render_email(message, metadata, body, attachments)
        timings['render'].append(time.time() - t0)

        timings['total'].append(time.time() - t_start)

    # Calculate statistics
    print("\n" + "="*70)
    print("TIMING BREAKDOWN (Average per email)")
    print("="*70)

    def stats(times):
        if not times:
            return 0, 0, 0
        avg = sum(times) / len(times)
        min_t = min(times)
        max_t = max(times)
        return avg, min_t, max_t

    total_avg = sum(timings['total']) / len(timings['total']) if timings['total'] else 0

    for operation, times in timings.items():
        avg, min_t, max_t = stats(times)
        pct = (avg / total_avg * 100) if total_avg > 0 else 0

        print(f"{operation:15} {avg*1000:7.2f}ms  "
              f"(min: {min_t*1000:6.2f}ms, max: {max_t*1000:6.2f}ms)  "
              f"{pct:5.1f}%")

    print("="*70)

    # Extrapolate to full dataset
    print(f"\n📊 EXTRAPOLATION TO FULL DATASET:")
    full_size = 39768
    estimated_time = total_avg * full_size
    print(f"  Sample size:        {limit:,} emails")
    print(f"  Avg time/email:     {total_avg*1000:.2f}ms")
    print(f"  Full dataset:       {full_size:,} emails")
    print(f"  Estimated time:     {estimated_time:.1f}s ({estimated_time/60:.1f} mins)")
    print(f"  Target:             5 minutes (300s)")
    print(f"  Status:             {'✅ TARGET MET' if estimated_time < 300 else f'❌ NEEDS {estimated_time/300:.1f}x SPEEDUP'}")
    print("="*70)


def benchmark_parallel_vs_sequential(mbox_path: str, limit: int, output_dir: str):
    """Compare sequential vs parallel processing performance."""
    from mail_parser.cli import MailParserCLI

    print("\n" + "="*70)
    print("PARALLEL vs SEQUENTIAL BENCHMARK")
    print("="*70)

    results = {}

    # Test 1: Sequential (1 worker)
    print("\n🔸 Test 1: Sequential Processing (1 worker)")
    print("-" * 70)

    app = MailParserCLI()
    app.config['output']['base_dir'] = f"{output_dir}/sequential"
    app.config['performance']['workers'] = 1
    app.initialize_database()

    start = time.time()
    app.parse_mbox(mbox_path, limit=limit)
    seq_time = time.time() - start

    results['sequential'] = {
        'time': seq_time,
        'throughput': limit / seq_time if seq_time > 0 else 0,
    }

    print(f"✅ Sequential completed in {seq_time:.1f}s ({limit/seq_time:.1f} emails/sec)")

    # Test 2: Parallel (4 workers)
    print("\n🔸 Test 2: Parallel Processing (4 workers)")
    print("-" * 70)

    app = MailParserCLI()
    app.config['output']['base_dir'] = f"{output_dir}/parallel_4"
    app.config['performance']['workers'] = 4
    app.initialize_database()

    start = time.time()
    app.parse_mbox(mbox_path, limit=limit)
    par4_time = time.time() - start

    results['parallel_4'] = {
        'time': par4_time,
        'throughput': limit / par4_time if par4_time > 0 else 0,
    }

    print(f"✅ Parallel (4w) completed in {par4_time:.1f}s ({limit/par4_time:.1f} emails/sec)")

    # Test 3: Parallel (8 workers)
    print("\n🔸 Test 3: Parallel Processing (8 workers)")
    print("-" * 70)

    app = MailParserCLI()
    app.config['output']['base_dir'] = f"{output_dir}/parallel_8"
    app.config['performance']['workers'] = 8
    app.initialize_database()

    start = time.time()
    app.parse_mbox(mbox_path, limit=limit)
    par8_time = time.time() - start

    results['parallel_8'] = {
        'time': par8_time,
        'throughput': limit / par8_time if par8_time > 0 else 0,
    }

    print(f"✅ Parallel (8w) completed in {par8_time:.1f}s ({limit/par8_time:.1f} emails/sec)")

    # Summary
    print("\n" + "="*70)
    print("BENCHMARK SUMMARY")
    print("="*70)

    speedup_4 = seq_time / par4_time if par4_time > 0 else 0
    speedup_8 = seq_time / par8_time if par8_time > 0 else 0
    efficiency_4 = (speedup_4 / 4) * 100
    efficiency_8 = (speedup_8 / 8) * 100

    print(f"\nSample size:           {limit:,} emails")
    print(f"\nSequential (1 worker):")
    print(f"  Time:                {seq_time:.1f}s")
    print(f"  Throughput:          {results['sequential']['throughput']:.1f} emails/sec")

    print(f"\nParallel (4 workers):")
    print(f"  Time:                {par4_time:.1f}s")
    print(f"  Throughput:          {results['parallel_4']['throughput']:.1f} emails/sec")
    print(f"  Speedup:             {speedup_4:.2f}x")
    print(f"  Efficiency:          {efficiency_4:.1f}% (ideal: 100%)")

    print(f"\nParallel (8 workers):")
    print(f"  Time:                {par8_time:.1f}s")
    print(f"  Throughput:          {results['parallel_8']['throughput']:.1f} emails/sec")
    print(f"  Speedup:             {speedup_8:.2f}x")
    print(f"  Efficiency:          {efficiency_8:.1f}% (ideal: 100%)")

    # Extrapolate to full dataset
    full_size = 39768
    full_time_seq = (full_size / limit) * seq_time
    full_time_par8 = (full_size / limit) * par8_time

    print(f"\n🔮 EXTRAPOLATION TO FULL DATASET ({full_size:,} emails):")
    print(f"  Sequential:          {full_time_seq:.1f}s ({full_time_seq/60:.1f} mins)")
    print(f"  Parallel (8w):       {full_time_par8:.1f}s ({full_time_par8/60:.1f} mins)")
    print(f"  Total speedup:       {full_time_seq/full_time_par8:.2f}x")
    print(f"  Target (5 mins):     {'✅ MET' if full_time_par8 < 300 else '❌ NOT MET'}")
    print("="*70)


def main():
    parser = argparse.ArgumentParser(description='Profile email parser performance')
    parser.add_argument('--mbox', required=True, help='Path to mbox file')
    parser.add_argument('--limit', type=int, default=1000, help='Number of emails to process')
    parser.add_argument('--output', default='./profile_output', help='Output directory')
    parser.add_argument('--profiler', choices=['cprofile', 'pyspy', 'line', 'bench'],
                       default='bench', help='Profiler to use')
    parser.add_argument('--benchmark', action='store_true',
                       help='Run parallel vs sequential benchmark')

    args = parser.parse_args()

    # Create output directory
    Path(args.output).mkdir(parents=True, exist_ok=True)

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║        EMAIL PARSER PERFORMANCE PROFILING                     ║
╠══════════════════════════════════════════════════════════════╣
║ MBOX file:        {args.mbox:<45} ║
║ Sample size:      {args.limit:>10,} emails                           ║
║ Output dir:       {args.output:<45} ║
║ Profiler:         {args.profiler:<45} ║
╚══════════════════════════════════════════════════════════════╝
    """)

    if args.benchmark:
        benchmark_parallel_vs_sequential(args.mbox, args.limit, args.output)
    elif args.profiler == 'cprofile':
        profile_with_cprofile(args.mbox, args.limit, args.output)
    elif args.profiler == 'pyspy':
        profile_with_pyspy(args.mbox, args.limit, args.output)
    elif args.profiler == 'line':
        profile_with_line_profiler(args.mbox, args.limit, args.output)
    elif args.profiler == 'bench':
        benchmark_operations(args.mbox, args.limit)


if __name__ == '__main__':
    main()
