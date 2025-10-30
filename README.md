# Mail Parser - High-Performance Gmail mbox Parser & Analyzer

A feature-rich, high-performance email analysis system that parses Gmail mbox files (like Google Takeout exports) with multi-dimensional organization, interactive web dashboard, and comprehensive analytics.

## 🎯 Key Features

### ✨ NEW: Human-Readable Filenames
Emails are saved with descriptive, sortable filenames that include:
- **Date & Time**: `20251028_1444_` for easy chronological sorting
- **Sender Name**: `john_doe_` for quick sender identification
- **Subject**: `meeting_notes_` for content preview
- **Index**: `_000123` for uniqueness

**Example**: `20251028_1444_john_doe_meeting_notes_about_project_000123.html`

### 🌐 NEW: Interactive Web Dashboard
Beautiful, responsive web interface (`index.html`) with:
- 🔍 **Real-time search** across all emails
- 🎯 **Advanced filtering** by domain, label, attachments
- 📊 **Live statistics** and email counts
- 📱 **Mobile-friendly** responsive design
- ⚡ **Fast pagination** for thousands of emails
- 🔄 **Three viewing modes**: By Date, By Sender, By Thread
- 📈 **Sortable columns** for all fields

### 🖥️ Cross-Platform Compatible
- ✅ **Windows** (WSL, native paths)
- ✅ **macOS** (Unix paths)
- ✅ **Linux** (all distributions)
- Uses `pathlib` for universal path handling
- Sanitizes filenames for all operating systems

### Core Features
- **High-performance streaming parser** - Processes 39K+ emails without loading entire file into memory
- **Multi-dimensional organization** - Organize by date, sender domain, and email thread simultaneously
- **Full HTML rendering** - Beautiful HTML emails with embedded images and styling
- **Gmail API integration** - OAuth 2.0 authentication for metadata enhancement (optional)
- **Comprehensive analytics** - Email volume, sender statistics, attachment analysis
- **Duplicate detection** - Identify and track duplicate emails
- **Full-text search** - SQLite FTS5 for fast searching across all emails

## Installation

### Prerequisites
- Python 3.10+
- UV package manager (recommended) or pip

### Setup

```bash
cd /mnt/c/codedev/auricleinc/mail_analysis/mail/mail_parser

# Install dependencies
uv pip install -e .

# Or using pip
pip install -e .
```

## Quick Start

### 1. Parse Your mbox File

```bash
uv run python -m mail_parser.cli parse \
  --mbox /path/to/your/mailbox.mbox \
  --output ./my_emails \
  --workers 8
```

### 2. Open the Interactive Dashboard

```bash
# Open in your web browser
open ./my_emails/index.html  # macOS
# or
start ./my_emails/index.html  # Windows
# or
xdg-open ./my_emails/index.html  # Linux
```

### 3. Browse Your Emails

The dashboard provides:
- **Search bar**: Type to search across subjects, senders, content
- **Filters**: Filter by domain, Gmail labels, or attachments
- **View modes**: Switch between Date, Sender, or Thread organization
- **Sortable table**: Click column headers to sort
- **Pagination**: Navigate through thousands of emails easily

## Usage Examples

### Test Run (First 100 Emails)

```bash
uv run python -m mail_parser.cli parse \
  --mbox your_file.mbox \
  --output ./test_output \
  --limit 100
```

### Full Processing

```bash
uv run python -m mail_parser.cli parse \
  --mbox david-martel.mbox \
  --output ./mail_archive \
  --workers 8
```

### Search Emails (Command Line)

```bash
uv run python -m mail_parser.cli search \
  --database ./mail_archive/email_index.db \
  --query "tinnitus trial" \
  --limit 50
```

### View Statistics

```bash
uv run python -m mail_parser.cli stats \
  --database ./mail_archive/email_index.db
```

### Gmail API Setup (Optional)

```bash
# 1. Get OAuth credentials from Google Cloud Console
# 2. Save as ./credentials/credentials.json

# 3. Authenticate
uv run python -m mail_parser.cli init

# 4. Parse with API enhancement
uv run python -m mail_parser.cli parse \
  --mbox your_file.mbox \
  --enable-gmail-api \
  --output ./output
```

## Output Structure

```
output/
├── index.html                       # 🌐 Interactive web dashboard (OPEN THIS!)
├── email_data.json                  # Email index for dashboard
├── analytics_report.html            # 📊 Analytics dashboard
├── email_index.db                   # 🔍 Search database
├── by-date/
│   └── 2025/
│       └── 10/
│           └── 28/
│               ├── 20251028_1444_john_doe_meeting_notes_000001.html
│               └── 20251028_1530_jane_smith_project_update_000002.html
├── by-sender/
│   ├── auricleinc.com/
│   │   └── 20251028_1444_david_martel_weekly_report_000003.html
│   └── umich.edu/
│       └── 20251028_0900_professor_jones_class_canceled_000004.html
└── by-thread/
    ├── thread_1847237176990937209/
    │   ├── pos001_20251028_1444_john_doe_meeting_notes_000001.html
    │   └── pos002_20251028_1500_jane_smith_re_meeting_notes_000002.html
    └── thread_1847237176990937210/
        └── pos001_20251029_0900_bob_johnson_hello_everyone_000003.html
```

## Dashboard Features

### Main Dashboard (`index.html`)

