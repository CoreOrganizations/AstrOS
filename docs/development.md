# AstrOS Development Guide 🛠️

Welcome to the comprehensive AstrOS development guide! This document will help you set up a complete development environment for contributing to AstrOS.

## 📋 Table of Contents

- [System Requirements](#-system-requirements)
- [Quick Setup](#-quick-setup)
- [Manual Setup](#-manual-setup)
- [Development Workflow](#-development-workflow)
- [Testing](#-testing)
- [Building & Distribution](#-building--distribution)
- [IDE Configuration](#-ide-configuration)
- [Common Issues](#-common-issues)

---

## 🖥️ System Requirements

### Supported Operating Systems

**Primary Development Platform:**
- **Ubuntu 24.04 LTS** (recommended)
- **Ubuntu 22.04 LTS** (supported)

**Secondary Platforms:**
- **Pop!_OS 22.04+** (Ubuntu-based)
- **Linux Mint 21+** (Ubuntu-based)
- **Debian 12+** (testing support)

**Note**: While AstrOS may work on other Linux distributions, we primarily test and support Ubuntu LTS releases.

### Hardware Requirements

**Minimum:**
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 20 GB free space
- **Network**: Stable internet connection

**Recommended:**
- **CPU**: 4+ cores, 3.0+ GHz
- **RAM**: 8+ GB
- **Storage**: 50+ GB SSD
- **GPU**: NVIDIA/AMD with driver support (for AI features)

### Software Prerequisites

```bash
# Essential build tools
sudo apt update && sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Python development stack
sudo apt install -y \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    python3-pip \
    python3-setuptools

# System development libraries
sudo apt install -y \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev
```

---

## 🚀 Quick Setup

### Automated Development Environment

The easiest way to get started is using our automated setup script:

```bash
# Clone the repository
git clone https://github.com/AstrOS-Project/astros-core.git
cd astros-core

# Run automated setup
./scripts/setup-dev.sh

# Verify installation
python -m astros.agent --version
pytest tests/ -v
```

### What the Setup Script Does

1. **Environment Detection**: Checks OS, Python version, and dependencies
2. **Virtual Environment**: Creates isolated Python environment
3. **Dependencies**: Installs all development and runtime dependencies
4. **Pre-commit Hooks**: Sets up code quality checks
5. **Configuration**: Creates default development configuration
6. **Database**: Initializes local development database
7. **Services**: Sets up systemd services for development

---

## 🔧 Manual Setup

If you prefer manual setup or need to customize the installation:

### Step 1: Repository Setup

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/astros-core.git
cd astros-core

# Add upstream remote
git remote add upstream https://github.com/AstrOS-Project/astros-core.git

# Verify remotes
git remote -v
```

### Step 2: Python Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate environment
source venv/bin/activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install development dependencies
pip install -r requirements/dev.txt
pip install -e .
```

### Step 3: Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Test pre-commit setup
pre-commit run --all-files
```

### Step 4: Configuration

```bash
# Copy example configuration
cp config/dev.yaml.example config/dev.yaml

# Edit configuration for your setup
nano config/dev.yaml
```

### Step 5: Database Setup

```bash
# Initialize database
python scripts/init-db.py --dev

# Run migrations
alembic upgrade head

# Create test data (optional)
python scripts/create-test-data.py
```

### Step 6: Service Configuration

```bash
# Install systemd service for development
sudo cp scripts/astros-dev.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable astros-dev.service

# Start the service
sudo systemctl start astros-dev.service
```

---

## 🔄 Development Workflow

### Daily Development Routine

```bash
# Start your development session
cd astros-core
source venv/bin/activate

# Sync with upstream
git fetch upstream
git checkout develop
git merge upstream/develop

# Create feature branch
git checkout -b feature/your-feature-name

# Start development server
python -m astros.agent --config config/dev.yaml --debug

# In another terminal, run tests in watch mode
pytest-watch tests/
```

### Code Quality Checks

Run these before committing:

```bash
# Format code
black src/ tests/ scripts/
isort src/ tests/ scripts/

# Lint code
ruff check src/ tests/ scripts/
mypy src/

# Run tests
pytest tests/ --cov=src --cov-report=html

# Security check
bandit -r src/
safety check
```

### Plugin Development

```bash
# Create new plugin
python scripts/create-plugin.py --name my-awesome-plugin

# Install plugin in development mode
cd plugins/my-awesome-plugin
pip install -e .

# Test plugin
python -m astros.plugins.test my-awesome-plugin
```

---

## 🧪 Testing

### Test Categories

AstrOS has several types of tests:

1. **Unit Tests**: Fast, isolated component tests
2. **Integration Tests**: Test component interactions
3. **System Tests**: End-to-end functionality tests
4. **Performance Tests**: Benchmark critical paths
5. **Security Tests**: Vulnerability and penetration tests

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/unit/ -v              # Unit tests only
pytest tests/integration/ -v       # Integration tests only
pytest tests/system/ -v --slow     # System tests (slower)

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run performance tests
pytest tests/performance/ --benchmark-only

# Run security tests
pytest tests/security/ -v
```

### Test Configuration

```yaml
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --tb=short
    --cov-fail-under=80
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    system: marks tests as system tests
    benchmark: marks tests as benchmarks
```

### Writing Tests

```python
# Example unit test
import pytest
from astros.core.agent import AstrOSAgent
from astros.types import Intent, Response

class TestAstrOSAgent:
    @pytest.fixture
    def agent(self):
        return AstrOSAgent(config_path="config/test.yaml")
    
    def test_process_intent(self, agent):
        intent = Intent(
            text="show me my files",
            user_id="test_user",
            timestamp=datetime.now()
        )
        
        response = agent.process_intent(intent)
        
        assert response.success is True
        assert "files" in response.message.lower()
        assert len(response.data) > 0

    @pytest.mark.integration
    def test_plugin_loading(self, agent):
        # Integration test example
        plugins = agent.load_plugins()
        assert len(plugins) > 0
        assert "file-manager" in [p.name for p in plugins]
```

---

## 📦 Building & Distribution

### Development Builds

```bash
# Build wheel package
python -m build

# Install locally
pip install dist/astros-*.whl

# Create development ISO
./scripts/build-iso.sh --dev --output astros-dev.iso
```

### Release Builds

```bash
# Build for production
python -m build --wheel --sdist

# Build production ISO
./scripts/build-iso.sh --release --version 1.0.0

# Test ISO in VM
./scripts/test-iso.sh astros-ubuntu-24.04-1.0.0.iso
```

### Docker Development

```bash
# Build development container
docker build -f docker/Dockerfile.dev -t astros:dev .

# Run development container
docker run -it --rm \
    -v $(pwd):/workspace \
    -p 8000:8000 \
    astros:dev

# Run tests in container
docker run --rm astros:dev pytest tests/
```

---

## 💻 IDE Configuration

### VS Code Setup

Install recommended extensions:

```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.isort",
        "charliermarsh.ruff",
        "ms-python.mypy-type-checker",
        "ms-vscode.test-adapter-converter",
        "littlefoxteam.vscode-python-test-adapter",
        "ms-vscode.vscode-json"
    ]
}
```

VS Code settings (`.vscode/settings.json`):

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.linting.mypyEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### PyCharm Setup

1. **Interpreter**: Set to `./venv/bin/python`
2. **Code Style**: Import `.editorconfig` settings
3. **Run Configurations**: Create configurations for tests and main application
4. **Plugins**: Install Python, Docker, and Git plugins

### Vim/Neovim Setup

```lua
-- For Neovim with LSP
require('lspconfig').pyright.setup{
    settings = {
        python = {
            pythonPath = "./venv/bin/python",
        }
    }
}

-- For formatting
require('null-ls').setup({
    sources = {
        require('null-ls').builtins.formatting.black,
        require('null-ls').builtins.formatting.isort,
        require('null-ls').builtins.diagnostics.ruff,
    },
})
```

---

## ⚠️ Common Issues

### Installation Issues

**Problem**: `pip install` fails with compilation errors
```bash
# Solution: Install system dependencies
sudo apt install python3.12-dev build-essential libffi-dev libssl-dev
```

**Problem**: Virtual environment creation fails
```bash
# Solution: Install venv module
sudo apt install python3.12-venv
```

### Runtime Issues

**Problem**: `ModuleNotFoundError` for AstrOS modules
```bash
# Solution: Install in development mode
pip install -e .
```

**Problem**: Permission denied for systemd service
```bash
# Solution: Fix permissions and reload
sudo chown root:root /etc/systemd/system/astros-dev.service
sudo systemctl daemon-reload
```

### Development Issues

**Problem**: Pre-commit hooks fail
```bash
# Solution: Run hooks manually to see errors
pre-commit run --all-files -v
```

**Problem**: Database connection errors
```bash
# Solution: Reinitialize database
rm data/dev.db
python scripts/init-db.py --dev
```

**Problem**: Plugin loading failures
```bash
# Solution: Check plugin configuration and dependencies
python -m astros.plugins.validate --all
```

### Performance Issues

**Problem**: Slow test execution
```bash
# Solution: Run tests in parallel
pytest tests/ -n auto
```

**Problem**: High memory usage during development
```bash
# Solution: Configure garbage collection
export PYTHONHASHSEED=0
export MALLOC_ARENA_MAX=2
```

---

## 🔧 Advanced Configuration

### Environment Variables

```bash
# Development environment variables
export ASTROS_ENV=development
export ASTROS_DEBUG=true
export ASTROS_LOG_LEVEL=DEBUG
export ASTROS_CONFIG_PATH=config/dev.yaml

# AI API configurations
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here

# Database configuration
export ASTROS_DB_URL=sqlite:///data/dev.db

# Plugin development
export ASTROS_PLUGIN_PATH=plugins/
export ASTROS_PLUGIN_DEV_MODE=true
```

### Development Configuration

```yaml
# config/dev.yaml
app:
  name: "AstrOS Development"
  version: "dev"
  debug: true
  log_level: "DEBUG"

agent:
  name: "AstrOS Agent Dev"
  personality: "helpful_debug"
  response_timeout: 30
  max_retries: 3

ai:
  default_provider: "openai"
  providers:
    openai:
      api_key: "${OPENAI_API_KEY}"
      model: "gpt-4"
      max_tokens: 2000
    anthropic:
      api_key: "${ANTHROPIC_API_KEY}"
      model: "claude-3-haiku"

database:
  url: "sqlite:///data/dev.db"
  echo: true  # Log SQL queries
  pool_size: 5

plugins:
  auto_load: true
  development_mode: true
  paths:
    - "plugins/"
    - "/usr/local/lib/astros/plugins/"

logging:
  level: "DEBUG"
  format: "detailed"
  file: "logs/astros-dev.log"
  max_size: "100MB"
  backup_count: 5
```

---

## 📚 Additional Resources

### Documentation
- **[Plugin Development Guide](plugin-development.md)** - Create AstrOS plugins
- **[Architecture Overview](architecture.md)** - System design and components
- **[API Reference](api/)** - Complete API documentation
- **[Troubleshooting Guide](troubleshooting.md)** - Common issues and solutions

### Community
- **[Discord](https://discord.gg/astros)** - Real-time development chat
- **[GitHub Discussions](https://github.com/orgs/AstrOS-Project/discussions)** - Design discussions
- **[Matrix](https://matrix.to/#/#astros:matrix.org)** - Open protocol chat

### Tools & Resources
- **[Python 3.12 Documentation](https://docs.python.org/3.12/)**
- **[Ubuntu Development](https://ubuntu.com/desktop/developers)**
- **[systemd Service Documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)**

---

## 🎯 Next Steps

Now that you have your development environment set up:

1. **Read the [Plugin Development Guide](plugin-development.md)** to create your first plugin
2. **Join our [Discord](https://discord.gg/astros)** to connect with other developers
3. **Check [GitHub Issues](https://github.com/AstrOS-Project/astros-core/issues)** for contribution opportunities
4. **Review the [Architecture Guide](architecture.md)** to understand the system design

Happy coding! 🚀

---

<div align="center">

**Questions about development setup?**  
**💬 [Join Discord](https://discord.gg/astros)** • **📖 [Read More Docs](https://docs.astros.org)** • **🐛 [Report Issues](https://github.com/AstrOS-Project/astros-core/issues)**

*Made with ❤️ by the AstrOS community*

</div>