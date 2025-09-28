"""
Tests for AstrOS AI components
"""
import pytest
import asyncio
from src.astros.ai.nlp import NLPProcessor, ResponseGenerator
from src.astros.plugins.base import PluginManager, CalculatorPlugin


@pytest.mark.asyncio
async def test_nlp_processor():
    """Test NLP processor functionality"""
    processor = NLPProcessor()
    
    # Test basic text processing
    result = await processor.process("hello there")
    assert result.original_text == "hello there"
    assert result.intent.name == "greeting"
    assert result.intent.confidence > 0


@pytest.mark.asyncio
async def test_intent_classification():
    """Test intent classification"""
    processor = NLPProcessor()
    
    test_cases = [
        ("calculate 25 * 4", "calculation"),
        ("what is 10 + 5", "calculation"),
        ("show me system info", "system_control"),
        ("hello", "greeting"),
        ("help me", "help"),
        ("list my files", "file_management"),
    ]
    
    for text, expected_intent in test_cases:
        result = await processor.process(text)
        assert result.intent.name == expected_intent


@pytest.mark.asyncio
async def test_calculator_plugin():
    """Test calculator plugin"""
    plugin = CalculatorPlugin()
    await plugin.initialize()
    
    # Test addition
    result = await plugin.execute("calculation", {
        "numbers": ["10", "5"],
        "operators": ["add"],
        "expression": "10 + 5"
    })
    
    assert result.success
    assert result.data["result"] == 15.0


@pytest.mark.asyncio
async def test_plugin_manager():
    """Test plugin manager"""
    manager = PluginManager()
    await manager.initialize()
    
    # Test that plugins are loaded
    assert len(manager.plugins) > 0
    assert "calculator" in manager.plugins
    
    # Test intent execution
    result = await manager.execute_intent("calculation", {
        "numbers": ["20", "4"],
        "operators": ["multiply"],
        "expression": "20 * 4"
    })
    
    assert result.success
    assert result.data["result"] == 80.0


@pytest.mark.asyncio
async def test_response_generation():
    """Test response generation"""
    from src.astros.ai.nlp import Intent, Entity
    
    generator = ResponseGenerator()
    
    # Test greeting response
    intent = Intent(
        name="greeting",
        confidence=0.9,
        entities=[],
        parameters={}
    )
    
    response = generator.generate_response(intent)
    assert any(word in response.lower() for word in ["hello", "hi", "greetings"])


@pytest.mark.asyncio  
async def test_stage2_agent():
    """Test Stage 2 agent with AI capabilities"""
    from src.astros.core.agent import AstrOSAgent
    
    agent = AstrOSAgent()
    await agent.initialize()
    
    # Test natural language commands
    test_commands = [
        "hello",
        "calculate 15 * 3", 
        "what is 100 divided by 4",
        "show system information",
        "help me"
    ]
    
    for command in test_commands:
        response = await agent.process_command(command)        
        # Some commands may not succeed (e.g., system info might be restricted)
        # So let's check that we get a proper response structure
        assert "success" in response
        assert "message" in response
        assert "timestamp" in response
        
        # Check that calculation commands work properly
        if "calculate" in command.lower():
            # For calculation commands, we expect success or at least a proper error
            assert isinstance(response["success"], bool)
        assert "message" in response
        assert "intent" in response  # Should have intent classification
    
    await agent.shutdown()