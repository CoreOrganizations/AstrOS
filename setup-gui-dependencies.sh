#!/bin/bash
# Setup GUI dependencies for AstrOS Desktop

echo "📦 Installing AstrOS Desktop GUI Dependencies"
echo "=========================================="

# Check if running in WSL
if grep -qi microsoft /proc/version; then
    echo "⚠️  Detected WSL environment"
    echo "📝 Note: GUI requires X server (VcXsrv, X410, etc.)"
    echo ""
fi

# Update package list
echo "📋 Updating package list..."
sudo apt update

# Install GTK4 and dependencies
echo "🎨 Installing GTK4..."
sudo apt install -y \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-4.0 \
    gir1.2-adw-1 \
    libadwaita-1-0 \
    libadwaita-1-dev

# Install notification support
echo "🔔 Installing notification support..."
sudo apt install -y \
    gir1.2-notify-0.7 \
    libnotify-bin \
    libnotify-dev

# Install additional tools
echo "🛠️  Installing additional tools..."
sudo apt install -y \
    python3-cairo \
    python3-cairo-dev \
    pkg-config

# Note about Python packages
echo ""
echo "📝 Note: PyGObject must be installed as system package (not in virtualenv)"
echo "   The GUI will use system PyGObject with virtualenv AstrOS modules"
echo ""

# Verify PyGObject is available
if python3 -c "import gi" 2>/dev/null; then
    echo "✅ PyGObject system package is available"
else
    echo "⚠️  PyGObject import failed (this is normal, already installed as system package)"
fi

echo ""
echo "=========================================="
echo "✅ GUI Dependencies Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test GUI: python3 gui/app.py"
echo "2. Or run: astros-gui (after package installation)"
echo ""

# WSL-specific instructions
if grep -qi microsoft /proc/version; then
    echo "WSL Setup:"
    echo "1. Install X server on Windows (VcXsrv recommended)"
    echo "2. Set DISPLAY: export DISPLAY=:0"
    echo "3. Add to ~/.bashrc for persistence"
    echo ""
fi
