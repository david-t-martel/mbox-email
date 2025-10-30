# Mail Parser - Windows One-Click Installer
# Installs Python, UV, and Mail Parser automatically
# Run with: .\install_windows.ps1

param(
    [string]$InstallPath = "$env:USERPROFILE\mail_parser",
    [switch]$SkipTest = $false
)

# Colors for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

# Banner
function Show-Banner {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                                                      ║" -ForegroundColor Cyan
    Write-Host "║          Mail Parser - Windows Installer            ║" -ForegroundColor Cyan
    Write-Host "║                                                      ║" -ForegroundColor Cyan
    Write-Host "║     High-Performance Gmail mbox Parser & Analyzer   ║" -ForegroundColor Cyan
    Write-Host "║                                                      ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

# Check if running as administrator
function Test-Administrator {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Step indicator
function Write-Step {
    param([string]$Message, [int]$Step, [int]$Total)
    Write-Host ""
    Write-Host "[$Step/$Total] $Message" -ForegroundColor $InfoColor
    Write-Host ("=" * 60) -ForegroundColor DarkGray
}

# Success message
function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor $SuccessColor
}

# Error message
function Write-Error-Message {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor $ErrorColor
}

# Info message
function Write-Info {
    param([string]$Message)
    Write-Host "→ $Message" -ForegroundColor $InfoColor
}

# Warning message
function Write-Warning-Message {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor $WarningColor
}

# Check Python installation
function Test-Python {
    try {
        $pythonVersion = & python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            if ($major -ge 3 -and $minor -ge 10) {
                Write-Success "Python $major.$minor found"
                return $true
            } else {
                Write-Warning-Message "Python $major.$minor found, but 3.10+ required"
                return $false
            }
        }
    } catch {
        Write-Warning-Message "Python not found"
        return $false
    }
    return $false
}

# Install Python using winget
function Install-Python {
    Write-Info "Installing Python 3.12..."

    # Try winget first (Windows 10/11)
    try {
        Write-Info "Attempting installation via winget..."
        winget install Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements

        # Refresh environment
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

        Write-Success "Python installed successfully"
        return $true
    } catch {
        Write-Warning-Message "Winget installation failed. Trying alternative method..."
    }

    # Fallback to chocolatey
    try {
        Write-Info "Attempting installation via Chocolatey..."
        if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
            Write-Info "Installing Chocolatey package manager..."
            Set-ExecutionPolicy Bypass -Scope Process -Force
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
            Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
        }

        choco install python312 -y
        refreshenv

        Write-Success "Python installed via Chocolatey"
        return $true
    } catch {
        Write-Error-Message "Automated installation failed."
        Write-Warning-Message "Please install Python manually from: https://www.python.org/downloads/"
        Write-Warning-Message "Make sure to check 'Add Python to PATH' during installation"
        return $false
    }
}

# Check UV installation
function Test-UV {
    try {
        $uvVersion = & uv --version 2>&1
        if ($uvVersion) {
            Write-Success "UV package manager found"
            return $true
        }
    } catch {
        Write-Warning-Message "UV not found"
        return $false
    }
    return $false
}

# Install UV
function Install-UV {
    Write-Info "Installing UV package manager..."

    try {
        # Install UV using the official installer
        Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -UseBasicParsing | Invoke-Expression

        # Refresh environment
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

        Write-Success "UV installed successfully"
        return $true
    } catch {
        Write-Error-Message "Failed to install UV: $_"
        return $false
    }
}

# Clone or download repository
function Get-Repository {
    param([string]$Path)

    Write-Info "Setting up Mail Parser in: $Path"

    # Create directory if it doesn't exist
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Success "Created directory: $Path"
    }

    # Check if git is available
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Write-Info "Cloning repository from GitHub..."
        try {
            git clone https://github.com/david-t-martel/mbox-email.git $Path 2>&1 | Out-Null
            Write-Success "Repository cloned"
            return $true
        } catch {
            Write-Warning-Message "Git clone failed, trying download..."
        }
    }

    # Fallback to download zip
    Write-Info "Downloading repository as ZIP..."
    try {
        $zipPath = "$env:TEMP\mail_parser.zip"
        Invoke-WebRequest -Uri "https://github.com/david-t-martel/mbox-email/archive/refs/heads/main.zip" -OutFile $zipPath

        Expand-Archive -Path $zipPath -DestinationPath $env:TEMP -Force
        Copy-Item -Path "$env:TEMP\mbox-email-main\*" -Destination $Path -Recurse -Force
        Remove-Item $zipPath

        Write-Success "Repository downloaded"
        return $true
    } catch {
        Write-Error-Message "Failed to download repository: $_"
        return $false
    }
}

