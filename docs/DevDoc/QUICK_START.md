# 🎯 Quick Start: Building AstrOS

**Get started with AstrOS development in 15 minutes**

---

## 🚀 What You'll Build

A complete Ubuntu-based operating system with native AI integration that:
- Runs AI as a system service (like networking or audio)
- Responds to Super+Space keyboard shortcut
- Provides natural language system control
- Works with MistralAI Ministral 8B model

---

## ⚡ Quick Setup (15 minutes)

### Step 1: Clone & Configure (5 min)

```bash
# Clone repository
git clone https://github.com/CoreOrganizations/AstrOS.git
cd AstrOS

# Copy environment file
cp .env.example .env

# Edit .env and add your OpenRouter API key
nano .env
# Set: ASTROS_API_KEY=sk-or-v1-your-key-here
```

### Step 2: Install Dependencies (5 min)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Validate setup
python validate_env.py
```

### Step 3: Test AI Agent (5 min)

```bash
# Run the AI agent
python astros.py

# Try these questions:
# - Hello! What model are you using?
# - What is quantum computing?
# - Calculate 456 * 789
```

**✅ If you see AI responses, you're ready to develop!**

---

## 📚 What to Read Next

### For Your Role

**👤 I want to USE AstrOS**
1. Wait for our first release (Q1 2025)
2. Join Discord for updates: https://discord.gg/9qQstuyt
3. Star the repo to get notified

**👨‍💻 I want to CONTRIBUTE to AstrOS**
1. Read [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
2. Check [STAGE_0_FOUNDATION.md](STAGE_0_FOUNDATION.md)
3. Pick a task from [STAGE_0_CHECKLIST.md](STAGE_0_CHECKLIST.md)
4. Join Discord: https://discord.gg/9qQstuyt

**🔌 I want to BUILD PLUGINS**
1. Read [STAGE_1_DESKTOP_PLUGINS.md](STAGE_1_DESKTOP_PLUGINS.md)
2. Check plugin examples in Stage 1 guide
3. Wait for Stage 1 (Q2 2025) or start early

**📝 I want to HELP with DOCS**
1. Check [README.md](README.md) in docs folder
2. Look for docs labeled "Coming soon"
3. Create PRs with improvements

---

## 🗺️ Development Roadmap Overview

```
2025 Timeline:

Q1 (Jan-Mar)  ███████░░░░░░░░░░░░░░ Stage 0: Foundation
              └─ Bootable ISO with basic AI

Q2 (Apr-Jun)  ░░░░░░░███████░░░░░░░░ Stage 1: Desktop & Plugins
              └─ Native UI, plugin system

Q3 (Jul-Sep)  ░░░░░░░░░░░░░░███████░ Stage 2: Integration
              └─ Voice, automation, 7+ plugins

Q4 (Oct-Dec)  ░░░░░░░░░░░░░░░░░░░░░ Stage 3: Polish
              └─ Production ready, v1.0.0

2026+         ░░░░░░░░░░░░░░░░░░░░░ Stage 4: Advanced
              └─ Multi-modal AI, variants
```

---

## 📖 Essential Documentation

### Start Here
- **[README.md](../README.md)** - What is AstrOS?
- **[ROADMAP.md](../ROADMAP.md)** - Full development plan
- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)** - Complete dev guide

### Current Stage (Stage 0)
- **[STAGE_0_FOUNDATION.md](STAGE_0_FOUNDATION.md)** - Week-by-week guide
- **[STAGE_0_CHECKLIST.md](STAGE_0_CHECKLIST.md)** - Track your progress

### Setup & Config
- **[API_SETUP.md](API_SETUP.md)** - Configure API keys
- **[ENV_SETUP.md](ENV_SETUP.md)** - Environment variables
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Installation guide

### Reference
- **[docs/README.md](README.md)** - Documentation index
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference

---

## 🎯 Current Focus

**We're currently in Stage 0: Building Foundation**

### What We're Building Now
- ISO build pipeline with live-build
- Systemd service for AI agent
- GNOME Shell extension
- First bootable AstrOS ISO

### How You Can Help
1. **ISO Building** (High Priority 🔴)
   - Test build scripts
   - Document build process
   - Fix ISO build issues

2. **AI Agent Service** (High Priority 🔴)
   - Systemd service implementation
   - D-Bus integration
   - Error handling

3. **Testing** (High Priority 🔴)
   - Test on different hardware
   - Report bugs
   - Write test cases

4. **Documentation** (Medium Priority 🟡)
   - Improve guides
   - Create tutorials
   - Add examples

---

## 💻 Development Commands

### Test Current Agent
```bash
# Run AI agent locally
python astros.py

# Validate configuration
python validate_env.py

# Check for errors
python -m pytest tests/
```

### Build ISO (Stage 0)
```bash
# Navigate to builder
cd iso-builder

# Build ISO
sudo ./build-iso.sh

# Test in VM
../tools/test-vm.sh *.iso
```

### Install Agent (Stage 0)
```bash
# Install locally for testing
./scripts/install-agent.sh

# Start service
sudo systemctl start astros-agent

# Check status
sudo systemctl status astros-agent

