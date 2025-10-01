# Stage 1: Desktop UI & Core Plugins (3-4 months) 🖥️

**Goal**: Native desktop experience with working plugin ecosystem

**Prerequisites**: Stage 0 completed with bootable ISO

**Current Status**: ⏳ Pending Stage 0 completion

---

## 📋 Overview

This stage focuses on building the user-facing components:
- Native desktop application for AI interaction
- Plugin system architecture
- Core plugins (System Control, File Manager, Terminal)

---

## Desktop Application (8 weeks)

### Week 1-2: Technology Decision & Setup

#### Task 1.1: Choose UI Framework
**Option A: Electron (Recommended for MVP)**
- ✅ Faster development
- ✅ Cross-platform ready
- ✅ Web technologies (React/TypeScript)
- ❌ Larger memory footprint (~150MB)

**Option B: GTK4 (Long-term goal)**
- ✅ Native Linux feel
- ✅ Lighter weight (~50MB)
- ✅ Better system integration
- ❌ Steeper learning curve

**Decision**: Start with Electron, plan GTK4 migration for v2.0

#### Task 1.2: Set Up Electron Project
```bash
# Create project directory
mkdir -p astros-desktop/electron-app
cd astros-desktop/electron-app

# Initialize project
npm init -y

# Install dependencies
npm install --save-dev \
    electron \
    electron-builder \
    @types/node

npm install --save \
    react \
    react-dom \
    @types/react \
    @types/react-dom \
    typescript \
    tailwindcss \
    dbus-next

# Initialize TypeScript
npx tsc --init
```

#### Task 1.3: Create Basic App Structure
**Directory Structure**:
```
astros-desktop/electron-app/
├── src/
│   ├── main/           # Electron main process
│   ├── renderer/       # React UI
│   ├── preload/        # Preload scripts
│   └── shared/         # Shared types
├── assets/             # Icons, images
├── package.json
└── electron-builder.yml
```

### Week 3-4: Main Chat Interface

#### Task 2.1: Create Main Window
**File**: `src/main/main.ts`
```typescript
import { app, BrowserWindow, ipcMain, globalShortcut } from 'electron';
import path from 'path';

class AstrOSApp {
  private mainWindow: BrowserWindow | null = null;
  
  constructor() {
    app.whenReady().then(() => this.init());
    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') app.quit();
    });
  }
  
  private init() {
    this.createWindow();
    this.registerGlobalShortcut();
    this.setupIPC();
  }
  
  private createWindow() {
    this.mainWindow = new BrowserWindow({
      width: 800,
      height: 600,
      webPreferences: {
        preload: path.join(__dirname, '../preload/preload.js'),
        contextIsolation: true,
        nodeIntegration: false,
      },
      title: 'AstrOS',
      icon: path.join(__dirname, '../../assets/icon.png'),
    });
    
    this.mainWindow.loadFile('index.html');
  }
  
  private registerGlobalShortcut() {
    // Super+Space to show/hide
    globalShortcut.register('Super+Space', () => {
      if (this.mainWindow) {
        if (this.mainWindow.isVisible()) {
          this.mainWindow.hide();
        } else {
          this.mainWindow.show();
          this.mainWindow.focus();
        }
      }
    });
  }
  
  private setupIPC() {
    ipcMain.handle('ask-ai', async (event, question: string) => {
      // Call astros agent via D-Bus
      return await this.callAstrOSAgent(question);
    });
  }
  
  private async callAstrOSAgent(question: string): Promise<string> {
    // Implementation to call astros-agent service via D-Bus
    return "Response from AI";
  }
}

new AstrOSApp();
```

#### Task 2.2: Create React UI
**File**: `src/renderer/App.tsx`
```typescript
import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';

const App: React.FC = () => {
  const [conversations, setConversations] = useState([]);
  
  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar conversations={conversations} />
      <ChatInterface />
    </div>
  );
};

export default App;
```

**File**: `src/renderer/components/ChatInterface.tsx`
```typescript
import React, { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const handleSend = async () => {
    if (!input.trim()) return;
    
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      // Call AI via IPC
      const response = await window.electronAPI.askAI(input);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Failed to get AI response:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="flex-1 flex flex-col">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <h1 className="text-xl font-bold">AstrOS Assistant</h1>
        <p className="text-sm text-gray-400">mistralai/ministral-8b</p>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] p-3 rounded-lg ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-100'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
              <span className="text-xs opacity-50 mt-1 block">
                {message.timestamp.toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 p-3 rounded-lg">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input */}
      <div className="bg-gray-800 p-4 border-t border-gray-700">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask me anything..."
            className="flex-1 bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-6 py-2 rounded-lg font-medium transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
```

### Week 5-6: Settings & Plugin Management

