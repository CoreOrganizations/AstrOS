#!/bin/bash
# Quick test script for AstrOS GUI

echo "🧪 AstrOS GUI Quick Test"
echo "========================"
echo ""

# Check Python
echo "1️⃣ Checking Python..."
python3 --version || { echo "❌ Python3 not found"; exit 1; }
echo "✅ Python OK"
echo ""

# Check if in WSL
if grep -qi microsoft /proc/version; then
    echo "📍 Environment: WSL2"
    echo "⚠️  GUI requires X server (VcXsrv, X410, etc.)"
    echo ""
    
    # Check DISPLAY
    if [ -z "$DISPLAY" ]; then
        echo "❌ DISPLAY not set"
        echo "💡 Run: export DISPLAY=\$(cat /etc/resolv.conf | grep nameserver | awk '{print \$2}'):0"
        echo ""
    else
        echo "✅ DISPLAY set to: $DISPLAY"
        echo ""
    fi
fi

# Check dependencies
echo "2️⃣ Checking dependencies..."

if python3 -c "import gi" 2>/dev/null; then
    echo "✅ PyGObject installed"
else
    echo "❌ PyGObject not found"
    echo "💡 Run: ./setup-gui-dependencies.sh"
    exit 1
fi

if python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "✅ GTK4 available"
else
    echo "❌ GTK4 not found"
    echo "💡 Run: sudo apt install gir1.2-gtk-4.0"
    exit 1
fi

if python3 -c "import gi; gi.require_version('Adw', '1'); from gi.repository import Adw" 2>/dev/null; then
    echo "✅ Libadwaita available"
else
    echo "❌ Libadwaita not found"
    echo "💡 Run: sudo apt install gir1.2-adw-1"
    exit 1
fi

echo ""

# Check AstrOS agent
echo "3️⃣ Checking AstrOS backend..."
if [ -d "$HOME/.local/share/astros/venv" ]; then
    echo "✅ AstrOS virtualenv found"
else
    echo "⚠️  AstrOS virtualenv not found (GUI will run in demo mode)"
fi

if [ -f "$HOME/.config/astros/agent.env" ]; then
    echo "✅ Config file exists"
    if grep -q "ASTROS_API_KEY" "$HOME/.config/astros/agent.env"; then
        echo "✅ API key configured"
    else
        echo "⚠️  API key not set"
    fi
else
    echo "⚠️  Config file not found (GUI will run in demo mode)"
fi

echo ""

# Check if we can import astros module
if python3 -c "import sys; sys.path.insert(0, '.'); from astros import AstrOSAgent" 2>/dev/null; then
    echo "✅ AstrOS module available"
else
    echo "⚠️  AstrOS module not in path (GUI will run in demo mode)"
fi

echo ""
echo "========================"
echo "🚀 Ready to test GUI!"
echo "========================"
echo ""
echo "Run: python3 gui/app.py"
echo ""

# Optionally run GUI
if [ "$1" == "--run" ]; then
    echo "Launching GUI..."
    python3 gui/app.py
fi
