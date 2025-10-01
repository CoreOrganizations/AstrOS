# AstrOS Setup Guide

## 🚀 Quick Start with .env Configuration

AstrOS now uses environment variables from the `.env` file for all configuration. This makes it easy to manage API keys and settings.

### 1. Prerequisites

- Python 3.8 or higher
- Internet connection
- OpenRouter API key (free)

### 2. Installation

```bash
# Clone or navigate to the AstrOS directory
cd AstrOS

# Install required packages
pip install -r requirements.txt

# Or install manually
pip install openai httpx python-dotenv
```

### 3. Configure Your .env File

The `.env` file is already set up with default values. You need to update the API key:

1. Get your free API key from [OpenRouter](https://openrouter.ai/keys)
2. Open `.env` file
3. Update the `ASTROS_API_KEY` with your key:

```bash
ASTROS_API_KEY=your-api-key-here
```

### 4. Run AstrOS

```bash
python astros.py
```

## 📋 Environment Configuration

### Core Settings

The `.env` file contains all configuration for AstrOS:

#### API Configuration
```bash
# Your OpenRouter API key
ASTROS_API_KEY=sk-or-v1-your-key-here

# API endpoint (default: OpenRouter)
ASTROS_BASE_URL=https://openrouter.ai/api/v1
```

#### AI Model Settings
```bash
# AI Model to use (default: OpenAI OSS 20B - free)
ASTROS_AI_MODEL__NAME=openai/gpt-oss-20b:free

# Model provider
ASTROS_AI_MODEL__PROVIDER=openrouter

# Model parameters
ASTROS_AI_MODEL__MAX_TOKENS=800
ASTROS_AI_MODEL__TEMPERATURE=0.7
ASTROS_AI_MODEL__TIMEOUT=30
```

#### Application Settings
```bash
# Environment mode
ASTROS_ENVIRONMENT=development

# Debug mode
ASTROS_DEBUG=true

# Server configuration
ASTROS_HOST=127.0.0.1
ASTROS_PORT=8000
```

## 🎯 Available AI Models

You can change the AI model in `.env` by updating `ASTROS_AI_MODEL__NAME`:

### Free Models (Recommended)
- `openai/gpt-oss-20b:free` (Default) - High quality, fast
- `x-ai/grok-4-fast:free` - Very fast responses
- `qwen/qwen-2.5-72b-instruct:free` - Great for complex tasks
- `meta-llama/llama-3.2-11b-vision-instruct:free` - Vision capabilities
- `microsoft/phi-3-medium-128k-instruct:free` - Large context window

### To change the model:
1. Open `.env`
2. Update `ASTROS_AI_MODEL__NAME=x-ai/grok-4-fast:free`
3. Restart AstrOS

## 🔧 Advanced Features

### Error Handling & Recovery
AstrOS includes advanced error handling:
- Circuit breaker pattern
- Intelligent fallback strategies
- Automatic retry with exponential backoff
- Graceful degradation

### Context Management
- Persistent conversation memory
- User facts extraction
- Conversation summarization
- Multi-level context storage

### To enable advanced features:
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## 🛠️ Troubleshooting

### "No API key found in .env file"
- Make sure `.env` file exists in the AstrOS directory
- Check that `ASTROS_API_KEY` is set with a valid key
- Verify there are no extra spaces or quotes

### "Environment variables loaded from .env file" but API fails
- Your API key might be invalid or expired
- Get a new free key from [OpenRouter](https://openrouter.ai/keys)
- Check your internet connection

### "Running in basic mode"
- Some advanced dependencies are missing
- Run: `pip install -r requirements.txt`
- Advanced features will activate automatically when dependencies are installed

## 📊 System Status

Type `status` in AstrOS to see:
- Conversation count
- Advanced features status
- Error statistics
- Circuit breaker status

## 🔐 Security Notes

- Never commit your `.env` file with real API keys to version control
- The `.env` file is already in `.gitignore`
- Keep your API keys private
- Rotate keys regularly

## 📝 Example .env Configuration

```bash
# Minimal configuration
ASTROS_API_KEY=your-api-key-here
ASTROS_AI_MODEL__NAME=openai/gpt-oss-20b:free

# Full configuration with all options
ASTROS_ENVIRONMENT=production
ASTROS_DEBUG=false
ASTROS_API_KEY=your-api-key-here
ASTROS_BASE_URL=https://openrouter.ai/api/v1
ASTROS_AI_MODEL__NAME=openai/gpt-oss-20b:free
ASTROS_AI_MODEL__MAX_TOKENS=800
ASTROS_AI_MODEL__TEMPERATURE=0.7
```

## 🎉 Features

- ✅ Environment-based configuration
- ✅ Secure API key management
- ✅ Multiple AI model support
- ✅ Advanced error handling
- ✅ Context management
- ✅ Conversation memory
- ✅ Fallback systems
- ✅ System status monitoring

## 📚 Next Steps

1. Configure your `.env` file with your API key
2. Choose your preferred AI model
3. Run `python astros.py`
4. Start asking questions!

For more information, see [ROADMAP.md](ROADMAP.md) for the development plan.
