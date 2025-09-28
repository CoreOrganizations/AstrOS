#!/usr/bin/env python3
"""
Debug script to test NLP intent classification
"""
import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from astros.ai.nlp import EnhancedNLPProcessor

async def debug_nlp():
    """Debug NLP processing"""
    nlp = EnhancedNLPProcessor()
    
    test_phrases = [
        "hello",
        "hi there", 
        "good morning",
        "help me",
        "what can you do",
        "calculate 2 + 3",
        "what is 5 * 6",
        "system info"
    ]
    
    print("🔍 Debug NLP Intent Classification")
    print("=" * 50)
    
    # Test local intent classification directly
    for phrase in test_phrases:
        print(f"\n🔸 Testing: '{phrase}'")
        
        # Test pattern matching logic manually
        text_lower = phrase.lower()
        patterns = nlp.intent_patterns
        
        for intent_name, intent_patterns in patterns.items():
            matches = []
            for pattern in intent_patterns:
                if pattern.lower() in text_lower:
                    matches.append(pattern)
            
            if matches:
                print(f"   ✅ {intent_name}: {matches}")
        
        # Test the actual classification
        result = await nlp._classify_intent_local(phrase, [])
        if result:
            print(f"   🎯 Final Intent: {result.name} (confidence: {result.confidence:.2f})")
        else:
            print(f"   ❌ No intent found")

if __name__ == "__main__":
    asyncio.run(debug_nlp())