# 🚀 AstrOS API Setup Guide

## Overview

AstrOS now features an **API-First Architecture** powered by GPT-OSS-20B! The system comes pre-configured with a working API key for immediate use, but contributors can bring their own API keys for enhanced control and customization.

### ✨ What's New: GPT-OSS-20B Integration

- 🚀 **Pre-configured** with microsoft/wizardlm-2-8x22b model via OpenRouter
- 🤖 **API-First processing** - all queries go to LLM first
- 🧠 **Intelligent responses** to any question or command
- 🔧 **Smart tool integration** - AI decides when to use local tools
- 🎯 **Response customization** system for fine-tuning outputs

## 🔑 API Provider Options

### Option 1: OpenAI Direct (Recommended)
- **Provider**: OpenAI
- **Models**: GPT-4, GPT-4-turbo, GPT-3.5-turbo
- **Cost**: Pay-per-use pricing
- **Setup**: Direct OpenAI account

### Option 2: OpenRouter (Cost-Effective Alternative) ⭐
- **Provider**: OpenRouter.ai
- **Models**: GPT-4, Claude, Llama, and many more
- **Cost**: Often cheaper than direct API access
- **Setup**: OpenRouter account (supports multiple providers)

## 🛠️ Setup Instructions

### Method 0: Use Pre-configured GPT-OSS-20B (Ready to Use!) ⭐

AstrOS comes with a working GPT-OSS-20B configuration:

```bash
# Test the pre-configured API
python test_quick_api.py

# Or start interactive mode
python demo_api_first.py interactive
```

**Features Available:**
- ✅ GPT-OSS-20B (microsoft/wizardlm-2-8x22b) model
- ✅ OpenRouter API integration
- ✅ 4000 token responses
- ✅ Response customization system
- ✅ Automatic fallback to local processing

### Method 1: OpenAI Direct Setup

1. **Create OpenAI Account**
   ```bash
   # Visit https://platform.openai.com/
   # Create account and verify email
   ```

2. **Generate API Key**
   ```bash
   # Go to https://platform.openai.com/api-keys
   # Click "Create new secret key"
   # Copy the key (starts with sk-...)
   ```

3. **Configure AstrOS**
   ```bash
   # Set environment variables
   export ASTROS_OPENAI_API_KEY="sk-your-key-here"
   export ASTROS_ENABLE_OPENAI=true
   export ASTROS_OPENAI_MODEL="gpt-4"
   ```

### Method 2: OpenRouter Setup (Recommended for Cost Savings)

1. **Create OpenRouter Account**
   ```bash
   # Visit https://openrouter.ai/
   # Sign up with GitHub or email
   ```

2. **Add Credits**
   ```bash
   # Go to https://openrouter.ai/credits
   # Add credits (as low as $5 minimum)
   # Much cheaper than OpenAI direct pricing
   ```

3. **Generate API Key**
   ```bash
   # Go to https://openrouter.ai/keys
   # Create new API key
   # Copy the key
   ```

4. **Configure AstrOS for OpenRouter**
   ```bash
   # Set environment variables for OpenRouter
   export ASTROS_OPENAI_API_KEY="sk-or-v1-your-openrouter-key"
   export ASTROS_OPENAI_BASE_URL="https://openrouter.ai/api/v1"
   export ASTROS_ENABLE_OPENAI=true
   export ASTROS_OPENAI_MODEL="openai/gpt-4"  # or "anthropic/claude-3-haiku" etc.
   ```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ASTROS_OPENAI_API_KEY` | Your API key | None | `sk-...` or `sk-or-v1-...` |
| `ASTROS_OPENAI_BASE_URL` | API endpoint | OpenAI default | `https://openrouter.ai/api/v1` |
| `ASTROS_ENABLE_OPENAI` | Enable GPT features | `false` | `true` |
| `ASTROS_OPENAI_MODEL` | Model to use | `gpt-4` | `openai/gpt-4` |
| `ASTROS_OPENAI_MAX_TOKENS` | Max response tokens | `1000` | `2000` |
| `ASTROS_OPENAI_TEMPERATURE` | Response creativity | `0.7` | `0.5` |
| `ASTROS_CONVERSATION_MEMORY` | Context size | `10` | `20` |
| `ASTROS_FALLBACK_TO_LOCAL` | Use local if API fails | `true` | `false` |

### Configuration File (Optional)

Create `~/.astros/config.yaml`:

```yaml
# AstrOS Enhanced Configuration
ai:
  enable_openai: true
  enable_local_nlp: true
  fallback_to_local: true
  conversation_memory_size: 10

openai:
  api_key: "sk-your-key-here"  # Better to use environment variable
  base_url: "https://openrouter.ai/api/v1"  # Optional: for OpenRouter
  model: "openai/gpt-4"
  max_tokens: 1000
  temperature: 0.7
  timeout: 30

agent:
  name: "AstrOS Enhanced Assistant"
  personality: "helpful"
  response_style: "conversational"

security:
  log_api_requests: false  # Don't log for privacy
  max_request_size: 10000
  rate_limit_per_minute: 60
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Make sure you're in the AstrOS directory
cd AstrOS

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install the enhanced version
pip install -e .
```

### 2. Set Your API Key
```bash
# For OpenAI Direct
export ASTROS_OPENAI_API_KEY="sk-your-openai-key"
export ASTROS_ENABLE_OPENAI=true

# OR for OpenRouter (cheaper alternative)
export ASTROS_OPENAI_API_KEY="sk-or-v1-your-openrouter-key"
export ASTROS_OPENAI_BASE_URL="https://openrouter.ai/api/v1"
export ASTROS_OPENAI_MODEL="openai/gpt-4"
export ASTROS_ENABLE_OPENAI=true
```

