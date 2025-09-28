# Development Environment Setup Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Development Machine Setup](#development-machine-setup)
3. [Project Structure](#project-structure)
4. [Development Tools Configuration](#development-tools-configuration)
5. [Build Environment](#build-environment)
6. [Testing Setup](#testing-setup)
7. [IDE Configuration](#ide-configuration)
8. [Workflow Automation](#workflow-automation)
9. [Team Development](#team-development)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware Requirements
```yaml
Minimum Development Setup:
  CPU: 4 cores (Intel i5 or AMD Ryzen 5 equivalent)
  RAM: 8GB (16GB recommended)
  Storage: 100GB free space (SSD recommended)
  Network: Stable internet connection
  
Recommended Development Setup:
  CPU: 8+ cores (Intel i7/i9 or AMD Ryzen 7/9)
  RAM: 16GB+ (32GB for heavy AI development)
  Storage: 250GB+ free space on SSD
  GPU: CUDA-compatible for local AI model testing
  Network: High-speed internet for model downloads

ISO Building Requirements:
  Additional Storage: 50GB for ISO builds
  RAM: 16GB minimum for live-build
  VM Software: VirtualBox/VMware for testing
```

### Operating System Support
```bash
# Primary development platform (recommended)
Ubuntu 24.04 LTS
Ubuntu 22.04 LTS

# Supported alternative platforms
Debian 12 (Bookworm)
Fedora 39/40
Pop!_OS 22.04 LTS

# Development also possible on (with limitations)
Windows 11 (WSL2 required)
macOS (Docker required for ISO building)
```

---

## Development Machine Setup

### Initial System Setup
```bash
#!/bin/bash
# setup-dev-machine.sh - Initial development environment setup

set -e

echo "🚀 Setting up AstrOS development environment..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install essential development tools
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    tree \
    htop \
    jq \
    unzip

# Install Python development stack
sudo apt install -y \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    python3-pip \
    python3-wheel \
    python3-setuptools

# Install Ubuntu development tools
sudo apt install -y \
    ubuntu-dev-tools \
    devscripts \
    dh-make \
    build-essential \
    lintian \
    pbuilder

# Install ISO building tools
sudo apt install -y \
    debootstrap \
    squashfs-tools \
    genisoimage \
    syslinux-utils \
    isolinux \
    live-build \
    xorriso

# Install container tools
sudo apt install -y \
    docker.io \
    docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Install Node.js for web development
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install additional tools
sudo apt install -y \
    code \
    firefox \
    gitg \
    meld \
    virtualbox

echo "✅ Basic setup complete. Please reboot to apply group changes."
echo "🔄 Run 'newgrp docker' or logout/login to use Docker without sudo."
```

### Python Environment Setup
```bash
#!/bin/bash
# setup-python-env.sh - Python development environment

# Install Python version manager
curl https://pyenv.run | bash

# Add to shell configuration
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc

# Install Python 3.12
pyenv install 3.12.0
pyenv global 3.12.0

# Install pipx for global Python tools
python -m pip install --user pipx
python -m pipx ensurepath

# Install global development tools
pipx install poetry
pipx install black
pipx install isort
pipx install flake8
pipx install mypy
pipx install pre-commit
pipx install mkdocs
pipx install cookiecutter

echo "✅ Python environment setup complete"
```

---

## Project Structure

### Directory Layout
```
astros-project/
├── README.md
├── Local/                          # Private development docs (gitignored)
├── docs/                           # Public documentation
├── scripts/                        # Build and utility scripts
├── src/                           # Source code
│   ├── astros/                    # Main Python package
│   │   ├── __init__.py
│   │   ├── core/                  # Core agent functionality
│   │   ├── plugins/               # Plugin system
│   │   ├── ai/                    # AI integration
│   │   ├── system/                # System integration
│   │   └── ui/                    # User interface
│   └── extensions/                # GNOME Shell extensions
├── tests/                         # Test suite
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── performance/               # Performance tests
├── build/                         # Build artifacts (gitignored)
├── dist/                          # Distribution packages (gitignored)
├── config/                        # Configuration files
│   ├── development.yaml
│   ├── production.yaml
│   └── testing.yaml
├── deployment/                    # Deployment configurations
│   ├── docker/
│   ├── kubernetes/
│   └── systemd/
├── .github/                       # GitHub workflows and templates
├── requirements/                  # Dependency specifications
│   ├── base.txt
│   ├── development.txt
│   ├── testing.txt
│   └── production.txt
├── pyproject.toml                 # Python project configuration
├── Makefile                       # Build automation
├── docker-compose.yml             # Development containers
└── .gitignore                     # Git ignore rules
```

### Create Project Structure
```bash
#!/bin/bash
# create-project-structure.sh

mkdir -p astros-project
cd astros-project

# Create main directories
mkdir -p {src/astros/{core,plugins,ai,system,ui},tests/{unit,integration,performance}}
mkdir -p {docs,scripts,config,deployment/{docker,kubernetes,systemd}}
mkdir -p {build,dist,Local}
mkdir -p {requirements,.github/workflows}

# Create initial files
touch src/astros/__init__.py
touch src/astros/{core,plugins,ai,system,ui}/__init__.py

# Create basic configuration files
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "astros"
version = "0.1.0"
description = "AI-Integrated Operating System"
authors = [{name = "AstrOS Team", email = "team@astros.org"}]
license = {text = "Apache-2.0"}
readme = "README.md"
requires-python = ">=3.12"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.5.0",
    "asyncio-mqtt>=0.16.0",
    "transformers>=4.35.0",
    "torch>=2.1.0",
    "speechrecognition>=3.10.0",
    "pyttsx3>=2.90",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.10.0",
    "isort>=5.12.0",
    "flake8>=6.1.0",
    "mypy>=1.7.0",
    "pre-commit>=3.5.0",
]

[project.scripts]
astros = "astros.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src/astros --cov-report=html --cov-report=term"
EOF

# Create basic Makefile
cat > Makefile << 'EOF'
.PHONY: help install install-dev test test-cov lint format clean build iso

help:
	@echo "Available commands:"
	@echo "  install     - Install the package"
	@echo "  install-dev - Install in development mode with dev dependencies"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build the package"
	@echo "  iso         - Build AstrOS ISO"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=src/astros --cov-report=html --cov-report=term

lint:
	flake8 src tests
	mypy src
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -delete

build:
	python -m build

iso:
	./scripts/build-iso.sh
EOF

echo "✅ Project structure created successfully"
```

---

## Development Tools Configuration

### Git Configuration
```bash
#!/bin/bash
# configure-git.sh

# Global Git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor "code --wait"

# Set up Git aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitg'

# Configure GPG signing (optional but recommended)
echo "Setting up GPG key for commit signing..."
echo "Generate a GPG key with: gpg --full-generate-key"
echo "List keys with: gpg --list-secret-keys --keyid-format LONG"
echo "Set signing key with: git config --global user.signingkey [KEY_ID]"
echo "Enable signing with: git config --global commit.gpgsign true"
```

### Pre-commit Hooks Setup
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: mixed-line-ending

  - repo: https://github.com/psf/black
    rev: 23.10.1
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', 'src/']
        exclude: ^tests/
```

### Docker Development Environment
```yaml
# docker-compose.yml
version: '3.8'

services:
  astros-dev:
    build:
      context: .
      dockerfile: deployment/docker/Dockerfile.dev
    volumes:
      - .:/workspace
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - "8000:8000"  # FastAPI dev server
      - "5000:5000"  # Additional services
    environment:
      - PYTHONPATH=/workspace/src
      - ASTROS_ENV=development
    command: tail -f /dev/null  # Keep container running

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: astros_dev
      POSTGRES_USER: astros
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  redis_data:
  postgres_data:
```

```dockerfile
# deployment/docker/Dockerfile.dev
FROM ubuntu:24.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3-pip \
    python3-venv \
    build-essential \
    git \
    curl \
    vim \
    tree \
    htop \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
RUN python3.12 -m pip install --upgrade pip setuptools wheel

# Create development user
RUN useradd -m -s /bin/bash astros
USER astros
WORKDIR /home/astros

# Set up workspace
VOLUME /workspace
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]
```

---

## Build Environment

### Build Scripts
```bash
#!/bin/bash
# scripts/build-iso.sh - ISO building script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_ROOT/build/iso"
VERSION="${1:-dev-$(date +%Y%m%d)}"

echo "🏗️  Building AstrOS ISO v$VERSION"

# Clean previous builds
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# Configure live-build
lb config \
    --distribution noble \
    --archive-areas "main restricted universe multiverse" \
    --apt-recommends false \
    --apt-suggests false \
    --binary-images iso-hybrid \
    --bootappend-live "boot=live components quiet splash" \
    --debian-installer false \
    --iso-application "AstrOS" \
    --iso-publisher "AstrOS Project" \
    --iso-volume "AstrOS-$VERSION-amd64" \
    --memtest none

# Copy configuration
cp -r "$PROJECT_ROOT/config/live-build"/* config/ 2>/dev/null || true

# Create package lists
mkdir -p config/package-lists

cat > config/package-lists/astros.list.chroot << 'EOF'
# Desktop environment
ubuntu-desktop-minimal
gnome-shell
gnome-terminal
firefox
nautilus

# Development tools
python3.12
python3-pip
python3-venv
git
vim
curl
wget

# AstrOS dependencies
python3-dev
build-essential
portaudio19-dev
espeak-ng
alsa-utils
pulseaudio

# System tools
htop
tree
net-tools
openssh-client
EOF

# Create installation hooks
mkdir -p config/hooks/live

cat > config/hooks/live/0100-install-astros.hook.chroot << 'EOF'
#!/bin/bash
set -e

echo "Installing AstrOS components..."

# Install Python dependencies
pip3 install --break-system-packages \
    fastapi \
    uvicorn \
    transformers \
    torch \
    speechrecognition \
    pyttsx3

# Create AstrOS directories
mkdir -p /opt/astros
mkdir -p /etc/astros
mkdir -p /var/lib/astros
mkdir -p /var/log/astros

# Copy AstrOS source (this would be copied from the host)
# For now, create placeholder
echo "# AstrOS will be installed here" > /opt/astros/README.md

# Create systemd service
cat > /etc/systemd/system/astros-agent.service << 'SERVICE'
[Unit]
Description=AstrOS AI Agent
After=network.target sound.target

[Service]
Type=simple
User=astros
Group=astros
WorkingDirectory=/opt/astros
ExecStart=/usr/bin/python3 -m astros.agent
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Create AstrOS user
useradd -r -d /opt/astros -s /bin/false astros
chown -R astros:astros /opt/astros /var/lib/astros /var/log/astros

# Enable service (but don't start it)
systemctl enable astros-agent.service

echo "✅ AstrOS components installed"
EOF

chmod +x config/hooks/live/0100-install-astros.hook.chroot

# Build the ISO
echo "🚀 Starting ISO build..."
sudo lb build

# Check if build succeeded
if [ -f "live-image-amd64.hybrid.iso" ]; then
    mv "live-image-amd64.hybrid.iso" "../astros-$VERSION-amd64.iso"
    echo "✅ ISO build complete: build/astros-$VERSION-amd64.iso"
    
    # Generate checksums
    cd "$PROJECT_ROOT/build"
    sha256sum "astros-$VERSION-amd64.iso" > "astros-$VERSION-amd64.iso.sha256"
    echo "📋 Checksums generated"
else
    echo "❌ ISO build failed"
    exit 1
fi
```

### Automated Testing
```bash
#!/bin/bash
# scripts/test-iso.sh - ISO testing script

ISO_FILE="$1"
TEST_DIR="$(mktemp -d)"

if [ ! -f "$ISO_FILE" ]; then
    echo "❌ ISO file not found: $ISO_FILE"
    exit 1
fi

echo "🧪 Testing ISO: $ISO_FILE"

# Test 1: ISO integrity
echo "Checking ISO integrity..."
if file "$ISO_FILE" | grep -q "ISO 9660"; then
    echo "✅ ISO format valid"
else
    echo "❌ Invalid ISO format"
    exit 1
fi

# Test 2: Mount test
echo "Testing ISO mount..."
mkdir -p "$TEST_DIR/mount"
if sudo mount -o loop "$ISO_FILE" "$TEST_DIR/mount"; then
    echo "✅ ISO mounts successfully"
    
    # Check for required files
    if [ -f "$TEST_DIR/mount/casper/filesystem.squashfs" ]; then
        echo "✅ SquashFS filesystem found"
    else
        echo "❌ SquashFS filesystem missing"
        exit 1
    fi
    
    sudo umount "$TEST_DIR/mount"
else
    echo "❌ Failed to mount ISO"
    exit 1
fi

# Test 3: Boot test with QEMU (if available)
if command -v qemu-system-x86_64 >/dev/null; then
    echo "Testing boot with QEMU..."
    timeout 120 qemu-system-x86_64 \
        -m 2048 \
        -cdrom "$ISO_FILE" \
        -boot d \
        -display none \
        -serial stdio &
    
    QEMU_PID=$!
    sleep 60  # Wait for boot
    
    if kill -0 $QEMU_PID 2>/dev/null; then
        echo "✅ Boot test successful"
        kill $QEMU_PID
    else
        echo "❌ Boot test failed"
        exit 1
    fi
else
    echo "⚠️  QEMU not available, skipping boot test"
fi

# Cleanup
rm -rf "$TEST_DIR"
echo "✅ All tests passed"
```

---

## Testing Setup

### Test Configuration
```python
# tests/conftest.py - pytest configuration
import asyncio
import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from astros.core.agent import AstrOSAgent
from astros.core.config import Config


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def test_config(temp_dir: Path) -> Config:
    """Create a test configuration."""
    config_file = temp_dir / "test_config.yaml"
    config_content = """
agent:
  name: "Test Agent"
  log_level: "DEBUG"
  
ai:
  provider: "mock"
  local_models: true
  
plugins:
  enabled: []
  
storage:
  database_url: "sqlite:///:memory:"
  
logging:
  level: "DEBUG"
  file: null
"""
    config_file.write_text(config_content)
    return Config.from_file(config_file)


@pytest.fixture
async def agent(test_config: Config) -> AstrOSAgent:
    """Create a test agent instance."""
    agent = AstrOSAgent(test_config)
    await agent.initialize()
    yield agent
    await agent.shutdown()


@pytest.fixture
def client(agent: AstrOSAgent) -> TestClient:
    """Create a test client for the FastAPI app."""
    from astros.api.app import create_app
    
    app = create_app(agent)
    return TestClient(app)
```

### Example Tests
```python
# tests/unit/test_agent.py
import pytest

from astros.core.agent import AstrOSAgent
from astros.core.intent import Intent
from astros.core.response import Response


class TestAstrOSAgent:
    """Test the main AstrOS agent functionality."""
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent: AstrOSAgent):
        """Test that the agent initializes correctly."""
        assert agent is not None
        assert agent.config is not None
        assert agent.plugin_manager is not None
    
    @pytest.mark.asyncio
    async def test_simple_command_processing(self, agent: AstrOSAgent):
        """Test processing a simple command."""
        response = await agent.process_request("hello")
        
        assert isinstance(response, Response)
        assert response.success
        assert "hello" in response.message.lower()
    
    @pytest.mark.asyncio
    async def test_invalid_command_handling(self, agent: AstrOSAgent):
        """Test handling of invalid commands."""
        response = await agent.process_request("")
        
        assert isinstance(response, Response)
        assert not response.success
        assert "invalid" in response.message.lower()


# tests/integration/test_api.py
from fastapi.testclient import TestClient


class TestAPI:
    """Test the FastAPI integration."""
    
    def test_health_endpoint(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_process_command_endpoint(self, client: TestClient):
        """Test the command processing endpoint."""
        response = client.post(
            "/api/v1/process",
            json={"command": "hello"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["success"] is True
```

---

## IDE Configuration

### VS Code Setup
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/build": true,
        "**/dist": true,
        "**/.pytest_cache": true,
        "**/htmlcov": true
    }
}
```

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "AstrOS Agent",
            "type": "python",
            "request": "launch",
            "module": "astros.agent",
            "args": ["--config", "config/development.yaml"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        },
        {
            "name": "Run Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.isort",
        "ms-python.flake8",
        "ms-python.mypy-type-checker",
        "ms-vscode.vscode-json",
        "redhat.vscode-yaml",
        "ms-vscode.makefile-tools",
        "ms-vscode-remote.remote-containers",
        "github.vscode-pull-request-github"
    ]
}
```

---

## Workflow Automation

### Development Workflow
```bash
#!/bin/bash
# scripts/dev-workflow.sh - Daily development workflow

echo "🚀 Starting AstrOS development workflow"

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Update dependencies
echo "📦 Updating dependencies..."
pip install -e ".[dev]"

# Run pre-commit hooks
echo "🔍 Running pre-commit checks..."
pre-commit run --all-files

# Run tests
echo "🧪 Running tests..."
make test-cov

# Check code quality
echo "📊 Checking code quality..."
make lint

# Start development server
echo "🖥️  Starting development server..."
python -m astros.agent --config config/development.yaml
```

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Run pre-commit
      uses: pre-commit/action@v3.0.0
    
    - name: Run tests
      run: |
        pytest --cov=src/astros --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  build-iso:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install ISO build dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y live-build debootstrap squashfs-tools
    
    - name: Build ISO
      run: |
        ./scripts/build-iso.sh
    
    - name: Test ISO
      run: |
        ./scripts/test-iso.sh build/astros-*.iso
    
    - name: Upload ISO artifact
      uses: actions/upload-artifact@v3
      with:
        name: astros-iso
        path: build/astros-*.iso*
```

---

## Team Development

### Development Guidelines
```yaml
Team Development Standards:
  Code Review Process:
    - All changes require peer review
    - Minimum one approving review for merge
    - Address all review comments before merge
    - Maintain civil and constructive feedback
  
  Branch Strategy:
    - main: Stable release branch
    - develop: Integration branch for features
    - feature/*: Individual feature development
    - hotfix/*: Critical fixes for releases
  
  Commit Standards:
    - Use conventional commit format
    - Include meaningful commit messages
    - Keep commits atomic and focused
    - Sign commits with GPG key
  
  Pull Request Guidelines:
    - Use PR template
    - Include comprehensive description
    - Link related issues
    - Ensure CI passes
    - Update documentation as needed
```

### Team Onboarding
```bash
#!/bin/bash
# scripts/onboard-developer.sh - New team member setup

echo "👋 Welcome to the AstrOS development team!"

# Clone repository
echo "📥 Cloning repository..."
git clone https://github.com/CoreOrganizations/AstrOS.git
cd AstrOS

# Set up development environment
echo "🛠️  Setting up development environment..."
./scripts/setup-dev-machine.sh

# Install project dependencies
echo "📦 Installing project dependencies..."
make install-dev

# Run initial tests
echo "🧪 Running tests to verify setup..."
make test

# Create development branch
echo "🌿 Creating development branch..."
git checkout -b "onboarding/$(whoami)"

echo "✅ Setup complete! You're ready to contribute to AstrOS."
echo "📚 Next steps:"
echo "  1. Read the contributing guidelines: CONTRIBUTING.md"
echo "  2. Browse good first issues: https://github.com/CoreOrganizations/AstrOS/labels/good%20first%20issue"
echo "  3. Join our Discord: https://discord.gg/astros"
echo "  4. Attend the next team meeting"
```

---

## Troubleshooting

### Common Issues and Solutions
```yaml
Development Environment Issues:
  Python Version Conflicts:
    Problem: "ModuleNotFoundError or compatibility issues"
    Solution: |
      - Use pyenv to manage Python versions
      - Ensure Python 3.12+ is being used
      - Recreate virtual environment if needed
  
  Permission Errors:
    Problem: "Permission denied when building ISO"
    Solution: |
      - Add user to docker group: sudo usermod -aG docker $USER
      - Use sudo for live-build commands
      - Check file permissions in project directory
  
  Build Failures:
    Problem: "ISO build fails with package errors"
    Solution: |
      - Update package lists: sudo apt update
      - Check network connectivity
      - Verify Ubuntu mirror accessibility
      - Clear build cache: rm -rf build/
  
  Test Failures:
    Problem: "Tests fail in CI but pass locally"
    Solution: |
      - Check Python version consistency
      - Verify all dependencies are in requirements files
      - Test in clean environment using Docker
      - Check for environment variable differences

IDE Configuration Issues:
  VS Code Python Path:
    Problem: "VS Code can't find Python interpreter"
    Solution: |
      - Set python.defaultInterpreterPath in settings
      - Reload VS Code window
      - Check virtual environment activation
  
  Import Resolution:
    Problem: "Import errors in IDE but code runs fine"
    Solution: |
      - Set PYTHONPATH to src/ directory
      - Configure IDE workspace settings
      - Install package in development mode
```

### Diagnostic Commands
```bash
#!/bin/bash
# scripts/diagnose-env.sh - Environment diagnostics

echo "🔍 AstrOS Development Environment Diagnostics"
echo "=============================================="

echo "System Information:"
echo "OS: $(lsb_release -d | cut -f2)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo ""

echo "Python Environment:"
echo "Python Version: $(python3 --version)"
echo "Python Path: $(which python3)"
echo "Pip Version: $(pip3 --version)"
echo "Virtual Environment: ${VIRTUAL_ENV:-Not activated}"
echo ""

echo "Git Configuration:"
echo "Git Version: $(git --version)"
echo "User Name: $(git config user.name)"
echo "User Email: $(git config user.email)"
echo "Current Branch: $(git branch --show-current 2>/dev/null || echo 'Not in git repo')"
echo ""

echo "Docker Status:"
if command -v docker >/dev/null; then
    echo "Docker Version: $(docker --version)"
    echo "Docker Status: $(systemctl is-active docker)"
    echo "Docker Group: $(groups | grep -o docker || echo 'Not in docker group')"
else
    echo "Docker: Not installed"
fi
echo ""

echo "Build Tools:"
echo "Live-build: $(lb --version 2>/dev/null || echo 'Not installed')"
echo "Make: $(make --version | head -1)"
echo "GCC: $(gcc --version | head -1)"
echo ""

echo "Project Status:"
if [ -f "pyproject.toml" ]; then
    echo "Project Config: Found"
    echo "Virtual Environment: $([ -d venv ] && echo 'Found' || echo 'Not found')"
    echo "Dependencies Installed: $(pip list | grep astros | head -1 || echo 'Not installed')"
else
    echo "Project Config: Not found (not in project directory?)"
fi
```

---

## Quick Reference

### Essential Commands
```bash
# Setup
make install-dev          # Install development dependencies
make format               # Format code
make lint                 # Check code quality
make test                 # Run tests

# Development
python -m astros.agent    # Start agent
./scripts/build-iso.sh    # Build ISO
./scripts/test-iso.sh     # Test ISO
docker-compose up         # Start development services

# Git workflow
git checkout -b feature/my-feature  # Create feature branch
git add .                          # Stage changes
git commit -m "feat: add feature"  # Commit changes
git push origin feature/my-feature # Push branch
gh pr create                       # Create pull request

# Troubleshooting
./scripts/diagnose-env.sh  # Check environment
make clean                 # Clean build artifacts
pip install -e ".[dev]"   # Reinstall in dev mode
```

This comprehensive setup ensures a consistent, productive development environment for all team members working on AstrOS. The automation and tooling will help maintain code quality while making development workflows efficient and enjoyable.