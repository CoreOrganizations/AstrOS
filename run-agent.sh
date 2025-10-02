#!/bin/bash
# Quick run script for AstrOS Agent (uses virtual environment)

VENV_PATH="$HOME/.local/share/astros/venv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: ./setup-venv.sh"
    exit 1
fi

# Activate venv and run daemon
echo "🚀 Starting AstrOS Agent..."
source "$VENV_PATH/bin/activate"
cd "$SCRIPT_DIR"
python3 astros_daemon.py
