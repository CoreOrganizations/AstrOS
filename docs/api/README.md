# AstrOS API Reference 📚

Complete API documentation for AstrOS core system and plugin development.

## 📋 Table of Contents

- [Core API](#-core-api)
- [Plugin API](#-plugin-api)
- [AI Provider API](#-ai-provider-api)
- [Storage API](#-storage-api)
- [System Integration API](#-system-integration-api)
- [Authentication & Security](#-authentication--security)
- [WebSocket API](#-websocket-api)
- [REST API](#-rest-api)

---

## 🔧 Core API

### AstrOS Agent

The main orchestrator for all system interactions.

#### `class AstrOSAgent`

```python
class AstrOSAgent:
    """Main AstrOS system orchestrator."""
    
    def __init__(self, config_path: str):
        """Initialize AstrOS agent.
        
        Args:
            config_path: Path to configuration file
        """
    
    async def start(self) -> None:
        """Start the AstrOS agent."""
    
    async def stop(self) -> None:
        """Stop the AstrOS agent gracefully."""
    
    async def process_request(self, request: UserRequest) -> Response:
        """Process a user request.
        
        Args:
            request: User request to process
            
        Returns:
            Response object with results
            
        Raises:
            ProcessingError: If request processing fails
        """
    
    async def get_status(self) -> SystemStatus:
        """Get current system status."""
    
    def register_plugin(self, plugin: BasePlugin) -> None:
        """Register a plugin with the system.
        
        Args:
            plugin: Plugin instance to register
        """
```

### Intent Recognition

#### `class IntentRecognizer`

```python
class IntentRecognizer:
    """Recognizes user intents from natural language."""
    
    async def recognize(self, request: UserRequest) -> Intent:
        """Recognize intent from user request.
        
        Args:
            request: Raw user request
            
        Returns:
            Parsed intent with confidence score
        """
    
    async def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of extracted entities
        """
    
    def register_intent_handler(
        self, 
        intent_type: str, 
        handler: Callable
    ) -> None:
        """Register custom intent handler.
        
        Args:
            intent_type: Type of intent to handle
            handler: Function to handle the intent
        """
```

### Response Generation

#### `class ResponseGenerator`

```python
class ResponseGenerator:
    """Generates responses for user requests."""
    
    async def generate(
        self, 
        result: ProcessingResult, 
        context: Context
    ) -> Response:
        """Generate response from processing result.
        
        Args:
            result: Processing result to respond to
            context: Current user context
            
        Returns:
            Formatted response for user
        """
    
    async def generate_suggestions(
        self, 
        intent: Intent
    ) -> List[str]:
        """Generate follow-up suggestions.
        
        Args:
            intent: Current user intent
            
        Returns:
            List of suggested actions
        """
    
    def set_response_format(self, format_type: ResponseFormat) -> None:
        """Set response format.
        
        Args:
            format_type: Format for responses (text, voice, gui)
        """
```

---

## 🧩 Plugin API

### Base Plugin Class

#### `class BasePlugin`

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class BasePlugin(ABC):
    """Base class for all AstrOS plugins."""
    
    # Plugin metadata (must be defined by subclass)
    name: str
    version: str
    description: str
    author: str
    
    # Plugin capabilities
    handles: List[str] = []
    requires_ai: bool = False
    requires_permissions: List[str] = []
    
    def __init__(self):
        """Initialize plugin."""
        self.logger = self._setup_logger()
        self.storage = None  # Set by plugin manager
        self.config = None   # Set by plugin manager
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize plugin resources."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Clean up plugin resources."""
        pass
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if plugin can handle intent.
        
        Args:
            intent: Intent to check
            
        Returns:
            True if plugin can handle intent
        """
    
    def get_handlers(self, intent: Intent) -> List[PluginHandler]:
        """Get handlers for intent.
        
        Args:
            intent: Intent to get handlers for
            
        Returns:
            List of applicable handlers
        """
    
    async def call_plugin(
        self, 
        plugin_name: str, 
        handler_name: str, 
        data: Dict[str, Any]
    ) -> Response:
        """Call another plugin.
        
        Args:
            plugin_name: Name of plugin to call
            handler_name: Handler method to call
            data: Data to pass to handler
            
        Returns:
            Response from the called plugin
        """
```

### Plugin Decorators

#### `@plugin_handler`

```python
def plugin_handler(
    intent_type: str, 
    priority: int = 5,
    requires_permissions: Optional[List[str]] = None
) -> Callable:
    """Decorator to mark methods as plugin handlers.
    
    Args:
        intent_type: Type of intent this handler processes
        priority: Handler priority (1-10, higher = more priority)
        requires_permissions: Additional permissions required
        
    Example:
        @plugin_handler("file_operation", priority=8)
        async def handle_files(self, intent: Intent) -> Response:
            # Handler implementation
            pass
    """
```

#### `@requires_permission`

```python
def requires_permission(*permissions: str) -> Callable:
    """Decorator to specify required permissions.
    
    Args:
        permissions: Required permission names
        
    Example:
        @requires_permission("file_system", "network")
        @plugin_handler("backup_files")
        async def backup_files(self, intent: Intent) -> Response:
            # Handler implementation
            pass
    """
```

### Plugin Storage API

#### `class PluginStorage`

```python
class PluginStorage:
    """Provides storage interface for plugins."""
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from plugin storage.
        
        Args:
            key: Storage key
            default: Default value if key not found
            
        Returns:
            Stored value or default
        """
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in plugin storage.
        
        Args:
            key: Storage key
            value: Value to store
            ttl: Time to live in seconds (optional)
        """
    
    async def delete(self, key: str) -> bool:
        """Delete value from storage.
        
        Args:
            key: Storage key to delete
            
        Returns:
            True if key was deleted
        """
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in storage.
        
        Args:
            key: Storage key to check
            
        Returns:
            True if key exists
        """
    
    async def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix.
        
        Args:
            prefix: Key prefix to filter by
            
        Returns:
            List of matching keys
        """
```

---

## 🤖 AI Provider API

### Base AI Provider

#### `class BaseAIProvider`

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseAIProvider(ABC):
    """Base class for AI providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize AI provider.
        
        Args:
            config: Provider configuration
        """
        self.config = config
    
    @abstractmethod
    async def complete(
        self, 
        prompt: str,
        max_tokens: int = 150,
        temperature: float = 0.7,
        **kwargs
    ) -> AIResponse:
        """Generate text completion.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Generation temperature (0.0-1.0)
            **kwargs: Provider-specific arguments
            
        Returns:
            AI response with generated text
        """
    
    @abstractmethod
    async def chat(
        self, 
        messages: List[Message],
        max_tokens: int = 150,
        temperature: float = 0.7,
        **kwargs
    ) -> AIResponse:
        """Generate chat response.
        
        Args:
            messages: Conversation history
            max_tokens: Maximum tokens to generate
            temperature: Generation temperature
            **kwargs: Provider-specific arguments
            
        Returns:
            AI response with chat completion
        """
    
    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
    
    async def analyze_image(
        self, 
        image_path: str, 
        prompt: str
    ) -> AIResponse:
        """Analyze image with vision model.
        
        Args:
            image_path: Path to image file
            prompt: Analysis prompt
            
        Returns:
            AI response with image analysis
        """
```

### AI Response Types

#### `class AIResponse`

```python
@dataclass
class AIResponse:
    """Response from AI provider."""
    
    content: str
    tokens_used: int
    model: str
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "tokens_used": self.tokens_used,
            "model": self.model,
            "confidence": self.confidence,
            "metadata": self.metadata
        }
```

#### `class Message`

```python
@dataclass
class Message:
    """Chat message."""
    
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### AI Utilities

#### `class AIProvider` (Factory)

```python
class AIProvider:
    """Factory for creating AI providers."""
    
    @staticmethod
    def create(
        provider: str, 
        config: Dict[str, Any]
    ) -> BaseAIProvider:
        """Create AI provider instance.
        
        Args:
            provider: Provider name ("openai", "anthropic", "local")
            config: Provider configuration
            
        Returns:
            AI provider instance
            
        Raises:
            ValueError: If provider is not supported
        """
    
    @staticmethod
    def list_providers() -> List[str]:
        """List available AI providers."""
    
    @staticmethod
    def register_provider(
        name: str, 
        provider_class: type
    ) -> None:
        """Register custom AI provider.
        
        Args:
            name: Provider name
            provider_class: Provider class
        """
```

---

## 💾 Storage API

### Database Operations

#### `class DatabaseManager`

```python
class DatabaseManager:
    """Manages database operations."""
    
    def __init__(self, config: DatabaseConfig):
        """Initialize database manager."""
    
    async def execute_query(
        self, 
        query: str, 
        params: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Execute SQL query.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            Query results
        """
    
    async def insert(
        self, 
        table: str, 
        data: Dict[str, Any]
    ) -> str:
        """Insert record into table.
        
        Args:
            table: Table name
            data: Record data
            
        Returns:
            Inserted record ID
        """
    
    async def update(
        self, 
        table: str, 
        record_id: str, 
        data: Dict[str, Any]
    ) -> bool:
        """Update record in table.
        
        Args:
            table: Table name
            record_id: Record ID to update
            data: Updated data
            
        Returns:
            True if record was updated
        """
    
    async def delete(self, table: str, record_id: str) -> bool:
        """Delete record from table.
        
        Args:
            table: Table name
            record_id: Record ID to delete
            
        Returns:
            True if record was deleted
        """
```

### Vector Store Operations

#### `class VectorStore`

```python
class VectorStore:
    """Manages vector embeddings for semantic search."""
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        collection: str = "default"
    ) -> List[str]:
        """Add documents to vector store.
        
        Args:
            documents: List of document texts
            metadatas: List of document metadata
            collection: Collection name
            
        Returns:
            List of document IDs
        """
    
    async def search(
        self,
        query: str,
        n_results: int = 5,
        collection: str = "default",
        filter_metadata: Optional[Dict] = None
    ) -> List[SearchResult]:
        """Search for similar documents.
        
        Args:
            query: Search query
            n_results: Number of results to return
            collection: Collection to search
            filter_metadata: Metadata filters
            
        Returns:
            List of search results
        """
    
    async def get_document(
        self, 
        document_id: str, 
        collection: str = "default"
    ) -> Optional[Document]:
        """Get document by ID.
        
        Args:
            document_id: Document ID
            collection: Collection name
            
        Returns:
            Document if found
        """
```

---

## 🔗 System Integration API

### File System Operations

#### `class FileManager`

```python
class FileManager:
    """Manages file system operations."""
    
    async def read_file(self, path: str) -> str:
        """Read text file content.
        
        Args:
            path: File path
            
        Returns:
            File content
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If no read permission
        """
    
    async def write_file(self, path: str, content: str) -> None:
        """Write content to file.
        
        Args:
            path: File path
            content: Content to write
            
        Raises:
            PermissionError: If no write permission
        """
    
    async def list_directory(self, path: str) -> List[FileInfo]:
        """List directory contents.
        
        Args:
            path: Directory path
            
        Returns:
            List of file information
        """
    
    async def create_directory(self, path: str) -> None:
        """Create directory.
        
        Args:
            path: Directory path to create
        """
    
    async def move_file(self, source: str, destination: str) -> None:
        """Move file or directory.
        
        Args:
            source: Source path
            destination: Destination path
        """
    
    async def copy_file(self, source: str, destination: str) -> None:
        """Copy file or directory.
        
        Args:
            source: Source path
            destination: Destination path
        """
    
    async def delete_file(self, path: str) -> None:
        """Delete file or directory.
        
        Args:
            path: Path to delete
        """
```

### System Process Management

#### `class ProcessManager`

```python
class ProcessManager:
    """Manages system processes."""
    
    async def run_command(
        self, 
        command: str, 
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> ProcessResult:
        """Run system command.
        
        Args:
            command: Command to run
            cwd: Working directory
            env: Environment variables
            timeout: Timeout in seconds
            
        Returns:
            Process execution result
        """
    
    async def get_running_processes(self) -> List[ProcessInfo]:
        """Get list of running processes."""
    
    async def kill_process(self, pid: int) -> bool:
        """Kill process by PID.
        
        Args:
            pid: Process ID
            
        Returns:
            True if process was killed
        """
    
    async def get_system_info(self) -> SystemInfo:
        """Get system information."""
```

---

## 🔐 Authentication & Security

### Authentication Manager

#### `class AuthenticationManager`

```python
class AuthenticationManager:
    """Manages user authentication."""
    
    async def authenticate_user(
        self, 
        username: str, 
        password: str
    ) -> Optional[User]:
        """Authenticate user credentials.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            User object if authentication successful
        """
    
    async def create_session(self, user: User) -> Session:
        """Create user session.
        
        Args:
            user: Authenticated user
            
        Returns:
            New session object
        """
    
    async def validate_session(self, session_id: str) -> Optional[Session]:
        """Validate session.
        
        Args:
            session_id: Session ID to validate
            
        Returns:
            Session if valid
        """
    
    async def revoke_session(self, session_id: str) -> bool:
        """Revoke user session.
        
        Args:
            session_id: Session ID to revoke
            
        Returns:
            True if session was revoked
        """
```

### Permission Manager

#### `class PermissionManager`

```python
class PermissionManager:
    """Manages user permissions."""
    
    async def check_permission(
        self, 
        user_id: str, 
        permission: str, 
        resource: Optional[str] = None
    ) -> bool:
        """Check user permission.
        
        Args:
            user_id: User ID
            permission: Permission name
            resource: Resource identifier (optional)
            
        Returns:
            True if user has permission
        """
    
    async def grant_permission(
        self, 
        user_id: str, 
        permission: str,
        resource: Optional[str] = None
    ) -> None:
        """Grant permission to user.
        
        Args:
            user_id: User ID
            permission: Permission name
            resource: Resource identifier (optional)
        """
    
    async def revoke_permission(
        self, 
        user_id: str, 
        permission: str,
        resource: Optional[str] = None
    ) -> None:
        """Revoke permission from user.
        
        Args:
            user_id: User ID
            permission: Permission name
            resource: Resource identifier (optional)
        """
    
    async def list_permissions(self, user_id: str) -> List[Permission]:
        """List user permissions.
        
        Args:
            user_id: User ID
            
        Returns:
            List of user permissions
        """
```

---

## 🌐 WebSocket API

### Real-time Communication

#### WebSocket Endpoints

```python
# WebSocket connection
ws://localhost:8000/ws/{user_id}

# Authentication
{
    "type": "auth",
    "data": {
        "session_id": "session_123",
        "token": "auth_token"
    }
}

# Send request
{
    "type": "request",
    "data": {
        "text": "organize my files",
        "context": {"path": "/home/user/Documents"}
    }
}

# Receive response
{
    "type": "response",
    "data": {
        "success": true,
        "message": "Files organized successfully",
        "data": {"files_processed": 42}
    }
}

# Status updates
{
    "type": "status",
    "data": {
        "status": "processing",
        "progress": 50,
        "message": "Analyzing files..."
    }
}
```

#### `class WebSocketManager`

```python
class WebSocketManager:
    """Manages WebSocket connections."""
    
    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        """Handle new WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
        """
    
    async def disconnect(self, user_id: str) -> None:
        """Handle WebSocket disconnection.
        
        Args:
            user_id: User ID
        """
    
    async def send_message(
        self, 
        user_id: str, 
        message: Dict[str, Any]
    ) -> None:
        """Send message to user.
        
        Args:
            user_id: Target user ID
            message: Message to send
        """
    
    async def broadcast_message(self, message: Dict[str, Any]) -> None:
        """Broadcast message to all connected users.
        
        Args:
            message: Message to broadcast
        """
```

---

## 🌍 REST API

### HTTP Endpoints

#### Authentication

```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "password123"
}

Response:
{
    "success": true,
    "data": {
        "user_id": "user_123",
        "session_id": "session_456",
        "token": "jwt_token_here"
    }
}
```

#### Process Request

```http
POST /api/v1/process
Authorization: Bearer jwt_token_here
Content-Type: application/json

{
    "text": "show me my files",
    "context": {
        "path": "/home/user/Documents"
    }
}

Response:
{
    "success": true,
    "message": "Found 25 files in Documents",
    "data": {
        "files": ["file1.txt", "file2.pdf"],
        "total_count": 25
    }
}
```

#### Plugin Management

```http
GET /api/v1/plugins
Authorization: Bearer jwt_token_here

Response:
{
    "success": true,
    "data": {
        "plugins": [
            {
                "name": "file-manager",
                "version": "1.0.0",
                "status": "active",
                "description": "File management plugin"
            }
        ]
    }
}
```

### HTTP Client

#### `class HTTPClient`

```python
class HTTPClient:
    """HTTP client for AstrOS API."""
    
    def __init__(self, base_url: str, token: Optional[str] = None):
        """Initialize HTTP client.
        
        Args:
            base_url: API base URL
            token: Authentication token
        """
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login and get authentication token.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Login response with token
        """
    
    async def process_request(
        self, 
        text: str, 
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process request via API.
        
        Args:
            text: Request text
            context: Request context
            
        Returns:
            Processing response
        """
    
    async def get_plugins(self) -> List[Dict[str, Any]]:
        """Get list of available plugins."""
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
```

---

## 📊 Data Types

### Common Data Types

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum

@dataclass
class UserRequest:
    """User request data."""
    text: str
    user_id: str
    session_id: str
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Intent:
    """Parsed user intent."""
    type: str
    confidence: float
    entities: Dict[str, Any]
    context: Dict[str, Any]
    timestamp: datetime
    original_request: UserRequest

@dataclass
class Response:
    """System response."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    suggestions: List[str] = field(default_factory=list)
    requires_followup: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

class ResponseFormat(Enum):
    """Response format types."""
    TEXT = "text"
    VOICE = "voice"
    GUI = "gui"
    JSON = "json"

@dataclass
class SystemStatus:
    """System status information."""
    status: str  # "running", "starting", "stopping", "error"
    uptime: int  # Seconds
    plugins_loaded: int
    active_sessions: int
    memory_usage: float  # MB
    cpu_usage: float     # Percentage
```

### Error Types

```python
class AstrOSError(Exception):
    """Base exception for AstrOS errors."""
    pass

class PluginError(AstrOSError):
    """Plugin-related errors."""
    pass

class AIError(AstrOSError):
    """AI provider errors."""
    pass

class PermissionError(AstrOSError):
    """Permission-related errors."""
    pass

class ProcessingError(AstrOSError):
    """Request processing errors."""
    pass

class AuthenticationError(AstrOSError):
    """Authentication errors."""
    pass
```

---

## 🔧 Configuration

### Configuration Classes

```python
@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str
    pool_size: int = 10
    echo: bool = False
    
@dataclass
class AIConfig:
    """AI configuration."""
    default_provider: str
    providers: Dict[str, Dict[str, Any]]
    max_tokens: int = 150
    temperature: float = 0.7

@dataclass
class PluginConfig:
    """Plugin configuration."""
    auto_load: bool = True
    plugin_paths: List[str] = field(default_factory=list)
    enabled_plugins: List[str] = field(default_factory=list)
    plugin_timeout: int = 30

@dataclass
class AstrOSConfig:
    """Main AstrOS configuration."""
    database: DatabaseConfig
    ai: AIConfig
    plugins: PluginConfig
    debug: bool = False
    log_level: str = "INFO"
```

---

<div align="center">

### 📚 Need More API Details?

**[💬 Join Discord](https://discord.gg/astros)** • **[🔧 Development Guide](../development.md)** • **[🧩 Plugin Tutorial](../plugin-development.md)**

*Complete API reference for building with AstrOS!*

</div>