# Stage 0 Checklist - Build Foundation 🏗️

**Complete checklist for Stage 0 development**

Use this checklist to track your progress through Stage 0. Mark items as you complete them!

---

## Week 1-2: Development Environment Setup ✅

### Day 1-2: System Setup
- [ ] Ubuntu 24.04 LTS installed (or VM ready)
- [ ] System fully updated (`sudo apt update && upgrade`)
- [ ] Git configured with name and email
- [ ] GitHub SSH keys set up
- [ ] Repository cloned locally

### Day 3-4: Build Tools Installation
- [ ] live-build installed and tested (`lb --version`)
- [ ] debootstrap installed (`debootstrap --version`)
- [ ] squashfs-tools installed
- [ ] xorriso and genisoimage installed
- [ ] Python 3.12+ verified (`python3 --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm installed (`npm --version`)

### Day 5-7: Project Structure
- [ ] Directory structure created:
  ```
  ~/AstrOS-Builder/
  ├── iso-builder/
  ├── packages/
  ├── overlays/
  ├── scripts/
  └── configs/
  ```
- [ ] Git repository initialized
- [ ] Remote origin configured
- [ ] Initial commit pushed

### Day 8-10: ISO Build Pipeline
- [ ] live-build configured (`lb config`)
- [ ] `auto/config` script created
- [ ] `build-iso.sh` script created and executable
- [ ] Script permissions set (`chmod +x build-iso.sh`)

### Day 11-14: First Build Test
- [ ] Test ISO build executed
- [ ] Build completed without errors
- [ ] ISO file created (check size)
- [ ] ISO boots in VM (test with VirtualBox/VMware)
- [ ] Boot process verified

### Week 1-2 Deliverables
- [ ] **Deliverable 1**: Working build pipeline
- [ ] **Deliverable 2**: Automated build script
- [ ] **Deliverable 3**: Test ISO created
- [ ] **Deliverable 4**: Documentation updated

---

## Week 3-4: Core AI Agent Integration 🤖

### Day 15-16: Service File Creation
- [ ] `configs/astros-agent.service` created
- [ ] Service file syntax validated
- [ ] Security settings configured
- [ ] Auto-restart configured

### Day 17-19: Daemon Implementation
- [ ] `astros_daemon.py` created
- [ ] Logging configured
- [ ] Import path set up correctly
- [ ] Error handling added
- [ ] Graceful shutdown implemented

### Day 20-21: Keyring Integration
- [ ] `keyring_manager.py` created
- [ ] GNOME Keyring integration tested
- [ ] Fallback to .env file working
- [ ] API key storage tested
- [ ] API key retrieval tested

### Day 22-24: Installation Script
- [ ] `install-agent.sh` created
- [ ] Directory creation working
- [ ] File copying working
- [ ] Service installation working
- [ ] Dependencies installation working

### Day 25-28: Testing & Validation
- [ ] Agent installed on test system
- [ ] Service starts successfully
- [ ] Service status shows active
- [ ] Logs accessible (`journalctl -u astros-agent`)
- [ ] Agent responds to requests
- [ ] API integration working
- [ ] Error cases handled gracefully

### Week 3-4 Deliverables
- [ ] **Deliverable 1**: `astros-agent.service` working
- [ ] **Deliverable 2**: `astros_daemon.py` functional
- [ ] **Deliverable 3**: Secure key storage
- [ ] **Deliverable 4**: Installation script
- [ ] **Deliverable 5**: Service running on test VM

---

## Week 5-8: First Bootable ISO 💿

### Day 29-31: Package Structure
- [ ] `packages/astros-core/` directory created
- [ ] DEBIAN control file created
- [ ] Package metadata filled out
- [ ] Version number set
- [ ] Dependencies listed

### Day 32-35: Package Files
- [ ] Agent files copied to package
- [ ] Service file included
- [ ] Directory structure correct:
  ```
  astros-core/
  ├── DEBIAN/
  │   ├── control
  │   ├── postinst
  │   └── prerm
  ├── usr/
  │   ├── lib/astros/agent/
  │   └── bin/
  └── etc/
      └── systemd/system/
  ```

### Day 36-38: Post-Install Scripts
- [ ] `postinst` script created
- [ ] Script installs dependencies
- [ ] Script creates directories
- [ ] Script enables service
- [ ] Script provides user feedback
- [ ] Script executable (`chmod 755`)

### Day 39-42: Package Building
- [ ] .deb package built successfully
- [ ] Package info verified (`dpkg-deb --info`)
- [ ] Package contents checked (`dpkg-deb --contents`)
- [ ] Package installs on test system
- [ ] Agent works after package install

### Day 43-46: First-Boot Wizard
- [ ] GTK4 wizard created
- [ ] UI layout complete
- [ ] API key input field
- [ ] Validation logic working
- [ ] Service start integrated
- [ ] Success/error messages

### Day 47-52: ISO Integration
- [ ] Package copied to ISO build
- [ ] Hook script created for installation
- [ ] Hook script tested
- [ ] First-boot wizard included
- [ ] Auto-start configured
- [ ] Full ISO build successful

### Day 53-56: Testing & Validation
- [ ] ISO boots in VM
- [ ] Installation completes
- [ ] First-boot wizard appears
- [ ] API key configuration works
- [ ] Agent starts after setup
- [ ] All features functional

### Week 5-8 Deliverables
- [ ] **Deliverable 1**: `astros-core.deb` package
- [ ] **Deliverable 2**: First-boot wizard
- [ ] **Deliverable 3**: Complete bootable ISO
- [ ] **Deliverable 4**: ISO tested and validated
- [ ] **Deliverable 5**: ISO size < 3GB

---

## Week 9-12: Basic Desktop Integration 🖥️

### Day 57-60: GNOME Extension Setup
- [ ] Extension directory created
- [ ] `metadata.json` created
- [ ] Extension UUID set
- [ ] Shell version specified
- [ ] Basic structure in place

### Day 61-65: Extension Development
- [ ] `extension.js` created
- [ ] Indicator icon added to panel
- [ ] Menu created
- [ ] Click handler working
- [ ] Extension loads without errors

### Day 66-70: Global Hotkey
- [ ] Hotkey binding registered (Super+Space)
- [ ] Hotkey triggers extension
- [ ] Extension shows/hides window
- [ ] No conflicts with system hotkeys
- [ ] Hotkey customizable

### Day 71-75: Quick Chat Dialog
- [ ] GTK4 quick chat created
- [ ] Input field functional
- [ ] AI response display working
- [ ] D-Bus communication set up
- [ ] Agent called successfully
- [ ] Response shown to user

### Day 76-80: System Tray Integration
- [ ] Tray icon visible
- [ ] Status indicator working
- [ ] Menu accessible
- [ ] Status updates in real-time
- [ ] Icon changes with state

### Day 81-84: Packaging & Integration
- [ ] Extension packaged (`gnome-extensions pack`)
- [ ] Extension added to ISO
- [ ] Extension auto-enables on first boot
- [ ] Quick chat in system path
- [ ] Desktop file created

### Week 9-12 Deliverables
- [ ] **Deliverable 1**: GNOME extension working
- [ ] **Deliverable 2**: System tray icon
- [ ] **Deliverable 3**: Super+Space hotkey
- [ ] **Deliverable 4**: Quick chat dialog
- [ ] **Deliverable 5**: Full integration in ISO

---

## Stage 0 Success Criteria ✅

### Must Have (Required for completion)
- [ ] ✅ Bootable ISO that installs Ubuntu + AstrOS
- [ ] ✅ AI agent runs automatically on login
- [ ] ✅ Can interact via Super+Space keyboard shortcut
- [ ] ✅ ISO size < 3GB
- [ ] ✅ Agent connects to MistralAI successfully
- [ ] ✅ First-boot setup wizard completes configuration
- [ ] ✅ No critical bugs or crashes

### Nice to Have (Optional enhancements)
- [ ] ⭐ Custom boot splash screen
- [ ] ⭐ AstrOS branding on desktop (wallpaper, theme)
- [ ] ⭐ System notifications for agent status
- [ ] ⭐ Agent status in system tray
- [ ] ⭐ Quick access keyboard shortcuts documented
- [ ] ⭐ Video demo/tutorial created

---

## Testing Checklist 🧪

### Pre-Release Testing
- [ ] **Installation Test**
  - [ ] ISO boots on bare metal
  - [ ] ISO boots in VirtualBox
  - [ ] ISO boots in VMware
  - [ ] Installation completes without errors
  - [ ] Post-install system boots correctly

- [ ] **Agent Test**
  - [ ] Service starts automatically
  - [ ] API connection established
  - [ ] Simple queries work
  - [ ] Complex queries work
  - [ ] Error handling works
  - [ ] Service restarts after crash

- [ ] **Desktop Integration Test**
  - [ ] GNOME extension loads
  - [ ] System tray icon appears
  - [ ] Super+Space opens dialog
  - [ ] Dialog accepts input
  - [ ] Dialog shows responses
  - [ ] Dialog can be closed

- [ ] **Performance Test**
  - [ ] Boot time < 60 seconds
  - [ ] Agent startup < 10 seconds
  - [ ] Response time < 3 seconds
  - [ ] Memory usage < 500MB idle
  - [ ] CPU usage < 10% idle

### Hardware Compatibility
- [ ] **Tested On**:
  - [ ] Intel processor
  - [ ] AMD processor
  - [ ] NVIDIA graphics
  - [ ] AMD graphics
  - [ ] Intel graphics
  - [ ] Laptop with WiFi
  - [ ] Desktop with Ethernet

---

## Documentation Checklist 📚

### User Documentation
- [ ] Installation guide created
- [ ] First-boot tutorial written
- [ ] Keyboard shortcuts documented
- [ ] API setup guide complete
- [ ] Troubleshooting section added
- [ ] FAQ created

### Developer Documentation
- [ ] Stage 0 guide complete (this document)
- [ ] Build process documented
- [ ] Service architecture explained
- [ ] Extension development notes
- [ ] Contributing guidelines updated

### Project Documentation
- [ ] README updated with Stage 0 status
- [ ] ROADMAP updated
- [ ] CHANGELOG updated
- [ ] Release notes prepared

---

## Release Checklist 🚀

### Pre-Release
- [ ] All success criteria met
- [ ] All critical bugs fixed
- [ ] Documentation complete
- [ ] Testing complete
- [ ] Code reviewed

### Release Process
- [ ] Version number updated (v0.1.0-alpha)
- [ ] Git tag created
- [ ] ISO uploaded to release server
- [ ] SHA256 checksums generated
- [ ] Release notes published
- [ ] GitHub release created

### Post-Release
- [ ] Announcement on Discord
- [ ] Tweet about release
- [ ] Email to mailing list
- [ ] Community feedback collected
- [ ] Bugs triaged
- [ ] Stage 1 planning begins

---

## Progress Tracking 📊

### Overall Progress

```
Stage 0: Build Foundation
███████████░░░░░░░░░░░░░░░░░ 40% Complete

Week 1-2: Environment Setup     ████████████████████ 100%
Week 3-4: Agent Integration     ██████████░░░░░░░░░░  50%
Week 5-8: Bootable ISO          ░░░░░░░░░░░░░░░░░░░░   0%
Week 9-12: Desktop Integration  ░░░░░░░░░░░░░░░░░░░░   0%
```

### Current Sprint
- **Sprint**: Week 3-4 (Day 15-28)
- **Focus**: Core AI Agent Integration
- **Status**: In Progress
- **Next**: Bootable ISO Development

---

## Notes & Issues 📝

### Blockers
- [ ] Issue #1: Description
- [ ] Issue #2: Description

### Questions
- [ ] Question 1: To be answered
- [ ] Question 2: To be answered

### Ideas for Improvement
- [ ] Idea 1: Description
- [ ] Idea 2: Description

---

## Team & Responsibilities 👥

### Core Team
- **Project Lead**: TBD
- **ISO Builder**: TBD
- **Agent Developer**: TBD
- **Desktop Integration**: TBD
- **Testing**: TBD
- **Documentation**: TBD

### Communication
- **Daily Standup**: Discord voice (Time TBD)
- **Weekly Review**: Discord (Fridays 3pm UTC)
- **Sprint Planning**: Start of each week
- **Retrospective**: End of each 2-week sprint

---

## Resources 🔗

### Documentation
- [Stage 0 Guide](STAGE_0_FOUNDATION.md)
- [Development Guide](DEVELOPMENT_GUIDE.md)
- [API Setup](API_SETUP.md)

### Tools
- [live-build Manual](https://live-team.pages.debian.net/live-manual/)
- [Systemd Documentation](https://www.freedesktop.org/software/systemd/man/)
- [GNOME Developer Docs](https://developer.gnome.org/)

### Community
- Discord: https://discord.gg/9qQstuyt
- GitHub: https://github.com/CoreOrganizations/AstrOS
- Email: aiastros2025@gmail.com

---

**Keep this checklist updated as you progress!** ✅

*Last Updated: October 2025*
