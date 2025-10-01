# Stage 0: Build Foundation (2-3 months) 🏗️

**Goal**: Get a bootable AstrOS ISO with basic AI integration

**Current Status**: 🔄 In Progress

---

## 📋 Overview

This stage focuses on creating the foundational infrastructure for AstrOS:
- Setting up ISO build pipeline
- Converting AI agent to systemd service
- Creating first bootable ISO
- Basic desktop integration

---

## Week 1-2: Development Environment Setup ✅

### Objectives
- Set up Ubuntu 24.04 LTS base system
- Install ISO build tools
- Create automation scripts
- Test basic ISO build

### Tasks

#### Task 1.1: Install Build Tools
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install live-build and dependencies
sudo apt install -y \
    live-build \
    debootstrap \
    squashfs-tools \
    xorriso \
    isolinux \
    syslinux-utils \
    genisoimage \
    memtest86+ \
    grub-pc-bin \
    grub-efi-amd64-bin \
    grub-efi-ia32-bin

# Install development tools
sudo apt install -y \
    git \
    build-essential \
    python3-pip \
    python3-venv \
    nodejs \
    npm

# Verify installations
lb --version
debootstrap --version
```

#### Task 1.2: Create ISO Build Directory Structure
```bash
# Create project structure
mkdir -p ~/AstrOS-Builder
cd ~/AstrOS-Builder

# Create subdirectories
mkdir -p {iso-builder,packages,overlays,scripts,configs}

# Initialize git repository
git init
git remote add origin https://github.com/CoreOrganizations/AstrOS.git
```

#### Task 1.3: Set Up Live-Build Configuration
```bash
# Create live-build config
cd ~/AstrOS-Builder/iso-builder
lb config \
    --distribution jammy \
    --archive-areas "main restricted universe multiverse" \
    --apt-recommends false \
    --binary-images iso-hybrid \
    --bootappend-live "boot=live components quiet splash" \
    --debian-installer false \
    --iso-application "AstrOS" \
    --iso-publisher "AstrOS Project" \
    --iso-volume "AstrOS_24.04"
```

**Create**: `iso-builder/auto/config`
```bash
#!/bin/bash
lb config noauto \
    --distribution jammy \
    --archive-areas "main restricted universe multiverse" \
    --binary-images iso-hybrid \
    --apt-recommends false \
    --bootappend-live "boot=live components quiet splash" \
    "${@}"
```

#### Task 1.4: Create Build Automation Script
**Create**: `iso-builder/build-iso.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Starting AstrOS ISO Build..."
echo "================================"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
sudo lb clean --purge

# Configure build
echo "⚙️  Configuring build..."
lb config

# Build ISO
echo "🔨 Building ISO (this will take 30-60 minutes)..."
sudo lb build

# Verify ISO was created
if [ -f *.iso ]; then
    ISO_FILE=$(ls *.iso)
    ISO_SIZE=$(du -h "$ISO_FILE" | cut -f1)
    echo "✅ ISO built successfully!"
    echo "📦 File: $ISO_FILE"
    echo "📏 Size: $ISO_SIZE"
else
    echo "❌ ISO build failed!"
    exit 1
fi

echo "================================"
echo "🎉 Build complete!"
```

#### Task 1.5: Test Basic ISO Build
```bash
# Make script executable
chmod +x iso-builder/build-iso.sh

# Run first test build
cd iso-builder
sudo ./build-iso.sh
```

### ✅ Week 1-2 Deliverables
- [ ] Working ISO build pipeline
- [ ] Automated build scripts
- [ ] Documentation for build process
- [ ] First Ubuntu 24.04 base ISO created

### 📝 Documentation Required
Create `docs/ISO_BUILD_GUIDE.md` with:
- Build tool installation instructions
- Common build errors and solutions
- ISO customization process
- Testing procedures

---

## Week 3-4: Core AI Agent Integration 🔄

### Objectives
- Convert astros.py to systemd service
- Create daemon for AI agent
- Set up secure API key storage
- Test on fresh Ubuntu install

### Tasks

#### Task 2.1: Create Systemd Service File
**Create**: `configs/astros-agent.service`
```ini
[Unit]
Description=AstrOS AI Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=%i
WorkingDirectory=/usr/lib/astros/agent
ExecStart=/usr/bin/python3 /usr/lib/astros/agent/astros_daemon.py
Restart=on-failure
RestartSec=5
Environment="PYTHONUNBUFFERED=1"

