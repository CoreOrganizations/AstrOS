# 🚀 AstrOS Complete Management Guide

**Version**: 0.1.0  
**Last Updated**: October 2, 2025  
**Status**: Production Ready

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Service Management](#service-management)
6. [Troubleshooting](#troubleshooting)
7. [Development](#development)
8. [Package Management](#package-management)
9. [Advanced Topics](#advanced-topics)

---

## 🚀 Quick Start

### 5-Minute Setup

```bash
# 1. Install package
sudo dpkg -i packages/astros-core.deb

# 2. Get API key from: https://openrouter.ai/keys

# 3. Configure
nano ~/.config/astros/agent.env
# Add your API key to ASTROS_API_KEY=

# 4. Start service
sudo systemctl enable astros-agent@$(whoami)
sudo systemctl start astros-agent@$(whoami)

# 5. Test it!
astros-cli "Hello! What is 2+2?"
```

**Done!** ✅

---

## 📦 Installation

### Prerequisites

- Ubuntu 24.04 LTS (or Ubuntu 22.04+)
- Python 3.10 or higher
- Internet connection
- OpenRouter API key (free at https://openrouter.ai/keys)

### Install from Package

```bash
# On Ubuntu (native or WSL2)
cd /path/to/AstrOS
sudo dpkg -i packages/astros-core.deb

# Fix dependencies if needed
sudo apt-get install -f
```

### Install from Source

```bash
# Clone repository
git clone https://github.com/CoreOrganizations/AstrOS.git
cd AstrOS

# Build package
./build-package.sh

# Install
sudo dpkg -i packages/astros-core.deb
```

### WSL2 Installation

```bash
# On Windows, open PowerShell
wsl -d Ubuntu-24.04

# Navigate to AstrOS directory
cd /mnt/d/AstrOS

# Install package
sudo dpkg -i packages/astros-core.deb
```

---

## ⚙️ Configuration

### Initial Setup

After installation, configure your API key:

```bash
# Edit configuration
nano ~/.config/astros/agent.env

# Required: Add your API key
ASTROS_API_KEY=your-actual-api-key-here

# Optional: Adjust model settings
ASTROS_AI_MODEL__NAME=mistralai/ministral-8b
ASTROS_AI_MODEL__MAX_TOKENS=2048
ASTROS_AI_MODEL__TEMPERATURE=0.7
```

### Configuration File Location

```
~/.config/astros/agent.env
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `ASTROS_API_KEY` | (required) | Your OpenRouter API key |
| `ASTROS_BASE_URL` | openrouter.ai | API endpoint |
| `ASTROS_AI_MODEL__NAME` | ministral-8b | AI model to use |
| `ASTROS_AI_MODEL__MAX_TOKENS` | 2048 | Max response length |
| `ASTROS_AI_MODEL__TEMPERATURE` | 0.7 | Creativity (0-1) |
| `ASTROS_AI_MODEL__TIMEOUT` | 60 | Request timeout (sec) |
| `LOG_LEVEL` | INFO | Logging level |

### Get API Key

1. Visit: https://openrouter.ai/keys
2. Sign up (free)
3. Create new API key
4. Copy key to configuration

---

## 🎮 Usage

### Command-Line Interface

#### Basic Usage

```bash
# Ask a question
astros-cli "What is the capital of France?"

# Multiple words (use quotes)
astros-cli "Explain quantum computing in simple terms"

# Math questions
astros-cli "What is 15 * 23?"

# Code help
astros-cli "Write a Python function to sort a list"
```

#### Examples

```bash
# General knowledge
astros-cli "Who invented the telephone?"

# Creative tasks
astros-cli "Write a haiku about programming"

# Technical help
astros-cli "How do I install Docker on Ubuntu?"

# Calculations
astros-cli "Convert 100 USD to EUR"
```

### Python Integration

```python
#!/usr/bin/env python3
import asyncio
import sys
sys.path.insert(0, '/usr/lib/astros/agent')

from astros import AstrOSAgent

async def main():
    agent = AstrOSAgent()
    response = await agent.get_response("Hello!")
    print(response)

asyncio.run(main())
```

---

## 🔧 Service Management

### Systemd Service

#### Check Status

```bash
# Check if running
sudo systemctl status astros-agent@$(whoami)

# Short status
systemctl is-active astros-agent@$(whoami)
```

#### Start/Stop Service

```bash
# Start
sudo systemctl start astros-agent@$(whoami)

# Stop
sudo systemctl stop astros-agent@$(whoami)

# Restart
sudo systemctl restart astros-agent@$(whoami)
```

#### Enable/Disable Auto-start

```bash
# Enable (start on boot)
sudo systemctl enable astros-agent@$(whoami)

# Disable
sudo systemctl disable astros-agent@$(whoami)
```

#### View Logs

```bash
# Live logs (follow)
journalctl -u astros-agent@$(whoami) -f

# Last 50 lines
journalctl -u astros-agent@$(whoami) -n 50

# Today's logs
journalctl -u astros-agent@$(whoami) --since today

# Logs with errors
journalctl -u astros-agent@$(whoami) -p err
```

### Health Monitoring

```bash
# Quick health check
cd /mnt/d/AstrOS
./health-check.sh

# Process check
ps aux | grep astros

# Memory usage
systemctl show astros-agent@$(whoami) --property=MemoryMax,MemoryCurrent
```

---

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check logs
journalctl -u astros-agent@$(whoami) -n 50

# Common issues:
# 1. Missing API key
nano ~/.config/astros/agent.env

# 2. Virtualenv issues
rm -rf ~/.local/share/astros/venv
sudo dpkg-reconfigure astros-core

# 3. Permission issues
sudo chown -R $(whoami):$(whoami) ~/.config/astros
sudo chown -R $(whoami):$(whoami) ~/.local/share/astros
```

### API Errors

```bash
# Test API connection
astros-cli "test"

# Check API key
grep ASTROS_API_KEY ~/.config/astros/agent.env

# Verify key at: https://openrouter.ai/keys
```

### CLI Not Working

```bash
# Check if installed
which astros-cli

# Check permissions
ls -la /usr/bin/astros-cli

# Test manually
python3 /usr/bin/astros-cli "test"

# Reinstall if needed
sudo dpkg -r astros-core
sudo dpkg -i packages/astros-core.deb
```

### High Memory Usage

```bash
# Check current usage
systemctl show astros-agent@$(whoami) --property=MemoryCurrent

# Restart service
sudo systemctl restart astros-agent@$(whoami)

# Adjust limits (edit service file)
sudo nano /etc/systemd/system/astros-agent@.service
# Change MemoryLimit=512M to desired value
sudo systemctl daemon-reload
sudo systemctl restart astros-agent@$(whoami)
```

---

## 💻 Development

### Build from Source

```bash
# Clone repository
git clone https://github.com/CoreOrganizations/AstrOS.git
cd AstrOS

# Setup development environment
./setup-venv.sh

# Test agent
source ~/.local/share/astros/venv/bin/activate
python3 astros.py
```

### Build Package

```bash
# Build .deb package
./build-package.sh

# Package will be at: packages/astros-core.deb
```

### Run Tests

```bash
# Functional tests
source ~/.local/share/astros/venv/bin/activate
python3 test-agent.py

# Health check
./health-check.sh

# Package test
./test-package.sh
```

### Development Workflow

```bash
# 1. Make changes to source files
nano astros.py

# 2. Test locally
./run-agent.sh

# 3. Build package
./build-package.sh

# 4. Test package
./test-package.sh

# 5. Commit changes
git add .
git commit -m "Description"
git push
```

---

## 📦 Package Management

### Install Package

```bash
# Standard installation
sudo dpkg -i packages/astros-core.deb

# Fix dependencies
sudo apt-get install -f
```

### Update Package

```bash
# Remove old version
sudo dpkg -r astros-core

# Install new version
sudo dpkg -i packages/astros-core.deb

# Or use upgrade
sudo dpkg -i packages/astros-core.deb
```

### Remove Package

```bash
# Remove package (keep config)
sudo dpkg -r astros-core

# Purge (remove everything)
sudo dpkg -P astros-core

# Manual cleanup
rm -rf ~/.config/astros
rm -rf ~/.local/share/astros
```

### Package Information

```bash
# Show package info
dpkg -l | grep astros-core

# Package files
dpkg -L astros-core

# Package status
dpkg -s astros-core
```

---

## 🔬 Advanced Topics

### Custom Model Configuration

```bash
# Edit config
nano ~/.config/astros/agent.env

# Available models:
# - mistralai/ministral-8b (default, fast)
# - openai/gpt-3.5-turbo (more capable)
# - anthropic/claude-3-haiku (balanced)
# - google/gemini-pro (free tier)

# Example:
ASTROS_AI_MODEL__NAME=openai/gpt-3.5-turbo
ASTROS_AI_MODEL__MAX_TOKENS=4096
ASTROS_AI_MODEL__TEMPERATURE=0.8

# Restart service
sudo systemctl restart astros-agent@$(whoami)
```

### Multi-User Setup

```bash
# Install once
sudo dpkg -i packages/astros-core.deb

# Configure for each user
su - user1
nano ~/.config/astros/agent.env
# Add API key
exit

su - user2
nano ~/.config/astros/agent.env
# Add API key
exit

# Enable services
sudo systemctl enable astros-agent@user1
sudo systemctl enable astros-agent@user2

# Start services
sudo systemctl start astros-agent@user1
sudo systemctl start astros-agent@user2
```

### Resource Limits

```bash
# Edit service file
sudo nano /etc/systemd/system/astros-agent@.service

# Adjust limits:
MemoryLimit=512M       # Max RAM
CPUQuota=50%           # Max CPU
RestartSec=10          # Restart delay

# Apply changes
sudo systemctl daemon-reload
sudo systemctl restart astros-agent@$(whoami)
```

### Backup Configuration

```bash
# Backup config
cp ~/.config/astros/agent.env ~/astros-backup.env

# Restore config
cp ~/astros-backup.env ~/.config/astros/agent.env
chmod 600 ~/.config/astros/agent.env
```

### Environment Variables

```bash
# Override config temporarily
ASTROS_AI_MODEL__NAME=openai/gpt-4 astros-cli "test"

# Export for session
export ASTROS_AI_MODEL__NAME=openai/gpt-4
astros-cli "test"
```

---

## 📊 Performance Tips

### Optimize Response Time

1. **Use faster models**: `ministral-8b` is fastest
2. **Reduce max_tokens**: Lower values = faster
3. **Lower temperature**: 0.5-0.7 for speed
4. **Keep conversations short**: Clear history periodically

### Reduce Memory Usage

1. **Restart service daily**: `sudo systemctl restart astros-agent@$(whoami)`
2. **Lower memory limit**: Edit service file
3. **Disable unused features**: Remove plugins
4. **Use lighter models**: Smaller models use less RAM

### Improve Accuracy

1. **Use better models**: `gpt-3.5-turbo`, `claude-3-haiku`
2. **Increase max_tokens**: Allow longer responses
3. **Adjust temperature**: 0.7-0.9 for creativity
4. **Provide context**: More detailed questions

---

## 🔐 Security

### API Key Security

```bash
# Config file permissions
chmod 600 ~/.config/astros/agent.env

# Check permissions
ls -la ~/.config/astros/agent.env
# Should show: -rw-------

# Never commit API keys to git
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
```

### Service Security

The service runs with these security features:

- ✅ NoNewPrivileges (no privilege escalation)
- ✅ PrivateTmp (isolated /tmp)
- ✅ ProtectSystem (read-only system files)
- ✅ ProtectHome (limited home access)
- ✅ Memory limits (512MB max)
- ✅ CPU limits (50% max)

---

## 📞 Support

### Get Help

- **Documentation**: https://github.com/CoreOrganizations/AstrOS
- **Discord**: https://discord.gg/9qQstuyt
- **Email**: aiastros2025@gmail.com
- **Issues**: https://github.com/CoreOrganizations/AstrOS/issues

### Report Bugs

```bash
# Collect debug info
journalctl -u astros-agent@$(whoami) -n 100 > debug.log
systemctl status astros-agent@$(whoami) >> debug.log
cat ~/.config/astros/agent.env | grep -v API_KEY >> debug.log

# Submit to GitHub Issues with debug.log
```

---

## 🎓 Common Commands Reference

```bash
# Installation
sudo dpkg -i packages/astros-core.deb

# Configuration
nano ~/.config/astros/agent.env

# Service Control
sudo systemctl start astros-agent@$(whoami)
sudo systemctl stop astros-agent@$(whoami)
sudo systemctl restart astros-agent@$(whoami)
sudo systemctl status astros-agent@$(whoami)

# Enable/Disable
sudo systemctl enable astros-agent@$(whoami)
sudo systemctl disable astros-agent@$(whoami)

# Logs
journalctl -u astros-agent@$(whoami) -f

# Usage
astros-cli "your question here"

# Health Check
./health-check.sh

# Testing
./test-agent.py
./test-package.sh

# Building
./build-package.sh

# Removal
sudo dpkg -r astros-core
```

---

## 📝 Files and Directories

```
System Files:
  /usr/lib/astros/agent/           # Agent code
  /usr/bin/astros-cli              # CLI tool
  /etc/systemd/system/astros-agent@.service  # Service

User Files:
  ~/.config/astros/agent.env       # Configuration
  ~/.local/share/astros/venv/      # Virtual environment

Logs:
  journalctl -u astros-agent@...   # Service logs

Package:
  packages/astros-core.deb         # Installation package
```

---

## ✅ Checklist

### Initial Setup
- [ ] Install Ubuntu 24.04 (or WSL2)
- [ ] Get OpenRouter API key
- [ ] Install package: `sudo dpkg -i packages/astros-core.deb`
- [ ] Configure API key in `~/.config/astros/agent.env`
- [ ] Enable service: `sudo systemctl enable astros-agent@$(whoami)`
- [ ] Start service: `sudo systemctl start astros-agent@$(whoami)`
- [ ] Test CLI: `astros-cli "test"`

### Daily Use
- [ ] Check service status: `sudo systemctl status astros-agent@$(whoami)`
- [ ] Use CLI: `astros-cli "your question"`
- [ ] Monitor logs: `journalctl -u astros-agent@$(whoami) -f`

### Troubleshooting
- [ ] Check logs for errors
- [ ] Verify API key is set
- [ ] Restart service
- [ ] Run health check
- [ ] Check internet connection

---

**🎉 You're all set! Start using AstrOS with `astros-cli`!**

*For more help, visit: https://github.com/CoreOrganizations/AstrOS*
