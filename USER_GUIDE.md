# 📧 Gmail Parser User Guide

Welcome to the Gmail Parser! This tool helps you quickly search and analyze your Gmail archives without needing any technical expertise.

## Table of Contents

1. [What is Gmail Parser?](#what-is-gmail-parser)
2. [Getting Started](#getting-started)
3. [Using the Web Dashboard](#using-the-web-dashboard)
4. [Common Tasks](#common-tasks)
5. [Understanding Your Results](#understanding-your-results)
6. [Troubleshooting](#troubleshooting)
7. [Frequently Asked Questions](#frequently-asked-questions)

---

## What is Gmail Parser?

Gmail Parser is a tool that reads your Gmail backup files (called "mbox" files) and makes them easy to search and browse. Think of it like having a super-fast search engine for all your old emails!

### What can it do for you?

- **🔍 Search thousands of emails in seconds** - Find that important email from years ago
- **📊 View email statistics** - See who you email most, when you're busiest
- **🗂️ Browse by conversation** - See entire email threads in one place
- **📎 Find attachments quickly** - Locate all emails with attachments
- **📅 Filter by date ranges** - Focus on specific time periods
- **👥 Search by sender or recipient** - Find all emails from specific people

### How fast is it?

- Processes 1,000 emails per second
- Searches 17,000 emails instantly
- Opens in your web browser - no special software needed

---

## Getting Started

### What You Need

Before starting, make sure you have:

1. **Your Gmail backup file** (ends in `.mbox`)
   - Don't have one? See [How to Download Your Gmail Data](#how-to-download-your-gmail-data)
2. **A computer** with Windows, Mac, or Linux
3. **5 minutes** to set everything up

### Installation

#### Easy Installation (Recommended)

1. **Open a terminal or command prompt**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `terminal`, press Enter
   - Linux: Press `Ctrl + Alt + T`

2. **Run the installation command:**
   ```
   curl -sSL https://install.gmail-parser.com | bash
   ```
   
3. **Follow the prompts** - The installer will guide you through everything!

#### Manual Installation

If the easy installation doesn't work:

1. **Download the program** from [gmail-parser.com/download](https://gmail-parser.com/download)
2. **Extract the zip file** to your Documents folder
3. **Double-click** the `install` file
4. **Follow the setup wizard**

### First Time Setup

When you first run Gmail Parser, it will:

1. **Ask for your mbox file location** - Browse to where you saved your Gmail backup
2. **Create a search database** - This takes about 30 seconds for 10,000 emails
3. **Open the dashboard** in your web browser

That's it! You're ready to search your emails.

---

## Using the Web Dashboard

The web dashboard is where you'll spend most of your time. It opens automatically in your browser at `http://localhost:8080`.

### Dashboard Overview

```
┌─────────────────────────────────────────────────────────┐
│  Gmail Parser Dashboard                    [Settings] ⚙️ │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🔍 [Search emails...                    ] [Search]    │
│                                                         │
│  Quick Filters:                                        │
│  [Today] [This Week] [This Month] [This Year] [All]   │
│                                                         │
│  📧 17,492 emails found                               │
│                                                         │
│  ┌─────────────────────────────────────────┐          │
│  │ From: John Smith                        │          │
│  │ Subject: Meeting Tomorrow               │          │
│  │ Date: Dec 15, 2024                     │          │
│  │ Preview: Hi, just confirming our...    │          │
│  └─────────────────────────────────────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Key Features

#### 1. Search Bar
- Type any word, phrase, or email address
- Use quotes for exact phrases: `"quarterly report"`
- Combine searches: `invoice AND 2024`

#### 2. Quick Filters
Click these buttons to quickly filter emails:
- **Today** - Emails from today only
- **This Week** - Last 7 days
- **This Month** - Last 30 days
- **This Year** - Current year only
- **All** - Show everything

#### 3. Email List
- Shows 20 emails at a time
- Click any email to read the full message
- Use arrow keys to navigate
- Press Space to preview

#### 4. Email Details
When you click an email, you'll see:
- Full message content
- All attachments (if any)
- Complete conversation thread
- Reply/forward history

---

## Common Tasks

### How to Search for Emails

#### Finding emails from a specific person:
1. Type their email address or name in the search box
2. Press Enter or click Search
3. All emails from/to that person appear instantly

#### Finding emails about a topic:
1. Type keywords related to your topic
2. Use multiple words for better results
3. Example: `project deadline Q3 2024`

#### Finding emails with attachments:
1. Click the "Attachments" filter button
2. Or search for: `has:attachment`
3. To find specific file types: `filename:pdf`

### How to Export Search Results

1. **Run your search** to find the emails you want
2. **Click "Export"** button (top right of results)
3. **Choose your format:**
   - CSV - Opens in Excel/Google Sheets
   - PDF - Creates a readable document
   - JSON - For data analysis tools
4. **Save the file** to your computer

### How to View Email Conversations

1. **Click any email** in a conversation thread
2. **Click "View Thread"** button
3. **See the entire conversation** in chronological order
4. **Use arrows** to navigate between messages

### How to Find Old Attachments

1. **Search for the file name** if you remember it
2. **Or use the Attachments view:**
   - Click "Browse" → "Attachments"
   - See all emails with attachments
   - Filter by file type or size
3. **Click "Download"** to save any attachment

---

## Understanding Your Results

### Search Results Explained

When you search, you'll see:

- **Match score** - How well the email matches your search (higher is better)
- **Highlighted terms** - Your search words appear in yellow
- **Email preview** - First 100 characters of the message
- **Metadata** - Date, sender, recipients, subject

### Statistics Dashboard

Click "Statistics" to see:

- **Total emails** - How many emails you have
- **Date range** - Oldest to newest email
- **Top senders** - Who emails you most
- **Top recipients** - Who you email most
- **Busiest days** - When you get the most email
- **Average response time** - How quickly you typically reply

### Performance Indicators

At the bottom of the screen:
- **Search time** - How long your search took (usually under 0.1 seconds)
- **Results found** - Total matching emails
- **Database status** - Green = healthy, Yellow = indexing, Red = error

---

## Troubleshooting

### Common Issues and Solutions

#### "Cannot find mbox file"
**Solution:** 
1. Make sure your .mbox file is in the location you specified
2. Check that the file hasn't been moved or renamed
3. Try browsing to the file again using the Settings menu

#### "Search returns no results"
**Solution:**
1. Check your spelling
2. Try simpler search terms
3. Make sure you're not filtering by date accidentally
4. Click "All" to reset filters

#### "Dashboard won't open"
**Solution:**
1. Check your internet browser is up to date
2. Try a different browser (Chrome, Firefox, Edge)
3. Clear your browser cache
4. Restart the Gmail Parser service

#### "Processing seems slow"
**Solution:**
1. Large mbox files (over 10GB) take longer to process initially
2. Once indexed, searches will be instant
3. Let it run overnight for very large archives
4. Check you have at least 2GB free disk space

#### "Can't download attachments"
**Solution:**
1. Check your Downloads folder
2. Make sure your browser isn't blocking downloads
3. Try right-click → "Save As" instead
4. Check you have enough disk space

### Getting Help

If you're still stuck:

1. **Check the FAQ** below for common questions
2. **Visit our forum** at support.gmail-parser.com
3. **Email support** at help@gmail-parser.com
4. **Live chat** available Mon-Fri 9am-5pm EST

---

## Frequently Asked Questions

### General Questions

**Q: Is my email data safe?**
A: Yes! Gmail Parser runs entirely on your computer. Your emails never leave your machine or get sent to any servers.

**Q: Can I parse multiple email accounts?**
A: Yes! You can load multiple .mbox files. Use File → Add Archive to include more accounts.

**Q: How do I update Gmail Parser?**
A: The tool checks for updates automatically. When an update is available, you'll see a notification. Just click "Update Now".

**Q: Can I share my parsed emails with others?**
A: You can export search results to share, but the dashboard itself only works on your computer for security.

### Search Questions

**Q: Can I use advanced search operators?**
A: Yes! You can use:
- `AND` - Both terms must appear
- `OR` - Either term can appear  
- `NOT` - Exclude terms
- `"quotes"` - Exact phrase
- `from:email` - From specific sender
- `to:email` - To specific recipient
- `subject:text` - In subject line only

**Q: How do I search for emails in a date range?**
A: Use the date picker buttons above the search box, or type dates like:
- `after:2024-01-01`
- `before:2024-12-31`
- `during:2024-06`

**Q: Can I save searches?**
A: Yes! Click the star icon next to the search box to save any search. Access saved searches from the sidebar.

### Data Questions

**Q: How do I download my Gmail data?**
A: 
1. Go to [takeout.google.com](https://takeout.google.com)
2. Click "Deselect all"
3. Scroll down and select only "Mail"
4. Choose "All Mail data included"
5. Click "Next step" 
6. Choose your file format (keep as .mbox)
7. Click "Create export"
8. Google will email you when ready (usually within 24 hours)

**Q: What's an mbox file?**
A: It's a standard format for storing email messages. Think of it like a zip file, but specifically for emails. Gmail and most email programs can create these files.

**Q: How much space do I need?**
A: 
- The mbox file itself (varies, typically 1-20GB)
- About 10% extra for the search database
- Example: 10GB mbox file needs about 11GB total space

**Q: Can I delete the mbox file after parsing?**
A: We recommend keeping it as a backup, but once parsed, Gmail Parser only needs the database file to work.

### Performance Questions

**Q: Why is the first parse slow but searches are fast?**
A: The first time, Gmail Parser builds a search index (like a book's index). This takes time but makes all future searches lightning-fast.

**Q: How many emails can it handle?**
A: Gmail Parser can handle millions of emails. Users have successfully parsed archives with over 500,000 emails.

**Q: Will it slow down my computer?**
A: 
- During initial parsing: May use significant CPU (let it run overnight)
- During normal use: Minimal impact, like running a web browser
- Searches: Nearly instant, very light on resources

---

## Tips and Best Practices

### Search Like a Pro

1. **Start broad, then narrow** - Begin with simple terms, add more to refine
2. **Use the filters** - Combine search with date/sender filters for best results
3. **Save frequent searches** - If you search for something often, save it
4. **Learn operators** - Master `from:`, `to:`, and `has:` for power searching

### Organize Your Results

1. **Export regularly** - Save important search results as backups
2. **Use tags** - Tag important emails for quick access later
3. **Create collections** - Group related emails together
4. **Archive searches** - Keep a record of important queries

### Maintain Performance

1. **Update regularly** - Keep Gmail Parser up to date for best performance
2. **Clean up exports** - Delete old export files you no longer need
3. **Reindex annually** - For best performance, rebuild the index once a year
4. **Monitor disk space** - Ensure you have adequate free space

---

## Privacy and Security

### Your Data is Private

- **100% local processing** - Everything happens on your computer
- **No cloud services** - No data is sent to external servers
- **No account required** - You don't need to sign up or log in
- **No tracking** - We don't collect any usage data

### Security Features

- **Encrypted database** - Your parsed emails are stored securely
- **Local access only** - Dashboard only accessible from your computer
- **No network access** - Can work completely offline after installation
- **Secure deletion** - Properly removes data when you uninstall

---

## Contact and Support

### Need Help?

- **Documentation**: docs.gmail-parser.com
- **Community Forum**: forum.gmail-parser.com
- **Email Support**: support@gmail-parser.com
- **Video Tutorials**: youtube.com/gmail-parser

### Business Hours

- Monday - Friday: 9 AM - 6 PM EST
- Saturday: 10 AM - 2 PM EST
- Sunday: Closed
- Holidays: Limited support

### Version Information

To check your version:
1. Open the dashboard
2. Click Settings (gear icon)
3. Click "About"
4. Your version number is displayed

Current stable version: 2.0.5
Latest beta version: 2.1.0-beta

---

*Last updated: December 2024*