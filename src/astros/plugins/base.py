"""
Base Plugin System for AstrOS
Provides the foundation for all AstrOS plugins
"""
import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class PluginStatus(Enum):
    """Plugin status enumeration"""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    RUNNING = "running"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class ExecutionResult:
    """Result of plugin execution"""
    success: bool
    data: Any = None
    message: str = ""
    error: Optional[str] = None
    
    @classmethod
    def success_result(cls, data: Any = None, message: str = ""):
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_result(cls, error: str, data: Any = None):
        return cls(success=False, data=data, error=error)


class BasePlugin(ABC):
    """Base class for all AstrOS plugins"""
    
    # Plugin metadata (override in subclasses)
    name: str = "base_plugin"
    version: str = "1.0.0"
    description: str = "Base plugin class"
    author: str = "AstrOS Team"
    
    # Plugin capabilities
    handled_intents: List[str] = []
    required_permissions: List[str] = []
    
    def __init__(self):
        self.logger = logging.getLogger(f"astros.plugins.{self.name}")
        self.status = PluginStatus.UNLOADED
        self.config = {}
        self.system_api = None
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the plugin. Return True if successful."""
        pass
    
    @abstractmethod
    async def execute(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute plugin functionality based on intent"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup plugin resources"""
        pass
    
    def can_handle_intent(self, intent_name: str) -> bool:
        """Check if plugin can handle the given intent"""
        return intent_name in self.handled_intents
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "status": self.status.value,
            "handled_intents": self.handled_intents,
            "required_permissions": self.required_permissions
        }


