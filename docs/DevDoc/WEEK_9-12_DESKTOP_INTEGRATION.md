# Week 9-12: Desktop Integration & GUI Implementation

**Start Date**: October 3, 2025  
**Status**: In Progress 🚀  
**Goal**: Build a complete GTK4 desktop experience for AstrOS

---

## 📋 Overview

Transform AstrOS from a CLI-only tool into a full-featured desktop application with:
- GTK4 system tray integration
- Visual configuration GUI
- Desktop notifications
- Keyboard shortcuts
- Context menu integration
- Modern, polished interface

---

## 🎯 Objectives

### Phase 1: System Tray Icon (Days 57-63)
- [ ] Design system tray icon
- [ ] Implement GTK4 status icon
- [ ] Add quick menu (Show/Hide, Settings, Quit)
- [ ] Show service status in tray
- [ ] Add click-to-query popup
- [ ] Indicator for running queries

### Phase 2: Main GUI Window (Days 64-70)
- [ ] Design main window layout
- [ ] Create chat interface with history
- [ ] Implement message bubbles (user/AI)
- [ ] Add text input with send button
- [ ] Show typing indicators
- [ ] Markdown rendering for responses
- [ ] Copy response button
- [ ] Clear history option

### Phase 3: Configuration GUI (Days 71-77)
- [ ] Settings window design
- [ ] API key input (secure)
- [ ] Model selection dropdown
- [ ] Temperature slider
- [ ] Max tokens input
- [ ] Timeout configuration
- [ ] Save/Apply/Cancel buttons
- [ ] Test connection button

### Phase 4: Desktop Notifications (Days 78-84)
- [ ] libnotify integration
- [ ] Notification on query complete
- [ ] Show preview of response
- [ ] Click notification to open window
- [ ] Notification settings (enable/disable)
- [ ] Custom notification icons

### Phase 5: Keyboard Shortcuts (Days 85-91)
- [ ] Global hotkey for quick query
- [ ] Window show/hide shortcut
- [ ] Send message shortcut (Ctrl+Enter)
- [ ] Clear history shortcut
- [ ] Settings shortcut
- [ ] Shortcut customization UI

### Phase 6: Polish & Package (Days 92-98)
- [ ] Theme support (light/dark)
- [ ] Custom styling/CSS
- [ ] Application icon
- [ ] .desktop file
- [ ] autostart option
- [ ] Update Debian package
- [ ] Integration testing

---

## 🏗️ Architecture

### Technology Stack
```
GTK4 (Python bindings via PyGObject)
├── Main Application
│   ├── System Tray (StatusIcon/AppIndicator)
│   ├── Main Window (Gtk.ApplicationWindow)
│   │   ├── HeaderBar
│   │   ├── Chat View (Gtk.ScrolledWindow)
│   │   ├── Text Input (Gtk.Entry/TextView)
│   │   └── Send Button
│   ├── Settings Window (Gtk.Dialog)
│   └── About Dialog
├── Notifications (GNotification/libnotify)
├── Keyboard Shortcuts (Gtk.Application)
└── Backend Integration
    ├── D-Bus service communication
    └── Direct astros.py integration
```

### File Structure
```
gui/
├── __init__.py
├── app.py              # Main GTK application
├── tray.py             # System tray implementation
├── chat_window.py      # Main chat interface
├── settings_window.py  # Configuration GUI
├── notifications.py    # Desktop notifications
├── shortcuts.py        # Keyboard shortcut handler
├── theme.py            # Theme and styling
└── resources/
    ├── icons/
    │   ├── astros-icon.svg
    │   ├── astros-tray.svg
    │   └── astros-notification.svg
    ├── ui/
    │   ├── main_window.ui      # Glade UI files
    │   ├── settings_window.ui
    │   └── about_dialog.ui
    └── styles/
        └── astros.css           # Custom CSS
```

---

## 📅 Development Timeline

### Week 9 (Days 57-63): System Tray & Basic Window
**Goal**: Working system tray with popup window

**Day 57-58**: Setup & Design
- Install GTK4 dependencies
- Create project structure
- Design mockups
- Icon creation

**Day 59-60**: System Tray
- StatusIcon/AppIndicator implementation
- Menu items (Show, Settings, Quit)
- Service status indicator
- Click handlers

**Day 61-62**: Basic Window
- Main window skeleton
- Header bar with title
- Basic chat layout
- Show/hide functionality

**Day 63**: Integration & Testing
- Connect tray to window
- Test show/hide
- Fix bugs
- Documentation

---

### Week 10 (Days 64-70): Chat Interface
**Goal**: Fully functional chat window

