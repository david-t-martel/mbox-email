#!/usr/bin/env bash

# Mail Parser - Linux One-Click Installer
# Supports Ubuntu, Debian, Fedora, CentOS, Arch
# Run with: ./install_linux.sh

set -e  # Exit on error

# Configuration
INSTALL_PATH="$HOME/mail_parser"
SKIP_TEST=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                      ║${NC}"
    echo -e "${CYAN}║          Mail Parser - Linux Installer              ║${NC}"
    echo -e "${CYAN}║                                                      ║${NC}"
    echo -e "${CYAN}║     High-Performance Gmail mbox Parser & Analyzer   ║${NC}"
    echo -e "${CYAN}║                                                      ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Step indicator
write_step() {
    local message=$1
    local step=$2
    local total=$3

    echo ""
    echo -e "${CYAN}[$step/$total] $message${NC}"
    echo -e "${BLUE}$(printf '=%.0s' {1..60})${NC}"
}

# Success message
write_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Error message
write_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Info message
write_info() {
    echo -e "${CYAN}→ $1${NC}"
}

# Warning message
write_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        echo "$DISTRIB_ID" | tr '[:upper:]' '[:lower:]'
    else
        echo "unknown"
    fi
}

# Check if running with sudo/root
check_sudo() {
    if [ "$EUID" -eq 0 ]; then
        return 0
    elif command_exists sudo; then
        return 0
    else
        return 1
    fi
}

# Check Python installation
check_python() {
    if command_exists python3; then
        local version=$(python3 --version 2>&1 | awk '{print $2}')
        local major=$(echo "$version" | cut -d. -f1)
        local minor=$(echo "$version" | cut -d. -f2)

        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            write_success "Python $version found"
            return 0
        else
            write_warning "Python $version found, but 3.10+ required"
            return 1
        fi
    else
        write_warning "Python not found"
        return 1
    fi
}

# Install Python based on distro
install_python() {
    local distro=$(detect_distro)

    write_info "Installing Python 3.12 for $distro..."

    case "$distro" in
        ubuntu|debian|linuxmint|pop)
            write_info "Using apt package manager..."
            sudo apt-get update
            sudo apt-get install -y software-properties-common
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y python3.12 python3.12-venv python3.12-dev python3-pip
            sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
            ;;

        fedora|centos|rhel)
            write_info "Using dnf/yum package manager..."
            sudo dnf install -y python3.12 python3.12-devel python3-pip || \
            sudo yum install -y python3.12 python3.12-devel python3-pip
            ;;

        arch|manjaro)
            write_info "Using pacman package manager..."
            sudo pacman -Sy --noconfirm python python-pip
            ;;

        opensuse*)
            write_info "Using zypper package manager..."
            sudo zypper install -y python312 python312-pip
            ;;

        *)
            write_error "Unsupported distribution: $distro"
            write_info "Please install Python 3.10+ manually"
            return 1
            ;;
    esac

    if check_python; then
        write_success "Python installed successfully"
        return 0
    else
        write_error "Failed to install Python"
        return 1
    fi
}

# Check UV installation
check_uv() {
    if command_exists uv; then
        write_success "UV package manager found"
        return 0
    else
        write_warning "UV not found"
        return 1
    fi
}

# Install UV
install_uv() {
    write_info "Installing UV package manager..."

    if curl -fsSL https://astral.sh/uv/install.sh | sh; then
        # Add UV to PATH
        export PATH="$HOME/.cargo/bin:$PATH"

        write_success "UV installed successfully"
        return 0
    else
        write_error "Failed to install UV"
        return 1
    fi
}

# Install system dependencies
install_system_deps() {
    local distro=$(detect_distro)

    write_info "Installing system dependencies..."

    case "$distro" in
        ubuntu|debian|linuxmint|pop)
            sudo apt-get install -y git curl wget unzip build-essential libssl-dev libffi-dev
            ;;

        fedora|centos|rhel)
            sudo dnf install -y git curl wget unzip gcc gcc-c++ make openssl-devel libffi-devel || \
            sudo yum install -y git curl wget unzip gcc gcc-c++ make openssl-devel libffi-devel
            ;;

        arch|manjaro)
            sudo pacman -S --noconfirm git curl wget unzip base-devel openssl
            ;;

        opensuse*)
            sudo zypper install -y git curl wget unzip gcc gcc-c++ make openssl-devel libffi-devel
            ;;

        *)
            write_warning "Unknown distribution, skipping system dependencies"
            ;;
    esac

    write_success "System dependencies installed"
}

