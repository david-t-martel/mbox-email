# 🖥️ Gmail Parser Web Dashboard Guide

Your complete guide to mastering the Gmail Parser dashboard interface.

---

## Opening the Dashboard

### First Time Launch

When you start Gmail Parser, the dashboard opens automatically in your default browser.

**If it doesn't open automatically:**
1. Open your web browser (Chrome, Firefox, Edge, or Safari)
2. Type in the address bar: `localhost:8080`
3. Press Enter
4. Bookmark this page for easy access!

### Daily Access

**Option 1: Browser Bookmark**
- Use your saved bookmark
- Dashboard opens instantly

**Option 2: Desktop Shortcut**
- Windows: Right-click desktop → New → Shortcut → Enter `http://localhost:8080`
- Mac: Drag the URL from your browser to desktop
- Linux: Create a .desktop file pointing to the URL

**Option 3: Terminal Command**
```
gmail-parser open
```

---

## Understanding the Interface

### Dashboard Layout

```
┌──────────────────────────────────────────────────────────────┐
│  📧 Gmail Parser             Home | Search | Browse | Stats  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────┐  ┌──────────────┐ │
│  │                                      │  │ Quick Stats  │ │
│  │     🔍 Search Box                    │  │              │ │
│  │     [                          ][Go] │  │ 📧 17,492   │ │
│  │                                      │  │ 📎 3,821    │ │
│  └─────────────────────────────────────┘  │ 👥 892      │ │
│                                            └──────────────┘ │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Filter Bar                                          │   │
│  │ [Today][Week][Month][Year] [📎][⭐][🏷️]           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Email List                          │   │
│  │  ┌──────────────────────────────────────────┐      │   │
│  │  │ From: John Smith         Dec 15, 2024    │      │   │
│  │  │ Meeting Tomorrow                         │      │   │
│  │  │ Hi, just confirming our meeting...       │      │   │
│  │  └──────────────────────────────────────────┘      │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### Key Areas Explained

#### 1. Navigation Bar (Top)
- **Home** - Main search interface
- **Search** - Advanced search options
- **Browse** - Browse by folders/labels
- **Stats** - Email statistics and insights

#### 2. Search Box (Center)
- Type anything to search
- Press Enter or click magnifying glass
- Auto-suggests as you type

#### 3. Quick Stats (Right Panel)
- **📧 Total Emails** - Click to see all
- **📎 With Attachments** - Click to filter
- **👥 Total Contacts** - Click for address book

#### 4. Filter Bar (Below Search)
Quick-access filters you can combine:
- **Date Filters**: Today, Week, Month, Year
- **Type Filters**: 
  - 📎 Attachments only
  - ⭐ Starred/Important
  - 🏷️ Tagged emails

#### 5. Email List (Main Area)
- Shows 20 emails per page
- Click to read full email
- Hover for quick actions

---

## Searching Emails

### Basic Search

Just type and press Enter! The search looks everywhere:
- Email content
- Subject lines  
- Sender names and addresses
- Attachments names

**Examples:**
```
invoice           - Finds all emails containing "invoice"
john@example.com  - All emails from/to John
"exact phrase"    - Must contain this exact phrase
```

### Search Operators

Make your searches more precise:

| What You Want | Type This | Example |
|--------------|-----------|---------|
| Emails FROM someone | `from:` | `from:boss@work.com` |
| Emails TO someone | `to:` | `to:client@company.com` |
| Subject contains | `subject:` | `subject:invoice` |
| Has attachments | `has:attachment` | `has:attachment` |
| Specific file type | `filename:` | `filename:pdf` |
| Date range | `after:` `before:` | `after:2024-01-01` |
| Exclude words | `-word` or `NOT` | `invoice -draft` |
| Either word | `OR` | `invoice OR receipt` |
| Both words | `AND` | `invoice AND paid` |

### Search Tips & Tricks

#### 🎯 Pro Search Combinations

**Find all invoices from this year with PDFs:**
```
invoice has:attachment filename:pdf after:2024-01-01
```

**Emails from your boss about meetings, not lunch:**
```
from:boss@company.com meeting -lunch
```

**Urgent emails from last week:**
```
(urgent OR important OR asap) after:2024-12-08
```

#### 💡 Search Shortcuts

- **Ctrl+F** (Cmd+F on Mac) - Jump to search box
- **Enter** - Search
- **Esc** - Clear search
- **Tab** - Navigate through results
- **Arrow keys** - Select emails
- **Space** - Preview selected email

---

## Filtering and Sorting

### Quick Filters

Click these buttons to instantly filter your view:

#### Date Range Filters
- **Today** - Last 24 hours only
- **This Week** - Last 7 days
- **This Month** - Last 30 days  
- **This Year** - January 1 to today
- **All Time** - Remove date filter
- **Custom** - Pick specific dates

#### Special Filters
- **📎 Attachments** - Only emails with files
- **⭐ Important** - Starred or marked important
- **🏷️ Tagged** - Emails you've tagged
- **💬 Threads** - Emails with replies
- **📤 Sent** - Emails you sent
- **📥 Received** - Emails sent to you

### Combining Filters

Filters work together! Click multiple filters to narrow results:

1. Click "This Month" 
2. Then click "📎 Attachments"
3. Result: This month's emails with attachments

To remove a filter, click it again (it will un-highlight).

### Sorting Options

Click the sort dropdown (⬇️) to reorder results:

- **Newest First** (default)
- **Oldest First**
- **Sender A-Z**
- **Sender Z-A**  
- **Subject A-Z**
- **Subject Z-A**
- **Largest First** (by size)
- **Most Attachments**

---

## Viewing Email Details

### Email Preview

When you click an email in the list, the preview panel opens:

```
┌────────────────────────────────────────────────┐
│ From: John Smith <john@example.com>           │
│ To: You <you@example.com>                     │
│ Date: December 15, 2024 at 3:45 PM           │
│ Subject: Meeting Tomorrow                      │
├────────────────────────────────────────────────┤
│                                                │
│ Hi there,                                      │
│                                                │
│ Just confirming our meeting tomorrow at 2 PM. │
│ I've attached the agenda for your review.     │
│                                                │
│ Best regards,                                  │
│ John                                           │
│                                                │
├────────────────────────────────────────────────┤
│ 📎 Attachments (1):                           │
│ • meeting-agenda.pdf (245 KB) [Download]      │
└────────────────────────────────────────────────┘
```

### Email Actions

Above each email, you'll see action buttons:

- **Reply** - (Currently exports to your email client)
- **Forward** - (Currently exports to your email client)
- **Print** - Print this email
- **Export** - Save as PDF or text file
- **Tag** - Add a tag for organization
- **Star** - Mark as important
- **Thread** - View entire conversation

### Viewing Conversations/Threads

To see an entire email conversation:

1. Click any email in the thread
2. Click "View Thread" button
3. The thread view opens showing:
   - All messages in chronological order
   - Participants on the left
   - Timeline on the right
   - Collapsed quoted text (click to expand)

Thread navigation:
- **↑↓ Arrow keys** - Move between messages
- **Space** - Expand/collapse message
- **Esc** - Return to list

### Handling Attachments

When an email has attachments:

1. **See attachment list** at bottom of email
2. **Click filename** to preview (if supported)
3. **Click Download** to save to your computer
4. **Click "Open"** to open with default program

Supported preview formats:
- Images (JPG, PNG, GIF)
- PDFs
- Text files
- Common Office documents

---

## Advanced Features

### Saved Searches

Save frequently-used searches:

1. **Perform your search**
2. **Click the star** (⭐) next to search box
3. **Name your search** (e.g., "Weekly Reports")
4. **Access saved searches** from sidebar

### Tags and Labels

Organize emails with tags:

1. **Select emails** (checkbox or Ctrl+Click)
2. **Click Tag button** 
3. **Choose existing tag** or create new
4. **Filter by tag** using the tag button

Common tag ideas:
- "To Review"
- "Important"
- "Project XYZ"
- "Tax Documents"
- "Follow Up"

### Bulk Operations

Select multiple emails for bulk actions:

1. **Check boxes** next to emails
2. **Or:** Hold Ctrl (Cmd on Mac) and click emails
3. **Or:** Click first, hold Shift, click last (selects range)

Bulk actions available:
- **Export selected** - Save multiple emails
- **Tag selected** - Apply same tag
- **Print selected** - Print batch
- **Delete from view** - Remove from results (doesn't delete originals)

### Keyboard Shortcuts

Speed up your workflow with these shortcuts:

| Action | Windows/Linux | Mac |
|--------|--------------|-----|
| Search | Ctrl+F | Cmd+F |
| Clear search | Esc | Esc |
| Next email | Down arrow | Down arrow |
| Previous email | Up arrow | Up arrow |
| Open email | Enter | Enter |
| Close email | Esc | Esc |
| Select all | Ctrl+A | Cmd+A |
| Export | Ctrl+E | Cmd+E |
| Print | Ctrl+P | Cmd+P |
| Refresh | F5 | Cmd+R |
| Settings | Ctrl+, | Cmd+, |

---

## Customization

### Theme Options

Change the dashboard appearance:

1. Click **Settings** (gear icon ⚙️)
2. Choose **Appearance**
3. Select theme:
   - **Light** - Default bright theme
   - **Dark** - Easy on the eyes
   - **Auto** - Follows system settings
   - **High Contrast** - Accessibility mode

### Display Settings

Customize how emails appear:

1. **Settings** → **Display**
2. Adjust:
   - **Emails per page**: 10, 20, 50, 100
   - **Preview length**: Short, Medium, Long
   - **Show avatars**: On/Off
   - **Date format**: Relative/Absolute
   - **Time zone**: Local/Original

### Column Configuration

Choose which columns to show:

1. Click **column icon** (☰) above email list
2. Check/uncheck columns:
   - Subject
   - From
   - To
   - Date
   - Size
   - Attachments
   - Tags
   - Thread Count

Drag column headers to reorder.

---

## Performance Tips

### Making Searches Faster

1. **Be specific** - More words = faster, more accurate results
2. **Use filters** - Date filters dramatically speed up searches
3. **Save complex searches** - Saved searches run faster
4. **Index regularly** - Settings → Maintenance → Reindex (monthly)

### Browser Optimization

For best performance:

1. **Use modern browser** - Chrome, Firefox, or Edge
2. **Clear cache monthly** - Settings → Clear Browser Cache
3. **Close unused tabs** - Each tab uses memory
4. **Disable extensions** - Some slow down the dashboard

### Large Archives

If you have 50,000+ emails:

1. **Use date filters first** - Narrow before searching
2. **Export results** - Work with exports for analysis
3. **Increase page size** - Fewer pages = faster navigation
4. **Consider splitting** - Separate archives by year

---

## Tips for Power Users

### Search Formulas

Create complex searches using formulas:

**All emails about Project Alpha from team members, excluding drafts:**
```
(from:@company.com OR from:@team.org) "Project Alpha" -draft -"work in progress"
```

**Financial documents from this quarter:**
```
(invoice OR receipt OR "purchase order" OR statement) has:attachment after:2024-10-01
```

**Urgent customer emails requiring response:**
```
from:@customer.com (urgent OR important OR asap) NOT "auto-reply" NOT "out of office"
```

### Dashboard URLs

Bookmark specific views:

- Search results: `localhost:8080/search?q=invoice`
- Date range: `localhost:8080/search?after=2024-01-01&before=2024-12-31`
- With attachments: `localhost:8080/search?has=attachment`
- Specific sender: `localhost:8080/search?from=boss@company.com`

### Data Export Automation

Set up automated exports:

1. **Settings** → **Automation**
2. **Create Rule**:
   - Name: "Weekly Report"
   - Search: "subject:weekly report"
   - Schedule: Every Monday
   - Format: CSV
   - Destination: Desktop folder

### Integration Tips

Connect with other tools:

- **Excel**: Export as CSV, open directly
- **Outlook**: Export as .eml files
- **Gmail**: Export with labels intact
- **Database**: Export as JSON for import
- **Analytics**: Use CSV exports in Tableau/PowerBI

---

## Mobile Access

While the dashboard is designed for desktop, you can access it on mobile:

### Setup for Mobile

1. **Ensure computer is on** and Gmail Parser is running
2. **Find your computer's IP**:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`
3. **On mobile browser**, go to: `http://[YOUR-IP]:8080`
4. **Bookmark** for easy access

