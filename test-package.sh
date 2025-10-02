#!/bin/bash
# Test AstrOS Package Installation

set -e

echo "🧪 AstrOS Package Installation Test"
echo "======================================"
echo ""

PACKAGE_FILE="/mnt/d/AstrOS/packages/astros-core.deb"

# Check if package exists
if [ ! -f "$PACKAGE_FILE" ]; then
    echo "❌ Package not found: $PACKAGE_FILE"
    exit 1
fi

echo "📦 Package: $PACKAGE_FILE"
echo ""

# Show package info
echo "📋 Package Information:"
dpkg-deb --info "$PACKAGE_FILE" | grep -E "Package:|Version:|Architecture:|Depends:|Description:" | head -6
echo ""

# Check if already installed
if dpkg -l | grep -q astros-core; then
    echo "⚠️  Package already installed. Removing first..."
    sudo dpkg -r astros-core
    echo "✅ Old package removed"
    echo ""
fi

# Install package
echo "📥 Installing package..."
sudo dpkg -i "$PACKAGE_FILE" || {
    echo "⚠️  Dependency issues detected. Installing dependencies..."
    sudo apt-get install -f -y
    echo "✅ Dependencies installed"
}

echo ""
echo "======================================"
echo "✅ Package Installed Successfully!"
echo "======================================"
echo ""

# Verify installation
echo "🔍 Verification Tests:"
echo ""

# Test 1: Check files
echo "📋 Test 1: Files Present"
if [ -f /usr/lib/astros/agent/astros.py ]; then
    echo "  ✅ astros.py"
else
    echo "  ❌ astros.py missing"
fi

if [ -f /usr/lib/astros/agent/astros_daemon.py ]; then
    echo "  ✅ astros_daemon.py"
else
    echo "  ❌ astros_daemon.py missing"
fi

if [ -f /usr/bin/astros-cli ]; then
    echo "  ✅ astros-cli"
else
    echo "  ❌ astros-cli missing"
fi

if [ -f /etc/systemd/system/astros-agent@.service ]; then
    echo "  ✅ Service file"
else
    echo "  ❌ Service file missing"
fi
echo ""

# Test 2: Check config
echo "📋 Test 2: Configuration"
if [ -f ~/.config/astros/agent.env ]; then
    echo "  ✅ Config file created"
    lines=$(wc -l < ~/.config/astros/agent.env)
    echo "  📄 Config lines: $lines"
else
    echo "  ❌ Config file missing"
fi
echo ""

# Test 3: Check virtualenv
echo "📋 Test 3: Virtual Environment"
if [ -d ~/.local/share/astros/venv ]; then
    echo "  ✅ Virtual environment created"
    
    # Check packages
    packages=$(~/.local/share/astros/venv/bin/pip list --format=freeze 2>/dev/null | grep -E "httpx|openai|python-dotenv" | wc -l)
    echo "  📦 Required packages: $packages/3"
else
    echo "  ❌ Virtual environment missing"
fi
echo ""

# Test 4: Service status
echo "📋 Test 4: Service Status"
if systemctl is-enabled astros-agent@$(whoami) &>/dev/null; then
    echo "  ✅ Service enabled"
else
    echo "  ⚠️  Service not enabled (expected if no API key configured)"
fi

if systemctl is-active astros-agent@$(whoami) &>/dev/null; then
    echo "  ✅ Service running"
    uptime=$(systemctl show astros-agent@$(whoami) --property=ActiveEnterTimestamp --value)
    echo "  ⏱️  Started: $uptime"
else
    echo "  ⚠️  Service not running (expected if no API key configured)"
fi
echo ""

# Test 5: CLI command
echo "📋 Test 5: CLI Tool"
if command -v astros-cli &>/dev/null; then
    echo "  ✅ astros-cli available"
    echo "  📝 Usage: astros-cli 'your question'"
else
    echo "  ❌ astros-cli not in PATH"
fi
echo ""

echo "======================================"
echo "📝 Next Steps:"
echo "======================================"
echo ""

if grep -q "your-api-key-here" ~/.config/astros/agent.env 2>/dev/null; then
    echo "⚠️  Configuration needed:"
    echo ""
    echo "1. Edit config:"
    echo "   nano ~/.config/astros/agent.env"
    echo ""
    echo "2. Add your API key from: https://openrouter.ai/keys"
    echo ""
    echo "3. Enable and start service:"
    echo "   sudo systemctl enable astros-agent@$(whoami)"
    echo "   sudo systemctl start astros-agent@$(whoami)"
    echo ""
    echo "4. Check status:"
    echo "   sudo systemctl status astros-agent@$(whoami)"
    echo ""
    echo "5. Test CLI:"
    echo "   astros-cli 'What is 2+2?'"
else
    echo "✅ API key configured!"
    echo ""
    echo "Test the service:"
    echo "  sudo systemctl status astros-agent@$(whoami)"
    echo "  journalctl -u astros-agent@$(whoami) -f"
    echo ""
    echo "Test the CLI:"
    echo "  astros-cli 'What is 2+2?'"
fi

echo ""
echo "======================================"
echo "🎉 Installation Test Complete!"
echo "======================================"