# Clone or download repository
get_repository() {
    local path=$1

    write_info "Setting up Mail Parser in: $path"

    # Create directory if it doesn't exist
    if [ ! -d "$path" ]; then
        mkdir -p "$path"
        write_success "Created directory: $path"
    fi

    # Check if git is available
    if command_exists git; then
        write_info "Cloning repository from GitHub..."
        if git clone https://github.com/david-t-martel/mbox-email.git "$path" 2>/dev/null; then
            write_success "Repository cloned"
            return 0
        else
            write_warning "Git clone failed, trying download..."
        fi
    fi

    # Fallback to download zip
    write_info "Downloading repository as ZIP..."
    local temp_dir=$(mktemp -d)
    if curl -L "https://github.com/david-t-martel/mbox-email/archive/refs/heads/main.zip" -o "$temp_dir/mail_parser.zip" && \
       unzip -q "$temp_dir/mail_parser.zip" -d "$temp_dir" && \
       cp -r "$temp_dir/mbox-email-main/"* "$path/"; then
        rm -rf "$temp_dir"
        write_success "Repository downloaded"
        return 0
    else
        rm -rf "$temp_dir"
        write_error "Failed to download repository"
        return 1
    fi
}

# Install Mail Parser dependencies
install_mail_parser() {
    local path=$1

    write_info "Installing Mail Parser and dependencies..."

    cd "$path" || return 1

    if uv pip install -e . >/dev/null 2>&1; then
        write_success "Mail Parser installed"
        return 0
    else
        write_error "Failed to install Mail Parser"
        return 1
    fi
}

# Create desktop entry
create_desktop_entry() {
    local path=$1

    write_info "Creating desktop application entry..."

    # Create launcher script
    local launcher_path="$path/mail-parser-gui.sh"

    cat > "$launcher_path" << 'EOF'
#!/usr/bin/env bash

# Mail Parser GUI Launcher
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

clear

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║          Mail Parser - Quick Start Menu             ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "[1] Parse mbox file"
echo "[2] Open dashboard"
echo "[3] Search emails"
echo "[4] View statistics"
echo "[5] Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        read -p "Enter path to mbox file: " mbox
        read -p "Enter output directory (default: ./output): " output
        output=${output:-./output}
        uv run python -m mail_parser.cli parse --mbox "$mbox" --output "$output" --workers 8
        ;;
    2)
        xdg-open ./output/index.html 2>/dev/null || \
        firefox ./output/index.html 2>/dev/null || \
        chromium ./output/index.html 2>/dev/null || \
        google-chrome ./output/index.html 2>/dev/null
        ;;
    3)
        read -p "Enter search query: " query
        uv run python -m mail_parser.cli search --database ./output/email_index.db --query "$query"
        ;;
    4)
        uv run python -m mail_parser.cli stats --database ./output/email_index.db
        ;;
    5)
        exit 0
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

read -p "Press Enter to continue..."
exec "$0"
EOF

    chmod +x "$launcher_path"
    write_success "Launcher created: $launcher_path"

    # Create .desktop file
    local desktop_file="$HOME/.local/share/applications/mail-parser.desktop"
    mkdir -p "$HOME/.local/share/applications"

    cat > "$desktop_file" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Mail Parser
Comment=High-Performance Gmail mbox Parser & Analyzer
Exec=x-terminal-emulator -e "$launcher_path"
Icon=mail-message-new
Terminal=true
Categories=Office;Email;Utility;
Keywords=email;mbox;parser;gmail;
EOF

    write_success "Desktop entry created: $desktop_file"

    # Create desktop shortcut
    if [ -d "$HOME/Desktop" ]; then
        cp "$desktop_file" "$HOME/Desktop/mail-parser.desktop"
        chmod +x "$HOME/Desktop/mail-parser.desktop"
        write_success "Desktop shortcut created"
    fi
}

