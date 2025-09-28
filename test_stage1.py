#!/usr/bin/env python3
"""
Quick test script for AstrOS Stage 1
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from astros.core.agent import AstrOSAgent

async def test_astros():
    print("🚀 Testing AstrOS Stage 1 Implementation")
    print("=" * 50)
    
    # Initialize agent
    agent = AstrOSAgent()
    await agent.initialize()
    
    # Test commands
    test_commands = [
        "hello",
        "status", 
        "help",
        "system info",
        "unknown command"
    ]
    
    for cmd in test_commands:
        print(f"\n> {cmd}")
        response = await agent.process_command(cmd)
        print(f"Response: {response['message']}")
    
    await agent.shutdown()
    print("\n🎉 Stage 1 test completed successfully!")
    print("\n✅ Next Steps:")
    print("  1. Run 'python -m astros.cli interactive' for interactive mode")
    print("  2. Start planning Stage 2: AI Integration")
    print("  3. Begin Ubuntu ISO building process")

if __name__ == "__main__":
    asyncio.run(test_astros())