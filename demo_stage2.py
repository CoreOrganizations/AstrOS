#!/usr/bin/env python3
"""
AstrOS Stage 2 AI Integration Demo
"""
import asyncio
from src.astros.core.agent import AstrOSAgent

async def demo():
    print('🚀 AstrOS Stage 2 AI Integration Demo')
    print('='*50)
    
    agent = AstrOSAgent()
    await agent.initialize()
    
    test_commands = [
        'hello',
        'calculate 25 * 4',
        'what is 100 divided by 4',
        'help me',
        'show system information'
    ]
    
    for cmd in test_commands:
        print(f'\n🔸 User: {cmd}')
        response = await agent.process_command(cmd)
        print(f'🤖 AstrOS: {response["message"]}')
        if response.get('data'):
            print(f'📊 Data: {response["data"]}')
    
    print('\n' + '='*50)
    print('✅ Stage 2 AI Integration Complete!')

if __name__ == "__main__":
    asyncio.run(demo())