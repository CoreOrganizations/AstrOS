"""
AstrOS Core Agent - Enhanced with OpenAI GPT Integration
Stages 1 & 2: Enhanced with GPT-powered intelligence and advanced configuration
"""
import asyncio
import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

from .config_enhanced import get_config, ConversationContext


class AstrOSAgent:
    """Enhanced AstrOS AI Agent with OpenAI GPT Integration"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.logger = logging.getLogger("astros.agent")
        self.is_running = False
        self.system = None
        
        # Enhanced configuration
        self.config = get_config()
        
        # AI Components (Stage 2 Enhanced)
        self.nlp_processor = None
        self.plugin_manager = None
        self.response_generator = None
        self.openai_client = None
        
        # Enhanced conversation context
        self.conversation_context = ConversationContext()
        self.fallback_mode = False
        
    async def initialize(self) -> None:
        """Initialize the agent and all components"""
        self.logger.info("Initializing AstrOS Agent...")
        
        # Set up basic configuration
        await self._setup_logging()
        await self._load_configuration()
        await self._initialize_system()
        
        self.is_running = True
        self.logger.info("AstrOS Agent initialized successfully")
    
    async def _setup_logging(self) -> None:
        """Configure logging for the agent"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
    
    async def _load_configuration(self) -> None:
        """Load enhanced agent configuration"""
        # Configuration is now handled by enhanced config system
        self.logger.info(f"Using configuration: OpenAI enabled={self.config.ai.enable_openai}")
        
        # Validate OpenAI configuration if enabled
        if self.config.ai.enable_openai:
            if not self.config.validate_openai_config():
                self.logger.warning("OpenAI configuration invalid, falling back to local mode")
                self.fallback_mode = True
    
    async def _initialize_system(self) -> None:
        """Initialize system integration and AI components"""
        try:
            from astros.system.integration import SystemIntegration
            self.system = SystemIntegration()
            self.logger.info("System integration initialized")
        except Exception as e:
            self.logger.warning(f"System integration not available: {e}")
        
        # Initialize AI components
        await self._initialize_ai_components()
    
    async def _initialize_ai_components(self) -> None:
        """Initialize enhanced AI and NLP components with OpenAI integration"""
        try:
            # Import AI components
            from ..ai.nlp import NLPProcessor, ResponseGenerator
            from ..plugins.base import PluginManager
            
            self.logger.info("Initializing enhanced AI components...")
            
            # Initialize OpenAI client if enabled
            if self.config.ai.enable_openai and not self.fallback_mode:
                try:
                    from ..ai.openai_client import get_openai_client
                    self.openai_client = get_openai_client()
                    self.logger.info("OpenAI client initialized")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize OpenAI client: {e}")
                    self.fallback_mode = True
            
            # Initialize NLP processor with OpenAI integration
            self.nlp_processor = NLPProcessor()
            if hasattr(self.nlp_processor, 'set_openai_client') and self.openai_client:
                self.nlp_processor.set_openai_client(self.openai_client)
            
            # Initialize enhanced response generator
            self.response_generator = ResponseGenerator()
            if hasattr(self.response_generator, 'set_openai_client') and self.openai_client:
                self.response_generator.set_openai_client(self.openai_client)
            
            # Initialize plugin manager
            self.plugin_manager = PluginManager()
            await self.plugin_manager.initialize()
            
            self.logger.info("Enhanced AI components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI components: {e}")
            # Fallback to basic mode
            self.nlp_processor = None
            self.plugin_manager = None
            self.response_generator = None
            self.openai_client = None
            self.fallback_mode = True
    
    async def process_command(self, command: str) -> Dict[str, Any]:
        """Process a user command with AI and natural language understanding"""
        self.logger.info(f"Processing command: {command}")
        
        try:
            # Stage 2: Use AI processing if available
            if self.nlp_processor and self.plugin_manager:
                return await self._process_with_ai(command)
            else:
                # Fallback to basic processing
                return await self._process_basic(command)
                
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            return {
                'success': False,
                'message': f"Error processing command: {e}",
                'timestamp': datetime.now().isoformat(),
                'agent': self.config['agent']['name']
            }
    
    async def _process_with_ai(self, command: str) -> Dict[str, Any]:
        """Process command using enhanced AI and NLP with OpenAI integration"""
        try:
            # Enhanced processing with OpenAI if available
            if self.openai_client and self.config.ai.enable_openai:
                return await self._process_with_openai(command)
            
            # Process with local NLP
            processed_input = await self.nlp_processor.process(command)
            
            # Enhanced conversation context management
            self._update_conversation_context(command, processed_input)
            
            # Handle special commands first
            if processed_input.intent and processed_input.intent.name == "shutdown":
                await self.shutdown()
                return {
                    'success': True,
                    'message': "Shutting down AstrOS Agent...",
                    'timestamp': datetime.now().isoformat(),
                    'agent': self.config.agent_name,  
                    'intent': processed_input.intent.name,
                    'confidence': processed_input.intent.confidence
                }
            
            # Check if we have a valid intent
            if not processed_input.intent:
                return {
                    'success': False,
                    'message': "I'm not sure how to help with that. Could you try rephrasing?",
                    'timestamp': datetime.now().isoformat(),
                    'agent': self.config.agent_name,
                    'intent': 'unknown',
                    'confidence': 0.0
                }
            
            # Execute intent with plugin system
            result = await self.plugin_manager.execute_intent(
                processed_input.intent.name,
                processed_input.intent.parameters
            )
            
            # Generate natural language response
            if self.response_generator:
                message = await self.response_generator.generate_response(
                    processed_input.intent, 
                    result.data if result.success else None,
                    result.error if not result.success else None
                )
            else:
                message = result.message if result.message else "Operation completed"
            
            return {
                'success': result.success,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'agent': self.config.agent_name,
                'intent': processed_input.intent.name if processed_input.intent else 'unknown',
                'confidence': processed_input.intent.confidence if processed_input.intent else 0.0,
                'entities': [{'text': e.text, 'label': e.label} for e in processed_input.entities],
                'data': result.data
            }
            
        except Exception as e:
            self.logger.error(f"AI processing error: {e}")
            return {
                'success': False,
                'message': f"AI processing error: {e}",
                'timestamp': datetime.now().isoformat(),
                'agent': self.config.agent_name
            }
    
    async def _process_with_openai(self, command: str) -> Dict[str, Any]:
        """Process command using OpenAI GPT for enhanced intelligence"""
        try:
            # Use OpenAI for intelligent response generation
            gpt_response = await self.openai_client.generate_response(
                user_input=command,
                context=self.conversation_context
            )
            
            # Try to classify intent using GPT
            possible_intents = ["greeting", "help", "calculation", "file_management", 
                              "system_control", "conversation", "shutdown"]
            
            intent_name, confidence, parameters = await self.openai_client.classify_intent_advanced(
                command, possible_intents
            )
            
            # Update conversation context
            self.conversation_context.messages.append({"role": "user", "content": command})
            self.conversation_context.messages.append({"role": "assistant", "content": gpt_response.content})
            
            # Limit conversation history
            if len(self.conversation_context.messages) > self.config.ai.conversation_memory_size * 2:
                # Keep system message and recent messages
                self.conversation_context.messages = self.conversation_context.messages[-self.config.ai.conversation_memory_size * 2:]
            
            # Execute plugin if needed
            result_data = None
            if intent_name in ["calculation", "file_management", "system_control"] and self.plugin_manager:
                try:
                    result = await self.plugin_manager.execute_intent(intent_name, parameters)
                    if result.success:
                        result_data = result.data
                        # Enhance the GPT response with plugin results
                        enhanced_response = await self.openai_client.enhance_response(
                            gpt_response.content, command, intent_name, self.conversation_context
                        )
                        gpt_response.content = enhanced_response
                except Exception as e:
                    self.logger.warning(f"Plugin execution failed: {e}")
            
            return {
                'success': True,
                'message': gpt_response.content,
                'timestamp': datetime.now().isoformat(),
                'agent': self.config.agent_name,
                'intent': intent_name,
                'confidence': confidence,
                'entities': [],  # GPT handles entity extraction internally
                'data': result_data,
                'model': gpt_response.model,
                'tokens_used': gpt_response.usage.get('total_tokens', 0) if gpt_response.usage else 0
            }
            
        except Exception as e:
            self.logger.error(f"OpenAI processing error: {e}")
            # Fallback to local processing
            if self.config.ai.fallback_to_local and self.nlp_processor:
                self.logger.info("Falling back to local NLP processing")
                return await self._process_with_local_ai(command)
            
            return {
                'success': False,
                'message': f"AI processing error: {e}",
                'timestamp': datetime.now().isoformat(),
                'agent': self.config.agent_name
            }
    
    async def _process_with_local_ai(self, command: str) -> Dict[str, Any]:
        """Process command using local NLP (fallback)"""
        try:
            processed_input = await self.nlp_processor.process(command)
            self._update_conversation_context(command, processed_input)
            
            # Handle special commands
            if processed_input.intent and processed_input.intent.name == "shutdown":
                await self.shutdown()
                return {
                    'success': True,
                    'message': "Shutting down AstrOS Agent...",
                    'timestamp': datetime.now().isoformat(),
                    'agent': self.config.agent_name,
                    'intent': processed_input.intent.name,
                    'confidence': processed_input.intent.confidence
                }
            
            # Check if we have a valid intent
            if not processed_input.intent:
                return {
                    'success': False,
                    'message': "I'm not sure how to help with that. Could you try rephrasing?",
                    'timestamp': datetime.now().isoformat(),
                    'agent': self.config.agent_name,
                    'intent': 'unknown',
                    'confidence': 0.0
                }
            
            # Execute intent with plugin system
            result = await self.plugin_manager.execute_intent(
                processed_input.intent.name,
                processed_input.intent.parameters
            )
            
            # Generate response
            if self.response_generator:
                message = await self.response_generator.generate_response(
                    processed_input.intent,
                    result.data if result.success else None,
                    result.error if not result.success else None
                )
            else:
                message = result.message if result.message else "Operation completed"
            
            return {
                'success': result.success,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'agent': self.config.agent_name,
                'intent': processed_input.intent.name if processed_input.intent else 'unknown',
                'confidence': processed_input.intent.confidence if processed_input.intent else 0.0,
                'entities': [{'text': e.text, 'label': e.label} for e in processed_input.entities],
                'data': result.data
            }
            
        except Exception as e:
            self.logger.error(f"Local AI processing error: {e}")
            return {
                'success': False,
                'message': f"Processing error: {e}",
                'timestamp': datetime.now().isoformat(),
                'agent': self.config.agent_name
            }
    
    def _update_conversation_context(self, command: str, processed_input=None) -> None:
        """Update conversation context with new interaction"""
        # Add to conversation history
        self.conversation_context.messages.append({"role": "user", "content": command})
        
        # Update last intent
        if processed_input and processed_input.intent:
            self.conversation_context.last_intent = processed_input.intent.name
        
        # Limit conversation history
        if len(self.conversation_context.messages) > self.config.ai.conversation_memory_size:
            self.conversation_context.messages = self.conversation_context.messages[-self.config.ai.conversation_memory_size:]
    
    async def _process_basic(self, command: str) -> Dict[str, Any]:
        """Enhanced basic command processing (secure fallback mode)"""
        response = {
            'success': True,
            'message': f"Received command: {command}",
            'timestamp': datetime.now().isoformat(),
            'agent': self.config.agent_name,
            'mode': 'basic_enhanced'
        }
        
        command_lower = command.lower().strip()
        
        if 'hello' in command_lower or 'hi' in command_lower:
            response['message'] = f"Hello! I'm {self.config.agent_name} running in basic mode. Enhanced AI features are not available."
        elif 'status' in command_lower:
            mode = "OpenAI-enabled" if self.config.ai.enable_openai else "Local"
            response['message'] = f"AstrOS Agent is operational ({mode} mode, basic fallback active)."
            response['data'] = {
                'openai_enabled': self.config.ai.enable_openai,
                'fallback_mode': self.fallback_mode,
                'plugins_enabled': self.config.enable_plugins
            }
        elif 'help' in command_lower:
            help_text = f"""
{self.config.agent_name} - Available Commands:
• hello, hi - Greet the assistant
• status - Check system status
• help - Show this help message
• system info - Display system information
• config - Show configuration status
• shutdown, quit - Stop the agent

Enhanced features available when AI components are loaded.
            """.strip()
            response['message'] = help_text
        elif 'config' in command_lower:
            config_info = {
                'openai_enabled': self.config.ai.enable_openai,
                'local_nlp_enabled': self.config.ai.enable_local_nlp,
                'plugins_enabled': self.config.enable_plugins,
                'conversation_memory': self.config.ai.conversation_memory_size,
                'agent_personality': self.config.agent_personality
            }
            response['message'] = "Configuration Status:"
            response['data'] = config_info
        elif 'system' in command_lower and 'info' in command_lower:
            if self.system:
                try:
                    system_info = self.system.get_system_info()
                    response['message'] = "System Information Retrieved"
                    response['data'] = system_info
                except Exception as e:
                    response['message'] = f"Error getting system info: {e}"
                    response['success'] = False
            else:
                response['message'] = "System integration not available"
                response['success'] = False
        elif 'shutdown' in command_lower or 'quit' in command_lower:
            response['message'] = f"Shutting down {self.config.agent_name}..."
            await self.shutdown()
        else:
            response['message'] = f"Command '{command}' processed in basic mode. Try 'help' for available commands."
        
        return response
    
    async def shutdown(self) -> None:
        """Enhanced graceful shutdown with cleanup"""
        self.logger.info(f"Shutting down {self.config.agent_name}...")
        
        # Shutdown enhanced AI components
        if self.plugin_manager:
            try:
                await self.plugin_manager.shutdown()
                self.logger.info("Plugin manager shut down")
            except Exception as e:
                self.logger.error(f"Error shutting down plugin manager: {e}")
        
        # Clear conversation context
        if hasattr(self.conversation_context, 'messages'):
            self.conversation_context.messages.clear()
        
        # Close OpenAI client if needed
        if self.openai_client:
            self.logger.info("OpenAI client connection closed")
        
        self.is_running = False
        self.logger.info("AstrOS Agent shutdown complete")
    
    async def run(self) -> None:
        """Main agent loop"""
        await self.initialize()
        
        self.logger.info("AstrOS Agent is running. Press Ctrl+C to stop.")
        
        try:
            while self.is_running:
                await asyncio.sleep(1)  # Basic event loop
        except KeyboardInterrupt:
            await self.shutdown()
        except Exception as e:
            self.logger.error(f"Agent error: {e}")
            await self.shutdown()


if __name__ == "__main__":
    agent = AstrOSAgent()
    asyncio.run(agent.run())