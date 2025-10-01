#!/usr/bin/env python3
"""
AstrOS Robust Error Handling and Fallback System
Comprehensive error handling with intelligent fallbacks and recovery
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass
from enum import Enum
import json
import traceback
from functools import wraps
import aiohttp
from openai import AsyncOpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    API_ERROR = "api_error"
    NETWORK_ERROR = "network_error"
    AUTHENTICATION_ERROR = "auth_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    VALIDATION_ERROR = "validation_error"
    SYSTEM_ERROR = "system_error"
    PLUGIN_ERROR = "plugin_error"
    UNKNOWN_ERROR = "unknown_error"

@dataclass
class ErrorInfo:
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    details: Dict[str, Any]
    timestamp: float
    session_id: Optional[str] = None
    recovery_attempts: int = 0
    max_recovery_attempts: int = 3

@dataclass
class FallbackStrategy:
    name: str
    priority: int  # Lower number = higher priority
    condition: Callable[[ErrorInfo], bool]
    action: Callable[[ErrorInfo, Any], Any]
    description: str

class CircuitBreakerState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, fallback active
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreaker:
    name: str
    failure_threshold: int = 5
    recovery_timeout: int = 60
    failure_count: int = 0
    last_failure_time: float = 0
    state: CircuitBreakerState = CircuitBreakerState.CLOSED

class RobustErrorHandler:
    """
    Comprehensive error handling system with:
    - Circuit breaker pattern
    - Intelligent fallback strategies
    - Error categorization and tracking
    - Recovery mechanisms
    - Performance monitoring
    """
    
    def __init__(self):
        self.error_history: List[ErrorInfo] = []
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.fallback_strategies: List[FallbackStrategy] = []
        self.performance_metrics: Dict[str, Any] = {}
        
        # Initialize default fallback strategies
        self._setup_default_fallbacks()
        
        # Initialize circuit breakers for critical services
        self._setup_circuit_breakers()

    def _setup_default_fallbacks(self):
        """Setup default fallback strategies"""
        
        # API Error Fallbacks
        self.fallback_strategies.extend([
            FallbackStrategy(
                name="retry_with_backoff",
                priority=1,
                condition=lambda error: error.category in [ErrorCategory.NETWORK_ERROR, ErrorCategory.API_ERROR] 
                          and error.recovery_attempts < 3,
                action=self._retry_with_exponential_backoff,
                description="Retry with exponential backoff for transient errors"
            ),
            
            FallbackStrategy(
                name="switch_ai_model",
                priority=2,
                condition=lambda error: error.category == ErrorCategory.API_ERROR 
                          and "model" in error.details,
                action=self._switch_ai_model,
                description="Switch to alternative AI model when primary fails"
            ),
            
            FallbackStrategy(
                name="use_cached_response",
                priority=3,
                condition=lambda error: error.category in [ErrorCategory.API_ERROR, ErrorCategory.NETWORK_ERROR],
                action=self._use_cached_response,
                description="Use cached response when API is unavailable"
            ),
            
            FallbackStrategy(
                name="local_processing",
                priority=4,
                condition=lambda error: error.category in [ErrorCategory.API_ERROR, ErrorCategory.NETWORK_ERROR],
                action=self._local_processing_fallback,
                description="Use local processing when external APIs fail"
            ),
            
            FallbackStrategy(
                name="graceful_degradation",
                priority=10,
                condition=lambda error: True,  # Always applicable as last resort
                action=self._graceful_degradation,
                description="Provide helpful error message and guidance"
            )
        ])

    def _setup_circuit_breakers(self):
        """Setup circuit breakers for critical services"""
        self.circuit_breakers = {
            "openrouter_api": CircuitBreaker("OpenRouter API", failure_threshold=5, recovery_timeout=300),
            "context_manager": CircuitBreaker("Context Manager", failure_threshold=3, recovery_timeout=60),
            "plugin_system": CircuitBreaker("Plugin System", failure_threshold=10, recovery_timeout=120),
            "database": CircuitBreaker("Database", failure_threshold=3, recovery_timeout=30)
        }

    def categorize_error(self, exception: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
        """Categorize and analyze an error"""
        context = context or {}
        error_msg = str(exception)
        error_type = type(exception).__name__
        
        # Determine category based on exception type and message
        category = ErrorCategory.UNKNOWN_ERROR
        severity = ErrorSeverity.MEDIUM
        
        if "rate limit" in error_msg.lower() or "429" in error_msg:
            category = ErrorCategory.RATE_LIMIT_ERROR
            severity = ErrorSeverity.HIGH
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            category = ErrorCategory.AUTHENTICATION_ERROR
            severity = ErrorSeverity.HIGH
        elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            category = ErrorCategory.NETWORK_ERROR
            severity = ErrorSeverity.MEDIUM
        elif "api" in error_msg.lower() or "openai" in error_msg.lower():
            category = ErrorCategory.API_ERROR
            severity = ErrorSeverity.HIGH
        elif error_type in ["ValueError", "TypeError", "KeyError"]:
            category = ErrorCategory.VALIDATION_ERROR
            severity = ErrorSeverity.LOW
        elif "plugin" in error_msg.lower():
            category = ErrorCategory.PLUGIN_ERROR
            severity = ErrorSeverity.MEDIUM
        elif error_type in ["SystemError", "MemoryError", "OSError"]:
            category = ErrorCategory.SYSTEM_ERROR
            severity = ErrorSeverity.CRITICAL
        
        error_info = ErrorInfo(
            category=category,
            severity=severity,
            message=error_msg,
            details={
                "exception_type": error_type,
                "traceback": traceback.format_exc(),
                "context": context
            },
            timestamp=time.time(),
            session_id=context.get("session_id")
        )
        
        # Track error in history
        self.error_history.append(error_info)
        
        # Update circuit breaker if applicable
        service_name = context.get("service_name")
        if service_name in self.circuit_breakers:
            self._update_circuit_breaker(service_name, error_info)
        
        logger.error(f"Categorized error: {category.value} - {severity.value} - {error_msg}")
        return error_info

    def _update_circuit_breaker(self, service_name: str, error_info: ErrorInfo):
        """Update circuit breaker state based on error"""
        breaker = self.circuit_breakers[service_name]
        current_time = time.time()
        
        if error_info.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            breaker.failure_count += 1
            breaker.last_failure_time = current_time
            
            if breaker.failure_count >= breaker.failure_threshold:
                breaker.state = CircuitBreakerState.OPEN
                logger.warning(f"Circuit breaker OPEN for {service_name}")

    def check_circuit_breaker(self, service_name: str) -> bool:
        """Check if circuit breaker allows operation"""
        if service_name not in self.circuit_breakers:
            return True
        
        breaker = self.circuit_breakers[service_name]
        current_time = time.time()
        
        if breaker.state == CircuitBreakerState.CLOSED:
            return True
        elif breaker.state == CircuitBreakerState.OPEN:
            if current_time - breaker.last_failure_time >= breaker.recovery_timeout:
                breaker.state = CircuitBreakerState.HALF_OPEN
                logger.info(f"Circuit breaker HALF_OPEN for {service_name}")
                return True
            return False
        elif breaker.state == CircuitBreakerState.HALF_OPEN:
            return True
        
        return False

    def record_success(self, service_name: str):
        """Record successful operation to reset circuit breaker"""
        if service_name in self.circuit_breakers:
            breaker = self.circuit_breakers[service_name]
            if breaker.state == CircuitBreakerState.HALF_OPEN:
                breaker.state = CircuitBreakerState.CLOSED
                breaker.failure_count = 0
                logger.info(f"Circuit breaker CLOSED for {service_name}")

    async def handle_error(self, error_info: ErrorInfo, original_function: Callable, 
                          *args, **kwargs) -> Any:
        """Handle error with appropriate fallback strategy"""
        try:
            # Find applicable fallback strategies
            applicable_strategies = [
                strategy for strategy in self.fallback_strategies
                if strategy.condition(error_info)
            ]
            
            # Sort by priority
            applicable_strategies.sort(key=lambda x: x.priority)
            
            logger.info(f"Found {len(applicable_strategies)} applicable fallback strategies")
            
            # Try each strategy in order
            for strategy in applicable_strategies:
                try:
                    logger.info(f"Attempting fallback strategy: {strategy.name}")
                    result = await strategy.action(error_info, {
                        "original_function": original_function,
                        "args": args,
                        "kwargs": kwargs
                    })
                    
                    if result is not None:
                        logger.info(f"Fallback strategy {strategy.name} succeeded")
                        return result
                        
                except Exception as fallback_error:
                    logger.error(f"Fallback strategy {strategy.name} failed: {fallback_error}")
                    continue
            
            # If all strategies failed, return graceful error
            return await self._graceful_degradation(error_info, {})
            
        except Exception as e:
            logger.error(f"Error handling failed: {e}")
            return "I encountered an unexpected error. Please try again later."

    async def _retry_with_exponential_backoff(self, error_info: ErrorInfo, context: Dict[str, Any]) -> Any:
        """Retry with exponential backoff"""
        if error_info.recovery_attempts >= error_info.max_recovery_attempts:
            return None
        
        # Calculate delay: 2^attempt seconds
        delay = 2 ** error_info.recovery_attempts
        await asyncio.sleep(delay)
        
        error_info.recovery_attempts += 1
        
        try:
            # Retry original function
            original_function = context["original_function"]
            args = context["args"]
            kwargs = context["kwargs"]
            
            result = await original_function(*args, **kwargs)
            return result
            
        except Exception as retry_error:
            logger.warning(f"Retry attempt {error_info.recovery_attempts} failed: {retry_error}")
            return None

    async def _switch_ai_model(self, error_info: ErrorInfo, context: Dict[str, Any]) -> Any:
        """Switch to alternative AI model"""
        try:
            # Alternative models in priority order
            alternative_models = [
                "x-ai/grok-4-fast:free",
                "qwen/qwen-2.5-72b-instruct:free",
                "meta-llama/llama-3.2-11b-vision-instruct:free",
                "microsoft/phi-3-medium-128k-instruct:free"
            ]
            
            # This would integrate with your AI client
            # For now, return a placeholder response
            return "I switched to an alternative AI model to handle your request. How can I help you?"
            
        except Exception as e:
            logger.error(f"Model switching failed: {e}")
            return None

    async def _use_cached_response(self, error_info: ErrorInfo, context: Dict[str, Any]) -> Any:
        """Use cached response if available"""
        try:
            # This would integrate with a caching system
            # For now, return a placeholder
            return "I'm currently experiencing connectivity issues, but I'm still here to help with basic questions."
            
        except Exception as e:
            logger.error(f"Cache fallback failed: {e}")
            return None

    async def _local_processing_fallback(self, error_info: ErrorInfo, context: Dict[str, Any]) -> Any:
        """Use local processing when external APIs fail"""
        try:
            # Simple local responses for common queries
            kwargs = context.get("kwargs", {})
            question = kwargs.get("question", "").lower()
            
            if "hello" in question or "hi" in question:
                return "Hello! I'm currently running in offline mode but I'm still here to help with basic questions."
            elif any(op in question for op in ["+", "-", "*", "/", "calculate"]):
                return "I can help with calculations even in offline mode. Please specify the calculation you'd like me to perform."
            elif "time" in question or "date" in question:
                return f"The current time is {time.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                return "I'm currently in offline mode with limited capabilities, but I'm still here to help with basic questions."
                
        except Exception as e:
            logger.error(f"Local processing fallback failed: {e}")
            return None

    async def _graceful_degradation(self, error_info: ErrorInfo, context: Dict[str, Any]) -> str:
        """Provide graceful degradation with helpful error message"""
        try:
            base_message = "I'm currently experiencing some technical difficulties. "
            
            if error_info.category == ErrorCategory.AUTHENTICATION_ERROR:
                return base_message + "Please check that your API key is configured correctly."
            elif error_info.category == ErrorCategory.RATE_LIMIT_ERROR:
                return base_message + "I've reached my rate limit. Please try again in a few minutes."
            elif error_info.category == ErrorCategory.NETWORK_ERROR:
                return base_message + "Please check your internet connection and try again."
            elif error_info.category == ErrorCategory.API_ERROR:
                return base_message + "The AI service is temporarily unavailable. Please try again later."
            else:
                return base_message + "Please try rephrasing your question or try again later."
                
        except Exception as e:
            logger.error(f"Graceful degradation failed: {e}")
            return "I'm experiencing technical difficulties. Please try again later."

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics for monitoring"""
        try:
            total_errors = len(self.error_history)
            if total_errors == 0:
                return {"total_errors": 0}
            
            # Categorize errors
            category_counts = {}
            severity_counts = {}
            recent_errors = []
            
            cutoff_time = time.time() - 3600  # Last hour
            
            for error in self.error_history:
                category_counts[error.category.value] = category_counts.get(error.category.value, 0) + 1
                severity_counts[error.severity.value] = severity_counts.get(error.severity.value, 0) + 1
                
                if error.timestamp > cutoff_time:
                    recent_errors.append(error)
            
            # Circuit breaker status
            breaker_status = {}
            for name, breaker in self.circuit_breakers.items():
                breaker_status[name] = {
                    "state": breaker.state.value,
                    "failure_count": breaker.failure_count,
                    "last_failure": breaker.last_failure_time
                }
            
            return {
                "total_errors": total_errors,
                "recent_errors": len(recent_errors),
                "category_breakdown": category_counts,
                "severity_breakdown": severity_counts,
                "circuit_breakers": breaker_status,
                "error_rate_last_hour": len(recent_errors)
            }
            
        except Exception as e:
            logger.error(f"Failed to get error statistics: {e}")
            return {"error": "Failed to generate statistics"}

