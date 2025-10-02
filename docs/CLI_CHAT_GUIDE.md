# AstrOS CLI Chatting & Testing Guide

## How to Test astros-cli (Chatting)

### 1. Make sure the service and virtualenv are set up
- Install the package: `sudo dpkg -i astros-core.deb`
- Set your API key in `~/.config/astros/agent.env`
- Start the service: `sudo systemctl start astros-agent@$(whoami)`

### 2. Run a chat query from the terminal
```bash
astros-cli "Hello! How are you?"
astros-cli "What is the weather in Paris?"
astros-cli "Write a Python function to reverse a string."
astros-cli "Tell me a joke."
```

### 3. Multi-turn chat (simulate by running multiple commands)
```bash
astros-cli "Who won the World Cup in 2022?"
astros-cli "What was the score in the final?"
astros-cli "Who scored the winning goal?"
```

### 4. Troubleshooting
- If you see errors about missing virtualenv, run: `sudo dpkg-reconfigure astros-core`
- If you see errors about missing API key, edit `~/.config/astros/agent.env` and add `ASTROS_API_KEY=your_key_here`
- To see logs: `sudo journalctl -u astros-agent@$(whoami) -n 20`

### 5. Example Chat Session
```bash
$ astros-cli "Hello!"
💭 Thinking...
Hi there! How can I assist you today?

$ astros-cli "What's 5+7?"
💭 Thinking...
The sum of 5 and 7 is 12.

$ astros-cli "Tell me a fun fact."
💭 Thinking...
Did you know? Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs!
```

### 6. Advanced: Use in scripts
You can call `astros-cli` from any shell script and capture the output:
```bash
RESPONSE=$(astros-cli "Summarize the latest news.")
echo "$RESPONSE"
```

---

## Documentation Location
- Main guide: `docs/INSTALLATION_GUIDE.md`
- Quick reference: `docs/QUICK_REFERENCE.md`
- Troubleshooting: `docs/INSTALLATION_GUIDE.md#troubleshooting`
- Example chats: This file (`docs/CLI_CHAT_GUIDE.md`)

---

## Need help?
- View logs: `sudo journalctl -u astros-agent@$(whoami) -f`
- Discord: https://discord.gg/9qQstuyt
- GitHub Issues: https://github.com/CoreOrganizations/AstrOS/issues

---

**Test your CLI by chatting with AstrOS!**
