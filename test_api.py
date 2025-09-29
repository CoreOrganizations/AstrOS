#!/usr/bin/env python3
"""
AstrOS API Test - Demonstrates API-only functionality
Run this with a valid OPENROUTER_API_KEY to test real AI responses
"""

import asyncio
import os
import sys

# Add current directory to path
sys.path.insert(0, '.')

from astros import EnhancedAstrOSAgent

async def test_api_responses():
    """Test the API-only functionality"""
    print("🧪 AstrOS API Test - OpenAI OSS 20B Only")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set!")
        print("📝 To test with real AI:")
        print("   1. Get free API key: https://openrouter.ai/keys")
        print("   2. Set: OPENROUTER_API_KEY=your-key-here")
        print("   3. Run this test again")
        return
    
    print(f"✅ API Key found: {api_key[:20]}...")
    print("🤖 Testing OpenAI OSS 20B responses...")
    
    # Initialize agent
    agent = EnhancedAstrOSAgent()
    
    # Test questions
    test_questions = [
        "What is 2+2?",
        "What is Paris?",
        "Who are you?",
        "Explain quantum physics in simple terms"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔸 Test {i}: {question}")
        print("-" * 40)
        
        try:
            response = await agent.get_response(question)
            print(f"✅ Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        if i < len(test_questions):
            await asyncio.sleep(1)  # Rate limiting
    
    print(f"\n🎉 API Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_api_responses())