# 🚀 AstrOS Quick Reference

## One-Line Setup
```bash
pip install openai httpx python-dotenv && python astros.py
```

## Essential Commands
```bash
# Validate configuration
python validate_env.py

# Run AstrOS
python astros.py

# Run tests
python test_system.py
```

## .env Quick Config
```bash
# Minimal required configuration
ASTROS_API_KEY=your-api-key-here
ASTROS_AI_MODEL__NAME=openai/gpt-oss-20b:free
```

## Get Free API Key
1. Visit: https://openrouter.ai/keys
2. Sign up (free)
3. Copy your key
4. Add to `.env`: `ASTROS_API_KEY=sk-or-v1-...`

## Switch AI Models
Edit `.env` and change `ASTROS_AI_MODEL__NAME`:
- `openai/gpt-oss-20b:free` - High quality (current)
- `x-ai/grok-4-fast:free` - Very fast
- `qwen/qwen-2.5-72b-instruct:free` - Complex tasks
- `meta-llama/llama-3.2-11b-vision-instruct:free` - Vision
- `microsoft/phi-3-medium-128k-instruct:free` - Large context

## Interactive Commands
While running AstrOS:
- `status` - Show system status
- `quit` or `exit` - Exit gracefully

## Files You Need
- `.env` - Configuration (✅ configured)
- `astros.py` - Main application (✅ ready)
- `validate_env.py` - Validator (✅ ready)

## Troubleshooting
| Issue | Solution |
|-------|----------|
| No API key found | Add `ASTROS_API_KEY` to `.env` |
| API fails | Check internet, verify API key |
| Import errors | Run `pip install -r requirements.txt` |
| Advanced features disabled | Install all requirements |

## Features
✅ Environment-based config  
✅ Error handling & recovery  
✅ Context management  
✅ Conversation memory  
✅ Multiple AI models  
✅ Fallback systems  

## Status Check
```bash
python validate_env.py
```
Should show: `✅ CONFIGURATION VALID`

## Need Help?
- Setup: `ENV_SETUP.md`
- Summary: `ENV_IMPLEMENTATION_SUMMARY.md`
- Roadmap: `ROADMAP.md`

---
**Current Model**: OpenAI OSS 20B  
**Status**: ✅ Ready to use  
**Version**: 1.2.0