### Mobile Interface Tips

- **Rotate to landscape** for better view
- **Pinch to zoom** on email content
- **Swipe left/right** to navigate emails
- **Long press** for context menu
- **Use simple searches** - typing is harder on mobile

---

## Troubleshooting Dashboard Issues

### Common Problems & Solutions

#### Dashboard Won't Load

1. **Check Gmail Parser is running**:
   - Look for the terminal window
   - Should show "Server running on port 8080"

2. **Try different address**:
   - `http://localhost:8080`
   - `http://127.0.0.1:8080`
   - `http://0.0.0.0:8080`

3. **Check firewall** isn't blocking port 8080

#### Search Not Working

1. **Wait for indexing** - Check progress bar
2. **Clear browser cache** - Ctrl+Shift+Delete
3. **Try simpler search** - Single word first
4. **Reset filters** - Click "Clear All"

#### Slow Performance

1. **Reduce results per page** - Settings → Display → 20 per page
2. **Clear old exports** - Settings → Storage → Clear Exports
3. **Restart browser** - Memory leak possible
4. **Check disk space** - Need 1GB free minimum

#### Display Issues

1. **Zoom level** - Reset with Ctrl+0 (Cmd+0 on Mac)
2. **Update browser** - Use latest version
3. **Disable extensions** - Try incognito/private mode
4. **Clear cache** - Forces fresh load

---

## Getting Additional Help

### Built-in Help

- Click **?** icon for context help
- Hover over any button for tooltip
- Check **Settings → Help** for guides

### Resources

- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Video Tutorials**: youtube.com/gmail-parser
- **Community Forum**: forum.gmail-parser.com
- **Email Support**: support@gmail-parser.com

---

*Dashboard version 2.0 - Last updated December 2024*