# Easy Installation Guide - Mail Parser

**No technical experience required!** Choose your operating system below and follow the simple steps.

## Quick Start - Choose Your Method

| Method | Best For | Time | Difficulty |
|--------|----------|------|------------|
| [One-Click Installer](#one-click-installers) | Windows/Mac/Linux users | 5 min | Easiest |
| [Docker Desktop](#docker-deployment) | Anyone with Docker | 2 min | Very Easy |
| [Cloud Deploy](#cloud-deployment) | Access from anywhere | 10 min | Easy |

---

## One-Click Installers

### Windows (10/11)

**Option 1: PowerShell Installer (Recommended)**

1. Download the installer:
   - Right-click this link: [install_windows.ps1](./install_windows.ps1)
   - Click "Save link as..."
   - Save to your Downloads folder

2. Run the installer:
   - Press `Windows Key + X`
   - Click "Windows PowerShell (Admin)" or "Terminal (Admin)"
   - Copy and paste this command:
   ```powershell
   cd ~/Downloads
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\install_windows.ps1
   ```

3. Follow the prompts:
   - Installer will check for Python
   - Install missing dependencies automatically
   - Set up the mail parser
   - Open the dashboard in your browser

**What the installer does:**
- ✅ Checks if Python is installed (installs if missing)
- ✅ Installs UV package manager
- ✅ Sets up mail parser
- ✅ Runs a test to verify everything works
- ✅ Opens the web dashboard

---

### macOS (10.15+)

**Terminal Installer**

1. Open Terminal:
   - Press `Cmd + Space`
   - Type "Terminal"
   - Press Enter

2. Run this single command:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/your-repo/mail_parser/main/install_macos.sh | bash
   ```

   **OR** download and run manually:
   ```bash
   cd ~/Downloads
   curl -O https://raw.githubusercontent.com/your-repo/mail_parser/main/install_macos.sh
   chmod +x install_macos.sh
   ./install_macos.sh
   ```

3. Enter your password when prompted (for installing dependencies)

4. Wait for installation to complete (5-10 minutes)

5. Dashboard will open automatically in Safari

**What the installer does:**
- ✅ Installs Homebrew (if needed)
- ✅ Installs Python 3.10+ (if needed)
- ✅ Installs UV package manager
- ✅ Sets up mail parser
- ✅ Creates desktop shortcut
- ✅ Opens dashboard

---

### Linux (Ubuntu/Debian/Fedora)

**One-Line Installer**

1. Open Terminal:
   - Press `Ctrl + Alt + T`

2. Run this command:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/your-repo/mail_parser/main/install_linux.sh | bash
   ```

   **OR** download and run manually:
   ```bash
   cd ~/Downloads
   wget https://raw.githubusercontent.com/your-repo/mail_parser/main/install_linux.sh
   chmod +x install_linux.sh
   ./install_linux.sh
   ```

3. Enter password when prompted (for package installation)

4. Wait for installation (5-10 minutes)

5. Dashboard opens in default browser

**What the installer does:**
- ✅ Detects your Linux distribution
- ✅ Installs Python 3.10+ (if needed)
- ✅ Installs UV package manager
- ✅ Sets up mail parser
- ✅ Creates application launcher
- ✅ Opens dashboard

---

## Docker Deployment

**Easiest way to run Mail Parser - works on any operating system!**

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (free)

### One-Command Setup

**Windows (PowerShell):**
```powershell
docker run -d -p 8080:8080 -v ${PWD}/mail_data:/data mailparser/app:latest
```

**Mac/Linux (Terminal):**
```bash
docker run -d -p 8080:8080 -v $(pwd)/mail_data:/data mailparser/app:latest
```

**That's it!** Open your browser to: http://localhost:8080

### Using Docker Compose (Recommended)

1. Download [docker-compose.yml](./docker-compose.yml)

2. Open Terminal/PowerShell in the same folder

3. Run:
   ```bash
   docker-compose up -d
   ```

4. Open browser to: http://localhost:8080

5. To stop:
   ```bash
   docker-compose down
   ```

**Benefits of Docker:**
- ✅ No Python installation needed
- ✅ Works identically on all operating systems
- ✅ Isolated from your system
- ✅ Easy to update (pull new image)
- ✅ Easy to uninstall (delete container)

---

## Cloud Deployment

**Access your email parser from anywhere, on any device!**

### Heroku (Free Tier Available)

1. Create account at [Heroku.com](https://heroku.com)

2. Install Heroku CLI:
   - Windows: Download from [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
   - Mac: `brew install heroku/brew/heroku`
   - Linux: `curl https://cli-assets.heroku.com/install.sh | sh`

3. Deploy with one command:
   ```bash
   # Clone the repository
   git clone https://github.com/your-repo/mail_parser.git
   cd mail_parser

   # Login to Heroku
   heroku login

   # Create and deploy
   heroku create my-mail-parser
   git push heroku main

   # Open in browser
   heroku open
   ```

**Free tier includes:**
- 550 dyno hours/month
- Custom domain support
- SSL certificates
- Automatic deployments

---

### Railway (Easiest Cloud Deploy)

1. Visit [Railway.app](https://railway.app)

2. Click "Deploy from GitHub"

3. Select mail_parser repository

4. Click "Deploy Now"

5. Wait 2-3 minutes

6. Click the generated URL

**That's it!** Railway handles everything automatically.

**Features:**
- $5 free credit/month
- Automatic HTTPS
- Custom domains
- Deploy in 1 click

---

### Render (Great Free Tier)

1. Visit [Render.com](https://render.com)

2. Click "New +" → "Web Service"

3. Connect your GitHub account

4. Select mail_parser repository

5. Configure:
   - Name: `mail-parser`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m mail_parser.cli serve`

6. Click "Create Web Service"

**Free tier includes:**
- 750 hours/month
- Custom domains
- Auto SSL
- Auto deploy on git push

---

## Troubleshooting

### Windows

**"Python not found"**
- Installer will download Python automatically
- Or download manually: [Python.org](https://python.org/downloads/)
- Make sure to check "Add Python to PATH"

**"Execution policy error"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**"Script blocked"**
- Right-click install_windows.ps1
- Click "Properties"
- Check "Unblock"
- Click OK

---

### macOS

**"Command not found: brew"**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**"Permission denied"**
```bash
chmod +x install_macos.sh
```

**"Unknown developer warning"**
- Right-click the script
- Click "Open With" → "Terminal"
- Click "Open" in warning dialog

---

### Linux

**"curl: command not found"**
```bash
# Ubuntu/Debian
sudo apt-get install curl

# Fedora
sudo dnf install curl
```

**"Permission denied"**
```bash
chmod +x install_linux.sh
```

---

### Docker

**"Docker daemon not running"**
- Open Docker Desktop
- Wait for it to start (whale icon in system tray)

**"Port 8080 already in use"**
- Change port: `-p 8081:8080` (use 8081 instead)

**"Cannot connect to Docker daemon"**
- Restart Docker Desktop
- Check Docker Desktop is running

---

## What Gets Installed?

All installers set up:

1. **Python 3.10+** (if not present)
2. **UV package manager** (fast Python package manager)
3. **Mail Parser** (the email parsing application)
4. **Dependencies** (all required libraries)
5. **Desktop shortcut** (for easy access)

**Total disk space:** ~500MB

**Installation location:**
- Windows: `C:\Users\YourName\mail_parser`
- Mac: `/Users/YourName/mail_parser`
- Linux: `/home/yourname/mail_parser`

---

## Using Mail Parser After Installation

### 1. Parse Your Email Export

**Easy way (Drag and Drop):**
- Drag your `.mbox` file onto the Mail Parser icon

**Command line way:**
```bash
mail-parser parse --mbox your_emails.mbox --output ./my_emails
```

### 2. Open the Dashboard

The installer creates shortcuts:

- **Windows:** Desktop icon "Mail Parser"
- **macOS:** Applications folder → Mail Parser
- **Linux:** Applications menu → Mail Parser

**Or open manually:**
- Navigate to output folder
- Double-click `index.html`

### 3. Browse Your Emails

Use the web dashboard to:
- 🔍 Search all emails
- 📁 Filter by sender
- 📅 Browse by date
- 💬 View conversations
- 📊 See statistics

---

## Updating Mail Parser

### Native Installation

**Windows:**
```powershell
cd C:\Users\YourName\mail_parser
git pull
uv pip install -e .
```

**Mac/Linux:**
```bash
cd ~/mail_parser
git pull
uv pip install -e .
```

### Docker

```bash
docker pull mailparser/app:latest
docker-compose up -d
```

### Cloud

**Heroku:**
```bash
git push heroku main
```

**Railway/Render:** Automatically updates on git push

---

## Uninstalling

### Windows

1. Run: `uninstall_windows.ps1` (in installation folder)
2. Or manually delete: `C:\Users\YourName\mail_parser`

### macOS

```bash
rm -rf ~/mail_parser
brew uninstall python@3.10  # if you want to remove Python
```

### Linux

```bash
rm -rf ~/mail_parser
sudo apt remove python3.10  # if you want to remove Python
```

### Docker

```bash
docker-compose down
docker rmi mailparser/app:latest
```

---

## Getting Help

### Common Questions

**Q: Is my email data safe?**
A: Yes! Everything runs locally on your computer. No data is sent to the cloud unless you choose cloud deployment.

**Q: Can I parse multiple mbox files?**
A: Yes! Run the parser multiple times with different output folders, or merge mbox files first.

**Q: Does this work with other email providers?**
A: Yes! Any email provider that exports to mbox format (Gmail, Outlook, Thunderbird, etc.)

**Q: How long does parsing take?**
A: Approximately 2,000 emails per minute. A 40,000 email archive takes about 20 minutes.

**Q: Can I use this without internet?**
A: Yes! The parser works completely offline. Internet only needed for Gmail API features (optional).

### Support

- 📖 Read the [full documentation](./README.md)
- 🐛 Report bugs: [GitHub Issues](https://github.com/your-repo/mail_parser/issues)
- 💬 Get help: [Discussions](https://github.com/your-repo/mail_parser/discussions)
- 📧 Email: support@example.com

---

## Next Steps

1. ✅ Install Mail Parser (pick method above)
2. 📥 Export your email (Google Takeout for Gmail)
3. 🔄 Run the parser on your mbox file
4. 🌐 Open the dashboard and explore!

**Happy email exploring!** 🎉