**Search & Filter:**
- Real-time search as you type
- Filter by sender domain (e.g., "umich.edu", "auricleinc.com")
- Filter by Gmail labels
- Filter by attachment status
- Combine multiple filters

**View Modes:**
- 📅 **By Date**: Browse emails chronologically
- 👤 **By Sender**: Group by sender's domain
- 💬 **By Thread**: See conversation threads

**Interactive Table:**
- Click column headers to sort (Date, Sender, Subject, Labels)
- Pagination for large email sets (50 per page)
- Direct links to open emails in new tabs
- Shows attachment indicators 📎
- Displays Gmail label badges

**Statistics Panel:**
- Total email count
- Unique threads
- Number of domains
- Emails with attachments

### Analytics Dashboard (`analytics_report.html`)

Interactive Plotly charts showing:
- Email volume over time (line chart)
- Hourly distribution (bar chart)
- Top 10 senders (horizontal bar)
- Top 10 domains
- Top 10 Gmail labels
- Day of week analysis
- Comprehensive summary statistics

## File Naming Scheme

**Format**: `YYYYMMDD_HHMM_sender_subject_index.html`

**Components**:
- `YYYYMMDD_HHMM`: Date and time for chronological sorting
- `sender`: Sender's name or email username (sanitized)
- `subject`: Email subject (truncated to 40 chars, sanitized)
- `index`: 6-digit unique index number

**Thread Files**: `pos###_YYYYMMDD_HHMM_sender_subject_index.html`
- `pos###`: Position in thread (001, 002, etc.)

**Benefits**:
- ✅ Alphabetically sortable by date/time
- ✅ Quickly find emails by sender
- ✅ Preview subject without opening
- ✅ Works on Windows, macOS, and Linux
- ✅ No special characters that break filesystems

## Configuration

Create `config.yaml`:

```yaml
# Input/Output
output:
  base_dir: "./output"
  organize_by:
    - date
    - sender
    - thread

# Performance
performance:
  workers: 8
  chunk_size: 1000

# Gmail API
gmail_api:
  enabled: false
  credentials_path: "./credentials/credentials.json"
  token_path: "./credentials/token.json"

# Analysis
analysis:
  enable_statistics: true
  enable_duplicate_detection: true

# Indexing
indexing:
  enable_full_text_search: true
  database_path: "./output/email_index.db"
```

## Performance

Tested on 3GB mbox file (39,768 emails):

- **Message counting**: ~4.5 minutes (can be optimized with `rg`)
- **Parsing speed**: ~2,000 emails/minute
- **Memory usage**: <2GB RAM
- **Storage**: ~500MB for 40K HTML files
- **Processing time**: ~20-30 minutes total
- **Dashboard load time**: <2 seconds for 40K emails

## Cross-Platform Notes

### Windows (WSL)
```bash
# Access Windows files
cd /mnt/c/path/to/emails

# Open dashboard in Windows browser
cmd.exe /c start ./output/index.html
```

### macOS
```bash
# Open dashboard in default browser
open ./output/index.html

# Or use specific browser
open -a Safari ./output/index.html
```

### Linux
```bash
# Open with default browser
xdg-open ./output/index.html

# Or use specific browser
firefox ./output/index.html
```

## Troubleshooting

### Dashboard Not Loading

1. Ensure `email_data.json` exists in output directory
2. Check browser console for JavaScript errors
3. Verify all files were generated
4. Try opening `index.html` with different browser

### Gmail API Authentication Fails

1. Ensure credentials.json is valid
2. Check internet connection
3. Enable Gmail API in Google Cloud Console
4. Try: `uv run python -m mail_parser.cli init`

### Out of Memory

Reduce workers:
```bash
uv run python -m mail_parser.cli parse --mbox file.mbox --workers 2
```

### Slow Processing

Increase workers (if you have more CPU cores):
```bash
uv run python -m mail_parser.cli parse --mbox file.mbox --workers 16
```

### Filenames Look Wrong

- Check that filenames are sanitized (no special characters)
- All slashes become underscores
- Maximum length limits applied
- Works on all operating systems

## Development

### Project Structure

```
mail_parser/
├── mail_parser/
│   ├── core/              # Parsing engine
│   │   ├── mbox_parser.py
│   │   ├── email_processor.py
│   │   ├── mime_handler.py
│   │   └── filename_generator.py  # NEW: Human-readable names
│   ├── renderers/         # HTML generation
│   ├── organizers/        # File organization
│   ├── api/               # Gmail API
│   ├── analysis/          # Statistics
│   ├── indexing/          # Database
│   ├── dashboard/         # NEW: Web dashboard
│   │   └── generator.py
│   └── cli.py             # CLI interface
├── config/
├── output/
└── README.md
```

## License

MIT License - see LICENSE file for details

## Credits

Built with:
- Python 3.10+
- Google Gmail API
- SQLite FTS5
- Jinja2, BeautifulSoup4, Plotly
- UV package manager

---

## 🎉 What's New in This Version

✨ **Human-readable filenames** with date, sender, and subject
🌐 **Interactive web dashboard** for browsing emails
🖥️ **Cross-platform compatibility** (Windows, macOS, Linux)
⚡ **Improved performance** and user experience
📱 **Mobile-responsive** dashboard design
🔍 **Advanced filtering** and search capabilities

**Open `index.html` and start exploring your emails!**