class PluginManager:
    """Manages all AstrOS plugins"""
    
    def __init__(self):
        self.logger = logging.getLogger("astros.plugins.manager")
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_handlers: Dict[str, BasePlugin] = {}  # intent -> plugin mapping
        
    async def initialize(self):
        """Initialize the plugin manager and load core plugins"""
        self.logger.info("Initializing plugin manager...")
        
        # Load core plugins
        await self._load_core_plugins()
        
        self.logger.info(f"Plugin manager initialized with {len(self.plugins)} plugins")
    
    async def _load_core_plugins(self):
        """Load the core plugins"""
        core_plugins = [
            CalculatorPlugin(),
            FileManagementPlugin(),
            SystemControlPlugin(),
            ConversationPlugin()
        ]
        
        for plugin in core_plugins:
            await self.load_plugin(plugin)
    
    async def load_plugin(self, plugin: BasePlugin) -> bool:
        """Load a plugin"""
        try:
            self.logger.info(f"Loading plugin: {plugin.name}")
            plugin.status = PluginStatus.LOADING
            
            # Initialize the plugin
            if await plugin.initialize():
                plugin.status = PluginStatus.LOADED
                self.plugins[plugin.name] = plugin
                
                # Register intent handlers
                for intent in plugin.handled_intents:
                    self.plugin_handlers[intent] = plugin
                
                self.logger.info(f"Plugin {plugin.name} loaded successfully")
                return True
            else:
                plugin.status = PluginStatus.ERROR
                self.logger.error(f"Failed to initialize plugin: {plugin.name}")
                return False
                
        except Exception as e:
            plugin.status = PluginStatus.ERROR
            self.logger.error(f"Error loading plugin {plugin.name}: {e}")
            return False
    
    async def execute_intent(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute an intent using the appropriate plugin"""
        try:
            plugin = self.plugin_handlers.get(intent_name)
            
            if not plugin:
                return ExecutionResult.error_result(f"No plugin found for intent: {intent_name}")
            
            if plugin.status != PluginStatus.LOADED:
                return ExecutionResult.error_result(f"Plugin {plugin.name} is not available")
            
            self.logger.info(f"Executing intent '{intent_name}' with plugin '{plugin.name}'")
            
            # Execute the plugin
            result = await plugin.execute(intent_name, parameters)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing intent {intent_name}: {e}")
            return ExecutionResult.error_result(str(e))
    
    def get_plugin_info(self, plugin_name: str = None) -> Dict[str, Any]:
        """Get information about plugins"""
        if plugin_name:
            plugin = self.plugins.get(plugin_name)
            return plugin.get_info() if plugin else {}
        else:
            return {name: plugin.get_info() for name, plugin in self.plugins.items()}
    
    async def shutdown(self):
        """Shutdown all plugins"""
        self.logger.info("Shutting down plugin manager...")
        
        for plugin in self.plugins.values():
            try:
                await plugin.shutdown()
            except Exception as e:
                self.logger.error(f"Error shutting down plugin {plugin.name}: {e}")
        
        self.plugins.clear()
        self.plugin_handlers.clear()


# Core Plugins Implementation

class CalculatorPlugin(BasePlugin):
    """Plugin for mathematical calculations"""
    
    name = "calculator"
    version = "1.0.0"
    description = "Performs mathematical calculations"
    author = "AstrOS Team"
    handled_intents = ["calculation"]
    
    async def initialize(self) -> bool:
        """Initialize calculator plugin"""
        self.logger.info("Calculator plugin initialized")
        return True
    
    async def execute(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute calculation"""
        try:
            expression = parameters.get("expression", "")
            numbers = parameters.get("numbers", [])
            operators = parameters.get("operators", [])
            
            # Simple calculation logic
            if len(numbers) >= 2 and operators:
                num1, num2 = float(numbers[0]), float(numbers[1])
                operator = operators[0]
                
                if operator == "add":
                    result = num1 + num2
                elif operator == "subtract":
                    result = num1 - num2
                elif operator == "multiply":
                    result = num1 * num2
                elif operator == "divide":
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        return ExecutionResult.error_result("Division by zero")
                elif operator == "percentage":
                    result = (num1 / 100) * num2
                else:
                    return ExecutionResult.error_result(f"Unknown operator: {operator}")
                
                return ExecutionResult.success_result(
                    data={"result": result, "expression": f"{num1} {operator} {num2} = {result}"},
                    message=f"The result is {result}"
                )
            
            # Try to evaluate simple expressions safely
            elif expression:
                # Basic safety check - only allow numbers, operators, and parentheses
                import re
                if re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expression):
                    try:
                        result = eval(expression)  # Safe for our limited pattern
                        return ExecutionResult.success_result(
                            data={"result": result, "expression": f"{expression} = {result}"},
                            message=f"The result is {result}"
                        )
                    except:
                        return ExecutionResult.error_result("Invalid mathematical expression")
                else:
                    return ExecutionResult.error_result("Expression contains invalid characters")
            
            return ExecutionResult.error_result("No valid calculation found")
            
        except Exception as e:
            return ExecutionResult.error_result(f"Calculation error: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown calculator plugin"""
        self.logger.info("Calculator plugin shutdown")


class FileManagementPlugin(BasePlugin):
    """Plugin for file system operations"""
    
    name = "file_management"
    version = "1.0.0"
    description = "Manages files and directories"
    author = "AstrOS Team"
    handled_intents = ["file_management"]
    
    async def initialize(self) -> bool:
        """Initialize file management plugin"""
        self.logger.info("File management plugin initialized")
        return True
    
    async def execute(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute file management operation"""
        try:
            actions = parameters.get("actions", [])
            file_paths = parameters.get("file_paths", [])
            original_text = parameters.get("original_text", "")
            
            # For now, return a simple response
            if "list" in actions:
                message = "Here are the files in the current directory (this is a demo response)"
                return ExecutionResult.success_result(
                    data={"action": "list", "files": ["file1.txt", "file2.py", "folder1/"]},
                    message=message
                )
            elif "create" in actions:
                message = "I would create a new file or folder here (demo response)"
                return ExecutionResult.success_result(
                    data={"action": "create", "created": "example_file.txt"},
                    message=message
                )
            else:
                message = f"File management request understood. Actions: {actions}"
                return ExecutionResult.success_result(
                    data={"actions": actions, "file_paths": file_paths},
                    message=message
                )
            
        except Exception as e:
            return ExecutionResult.error_result(f"File management error: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown file management plugin"""
        self.logger.info("File management plugin shutdown")


class SystemControlPlugin(BasePlugin):
    """Plugin for system control operations"""
    
    name = "system_control"
    version = "1.0.0"
    description = "Controls system operations"
    author = "AstrOS Team"
    handled_intents = ["system_control"]
    
    async def initialize(self) -> bool:
        """Initialize system control plugin"""
        self.logger.info("System control plugin initialized")
        return True
    
    async def execute(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute system control operation"""
        try:
            # Import system integration
            from astros.system.integration import SystemIntegration
            
            system = SystemIntegration()
            system_info = system.get_system_info()
            
            return ExecutionResult.success_result(
                data={"system_info": system_info},
                message="Here's your system information"
            )
            
        except Exception as e:
            return ExecutionResult.error_result(f"System control error: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown system control plugin"""
        self.logger.info("System control plugin shutdown")


class ConversationPlugin(BasePlugin):
    """Plugin for conversational interactions"""
    
    name = "conversation"
    version = "1.0.0"
    description = "Handles conversational interactions"
    author = "AstrOS Team"
    handled_intents = ["greeting", "status", "help", "time_date"]
    
    async def initialize(self) -> bool:
        """Initialize conversation plugin"""
        self.logger.info("Conversation plugin initialized")
        return True
    
    async def execute(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute conversation"""
        try:
            if intent_name == "greeting":
                message = "Hello! I'm AstrOS, your intelligent AI assistant. I can help you with calculations, file management, system information, and more!"
            elif intent_name == "status":
                message = "I'm running smoothly! All my plugins are loaded and ready to help you."
            elif intent_name == "help":
                message = "I can help you with:\n• Mathematical calculations (try: 'calculate 25 * 4')\n• File management (try: 'list my files')\n• System information (try: 'show system info')\n• And much more! Just ask me naturally."
            elif intent_name == "time_date":
                from datetime import datetime
                now = datetime.now()
                message = f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                message = "I'm here and ready to help!"
            
            return ExecutionResult.success_result(
                data={"intent": intent_name},
                message=message
            )
            
        except Exception as e:
            return ExecutionResult.error_result(f"Conversation error: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown conversation plugin"""
        self.logger.info("Conversation plugin shutdown")