#### Task 3.1: Settings Panel
**File**: `src/renderer/components/Settings.tsx`
```typescript
import React, { useState, useEffect } from 'react';

const Settings: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('mistralai/ministral-8b');
  const [theme, setTheme] = useState('dark');
  
  const handleSave = async () => {
    await window.electronAPI.saveSettings({
      apiKey,
      model,
      theme,
    });
  };
  
  return (
    <div className="p-6 max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>
      
      {/* API Configuration */}
      <section className="mb-8">
        <h3 className="text-lg font-semibold mb-4">API Configuration</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              OpenRouter API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-or-v1-..."
              className="w-full bg-gray-700 px-4 py-2 rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">
              AI Model
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full bg-gray-700 px-4 py-2 rounded"
            >
              <option value="mistralai/ministral-8b">MistralAI Ministral 8B</option>
              <option value="openai/gpt-4">OpenAI GPT-4</option>
              <option value="anthropic/claude-3">Claude 3</option>
            </select>
          </div>
        </div>
      </section>
      
      {/* Appearance */}
      <section className="mb-8">
        <h3 className="text-lg font-semibold mb-4">Appearance</h3>
        <div>
          <label className="block text-sm font-medium mb-2">Theme</label>
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            className="w-full bg-gray-700 px-4 py-2 rounded"
          >
            <option value="dark">Dark</option>
            <option value="light">Light</option>
            <option value="auto">Auto</option>
          </select>
        </div>
      </section>
      
      <button
        onClick={handleSave}
        className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-medium"
      >
        Save Settings
      </button>
    </div>
  );
};

export default Settings;
```

### Week 7-8: Build & Package

#### Task 4.1: Create Build Configuration
**File**: `electron-builder.yml`
```yaml
appId: org.astros.desktop
productName: AstrOS
copyright: Copyright © 2025 AstrOS Project

directories:
  output: dist
  buildResources: assets

files:
  - src/**/*
  - package.json

linux:
  target:
    - deb
    - AppImage
  category: Utility
  icon: assets/icon.png
  desktop:
    Name: AstrOS
    Comment: AI-powered desktop assistant
    Exec: astros %U
    Terminal: false
    Type: Application
    Categories: Utility;

deb:
  depends:
    - libnotify4
    - libappindicator3-1
```

#### Task 4.2: Build Package
```bash
# Build for Linux
npm run build
npm run pack

# Test .deb package
sudo dpkg -i dist/astros_0.1.0_amd64.deb
```

---

## Plugin System Architecture (4 weeks)

### Week 1: D-Bus Interface Design

#### Task 1.1: Create D-Bus Service Definition
**File**: `astros-core/dbus/org.astros.PluginManager.xml`
```xml
<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
 "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
  <interface name="org.astros.PluginManager">
    <method name="ListPlugins">
      <arg direction="out" type="a{ss}" name="plugins"/>
    </method>
    <method name="EnablePlugin">
      <arg direction="in" type="s" name="plugin_id"/>
      <arg direction="out" type="b" name="success"/>
    </method>
    <method name="DisablePlugin">
      <arg direction="in" type="s" name="plugin_id"/>
      <arg direction="out" type="b" name="success"/>
    </method>
    <method name="ExecutePlugin">
      <arg direction="in" type="s" name="plugin_id"/>
      <arg direction="in" type="s" name="command"/>
      <arg direction="in" type="a{sv}" name="params"/>
      <arg direction="out" type="s" name="result"/>
    </method>
  </interface>
</node>
```

### Week 2-3: Plugin System Implementation

#### Task 2.1: Plugin Base Class
**File**: `astros-core/plugins/base_plugin.py`
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json

class AstrOSPlugin(ABC):
    """Base class for all AstrOS plugins"""
    
    def __init__(self, plugin_id: str, manifest: Dict[str, Any]):
        self.plugin_id = plugin_id
        self.manifest = manifest
        self.enabled = False
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize plugin resources"""
        pass
    
    @abstractmethod
    async def execute(self, command: str, params: Dict[str, Any]) -> str:
        """Execute plugin command"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Clean up plugin resources"""
        pass
    
    def get_commands(self) -> List[str]:
        """Get list of supported commands"""
        return self.manifest.get('commands', [])
    
    def get_permissions(self) -> List[str]:
        """Get required permissions"""
        return self.manifest.get('permissions', [])
```

#### Task 2.2: Plugin Manager
**File**: `astros-core/plugins/plugin_manager.py`
```python
import os
import json
import importlib.util
from pathlib import Path
from typing import Dict, List
import asyncio

