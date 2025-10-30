// Benchmarks for mail_parser_rust
// Run with: cargo bench

use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};

// Note: These benchmarks test the internal Rust functions
// For end-to-end benchmarks including Python overhead, use pytest-benchmark

fn benchmark_regex_operations(c: &mut Criterion) {
    let text = include_str!("../test_data/sample_email.txt");

    c.bench_function("email_extraction", |b| {
        b.iter(|| {
            let re = regex::Regex::new(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}").unwrap();
            re.find_iter(black_box(text)).count()
        });
    });

    c.bench_function("url_extraction", |b| {
        b.iter(|| {
            let re = regex::Regex::new(r#"https?://[^\s<>"{}|\\^`\[\]]+"#).unwrap();
            re.find_iter(black_box(text)).count()
        });
    });
}

fn benchmark_encoding_detection(c: &mut Criterion) {
    let samples = vec![
        ("ascii", b"Hello, World!"),
        ("utf8", "Hello, 世界! 你好".as_bytes()),
        ("mixed", "Contact: test@example.com with UTF-8: 日本語".as_bytes()),
    ];

    let mut group = c.benchmark_group("encoding_detection");

    for (name, data) in samples.iter() {
        group.bench_with_input(BenchmarkId::from_parameter(name), data, |b, data| {
            b.iter(|| {
                // ASCII fast path check
                if data.iter().all(|&b| b < 128) {
                    return "ASCII";
                }
                // UTF-8 check
                if std::str::from_utf8(data).is_ok() {
                    return "UTF-8";
                }
                "UNKNOWN"
            });
        });
    }
    group.finish();
}

fn benchmark_text_decoding(c: &mut Criterion) {
    use encoding_rs::UTF_8;

    let utf8_text = "Hello, 世界! Test email content with mixed 日本語 characters.".as_bytes();

    c.bench_function("decode_utf8", |b| {
        b.iter(|| {
            let (result, _encoding, _had_errors) = UTF_8.decode(black_box(utf8_text));
            result.to_string()
        });
    });
}

fn benchmark_filename_sanitization(c: &mut Criterion) {
    let filenames = vec![
        "simple.txt",
        "with spaces.txt",
        "special<>chars:?.txt",
        "very_long_filename_that_needs_to_be_truncated_because_it_exceeds_the_255_character_limit_imposed_by_most_filesystems_and_we_need_to_test_that_our_sanitization_function_properly_handles_this_case_without_breaking_or_causing_errors_in_the_file_system.txt",
    ];

    let mut group = c.benchmark_group("filename_sanitization");

    for (idx, filename) in filenames.iter().enumerate() {
        group.bench_with_input(BenchmarkId::from_parameter(idx), filename, |b, filename| {
            b.iter(|| {
                let re = regex::Regex::new(r#"[<>:"/\\|?*\x00-\x1f]"#).unwrap();
                let mut sanitized = re.replace_all(filename, "_").to_string();
                sanitized = sanitized.trim().trim_matches('.').to_string();
                if sanitized.len() > 255 {
                    sanitized.truncate(255);
                }
                sanitized
            });
        });
    }
    group.finish();
}

criterion_group!(
    benches,
    benchmark_regex_operations,
    benchmark_encoding_detection,
    benchmark_text_decoding,
    benchmark_filename_sanitization
);
criterion_main!(benches);