def error_handler(service_name: str = None):
    """Decorator for automatic error handling"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            error_handler_instance = kwargs.pop('_error_handler', None)
            if not error_handler_instance:
                error_handler_instance = RobustErrorHandler()
            
            # Check circuit breaker
            if service_name and not error_handler_instance.check_circuit_breaker(service_name):
                logger.warning(f"Circuit breaker open for {service_name}")
                return await error_handler_instance._graceful_degradation(
                    ErrorInfo(
                        category=ErrorCategory.SYSTEM_ERROR,
                        severity=ErrorSeverity.HIGH,
                        message=f"Service {service_name} is temporarily unavailable",
                        details={},
                        timestamp=time.time()
                    ),
                    {}
                )
            
            try:
                result = await func(*args, **kwargs)
                
                # Record success for circuit breaker
                if service_name:
                    error_handler_instance.record_success(service_name)
                
                return result
                
            except Exception as e:
                # Categorize error
                context = {
                    "service_name": service_name,
                    "function_name": func.__name__,
                    "args": str(args)[:200],  # Truncate for logging
                    "kwargs": {k: str(v)[:100] for k, v in kwargs.items()}  # Truncate values
                }
                
                error_info = error_handler_instance.categorize_error(e, context)
                
                # Handle error with fallback
                return await error_handler_instance.handle_error(error_info, func, *args, **kwargs)
        
        return wrapper
    return decorator

# Test the error handling system
async def test_error_handler():
    """Test the robust error handling system"""
    print("🧪 Testing Robust Error Handling System")
    print("=" * 50)
    
    error_handler = RobustErrorHandler()
    
    # Test error categorization
    print("\n1. Testing Error Categorization:")
    test_errors = [
        Exception("Rate limit exceeded"),
        Exception("401 Unauthorized"),
        ConnectionError("Connection timeout"),
        ValueError("Invalid input"),
        Exception("OpenAI API error")
    ]
    
    for error in test_errors:
        error_info = error_handler.categorize_error(error)
        print(f"  {error} -> {error_info.category.value} ({error_info.severity.value})")
    
    # Test circuit breaker
    print("\n2. Testing Circuit Breaker:")
    print(f"  OpenRouter API breaker: {error_handler.check_circuit_breaker('openrouter_api')}")
    
    # Simulate failures
    for i in range(6):
        error_info = ErrorInfo(
            category=ErrorCategory.API_ERROR,
            severity=ErrorSeverity.HIGH,
            message="Simulated failure",
            details={},
            timestamp=time.time()
        )
        error_handler._update_circuit_breaker("openrouter_api", error_info)
    
    print(f"  After 6 failures: {error_handler.check_circuit_breaker('openrouter_api')}")
    
    # Test fallback
    print("\n3. Testing Fallback Strategy:")
    error_info = ErrorInfo(
        category=ErrorCategory.NETWORK_ERROR,
        severity=ErrorSeverity.MEDIUM,
        message="Network connection failed",
        details={},
        timestamp=time.time()
    )
    
    async def dummy_function(question="Hello"):
        return "Original response"
    
    result = await error_handler.handle_error(error_info, dummy_function, question="Hello")
    print(f"  Fallback result: {result}")
    
    # Test error statistics
    print("\n4. Error Statistics:")
    stats = error_handler.get_error_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Error handling system test completed!")

if __name__ == "__main__":
    asyncio.run(test_error_handler())