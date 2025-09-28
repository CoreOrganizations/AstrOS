#!/usr/bin/env python3
"""
Comprehensive AstrOS Testing Script
Tests both local and API modes with debugging information
"""
import asyncio
import os
from src.astros.core.agent import AstrOSAgent

async def test_local_mode():
    """Test local mode functionality"""
    print('🔧 Testing Local Mode (No API)')
    print('='*50)
    
    # Ensure local mode
    os.environ['ASTROS_ENABLE_OPENAI'] = 'false'
    os.environ['ASTROS_ENABLE_LOCAL_NLP'] = 'true'
    
    agent = AstrOSAgent()
    await agent.initialize()
    
    test_commands = [
        'hello',
        'hi there',
        'help me',
        'calculate 2 + 3',
        'what is 5 * 6',
        'status',
        'system info'
    ]
    
    for command in test_commands:
        print(f'\n🔸 Command: {command}')
        try:
            response = await agent.process_command(command)
            print(f'✅ Success: {response["success"]}')
            print(f'📝 Message: {response["message"]}')
            print(f'🎯 Intent: {response.get("intent", "unknown")} (confidence: {response.get("confidence", 0.0):.2f})')
        except Exception as e:
            print(f'❌ Error: {e}')
    
    await agent.shutdown()

async def test_nlp_directly():
    """Test NLP processor directly to debug intent classification"""
    print('\n🧠 Testing NLP Processor Directly')
    print('='*50)
    
    from src.astros.ai.nlp import EnhancedNLPProcessor
    
    nlp = EnhancedNLPProcessor()
    
    test_phrases = [
        'hello',
        'hi there',
        'help me',
        'what can you do',
        'calculate 2 + 3'
    ]
    
    for phrase in test_phrases:
        print(f'\n🔸 Phrase: "{phrase}"')
        try:
            processed = await nlp.process(phrase, use_gpt=False)  # Force local processing
            print(f'🎯 Intent: {processed.intent.name if processed.intent else "None"} (confidence: {processed.intent.confidence if processed.intent else 0.0:.2f})')
            print(f'📊 Entities: {len(processed.entities)} found')
            print(f'⏱️ Processing time: {processed.processing_time:.3f}s')
        except Exception as e:
            print(f'❌ Error: {e}')
            import traceback
            traceback.print_exc()

async def test_with_api_if_configured():
    """Test API mode if API key is configured"""
    print('\n\n🚀 Testing API Mode (if configured)')
    print('='*50)
    
    # Check if API key is set
    api_key = os.getenv('ASTROS_OPENAI_API_KEY')
    if not api_key:
        print('❌ No API key found. Set ASTROS_OPENAI_API_KEY to test API mode.')
        print('Example: export ASTROS_OPENAI_API_KEY="your-key-here"')
        return
    
    # Enable API mode
    os.environ['ASTROS_ENABLE_OPENAI'] = 'true'
    
    agent = AstrOSAgent()
    await agent.initialize()
    
    test_commands = [
        'hello there!',
        'calculate 15 * 23',
        'help me understand what you can do'
    ]
    
    for command in test_commands:
        print(f'\n🔸 Command: {command}')
        try:
            response = await agent.process_command(command)
            print(f'✅ Success: {response["success"]}')
            print(f'📝 Message: {response["message"]}')
            print(f'🎯 Intent: {response.get("intent", "unknown")} (confidence: {response.get("confidence", 0.0):.2f})')
            if response.get("tokens_used"):
                print(f'🪙 Tokens used: {response["tokens_used"]}')
        except Exception as e:
            print(f'❌ Error: {e}')
    
    await agent.shutdown()

async def test_plugin_system():
    """Test plugin system directly"""
    print('\n\n🔌 Testing Plugin System')
    print('='*50)
    
    from src.astros.plugins.base import PluginManager
    
    manager = PluginManager()
    await manager.initialize()
    
    print(f'📦 Loaded plugins: {list(manager.plugins.keys())}')
    
    # Test each plugin
    test_intents = [
        ('greeting', {}),
        ('help', {}),
        ('calculation', {'expression': '2 + 3', 'numbers': ['2', '3'], 'operators': ['add']})
    ]
    
    for intent_name, parameters in test_intents:
        print(f'\n🔸 Testing intent: {intent_name}')
        try:
            result = await manager.execute_intent(intent_name, parameters)
            print(f'✅ Success: {result.success}')
            print(f'📝 Message: {result.message}')
            if result.data:
                print(f'📊 Data: {result.data}')
        except Exception as e:
            print(f'❌ Error: {e}')
    
    await manager.shutdown()

if __name__ == "__main__":
    async def main():
        print('🧪 AstrOS Comprehensive Testing Suite')
        print('='*60)
        
        # Test local mode
        await test_local_mode()
        
        # Test NLP directly
        await test_nlp_directly()
        
        # Test plugin system
        await test_plugin_system()
        
        # Test API mode if configured
        await test_with_api_if_configured()
        
        print('\n' + '='*60)
        print('🎉 Testing complete!')
        
        # Instructions for user
        print('\n📋 Next Steps:')
        print('1. If local mode is working, you can use AstrOS without API keys')
        print('2. To test API features, set: export ASTROS_OPENAI_API_KEY="your-key"')
        print('3. For OpenRouter (cheaper): export ASTROS_OPENAI_BASE_URL="https://openrouter.ai/api/v1"')
        print('4. Run the enhanced demo: python demo_enhanced.py')
    
    asyncio.run(main())