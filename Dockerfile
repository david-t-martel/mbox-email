# Mail Parser - Production Dockerfile
# Multi-stage build for optimized image size

# Stage 1: Builder
FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -fsSL https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml requirements.txt ./
COPY mail_parser ./mail_parser/
COPY README.md LICENSE ./

# Install dependencies
RUN uv pip install --system -e .

# Stage 2: Runtime
FROM python:3.12-slim

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 mailparser && \
    mkdir -p /data /output && \
    chown -R mailparser:mailparser /data /output

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
COPY --from=builder --chown=mailparser:mailparser /app /app

WORKDIR /app

# Switch to non-root user
USER mailparser

# Volumes for data
VOLUME ["/data", "/output"]

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OUTPUT_DIR=/output

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import mail_parser; print('OK')" || exit 1

# Default command shows help
CMD ["python", "-m", "mail_parser.cli", "--help"]

# Labels
LABEL maintainer="David T. Martel <david.martel@auricleinc.com>" \
      version="1.0.0" \
      description="High-performance Gmail mbox parser and analyzer" \
      org.opencontainers.image.source="https://github.com/david-t-martel/mbox-email" \
      org.opencontainers.image.licenses="MIT"
