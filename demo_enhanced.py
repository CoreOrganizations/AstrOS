#!/usr/bin/env python3
"""
Enhanced AstrOS Demo with OpenAI Integration
Tests both local and GPT-powered processing
"""
import asyncio
import os
from src.astros.core.agent import AstrOSAgent
from src.astros.core.config_enhanced import get_config

async def demo_enhanced_astros():
    print('🚀 Enhanced AstrOS Stages 1 & 2 Demo')
    print('='*60)
    
    # Show configuration status
    config = get_config()
    print(f"🔧 Configuration Status:")
    print(f"   • OpenAI Enabled: {config.ai.enable_openai}")
    print(f"   • Local NLP Enabled: {config.ai.enable_local_nlp}")
    print(f"   • Agent Name: {config.agent_name}")
    print(f"   • Model: {config.openai.model}")
    print(f"   • Conversation Memory: {config.ai.conversation_memory_size}")
    
    # Check for API key
    api_key = config.get_openai_api_key()
    if api_key:
        print(f"   • API Key: {'*' * 20}...{api_key[-4:] if len(api_key) > 4 else 'SET'}")
    else:
        print("   • API Key: NOT SET (will use local processing)")
    
    print('\n' + '='*60)
    
    # Initialize agent
    agent = AstrOSAgent()
    await agent.initialize()
    
    # Test commands
    test_commands = [
        # Basic interactions
        "hello there!",
        "what can you help me with?",
        
        # Mathematical calculations  
        "calculate 127 * 23",
        "what is 156 divided by 12?",
        
        # Complex natural language
        "I need to organize my files in the downloads folder",
        "show me system information about memory and CPU",
        
        # Conversational
        "tell me about the weather capabilities",
        "what time is it right now?",
        
        # Advanced queries
        "help me understand how to use AstrOS effectively",
        "calculate the percentage: 75 out of 200"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f'\n🔸 Test {i}/10: {command}')
        print('-' * 50)
        
        try:
            response = await agent.process_command(command)
            
            print(f'🤖 {response["message"]}')
            
            # Show additional metadata
            metadata = []
            if 'intent' in response:
                metadata.append(f"Intent: {response['intent']} ({response.get('confidence', 0):.2f})")
            if 'tokens_used' in response:
                metadata.append(f"Tokens: {response['tokens_used']}")
            if response.get('used_gpt'):
                metadata.append("Powered by GPT")
            
            if metadata:
                print(f'📊 {" | ".join(metadata)}')
                
            if response.get('data'):
                print(f'📋 Data: {response["data"]}')
                
        except Exception as e:
            print(f'❌ Error: {e}')
        
        # Add a small delay between requests
        await asyncio.sleep(0.5)
    
    print('\n' + '='*60)
    print('✅ Enhanced AstrOS Demo Complete!')
    
    # Shutdown
    await agent.shutdown()

def setup_demo_environment():
    """Setup environment for demo"""
    print("🔧 Setting up demo environment...")
    
    # You can set your OpenAI API key here for testing
    # os.environ['ASTROS_OPENAI_API_KEY'] = 'your-api-key-here'
    
    # Configure demo settings
    os.environ['ASTROS_DEBUG'] = 'true'
    os.environ['ASTROS_AGENT_NAME'] = 'AstrOS Enhanced Demo'
    os.environ['ASTROS_ENABLE_OPENAI'] = 'false'  # Set to 'true' if you have API key
    
    print("Environment configured for demo")

if __name__ == "__main__":
    setup_demo_environment()
    asyncio.run(demo_enhanced_astros())