class PluginManager:
    """Manage AstrOS plugins"""
    
    def __init__(self, plugin_dir: str = "/usr/lib/astros/plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, AstrOSPlugin] = {}
        self.enabled_plugins: set = set()
    
    async def discover_plugins(self):
        """Discover all available plugins"""
        for plugin_path in self.plugin_dir.iterdir():
            if plugin_path.is_dir():
                manifest_file = plugin_path / "manifest.json"
                if manifest_file.exists():
                    await self.load_plugin(plugin_path)
    
    async def load_plugin(self, plugin_path: Path):
        """Load a single plugin"""
        try:
            # Read manifest
            with open(plugin_path / "manifest.json") as f:
                manifest = json.load(f)
            
            plugin_id = manifest['id']
            
            # Load plugin module
            spec = importlib.util.spec_from_file_location(
                plugin_id,
                plugin_path / "plugin.py"
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Instantiate plugin
            plugin_class = getattr(module, manifest['class'])
            plugin = plugin_class(plugin_id, manifest)
            
            self.plugins[plugin_id] = plugin
            print(f"✅ Loaded plugin: {plugin_id}")
            
        except Exception as e:
            print(f"❌ Failed to load plugin {plugin_path}: {e}")
    
    async def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin"""
        if plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            if await plugin.initialize():
                self.enabled_plugins.add(plugin_id)
                plugin.enabled = True
                return True
        return False
    
    async def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin"""
        if plugin_id in self.enabled_plugins:
            plugin = self.plugins[plugin_id]
            await plugin.cleanup()
            self.enabled_plugins.remove(plugin_id)
            plugin.enabled = False
            return True
        return False
    
    async def execute_plugin(self, plugin_id: str, command: str, params: Dict) -> str:
        """Execute a plugin command"""
        if plugin_id in self.enabled_plugins:
            plugin = self.plugins[plugin_id]
            return await plugin.execute(command, params)
        return "Plugin not enabled"
    
    def list_plugins(self) -> Dict[str, Dict]:
        """List all plugins with their status"""
        return {
            pid: {
                'name': p.manifest['name'],
                'version': p.manifest['version'],
                'enabled': p.enabled,
                'commands': p.get_commands()
            }
            for pid, p in self.plugins.items()
        }
```

### Week 4: Plugin Sandboxing

#### Task 3.1: Bubblewrap Integration
**File**: `astros-core/plugins/sandbox.py`
```python
import subprocess
from typing import List

class PluginSandbox:
    """Sandbox plugins using bubblewrap"""
    
    @staticmethod
    def run_sandboxed(command: List[str], permissions: List[str]) -> str:
        """Run command in sandbox with specified permissions"""
        
        bwrap_args = [
            'bwrap',
            '--ro-bind', '/usr', '/usr',
            '--ro-bind', '/lib', '/lib',
            '--ro-bind', '/lib64', '/lib64',
            '--ro-bind', '/bin', '/bin',
            '--ro-bind', '/sbin', '/sbin',
            '--proc', '/proc',
            '--dev', '/dev',
            '--tmpfs', '/tmp',
        ]
        
        # Add permissions
        if 'filesystem.read' in permissions:
            bwrap_args.extend(['--ro-bind', '/home', '/home'])
        if 'filesystem.write' in permissions:
            bwrap_args.extend(['--bind', '/home', '/home'])
        if 'network' in permissions:
            bwrap_args.append('--share-net')
        
        # Add command
        bwrap_args.extend(command)
        
        # Execute
        result = subprocess.run(
            bwrap_args,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result.stdout
```

---

## Core Plugins (6 weeks)

### Plugin 1: System Control (Week 1-2)

**File**: `astros-plugins/system-control/manifest.json`
```json
{
  "id": "system-control",
  "name": "System Control",
  "version": "1.0.0",
  "class": "SystemControlPlugin",
  "permissions": ["system.exec", "audio", "display"],
  "commands": [
    "volume",
    "brightness",
    "launch",
    "screenshot",
    "power"
  ]
}
```

**File**: `astros-plugins/system-control/plugin.py`
```python
from astros.plugins.base_plugin import AstrOSPlugin
import subprocess

class SystemControlPlugin(AstrOSPlugin):
    async def initialize(self) -> bool:
        return True
    
    async def execute(self, command: str, params: dict) -> str:
        if command == "volume":
            return await self.control_volume(params)
        elif command == "brightness":
            return await self.control_brightness(params)
        elif command == "launch":
            return await self.launch_app(params)
        elif command == "screenshot":
            return await self.take_screenshot(params)
        return "Unknown command"
    
    async def control_volume(self, params: dict) -> str:
        action = params.get('action', 'get')
        if action == 'set':
            level = params.get('level', 50)
            subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{level}%'])
            return f"Volume set to {level}%"
        # Get current volume
        result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], capture_output=True, text=True)
        return result.stdout
    
    async def control_brightness(self, params: dict) -> str:
        action = params.get('action', 'get')
        if action == 'set':
            level = params.get('level', 50)
            subprocess.run(['brightnessctl', 'set', f'{level}%'])
            return f"Brightness set to {level}%"
        result = subprocess.run(['brightnessctl', 'get'], capture_output=True, text=True)
        return f"Current brightness: {result.stdout}"
    
    async def launch_app(self, params: dict) -> str:
        app = params.get('app')
        subprocess.Popen([app])
        return f"Launched {app}"
    
    async def take_screenshot(self, params: dict) -> str:
        filename = params.get('filename', '/tmp/screenshot.png')
        subprocess.run(['gnome-screenshot', '-f', filename])
        return f"Screenshot saved to {filename}"
    
    async def cleanup(self):
        pass
```

### Plugin 2: File Manager (Week 3-4)

**File**: `astros-plugins/file-manager/plugin.py`
```python
from astros.plugins.base_plugin import AstrOSPlugin
import os
from pathlib import Path
import shutil

class FileManagerPlugin(AstrOSPlugin):
    async def initialize(self) -> bool:
        return True
    
    async def execute(self, command: str, params: dict) -> str:
        if command == "find":
            return await self.find_files(params)
        elif command == "organize":
            return await self.organize_files(params)
        elif command == "search":
            return await self.search_content(params)
        return "Unknown command"
    
    async def find_files(self, params: dict) -> str:
        pattern = params.get('pattern', '*')
        directory = params.get('directory', str(Path.home()))
        
        matches = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if pattern in file:
                    matches.append(os.path.join(root, file))
        
        return f"Found {len(matches)} files:\n" + "\n".join(matches[:20])
    
    async def organize_files(self, params: dict) -> str:
        directory = params.get('directory', str(Path.home() / "Downloads"))
        
        # Organize by extension
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.is file(filepath):
                ext = Path(filename).suffix[1:]  # Remove dot
                if ext:
                    dest_dir = os.path.join(directory, ext.upper())
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.move(filepath, os.path.join(dest_dir, filename))
        
        return f"Organized files in {directory}"
    
    async def cleanup(self):
        pass
```

### Plugin 3: Terminal (Week 5-6)

**File**: `astros-plugins/terminal/plugin.py`
```python
from astros.plugins.base_plugin import AstrOSPlugin
import subprocess

class TerminalPlugin(AstrOSPlugin):
    async def initialize(self) -> bool:
        return True
    
    async def execute(self, command: str, params: dict) -> str:
        if command == "run":
            return await self.run_command(params)
        elif command == "suggest":
            return await self.suggest_command(params)
        return "Unknown command"
    
    async def run_command(self, params: dict) -> str:
        cmd = params.get('command')
        
        # Safety check
        dangerous_commands = ['rm -rf', 'dd', 'mkfs', ':(){:|:&};:']
        if any(danger in cmd for danger in dangerous_commands):
            return "❌ Dangerous command detected. Please run manually."
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout or result.stderr
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error: {e}"
    
    async def suggest_command(self, params: dict) -> str:
        intent = params.get('intent')
        
        suggestions = {
            'compress': 'tar -czf archive.tar.gz directory/',
            'extract': 'tar -xzf archive.tar.gz',
            'find large files': 'find ~ -type f -size +100M',
            'disk usage': 'df -h',
            'process list': 'ps aux | grep',
        }
        
        for key, cmd in suggestions.items():
            if key in intent.lower():
                return f"Suggested command: {cmd}"
        
        return "No suggestion available"
    
    async def cleanup(self):
        pass
```

---

## 🎯 Stage 1 Success Criteria

### Must Have ✅
- [ ] Native desktop app working (Electron)
- [ ] Chat interface with conversation history
- [ ] Settings panel functional
- [ ] Plugin system implemented
- [ ] 3 core plugins working:
  - [ ] System Control
  - [ ] File Manager
  - [ ] Terminal
- [ ] Response time < 500ms for local operations
- [ ] Packaged as .deb for easy installation

### Nice to Have ⭐
- [ ] Plugin marketplace UI
- [ ] Voice input button
- [ ] Conversation export
- [ ] Custom themes

---

## 📊 Progress Tracking

| Component | Status | Progress |
|-----------|--------|----------|
| Desktop App | ⏳ | 0% |
| Plugin System | ⏳ | 0% |
| System Control Plugin | ⏳ | 0% |
| File Manager Plugin | ⏳ | 0% |
| Terminal Plugin | ⏳ | 0% |

---

## 🔗 Related Documentation

- [Electron Development Guide](ELECTRON_GUIDE.md)
- [Plugin Development Guide](PLUGIN_DEVELOPMENT.md)
- [D-Bus Integration Guide](DBUS_GUIDE.md)

---

**Previous Stage**: [Stage 0: Build Foundation](STAGE_0_FOUNDATION.md)  
**Next Stage**: [Stage 2: System Integration & Automation](STAGE_2_INTEGRATION.md)
