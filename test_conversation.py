#!/usr/bin/env python3
"""
Custom test script for AstrOS enhanced conversation
"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from astros.core.agent import AstrOSAgent

async def test_enhanced_conversation():
    """Test enhanced conversation capabilities"""
    print("🧪 Testing Enhanced AstrOS Conversation")
    print("=" * 50)
    
    # Initialize agent
    agent = AstrOSAgent()
    await agent.initialize()
    
    # Test cases
    test_queries = [
        "how are you?",
        "what is paris?", 
        "who are you?",
        "why error?",
        "calculate 15 + 25",
        "tell me about AI"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔸 Test {i}: {query}")
        print("-" * 30)
        
        try:
            result = await agent.process_command(query)
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
        except Exception as e:
            print(f"💥 Error: {e}")
    
    # Shutdown
    await agent.shutdown()
    print(f"\n🎉 Testing complete!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_conversation())