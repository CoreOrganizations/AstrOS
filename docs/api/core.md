# Core API Reference 🔧

Complete reference for AstrOS core system APIs.

---

## AstrOS Agent

### `class AstrOSAgent`

The main orchestrator for all AstrOS operations.

```python
from astros.core import AstrOSAgent
from astros.types import UserRequest, Response, SystemStatus

agent = AstrOSAgent(config_path="config/astros.yaml")
await agent.start()
```

#### Methods

##### `__init__(config_path: str)`

Initialize the AstrOS agent with configuration.

**Parameters:**
- `config_path` (str): Path to YAML configuration file

**Example:**
```python
agent = AstrOSAgent("config/production.yaml")
```

##### `start() -> None`

Start the AstrOS agent and all subsystems.

**Raises:**
- `StartupError`: If agent fails to start

**Example:**
```python
await agent.start()
```

##### `stop() -> None`

Gracefully stop the AstrOS agent.

**Example:**
```python
await agent.stop()
```

##### `process_request(request: UserRequest) -> Response`

Process a user request through the complete pipeline.

**Parameters:**
- `request` (UserRequest): User request to process

**Returns:**
- `Response`: Processed response

**Raises:**
- `ProcessingError`: If request processing fails

**Example:**
```python
request = UserRequest(
    text="organize my files",
    user_id="user_123",
    session_id="session_456",
    timestamp=datetime.now()
)

response = await agent.process_request(request)
print(response.message)
```

##### `get_status() -> SystemStatus`

Get current system status and metrics.

**Returns:**
- `SystemStatus`: Current system status

**Example:**
```python
status = await agent.get_status()
print(f"System status: {status.status}")
print(f"Uptime: {status.uptime} seconds")
```

##### `register_plugin(plugin: BasePlugin) -> None`

Register a plugin with the system.

**Parameters:**
- `plugin` (BasePlugin): Plugin instance to register

**Example:**
```python
from my_plugin import MyAwesomePlugin

plugin = MyAwesomePlugin()
agent.register_plugin(plugin)
```

---

## Intent Recognition

### `class IntentRecognizer`

Recognizes user intents from natural language input.

```python
from astros.core.intent import IntentRecognizer

recognizer = IntentRecognizer(config=intent_config)
```

#### Methods

##### `recognize(request: UserRequest) -> Intent`

Recognize intent from user request using NLP models.

**Parameters:**
- `request` (UserRequest): Raw user request

**Returns:**
- `Intent`: Parsed intent with confidence score

**Example:**
```python
request = UserRequest(
    text="show me all Python files in my project",
    user_id="user_123",
    session_id="session_456",
    timestamp=datetime.now()
)

intent = await recognizer.recognize(request)
print(f"Intent type: {intent.type}")
print(f"Confidence: {intent.confidence}")
print(f"Entities: {intent.entities}")
```

##### `extract_entities(text: str) -> Dict[str, Any]`

Extract named entities from text.

**Parameters:**
- `text` (str): Text to analyze

**Returns:**
- `Dict[str, Any]`: Dictionary of extracted entities

**Example:**
```python
entities = await recognizer.extract_entities(
    "Find all PDF files larger than 10MB created last week"
)
# Returns: {
#     "file_type": "PDF",
#     "size_constraint": "larger than 10MB",
#     "time_constraint": "last week"
# }
```

##### `register_intent_handler(intent_type: str, handler: Callable) -> None`

Register custom intent recognition handler.

**Parameters:**
- `intent_type` (str): Type of intent to handle
- `handler` (Callable): Function to handle intent recognition

**Example:**
```python
def custom_file_handler(text: str) -> Optional[Dict[str, Any]]:
    # Custom intent recognition logic
    if "special file operation" in text.lower():
        return {"type": "special_file_op", "confidence": 0.9}
    return None

recognizer.register_intent_handler("file_operations", custom_file_handler)
```

---