# Security settings
PrivateTmp=yes
NoNewPrivileges=yes

[Install]
WantedBy=multi-user.target
```

#### Task 2.2: Create Daemon Script
**Create**: `astros-core/agent/astros_daemon.py`
```python
#!/usr/bin/env python3
"""
AstrOS Agent Daemon
Runs as systemd service to provide AI capabilities
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/astros/agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('astros-agent')

# Import the AI client from astros.py
sys.path.insert(0, str(Path(__file__).parent))
from astros import AstrOSAgent

class AstrOSDaemon:
    """Daemon wrapper for AstrOS Agent"""
    
    def __init__(self):
        self.agent = None
        self.running = False
        
    async def start(self):
        """Start the daemon"""
        logger.info("🚀 Starting AstrOS Agent Daemon")
        
        try:
            self.agent = AstrOSAgent()
            self.running = True
            logger.info("✅ AstrOS Agent started successfully")
            
            # Keep daemon running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ Failed to start agent: {e}")
            raise
            
    async def stop(self):
        """Stop the daemon"""
        logger.info("🛑 Stopping AstrOS Agent Daemon")
        self.running = False

async def main():
    """Main entry point"""
    daemon = AstrOSDaemon()
    
    try:
        await daemon.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
        await daemon.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Create log directory
    os.makedirs("/var/log/astros", exist_ok=True)
    
    # Run daemon
    asyncio.run(main())
```

#### Task 2.3: Set Up Secure API Key Storage
**Create**: `astros-core/agent/keyring_manager.py`
```python
#!/usr/bin/env python3
"""
Secure API key management using GNOME Keyring
"""

import os
import keyring
from pathlib import Path

class AstrOSKeyring:
    """Manage API keys securely"""
    
    SERVICE_NAME = "AstrOS"
    
    @staticmethod
    def store_api_key(key: str, provider: str = "default"):
        """Store API key in system keyring"""
        try:
            keyring.set_password(
                AstrOSKeyring.SERVICE_NAME,
                f"api_key_{provider}",
                key
            )
            return True
        except Exception as e:
            print(f"Failed to store API key: {e}")
            return False
    
    @staticmethod
    def get_api_key(provider: str = "default") -> str:
        """Retrieve API key from system keyring"""
        try:
            # Try keyring first
            key = keyring.get_password(
                AstrOSKeyring.SERVICE_NAME,
                f"api_key_{provider}"
            )
            
            # Fallback to .env file
            if not key:
                key = os.getenv('ASTROS_API_KEY')
            
            return key
        except Exception as e:
            print(f"Failed to retrieve API key: {e}")
            return None
    
    @staticmethod
    def delete_api_key(provider: str = "default"):
        """Delete API key from keyring"""
        try:
            keyring.delete_password(
                AstrOSKeyring.SERVICE_NAME,
                f"api_key_{provider}"
            )
            return True
        except Exception as e:
            print(f"Failed to delete API key: {e}")
            return False
```

#### Task 2.4: Create Installation Script
**Create**: `scripts/install-agent.sh`
```bash
#!/bin/bash
set -e

echo "📦 Installing AstrOS Agent..."

# Create directories
sudo mkdir -p /usr/lib/astros/agent
sudo mkdir -p /var/log/astros
sudo mkdir -p /etc/astros

# Copy agent files
sudo cp -r astros-core/agent/* /usr/lib/astros/agent/

# Install Python dependencies
sudo pip3 install -r astros-core/agent/requirements.txt

# Copy systemd service
sudo cp configs/astros-agent.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable astros-agent.service

echo "✅ AstrOS Agent installed successfully!"
echo "🔧 Configure API key and start with: sudo systemctl start astros-agent"
```

#### Task 2.5: Test Agent on Fresh Ubuntu
```bash
# Install on test VM
./scripts/install-agent.sh

# Start service
sudo systemctl start astros-agent

# Check status
sudo systemctl status astros-agent

# View logs
sudo journalctl -u astros-agent -f
```

### ✅ Week 3-4 Deliverables
- [ ] `astros-agent.service` systemd unit file
- [ ] Daemon script (`astros_daemon.py`)
- [ ] Secure API key management
- [ ] Installation script
- [ ] Service running on test system

---

## Week 5-8: First Bootable ISO 🎯

### Objectives
- Create astros-core package
- Build .deb packages
- Customize Ubuntu ISO
- Add first-boot wizard
- Test complete installation

### Tasks

#### Task 3.1: Create Debian Package Structure
```bash
# Create package directory
mkdir -p packages/astros-core/DEBIAN
mkdir -p packages/astros-core/usr/lib/astros/agent
mkdir -p packages/astros-core/etc/systemd/system
mkdir -p packages/astros-core/usr/bin

# Create control file
cat > packages/astros-core/DEBIAN/control << EOF
Package: astros-core
Version: 0.1.0
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.12), python3-pip, python3-dotenv, python3-httpx
Maintainer: AstrOS Team <aiastros2025@gmail.com>
Description: AstrOS AI Agent Core
 Native AI integration for Ubuntu with MistralAI support.
 Provides system-level AI capabilities through natural language.
EOF
```

#### Task 3.2: Create Post-Install Script
**Create**: `packages/astros-core/DEBIAN/postinst`
```bash
#!/bin/bash
set -e

echo "🚀 Configuring AstrOS Agent..."

# Install Python dependencies
pip3 install -r /usr/lib/astros/agent/requirements.txt --quiet

# Create log directory
mkdir -p /var/log/astros
chmod 755 /var/log/astros

# Reload systemd
systemctl daemon-reload

# Enable service (don't start yet, user needs to configure API key)
systemctl enable astros-agent.service

echo "✅ AstrOS Agent installed!"
echo "📝 Configure API key in /etc/astros/.env before starting"

exit 0
```

#### Task 3.3: Build .deb Package
```bash
# Copy files
cp -r astros-core/agent/* packages/astros-core/usr/lib/astros/agent/
cp configs/astros-agent.service packages/astros-core/etc/systemd/system/

# Make scripts executable
chmod 755 packages/astros-core/DEBIAN/postinst

# Build package
dpkg-deb --build packages/astros-core

# Verify package
dpkg-deb --info packages/astros-core.deb
```

#### Task 3.4: Integrate Package into ISO
**Create**: `iso-builder/config/package-lists/astros.list.chroot`
```
# AstrOS Core Packages
python3
python3-pip
python3-venv
python3-dotenv

# Copy our custom package
# (handled by hooks)
```

**Create**: `iso-builder/config/hooks/live/install-astros.hook.chroot`
```bash
#!/bin/bash
# Install AstrOS custom package

# Copy package from host
cp /tmp/packages/astros-core.deb /tmp/

# Install package
dpkg -i /tmp/astros-core.deb

# Clean up
rm /tmp/astros-core.deb
```

#### Task 3.5: Create First-Boot Wizard
**Create**: `astros-core/first-boot/astros-setup.py`
```python
#!/usr/bin/env python3
"""
AstrOS First Boot Setup Wizard
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import os

