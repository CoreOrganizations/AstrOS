# 🚀 Getting Started with AstrOS

Welcome to AstrOS - the world's first AI-integrated operating system! This guide will help you get up and running quickly.

## 📋 Prerequisites

- **Python 3.10+** (Python 3.12+ recommended)
- **Git** for cloning the repository
- **Virtual environment** support (venv, conda, etc.)
- **Optional**: OpenAI or OpenRouter API key for enhanced AI features

## 🎯 Quick Setup (5 Minutes)

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/CoreOrganizations/AstrOS.git
cd AstrOS

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install AstrOS
pip install -e .
```

### 2. Choose Your Mode

#### 🆓 Option A: Local Mode (No API Key Required)
```bash
# Set environment variables for local mode
export ASTROS_ENABLE_OPENAI=false
export ASTROS_ENABLE_LOCAL_NLP=true

# Run AstrOS
python demo_enhanced.py
```

#### 🚀 Option B: Enhanced Mode with API (Recommended)
```bash
# Get API key from OpenRouter (cheaper) or OpenAI
# OpenRouter: https://openrouter.ai/keys
# OpenAI: https://platform.openai.com/api-keys

# For OpenRouter (recommended - cheaper):
export ASTROS_OPENAI_API_KEY="sk-or-v1-your-openrouter-key"
export ASTROS_OPENAI_BASE_URL="https://openrouter.ai/api/v1"
export ASTROS_OPENAI_MODEL="openai/gpt-4"
export ASTROS_ENABLE_OPENAI=true

# For OpenAI Direct:
export ASTROS_OPENAI_API_KEY="sk-your-openai-key"
export ASTROS_ENABLE_OPENAI=true

# Run enhanced AstrOS
python demo_enhanced.py
```

## 🎬 Your First AstrOS Experience

### Try These Commands:
- `"hello there!"` - Greet your AI assistant
- `"calculate 25 * 47"` - Perform calculations
- `"what can you help me with?"` - Learn about capabilities
- `"show system information"` - Get system details
- `"help me understand AstrOS"` - Get guidance

### Expected Output:
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
🤖 Hello! I'm AstrOS, your enhanced AI assistant. I can help you with calculations, file management, system information, and much more. How can I assist you today?
📊 Intent: greeting (0.95) | Powered by GPT
```

## 🔧 Interactive Mode

For a chat-like experience:

```bash
# Start interactive chat
python -c "
import asyncio
from src.astros.core.agent import AstrOSAgent

async def chat():
    print('🤖 AstrOS Interactive Mode - Type \"quit\" to exit')
    agent = AstrOSAgent()
    await agent.initialize()
    
    while True:
        user_input = input('\n👤 You: ')
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        response = await agent.process_command(user_input)
        print(f'🤖 AstrOS: {response[\"message\"]}')
    
    await agent.shutdown()
    print('👋 Goodbye!')

asyncio.run(chat())
"
```

## 🧪 Verify Your Setup

### Test Basic Functionality
```bash
# Run simple test
python test_simple.py
```

### Test API Connection (if using API)
```bash
# Test OpenAI/OpenRouter connection
python -c "
import asyncio
from src.astros.ai.openai_client import test_openai_connection

async def test():
    result = await test_openai_connection()
    print(f'✅ API Connection: {\"Working\" if result else \"Failed\"}')

asyncio.run(test())
"
```

### Run Full Test Suite
```bash
# Run all tests
python -m pytest tests/ -v
```

## 📁 Project Structure

```
AstrOS/
├── src/astros/                 # Main source code
│   ├── core/
│   │   ├── agent.py           # Main AI agent
│   │   └── config_enhanced.py # Configuration system
│   ├── ai/
│   │   ├── openai_client.py   # GPT integration
│   │   └── nlp.py            # Natural language processing
│   ├── plugins/               # Plugin system
│   └── system/               # System integration
├── tests/                     # Test suite
├── demo_enhanced.py          # Enhanced demo script
├── API_SETUP.md             # Detailed API setup guide
├── CONTRIBUTING_API.md       # Contributor guide
└── README.md                # Project overview
```

## 🔑 API Setup Details

### Cost-Effective Options

1. **OpenRouter (Recommended)**
   - Cheaper than OpenAI direct
   - Multiple AI providers
   - $5 minimum credit
   - Sign up: https://openrouter.ai

2. **OpenAI Direct**
   - Direct from OpenAI
   - Higher costs but stable
   - Sign up: https://platform.openai.com

### Environment Variables
```bash
# Required for API mode
export ASTROS_OPENAI_API_KEY="your-key-here"
export ASTROS_ENABLE_OPENAI=true

# Optional configurations
export ASTROS_OPENAI_MODEL="gpt-4"          # Model selection
export ASTROS_OPENAI_MAX_TOKENS=1000        # Response length
export ASTROS_OPENAI_TEMPERATURE=0.7        # Creativity level
export ASTROS_CONVERSATION_MEMORY=10        # Context length
```

## 🛠️ Troubleshooting

### Common Issues

#### "ImportError: No module named 'astros'"
```bash
# Make sure you installed in development mode
pip install -e .
```

#### "API Key not configured"
```bash
# Check your environment variables
echo $ASTROS_OPENAI_API_KEY
echo $ASTROS_ENABLE_OPENAI

# Set them if missing
export ASTROS_OPENAI_API_KEY="your-key-here"
export ASTROS_ENABLE_OPENAI=true
```

#### "OpenAI API error: 401 Unauthorized"
```bash
# Verify your API key is correct
# Check billing on your provider dashboard
# For OpenRouter, make sure you have credits
```

#### "Rate limit exceeded"
```bash
# Reduce request frequency or upgrade your plan
export ASTROS_RATE_LIMIT_PER_MINUTE=30
```

### Getting Help

1. **Check the logs** - AstrOS provides detailed error information
2. **Join Discord** - Real-time community support
3. **GitHub Issues** - Report bugs and get help
4. **Read the docs** - Check API_SETUP.md for detailed guides

## 🎯 What's Next?

### For Users
- Explore different AI models and providers
- Try building custom plugins
- Integrate with your daily workflow
- Join the community discussions

### For Developers
- Read [CONTRIBUTING_API.md](CONTRIBUTING_API.md)
- Check out open issues on GitHub
- Join our contributor Discord channel
- Start with issues labeled `good-first-issue`

### For System Integration
- Build custom Ubuntu ISO with AstrOS
- Create desktop integration
- Develop voice control features
- Implement system automation

## 📚 Additional Resources

- **[Complete API Setup Guide](API_SETUP.md)** - Detailed API configuration
- **[Contributing Guide](CONTRIBUTING_API.md)** - How to contribute
- **[Security Policy](SECURITY.md)** - Security best practices
- **[Project Roadmap](ROADMAP.md)** - Future development plans

## 💬 Community

- **Discord**: Join our active community
- **GitHub Discussions**: Technical questions and ideas
- **Twitter**: @AstrOSProject for updates
- **Email**: aiastros2025@gmail.com for security issues

---

## 🎉 Welcome to AstrOS!

You're now ready to experience the future of AI-integrated computing. Whether you're using local mode or enhanced API features, AstrOS will revolutionize how you interact with your computer.

**Happy exploring! 🚀**

---

*Need help? Join our Discord community or check out our documentation*