## Response Generation

### `class ResponseGenerator`

Generates natural language responses for user requests.

```python
from astros.core.response import ResponseGenerator

generator = ResponseGenerator(config=response_config)
```

#### Methods

##### `generate(result: ProcessingResult, context: Context) -> Response`

Generate response from processing result.

**Parameters:**
- `result` (ProcessingResult): Processing result to respond to
- `context` (Context): Current user context

**Returns:**
- `Response`: Formatted response for user

**Example:**
```python
response = await generator.generate(processing_result, user_context)
print(response.message)  # "I found 15 Python files in your project"
```

##### `generate_suggestions(intent: Intent) -> List[str]`

Generate follow-up suggestions based on intent.

**Parameters:**
- `intent` (Intent): Current user intent

**Returns:**
- `List[str]`: List of suggested actions

**Example:**
```python
suggestions = await generator.generate_suggestions(intent)
# Returns: [
#     "Would you like me to organize these files?",
#     "Shall I create a backup of these files?",
#     "Do you want to see file details?"
# ]
```

##### `set_response_format(format_type: ResponseFormat) -> None`

Set the format for generated responses.

**Parameters:**
- `format_type` (ResponseFormat): Format for responses

**Example:**
```python
from astros.types import ResponseFormat

generator.set_response_format(ResponseFormat.VOICE)
# Now responses will be optimized for voice output
```

---

## Context Management

### `class ContextManager`

Manages user context and conversation history.

```python
from astros.core.context import ContextManager

context_manager = ContextManager(config=context_config)
```

#### Methods

##### `get_context(user_id: str) -> Context`

Get current context for user.

**Parameters:**
- `user_id` (str): User identifier

**Returns:**
- `Context`: Current user context

**Example:**
```python
context = await context_manager.get_context("user_123")
print(f"Recent intents: {len(context.conversation_history)}")
```

##### `update_context(user_id: str, intent: Intent, response: Response) -> None`

Update user context with new interaction.

**Parameters:**
- `user_id` (str): User identifier
- `intent` (Intent): User intent
- `response` (Response): System response

**Example:**
```python
await context_manager.update_context(
    user_id="user_123",
    intent=user_intent,
    response=system_response
)
```

##### `clear_context(user_id: str) -> None`

Clear user context and history.

**Parameters:**
- `user_id` (str): User identifier

**Example:**
```python
await context_manager.clear_context("user_123")
```

##### `get_relevant_context(user_id: str, query: str) -> Dict[str, Any]`

Get context relevant to current query using semantic search.

**Parameters:**
- `user_id` (str): User identifier
- `query` (str): Current query

**Returns:**
- `Dict[str, Any]`: Relevant context information

**Example:**
```python
relevant = await context_manager.get_relevant_context(
    "user_123", 
    "organize files"
)
# Returns context about previous file operations
```

---

## Configuration Management

### `class ConfigManager`

Manages system configuration and settings.

```python
from astros.core.config import ConfigManager

config = ConfigManager.load("config/astros.yaml")
```

#### Methods

##### `load(config_path: str) -> AstrOSConfig`

Load configuration from file.

**Parameters:**
- `config_path` (str): Path to configuration file

**Returns:**
- `AstrOSConfig`: Loaded configuration

**Example:**
```python
config = ConfigManager.load("config/production.yaml")
```

##### `save(config: AstrOSConfig, config_path: str) -> None`

Save configuration to file.

**Parameters:**
- `config` (AstrOSConfig): Configuration to save
- `config_path` (str): Path to save configuration

**Example:**
```python
ConfigManager.save(config, "config/updated.yaml")
```

##### `get_plugin_config(plugin_name: str) -> Dict[str, Any]`

Get configuration for specific plugin.

**Parameters:**
- `plugin_name` (str): Name of plugin

**Returns:**
- `Dict[str, Any]`: Plugin configuration

**Example:**
```python
plugin_config = config.get_plugin_config("file-manager")
```

