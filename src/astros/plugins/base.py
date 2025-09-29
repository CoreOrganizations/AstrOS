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

# Plugin imports removed to avoid circular imports


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
            
            # Handle direct text input - look for mathematical expressions
            if not expression and not numbers:
                # Try to extract from the original text
                original_text = parameters.get("original_text", "")
                if original_text:
                    # Look for mathematical expressions in the text
                    import re
                    math_pattern = r'[\d\+\-\*\/\(\)\.\s]+'
                    match = re.search(math_pattern, original_text)
                    if match:
                        expression = match.group().strip()
            
            # Simple calculation logic with multiple numbers
            if len(numbers) >= 2 and operators:
                result = float(numbers[0])
                for i, operator in enumerate(operators):
                    if i + 1 < len(numbers):
                        num = float(numbers[i + 1])
                        if operator == "add":
                            result += num
                        elif operator == "subtract":
                            result -= num
                        elif operator == "multiply":
                            result *= num
                        elif operator == "divide":
                            if num != 0:
                                result /= num
                            else:
                                return ExecutionResult.error_result("Division by zero")
                
                return ExecutionResult.success_result(
                    data={"result": result},
                    message=f"The answer is {result}."
                )
            
            # Try to evaluate mathematical expressions safely
            elif expression:
                # Enhanced safety check - only allow numbers, basic operators, and parentheses
                import re
                if re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expression):
                    try:
                        # Clean the expression
                        clean_expr = expression.strip()
                        result = eval(clean_expr)  # Safe for our limited pattern
                        return ExecutionResult.success_result(
                            data={"result": result, "expression": f"{clean_expr} = {result}"},
                            message=f"The answer is {result}."
                        )
                    except Exception as eval_error:
                        return ExecutionResult.error_result(f"Invalid mathematical expression: {eval_error}")
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
    """Enhanced plugin for conversational interactions with knowledge base"""
    
    name = "conversation"
    version = "2.0.0"
    description = "Handles conversational interactions with intelligence"
    author = "AstrOS Team"
    handled_intents = ["greeting", "status", "help", "time_date", "general", "question", "unknown"]
    
    def __init__(self):
        super().__init__()
        self.conversation_history = []
        self.knowledge_base = {
            # Geography and Places
            "paris": "Paris is the capital and largest city of France, known for the Eiffel Tower, Louvre Museum, Notre-Dame Cathedral, and its rich culture, art, and cuisine. It's often called the 'City of Light'.",
            "london": "London is the capital of England and the United Kingdom, famous for Big Ben, the Tower of London, Buckingham Palace, and being a global financial center.",
            "tokyo": "Tokyo is the capital of Japan, known for its blend of traditional and modern culture, advanced technology, delicious cuisine, and being one of the world's largest metropolitan areas.",
            "new york": "New York City is the largest city in the United States, famous for Times Square, Central Park, the Statue of Liberty, Wall Street, and being a global hub for finance, arts, and culture.",
            
            # Science and Technology
            "ai": "Artificial Intelligence (AI) is technology that enables machines to simulate human intelligence, including learning, reasoning, and problem-solving. It's used in many applications from virtual assistants to autonomous vehicles.",
            "machine learning": "Machine Learning is a subset of AI where computers learn patterns from data to make predictions or decisions without being explicitly programmed for each specific task.",
            "python": "Python is a popular programming language known for its simplicity and readability. It's widely used for web development, data science, AI/ML, automation, and many other applications.",
            "computer": "A computer is an electronic device that processes data, performs calculations, and executes instructions through hardware and software to help users accomplish various tasks.",
            
            # General Knowledge
            "sun": "The Sun is the star at the center of our solar system. It provides light and heat energy that sustains life on Earth and is about 4.6 billion years old.",
            "earth": "Earth is the third planet from the Sun and the only known planet with life. It has diverse ecosystems, water oceans, and an atmosphere that supports billions of species.",
            "water": "Water is essential for all known forms of life. It covers about 71% of Earth's surface and is composed of hydrogen and oxygen (H2O).",
            "music": "Music is an art form that combines sounds, rhythms, and melodies to create expressions of emotion, culture, and creativity. It's enjoyed worldwide in countless styles and genres.",
        }
    
    async def initialize(self) -> bool:
        """Initialize enhanced conversation plugin"""
        self.logger.info("Enhanced conversation plugin initialized with knowledge base")
        return True
    
    def _get_knowledge_response(self, query: str) -> str:
        """Get response from knowledge base"""
        query_lower = query.lower().strip()
        
        # Direct matches
        for key, value in self.knowledge_base.items():
            if key in query_lower:
                return value
        
        # Pattern matching for common questions
        if "what is" in query_lower or "tell me about" in query_lower:
            for key in self.knowledge_base.keys():
                if key in query_lower:
                    return self.knowledge_base[key]
        
        if "how are you" in query_lower:
            return "I'm doing great! I'm an AI assistant running smoothly and ready to help you with any questions or tasks. How can I assist you today?"
        
        if "who are you" in query_lower:
            return "I'm AstrOS, your intelligent AI assistant! I can help you with calculations, answer questions, provide information, manage files, and much more. I'm powered by advanced AI technology and always ready to assist."
        
        if "what can you do" in query_lower:
            return "I can help you with many things! I can:\n• Answer questions on various topics\n• Perform mathematical calculations\n• Provide information about places, science, technology\n• Help with file management\n• Give system information\n• Have natural conversations\n• And much more! Just ask me anything!"
        
        if "why error" in query_lower or "error" in query_lower:
            return "I encountered a temporary issue with my cloud AI connection, but I'm still working! My local intelligence is active and ready to help. You can ask me questions about various topics, request calculations, or chat naturally."
        
        if "thank" in query_lower:
            return "You're very welcome! I'm happy to help. Feel free to ask me anything else!"
        
        if "bye" in query_lower or "goodbye" in query_lower:
            return "Goodbye! It was great chatting with you. Come back anytime if you need assistance!"
        
        # Default intelligent response
        return "That's an interesting question! While I may not have specific information about that topic in my immediate knowledge base, I'm here to help however I can. Could you provide more details or ask about something else I might know?"
    
    async def execute(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute enhanced conversation with context"""
        try:
            # Get the original query from parameters
            query = parameters.get('query', parameters.get('text', ''))
            
            # Add to conversation history
            if query:
                self.conversation_history.append(f"User: {query}")
            
            if intent_name == "greeting":
                message = "Hello! I'm AstrOS, your intelligent AI assistant. I'm here to help you with questions, calculations, information, and much more. What would you like to know?"
            elif intent_name == "status":
                message = "I'm running perfectly! All my systems are operational and I'm ready to assist you with any questions or tasks."
            elif intent_name == "help":
                message = "I'm here to help! I can:\n\n🧠 Answer questions about places, science, technology, and general topics\n🔢 Perform mathematical calculations\n📁 Help with file management\n💻 Provide system information\n💬 Have natural conversations\n\nJust ask me anything naturally, like 'What is Paris?' or 'Calculate 15 * 8'!"
            elif intent_name == "time_date":
                from datetime import datetime
                now = datetime.now()
                message = f"Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"
            elif intent_name in ["general", "question", "unknown"] or query:
                # Use enhanced knowledge base
                message = self._get_knowledge_response(query)
            else:
                message = "I'm here and ready to help! Ask me anything you'd like to know."
            
            # Add response to history
            self.conversation_history.append(f"AstrOS: {message}")
            
            # Keep history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return ExecutionResult.success_result(
                data={"intent": intent_name, "query": query, "history_length": len(self.conversation_history)},
                message=message
            )
            
        except Exception as e:
            return ExecutionResult.error_result(f"Conversation error: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown conversation plugin"""
        self.logger.info("Conversation plugin shutdown")