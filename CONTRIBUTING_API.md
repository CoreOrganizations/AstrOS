# 🤝 Contributing to AstrOS with API Integration

## Welcome Contributors! 

Thank you for your interest in contributing to AstrOS! This guide covers everything you need to know about working with our enhanced AI features and API integrations.

## 🚀 Quick Contributor Setup

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/AstrOS.git
cd AstrOS
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install in development mode
pip install -e .
```

### 3. Choose Your API Setup

**🆓 Option A: Local Development (No API Key)**
```bash
# Work with local AI features only
export ASTROS_ENABLE_OPENAI=false
export ASTROS_ENABLE_LOCAL_NLP=true
```

**💰 Option B: OpenRouter (Recommended for Contributors)**
```bash
# Sign up at https://openrouter.ai
# Add $5+ credits (much cheaper than OpenAI direct)
export ASTROS_OPENAI_API_KEY="sk-or-v1-your-openrouter-key"
export ASTROS_OPENAI_BASE_URL="https://openrouter.ai/api/v1"
export ASTROS_OPENAI_MODEL="openai/gpt-4"
export ASTROS_ENABLE_OPENAI=true
```

**🔧 Option C: OpenAI Direct**
```bash
# Get API key from https://platform.openai.com/api-keys
export ASTROS_OPENAI_API_KEY="sk-your-openai-key"
export ASTROS_ENABLE_OPENAI=true
```

## 🧪 Testing Your Setup

### Run Tests
```bash
# Test both API and local modes
export ASTROS_ENABLE_OPENAI=true
python -m pytest tests/ -v -k "test_openai"

export ASTROS_ENABLE_OPENAI=false  
python -m pytest tests/ -v -k "test_local"
```

### Interactive Testing
```bash
# Test enhanced features
python demo_enhanced.py

# Simple functionality test
python test_simple.py
```

## 📋 Development Guidelines

### 🔒 Security Best Practices

1. **Never Commit API Keys**
   ```bash
   # ❌ NEVER do this
   API_KEY = "sk-1234567890"
   
   # ✅ Always use environment variables
   API_KEY = os.getenv("ASTROS_OPENAI_API_KEY")
   ```

2. **Use .env Files for Local Development**
   ```bash
   # Create .env file (already in .gitignore)
   echo "ASTROS_OPENAI_API_KEY=your-key-here" > .env
   echo "ASTROS_ENABLE_OPENAI=true" >> .env
   
   # Load in your development scripts
   from dotenv import load_dotenv
   load_dotenv()
   ```

3. **Validate Configuration**
   ```python
   # Always check if API is available before using
   if config.ai.enable_openai and openai_client.is_available():
       # Use enhanced features
   else:
       # Fallback to local processing
   ```

### 🧩 Code Architecture

#### Working with API Features
```python
# Example: Adding a new AI-powered feature
from src.astros.core.config_enhanced import get_config
from src.astros.ai.openai_client import get_openai_client

async def my_enhanced_feature(user_input: str):
    config = get_config()
    
    if config.ai.enable_openai:
        # Try GPT-powered approach
        try:
            client = get_openai_client()
            if client.is_available():
                response = await client.generate_response(user_input)
                return response.content
        except Exception as e:
            logger.warning(f"GPT processing failed: {e}")
    
    # Always provide local fallback
    return local_processing_function(user_input)
