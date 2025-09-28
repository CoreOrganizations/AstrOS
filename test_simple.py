#!/usr/bin/env python3
"""
Simple test to debug enhanced AstrOS issues
"""
import asyncio
from src.astros.core.agent import AstrOSAgent

async def simple_test():
    print('🔧 Simple AstrOS Test')
    print('='*40)
    
    agent = AstrOSAgent()
    await agent.initialize()
    
    # Simple test command
    try:
        response = await agent.process_command("hello")
        print(f'Response: {response}')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
    
    await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(simple_test())