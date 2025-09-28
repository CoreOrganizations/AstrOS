"""
Enhanced configuration management for AstrOS with OpenAI API integration
"""
import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, SecretStr
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class OpenAIConfig(BaseModel):
    """OpenAI API configuration with OpenRouter support"""
    api_key: Optional[SecretStr] = Field(default=None, description="OpenAI/OpenRouter API key")
    base_url: Optional[str] = Field(default=None, description="Custom API endpoint (e.g., OpenRouter)")
    model: str = Field(default="gpt-4", description="Model to use (e.g., 'openai/gpt-4' for OpenRouter)")
    max_tokens: int = Field(default=1000, description="Maximum tokens per request")
    temperature: float = Field(default=0.7, description="Response creativity (0.0-1.0)")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")


class AIConfig(BaseModel):
    """AI processing configuration"""
    enable_local_nlp: bool = Field(default=True, description="Enable local NLP processing")
    enable_openai: bool = Field(default=False, description="Enable OpenAI integration")
    fallback_to_local: bool = Field(default=True, description="Fallback to local NLP if OpenAI fails")
    conversation_memory_size: int = Field(default=10, description="Number of messages to remember")
    context_window: int = Field(default=2000, description="Context window size for conversations")


class SecurityConfig(BaseModel):
    """Security and privacy configuration"""
    log_api_requests: bool = Field(default=False, description="Log API requests (security risk)")
    encrypt_stored_data: bool = Field(default=True, description="Encrypt stored conversation data")
    max_request_size: int = Field(default=10000, description="Maximum request size in characters")
    rate_limit_per_minute: int = Field(default=60, description="API requests per minute limit")


class EnhancedConfig(BaseModel):
    """Enhanced AstrOS configuration with AI integration"""
    # Core settings
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Agent settings
    agent_name: str = Field(default="AstrOS Assistant", description="Agent display name")
    agent_personality: str = Field(default="helpful", description="Agent personality mode")
    response_style: str = Field(default="conversational", description="Response style")
    
    # AI configurations
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    
    # Plugin settings
    enable_plugins: bool = Field(default=True, description="Enable plugin system")
    plugin_timeout: int = Field(default=10, description="Plugin execution timeout")
    
    @classmethod
    def load_from_file(cls, config_path: Optional[Path] = None) -> "EnhancedConfig":
        """Load configuration from file with environment variable override"""
        if config_path is None:
            config_path = Path.home() / ".astros" / "config.yaml"
        
        config_data = {}
        
        # Load from file if exists
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
                logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config file {config_path}: {e}")
        
        # Override with environment variables
        config_data = cls._apply_env_overrides(config_data)
        
        return cls(**config_data)
    
    @staticmethod
    def _apply_env_overrides(config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides"""
        env_mappings = {
            "ASTROS_OPENAI_API_KEY": ["openai", "api_key"],
            "ASTROS_OPENAI_BASE_URL": ["openai", "base_url"],
            "ASTROS_OPENAI_MODEL": ["openai", "model"],
            "ASTROS_OPENAI_MAX_TOKENS": ["openai", "max_tokens"],
            "ASTROS_OPENAI_TEMPERATURE": ["openai", "temperature"],
            "ASTROS_DEBUG": ["debug"],
            "ASTROS_LOG_LEVEL": ["log_level"],
            "ASTROS_AGENT_NAME": ["agent_name"],
            "ASTROS_ENABLE_OPENAI": ["ai", "enable_openai"],
            "ASTROS_CONVERSATION_MEMORY": ["ai", "conversation_memory_size"],
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Navigate to the nested config location
                current = config_data
                for key in config_path[:-1]:
                    current = current.setdefault(key, {})
                
                # Convert value to appropriate type
                if config_path[-1] in ["debug", "enable_openai", "enable_plugins"]:
                    value = value.lower() in ("true", "1", "yes", "on")
                elif config_path[-1] in ["conversation_memory_size", "max_tokens", "timeout"]:
                    value = int(value)
                elif config_path[-1] in ["temperature"]:
                    value = float(value)
                
                current[config_path[-1]] = value
                logger.info(f"Applied environment override: {env_var}")
        
        return config_data
    
    def save_to_file(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file"""
        if config_path is None:
            config_path = Path.home() / ".astros" / "config.yaml"
        
        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict and handle SecretStr
        config_dict = self.model_dump()
        if config_dict.get("openai", {}).get("api_key"):
            # Don't save the actual API key to file for security
            config_dict["openai"]["api_key"] = "*** SET VIA ENVIRONMENT ***"
        
        try:
            with open(config_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            logger.info(f"Saved configuration to {config_path}")
        except Exception as e:
            logger.error(f"Failed to save config to {config_path}: {e}")
    
    def get_openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from config or environment"""
        if self.openai.api_key:
            return self.openai.api_key.get_secret_value()
        return os.getenv("ASTROS_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    def validate_openai_config(self) -> bool:
        """Validate OpenAI configuration"""
        if not self.ai.enable_openai:
            return True
        
        api_key = self.get_openai_api_key()
        if not api_key:
            logger.error("OpenAI API key not configured. Set ASTROS_OPENAI_API_KEY environment variable.")
            return False
        
        if not api_key.startswith(('sk-', 'sess-')):
            logger.warning("OpenAI API key format may be invalid")
        
        return True


@dataclass
class ConversationContext:
    """Context for maintaining conversation state"""
    messages: list = None
    user_preferences: dict = None
    session_id: str = ""
    last_intent: str = ""
    
    def __post_init__(self):
        if self.messages is None:
            self.messages = []
        if self.user_preferences is None:
            self.user_preferences = {}


# Global configuration instance
_config_instance: Optional[EnhancedConfig] = None


def get_config() -> EnhancedConfig:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = EnhancedConfig.load_from_file()
    return _config_instance


def reload_config() -> EnhancedConfig:
    """Reload configuration from file"""
    global _config_instance
    _config_instance = EnhancedConfig.load_from_file()
    return _config_instance


def set_config(config: EnhancedConfig) -> None:
    """Set global configuration instance"""
    global _config_instance
    _config_instance = config