# 🚀 Getting Started with AstrOS

Welcome to AstrOS - the world's first AI-integrated operating system! Featuring **API-First Architecture** with **GPT-OSS-20B** for intelligent responses to any question or command.

## ✨ What's New: Complete AI Agent Ready!

🎉 **Zero Setup Required!** AstrOS comes pre-configured with:
- ✅ GPT-OSS-20B (microsoft/wizardlm-2-8x22b) API access 
- ✅ Complete dependency management
- ✅ Interactive and demo modes
- ✅ Full AI capabilities out of the box

## 📋 Prerequisites

- **Python 3.10+** (Python 3.12+ recommended)  
- **Git** for cloning the repository
- **Internet connection** for AI model access
- **✅ Everything else is auto-installed!**

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

### 2. Launch the Complete AI Agent (One Command!)

#### 🚀 **Start AstrOS** (Clean & Simple)
```bash
# Interactive mode - chat with GPT-OSS-20B
python astros.py interactive

# Quick demo - see AI capabilities  
python astros.py demo

# Or just run and choose mode
python astros.py
```

#### � **Quick Demo** (See AI capabilities)
```bash
# Run 5 sample queries to see GPT-OSS-20B in action
python run_complete_agent.py demo
```

#### 🔧 **Advanced Options**
```bash
# Manual mode selection
python run_complete_agent.py
# Then choose: 1=Interactive, 2=Demo, 3=Server

# Legacy test scripts (if needed)
python test_quick_api.py
python showcase_gpt_oss_20b.py interactive
```

### 🎮 What You Can Ask the AI

Once running, try these example commands:

**🧮 Mathematics & Calculations:**
- "Calculate 247 * 139 + 567 step by step"
- "What's the derivative of x³ + 2x² - 5x + 7?"
- "Solve this equation: 2x + 5 = 15"

**💻 Programming & Code:**
- "Write a Python function to find prime numbers"
- "Explain the difference between async and sync programming"
- "Debug this code: [paste your code]"

**🧠 Knowledge & Explanations:**
- "Explain quantum computing in simple terms"
- "What are the differences between AI, ML, and Deep Learning?"
- "How does blockchain technology work?"

**🎨 Creative & Problem Solving:**
- "Write a short story about an AI learning emotions"
- "Give me 5 creative ways to organize digital files"
- "Help me brainstorm ideas for a mobile app"

**🔧 System & Technical Help:**
- "How do I speed up my computer?"
- "What are the best practices for password security?"
- "Help me understand network protocols"
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

### 🎯 **What You'll See (GPT-OSS-20B Demo)**
```
🚀 AstrOS Complete AI Agent
==================================================
🤖 Powered by GPT-OSS-20B (microsoft/wizardlm-2-8x22b)
🌐 API Endpoint: OpenRouter
🧠 Features: API-First Intelligence + Local Tools
==================================================

🔑 API Status: ✅ READY
🤖 Model: microsoft/wizardlm-2-8x22b

✅ Agent ready!

💡 Try these commands:
   • 'Explain quantum computing in simple terms'
   • 'Write a Python function to sort numbers'
   • 'Calculate 247 * 139 + 567 step by step'
   • 'What can you help me with?'
   • 'Hello, how are you?'

🌟 You: Hello! What can you do?
🤖 AstrOS: Hello! I'm AstrOS, an intelligent AI assistant designed to help you with a wide range of tasks...
   📊 [567 tokens, openai_api]
```

### 🧪 **Try These Example Commands:**
- **"Hello! What are you and what can you do?"** - Get a comprehensive introduction
- **"Calculate 25 * 47 + 123"** - See intelligent math with step-by-step reasoning  
- **"Explain artificial intelligence in simple terms"** - Get clear explanations
- **"Write a Python function to find prime numbers"** - Code generation and programming help
- **"Help me organize my digital photos efficiently"** - Creative problem solving

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