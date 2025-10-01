# AstrOS Development Guide 🚀

**Complete step-by-step guide for building AstrOS from the ground up**

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Development Stages](#development-stages)
3. [Getting Started](#getting-started)
4. [Repository Structure](#repository-structure)
5. [Development Workflow](#development-workflow)
6. [Testing & Quality](#testing--quality)
7. [Release Process](#release-process)
8. [Contributing](#contributing)

---

## 🎯 Project Overview

**AstrOS** is a complete Ubuntu-based operating system with native AI capabilities built into the OS layer. We're building this in 5 major stages over 12-18 months.

### Vision
- 🖥️ OS-level AI integration (not just an app)
- 🎙️ Voice-first interface
- 🔧 Intelligent automation
- 🎨 Custom GNOME desktop environment
- 🔒 Privacy-focused with local+cloud AI

### Current Status
- **Current Stage**: Stage 0 - Build Foundation
- **Current Model**: mistralai/ministral-8b via OpenRouter
- **Target Release**: Q1 2025 (Alpha 0.1.0)

---

## 📅 Development Stages

### [Stage 0: Build Foundation](STAGE_0_FOUNDATION.md) (2-3 months) 🏗️
**Goal**: Bootable ISO with basic AI integration

**Weeks 1-2**: Development Environment Setup
- Install ISO build tools (live-build, debootstrap, etc.)
- Create build automation scripts
- Test basic ISO build process

**Weeks 3-4**: Core AI Agent Integration
- Convert astros.py to systemd service
- Secure API key storage with GNOME Keyring
- Auto-start on user login

**Weeks 5-8**: First Bootable ISO
- Create astros-core .deb package
- Customize Ubuntu ISO
- First-boot setup wizard

**Weeks 9-12**: Basic Desktop Integration
- GNOME Shell extension
- System tray icon
- Global hotkey (Super+Space)
- Quick chat dialog

**Success Criteria**:
- ✅ Bootable ISO < 3GB
- ✅ AI agent auto-starts
- ✅ Super+Space activates AI
- ✅ MistralAI integration working

---

### [Stage 1: Desktop UI & Core Plugins](STAGE_1_DESKTOP_PLUGINS.md) (3-4 months) 🖥️
**Goal**: Native desktop experience with plugin ecosystem

**Weeks 1-2**: Technology Decision & Setup
- Choose Electron vs GTK4 (Start with Electron)
- Set up project structure
- Create basic window

**Weeks 3-4**: Main Chat Interface
- React-based chat UI
- Conversation history
- Real-time AI responses
- D-Bus integration

**Weeks 5-6**: Settings & Plugin Management
- Settings panel for API configuration
- Plugin management UI
- Theme support

**Weeks 7-8**: Build & Package
- Create .deb package
- AppImage for portability
- Integration with ISO

**Plugin System (4 weeks)**:
- D-Bus interface for plugins
- Plugin discovery and loading
- Sandboxing with bubblewrap
- Permission system

**Core Plugins (6 weeks)**:
1. System Control - Volume, brightness, app launching
2. File Manager - Smart file operations
3. Terminal - Safe command execution

**Success Criteria**:
- ✅ Native app with chat interface
- ✅ 3 plugins working
- ✅ Response time < 500ms
- ✅ .deb package ready

---

### Stage 2: System Integration & Automation (4-6 months) 🔧
**Goal**: Deep OS integration with automation

**System Hooks (8 weeks)**:
- Monitor D-Bus events (USB, network, power)
- Automation rules engine
- Systemd integration

**Advanced Plugins (10 weeks)**:
4. Developer Tools - Git, code search, scaffolding
5. Package Manager - APT, Snap, Flatpak
6. Networking - VPN, firewall, diagnostics
7. Security - Passwords, encryption, auditing

**Voice Integration (4 weeks)**:
- Whisper speech-to-text
- Text-to-speech (Coqui TTS)
- Wake word detection
- Push-to-talk hotkey

**Success Criteria**:
- ✅ 7+ plugins working
- ✅ Event-driven automation
- ✅ Voice control functional
- ✅ < 200MB RAM idle

---

### Stage 3: Polish, Testing & Community (3-4 months) ✨
**Goal**: Production-ready release

**Quality & Stability (6 weeks)**:
- Hardware compatibility testing
- Memory leak fixes
- Performance optimization
- Battery life improvements

**Installation & Setup (4 weeks)**:
- Custom installer (Ubiquity)
- First-boot tutorial
- Migration tool from Ubuntu

**Documentation (3 weeks)**:
- User manual
- Plugin development guide
- Video tutorials

**Community Infrastructure (3 weeks)**:
- Plugin repository
- Forums (Discourse)
- Bug tracker templates

**Success Criteria**:
- ✅ < 1 crash per week
- ✅ Complete documentation
- ✅ Beta release ready
- ✅ Active community

---

### Stage 4: Advanced Features (6-12 months) 🚀
**Goal**: Next-generation capabilities

- Intelligent system management
- Multi-modal AI (vision, image gen)
- Desktop environment variants (KDE, XFCE)
- Hardware optimizations (ARM, GPU)

---

## 🚀 Getting Started

### Prerequisites

```bash
# System Requirements
- Ubuntu 24.04 LTS (or similar Debian-based)
- 16GB RAM (minimum 8GB)
- 50GB free disk space
- Intel/AMD 64-bit processor
```

### Initial Setup

```bash
# 1. Clone repository
git clone https://github.com/CoreOrganizations/AstrOS.git
cd AstrOS

# 2. Install dependencies
sudo apt update
sudo apt install -y \
    live-build debootstrap squashfs-tools xorriso \
    python3-pip python3-venv nodejs npm \
    git build-essential

# 3. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OpenRouter API key

# 5. Validate setup
python validate_env.py
```

### Quick Test

```bash
# Test current AI agent
python astros.py

# Ask a question
# You: Hello! What model are you using?
# AstrOS: I'm using mistralai/ministral-8b...
```

---

## 📁 Repository Structure

```
AstrOS/
├── astros.py                    # Current AI agent (Python)
├── validate_env.py              # Environment validation
├── .env                         # Configuration (gitignored)
├── requirements.txt             # Python dependencies
│
├── docs/                        # 📚 Documentation
│   ├── DEVELOPMENT_GUIDE.md    # This file
│   ├── STAGE_0_FOUNDATION.md   # Stage 0 detailed guide
│   ├── STAGE_1_DESKTOP_PLUGINS.md  # Stage 1 guide
│   ├── API_SETUP.md            # API configuration
│   ├── GETTING_STARTED.md      # Quick start
│   └── ENV_SETUP.md            # Environment setup
│
├── iso-builder/                 # 💿 ISO Build System
│   ├── build-iso.sh            # Main build script
│   ├── config/                 # Live-build configs
│   └── overlays/               # File system overlays
│
├── astros-core/                 # 🤖 Core AI Agent
│   ├── agent/                  # Main agent code
│   │   ├── astros_daemon.py   # Systemd daemon
│   │   └── keyring_manager.py # Secure key storage
│   └── dbus/                   # D-Bus interfaces
│
├── astros-desktop/              # 🖥️ Desktop Application
│   ├── electron-app/           # Electron UI (Phase 1)
│   ├── gtk-app/                # GTK4 UI (Phase 2)
│   └── gnome-shell/            # GNOME extensions
│
├── astros-plugins/              # 🔌 Official Plugins
│   ├── base_plugin.py          # Plugin base class
│   ├── plugin_manager.py       # Plugin management
│   ├── system-control/         # System control plugin
│   ├── file-manager/           # File operations
│   ├── terminal/               # Terminal integration
│   ├── developer-tools/        # Dev tools
│   ├── package-manager/        # Package management
│   ├── networking/             # Network tools
│   └── security/               # Security tools
│
├── astros-voice/                # 🎙️ Voice Processing
│   ├── whisper/                # Speech-to-text
│   ├── tts/                    # Text-to-speech
│   └── hotword/                # Wake word detection
│
├── packages/                    # 📦 Debian Packages
│   └── astros-core/            # Core package structure
│
├── scripts/                     # 🔧 Build Scripts
│   ├── install-agent.sh        # Agent installation
│   └── setup-dev-env.sh        # Dev environment setup
│
├── configs/                     # ⚙️ Configuration Files
│   └── astros-agent.service    # Systemd service
│
├── tests/                       # 🧪 Testing Suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
│
├── tools/                       # 🛠️ Development Tools
│   ├── test-vm.sh              # VM testing
│   └── debug/                  # Debugging utilities
│
├── assets/                      # 🎨 Assets
│   └── icons/                  # Application icons
│
├── README.md                    # Project overview
├── ROADMAP.md                   # Development roadmap
├── LICENSE                      # Apache 2.0
└── CONTRIBUTING.md              # Contributing guidelines
```

---

## 🔄 Development Workflow

### Daily Development

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and test
# Edit files...
python validate_env.py  # Test configuration
python astros.py        # Test agent

# 4. Commit changes
git add .
git commit -m "feat: add your feature description"

# 5. Push and create PR
git push origin feature/your-feature-name
# Create Pull Request on GitHub
```

### Branch Strategy

- `main` - Latest stable development
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `release/*` - Release preparation
- `hotfix/*` - Critical fixes

### Commit Message Format

```
type(scope): brief description

Detailed description if needed

Fixes #123
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## 🧪 Testing & Quality

### Running Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Full test suite
pytest tests/

# With coverage
pytest --cov=astros tests/
```

### Code Quality

```bash
# Linting
flake8 astros-core/
pylint astros-core/

# Type checking
mypy astros-core/

# Formatting
black astros-core/
isort astros-core/
```

### ISO Testing

```bash
# Build test ISO
cd iso-builder
sudo ./build-iso.sh

# Test in VM
cd ..
./tools/test-vm.sh iso-builder/*.iso

# Test on real hardware (USB boot)
sudo dd if=astros-*.iso of=/dev/sdX bs=4M status=progress
```

---

## 📦 Release Process

### Version Numbers

Format: `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes (v1.0.0, v2.0.0)
- `MINOR`: New features (v1.1.0, v1.2.0)
- `PATCH`: Bug fixes (v1.1.1, v1.1.2)

### Release Checklist

```bash
# 1. Update version
# Edit version in:
# - package.json
# - setup.py
# - astros-core/VERSION

# 2. Update changelog
# Edit CHANGELOG.md

# 3. Build release
./scripts/build-release.sh

# 4. Test release
./scripts/test-release.sh

# 5. Create git tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# 6. Create GitHub release
# Upload ISO and checksums

# 7. Announce release
# Discord, Twitter, mailing list
```

---

## 🤝 Contributing

### How to Contribute

1. **Join Community**
   - Discord: https://discord.gg/9qQstuyt
   - GitHub Discussions
   - Weekly dev meetings (Fridays 3pm UTC)

2. **Pick a Task**
   - Check current stage tasks
   - Look for `good-first-issue` labels
   - Join a working group

3. **Development Areas**

| Area | Skills | Current Need |
|------|--------|--------------|
| ISO Builder | Bash, Linux | 🔴 High |
| AI Agent | Python, AI/ML | 🔴 High |
| Desktop UI | TypeScript, React | 🟡 Medium |
| Plugins | Python, D-Bus | 🔴 High |
| Voice | Audio, ML | 🟢 Low |
| Docs | Writing | 🟡 Medium |
| Testing | QA | 🔴 High |

4. **Getting Help**
   - Ask in Discord #development channel
   - Comment on GitHub issues
   - Tag maintainers in PRs
   - Weekly office hours (Wednesdays 2pm UTC)

### Code Review Process

1. Create PR with clear description
2. Automated checks must pass (CI/CD)
3. At least 1 maintainer review required
4. Address review feedback
5. Maintainer merges when approved

### Plugin Development

See [Plugin Development Guide](PLUGIN_DEVELOPMENT.md) for:
- Plugin API reference
- Template generation
- Testing plugins
- Publishing to plugin store

---

## 📚 Additional Resources

### Documentation
- [API Setup Guide](API_SETUP.md)
- [Stage 0 Guide](STAGE_0_FOUNDATION.md)
- [Stage 1 Guide](STAGE_1_DESKTOP_PLUGINS.md)
- [Environment Setup](ENV_SETUP.md)

### External Resources
- [Ubuntu Live-Build Manual](https://live-team.pages.debian.net/live-manual/)
- [GNOME Shell Extensions](https://gjs.guide/)
- [D-Bus Tutorial](https://dbus.freedesktop.org/doc/dbus-tutorial.html)
- [Electron Documentation](https://www.electronjs.org/docs)

### Community
- **Discord**: https://discord.gg/9qQstuyt
- **Email**: aiastros2025@gmail.com
- **GitHub**: https://github.com/CoreOrganizations/AstrOS
- **Twitter**: @AstrOS_Project

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Validate environment
python validate_env.py

# Test AI agent
python astros.py

# Build ISO
cd iso-builder && sudo ./build-iso.sh

# Run tests
pytest tests/

# Install agent locally
./scripts/install-agent.sh

# Start agent service
sudo systemctl start astros-agent

# View agent logs
sudo journalctl -u astros-agent -f
```

### Key Files to Know

- `astros.py` - Main AI agent
- `.env` - Configuration (API keys)
- `iso-builder/build-iso.sh` - ISO build script
- `configs/astros-agent.service` - Systemd service
- `packages/astros-core/DEBIAN/control` - Package definition

---

## ⚠️ Common Issues & Solutions

### Issue: ISO build fails
```bash
# Solution: Clean and rebuild
cd iso-builder
sudo lb clean --purge
sudo ./build-iso.sh
```

### Issue: Agent won't start
```bash
# Check logs
sudo journalctl -u astros-agent -n 50

# Check API key
cat /etc/astros/.env

# Restart service
sudo systemctl restart astros-agent
```

### Issue: Plugin not loading
```bash
# Check plugin directory
ls -la /usr/lib/astros/plugins/

# Check permissions
sudo chmod +x /usr/lib/astros/plugins/*/plugin.py

# Reload plugins
sudo systemctl restart astros-agent
```

---

## 📞 Get Help

- **Stuck?** Ask in Discord #help channel
- **Bug?** Create GitHub issue with `bug` label
- **Feature idea?** Create GitHub issue with `enhancement` label
- **Security issue?** Email aiastros2025@gmail.com (do not create public issue)

---

**Ready to build the future of operating systems?** Let's go! 🚀

*Last Updated: October 2025*
*Current Stage: Stage 0 - Build Foundation*