### 3. Run AstrOS
```bash
# Run the enhanced demo
python demo_enhanced.py

# Or run interactively
python -c "
import asyncio
from src.astros.core.agent import AstrOSAgent

async def chat():
    agent = AstrOSAgent()
    await agent.initialize()
    
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['quit', 'exit']:
            break
        response = await agent.process_command(user_input)
        print(f'AstrOS: {response[\"message\"]}')
    
    await agent.shutdown()

asyncio.run(chat())
"
```

**💡 Tip**: Start with OpenRouter for cost-effective experimentation!

## 🔒 Security & Privacy

### API Key Security
- **Never commit API keys to Git**
- **Use environment variables**
- **Rotate keys regularly**
- **Monitor usage on provider dashboards**

### Privacy Controls
```bash
# Configure privacy settings
export ASTROS_LOG_API_REQUESTS=false    # Don't log requests
export ASTROS_FALLBACK_TO_LOCAL=true    # Use local processing when possible
export ASTROS_MAX_REQUEST_SIZE=5000     # Limit request size
```

### Local-First Approach
- **AstrOS works without API keys** (local mode)
- **API calls are optional enhancements**
- **Fallback to local processing if API fails**
- **You control what data is sent to APIs**

## 🧪 Testing Your Setup

### Verify API Connection
```bash
# Test API connectivity
python -c "
import asyncio
from src.astros.ai.openai_client import test_openai_connection

async def test():
    result = await test_openai_connection()
    print(f'API Connection: {'✅ Working' if result else '❌ Failed'}')

asyncio.run(test())
"
```

### Run Enhanced Features Test
```bash
# Test enhanced capabilities
python demo_enhanced.py
```

Expected output with API:
```
🚀 Enhanced AstrOS Stages 1 & 2 Demo
============================================================
🔧 Configuration Status:
   • OpenAI Enabled: True
   • Local NLP Enabled: True
   • Agent Name: AstrOS Enhanced Demo
   • Model: gpt-4
   • API Key: ********************abcd

🔸 Test 1/10: hello there!
🤖 Hello! I'm AstrOS, your enhanced AI assistant powered by GPT-4. I can help you with calculations, file management, system information, and much more. How can I assist you today?
📊 Intent: greeting (0.95) | Tokens: 45 | Powered by GPT
```

## 🔧 Troubleshooting

### Common Issues

#### "API Key not configured"
```bash
# Check environment variables
echo $ASTROS_OPENAI_API_KEY
echo $ASTROS_ENABLE_OPENAI

# Set them if missing
export ASTROS_OPENAI_API_KEY="your-key-here"
export ASTROS_ENABLE_OPENAI=true
```

#### "OpenAI API error: 401 Unauthorized"
```bash
# Verify your API key is correct
# Check your OpenAI/OpenRouter dashboard
# Ensure key has proper permissions
```

#### "Rate limit exceeded"
```bash
# Reduce request frequency
export ASTROS_RATE_LIMIT_PER_MINUTE=30

# Or use a different model
export ASTROS_OPENAI_MODEL="gpt-3.5-turbo"
```

#### "Model not found"
```bash
# For OpenRouter, use full model names:
export ASTROS_OPENAI_MODEL="openai/gpt-4"
export ASTROS_OPENAI_MODEL="anthropic/claude-3-haiku"
export ASTROS_OPENAI_MODEL="meta-llama/llama-2-70b-chat"
```

### Getting Help

1. **Check the logs**: AstrOS provides detailed logging
2. **Join our Discord**: Get real-time help from the community
3. **GitHub Issues**: Report bugs and get support
4. **Documentation**: Check our full documentation at docs.astros.org

## 🎯 Advanced Configuration

### Multiple API Providers
```yaml
# ~/.astros/config.yaml
ai:
  providers:
    - name: "openai"
      base_url: "https://api.openai.com/v1"
      api_key: "${OPENAI_API_KEY}"
      models: ["gpt-4", "gpt-3.5-turbo"]
    
    - name: "openrouter"
      base_url: "https://openrouter.ai/api/v1"
      api_key: "${OPENROUTER_API_KEY}"
      models: ["openai/gpt-4", "anthropic/claude-3-haiku"]
  
  default_provider: "openrouter"
  fallback_provider: "local"
```

### Custom Model Configuration
```bash
# Use specific models for different tasks
export ASTROS_CHAT_MODEL="openai/gpt-4"           # For conversations
export ASTROS_TASK_MODEL="anthropic/claude-3-haiku"  # For tasks
export ASTROS_CODE_MODEL="openai/gpt-4"           # For code generation
```

## 📊 Monitoring Usage

### Track API Costs
```bash
# Monitor token usage
python -c "
from src.astros.core.config_enhanced import get_config
config = get_config()
print(f'Current model: {config.openai.model}')
print(f'Max tokens per request: {config.openai.max_tokens}')
"
```

### Usage Analytics
- Check OpenAI/OpenRouter dashboards for detailed usage
- Monitor costs and set billing alerts
- Track which features use the most tokens

## 🤝 Contributing

### For Contributors
1. **Set up your own API key** for testing
2. **Use OpenRouter** for cost-effective development
3. **Test both API and local modes** before submitting PRs
4. **Don't commit API keys** - use environment variables
5. **Document any new API features** you add

### Testing Guidelines
```bash
# Always test both modes
export ASTROS_ENABLE_OPENAI=true    # Test API mode
export ASTROS_ENABLE_OPENAI=false   # Test local mode

# Run the test suite
python -m pytest tests/ -v
```

---

## 📞 Support

- **Discord**: Join our community for real-time help
- **GitHub Issues**: Report bugs and feature requests
- **Email**: aiastros2025@gmail.com for security issues
- **Documentation**: Full docs at docs.astros.org

**Happy coding with AstrOS! 🚀**