```

#### Plugin Development with AI
```python
# Example: GPT-enhanced plugin
class EnhancedCalculatorPlugin(BasePlugin):
    async def execute(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        # Try GPT for complex math problems
        if self.openai_client and "complex" in parameters:
            try:
                gpt_result = await self.openai_client.generate_response(
                    f"Solve this math problem: {parameters['expression']}"
                )
                return ExecutionResult.success_result(data={"result": gpt_result.content})
            except Exception:
                pass  # Fall through to local processing
        
        # Local calculation fallback
        return self.calculate_locally(parameters)
```

### 🏗️ Project Structure for Contributors

```
AstrOS/
├── src/astros/
│   ├── core/
│   │   ├── agent.py              # Main orchestrator with GPT integration
│   │   ├── config_enhanced.py    # Enhanced configuration system
│   │   └── __init__.py
│   ├── ai/
│   │   ├── openai_client.py      # GPT client wrapper
│   │   ├── nlp.py               # Enhanced NLP with GPT support
│   │   └── __init__.py
│   ├── plugins/
│   │   ├── base.py              # Plugin system (can use GPT)
│   │   └── __init__.py
│   └── system/
│       └── integration.py       # System integration
├── tests/
│   ├── unit/
│   │   ├── test_agent.py
│   │   ├── test_ai_components.py
│   │   └── test_openai.py       # API-specific tests
│   └── integration/
├── API_SETUP.md                 # API setup guide
├── CONTRIBUTING_API.md           # This file
├── demo_enhanced.py             # Enhanced demo with GPT
└── requirements.txt
```

## 🎯 Contribution Areas

### High-Priority Areas

1. **🧠 AI Enhancement**
   - Improve GPT prompt engineering
   - Add support for more AI providers
   - Enhance local AI capabilities
   - Better error handling for API failures

2. **🔌 Plugin Development**
   - Create GPT-powered plugins
   - Improve existing plugins with AI
   - Add plugin marketplace features
   - Better plugin configuration

3. **🔧 System Integration**
   - Ubuntu ISO building improvements
   - Better hardware support
   - Performance optimizations
   - Security enhancements

4. **📚 Documentation**
   - API integration guides
   - Plugin development tutorials
   - User documentation
   - Code examples and demos

### 🏷️ Issue Labels to Look For

- `good-first-issue` - Perfect for new contributors
- `api-integration` - Related to OpenAI/OpenRouter features
- `local-ai` - Local processing improvements
- `plugin-system` - Plugin-related work
- `documentation` - Docs improvements
- `testing` - Test coverage improvements

## 🧪 Testing Guidelines

### Test Coverage Requirements
- **All new API features must have tests**
- **Test both API and local modes**
- **Include error handling tests**
- **Mock API calls in unit tests**

### Example Test Structure
```python
import pytest
from unittest.mock import patch, AsyncMock

class TestEnhancedAgent:
    @pytest.mark.asyncio
    async def test_with_api_enabled(self):
        """Test agent with API features enabled"""
        with patch.dict(os.environ, {"ASTROS_ENABLE_OPENAI": "true"}):
            agent = AstrOSAgent()
            await agent.initialize()
            response = await agent.process_command("hello")
            assert response["success"] == True
    
    @pytest.mark.asyncio
    async def test_local_fallback(self):
        """Test fallback to local processing"""
        with patch.dict(os.environ, {"ASTROS_ENABLE_OPENAI": "false"}):
            agent = AstrOSAgent()
            await agent.initialize()
            response = await agent.process_command("hello")
            assert response["success"] == True
    
    @pytest.mark.asyncio
    @patch('src.astros.ai.openai_client.AsyncOpenAI')
    async def test_api_error_handling(self, mock_openai):
        """Test graceful handling of API errors"""
        mock_openai.side_effect = Exception("API Error")
        # Test should still pass with local fallback
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run only API-related tests
python -m pytest tests/ -v -k "openai or api"

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## 📝 Pull Request Guidelines

### Before Submitting
1. **Test both API and local modes**
2. **Update documentation if needed**
3. **Add tests for new features**
4. **Ensure no API keys in code**
5. **Run the linter**: `black src/ && isort src/`

### PR Description Template
```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] API integration improvement
- [ ] Documentation update
- [ ] Test improvement

## API Testing
- [ ] Tested with OpenAI API
- [ ] Tested with OpenRouter
- [ ] Tested in local mode
- [ ] All tests pass

## Checklist
- [ ] No API keys committed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Code formatted with black
```

## 💰 Cost Management for Contributors

### Free Development Options
1. **Local Mode**: Full functionality without API costs
2. **OpenRouter Free Tier**: Some models have free tiers
3. **OpenAI Free Credits**: New accounts get free credits

### Cost-Effective Testing
```bash
# Use cheaper models for testing
export ASTROS_OPENAI_MODEL="gpt-3.5-turbo"  # OpenAI
export ASTROS_OPENAI_MODEL="openai/gpt-3.5-turbo"  # OpenRouter

# Limit token usage
export ASTROS_OPENAI_MAX_TOKENS=100
export ASTROS_CONVERSATION_MEMORY=3
```

### Monitor Your Usage
- Check OpenAI/OpenRouter dashboards regularly
- Set billing alerts
- Use local mode for extensive testing

## 🤝 Community Support

### Getting Help
- **Discord**: Join our contributor channel
- **GitHub Discussions**: For technical questions
- **Office Hours**: Weekly contributor meetups
- **Pair Programming**: Find a coding buddy

### Mentorship Program
New contributors can request mentorship:
- Code review guidance
- Architecture explanations
- API integration help
- Career development advice

## 🏆 Recognition

### Contributor Benefits
- **Featured in README**: Top contributors get recognition
- **Early Access**: Preview new features before release
- **Conference Talks**: Opportunities to present your work
- **Swag**: AstrOS merchandise for regular contributors

### Hall of Fame
We maintain a contributors wall recognizing:
- First-time contributors
- Regular contributors
- Major feature implementations
- Documentation improvements
- Community support

## 📞 Contact

- **General Questions**: Join our Discord
- **Security Issues**: aiastros2025@gmail.com
- **Contributor Support**: #contributors channel on Discord
- **Mentorship Requests**: #mentorship channel on Discord

---

## 🚀 Ready to Contribute?

1. **Set up your development environment**
2. **Choose an issue to work on**
3. **Join our Discord for support**
4. **Submit your first PR**

**Welcome to the AstrOS community! Let's build the future of AI-integrated computing together! 🚀**

---

*Last updated: September 28, 2025*