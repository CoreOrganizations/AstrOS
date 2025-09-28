# Ubuntu ISO Customization - Complete Technical Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Method 1: Using Live-Build (Recommended)](#method-1-using-live-build-recommended)
4. [Method 2: Using Cubic GUI Tool](#method-2-using-cubic-gui-tool)
5. [Method 3: Manual Chroot Method](#method-3-manual-chroot-method)
6. [AstrOS Specific Customizations](#astros-specific-customizations)
7. [Build Automation](#build-automation)
8. [Testing and Validation](#testing-and-validation)
9. [Distribution and Updates](#distribution-and-updates)

---

## Overview

This guide explains how to create a custom Ubuntu ISO with AstrOS components pre-installed. We'll cover multiple methods, from beginner-friendly GUI tools to advanced automated build systems.

### What We're Doing
- Starting with Ubuntu 24.04 LTS base
- Adding AstrOS Python agent and dependencies  
- Installing AI models and plugins
- Customizing desktop environment
- Creating bootable ISO with everything pre-configured

### Key Benefits
- Users get working AstrOS without complex installation
- Consistent experience across all installations
- Easy distribution and sharing
- Professional appearance for the project

---

## Prerequisites

### Development Machine Requirements
```bash
# Minimum requirements
- Ubuntu 24.04 LTS (recommended) or 22.04 LTS
- 8GB RAM (16GB recommended for faster builds)
- 50GB free disk space
- Fast internet connection
- Admin/sudo access

# Install essential tools
sudo apt update
sudo apt install -y \
    debootstrap \
    squashfs-tools \
    genisoimage \
    syslinux-utils \
    isolinux \
    live-build \
    ubuntu-dev-tools \
    git \
    curl \
    wget
```

### Understanding the Process
```
Base Ubuntu ISO → Extract → Modify → Add AstrOS → Repackage → Test → Distribute
```

---

## Method 1: Using Live-Build (Recommended)

Live-build is Ubuntu's official tool for creating custom distributions.

### Step 1: Setup Live-Build Environment
```bash
# Create build directory
mkdir -p ~/astros-build
cd ~/astros-build

# Initialize live-build configuration
lb config \
    --distribution noble \
    --archive-areas "main restricted universe multiverse" \
    --apt-recommends false \
    --apt-suggests false \
    --binary-images iso-hybrid \
    --bootappend-live "boot=live components quiet splash" \
    --debian-installer false \
    --iso-application "AstrOS" \
    --iso-publisher "AstrOS Project" \
    --iso-volume "AstrOS-24.04-amd64"
```

### Step 2: Customize Package Selection
```bash
# Create package lists
mkdir -p config/package-lists

# Essential desktop packages
cat > config/package-lists/desktop.list.chroot << 'EOF'
ubuntu-desktop-minimal
gnome-shell
gnome-terminal
firefox
libreoffice
python3.12
python3-pip
python3-venv
git
curl
vim
EOF

# AstrOS specific packages
cat > config/package-lists/astros.list.chroot << 'EOF'
python3-dev
python3-setuptools
build-essential
portaudio19-dev
espeak-ng
alsa-utils
pulseaudio
EOF
```

### Step 3: Add AstrOS Components
```bash
# Create hooks directory for custom scripts
mkdir -p config/hooks/live

# Create hook to install AstrOS
cat > config/hooks/live/0100-install-astros.hook.chroot << 'EOF'
#!/bin/bash
set -e

# Install Python dependencies
pip3 install --system \
    fastapi \
    uvicorn \
    transformers \
    torch \
    speechrecognition \
    pyttsx3 \
    openai

# Clone and install AstrOS agent
cd /opt
git clone https://github.com/CoreOrganizations/AstrOS.git astros
cd astros
python3 -m pip install -e .

# Create systemd service
cat > /etc/systemd/system/astros-agent.service << 'SERVICE'
[Unit]
Description=AstrOS AI Agent
After=network.target sound.target

[Service]
Type=simple
User=astros
Group=astros
WorkingDirectory=/opt/astros
ExecStart=/usr/bin/python3 -m astros.agent
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Create AstrOS user
useradd -r -s /bin/false astros
chown -R astros:astros /opt/astros

# Enable service
systemctl enable astros-agent.service
EOF

chmod +x config/hooks/live/0100-install-astros.hook.chroot
```

### Step 4: Desktop Customization
```bash
# Create desktop customization hook
cat > config/hooks/live/0200-customize-desktop.hook.chroot << 'EOF'
#!/bin/bash
set -e

# Install GNOME Shell extension for AstrOS
mkdir -p /usr/share/gnome-shell/extensions/astros@astros.org
cat > /usr/share/gnome-shell/extensions/astros@astros.org/metadata.json << 'META'
{
  "name": "AstrOS Integration",
  "description": "AI assistant integration for GNOME Shell",
  "uuid": "astros@astros.org",
  "shell-version": ["42", "43", "44"],
  "version": 1
}
META

# Set default wallpaper and theme
mkdir -p /usr/share/astros/wallpapers
# Add AstrOS wallpaper here

# Configure default settings
mkdir -p /etc/dconf/db/site.d
cat > /etc/dconf/db/site.d/00-astros-defaults << 'DCONF'
[org/gnome/desktop/background]
picture-uri='file:///usr/share/astros/wallpapers/default.jpg'

[org/gnome/shell]
enabled-extensions=['astros@astros.org']

[org/gnome/desktop/interface]
gtk-theme='Adwaita-dark'
icon-theme='Adwaita'
DCONF

dconf update
EOF

chmod +x config/hooks/live/0200-customize-desktop.hook.chroot
```

### Step 5: Build the ISO
```bash
# Build the custom ISO
sudo lb build

# The ISO will be created as live-image-amd64.hybrid.iso
# Rename it for distribution
mv live-image-amd64.hybrid.iso astros-24.04-amd64.iso
```

---

## Method 2: Using Cubic GUI Tool

Cubic provides a user-friendly GUI for ISO customization.

### Step 1: Install Cubic
```bash
sudo apt-add-repository universe
sudo apt-add-repository ppa:cubic-wizard/release
sudo apt update
sudo apt install cubic
```

### Step 2: Using Cubic
```bash
# Launch Cubic
cubic

# Follow the GUI wizard:
# 1. Select original Ubuntu 24.04 ISO
# 2. Choose project directory
# 3. Enter custom ISO information
# 4. Modify the live environment
# 5. Test in virtual environment
# 6. Generate custom ISO
```

### Step 3: Customization in Cubic Terminal
```bash
# Inside Cubic's chroot environment
# Install AstrOS components
apt update
apt install -y python3-pip python3-venv build-essential

# Install AstrOS
cd /opt
git clone https://github.com/CoreOrganizations/AstrOS.git astros
cd astros
pip3 install -r requirements.txt
python3 setup.py install

# Configure services
systemctl enable astros-agent.service
```

---

## Method 3: Manual Chroot Method

For maximum control and understanding.

### Step 1: Extract Original ISO
```bash
# Create working directory
mkdir -p ~/astros-iso/{extract,edit,new}
cd ~/astros-iso

# Download Ubuntu 24.04 LTS ISO
wget https://releases.ubuntu.com/24.04/ubuntu-24.04-desktop-amd64.iso

# Mount and extract ISO
sudo mount -o loop ubuntu-24.04-desktop-amd64.iso extract/
sudo cp -rT extract/ edit/
sudo umount extract/
```

### Step 2: Extract and Modify SquashFS
```bash
# Extract the main filesystem
cd edit
sudo unsquashfs casper/filesystem.squashfs
sudo mv squashfs-root filesystem

# Prepare chroot environment
sudo cp /etc/resolv.conf filesystem/etc/
sudo cp /etc/hosts filesystem/etc/

# Bind mount necessary filesystems
sudo mount --bind /dev filesystem/dev
sudo mount --bind /proc filesystem/proc
sudo mount --bind /sys filesystem/sys
sudo mount --bind /dev/pts filesystem/dev/pts
```

### Step 3: Customize in Chroot
```bash
# Enter chroot environment
sudo chroot filesystem /bin/bash

# Update package lists
apt update

# Install AstrOS dependencies
apt install -y \
    python3.12 \
    python3-pip \
    python3-venv \
    build-essential \
    git \
    curl

# Install AstrOS
cd /opt
git clone https://github.com/CoreOrganizations/AstrOS.git astros
cd astros
pip3 install -r requirements.txt
python3 setup.py install

# Configure system
systemctl enable astros-agent.service

# Clean up
apt autoremove -y
apt autoclean
rm -rf /tmp/*
rm -rf /var/lib/apt/lists/*

# Exit chroot
exit
```

### Step 4: Rebuild SquashFS and ISO
```bash
# Unmount bind mounts
sudo umount filesystem/dev/pts filesystem/dev filesystem/proc filesystem/sys

# Clean chroot environment
sudo rm filesystem/etc/resolv.conf filesystem/etc/hosts

# Create new squashfs
sudo mksquashfs filesystem casper/filesystem.squashfs -comp xz -e boot

# Update filesystem size
printf $(sudo du -sx --block-size=1 filesystem | cut -f1) > casper/filesystem.size

# Calculate MD5 checksums
cd new
sudo find . -type f -print0 | xargs -0 md5sum | grep -v isolinux/boot.cat > md5sum.txt

# Create new ISO
sudo genisoimage \
    -rational-rock \
    -volid "AstrOS 24.04 LTS" \
    -cache-inodes \
    -joliet \
    -hfs \
    -full-iso9660-filenames \
    -b isolinux/isolinux.bin \
    -c isolinux/boot.cat \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    -eltorito-alt-boot \
    -e boot/grub/efi.img \
    -no-emul-boot \
    -append_partition 2 0xef boot/grub/efi.img \
    -o ../astros-24.04-amd64.iso \
    .
```

---

## AstrOS Specific Customizations

### Pre-installed AI Models
```bash
# Download and install local AI models
mkdir -p /opt/astros/models

# Download lightweight models for offline operation
python3 -c "
from transformers import pipeline
nlp = pipeline('text-classification', model='distilbert-base-uncased')
nlp.save_pretrained('/opt/astros/models/intent-classifier')
"
```

### Default Configuration
```yaml
# /etc/astros/config.yaml
agent:
  name: "AstrOS Assistant"
  voice_enabled: true
  local_models: true
  
ai:
  provider: "local"  # Start with local models
  fallback: "openai"  # Allow user to configure API keys
  
plugins:
  enabled:
    - file_management
    - system_control
    - development_tools
  
privacy:
  data_retention: 30  # days
  local_processing: true
  telemetry: false  # opt-in only
```

### Desktop Integration
```javascript
// GNOME Shell extension for AstrOS
const Main = imports.ui.main;
const PanelMenu = imports.ui.panelMenu;

class AstrOSIndicator extends PanelMenu.Button {
    _init() {
        super._init(0.0, 'AstrOS');
        
        // Add AI assistant indicator to top panel
        this.add_child(new St.Icon({
            icon_name: 'microphone-symbolic',
            style_class: 'system-status-icon'
        }));
        
        // Connect to AstrOS agent via D-Bus
        this._proxy = new Gio.DBusProxy.makeProxyWrapper(AstrOSInterface);
    }
}
```

---

## Build Automation

### GitHub Actions Workflow
```yaml
# .github/workflows/build-iso.yml
name: Build AstrOS ISO

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  
  pull_request:
    branches: [main]

jobs:
  build-iso:
    runs-on: ubuntu-24.04
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup build environment
      run: |
        sudo apt update
        sudo apt install -y live-build debootstrap squashfs-tools
        
    - name: Configure live-build
      run: |
        lb config \
          --distribution noble \
          --binary-images iso-hybrid \
          --iso-application "AstrOS" \
          --iso-volume "AstrOS-${{ github.ref_name }}"
          
    - name: Add AstrOS packages
      run: |
        mkdir -p config/hooks/live
        cp scripts/install-astros.hook.chroot config/hooks/live/
        
    - name: Build ISO
      run: |
        sudo lb build
        
    - name: Test ISO
      run: |
        ./scripts/test-iso.sh live-image-amd64.hybrid.iso
        
    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: astros-iso-${{ github.sha }}
        path: live-image-amd64.hybrid.iso
        
    - name: Create release
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: live-image-amd64.hybrid.iso
        name: AstrOS ${{ github.ref_name }}
        draft: false
        prerelease: contains(github.ref, 'alpha') || contains(github.ref, 'beta')
```

### Local Build Script
```bash
#!/bin/bash
# scripts/build-iso.sh

set -e

BUILD_DIR="build"
VERSION="${1:-dev}"
ARCH="${2:-amd64}"

echo "Building AstrOS ISO v${VERSION} for ${ARCH}"

# Clean previous builds
rm -rf ${BUILD_DIR}
mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}

# Configure live-build
lb config \
    --distribution noble \
    --archive-areas "main restricted universe multiverse" \
    --binary-images iso-hybrid \
    --iso-application "AstrOS" \
    --iso-publisher "AstrOS Project" \
    --iso-volume "AstrOS-${VERSION}-${ARCH}"

# Copy configuration
cp -r ../config/* config/

# Build ISO
sudo lb build

# Rename output
mv live-image-${ARCH}.hybrid.iso ../astros-${VERSION}-${ARCH}.iso

echo "Build complete: astros-${VERSION}-${ARCH}.iso"
```

---

## Testing and Validation

### Automated Testing
```bash
#!/bin/bash
# scripts/test-iso.sh

ISO_FILE="$1"

if [ ! -f "$ISO_FILE" ]; then
    echo "ISO file not found: $ISO_FILE"
    exit 1
fi

echo "Testing ISO: $ISO_FILE"

# Test 1: ISO integrity
echo "Checking ISO integrity..."
if ! file "$ISO_FILE" | grep -q "ISO 9660"; then
    echo "❌ Invalid ISO format"
    exit 1
fi
echo "✅ ISO format valid"

# Test 2: Boot test with QEMU
echo "Testing boot process..."
timeout 300 qemu-system-x86_64 \
    -m 2048 \
    -cdrom "$ISO_FILE" \
    -boot d \
    -nographic \
    -serial stdio \
    -vnc :1 &

QEMU_PID=$!
sleep 120  # Wait for boot

if kill -0 $QEMU_PID 2>/dev/null; then
    echo "✅ Boot test successful"
    kill $QEMU_PID
else
    echo "❌ Boot test failed"
    exit 1
fi

# Test 3: Check AstrOS components
echo "Testing AstrOS components..."
# Mount ISO and check for AstrOS files
mkdir -p /tmp/iso-test
sudo mount -o loop "$ISO_FILE" /tmp/iso-test

if [ -f "/tmp/iso-test/casper/filesystem.squashfs" ]; then
    echo "✅ SquashFS found"
    
    # Extract and check for AstrOS
    sudo unsquashfs -q -d /tmp/squashfs-test /tmp/iso-test/casper/filesystem.squashfs
    
    if [ -d "/tmp/squashfs-test/opt/astros" ]; then
        echo "✅ AstrOS installation found"
    else
        echo "❌ AstrOS installation missing"
        exit 1
    fi
    
    sudo rm -rf /tmp/squashfs-test
else
    echo "❌ SquashFS not found"
    exit 1
fi

sudo umount /tmp/iso-test
rmdir /tmp/iso-test

echo "✅ All tests passed"
```

### Manual Testing Checklist
```markdown
## AstrOS ISO Testing Checklist

### Boot Testing
- [ ] ISO boots successfully from USB
- [ ] ISO boots successfully from DVD
- [ ] Live environment loads without errors
- [ ] Desktop environment appears correctly
- [ ] AstrOS branding visible

### AstrOS Functionality
- [ ] AstrOS agent service starts automatically
- [ ] Voice input working (if microphone available)
- [ ] Text input processing working
- [ ] Basic commands execute successfully
- [ ] Plugin system loads correctly

### System Integration
- [ ] Network connection works
- [ ] Audio system functional
- [ ] Graphics drivers loaded
- [ ] USB devices recognized
- [ ] Wireless hardware detected

### Installation Testing
- [ ] Installation to hard drive works
- [ ] Installed system boots correctly
- [ ] AstrOS functionality preserved after installation
- [ ] Updates work correctly
```

---

## Distribution and Updates

### Release Process
```bash
# 1. Version tagging
git tag -a v1.0.0 -m "AstrOS v1.0.0 stable release"
git push origin v1.0.0

# 2. Automated build triggers
# GitHub Actions builds and uploads ISO

# 3. Release announcement
# Create GitHub release with changelog
# Update website download links
# Announce on social media and forums

# 4. Mirror distribution
# Upload to multiple mirrors for reliability
# Create torrent for peer-to-peer distribution
```

### Update System
```python
# astros/updates.py
class UpdateManager:
    def __init__(self):
        self.update_server = "https://updates.astros.org"
        self.current_version = self.get_current_version()
    
    async def check_updates(self):
        """Check for available updates"""
        response = await self.fetch_update_info()
        if response['latest_version'] > self.current_version:
            return response
        return None
    
    async def download_update(self, update_info):
        """Download and verify update package"""
        # Download delta update if available
        # Verify signature and checksums
        # Apply update safely with rollback capability
        pass
```

---

## Next Steps

### Development Priority
1. **Set up basic live-build configuration**
2. **Create minimal working ISO with AstrOS**
3. **Implement automated testing**
4. **Set up CI/CD pipeline**
5. **Create update mechanism**

### Community Involvement
1. **Document build process thoroughly**
2. **Create video tutorials**
3. **Set up build infrastructure**
4. **Enable community contributions**
5. **Establish quality standards**

Remember: Start simple, iterate quickly, and always test thoroughly. The goal is to create a reliable, professional distribution that showcases AstrOS capabilities while maintaining Ubuntu's stability and compatibility.