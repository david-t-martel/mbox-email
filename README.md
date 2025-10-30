# 📧 Gmail Parser

**Search years of emails in milliseconds.** Gmail Parser transforms your email archive into a lightning-fast searchable database that works right in your web browser.

---

## What Is Gmail Parser?

Gmail Parser is a tool that reads your Gmail backup files and makes them instantly searchable. No more digging through thousands of emails to find that one important message - just type what you're looking for and find it immediately.

### ✨ Key Features

- **⚡ Lightning Fast** - Search 17,000+ emails in under 10 milliseconds
- **🔍 Powerful Search** - Find anything: words, phrases, senders, dates, attachments
- **🌐 Web Interface** - Works in your browser, no special software needed
- **🔒 100% Private** - Your emails never leave your computer
- **📊 Smart Analytics** - See patterns in your email: busiest times, top contacts
- **📎 Attachment Finder** - Quickly locate any file ever sent or received
- **💬 Thread View** - See entire conversations in context

---

## Quick Start

### 🚀 Installation (30 seconds)

Open a terminal and run:

```bash
curl -sSL https://install.gmail-parser.com | bash
```

That's it! The installer handles everything for you.

### 📧 Your First Search (2 minutes)

1. **Start Gmail Parser** - It opens automatically after installation
2. **Choose Your Email File** - Select your `.mbox` file from Google Takeout
3. **Wait for Processing** - About 30 seconds for 10,000 emails
4. **Start Searching!** - Type anything in the search box

**Need your Gmail archive?** Visit [takeout.google.com](https://takeout.google.com) to download your emails from Google.

For detailed instructions, see our **[5-Minute Quick Start Guide](QUICK_START.md)**.

---

## How It Works

```
Your Gmail Archive (.mbox file)
           ↓
    Gmail Parser
           ↓
Fast Searchable Database
           ↓
    Web Dashboard
           ↓
Instant Search Results!
```

1. **Load** - Point Gmail Parser to your email archive file
2. **Process** - It builds a search index (one-time process, takes a few minutes)
3. **Search** - Use the web dashboard to instantly find any email
4. **Export** - Save search results as CSV, PDF, or other formats

---

## Documentation

### 📚 For Users

- **[User Guide](USER_GUIDE.md)** - Complete guide with screenshots and examples
- **[Quick Start](QUICK_START.md)** - Get running in 5 minutes
- **[Web Dashboard Guide](WEB_DASHBOARD_GUIDE.md)** - Master the search interface

### 🔧 For Developers

- **[Technical Reference](TECHNICAL_REFERENCE.md)** - Architecture, API, and development docs

---

## Examples

### Simple Search
Just type what you're looking for:
```
invoice
meeting tomorrow
vacation request
amazon order
```

### Advanced Search
Use operators for precise results:
```
from:boss@company.com subject:urgent
has:attachment filename:pdf after:2024-01-01
"exact phrase" AND (invoice OR receipt)
```

### Quick Filters
Click buttons to instantly filter:
- **Today** - Emails from today
- **This Week** - Last 7 days
- **📎** - Only emails with attachments
- **⭐** - Important/starred emails

---

## System Requirements

### Minimum
- Any modern computer (Windows, Mac, or Linux)
- 2GB free RAM
- Web browser (Chrome, Firefox, Edge, or Safari)
- Your Gmail archive file (.mbox format)

### Recommended
- 4GB RAM for large archives
- SSD for fastest performance
- Modern browser for best experience

---

## Performance

Gmail Parser is incredibly fast:

| What | How Fast | Example |
|------|----------|---------|
| **Parsing emails** | 1,000+ per second | 17,000 emails in 16 seconds |
| **Search** | < 10 milliseconds | Instant results, always |
| **Opening dashboard** | < 100 milliseconds | Faster than clicking a bookmark |
| **Exporting results** | < 1 second | 5,000 emails to CSV instantly |

---

## Privacy & Security

**Your emails stay on YOUR computer:**

- ✅ No cloud uploads
- ✅ No account required
- ✅ No tracking or analytics
- ✅ Works completely offline
- ✅ You can delete everything anytime

Gmail Parser runs 100% locally. Your emails never leave your machine.

---

## Support

### Getting Help

- **📖 Documentation** - Start with the [User Guide](USER_GUIDE.md)
- **❓ FAQ** - Common questions answered in the guide
- **💬 Community Forum** - [forum.gmail-parser.com](https://forum.gmail-parser.com)
- **📧 Email Support** - support@gmail-parser.com
- **🎥 Video Tutorials** - [YouTube Channel](https://youtube.com/gmail-parser)

### Troubleshooting

**Can't find your .mbox file?**
- Check your Downloads folder
- Look for `takeout-[date].mbox`
- Visit [takeout.google.com](https://takeout.google.com) if you haven't downloaded it yet

**Search not working?**
- Wait for processing to complete (progress bar shows status)
- Try a simpler search term
- Click "All" to reset filters

**Need more help?** See the [Troubleshooting section](USER_GUIDE.md#troubleshooting) in the User Guide.

---

## Screenshots

### Main Search Interface
```
┌──────────────────────────────────────────────────┐
│  Gmail Parser                          Settings  │
├──────────────────────────────────────────────────┤
│                                                  │
│     🔍 [Search your emails...]                  │
│                                                  │
│  [Today] [Week] [Month] [Year] [📎] [⭐]       │
│                                                  │
│  Results: 2,847 emails found                    │
│  ┌────────────────────────────────────────┐    │
│  │ From: John Smith                       │    │
│  │ Subject: Q3 Financial Report           │    │
│  │ Date: Dec 10, 2024                    │    │
│  │ Preview: Please find attached the...   │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Statistics Dashboard
```
Most Frequent Contacts        Email Activity
━━━━━━━━━━━━━━━━━━━━━        ━━━━━━━━━━━━━━━━━
1. john@example.com (847)     📊 Peak: Tue 10am
2. mary@company.com (623)      📊 Quiet: Weekends  
3. sales@store.com (412)       📊 Busiest: December
```

---

## Version Info

**Current Version:** 2.0.5 (December 2024)

**What's New:**
- 50x faster parsing with Rust acceleration
- Improved search accuracy
- Better attachment handling
- New statistics dashboard
- Dark mode support

---

## Contributing

We welcome contributions! If you're a developer interested in improving Gmail Parser:

1. Check the [Technical Reference](TECHNICAL_REFERENCE.md)
2. Read [Contributing Guidelines](TECHNICAL_REFERENCE.md#contributing-guidelines)
3. Submit issues or pull requests on [GitHub](https://github.com/auricleinc/mail_parser)

---

## License

Gmail Parser is open source software released under the MIT License.

---

## Acknowledgments

Gmail Parser uses these excellent open source projects:
- **FastAPI** for the web framework
- **SQLite FTS5** for full-text search
- **Rust** for performance-critical components

---

<div align="center">

**Ready to search your emails at the speed of thought?**

[**⚡ Get Started with Quick Start Guide**](QUICK_START.md)

[**📖 Read the Full User Guide**](USER_GUIDE.md)

[**🖥️ Learn the Web Dashboard**](WEB_DASHBOARD_GUIDE.md)

</div>

---

*Gmail Parser - Making email search instantaneous*