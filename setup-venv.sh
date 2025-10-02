#!/bin/bash
# Setup script for AstrOS Agent development environment

set -e

echo "🔧 Setting up AstrOS Agent virtual environment..."
echo "=================================================="

# Check if Python 3.12+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment
VENV_PATH="$HOME/.local/share/astros/venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "📦 Creating virtual environment at $VENV_PATH..."
    mkdir -p "$HOME/.local/share/astros"
    python3 -m venv "$VENV_PATH"
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate and install dependencies
echo "📦 Installing dependencies..."
source "$VENV_PATH/bin/activate"

pip install --upgrade pip setuptools wheel
pip install httpx openai python-dotenv

echo ""
echo "✅ Setup complete!"
echo ""
echo "=================================================="
echo "To activate the environment manually:"
echo "  source $VENV_PATH/bin/activate"
echo ""
echo "To test the agent:"
echo "  source $VENV_PATH/bin/activate"
echo "  python3 astros_daemon.py"
echo "=================================================="
