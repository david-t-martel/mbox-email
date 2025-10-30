# 🚀 Quick Start Guide - Email Dashboard

## What's Happening Now

Your **39,768 emails** are being processed right now! The parser is:

1. ✅ **Counting messages** (4-5 minutes) - Currently running
2. ⏳ **Parsing emails** (20-30 minutes) - Coming next
3. ⏳ **Generating dashboard** (10 seconds) - Final step

## When It's Done

You'll have an **interactive web dashboard** ready to use!

### 📂 What Gets Generated

```
output/
├── index.html ← OPEN THIS IN YOUR BROWSER!
├── email_data.json
├── analytics_report.html
├── email_index.db
├── by-date/
│   └── 2025/10/28/
│       └── 20251028_1444_sender_subject_000123.html
├── by-sender/
│   └── auricleinc.com/
│       └── 20251028_1444_sender_subject_000123.html
└── by-thread/
    └── thread_1847.../
        └── pos001_20251028_1444_sender_subject_000123.html
```

## 🌐 Using the Dashboard

### Step 1: Open the Dashboard

**macOS:**
```bash
open ./output/index.html
```

**Windows:**
```bash
start ./output/index.html
# or in WSL:
cmd.exe /c start ./output/index.html
```

**Linux:**
```bash
xdg-open ./output/index.html
```

### Step 2: Browse Your Emails

The dashboard gives you multiple ways to find emails:

#### 🔍 **Search Bar** (Top of page)
Type to search across:
- Email subjects
- Sender names
- Sender email addresses

**Example searches:**
- `tinnitus` - Find all emails about tinnitus
- `john doe` - Find emails from John Doe
- `meeting` - Find meeting-related emails

#### 🎯 **Filters** (Below search)

**Filter by Domain:**
- Select a domain (e.g., "umich.edu", "auricleinc.com")
- See only emails from that domain

**Filter by Label:**
- Select a Gmail label
- See only emails with that label

**Filter by Attachments:**
- "Yes" - Only emails with attachments
- "No" - Only emails without attachments

**Combine Filters:**
- Use search + domain + label together
- Example: Search "project" + Domain "auricleinc.com" + Has Attachments "Yes"

#### 🔄 **View Modes** (Tabs)

**📅 By Date:**
- Browse emails chronologically
- Files organized by year/month/day

**👤 By Sender:**
- Group emails by sender's domain
- Quickly find all emails from a specific company

**💬 By Thread:**
- See email conversations
- Follow thread discussions in order

### Step 3: Open Emails

- **Click** the subject link to open email in new tab
- **Or** click "Open" button in Actions column
- Emails open as beautiful HTML pages with:
  - Full formatting
  - Embedded images
  - Attachment list
  - Thread information

## 📊 Dashboard Features

### Statistics Panel (Header)
- **Total Emails**: Complete count
- **Threads**: Unique conversations
- **Domains**: Number of unique senders
- **With Attachments**: Count of emails with files

### Email Table

**Sortable Columns** (click headers to sort):
- **Date**: Sort by time received
- **From**: Sort by sender name
- **Subject**: Sort alphabetically
- **Labels**: Sort by Gmail labels

**What You See:**
- Date in readable format
- Sender name and email
- Subject (clickable link)
- Gmail labels as colored badges
- Attachment icon (📎) if present

### Pagination
- Shows 50 emails per page
- "Previous" and "Next" buttons
- Page indicator (e.g., "Page 1 of 795")

## 🎨 Human-Readable Filenames

All email files have descriptive names:

**Format**: `YYYYMMDD_HHMM_sender_subject_index.html`

**Example**: `20251028_1444_john_doe_meeting_notes_about_project_000123.html`

**What each part means:**
- `20251028` - Date (October 28, 2025)
- `1444` - Time (2:44 PM)
- `john_doe` - Sender's name
- `meeting_notes_about_project` - Subject (truncated, sanitized)
- `000123` - Unique index number

**Benefits:**
✅ Sort alphabetically by date/time
✅ Quickly identify sender
✅ Preview subject without opening
✅ Works on any operating system

## 📈 Analytics Dashboard

Open `output/analytics_report.html` for:
- Email volume charts (daily, hourly)
- Top senders/domains
- Label distribution
- Day of week patterns
- Interactive Plotly visualizations

## 🔍 Command-Line Search

You can also search from command line:

```bash
uv run python -m mail_parser.cli search \
  --database ./output/email_index.db \
  --query "your search term" \
  --limit 50
```

## 💡 Pro Tips

### Finding Specific Emails

1. **Recent emails**: Click "Date" column header twice to sort newest first
2. **From specific person**: Use domain filter or search their name
3. **With attachments**: Use attachment filter + search term
4. **In a conversation**: Switch to "By Thread" view

### Keyboard Shortcuts

- `Ctrl+F` (or `Cmd+F`) to search the current page
- Arrow keys to navigate
- Enter to follow links

### Mobile Access

The dashboard is mobile-friendly:
- Responsive design
- Touch-friendly buttons
- Readable on small screens
- Horizontal scrolling for table

## ⚠️ Troubleshooting

### Dashboard Won't Load

1. Make sure `output/email_data.json` exists
2. Check browser console (F12) for errors
3. Try a different browser (Chrome, Firefox, Safari)
4. Make sure parsing completed successfully

### Can't Find an Email

1. Try different search terms
2. Check if filters are active (clear them)
3. Use "By Date" view and browse chronologically
4. Try command-line search (more powerful)

### Slow Performance

1. Reduce emails per page (edit index.html)
2. Use filters to narrow results
3. Search instead of browsing all
4. Close other browser tabs

## 📞 Need Help?

- Check `parse.log` for processing details
- Read `README.md` for full documentation
- Look at `analytics_report.html` for statistics

---

## 🎉 Enjoy Exploring Your Emails!

The dashboard makes it easy to:
- Find that important email from years ago
- See all emails from a specific sender
- Follow conversation threads
- Identify patterns in your email history
- Export and organize your digital correspondence

**Happy browsing! 📧**
