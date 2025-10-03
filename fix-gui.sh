#!/bin/bash
# Fix GUI issues and install missing dependencies

echo "🔧 Fixing AstrOS GUI Issues"
echo "============================"
echo ""

# 1. Install missing system package for girepository
echo "1️⃣ Installing girepository development files..."
sudo apt install -y libgirepository1.0-dev gobject-introspection

# 2. Verify PyGObject system installation
echo ""
echo "2️⃣ Verifying PyGObject (system package)..."
python3 -c "import gi; print('✅ PyGObject version:', gi.__version__)" 2>/dev/null || {
    echo "⚠️  PyGObject not fully installed, installing..."
    sudo apt install -y python3-gi python3-gi-cairo
}

# 3. Verify GTK4
echo ""
echo "3️⃣ Verifying GTK4..."
python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk; print('✅ GTK4 version:', Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)" || {
    echo "❌ GTK4 not available"
    exit 1
}

# 4. Verify Adwaita
echo ""
echo "4️⃣ Verifying Libadwaita..."
python3 -c "import gi; gi.require_version('Adw', '1'); from gi.repository import Adw; print('✅ Libadwaita available')" || {
    echo "❌ Libadwaita not available"
    exit 1
}

# 5. Make launcher executable
echo ""
echo "5️⃣ Setting up launcher..."
chmod +x astros-gui
echo "✅ Launcher ready: ./astros-gui"

# 6. Check DISPLAY
echo ""
echo "6️⃣ Checking display..."
if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY not set"
    if grep -qi microsoft /proc/version; then
        echo "💡 For WSL2, run:"
        echo '   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '\''{print $2}'\''):0'
        echo ""
        echo "   And make sure VcXsrv is running on Windows"
    fi
else
    echo "✅ DISPLAY set to: $DISPLAY"
fi

echo ""
echo "============================"
echo "✅ GUI Setup Complete!"
echo "============================"
echo ""
echo "To launch GUI:"
echo "  ./astros-gui"
echo ""
echo "Or directly:"
echo "  ~/.local/share/astros/venv/bin/python3 gui/app.py"
echo ""