**Day 64-65**: Chat View
- ScrolledWindow setup
- Message bubble design
- User vs AI styling
- Auto-scroll to bottom

**Day 66-67**: Input & Send
- Text entry widget
- Send button with icon
- Ctrl+Enter shortcut
- Input validation

**Day 68-69**: Response Handling
- Async query execution
- Loading spinner/indicator
- Markdown rendering
- Error display

**Day 70**: Features & Polish
- Copy response button
- Clear history
- Timestamp display
- Testing

---

### Week 11 (Days 71-77): Settings & Configuration
**Goal**: Complete settings management

**Day 71-72**: Settings Window
- Dialog design
- Tabbed interface
- General/Advanced tabs
- Form widgets

**Day 73-74**: API Configuration
- API key input (password field)
- Model selection combo
- Endpoint URL entry
- Test connection button

**Day 75-76**: Advanced Settings
- Temperature slider
- Max tokens spinner
- Timeout setting
- Auto-start checkbox

**Day 77**: Save & Apply
- Config file writing
- Apply without restart
- Validation
- Testing

---

### Week 12 (Days 78-84): Notifications & Shortcuts
**Goal**: Desktop integration complete

**Day 78-79**: Notifications
- libnotify setup
- Query complete notification
- Response preview
- Click to open window

**Day 80-81**: Keyboard Shortcuts
- Global hotkey registration
- Quick query dialog
- Window shortcuts
- Shortcut customization

**Day 82-83**: Theme & Polish
- Dark/light theme support
- Custom CSS styling
- Icon refinement
- Animation tweaks

**Day 84**: Final Integration
- Package update
- .desktop file
- Autostart option
- Complete testing

---

## 🎨 Design Specifications

### System Tray Icon
```
Size: 22x22px (scalable SVG)
States:
- Idle: Blue/gray icon
- Working: Animated spinner
- Error: Red icon
- Disabled: Gray icon

Menu:
├── Show AstrOS
├── Quick Query... (Ctrl+Alt+A)
├── ──────────
├── Settings
├── About
└── Quit
```

### Main Window
```
Title: AstrOS - AI Assistant
Size: 800x600px (resizable)
Min Size: 600x400px

Layout:
┌────────────────────────────────────┐
│ ☰ AstrOS          [-][□][×]       │ HeaderBar
├────────────────────────────────────┤
│                                    │
│  [User] Hello!                     │
│         ┌──────────────────┐       │
│         │ Hi! How can I    │       │
│         │ help you today?  │ [AI]  │
│         └──────────────────┘       │
│                                    │ Chat Area
│  [User] Tell me about Linux        │
│         ┌──────────────────┐       │
│         │ Linux is a free  │       │
│         │ open-source...   │ [AI]  │
│         └──────────────────┘       │
│                                    │
├────────────────────────────────────┤
│ Type your message...    [Send] 📤  │ Input Area
└────────────────────────────────────┘
```

### Settings Window
```
Title: AstrOS Settings
Size: 600x400px

Tabs: [General] [Advanced] [About]

General Tab:
┌────────────────────────────────────┐
│ API Configuration                  │
│                                    │
│ API Key: [******************] 🔑   │
│ Model:   [mistralai/ministral-8b▼] │
│ Endpoint:[https://openrouter.ai/..] │
│                                    │
│ [Test Connection]                  │
│                                    │
│ Interface                          │
│ ☑ Start on login                   │
│ ☑ Show notifications               │
│ ☐ Minimize to tray on close        │
│                                    │
│        [Cancel] [Apply] [OK]       │
└────────────────────────────────────┘
```

---

## 🔧 Technical Implementation

### 1. System Tray (tray.py)
```python
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class AstrosTray:
    def __init__(self, app):
        self.app = app
        self.indicator = self.create_indicator()
        
    def create_indicator(self):
        # AppIndicator or StatusIcon implementation
        pass
        
    def show_menu(self, icon, button, time):
        menu = Gtk.Menu()
        # Add menu items
        menu.popup(None, None, None, None, button, time)
```

### 2. Main Window (chat_window.py)
```python
class ChatWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.setup_ui()
        
    def setup_ui(self):
        self.set_default_size(800, 600)
        self.set_title("AstrOS - AI Assistant")
        
        # Header bar
        header = Gtk.HeaderBar()
        header.set_show_title_buttons(True)
        self.set_titlebar(header)
        
        # Main layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Chat view
        self.chat_view = self.create_chat_view()
        vbox.append(self.chat_view)
        
        # Input area
        input_box = self.create_input_area()
        vbox.append(input_box)
        
        self.set_child(vbox)
```

