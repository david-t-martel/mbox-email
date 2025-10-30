# ⚡ Gmail Parser Quick Start Guide

**Get up and running in 5 minutes!**

---

## 📋 Before You Start

You'll need:
- ✅ Your Gmail backup file (ending in `.mbox`) 
- ✅ A computer with internet access
- ✅ 5 minutes of time

**Don't have your Gmail backup yet?** 
→ Visit [takeout.google.com](https://takeout.google.com) and download your Gmail data first

---

## 🚀 One-Command Installation

### Step 1: Open Your Terminal

**Windows Users:**
- Press `Windows key + R`
- Type `cmd` 
- Press Enter

**Mac Users:**
- Press `Cmd + Space`
- Type `terminal`
- Press Enter

**Linux Users:**
- Press `Ctrl + Alt + T`

### Step 2: Install Gmail Parser

Copy and paste this command:

```bash
curl -sSL https://install.gmail-parser.com | bash
```

Press Enter and wait about 30 seconds. You'll see:
```
✅ Gmail Parser installed successfully!
🌐 Opening dashboard in your browser...
```

---

## 📧 Your First Email Parse

### Step 3: Load Your Gmail Archive

When your browser opens to the dashboard:

1. **You'll see:** "Welcome! Let's load your emails"
   
2. **Click:** "Choose File" button
   
3. **Browse to:** Your `.mbox` file (probably in Downloads folder)
   
4. **Click:** "Start Parsing"

5. **Wait:** 
   - Small archive (under 1GB): ~30 seconds
   - Medium archive (1-5GB): 2-5 minutes  
   - Large archive (5GB+): 5-15 minutes
   
   You'll see a progress bar:
   ```
   Parsing emails... 
   [████████░░░░░░░░] 8,421 / 17,000 emails
   ```

### Step 4: Start Searching!

Once parsing completes:

1. **Try searching for:**
   - A person's name
   - A company name
   - A specific topic
   
2. **Example searches to try:**
   ```
   Amazon
   meeting
   invoice
   vacation
   "important update"
   ```

3. **See results instantly!** Click any email to read it.

---

## 📍 Where to Find Everything

### Your Dashboard
- **URL:** http://localhost:8080
- **Bookmark it!** This is where you'll always access your emails

### Your Parsed Email Database
- **Location:** `Documents/GmailParser/my-emails.db`
- **This file** contains your searchable email index
- **Keep it safe** - it's your parsed email data

### Settings and Configuration
- Click the **gear icon** ⚙️ in the top-right corner
- Change themes, adjust settings, manage archives

---

## 🎯 Quick Success Test

Let's make sure everything works:

1. **Search for your own email address**
   - Type it in the search box
   - You should see all emails you've sent

2. **Click the "Statistics" tab**
   - You should see graphs and numbers
   - Shows your email patterns and top contacts

3. **Try the date filter**
   - Click "This Year" 
   - Only recent emails should appear

**All working?** Congratulations! You're ready to use Gmail Parser! 🎉

---

## 💡 What to Do Next

### Essential Features to Try

1. **Advanced Search**
   ```
   from:boss@company.com
   has:attachment
   after:2024-01-01
   ```

2. **Export Your Results**
   - Search for something
   - Click "Export" → "CSV"
   - Open in Excel

3. **View Email Threads**
   - Click any email
   - Click "View Conversation"
   - See the whole discussion

### Explore More Features

- **Read the full guide:** [USER_GUIDE.md](USER_GUIDE.md)
- **Learn the dashboard:** [WEB_DASHBOARD_GUIDE.md](WEB_DASHBOARD_GUIDE.md)
- **Watch tutorials:** [youtube.com/gmail-parser](https://youtube.com/gmail-parser)

---

## ❓ Quick Troubleshooting

### Nothing happens when I search?
- Make sure parsing finished (check the progress bar)
- Try a simpler search term
- Click "All" to reset filters

### Can't find my mbox file?
- Check your Downloads folder
- Look for files named like `takeout-20241215.mbox`
- It might still be downloading from Google

### Browser shows error?
- Refresh the page (F5)
- Try a different browser
- Make sure the parser is running (check terminal)

### Still stuck?
- **Quick help:** Type `gmail-parser help` in terminal
- **Full guide:** See [USER_GUIDE.md](USER_GUIDE.md)
- **Email us:** support@gmail-parser.com

---

## ✨ Pro Tips for New Users

1. **Start with simple searches** - Just type one word at first
2. **Use the quick filters** - They're faster than typing dates
3. **Star important searches** - Save them for quick access
4. **Export regularly** - Keep backups of important search results
5. **Let big archives parse overnight** - Start before bed, wake up to searchable emails

---

## 🎉 You're Ready!

You now know how to:
- ✅ Install Gmail Parser
- ✅ Load your email archive
- ✅ Search your emails
- ✅ Access your dashboard
- ✅ Find help when needed

**Happy searching!** 📧🔍

---

*Installation problems? Email quickstart@gmail-parser.com for help within 24 hours*