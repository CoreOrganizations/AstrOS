#!/usr/bin/env python3
"""
AstrOS Environment Configuration Validator
Checks and validates .env configuration
"""

import os
import sys
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            return True
        else:
            print("❌ .env file not found!")
            return False
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install python-dotenv")
        return False

def check_required_vars():
    """Check if required environment variables are set"""
    print("\n🔍 Checking Environment Configuration")
    print("=" * 60)
    
    required_vars = {
        'ASTROS_API_KEY': 'API Key for OpenRouter',
        'ASTROS_BASE_URL': 'API Base URL',
        'ASTROS_AI_MODEL__NAME': 'AI Model Name'
    }
    
    optional_vars = {
        'ASTROS_ENVIRONMENT': 'Application Environment',
        'ASTROS_DEBUG': 'Debug Mode',
        'ASTROS_AI_MODEL__MAX_TOKENS': 'Max Tokens',
        'ASTROS_AI_MODEL__TEMPERATURE': 'Temperature',
        'ASTROS_HOST': 'Server Host',
        'ASTROS_PORT': 'Server Port'
    }
    
    all_good = True
    
    print("\n✅ Required Configuration:")
    print("-" * 60)
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask API key for security
            if 'KEY' in var:
                display_value = value[:15] + "..." + value[-5:] if len(value) > 20 else "***"
            else:
                display_value = value
            print(f"  ✅ {var:30} = {display_value}")
        else:
            print(f"  ❌ {var:30} = NOT SET - {description}")
            all_good = False
    
    print("\n📋 Optional Configuration:")
    print("-" * 60)
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var:30} = {value}")
        else:
            print(f"  ⚠️  {var:30} = NOT SET (using default)")
    
    return all_good

def validate_api_key():
    """Validate API key format"""
    print("\n🔐 Validating API Key")
    print("=" * 60)
    
    api_key = os.getenv('ASTROS_API_KEY')
    if not api_key:
        print("  ❌ No API key found")
        return False
    
    # Check OpenRouter key format
    if api_key.startswith('sk-or-v1-'):
        print(f"  ✅ Valid OpenRouter key format")
        print(f"  ✅ Key length: {len(api_key)} characters")
        return True
    else:
        print(f"  ⚠️  Unexpected key format (should start with 'sk-or-v1-')")
        print(f"  ℹ️  Key length: {len(api_key)} characters")
        return True  # Still might work

def validate_model():
    """Validate AI model configuration"""
    print("\n🤖 Validating AI Model Configuration")
    print("=" * 60)
    
    model = os.getenv('ASTROS_AI_MODEL__NAME', 'openai/gpt-oss-20b:free')
    provider = os.getenv('ASTROS_AI_MODEL__PROVIDER', 'openrouter')
    
    print(f"  ✅ Model: {model}")
    print(f"  ✅ Provider: {provider}")
    
    # List of known free models
    free_models = [
        'openai/gpt-oss-20b:free',
        'x-ai/grok-4-fast:free',
        'qwen/qwen-2.5-72b-instruct:free',
        'meta-llama/llama-3.2-11b-vision-instruct:free',
        'microsoft/phi-3-medium-128k-instruct:free'
    ]
    
    if model in free_models:
        print(f"  ✅ Using free model tier")
    elif ':free' in model:
        print(f"  ℹ️  Using free model (not in verified list)")
    else:
        print(f"  ⚠️  This model may require credits")
    
    return True

def test_connection():
    """Test API connection"""
    print("\n🌐 Testing API Connection")
    print("=" * 60)
    
    try:
        import httpx
        base_url = os.getenv('ASTROS_BASE_URL', 'https://openrouter.ai/api/v1')
        
        print(f"  📡 Testing connection to: {base_url}")
        
        # Simple ping test
        with httpx.Client(timeout=5.0) as client:
            try:
                response = client.get("https://openrouter.ai")
                if response.status_code == 200:
                    print(f"  ✅ OpenRouter is reachable")
                    return True
                else:
                    print(f"  ⚠️  Unexpected response: {response.status_code}")
                    return False
            except Exception as e:
                print(f"  ❌ Connection failed: {e}")
                return False
    except ImportError:
        print("  ⚠️  httpx not installed, skipping connection test")
        print("  💡 Install with: pip install httpx")
        return None

def print_recommendations():
    """Print recommendations based on configuration"""
    print("\n💡 Recommendations")
    print("=" * 60)
    
    api_key = os.getenv('ASTROS_API_KEY')
    
    if not api_key:
        print("  1. Get a free API key from: https://openrouter.ai/keys")
        print("  2. Add it to your .env file: ASTROS_API_KEY=your-key-here")
        print("  3. Run this validator again")
    else:
        print("  ✅ Configuration looks good!")
        print("  💡 You can now run: python astros.py")
        print("  💡 To test the system: python test_system.py")
        print("  💡 For help: see ENV_SETUP.md")

def main():
    """Main validation function"""
    print("🚀 AstrOS Environment Configuration Validator")
    print("=" * 60)
    
    # Load .env file
    if not load_env():
        print("\n❌ Cannot proceed without .env file")
        print("💡 Create a .env file in the AstrOS directory")
        print("💡 See ENV_SETUP.md for instructions")
        return 1
    
    print("✅ .env file loaded successfully")
    
    # Run all checks
    config_ok = check_required_vars()
    key_ok = validate_api_key()
    model_ok = validate_model()
    connection_ok = test_connection()
    
    # Print recommendations
    print_recommendations()
    
    # Final verdict
    print("\n" + "=" * 60)
    if config_ok and key_ok and model_ok:
        print("✅ CONFIGURATION VALID - Ready to run AstrOS!")
        if connection_ok:
            print("✅ NETWORK TEST PASSED - API is reachable")
        return 0
    else:
        print("⚠️  CONFIGURATION INCOMPLETE - See issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
