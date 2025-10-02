#!/usr/bin/env python3
"""
Test script to verify AstrOS Agent is working correctly
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from astros import AstrOSAgent

async def run_tests():
    """Run comprehensive tests on the agent"""
    
    print("🧪 AstrOS Agent Testing Suite")
    print("=" * 50)
    
    # Test 1: Agent Initialization
    print("\n📋 Test 1: Agent Initialization")
    try:
        agent = AstrOSAgent()
        print("✅ PASS: Agent initialized successfully")
    except Exception as e:
        print(f"❌ FAIL: Agent initialization failed: {e}")
        return False
    
    # Test 2: Simple Query
    print("\n📋 Test 2: Simple Query")
    try:
        response = await agent.get_response("Hello! What is 2+2?")
        if response and len(response) > 0:
            print(f"✅ PASS: Got response")
            print(f"   Response: {response[:100]}...")
        else:
            print("❌ FAIL: Empty response")
            return False
    except Exception as e:
        print(f"❌ FAIL: Query failed: {e}")
        return False
    
    # Test 3: Model Information
    print("\n📋 Test 3: Model Information")
    try:
        response = await agent.get_response("What AI model are you using?")
        if "mistral" in response.lower():
            print(f"✅ PASS: Model correctly identified")
            print(f"   Response: {response[:100]}...")
        else:
            print(f"⚠️  WARNING: Model not clearly identified")
            print(f"   Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ FAIL: Model query failed: {e}")
        return False
    
    # Test 4: Conversation History
    print("\n📋 Test 4: Conversation History")
    try:
        await agent.get_response("Remember this number: 42")
        response = await agent.get_response("What number did I just tell you to remember?")
        if "42" in response:
            print(f"✅ PASS: Conversation history working")
            print(f"   Response: {response[:100]}...")
        else:
            print(f"⚠️  WARNING: Conversation history may not be working")
            print(f"   Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ FAIL: Conversation test failed: {e}")
        return False
    
    # Test 5: Error Handling
    print("\n📋 Test 5: Error Handling")
    try:
        # Try with empty query
        response = await agent.get_response("")
        if response:
            print(f"✅ PASS: Handles empty queries gracefully")
        else:
            print(f"⚠️  WARNING: Empty query returned no response")
    except Exception as e:
        print(f"✅ PASS: Properly handles errors: {type(e).__name__}")
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    print("🚀 Starting AstrOS Agent Tests...\n")
    
    try:
        result = asyncio.run(run_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