# Install Mail Parser dependencies
function Install-MailParser {
    param([string]$Path)

    Write-Info "Installing Mail Parser and dependencies..."

    Push-Location $Path
    try {
        # Install using UV
        & uv pip install -e . 2>&1 | Out-Null
        Write-Success "Mail Parser installed"

        Pop-Location
        return $true
    } catch {
        Write-Error-Message "Failed to install Mail Parser: $_"
        Pop-Location
        return $false
    }
}

# Create desktop shortcut
function New-DesktopShortcut {
    param([string]$Path)

    Write-Info "Creating desktop shortcut..."

    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Mail Parser.lnk")
    $Shortcut.TargetPath = "powershell.exe"
    $Shortcut.Arguments = "-NoExit -Command `"cd '$Path'; Write-Host 'Mail Parser Ready!' -ForegroundColor Green`""
    $Shortcut.WorkingDirectory = $Path
    $Shortcut.IconLocation = "shell32.dll,43"
    $Shortcut.Description = "Mail Parser - Email Analysis Tool"
    $Shortcut.Save()

    Write-Success "Desktop shortcut created"
}

# Create batch launcher
function New-Launcher {
    param([string]$Path)

    Write-Info "Creating launcher script..."

    $launcherPath = Join-Path $Path "mail-parser-gui.bat"
    $launcherContent = @"
@echo off
title Mail Parser
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║          Mail Parser - Quick Start Menu             ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo [1] Parse mbox file
echo [2] Open dashboard
echo [3] Search emails
echo [4] View statistics
echo [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto parse
if "%choice%"=="2" goto dashboard
if "%choice%"=="3" goto search
if "%choice%"=="4" goto stats
if "%choice%"=="5" goto end

:parse
set /p mbox="Enter path to mbox file: "
set /p output="Enter output directory (default: .\output): "
if "%output%"=="" set output=.\output
uv run python -m mail_parser.cli parse --mbox "%mbox%" --output "%output%" --workers 8
goto menu

:dashboard
start .\output\index.html
goto menu

:search
set /p query="Enter search query: "
uv run python -m mail_parser.cli search --database .\output\email_index.db --query "%query%"
goto menu

:stats
uv run python -m mail_parser.cli stats --database .\output\email_index.db
goto menu

:menu
echo.
pause
cls
goto start

:end
exit
"@

    Set-Content -Path $launcherPath -Value $launcherContent
    Write-Success "Launcher created: $launcherPath"
}

# Run test
function Test-Installation {
    param([string]$Path)

    Write-Info "Running installation test..."

    Push-Location $Path
    try {
        # Create test mbox
        $testMbox = Join-Path $env:TEMP "test.mbox"
        $testOutput = Join-Path $env:TEMP "test_output"

        # Create simple test mbox file
        $testEmail = @"
From test@example.com Mon Jan 01 00:00:00 2024
From: Test User <test@example.com>
To: recipient@example.com
Subject: Test Email
Date: Mon, 01 Jan 2024 00:00:00 +0000

This is a test email.
"@
        Set-Content -Path $testMbox -Value $testEmail

        # Run parser
        & uv run python -m mail_parser.cli parse --mbox $testMbox --output $testOutput --limit 1 2>&1 | Out-Null

        # Check if output was created
        if (Test-Path "$testOutput\index.html") {
            Write-Success "Installation test passed"

            # Cleanup
            Remove-Item $testMbox -Force
            Remove-Item $testOutput -Recurse -Force

            Pop-Location
            return $true
        } else {
            Write-Error-Message "Installation test failed"
            Pop-Location
            return $false
        }
    } catch {
        Write-Error-Message "Test failed: $_"
        Pop-Location
        return $false
    }
}

# Main installation flow
function Start-Installation {
    Show-Banner

    $totalSteps = 8
    $currentStep = 0

    # Step 1: Check administrator
    $currentStep++
    Write-Step "Checking permissions" $currentStep $totalSteps

    if (-not (Test-Administrator)) {
        Write-Warning-Message "Not running as administrator. Some installations may require elevation."
        Write-Info "Right-click PowerShell and select 'Run as Administrator' for best results."
        $continue = Read-Host "Continue anyway? (Y/N)"
        if ($continue -ne "Y" -and $continue -ne "y") {
            Write-Error-Message "Installation cancelled"
            exit 1
        }
    } else {
        Write-Success "Running with administrator privileges"
    }

    # Step 2: Check/Install Python
    $currentStep++
    Write-Step "Checking Python installation" $currentStep $totalSteps

    if (-not (Test-Python)) {
        $install = Read-Host "Python 3.10+ not found. Install now? (Y/N)"
        if ($install -eq "Y" -or $install -eq "y") {
            if (-not (Install-Python)) {
                Write-Error-Message "Python installation failed. Please install manually."
                exit 1
            }
        } else {
            Write-Error-Message "Python is required. Exiting."
            exit 1
        }
    }

    # Step 3: Check/Install UV
    $currentStep++
    Write-Step "Checking UV package manager" $currentStep $totalSteps

    if (-not (Test-UV)) {
        Write-Info "UV not found. Installing..."
        if (-not (Install-UV)) {
            Write-Error-Message "UV installation failed"
            exit 1
        }
    }

    # Step 4: Get repository
    $currentStep++
    Write-Step "Downloading Mail Parser" $currentStep $totalSteps

    if (-not (Get-Repository -Path $InstallPath)) {
        Write-Error-Message "Failed to download Mail Parser"
        exit 1
    }

    # Step 5: Install dependencies
    $currentStep++
    Write-Step "Installing dependencies" $currentStep $totalSteps

    if (-not (Install-MailParser -Path $InstallPath)) {
        Write-Error-Message "Failed to install dependencies"
        exit 1
    }

    # Step 6: Create shortcuts
    $currentStep++
    Write-Step "Creating shortcuts and launchers" $currentStep $totalSteps

    New-DesktopShortcut -Path $InstallPath
    New-Launcher -Path $InstallPath

    # Step 7: Test installation
    $currentStep++
    Write-Step "Testing installation" $currentStep $totalSteps

    if (-not $SkipTest) {
        if (-not (Test-Installation -Path $InstallPath)) {
            Write-Warning-Message "Installation test failed, but Mail Parser may still work"
        }
    } else {
        Write-Info "Skipping installation test"
    }

    # Step 8: Complete
    $currentStep++
    Write-Step "Installation complete!" $currentStep $totalSteps

    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                      ║" -ForegroundColor Green
    Write-Host "║         Mail Parser Installed Successfully!         ║" -ForegroundColor Green
    Write-Host "║                                                      ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""

    Write-Info "Installation location: $InstallPath"
    Write-Info "Desktop shortcut created"
    Write-Info "Launcher script: $InstallPath\mail-parser-gui.bat"
    Write-Host ""

    Write-Host "Quick Start:" -ForegroundColor Cyan
    Write-Host "  1. Get your Gmail mbox file (Google Takeout)" -ForegroundColor White
    Write-Host "  2. Double-click desktop shortcut 'Mail Parser'" -ForegroundColor White
    Write-Host "  3. Run: uv run python -m mail_parser.cli parse --mbox your_file.mbox --output .\output" -ForegroundColor White
    Write-Host "  4. Open: .\output\index.html" -ForegroundColor White
    Write-Host ""

    $openDocs = Read-Host "Open documentation now? (Y/N)"
    if ($openDocs -eq "Y" -or $openDocs -eq "y") {
        Start-Process "https://github.com/david-t-martel/mbox-email"
    }

    Write-Host ""
    Write-Host "Thank you for installing Mail Parser!" -ForegroundColor Green
    Write-Host ""
}

# Run installation
try {
    Start-Installation
} catch {
    Write-Error-Message "Installation failed: $_"
    Write-Host ""
    Write-Host "Please report this issue at:" -ForegroundColor Yellow
    Write-Host "https://github.com/david-t-martel/mbox-email/issues" -ForegroundColor Yellow
    exit 1
}