# Add to shell profile
add_to_profile() {
    local path=$1

    write_info "Adding Mail Parser to shell profile..."

    # Detect shell
    local shell_rc=""
    if [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    fi

    if [ -n "$shell_rc" ] && [ -f "$shell_rc" ]; then
        # Add alias for mail-parser
        if ! grep -q "alias mail-parser=" "$shell_rc" 2>/dev/null; then
            echo "" >> "$shell_rc"
            echo "# Mail Parser" >> "$shell_rc"
            echo "alias mail-parser='cd $path && uv run python -m mail_parser.cli'" >> "$shell_rc"
            echo "export PATH=\"\$HOME/.cargo/bin:\$PATH\"" >> "$shell_rc"
            write_success "Added mail-parser alias to $shell_rc"
        fi
    fi
}

# Run test
test_installation() {
    local path=$1

    write_info "Running installation test..."

    cd "$path" || return 1

    # Create test mbox
    local test_mbox="/tmp/test.mbox"
    local test_output="/tmp/test_output"

    # Create simple test mbox file
    cat > "$test_mbox" << 'EOF'
From test@example.com Mon Jan 01 00:00:00 2024
From: Test User <test@example.com>
To: recipient@example.com
Subject: Test Email
Date: Mon, 01 Jan 2024 00:00:00 +0000

This is a test email.
EOF

    # Run parser
    if uv run python -m mail_parser.cli parse --mbox "$test_mbox" --output "$test_output" --limit 1 >/dev/null 2>&1; then
        # Check if output was created
        if [ -f "$test_output/index.html" ]; then
            write_success "Installation test passed"

            # Cleanup
            rm -f "$test_mbox"
            rm -rf "$test_output"

            return 0
        fi
    fi

    write_error "Installation test failed"
    return 1
}

# Main installation flow
main() {
    show_banner

    local total_steps=10
    local current_step=0

    # Step 1: Check sudo access
    ((current_step++))
    write_step "Checking system permissions" $current_step $total_steps

    if ! check_sudo; then
        write_error "This script requires sudo access for package installation"
        write_info "Please ensure sudo is installed and you have sudo privileges"
        exit 1
    fi
    write_success "Sudo access confirmed"

    # Step 2: Detect distribution
    ((current_step++))
    write_step "Detecting Linux distribution" $current_step $total_steps

    local distro=$(detect_distro)
    write_success "Detected: $distro"

    # Step 3: Install system dependencies
    ((current_step++))
    write_step "Installing system dependencies" $current_step $total_steps

    install_system_deps

    # Step 4: Check/Install Python
    ((current_step++))
    write_step "Checking Python installation" $current_step $total_steps

    if ! check_python; then
        read -p "Python 3.10+ not found. Install now? (Y/n): " install
        install=${install:-Y}
        if [[ $install =~ ^[Yy]$ ]]; then
            if ! install_python; then
                write_error "Python installation failed. Please install manually."
                exit 1
            fi
        else
            write_error "Python is required. Exiting."
            exit 1
        fi
    fi

    # Step 5: Check/Install UV
    ((current_step++))
    write_step "Checking UV package manager" $current_step $total_steps

    if ! check_uv; then
        write_info "UV not found. Installing..."
        if ! install_uv; then
            write_error "UV installation failed"
            exit 1
        fi
    fi

    # Step 6: Get repository
    ((current_step++))
    write_step "Downloading Mail Parser" $current_step $total_steps

    if ! get_repository "$INSTALL_PATH"; then
        write_error "Failed to download Mail Parser"
        exit 1
    fi

    # Step 7: Install dependencies
    ((current_step++))
    write_step "Installing dependencies" $current_step $total_steps

    if ! install_mail_parser "$INSTALL_PATH"; then
        write_error "Failed to install dependencies"
        exit 1
    fi

    # Step 8: Create desktop entry
    ((current_step++))
    write_step "Creating application launchers" $current_step $total_steps

    create_desktop_entry "$INSTALL_PATH"

    # Step 9: Add to shell profile
    ((current_step++))
    write_step "Configuring shell environment" $current_step $total_steps

    add_to_profile "$INSTALL_PATH"

    # Step 10: Test installation
    ((current_step++))
    write_step "Testing installation" $current_step $total_steps

    if [ "$SKIP_TEST" != "true" ]; then
        if ! test_installation "$INSTALL_PATH"; then
            write_warning "Installation test failed, but Mail Parser may still work"
        fi
    else
        write_info "Skipping installation test"
    fi

    # Complete
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                      ║${NC}"
    echo -e "${GREEN}║         Mail Parser Installed Successfully!         ║${NC}"
    echo -e "${GREEN}║                                                      ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
    echo ""

    write_info "Installation location: $INSTALL_PATH"
    write_info "Desktop application: Mail Parser (in Applications menu)"
    write_info "Desktop shortcut created"
    write_info "Launcher script: $INSTALL_PATH/mail-parser-gui.sh"
    echo ""

    echo -e "${CYAN}Quick Start:${NC}"
    echo "  1. Get your Gmail mbox file (Google Takeout)"
    echo "  2. Open 'Mail Parser' from Applications menu or Desktop"
    echo "  3. Or use command: mail-parser parse --mbox your_file.mbox --output ./output"
    echo "  4. Open: ./output/index.html"
    echo ""

    echo -e "${YELLOW}Note: Restart your terminal or run 'source ~/.bashrc' to use the mail-parser command${NC}"
    echo ""

    read -p "Open documentation now? (Y/n): " open_docs
    open_docs=${open_docs:-Y}
    if [[ $open_docs =~ ^[Yy]$ ]]; then
        xdg-open "https://github.com/david-t-martel/mbox-email" 2>/dev/null || \
        firefox "https://github.com/david-t-martel/mbox-email" 2>/dev/null || \
        chromium "https://github.com/david-t-martel/mbox-email" 2>/dev/null || \
        google-chrome "https://github.com/david-t-martel/mbox-email" 2>/dev/null
    fi

    echo ""
    write_success "Thank you for installing Mail Parser!"
    echo ""
}

# Run installation
main "$@"
