# AstrOS Desktop GUI - User Guide

## Overview

AstrOS Desktop provides a beautiful, modern graphical interface for interacting with your AI assistant. Built with GTK4 and Adwaita, it seamlessly integrates with your Linux desktop.

---

## Features

### 🎨 Modern Chat Interface
- Clean, bubble-style chat UI
- User messages in blue, AI responses in gray
- Smooth scrolling and animations
- Message history preserved during session

### ⚡ Quick Actions
- Send messages with Ctrl+Enter
- Clear chat history with one click
- Easy access to settings
- Keyboard shortcuts for power users

### 🔔 Desktop Integration
- Application menu integration
- System notifications (coming soon)
- Minimize to tray (coming soon)
- Auto-start option (coming soon)

---

## Installation

### Prerequisites
```bash
# Install dependencies
./setup-gui-dependencies.sh

# Or manually:
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libadwaita-1-0
```

### Running the GUI

**Option 1: From source**
```bash
cd /path/to/AstrOS
python3 gui/app.py
```

**Option 2: Installed package** (coming soon)
```bash
astros-gui
```

### WSL2 Setup

If using WSL2, you need an X server:

1. **Install VcXsrv on Windows**
   - Download from: https://sourceforge.net/projects/vcxsrv/
   - Run XLaunch with default settings

2. **Configure WSL**
   ```bash
   # Add to ~/.bashrc
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
   export LIBGL_ALWAYS_INDIRECT=1
   
   # Reload
   source ~/.bashrc
   ```

3. **Test**
   ```bash
   python3 gui/app.py
   ```

---

## Using the GUI

### First Launch

1. **Launch the application**
   ```bash
   python3 gui/app.py
   ```

2. **You'll see the main chat window**
   - Welcome message from AstrOS
   - Text input at the bottom
   - Send button (or press Enter)

### Sending Messages

1. **Type your message** in the input field at the bottom
2. **Press Enter** or click the Send button
3. **Wait for response** - you'll see "💭 Thinking..." while processing
4. **View the response** - appears as a gray bubble

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Ctrl+Q` | Quit application |
| `Ctrl+,` | Open settings (coming soon) |
| `Ctrl+L` | Clear chat history (coming soon) |

### Menu Options

Click the **☰** menu button (top right) to access:

- **Settings** - Configure API key, model, etc. (coming soon)
- **About** - View app information and version
- **Quit** - Close the application

### Clearing Chat History

Click the **clear icon** (🗑️) in the top left to clear all messages except the welcome message.

---

## Configuration

### API Key Setup

The GUI uses the same configuration as the CLI:

```bash
# Edit config file
nano ~/.config/astros/agent.env

# Add your API key
ASTROS_API_KEY=your_key_here
```

### Settings Window (Coming Soon)

Future releases will include a visual settings interface for:
- API key management
- Model selection
- Response customization
- Appearance options
- Notification preferences

---

## Troubleshooting

### GUI won't start

**Problem**: Import errors or missing dependencies

**Solution**:
```bash
# Install dependencies
./setup-gui-dependencies.sh

# Test imports
python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk"
```

### No responses from AI

**Problem**: Agent not configured

**Solution**:
```bash
# Check config file exists
cat ~/.config/astros/agent.env

# Verify API key is set
grep ASTROS_API_KEY ~/.config/astros/agent.env

# Test CLI first
astros-cli "Hello"
```

### WSL2: Can't connect to display

**Problem**: DISPLAY variable not set or X server not running

**Solution**:
```bash
# Check DISPLAY
echo $DISPLAY

# Set DISPLAY
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

# Make sure VcXsrv is running on Windows
# Check "Disable access control" in XLaunch settings
```

### Window too small/large

**Problem**: Default size doesn't fit your screen

**Solution**:
- Resize the window manually (it will remember size in future versions)
- Minimum size: 600x400px
- Recommended: 800x600px or larger

---

## Tips & Tricks

### Efficient Chatting

1. **Press Enter to send** - No need to click
2. **Use clear, specific questions** - Better responses
3. **Review chat history** - Scroll up to see previous messages
4. **Copy responses** - Select text in AI bubbles to copy

### Performance

- **Keep chat history reasonable** - Clear old messages if chat gets slow
- **One question at a time** - Wait for response before sending next
- **Check service status** - Ensure backend is running:
  ```bash
  sudo systemctl status astros-agent@$(whoami)
  ```

### Best Practices

- Configure API key before first use
- Start with simple questions to test
- Use the CLI for automation/scripting
- Use the GUI for interactive conversations
- Clear chat when changing topics

---

## Known Limitations (Current Version)

- [ ] No system tray icon yet (GTK4 migration)
- [ ] Settings must be edited in config file
- [ ] No conversation persistence across sessions
- [ ] No notification support yet
- [ ] No keyboard shortcut customization

These will be addressed in future releases!

---

## Screenshots

### Main Window
```
┌────────────────────────────────────┐
│ ☰ AstrOS          🗑️  [-][□][×]   │
├────────────────────────────────────┤
│ 👋 Hello! I'm AstrOS...            │
│                                    │
│              ┌──────────────┐      │
│    Hello!    │              │      │
│              └──────────────┘      │
│                                    │
│ ┌────────────────────────┐         │
│ │ Hi! How can I help?    │         │
│ └────────────────────────┘         │
│                                    │
├────────────────────────────────────┤
│ Type your message...      [Send]📤 │
└────────────────────────────────────┘
```

---

## Future Features

### Coming Soon
- 🔔 Desktop notifications
- 💾 Chat history persistence
- 🎨 Theme customization
- ⌨️ Custom keyboard shortcuts
- 📋 Copy/export conversations

### Planned
- 🗣️ Voice input/output
- 🔌 Plugin system
- 📱 Mobile companion app
- 🌐 Web interface
- 🤖 Multiple AI assistants

---

## Getting Help

### Resources
- **Documentation**: `docs/`
- **CLI Guide**: `docs/CLI_CHAT_GUIDE.md`
- **Installation**: `docs/INSTALLATION_GUIDE.md`

### Support
- **GitHub Issues**: https://github.com/CoreOrganizations/AstrOS/issues
- **Discord**: https://discord.gg/9qQstuyt
- **Email**: support@astros.ai

### Reporting Bugs
When reporting GUI bugs, include:
1. Your OS and version
2. GTK version: `gtk4-demo --version`
3. Python version: `python3 --version`
4. Error messages from terminal
5. Steps to reproduce

---

## Contributing

Want to help improve the GUI? Check out:
- `docs/DevDoc/WEEK_9-12_DESKTOP_INTEGRATION.md` - Development plan
- Source code in `gui/` directory
- Design guidelines in docs

---

**Enjoy chatting with AstrOS!** 🚀

*Version: 0.1.0 (Alpha)*  
*Last Updated: October 3, 2025*