##### `update_config(updates: Dict[str, Any]) -> None`

Update configuration with new values.

**Parameters:**
- `updates` (Dict[str, Any]): Configuration updates

**Example:**
```python
config.update_config({
    "ai.default_provider": "local",
    "plugins.auto_load": False
})
```

---

## Event System

### `class EventBus`

System-wide event bus for component communication.

```python
from astros.core.events import EventBus

event_bus = EventBus()
```

#### Methods

##### `publish(event: str, data: Any, source: str) -> None`

Publish event to all subscribers.

**Parameters:**
- `event` (str): Event name
- `data` (Any): Event data
- `source` (str): Event source

**Example:**
```python
await event_bus.publish(
    "file.created",
    {"path": "/home/user/document.txt"},
    "file-manager"
)
```

##### `subscribe(event: str, handler: Callable, subscriber: str) -> None`

Subscribe to events.

**Parameters:**
- `event` (str): Event name to subscribe to
- `handler` (Callable): Event handler function
- `subscriber` (str): Subscriber identifier

**Example:**
```python
async def handle_file_created(event_data):
    print(f"New file created: {event_data['path']}")

await event_bus.subscribe("file.created", handle_file_created, "my-plugin")
```

##### `unsubscribe(event: str, subscriber: str) -> None`

Unsubscribe from events.

**Parameters:**
- `event` (str): Event name
- `subscriber` (str): Subscriber identifier

**Example:**
```python
await event_bus.unsubscribe("file.created", "my-plugin")
```

---

## Error Handling

### Exception Classes

```python
from astros.core.exceptions import (
    AstrOSError,
    ProcessingError,
    ConfigurationError,
    StartupError
)

try:
    await agent.process_request(request)
except ProcessingError as e:
    print(f"Processing failed: {e}")
except AstrOSError as e:
    print(f"System error: {e}")
```

#### `AstrOSError`

Base exception for all AstrOS errors.

#### `ProcessingError`

Raised when request processing fails.

#### `ConfigurationError`

Raised when configuration is invalid.

#### `StartupError`

Raised when system fails to start.

#### `PluginError`

Raised when plugin operations fail.

---

## Utilities

### `class Logger`

Structured logging for AstrOS components.

```python
from astros.core.utils import Logger

logger = Logger(__name__)
```

#### Methods

##### `info(message: str, **kwargs) -> None`

Log info message with structured data.

**Example:**
```python
logger.info("Processing request", user_id="user_123", intent_type="file_search")
```

##### `error(message: str, **kwargs) -> None`

Log error message with structured data.

**Example:**
```python
logger.error("Plugin failed", plugin_name="file-manager", error=str(e))
```

##### `debug(message: str, **kwargs) -> None`

Log debug message (only in debug mode).

**Example:**
```python
logger.debug("Cache hit", cache_key="user_123_context")
```

### `class Metrics`

System metrics collection and reporting.

```python
from astros.core.utils import Metrics

metrics = Metrics()
```

#### Methods

##### `increment(metric: str, tags: Dict[str, str] = None) -> None`

Increment counter metric.

**Example:**
```python
metrics.increment("requests.processed", {"status": "success"})
```

##### `timing(metric: str, duration: float, tags: Dict[str, str] = None) -> None`

Record timing metric.

**Example:**
```python
metrics.timing("request.duration", 0.5, {"handler": "file_search"})
```

##### `gauge(metric: str, value: float, tags: Dict[str, str] = None) -> None`

Set gauge metric value.

**Example:**
```python
metrics.gauge("system.memory_usage", 512.5, {"unit": "MB"})
```

---

<div align="center">

### 🔧 Questions About Core API?

**[💬 Join Discord](https://discord.gg/astros)** • **[📖 Full API Docs](README.md)** • **[🧩 Plugin API](plugins.md)**

*Master the AstrOS core system APIs!*

</div>