class AstrOSSetupWizard(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.astros.setup')
        
    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Welcome to AstrOS")
        window.set_default_size(600, 400)
        
        # Create content
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(40)
        box.set_margin_bottom(40)
        box.set_margin_start(40)
        box.set_margin_end(40)
        
        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>Welcome to AstrOS</b></big>")
        box.append(title)
        
        # Description
        desc = Gtk.Label()
        desc.set_text("Let's set up your AI assistant. You'll need an API key from OpenRouter.")
        desc.set_wrap(True)
        box.append(desc)
        
        # API Key entry
        api_key_label = Gtk.Label()
        api_key_label.set_text("OpenRouter API Key:")
        api_key_label.set_xalign(0)
        box.append(api_key_label)
        
        api_key_entry = Gtk.Entry()
        api_key_entry.set_placeholder_text("sk-or-v1-...")
        box.append(api_key_entry)
        
        # Help text
        help_text = Gtk.Label()
        help_text.set_markup('<small>Get your free API key at <a href="https://openrouter.ai/keys">OpenRouter.ai</a></small>')
        box.append(help_text)
        
        # Continue button
        continue_btn = Gtk.Button(label="Continue")
        continue_btn.connect("clicked", self.on_continue, api_key_entry, window)
        box.append(continue_btn)
        
        window.set_child(box)
        window.present()
    
    def on_continue(self, button, entry, window):
        api_key = entry.get_text()
        
        if api_key.startswith("sk-or-"):
            # Save API key
            os.makedirs("/etc/astros", exist_ok=True)
            with open("/etc/astros/.env", "w") as f:
                f.write(f"ASTROS_API_KEY={api_key}\n")
                f.write("ASTROS_BASE_URL=https://openrouter.ai/api/v1\n")
                f.write("ASTROS_AI_MODEL__NAME=mistralai/ministral-8b\n")
            
            # Start service
            os.system("sudo systemctl start astros-agent")
            
            # Show success
            dialog = Gtk.MessageDialog(
                transient_for=window,
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Setup Complete!"
            )
            dialog.format_secondary_text(
                "AstrOS is now ready! Press Super+Space to activate your AI assistant."
            )
            dialog.connect("response", lambda d, r: window.close())
            dialog.present()
        else:
            # Show error
            dialog = Gtk.MessageDialog(
                transient_for=window,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Invalid API Key"
            )
            dialog.format_secondary_text(
                "Please enter a valid OpenRouter API key starting with 'sk-or-'."
            )
            dialog.present()

if __name__ == "__main__":
    app = AstrOSSetupWizard()
    app.run()
```

#### Task 3.6: Build Complete ISO
```bash
# Update build script to include package
cd iso-builder

# Copy package to build
mkdir -p config/includes.chroot/tmp/packages
cp ../packages/astros-core.deb config/includes.chroot/tmp/packages/

# Build ISO
sudo ./build-iso.sh

# Test ISO in VM
../tools/test-vm.sh *.iso
```

### ✅ Week 5-8 Deliverables
- [ ] `astros-core` .deb package
- [ ] First-boot setup wizard
- [ ] Complete bootable ISO (< 3GB)
- [ ] ISO tested in virtual machine
- [ ] Agent starts automatically after setup

---

## Week 9-12: Basic Desktop Integration 🖥️

### Objectives
- Create GNOME Shell extension
- Add system tray icon
- Implement global hotkey
- Add notification system
- Create input dialog

### Tasks

#### Task 4.1: Create GNOME Shell Extension
```bash
# Create extension directory
mkdir -p astros-desktop/gnome-shell/astros@astros.org

cd astros-desktop/gnome-shell/astros@astros.org
```

**Create**: `metadata.json`
```json
{
  "name": "AstrOS",
  "description": "Native AI assistant for Ubuntu",
  "uuid": "astros@astros.org",
  "shell-version": ["46"],
  "url": "https://github.com/CoreOrganizations/AstrOS",
  "version": 1
}
```

**Create**: `extension.js`
```javascript
import St from 'gi://St';
import GObject from 'gi://GObject';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import Gio from 'gi://Gio';
import Meta from 'gi://Meta';
import Shell from 'gi://Shell';

const AstrOSIndicator = GObject.registerClass(
class AstrOSIndicator extends PanelMenu.Button {
    _init() {
        super._init(0.0, 'AstrOS Indicator');
        
        // Create icon
        let icon = new St.Icon({
            icon_name: 'emblem-system-symbolic',
            style_class: 'system-status-icon'
        });
        
        this.add_child(icon);
        
        // Add menu items
        let statusItem = new PopupMenu.PopupMenuItem('AstrOS Active');
        statusItem.connect('activate', () => {
            this._openAstrOS();
        });
        this.menu.addMenuItem(statusItem);
    }
    
    _openAstrOS() {
        // Open AstrOS chat window
        imports.gi.Gio.app_info_launch_default_for_uri(
            'astros://open',
            null
        );
    }
});

export default class Extension {
    constructor() {
        this._indicator = null;
        this._settings = null;
    }
    
    enable() {
        log('Enabling AstrOS extension');
        
        // Add indicator to panel
        this._indicator = new AstrOSIndicator();
        Main.panel.addToStatusArea('astros-indicator', this._indicator);
        
        // Register global hotkey (Super+Space)
        this._registerHotkey();
    }
    
    disable() {
        log('Disabling AstrOS extension');
        
        if (this._indicator) {
            this._indicator.destroy();
            this._indicator = null;
        }
        
        this._unregisterHotkey();
    }
    
    _registerHotkey() {
        Main.wm.addKeybinding(
            'astros-activate',
            new Gio.Settings({schema_id: 'org.gnome.shell.keybindings'}),
            Meta.KeyBindingFlags.NONE,
            Shell.ActionMode.NORMAL,
            () => this._activateAstrOS()
        );
    }
    
    _unregisterHotkey() {
        Main.wm.removeKeybinding('astros-activate');
    }
    
    _activateAstrOS() {
        log('AstrOS activated via hotkey');
        // Launch AstrOS chat interface
        imports.gi.Gio.Subprocess.new(
            ['astros-chat'],
            imports.gi.Gio.SubprocessFlags.NONE
        );
    }
}
```

#### Task 4.2: Create Simple GTK Input Dialog
**Create**: `astros-desktop/astros-chat-quick.py`
```python
#!/usr/bin/env python3
"""
Quick AstrOS chat dialog
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import subprocess
import asyncio

class AstrOSQuickChat(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, title="AstrOS")
        self.set_default_size(500, 150)
        
        # Create UI
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        
        # Input field
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Ask me anything...")
        self.entry.connect("activate", self.on_ask)
        box.append(self.entry)
        
        # Response label
        self.response = Gtk.Label()
        self.response.set_wrap(True)
        self.response.set_xalign(0)
        box.append(self.response)
        
        self.set_child(box)
    
    def on_ask(self, entry):
        question = entry.get_text()
        if question:
            self.response.set_text("🤔 Thinking...")
            GLib.timeout_add(100, self.get_response, question)
    
    def get_response(self, question):
        # Call astros agent via D-Bus or CLI
        try:
            result = subprocess.run(
                ['astros-cli', 'ask', question],
                capture_output=True,
                text=True,
                timeout=30
            )
            self.response.set_text(result.stdout)
        except Exception as e:
            self.response.set_text(f"Error: {e}")
        return False

class AstrOSQuickChatApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.astros.quickchat')
    
    def do_activate(self):
        win = AstrOSQuickChat(application=self)
        win.present()

if __name__ == "__main__":
    app = AstrOSQuickChatApp()
    app.run()
```

#### Task 4.3: Package Extension for ISO
```bash
# Package extension
cd astros-desktop/gnome-shell/astros@astros.org
gnome-extensions pack --force

# Copy to ISO overlay
mkdir -p iso-builder/config/includes.chroot/usr/share/gnome-shell/extensions/
cp -r ../astros@astros.org iso-builder/config/includes.chroot/usr/share/gnome-shell/extensions/
```

### ✅ Week 9-12 Deliverables
- [ ] GNOME Shell extension working
- [ ] System tray icon visible
- [ ] Super+Space hotkey activates AI
- [ ] Quick chat dialog functional
- [ ] Extension included in ISO

---

## 🎯 Stage 0 Success Criteria

### Must Have ✅
- [ ] Bootable ISO that installs Ubuntu + AstrOS
- [ ] AI agent runs automatically on login
- [ ] Can interact via Super+Space keyboard shortcut
- [ ] ISO size < 3GB
- [ ] Agent connects to MistralAI Ministral 8B successfully
- [ ] First-boot setup wizard completes configuration

### Nice to Have ⭐
- [ ] Custom boot splash screen
- [ ] AstrOS branding on desktop
- [ ] Basic system notifications
- [ ] Agent status indicator in system tray

---

## 📊 Progress Tracking

| Week | Component | Status | Notes |
|------|-----------|--------|-------|
| 1-2 | Build Environment | 🔄 | ISO tools installed |
| 3-4 | AI Agent Service | ⏳ | Starting soon |
| 5-8 | Bootable ISO | ⏳ | Pending |
| 9-12 | Desktop Integration | ⏳ | Pending |

---

## 🔗 Related Documentation

- [ISO Build Guide](ISO_BUILD_GUIDE.md)
- [Systemd Service Guide](SYSTEMD_GUIDE.md)
- [GNOME Extension Development](GNOME_EXTENSION_GUIDE.md)
- [Testing Guide](TESTING_GUIDE.md)

---

## 💬 Need Help?

- Discord: https://discord.gg/9qQstuyt
- Email: aiastros2025@gmail.com
- GitHub Issues: https://github.com/CoreOrganizations/AstrOS/issues

---

**Next Stage**: [Stage 1: Desktop UI & Core Plugins](STAGE_1_DESKTOP_PLUGINS.md)