# View logs
sudo journalctl -u astros-agent -f
```

---

## 🤝 Get Involved

### Join the Community
- **Discord**: https://discord.gg/9qQstuyt (Most active!)
- **GitHub**: https://github.com/CoreOrganizations/AstrOS
- **Email**: aiastros2025@gmail.com

### Weekly Schedule
- **Monday**: Week planning (Discord voice)
- **Wednesday**: Office hours (2pm UTC)
- **Friday**: Sprint review (3pm UTC)

### Communication Channels
- `#general` - General discussion
- `#development` - Dev questions
- `#stage-0` - Current stage work
- `#help` - Get unstuck
- `#documentation` - Docs discussion

---

## 🐛 Found an Issue?

### Bug Reports
1. Check if already reported
2. Create GitHub issue with `bug` label
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - System info
   - Logs if applicable

### Security Issues
**Do NOT create public issues!**
- Email: aiastros2025@gmail.com
- We'll respond within 48 hours

---

## 🌟 Quick Wins

**Want to contribute but not sure where to start?** Try these:

### Easy (Good First Issues)
- [ ] Fix typos in documentation
- [ ] Add examples to guides
- [ ] Test installation on different systems
- [ ] Report detailed bug reports
- [ ] Improve error messages

### Medium
- [ ] Write unit tests
- [ ] Create GitHub Actions workflows
- [ ] Document common issues
- [ ] Create video tutorials
- [ ] Improve build scripts

### Advanced
- [ ] Implement systemd service
- [ ] Create GNOME extension
- [ ] Build .deb packages
- [ ] Optimize ISO size
- [ ] Add plugin system

---

## 📊 Project Status

### Current Stage
**Stage 0: Build Foundation** (2-3 months)
- Started: October 2025
- Target Completion: December 2025
- Progress: ~40% (Week 3-4)

### What's Working
✅ AI agent with MistralAI Ministral 8B  
✅ Environment configuration  
✅ API key management  
✅ Basic conversation handling  

### What's In Progress
🔄 ISO build pipeline  
🔄 Systemd service implementation  
🔄 GNOME Shell extension  

### What's Next
⏳ First bootable ISO  
⏳ Desktop integration  
⏳ First alpha release (v0.1.0)  

---

## 🎓 Learning Resources

### Ubuntu/Linux
- [Ubuntu Live-Build Manual](https://live-team.pages.debian.net/live-manual/)
- [Systemd Documentation](https://www.freedesktop.org/software/systemd/man/)
- [Debian Package Guide](https://www.debian.org/doc/manuals/maint-guide/)

### GNOME Development
- [GNOME Developer Center](https://developer.gnome.org/)
- [GJS Guide](https://gjs.guide/)
- [GNOME Shell Extensions](https://wiki.gnome.org/Projects/GnomeShell/Extensions)

### D-Bus
- [D-Bus Tutorial](https://dbus.freedesktop.org/doc/dbus-tutorial.html)
- [D-Bus Specification](https://dbus.freedesktop.org/doc/dbus-specification.html)

### AI Integration
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [MistralAI Documentation](https://docs.mistral.ai/)

---

## 🎉 Success Stories

### Milestones Achieved
- ✅ Project structure defined
- ✅ AI agent working with MistralAI
- ✅ Environment configuration system
- ✅ Documentation framework
- ✅ Community Discord active

### Coming Soon
- 🔜 First bootable ISO
- 🔜 GNOME Shell extension
- 🔜 Alpha release v0.1.0
- 🔜 Plugin system
- 🔜 Voice integration

---

## 💡 Tips for Success

### For New Contributors
1. **Start Small** - Fix typos, improve docs
2. **Ask Questions** - We're friendly on Discord!
3. **Read the Guides** - Especially Stage 0
4. **Test Often** - Validate your changes
5. **Document** - Help others learn

### For Development
1. **One Feature at a Time** - Don't overwhelm yourself
2. **Test in VM** - Don't break your main system
3. **Commit Often** - Small, focused commits
4. **Ask for Review** - Get feedback early
5. **Celebrate Wins** - Every contribution matters!

---

## 🚀 Ready to Start?

### Checklist Before You Begin
- [ ] Repository cloned
- [ ] API key configured
- [ ] Dependencies installed
- [ ] Agent tested successfully
- [ ] Joined Discord community
- [ ] Read Stage 0 guide
- [ ] Picked a task from checklist

### Your First Task
1. Go to [STAGE_0_CHECKLIST.md](STAGE_0_CHECKLIST.md)
2. Find an incomplete task you can help with
3. Comment on related GitHub issue (or create one)
4. Ask for guidance in Discord #stage-0
5. Start coding! 🎉

---

## 📞 Need Help?

**Don't hesitate to ask!** We're here to help:

- 💬 **Discord #help** - Quick questions
- 📧 **Email** - aiastros2025@gmail.com
- 🐛 **GitHub Issues** - Bugs and features
- 📖 **Documentation** - Read the guides

---

**Welcome to AstrOS! Let's build the future of operating systems together!** 🚀

---

*Last Updated: October 2025*  
*Current Version: 0.1.0-dev*  
*Current Stage: Stage 0 - Build Foundation*
