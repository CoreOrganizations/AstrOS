"""
Tests for AstrOS Agent
"""
import pytest
import asyncio
from src.astros.core.agent import AstrOSAgent


@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initializes correctly"""
    agent = AstrOSAgent()
    await agent.initialize()
    
    assert agent.is_running == True
    assert agent.config is not None
    
    await agent.shutdown()


@pytest.mark.asyncio
async def test_basic_commands():
    """Test basic command processing"""
    agent = AstrOSAgent()
    await agent.initialize()
    
    # Test hello command
    response = await agent.process_command("hello")
    assert response['success'] == True
    assert any(word in response['message'].lower() for word in ['hello', 'greetings', 'hi'])
    
    # Test status command
    response = await agent.process_command("status")
    assert response['success'] == True
    assert any(word in response['message'].lower() for word in ['operational', 'running', 'ready', 'smoothly'])
    
    # Test help command
    response = await agent.process_command("help")
    assert response['success'] == True
    assert any(word in response['message'].lower() for word in ['help', 'commands', 'can', 'try'])
    
    await agent.shutdown()


@pytest.mark.asyncio
async def test_system_commands():
    """Test system integration commands"""
    agent = AstrOSAgent()
    await agent.initialize()
    
    response = await agent.process_command("system info")
    assert response['success'] == True
    
    await agent.shutdown()


@pytest.mark.asyncio
async def test_shutdown_command():
    """Test shutdown command"""
    agent = AstrOSAgent()
    await agent.initialize()
    
    response = await agent.process_command("shutdown")
    assert response['success'] == True
    assert 'shutting down' in response['message'].lower()
    assert agent.is_running == False