# AstrOS Complete Installation & Management Guide
*Version 0.1.0 - Production Ready*

---

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Service Management](#service-management)
6. [Troubleshooting](#troubleshooting)
7. [Development](#development)

---

## 🚀 Quick Start

### 5-Minute Setup

```bash
# 1. Install the package
sudo dpkg -i astros-core.deb

# 2. Set your API key
echo "ASTROS_API_KEY=your_api_key_here" >> ~/.config/astros/agent.env

# 3. Start the service
sudo systemctl enable astros-agent@$(whoami)
sudo systemctl start astros-agent@$(whoami)

# 4. Test it!
astros-cli "Hello! What can you do?"
```

---

## 📦 Installation

### Prerequisites
- **OS**: Ubuntu 20.04+, Debian 11+, or WSL2
- **Python**: 3.10 or higher
- **RAM**: Minimum 512MB available
- **Internet**: For API calls

### From Package (Recommended)

```bash
# Download the package
wget https://github.com/CoreOrganizations/AstrOS/releases/latest/download/astros-core.deb

# Install
sudo dpkg -i astros-core.deb

# Verify installation
dpkg -l | grep astros-core
```

### From Source

```bash
# Clone repository
git clone https://github.com/CoreOrganizations/AstrOS.git
cd AstrOS

# Build package
chmod +x build-package.sh
./build-package.sh

# Install
sudo dpkg -i packages/astros-core.deb
```

### WSL2 Installation

```bash
# From Windows PowerShell
wsl -d Ubuntu-24.04 bash -c "cd /mnt/d/AstrOS && sudo dpkg -i packages/astros-core.deb"

# Configure
wsl -d Ubuntu-24.04 bash -c "echo 'ASTROS_API_KEY=your_key' >> ~/.config/astros/agent.env"

# Start service
wsl -d Ubuntu-24.04 bash -c "sudo systemctl enable astros-agent@\$(whoami) && sudo systemctl start astros-agent@\$(whoami)"
```

---

## ⚙️ Configuration

### Initial Setup

After installation, configure your API key:

```bash
# Edit configuration file
nano ~/.config/astros/agent.env
```

Add your configuration:

```env
# Required: OpenRouter API Key
ASTROS_API_KEY=your_api_key_here

# Optional: Model Selection
ASTROS_MODEL=mistralai/ministral-8b

# Optional: API Settings
ASTROS_API_BASE=https://openrouter.ai/api/v1
ASTROS_MAX_TOKENS=2048
ASTROS_TEMPERATURE=0.7
ASTROS_TIMEOUT=60
```

### Configuration File Locations

| File | Path | Purpose |
|------|------|---------|
| **User Config** | `~/.config/astros/agent.env` | API key and settings |
| **Virtualenv** | `~/.local/share/astros/venv/` | Python packages |
| **Service File** | `/etc/systemd/system/astros-agent@.service` | Systemd configuration |
| **Agent Code** | `/usr/lib/astros/agent/` | Main application |
| **CLI Tool** | `/usr/bin/astros-cli` | Command-line interface |

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `ASTROS_API_KEY` | *Required* | OpenRouter API key |
| `ASTROS_MODEL` | `mistralai/ministral-8b` | AI model to use |
| `ASTROS_API_BASE` | `https://openrouter.ai/api/v1` | API endpoint |
| `ASTROS_MAX_TOKENS` | `2048` | Maximum response tokens |
| `ASTROS_TEMPERATURE` | `0.7` | Response creativity (0.0-1.0) |
| `ASTROS_TIMEOUT` | `60` | Request timeout in seconds |

### Get API Key

1. Visit [OpenRouter](https://openrouter.ai/keys)
2. Sign up for a free account
3. Create an API key
4. Copy the key to your config file

---

## 💬 Usage

### Command-Line Interface

```bash
# Simple query
astros-cli "What is the weather like today?"

# Complex questions
astros-cli "Explain quantum computing in simple terms"

# Code generation
astros-cli "Write a Python function to calculate fibonacci numbers"

# Multi-line queries
astros-cli "What are the key differences between
Docker and Podman? Give me 3 main points."
```

### Service Management

```bash
# Start service
sudo systemctl start astros-agent@$(whoami)

# Stop service
sudo systemctl stop astros-agent@$(whoami)

# Restart service
sudo systemctl restart astros-agent@$(whoami)

# Check status
sudo systemctl status astros-agent@$(whoami)

# Enable auto-start
sudo systemctl enable astros-agent@$(whoami)

# Disable auto-start
sudo systemctl disable astros-agent@$(whoami)
```

### View Logs

```bash
# Real-time logs
sudo journalctl -u astros-agent@$(whoami) -f

# Last 50 lines
sudo journalctl -u astros-agent@$(whoami) -n 50

# Logs from today
sudo journalctl -u astros-agent@$(whoami) --since today

# Filter by priority
sudo journalctl -u astros-agent@$(whoami) -p err
```

### Health Check

```bash
# Quick check
systemctl is-active astros-agent@$(whoami)

# Detailed status
sudo systemctl status astros-agent@$(whoami) --no-pager

# Memory usage
systemd-cgtop -1 | grep astros
```

---

## 🔧 Service Management

### Service Configuration

The systemd service runs as a user instance with these features:

- ✅ **Auto-restart**: Restarts on failure
- ✅ **Resource limits**: 512MB RAM, 50% CPU
- ✅ **Security**: Sandboxed with limited access
- ✅ **Logging**: All output to journald

### Service Commands

```bash
# Full status with recent logs
sudo systemctl status astros-agent@$(whoami) --no-pager -l

# Reload service configuration
sudo systemctl daemon-reload

# Check if service is running
systemctl is-active astros-agent@$(whoami)

# Check if service is enabled
systemctl is-enabled astros-agent@$(whoami)
```

### Multi-User Setup

```bash
# Install for multiple users
sudo systemctl enable astros-agent@user1
sudo systemctl enable astros-agent@user2

# Start all instances
sudo systemctl start astros-agent@user1
sudo systemctl start astros-agent@user2

# Check all instances
sudo systemctl status 'astros-agent@*'
```

---

## 🐛 Troubleshooting

### Service Won't Start

**Check status:**
```bash
sudo systemctl status astros-agent@$(whoami) --no-pager
```

**Common causes:**

1. **Missing API key**
   ```bash
   # Fix: Add API key
   echo "ASTROS_API_KEY=your_key" >> ~/.config/astros/agent.env
   sudo systemctl restart astros-agent@$(whoami)
   ```

2. **Wrong file permissions**
   ```bash
   # Fix: Set correct permissions
   chmod 600 ~/.config/astros/agent.env
   ```

3. **Virtualenv missing**
   ```bash
   # Fix: Reinstall package
   sudo dpkg-reconfigure astros-core
   ```

### CLI Not Working

**Check virtualenv:**
```bash
ls -la ~/.local/share/astros/venv/
```

**Check CLI path:**
```bash
which astros-cli
file $(which astros-cli)
```

**Fix:**
```bash
# Reinstall package
sudo dpkg -i --force-confmiss astros-core.deb
```

### API Errors

**Check API key:**
```bash
grep ASTROS_API_KEY ~/.config/astros/agent.env
```

**Test API connection:**
```bash
astros-cli "Test connection"
```

**Check logs for API errors:**
```bash
sudo journalctl -u astros-agent@$(whoami) | grep -i "error\|fail"
```

### High Memory Usage

**Check current usage:**
```bash
sudo systemctl status astros-agent@$(whoami) | grep Memory
```

**Adjust limit:**
```bash
sudo systemctl edit astros-agent@$(whoami)

# Add:
[Service]
MemoryMax=256M
```

### Service Keeps Restarting

**Check failure logs:**
```bash
sudo journalctl -u astros-agent@$(whoami) -p err --since "5 minutes ago"
```

**Common fixes:**
```bash
# 1. Check API key is valid
cat ~/.config/astros/agent.env

# 2. Verify network connectivity
ping -c 3 openrouter.ai

# 3. Reset and restart
sudo systemctl reset-failed astros-agent@$(whoami)
sudo systemctl restart astros-agent@$(whoami)
```

---

## 🧑‍💻 Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/CoreOrganizations/AstrOS.git
cd AstrOS

# Build package
./build-package.sh

# Install locally
sudo dpkg -i packages/astros-core.deb
```

### Running Tests

```bash
# Test package build
./test-package.sh

# Test agent directly
python3 -m pytest tests/

# Health check
./scripts/health-check.sh
```

### Package Structure

```
astros-core/
├── DEBIAN/
│   ├── control          # Package metadata
│   ├── postinst         # Post-installation script
│   └── prerm            # Pre-removal script
├── etc/systemd/system/
│   └── astros-agent@.service  # Systemd service
├── usr/bin/
│   └── astros-cli       # CLI wrapper
└── usr/lib/astros/agent/
    ├── astros.py        # Main agent code
    ├── astros_daemon.py # Daemon wrapper
    ├── astros_cli.py    # CLI implementation
    └── start_daemon.sh  # Daemon startup script
```

### Development Workflow

```bash
# 1. Make changes to source files
nano astros.py

# 2. Rebuild package
./build-package.sh

# 3. Test in clean environment
wsl -d Ubuntu-24.04 bash -c "cd /mnt/d/AstrOS && sudo dpkg -i packages/astros-core.deb"

# 4. Verify changes
astros-cli "Test new feature"
```

---

## 📊 Package Management

### Update Package

```bash
# Download new version
wget https://github.com/CoreOrganizations/AstrOS/releases/latest/download/astros-core.deb

# Upgrade (keeps config)
sudo dpkg -i astros-core.deb
```

### Remove Package

```bash
# Remove but keep config
sudo dpkg -r astros-core

# Remove everything
sudo dpkg -P astros-core
```

### Backup Configuration

```bash
# Backup config
cp ~/.config/astros/agent.env ~/astros-backup.env

# Restore config
cp ~/astros-backup.env ~/.config/astros/agent.env
```

---

## 🔐 Security

### API Key Security

- ✅ Store in `~/.config/astros/agent.env`
- ✅ Set permissions: `chmod 600 ~/.config/astros/agent.env`
- ✅ Never commit to git
- ✅ Use environment-specific keys

### Service Security Features

- **No new privileges**: Service can't escalate permissions
- **Private tmp**: Isolated temporary directory
- **Protected system**: Read-only access to system files
- **Protected home**: Limited home directory access
- **Resource limits**: RAM and CPU caps

---

## 📚 Advanced Topics

### Custom Models

```bash
# Edit config
nano ~/.config/astros/agent.env

# Add model
ASTROS_MODEL=anthropic/claude-3-haiku

# Restart service
sudo systemctl restart astros-agent@$(whoami)
```

### Multiple Environments

```bash
# Development
export ASTROS_MODEL=mistralai/ministral-8b
astros-cli "Dev test"

# Production
export ASTROS_MODEL=openai/gpt-4
astros-cli "Prod test"
```

### Monitoring

```bash
# Watch memory usage
watch -n 1 'systemctl status astros-agent@$(whoami) | grep Memory'

# Performance metrics
systemd-analyze plot > boot.svg

# Resource usage over time
sudo journalctl -u astros-agent@$(whoami) | grep -i memory
```

---

## 🆘 Support

### Resources

- 📖 [Documentation](https://github.com/CoreOrganizations/AstrOS/docs)
- 💬 [Discord Community](https://discord.gg/9qQstuyt)
- 🐛 [Issue Tracker](https://github.com/CoreOrganizations/AstrOS/issues)
- 📧 [Email Support](mailto:support@astros.ai)

### Common Commands Reference

```bash
# Installation
sudo dpkg -i astros-core.deb

# Configuration
nano ~/.config/astros/agent.env

# Service control
sudo systemctl {start|stop|restart|status} astros-agent@$(whoami)

# Logs
sudo journalctl -u astros-agent@$(whoami) -f

# CLI usage
astros-cli "Your question here"

# Health check
systemctl is-active astros-agent@$(whoami)

# Uninstall
sudo dpkg -r astros-core
```

---

## ✅ Installation Checklist

- [ ] Download `astros-core.deb`
- [ ] Install: `sudo dpkg -i astros-core.deb`
- [ ] Create config: `~/.config/astros/agent.env`
- [ ] Add API key: `ASTROS_API_KEY=...`
- [ ] Enable service: `sudo systemctl enable astros-agent@$(whoami)`
- [ ] Start service: `sudo systemctl start astros-agent@$(whoami)`
- [ ] Check status: `sudo systemctl status astros-agent@$(whoami)`
- [ ] Test CLI: `astros-cli "Hello!"`
- [ ] View logs: `sudo journalctl -u astros-agent@$(whoami) -f`

---

## 📝 Quick Reference Card

### File Locations
| What | Where |
|------|-------|
| Config | `~/.config/astros/agent.env` |
| Virtualenv | `~/.local/share/astros/venv/` |
| Logs | `journalctl -u astros-agent@$USER` |
| Service | `/etc/systemd/system/astros-agent@.service` |

### Service Commands
```bash
sudo systemctl start astros-agent@$(whoami)    # Start
sudo systemctl stop astros-agent@$(whoami)     # Stop
sudo systemctl restart astros-agent@$(whoami)  # Restart
sudo systemctl status astros-agent@$(whoami)   # Status
```

### CLI Usage
```bash
astros-cli "your question"                     # Ask question
astros-cli "explain $(cat file.py)"           # Analyze file
astros-cli "fix this: $(command)"             # Debug command
```

---

**Version**: 0.1.0  
**Last Updated**: 2025-10-02  
**Status**: Production Ready ✅

For more information, visit: https://github.com/CoreOrganizations/AstrOS
