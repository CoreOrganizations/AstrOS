#!/bin/bash
# Installation script for AstrOS Agent Service

set -e

echo "🔧 Installing AstrOS Agent Service..."
echo "======================================"

# Determine the actual user (handle root and sudo cases)
if [ "$EUID" -eq 0 ]; then
    if [ -n "$SUDO_USER" ]; then
        USERNAME="$SUDO_USER"
        USER_HOME=$(eval echo ~$SUDO_USER)
        echo "📝 Installing for sudo user: $USERNAME"
    else
        # Running as root directly - use root
        USERNAME="root"
        USER_HOME="/root"
        echo "📝 Installing for user: root"
    fi
else
    USERNAME=$(whoami)
    USER_HOME="$HOME"
    echo "📝 Installing for user: $USERNAME"
fi

echo "🏠 Home directory: $USER_HOME"

# 1. Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p /usr/lib/astros/agent 2>/dev/null || sudo mkdir -p /usr/lib/astros/agent
mkdir -p $USER_HOME/.config/astros
mkdir -p $USER_HOME/.local/share/astros

# 2. Copy agent files
echo "📦 Copying agent files..."
sudo cp astros.py /usr/lib/astros/agent/
sudo cp astros_daemon.py /usr/lib/astros/agent/
sudo chown -R root:root /usr/lib/astros
sudo chmod 755 /usr/lib/astros/agent
sudo chmod 644 /usr/lib/astros/agent/*.py

# 3. Setup virtual environment
echo "🐍 Setting up virtual environment..."
if [ ! -d $USER_HOME/.local/share/astros/venv ]; then
    python3 -m venv $USER_HOME/.local/share/astros/venv
    source $USER_HOME/.local/share/astros/venv/bin/activate
    pip install --upgrade pip --quiet
    pip install httpx openai python-dotenv --quiet
    deactivate
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# 4. Setup environment configuration
if [ ! -f $USER_HOME/.config/astros/agent.env ]; then
    echo "📝 Creating environment configuration..."
    
    # Check if we have the current .env file
    if [ -f .env ]; then
        # Copy current .env as agent.env
        cp .env $USER_HOME/.config/astros/agent.env
        echo "✅ Copied existing .env configuration"
    else
        # Use template
        cp configs/agent.env.template $USER_HOME/.config/astros/agent.env
        echo "⚠️  Created from template - please add your API key!"
    fi
    
    chmod 600 $USER_HOME/.config/astros/agent.env
else
    echo "✅ Environment configuration already exists"
fi

# 5. Install systemd service
echo "🔧 Installing systemd service..."
sudo cp configs/astros-agent.service /etc/systemd/system/astros-agent@.service
sudo systemctl daemon-reload

# 6. Enable and start service
echo "🚀 Enabling service for user $USERNAME..."
sudo systemctl enable astros-agent@$USERNAME
sudo systemctl start astros-agent@$USERNAME

# Wait for service to start
sleep 2

# 7. Check service status
echo ""
echo "======================================"
echo "✅ Installation complete!"
echo ""
echo "Service Status:"
sudo systemctl status astros-agent@$USERNAME --no-pager || true

echo ""
echo "======================================"
echo "📝 Configuration:"
echo "   Config file: $USER_HOME/.config/astros/agent.env"
echo "   Virtual env: $USER_HOME/.local/share/astros/venv"
echo ""
echo "📝 Useful Commands:"
echo "   View logs:    journalctl -u astros-agent@$USERNAME -f"
echo "   Restart:      sudo systemctl restart astros-agent@$USERNAME"
echo "   Status:       sudo systemctl status astros-agent@$USERNAME"
echo "   Stop:         sudo systemctl stop astros-agent@$USERNAME"
echo "======================================"