### 3. Settings Window (settings_window.py)
```python
class SettingsWindow(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Settings", parent=parent)
        self.set_default_size(600, 400)
        
        # Create notebook (tabs)
        notebook = Gtk.Notebook()
        notebook.append_page(self.create_general_tab(), 
                           Gtk.Label(label="General"))
        notebook.append_page(self.create_advanced_tab(),
                           Gtk.Label(label="Advanced"))
        
        self.get_content_area().append(notebook)
```

---

## 📦 Dependencies

### Required Packages
```bash
# System packages
sudo apt install -y \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-4.0 \
    gir1.2-notify-0.7 \
    gir1.2-appindicator3-0.1 \
    libnotify-bin

# Python packages (in virtualenv)
pip install PyGObject pycairo
```

### Update debian/control
```
Depends: python3 (>= 3.10), 
         python3-venv, 
         python3-pip, 
         systemd,
         python3-gi,
         python3-gi-cairo,
         gir1.2-gtk-4.0,
         gir1.2-notify-0.7,
         libnotify-bin
```

---

## ✅ Success Criteria

### Functional Requirements
- [ ] System tray icon always visible
- [ ] Click tray to show/hide window
- [ ] Chat interface works smoothly
- [ ] Messages display correctly (user/AI)
- [ ] Settings save and apply correctly
- [ ] Notifications appear on completion
- [ ] Keyboard shortcuts work globally
- [ ] Autostart option functional

### Performance Requirements
- [ ] Window opens in <500ms
- [ ] No UI lag during queries
- [ ] Smooth scrolling in chat
- [ ] Memory usage <50MB idle
- [ ] Response time <100ms for UI actions

### Quality Requirements
- [ ] Clean, modern design
- [ ] Consistent with GNOME HIG
- [ ] No crashes or freezes
- [ ] Proper error handling
- [ ] All features documented
- [ ] Accessible (keyboard navigation)

---

## 🧪 Testing Plan

### Unit Tests
- [ ] Settings load/save
- [ ] Message formatting
- [ ] API integration
- [ ] Notification triggers

### Integration Tests
- [ ] Tray → Window interaction
- [ ] Settings → Service restart
- [ ] Keyboard → Action dispatch
- [ ] Notification → Window focus

### UI Tests
- [ ] Window resize/maximize
- [ ] Theme switching
- [ ] Long message handling
- [ ] Markdown rendering
- [ ] Error display

### User Acceptance Tests
- [ ] Install and first run
- [ ] Configure API key
- [ ] Send first message
- [ ] Change settings
- [ ] Use keyboard shortcuts
- [ ] Receive notifications

---

## 📝 Documentation Tasks

- [ ] GUI User Guide
- [ ] Keyboard Shortcuts Reference
- [ ] Settings Documentation
- [ ] Theme Customization Guide
- [ ] Developer API Documentation
- [ ] Screenshot gallery
- [ ] Video demo

---

## 🎯 Milestones

### Milestone 1: Basic GUI (Week 9)
**Deliverable**: Working system tray + basic window
**Date**: October 9, 2025

### Milestone 2: Chat Interface (Week 10)
**Deliverable**: Full chat functionality
**Date**: October 16, 2025

### Milestone 3: Settings & Config (Week 11)
**Deliverable**: Complete settings management
**Date**: October 23, 2025

### Milestone 4: Desktop Integration (Week 12)
**Deliverable**: Notifications, shortcuts, packaging
**Date**: October 30, 2025

---

## 🚀 Next Steps

**Immediate Actions** (Today - October 3):
1. ✅ Create this planning document
2. [ ] Install GTK4 dependencies
3. [ ] Create GUI project structure
4. [ ] Design system tray icon (SVG)
5. [ ] Create basic app.py skeleton
6. [ ] Test PyGObject imports

**Tomorrow** (October 4):
1. [ ] Implement basic GTK application
2. [ ] Create system tray icon
3. [ ] Add simple menu
4. [ ] Test tray functionality
5. [ ] Create main window skeleton

---

## 💡 Notes & Ideas

### Future Enhancements
- Voice input/output integration
- Plugin system for custom commands
- Multiple chat sessions/tabs
- Export chat history
- Custom themes marketplace
- Wayland support optimization
- Mobile app companion

### Technical Considerations
- Use async/await for non-blocking UI
- Implement proper MVC pattern
- Cache responses for offline viewing
- Use D-Bus for IPC with daemon
- Consider Flatpak packaging
- Implement proper logging

---

**Status**: Ready to begin implementation! 🎉
**Next**: Install dependencies and create project structure
