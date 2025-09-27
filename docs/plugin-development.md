# AstrOS Plugin Development Guide 🧩

Learn how to extend AstrOS with powerful AI-powered plugins! This comprehensive guide covers everything from basic plugin creation to advanced AI integration.

## 📋 Table of Contents

- [What Are AstrOS Plugins?](#-what-are-astros-plugins)
- [Quick Start](#-quick-start)
- [Plugin Architecture](#-plugin-architecture)
- [Core Concepts](#-core-concepts)
- [Development Tutorial](#-development-tutorial)
- [AI Integration](#-ai-integration)
- [Best Practices](#-best-practices)
- [Testing & Debugging](#-testing--debugging)
- [Distribution](#-distribution)
- [Advanced Topics](#-advanced-topics)

---

## 🎯 What Are AstrOS Plugins?

AstrOS plugins are Python modules that extend the operating system's capabilities through natural language interactions. They allow users to perform complex tasks by simply talking to their computer.

### Plugin Categories

<table>
<tr>
<td width="50%">

#### 🗂️ **System Plugins**
- **File Management**: Organize, search, and manipulate files
- **System Control**: Manage services, processes, and settings
- **Hardware Integration**: Control peripherals and sensors
- **Network Management**: WiFi, VPN, and connectivity tools

</td>
<td width="50%">

#### 🚀 **Productivity Plugins**
- **Development Tools**: Code generation, project management
- **Communication**: Email, messaging, social media
- **Content Creation**: Documents, presentations, media
- **Automation**: Workflow orchestration and scheduling

</td>
</tr>
</table>

### How Plugins Work

```mermaid
graph LR
    A[User Voice/Text] --> B[AstrOS Agent]
    B --> C[Intent Recognition]
    C --> D[Plugin Matching]
    D --> E[Plugin Execution]
    E --> F[AI Processing]
    F --> G[System Actions]
    G --> H[Response to User]
```

---

## 🚀 Quick Start

### Create Your First Plugin

```bash
# Generate plugin scaffold
python scripts/create-plugin.py --name hello-world --author "Your Name"

# Navigate to plugin directory
cd plugins/hello-world

# Install in development mode
pip install -e .

# Test the plugin
python -m astros.plugins.test hello-world
```

### Minimal Plugin Example

```python
# plugins/hello-world/src/main.py
from astros.plugin import BasePlugin, plugin_handler
from astros.types import Intent, Response

class HelloWorldPlugin(BasePlugin):
    """A simple greeting plugin to demonstrate basic functionality."""
    
    # Plugin metadata
    name = "hello-world"
    version = "1.0.0"
    description = "Responds to greetings with friendly messages"
    author = "Your Name <your.email@example.com>"
    
    # Define what this plugin can handle
    handles = ["greetings", "introductions"]
    requires_ai = False  # This plugin doesn't need AI processing
    
    @plugin_handler("say_hello")
    async def say_hello(self, intent: Intent) -> Response:
        """Handle greeting requests."""
        user_name = intent.context.get("user_name", "friend")
        
        return Response(
            success=True,
            message=f"Hello, {user_name}! Welcome to AstrOS!",
            data={"greeting": "hello", "timestamp": intent.timestamp}
        )
    
    @plugin_handler("introduce_astros")
    async def introduce_astros(self, intent: Intent) -> Response:
        """Introduce AstrOS capabilities."""
        return Response(
            success=True,
            message="I'm AstrOS, your AI-powered assistant! I can help you manage files, automate tasks, and much more through natural conversation.",
            data={"introduction": True}
        )
```

---

## 🏗️ Plugin Architecture

### Plugin Structure

```
plugins/your-plugin/
├── plugin.yaml                 # Plugin metadata and configuration
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main plugin class
│   ├── handlers/               # Intent handlers
│   │   ├── __init__.py
│   │   ├── file_operations.py
│   │   └── ai_interactions.py
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── models/                 # Data models
│       ├── __init__.py
│       └── schemas.py
├── tests/
│   ├── __init__.py
│   ├── test_plugin.py
│   ├── test_handlers.py
│   └── fixtures/
├── docs/
│   ├── README.md
│   ├── usage.md
│   └── api.md
├── requirements.txt            # Plugin dependencies
└── setup.py                   # Installation script
```

### Plugin Configuration

```yaml
# plugin.yaml
metadata:
  name: "awesome-plugin"
  version: "1.0.0"
  description: "An awesome plugin that does amazing things"
  author: "Your Name <your.email@example.com>"
  license: "Apache-2.0"
  homepage: "https://github.com/your-username/astros-awesome-plugin"
  
capabilities:
  handles:
    - "file_management"
    - "automation"
    - "ai_assistance"
  
  requires_ai: true
  requires_permissions:
    - "file_system"
    - "network"
    - "system_control"
  
  supports_voice: true
  supports_gui: true

configuration:
  settings:
    max_file_size: 100MB
    cache_duration: 3600
    ai_model_preference: "gpt-4"
  
  user_configurable:
    - "max_file_size"
    - "cache_duration"

dependencies:
  python: ">=3.12"
  astros: ">=1.0.0"
  external:
    - "requests>=2.28.0"
    - "aiofiles>=23.0.0"
```

---

## 💡 Core Concepts

### Intents and Responses

**Intents** represent user requests parsed from natural language:

```python
from astros.types import Intent

# Example intent
intent = Intent(
    text="organize my photos by date",
    intent_type="file_organization",
    confidence=0.95,
    user_id="user123",
    context={
        "file_types": ["jpg", "png", "gif"],
        "location": "/home/user/Pictures",
        "organization_method": "date"
    },
    timestamp=datetime.now()
)
```

**Responses** contain the plugin's output:

```python
from astros.types import Response

# Example response
response = Response(
    success=True,
    message="Successfully organized 150 photos by date into folders",
    data={
        "files_processed": 150,
        "folders_created": ["2023-01", "2023-02", "2023-03"],
        "processing_time": 2.5
    },
    requires_followup=False,
    suggested_actions=["backup_photos", "create_slideshow"]
)
```

### Plugin Handlers

Plugin handlers are methods that process specific types of intents:

```python
from astros.plugin import plugin_handler
from astros.types import Intent, Response

class MyPlugin(BasePlugin):
    @plugin_handler("organize_files")
    async def organize_files(self, intent: Intent) -> Response:
        """Handle file organization requests."""
        # Your logic here
        return Response(success=True, message="Files organized!")
    
    @plugin_handler("search_files", priority=10)
    async def search_files(self, intent: Intent) -> Response:
        """Handle file search requests with high priority."""
        # Higher priority handlers are tried first
        return Response(success=True, message="Files found!")
```

### Context and State Management

```python
class StatefulPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.state = {}  # Plugin-specific state
    
    async def initialize(self):
        """Called when plugin is loaded."""
        self.state["initialized_at"] = datetime.now()
        await self.load_user_preferences()
    
    async def shutdown(self):
        """Called when plugin is unloaded."""
        await self.save_user_preferences()
    
    @plugin_handler("remember_preference")
    async def remember_preference(self, intent: Intent) -> Response:
        """Store user preferences."""
        key = intent.context.get("preference_key")
        value = intent.context.get("preference_value")
        
        # Use AstrOS storage API
        await self.storage.set(f"user_pref_{key}", value)
        
        return Response(
            success=True,
            message=f"Remembered your preference for {key}"
        )
```

---

## 🎓 Development Tutorial

Let's build a comprehensive file organizer plugin step by step.

### Step 1: Project Setup

```bash
# Create plugin
python scripts/create-plugin.py --name smart-organizer --author "Your Name"
cd plugins/smart-organizer
```

### Step 2: Define Plugin Metadata

Update `plugin.yaml`:

```yaml
metadata:
  name: "smart-organizer"
  version: "1.0.0"
  description: "AI-powered file organization and management"
  author: "Your Name <your.email@example.com>"

capabilities:
  handles:
    - "file_organization"
    - "file_management"
    - "smart_sorting"
  
  requires_ai: true
  requires_permissions:
    - "file_system"

configuration:
  settings:
    organization_methods:
      - "by_date"
      - "by_type" 
      - "by_size"
      - "by_content"
    default_method: "by_type"
```

### Step 3: Create the Main Plugin Class

```python
# src/main.py
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from astros.plugin import BasePlugin, plugin_handler
from astros.types import Intent, Response
from astros.ai import AIProvider

class SmartOrganizerPlugin(BasePlugin):
    """AI-powered file organization plugin."""
    
    name = "smart-organizer"
    version = "1.0.0"
    description = "Organize files intelligently using AI"
    author = "Your Name <your.email@example.com>"
    
    handles = ["file_organization", "file_management"]
    requires_ai = True
    requires_permissions = ["file_system"]
    
    def __init__(self):
        super().__init__()
        self.supported_formats = {
            "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
            "documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"],
            "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
            "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"]
        }
    
    async def initialize(self):
        """Initialize the plugin."""
        self.logger.info("Smart Organizer plugin initialized")
        
        # Initialize AI provider for content analysis
        self.ai = AIProvider(
            provider="openai",
            model="gpt-4-vision-preview"  # For image analysis
        )
    
    @plugin_handler("organize_files")
    async def organize_files(self, intent: Intent) -> Response:
        """Main file organization handler."""
        try:
            # Extract parameters from intent
            source_path = intent.context.get("path", os.path.expanduser("~/Downloads"))
            method = intent.context.get("method", "by_type")
            dry_run = intent.context.get("dry_run", False)
            
            # Validate source path
            if not os.path.exists(source_path):
                return Response(
                    success=False,
                    message=f"Path does not exist: {source_path}"
                )
            
            # Organize files based on method
            if method == "by_type":
                result = await self._organize_by_type(source_path, dry_run)
            elif method == "by_date":
                result = await self._organize_by_date(source_path, dry_run)
            elif method == "by_content":
                result = await self._organize_by_content(source_path, dry_run)
            else:
                return Response(
                    success=False,
                    message=f"Unknown organization method: {method}"
                )
            
            return Response(
                success=True,
                message=result["message"],
                data=result["details"]
            )
            
        except Exception as e:
            self.logger.error(f"Error organizing files: {e}")
            return Response(
                success=False,
                message=f"Failed to organize files: {str(e)}"
            )
    
    async def _organize_by_type(self, source_path: str, dry_run: bool) -> Dict:
        """Organize files by their type/extension."""
        files_moved = 0
        folders_created = []
        
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                # Determine category
                category = self._get_file_category(file_ext)
                category_folder = os.path.join(source_path, category.title())
                
                # Create category folder if needed
                if not dry_run and not os.path.exists(category_folder):
                    os.makedirs(category_folder)
                    folders_created.append(category.title())
                
                # Move file
                if not dry_run:
                    destination = os.path.join(category_folder, file)
                    shutil.move(file_path, destination)
                
                files_moved += 1
        
        return {
            "message": f"{'Would organize' if dry_run else 'Organized'} {files_moved} files into {len(set(folders_created))} categories",
            "details": {
                "files_processed": files_moved,
                "folders_created": list(set(folders_created)),
                "dry_run": dry_run
            }
        }
    
    async def _organize_by_date(self, source_path: str, dry_run: bool) -> Dict:
        """Organize files by creation/modification date."""
        files_moved = 0
        folders_created = []
        
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Get file date
                stat = os.stat(file_path)
                file_date = datetime.fromtimestamp(stat.st_mtime)
                date_folder = file_date.strftime("%Y-%m")
                date_path = os.path.join(source_path, date_folder)
                
                # Create date folder if needed
                if not dry_run and not os.path.exists(date_path):
                    os.makedirs(date_path)
                    folders_created.append(date_folder)
                
                # Move file
                if not dry_run:
                    destination = os.path.join(date_path, file)
                    shutil.move(file_path, destination)
                
                files_moved += 1
        
        return {
            "message": f"{'Would organize' if dry_run else 'Organized'} {files_moved} files by date",
            "details": {
                "files_processed": files_moved,
                "folders_created": folders_created,
                "dry_run": dry_run
            }
        }
    
    async def _organize_by_content(self, source_path: str, dry_run: bool) -> Dict:
        """Organize files by content using AI analysis."""
        files_analyzed = 0
        categories = {}
        
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip large files for AI analysis
                if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10MB
                    continue
                
                # Analyze file content with AI
                category = await self._analyze_file_content(file_path)
                
                if category not in categories:
                    categories[category] = []
                categories[category].append(file)
                
                # Create category folder and move file
                if not dry_run:
                    category_path = os.path.join(source_path, category)
                    if not os.path.exists(category_path):
                        os.makedirs(category_path)
                    
                    destination = os.path.join(category_path, file)
                    shutil.move(file_path, destination)
                
                files_analyzed += 1
        
        return {
            "message": f"{'Would analyze and organize' if dry_run else 'Analyzed and organized'} {files_analyzed} files by content",
            "details": {
                "files_processed": files_analyzed,
                "categories_found": list(categories.keys()),
                "dry_run": dry_run
            }
        }
    
    async def _analyze_file_content(self, file_path: str) -> str:
        """Use AI to analyze file content and suggest category."""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext in [".jpg", ".jpeg", ".png", ".gif"]:
                # Analyze image content
                prompt = "Analyze this image and categorize it into one of: photos, screenshots, memes, documents, artwork, other"
                response = await self.ai.analyze_image(file_path, prompt)
                return response.get("category", "other")
            
            elif file_ext in [".txt", ".md", ".py", ".js", ".html"]:
                # Analyze text content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:1000]  # First 1000 chars
                
                prompt = f"Categorize this text content into one of: code, documentation, notes, articles, other. Content: {content}"
                response = await self.ai.complete(prompt)
                return response.get("category", "other")
            
            else:
                return self._get_file_category(file_ext)
                
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {e}")
            return "other"
    
    def _get_file_category(self, extension: str) -> str:
        """Get file category based on extension."""
        for category, extensions in self.supported_formats.items():
            if extension in extensions:
                return category
        return "other"
    
    @plugin_handler("clean_duplicates")
    async def clean_duplicates(self, intent: Intent) -> Response:
        """Find and remove duplicate files."""
        # Implementation for duplicate cleaning
        pass
    
    @plugin_handler("smart_rename")
    async def smart_rename(self, intent: Intent) -> Response:
        """Rename files intelligently based on content."""
        # Implementation for smart renaming
        pass
```

### Step 4: Add Tests

```python
# tests/test_plugin.py
import pytest
import tempfile
import os
from pathlib import Path

from src.main import SmartOrganizerPlugin
from astros.types import Intent

class TestSmartOrganizerPlugin:
    
    @pytest.fixture
    def plugin(self):
        return SmartOrganizerPlugin()
    
    @pytest.fixture
    def temp_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_files = [
                "document.pdf",
                "photo.jpg",
                "video.mp4",
                "music.mp3",
                "archive.zip"
            ]
            
            for file_name in test_files:
                file_path = os.path.join(temp_dir, file_name)
                Path(file_path).touch()
            
            yield temp_dir
    
    @pytest.mark.asyncio
    async def test_organize_by_type(self, plugin, temp_directory):
        """Test organizing files by type."""
        intent = Intent(
            text="organize files by type",
            context={
                "path": temp_directory,
                "method": "by_type",
                "dry_run": True
            }
        )
        
        response = await plugin.organize_files(intent)
        
        assert response.success is True
        assert response.data["files_processed"] == 5
        assert "Documents" in response.data["folders_created"]
    
    @pytest.mark.asyncio
    async def test_organize_by_date(self, plugin, temp_directory):
        """Test organizing files by date."""
        intent = Intent(
            text="organize files by date",
            context={
                "path": temp_directory,
                "method": "by_date",
                "dry_run": True
            }
        )
        
        response = await plugin.organize_files(intent)
        
        assert response.success is True
        assert response.data["files_processed"] == 5
    
    def test_get_file_category(self, plugin):
        """Test file category detection."""
        assert plugin._get_file_category(".jpg") == "images"
        assert plugin._get_file_category(".pdf") == "documents"
        assert plugin._get_file_category(".mp4") == "videos"
        assert plugin._get_file_category(".unknown") == "other"
```

---

## 🤖 AI Integration

### Using AI Providers

AstrOS provides a unified interface for different AI providers:

```python
from astros.ai import AIProvider, AIError

class AIEnabledPlugin(BasePlugin):
    async def initialize(self):
        # Initialize AI provider
        self.ai = AIProvider(
            provider="openai",  # or "anthropic", "local"
            model="gpt-4"
        )
    
    @plugin_handler("analyze_content")
    async def analyze_content(self, intent: Intent) -> Response:
        """Analyze content using AI."""
        try:
            content = intent.context.get("content")
            
            # Text completion
            prompt = f"Analyze this content and provide insights: {content}"
            response = await self.ai.complete(prompt, max_tokens=500)
            
            return Response(
                success=True,
                message="Content analyzed successfully",
                data={"insights": response["content"]}
            )
            
        except AIError as e:
            return Response(
                success=False,
                message=f"AI analysis failed: {str(e)}"
            )
```

### Advanced AI Features

```python
class AdvancedAIPlugin(BasePlugin):
    
    @plugin_handler("image_analysis")
    async def analyze_image(self, intent: Intent) -> Response:
        """Analyze images using vision models."""
        image_path = intent.context.get("image_path")
        
        # Vision analysis
        result = await self.ai.analyze_image(
            image_path,
            prompt="Describe this image in detail and identify any text"
        )
        
        return Response(
            success=True,
            message="Image analyzed",
            data=result
        )
    
    @plugin_handler("conversation")
    async def maintain_conversation(self, intent: Intent) -> Response:
        """Maintain conversational context."""
        user_id = intent.user_id
        message = intent.text
        
        # Get conversation history
        history = await self.storage.get(f"conversation_{user_id}", [])
        
        # Add user message
        history.append({"role": "user", "content": message})
        
        # Generate response with context
        response = await self.ai.chat(
            messages=history,
            max_tokens=300
        )
        
        # Add assistant response to history
        history.append({"role": "assistant", "content": response["content"]})
        
        # Store updated history
        await self.storage.set(f"conversation_{user_id}", history[-10:])  # Keep last 10 messages
        
        return Response(
            success=True,
            message=response["content"],
            data={"conversation_id": user_id}
        )
```

### Local AI Models

```python
class LocalAIPlugin(BasePlugin):
    async def initialize(self):
        # Use local models for privacy
        self.ai = AIProvider(
            provider="local",
            model="llama2-7b",
            config={
                "model_path": "/opt/astros/models/llama2-7b.gguf",
                "context_length": 4096,
                "temperature": 0.7
            }
        )
    
    @plugin_handler("private_analysis")
    async def private_analysis(self, intent: Intent) -> Response:
        """Analyze data privately using local models."""
        # All processing happens locally
        result = await self.ai.complete(
            prompt=intent.text,
            max_tokens=200
        )
        
        return Response(
            success=True,
            message=result["content"]
        )
```

---

## ✅ Best Practices

### Code Quality

1. **Type Hints**: Always use type hints for better code clarity
```python
from typing import List, Dict, Optional, Union

@plugin_handler("process_files")
async def process_files(
    self, 
    intent: Intent
) -> Response:
    files: List[str] = intent.context.get("files", [])
    options: Dict[str, Union[str, int]] = intent.context.get("options", {})
    # ...
```

2. **Error Handling**: Implement comprehensive error handling
```python
@plugin_handler("risky_operation")
async def risky_operation(self, intent: Intent) -> Response:
    try:
        result = await self._perform_operation()
        return Response(success=True, message="Operation completed", data=result)
    
    except FileNotFoundError as e:
        self.logger.error(f"File not found: {e}")
        return Response(success=False, message="Required file not found")
    
    except PermissionError as e:
        self.logger.error(f"Permission denied: {e}")
        return Response(success=False, message="Insufficient permissions")
    
    except Exception as e:
        self.logger.error(f"Unexpected error: {e}")
        return Response(success=False, message="An unexpected error occurred")
```

3. **Logging**: Use structured logging
```python
import structlog

class WellLoggedPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.logger = structlog.get_logger(__name__)
    
    @plugin_handler("important_operation")
    async def important_operation(self, intent: Intent) -> Response:
        self.logger.info(
            "Starting important operation",
            user_id=intent.user_id,
            operation_type="important"
        )
        
        try:
            result = await self._do_operation()
            
            self.logger.info(
                "Operation completed successfully",
                result_count=len(result),
                duration=result.get("duration")
            )
            
            return Response(success=True, data=result)
            
        except Exception as e:
            self.logger.error(
                "Operation failed",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
```

### Performance Optimization

1. **Async/Await**: Use async programming for I/O operations
```python
import asyncio
import aiofiles

@plugin_handler("process_large_file")
async def process_large_file(self, intent: Intent) -> Response:
    file_path = intent.context.get("file_path")
    
    # Async file operations
    async with aiofiles.open(file_path, 'r') as f:
        content = await f.read()
    
    # Async processing
    tasks = [
        self._process_chunk(chunk) 
        for chunk in self._split_content(content)
    ]
    
    results = await asyncio.gather(*tasks)
    
    return Response(success=True, data=results)
```

2. **Caching**: Implement intelligent caching
```python
from functools import lru_cache
import time

class CachedPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self._cache = {}
        self._cache_ttl = 3600  # 1 hour
    
    async def _get_cached_result(self, key: str):
        """Get cached result if still valid."""
        if key in self._cache:
            result, timestamp = self._cache[key]
            if time.time() - timestamp < self._cache_ttl:
                return result
        return None
    
    async def _cache_result(self, key: str, result):
        """Cache result with timestamp."""
        self._cache[key] = (result, time.time())
    
    @plugin_handler("expensive_operation")
    async def expensive_operation(self, intent: Intent) -> Response:
        cache_key = f"expensive_{hash(intent.text)}"
        
        # Check cache first
        cached = await self._get_cached_result(cache_key)
        if cached:
            return Response(success=True, data=cached, from_cache=True)
        
        # Perform expensive operation
        result = await self._do_expensive_work()
        
        # Cache result
        await self._cache_result(cache_key, result)
        
        return Response(success=True, data=result)
```

3. **Resource Management**: Properly manage system resources
```python
import psutil
from contextlib import asynccontextmanager

class ResourceManagedPlugin(BasePlugin):
    
    @asynccontextmanager
    async def _resource_monitor(self):
        """Monitor resource usage during operations."""
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        try:
            yield
        finally:
            final_memory = process.memory_info().rss
            memory_used = final_memory - initial_memory
            
            self.logger.info(
                "Operation completed",
                memory_used_mb=memory_used / 1024 / 1024
            )
    
    @plugin_handler("resource_intensive")
    async def resource_intensive_operation(self, intent: Intent) -> Response:
        async with self._resource_monitor():
            # Perform resource-intensive work
            result = await self._heavy_computation()
            
            return Response(success=True, data=result)
```

### Security Best Practices

1. **Input Validation**: Always validate user inputs
```python
from pathlib import Path
import re

class SecurePlugin(BasePlugin):
    
    def _validate_file_path(self, path: str) -> bool:
        """Validate file path for security."""
        try:
            # Resolve path and check if it's within allowed directories
            resolved = Path(path).resolve()
            allowed_dirs = [
                Path.home(),
                Path("/tmp"),
                Path("/var/tmp")
            ]
            
            return any(
                str(resolved).startswith(str(allowed_dir))
                for allowed_dir in allowed_dirs
            )
        except Exception:
            return False
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent directory traversal."""
        # Remove dangerous characters
        sanitized = re.sub(r'[^\w\-_.]', '_', filename)
        
        # Remove path separators
        sanitized = sanitized.replace('/', '_').replace('\\', '_')
        
        # Limit length
        return sanitized[:255]
    
    @plugin_handler("secure_file_operation")
    async def secure_file_operation(self, intent: Intent) -> Response:
        file_path = intent.context.get("file_path")
        
        if not self._validate_file_path(file_path):
            return Response(
                success=False,
                message="Access to this path is not allowed"
            )
        
        # Proceed with secure operation
        result = await self._process_file(file_path)
        return Response(success=True, data=result)
```

2. **Permission Checking**: Verify permissions before operations
```python
import os
import stat

class PermissionAwarePlugin(BasePlugin):
    
    def _check_file_permissions(self, file_path: str, required_perms: str) -> bool:
        """Check if file has required permissions."""
        try:
            file_stat = os.stat(file_path)
            file_mode = stat.filemode(file_stat.st_mode)
            
            if 'r' in required_perms and not os.access(file_path, os.R_OK):
                return False
            if 'w' in required_perms and not os.access(file_path, os.W_OK):
                return False
            if 'x' in required_perms and not os.access(file_path, os.X_OK):
                return False
                
            return True
        except OSError:
            return False
    
    @plugin_handler("modify_file")
    async def modify_file(self, intent: Intent) -> Response:
        file_path = intent.context.get("file_path")
        
        if not self._check_file_permissions(file_path, "rw"):
            return Response(
                success=False,
                message="Insufficient permissions to modify file"
            )
        
        # Proceed with modification
        # ...
```

---

## 🧪 Testing & Debugging

### Comprehensive Testing Strategy

```python
# tests/test_comprehensive.py
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.main import MyPlugin
from astros.types import Intent, Response

class TestMyPlugin:
    
    @pytest.fixture
    def plugin(self):
        """Create plugin instance for testing."""
        plugin = MyPlugin()
        plugin.logger = Mock()
        plugin.storage = AsyncMock()
        return plugin
    
    @pytest.fixture
    def sample_intent(self):
        """Create sample intent for testing."""
        return Intent(
            text="test command",
            user_id="test_user",
            context={"test": "data"}
        )
    
    @pytest.mark.asyncio
    async def test_successful_operation(self, plugin, sample_intent):
        """Test successful operation."""
        with patch.object(plugin, '_internal_method', return_value="success"):
            response = await plugin.my_handler(sample_intent)
            
            assert response.success is True
            assert "success" in response.message
    
    @pytest.mark.asyncio
    async def test_error_handling(self, plugin, sample_intent):
        """Test error handling."""
        with patch.object(plugin, '_internal_method', side_effect=Exception("Test error")):
            response = await plugin.my_handler(sample_intent)
            
            assert response.success is False
            assert "error" in response.message.lower()
    
    @pytest.mark.parametrize("input_data,expected_output", [
        ({"type": "A"}, "result_A"),
        ({"type": "B"}, "result_B"),
        ({"type": "C"}, "result_C"),
    ])
    @pytest.mark.asyncio
    async def test_different_inputs(self, plugin, input_data, expected_output):
        """Test plugin with different input combinations."""
        intent = Intent(text="test", context=input_data)
        response = await plugin.my_handler(intent)
        
        assert expected_output in response.data
    
    def test_performance(self, plugin):
        """Test plugin performance."""
        import time
        
        start_time = time.time()
        # Run performance-critical code
        end_time = time.time()
        
        duration = end_time - start_time
        assert duration < 1.0  # Should complete within 1 second
```

### Integration Testing

```python
# tests/test_integration.py
import pytest
from astros.testing import AstrOSTestClient

class TestPluginIntegration:
    
    @pytest.fixture
    async def client(self):
        """Create AstrOS test client."""
        client = AstrOSTestClient()
        await client.load_plugin("my-plugin")
        return client
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, client):
        """Test complete user workflow."""
        # Simulate user interaction
        response1 = await client.process_text("start the process")
        assert response1.success
        
        # Follow up interaction
        response2 = await client.process_text("continue with next step")
        assert response2.success
        
        # Final interaction
        response3 = await client.process_text("finish the process")
        assert response3.success
        assert "completed" in response3.message.lower()
```

### Debugging Tools

```python
# src/debugging.py
import functools
import time
from typing import Any, Callable

def debug_handler(func: Callable) -> Callable:
    """Decorator to add debugging information to handlers."""
    
    @functools.wraps(func)
    async def wrapper(self, intent: Intent) -> Response:
        start_time = time.time()
        
        self.logger.debug(
            f"Handler {func.__name__} called",
            intent_text=intent.text,
            user_id=intent.user_id,
            context_keys=list(intent.context.keys())
        )
        
        try:
            response = await func(self, intent)
            
            duration = time.time() - start_time
            self.logger.debug(
                f"Handler {func.__name__} completed",
                success=response.success,
                duration=duration,
                response_length=len(response.message)
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                f"Handler {func.__name__} failed",
                error=str(e),
                duration=duration
            )
            raise
    
    return wrapper

# Usage
class DebuggablePlugin(BasePlugin):
    
    @debug_handler
    @plugin_handler("debug_operation")
    async def debug_operation(self, intent: Intent) -> Response:
        # Your handler code here
        return Response(success=True, message="Debug complete")
```

---

## 📦 Distribution

### Plugin Packaging

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="astros-awesome-plugin",
    version="1.0.0",
    description="An awesome plugin for AstrOS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/your-username/astros-awesome-plugin",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    install_requires=[
        "astros>=1.0.0",
        "requests>=2.28.0",
        "aiofiles>=23.0.0",
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "ruff>=0.0.261",
            "mypy>=1.0.0",
        ]
    },
    
    python_requires=">=3.12",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    
    entry_points={
        "astros.plugins": [
            "awesome-plugin = awesome_plugin.main:AwesomePlugin",
        ]
    },
    
    include_package_data=True,
    zip_safe=False,
)
```

### Plugin Registry

Submit your plugin to the AstrOS Plugin Registry:

```bash
# Build distribution packages
python -m build

# Test the package
twine check dist/*

# Upload to test repository first
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ astros-awesome-plugin

# Upload to production
twine upload dist/*
```

### Documentation

Create comprehensive documentation:

```markdown
# Awesome Plugin Documentation

## Installation

```bash
pip install astros-awesome-plugin
```

## Configuration

```yaml
# Add to your AstrOS config
plugins:
  awesome-plugin:
    enabled: true
    settings:
      feature_x: true
      max_items: 100
```

## Usage Examples

### Basic Usage
"Organize my files by type"

### Advanced Usage
"Organize my Downloads folder by content using AI analysis"

## API Reference

### Handlers

#### `organize_files`
Organizes files in a directory.

**Parameters:**
- `path`: Directory path to organize
- `method`: Organization method ("by_type", "by_date", "by_content")
- `dry_run`: Preview changes without applying them

**Returns:**
Response with organization results.
```

---

## 🚀 Advanced Topics

### Custom AI Providers

```python
# src/custom_ai.py
from astros.ai.base import BaseAIProvider
from typing import Dict, Any

class CustomAIProvider(BaseAIProvider):
    """Custom AI provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.endpoint = config.get("endpoint")
    
    async def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text completion."""
        # Your custom AI implementation
        pass
    
    async def chat(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Generate chat response."""
        # Your custom chat implementation
        pass

# Register custom provider
from astros.ai import register_provider
register_provider("custom", CustomAIProvider)
```

### Plugin Communications

```python
# Plugins can communicate with each other
class CommunicatingPlugin(BasePlugin):
    
    @plugin_handler("coordinate_action")
    async def coordinate_action(self, intent: Intent) -> Response:
        """Coordinate with other plugins."""
        
        # Call another plugin
        file_result = await self.call_plugin(
            "file-manager",
            "list_files",
            {"path": "/home/user/Documents"}
        )
        
        if not file_result.success:
            return Response(
                success=False,
                message="Failed to get file list"
            )
        
        # Process the results
        files = file_result.data.get("files", [])
        
        # Send notification through notification plugin
        await self.call_plugin(
            "notification-manager",
            "send_notification",
            {
                "title": "File Processing Complete",
                "message": f"Processed {len(files)} files",
                "type": "info"
            }
        )
        
        return Response(
            success=True,
            message=f"Coordinated action completed for {len(files)} files"
        )
```

### System Integration

```python
# Deep system integration
import dbus
from gi.repository import Gio

class SystemIntegratedPlugin(BasePlugin):
    
    async def initialize(self):
        """Initialize system connections."""
        # Connect to system D-Bus
        self.system_bus = dbus.SystemBus()
        
        # Connect to session D-Bus
        self.session_bus = dbus.SessionBus()
        
        # Monitor file system changes
        self.file_monitor = Gio.File.new_for_path("/home/user/Documents")
        self.monitor = self.file_monitor.monitor_directory(
            Gio.FileMonitorFlags.NONE,
            None
        )
        self.monitor.connect("changed", self._on_file_changed)
    
    def _on_file_changed(self, monitor, file, other_file, event_type):
        """Handle file system changes."""
        self.logger.info(f"File changed: {file.get_path()}")
        # React to file system changes
    
    @plugin_handler("system_control")
    async def system_control(self, intent: Intent) -> Response:
        """Control system services."""
        service_name = intent.context.get("service")
        action = intent.context.get("action")
        
        try:
            # Use systemd D-Bus interface
            systemd = self.system_bus.get_object(
                'org.freedesktop.systemd1',
                '/org/freedesktop/systemd1'
            )
            
            if action == "start":
                systemd.StartUnit(f"{service_name}.service", "replace")
            elif action == "stop":
                systemd.StopUnit(f"{service_name}.service", "replace")
            
            return Response(
                success=True,
                message=f"Service {service_name} {action}ed successfully"
            )
            
        except Exception as e:
            return Response(
                success=False,
                message=f"Failed to {action} service: {str(e)}"
            )
```

---

## 📚 Resources & Next Steps

### Essential Reading
- **[AstrOS Core API](../api/core.md)** - Core system APIs
- **[Plugin API Reference](../api/plugins.md)** - Complete plugin API
- **[AI Provider Guide](../api/ai.md)** - AI integration patterns
- **[System Integration](../api/system.md)** - Deep system integration

### Example Plugins
- **[File Manager Plugin](https://github.com/AstrOS-Project/plugin-file-manager)** - Reference implementation
- **[AI Assistant Plugin](https://github.com/AstrOS-Project/plugin-ai-assistant)** - Advanced AI features
- **[System Monitor Plugin](https://github.com/AstrOS-Project/plugin-system-monitor)** - System integration

### Community
- **[Discord](https://discord.gg/astros)** - Plugin development discussions
- **[GitHub Discussions](https://github.com/orgs/AstrOS-Project/discussions)** - Design discussions
- **[Plugin Registry](https://plugins.astros.org)** - Discover and share plugins

### Tools
- **[Plugin Generator](../../scripts/create-plugin.py)** - Scaffold new plugins
- **[Plugin Validator](../../scripts/validate-plugin.py)** - Validate plugin structure
- **[Test Runner](../../scripts/test-plugin.py)** - Run plugin tests

---

<div align="center">

### 🚀 Ready to Build Amazing Plugins?

**[💬 Join Discord](https://discord.gg/astros)** • **[📖 API Docs](../api/)** • **[🔍 Find Issues](https://github.com/search?q=org%3AAstrOS-Project+label%3A%22plugin+help+wanted%22&type=issues)**

*Build the future of AI-powered computing, one plugin at a time!*

</div>