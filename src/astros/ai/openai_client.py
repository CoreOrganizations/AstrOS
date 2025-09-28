"""
OpenAI GPT integration for AstrOS
Provides intelligent conversation and enhanced NLP capabilities
"""
import asyncio
import logging
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

import openai
import tiktoken
from openai import AsyncOpenAI

from ..core.config_enhanced import get_config, ConversationContext

logger = logging.getLogger(__name__)


@dataclass
class GPTResponse:
    """Response from GPT API"""
    content: str
    usage: Dict[str, int]
    model: str
    finish_reason: str
    confidence: float = 0.9


class OpenAIClient:
    """Enhanced OpenAI client for AstrOS"""
    
    def __init__(self):
        self.config = get_config()
        self.client: Optional[AsyncOpenAI] = None
        self.token_encoder = None
        self._setup_client()
    
    def _setup_client(self):
        """Initialize OpenAI client with support for OpenRouter and custom endpoints"""
        try:
            api_key = self.config.get_openai_api_key()
            if not api_key:
                logger.warning("OpenAI API key not configured")
                return
            
            # Support for custom base URLs (e.g., OpenRouter)
            base_url = os.getenv("ASTROS_OPENAI_BASE_URL")
            
            client_kwargs = {
                "api_key": api_key,
                "timeout": self.config.openai.timeout,
                "max_retries": self.config.openai.max_retries
            }
            
            if base_url:
                client_kwargs["base_url"] = base_url
                logger.info(f"Using custom OpenAI endpoint: {base_url}")
            
            self.client = AsyncOpenAI(**client_kwargs)
            
            # Initialize token encoder for the model
            try:
                self.token_encoder = tiktoken.encoding_for_model(self.config.openai.model)
            except:
                # Fallback to cl100k_base encoding
                self.token_encoder = tiktoken.get_encoding("cl100k_base")
            
            logger.info(f"OpenAI client initialized with model: {self.config.openai.model}")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        if not self.token_encoder:
            # Rough estimate: ~4 characters per token
            return len(text) // 4
        return len(self.token_encoder.encode(text))
    
    def is_available(self) -> bool:
        """Check if OpenAI client is available"""
        return self.client is not None and self.config.ai.enable_openai
    
    async def generate_response(
        self, 
        user_input: str, 
        context: Optional[ConversationContext] = None,
        system_prompt: Optional[str] = None
    ) -> GPTResponse:
        """Generate intelligent response using GPT"""
        if not self.is_available():
            raise RuntimeError("OpenAI client not available")
        
        try:
            messages = self._build_messages(user_input, context, system_prompt)
            
            # Check token count
            total_tokens = sum(self.count_tokens(str(msg)) for msg in messages)
            if total_tokens > self.config.ai.context_window:
                messages = self._trim_messages(messages, self.config.ai.context_window // 2)
            
            response = await self.client.chat.completions.create(
                model=self.config.openai.model,
                messages=messages,
                max_tokens=self.config.openai.max_tokens,
                temperature=self.config.openai.temperature,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            choice = response.choices[0]
            usage_dict = response.usage.model_dump() if response.usage else {}
            
            return GPTResponse(
                content=choice.message.content.strip(),
                usage=usage_dict,
                model=response.model,
                finish_reason=choice.finish_reason,
                confidence=0.95 if choice.finish_reason == "stop" else 0.8
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def classify_intent_advanced(
        self, 
        user_input: str, 
        possible_intents: List[str]
    ) -> Tuple[str, float, Dict[str, Any]]:
        """Advanced intent classification using GPT"""
        if not self.is_available():
            raise RuntimeError("OpenAI client not available")
        
        system_prompt = f"""You are an intent classifier for an AI assistant. 
        Analyze the user input and classify it into one of these intents: {', '.join(possible_intents)}.
        
        Also extract any relevant parameters from the input.
        
        Respond with a JSON object containing:
        - "intent": the classified intent
        - "confidence": confidence score (0.0-1.0)
        - "parameters": extracted parameters as key-value pairs
        - "reasoning": brief explanation of the classification
        
        Be precise and confident in your classification."""
        
        try:
            response = await self.generate_response(
                user_input=user_input,
                system_prompt=system_prompt
            )
            
            # Parse JSON response
            result = json.loads(response.content)
            
            return (
                result.get("intent", "unknown"),
                result.get("confidence", 0.5),
                result.get("parameters", {})
            )
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse GPT intent classification response")
            return "unknown", 0.0, {}
        except Exception as e:
            logger.error(f"GPT intent classification error: {e}")
            raise
    
    async def enhance_response(
        self, 
        basic_response: str, 
        user_input: str, 
        intent: str,
        context: Optional[ConversationContext] = None
    ) -> str:
        """Enhance a basic response using GPT"""
        if not self.is_available():
            return basic_response
        
        system_prompt = f"""You are AstrOS, an intelligent AI assistant. 
        The user asked: "{user_input}"
        The intent was classified as: {intent}
        A basic response was generated: "{basic_response}"
        
        Your task is to enhance this response to be more helpful, natural, and conversational.
        Keep the core information but make it more engaging and personalized.
        Be concise but friendly."""
        
        try:
            response = await self.generate_response(
                user_input="Please enhance this response.",
                context=context,
                system_prompt=system_prompt
            )
            return response.content
            
        except Exception as e:
            logger.warning(f"Failed to enhance response with GPT: {e}")
            return basic_response
    
    async def extract_entities_advanced(
        self, 
        text: str, 
        entity_types: List[str]
    ) -> Dict[str, List[str]]:
        """Advanced entity extraction using GPT"""
        if not self.is_available():
            return {}
        
        system_prompt = f"""Extract entities of these types from the text: {', '.join(entity_types)}.
        
        Return a JSON object where keys are entity types and values are lists of extracted entities.
        
        Example:
        {{
            "numbers": ["15", "25"],
            "dates": ["tomorrow"],
            "file_paths": ["/home/user/document.txt"]
        }}
        
        Only include entity types that are found in the text."""
        
        try:
            response = await self.generate_response(
                user_input=text,
                system_prompt=system_prompt
            )
            
            result = json.loads(response.content)
            return result
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse GPT entity extraction response")
            return {}
        except Exception as e:
            logger.warning(f"GPT entity extraction error: {e}")
            return {}
    
    def _build_messages(
        self, 
        user_input: str, 
        context: Optional[ConversationContext],
        system_prompt: Optional[str]
    ) -> List[Dict[str, str]]:
        """Build message list for GPT API"""
        messages = []
        
        # System message
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            default_system = f"""You are {self.config.agent_name}, an intelligent AI assistant integrated into AstrOS.
            
            Your personality is {self.config.agent_personality} and your response style is {self.config.response_style}.
            
            You can help with:
            - File management and organization
            - Mathematical calculations and computations
            - System information and control
            - General questions and conversations
            - Task automation and productivity
            
            Be helpful, accurate, and maintain context across conversations.
            Keep responses concise but informative."""
            
            messages.append({"role": "system", "content": default_system})
        
        # Add conversation history
        if context and context.messages:
            # Limit context to recent messages
            recent_messages = context.messages[-self.config.ai.conversation_memory_size:]
            messages.extend(recent_messages)
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def _trim_messages(
        self, 
        messages: List[Dict[str, str]], 
        target_tokens: int
    ) -> List[Dict[str, str]]:
        """Trim messages to fit within token limit"""
        # Always keep system message and current user message
        if len(messages) <= 2:
            return messages
        
        system_msg = messages[0]
        user_msg = messages[-1]
        history = messages[1:-1]
        
        # Calculate tokens for fixed messages
        fixed_tokens = self.count_tokens(str(system_msg)) + self.count_tokens(str(user_msg))
        available_tokens = target_tokens - fixed_tokens
        
        # Trim history from the beginning
        trimmed_history = []
        current_tokens = 0
        
        for msg in reversed(history):
            msg_tokens = self.count_tokens(str(msg))
            if current_tokens + msg_tokens <= available_tokens:
                trimmed_history.insert(0, msg)
                current_tokens += msg_tokens
            else:
                break
        
        return [system_msg] + trimmed_history + [user_msg]


# Global client instance
_openai_client: Optional[OpenAIClient] = None


def get_openai_client() -> OpenAIClient:
    """Get global OpenAI client instance"""
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAIClient()
    return _openai_client


async def test_openai_connection() -> bool:
    """Test OpenAI API connection"""
    try:
        client = get_openai_client()
        if not client.is_available():
            return False
        
        response = await client.generate_response("Hello, this is a test.")
        return len(response.content) > 0
        
    except Exception as e:
        logger.error(f"OpenAI connection test failed: {e}")
        return False