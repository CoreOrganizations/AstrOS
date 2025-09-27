# AstrOS Troubleshooting Guide 🔧

Comprehensive troubleshooting guide for common AstrOS issues and their solutions.

## 📋 Table of Contents

- [Quick Diagnostics](#-quick-diagnostics)
- [Installation Issues](#-installation-issues)
- [Development Environment](#-development-environment)
- [Runtime Problems](#-runtime-problems)
- [Plugin Issues](#-plugin-issues)
- [Performance Problems](#-performance-problems)
- [AI Integration Issues](#-ai-integration-issues)
- [System Integration](#-system-integration)
- [Database Issues](#-database-issues)
- [Getting Help](#-getting-help)

---

## 🚀 Quick Diagnostics

### System Health Check

Run these commands to quickly assess system health:

```bash
# Check AstrOS service status
sudo systemctl status astros

# Check logs for errors
journalctl -u astros -f --no-pager

# Test basic functionality
python -m astros.agent --test

# Check plugin status
python -m astros.plugins --list --status

# Verify configuration
python -m astros.config --validate
```

### Common Status Indicators

| Status | Meaning | Action |
|--------|---------|--------|
| 🟢 Active | System running normally | No action needed |
| 🟡 Starting | System initializing | Wait 30-60 seconds |
| 🟠 Warning | Non-critical issues | Check logs |
| 🔴 Failed | System not working | Follow troubleshooting steps |

---

## 💾 Installation Issues

### Ubuntu Version Compatibility

**Problem**: AstrOS won't install on your Ubuntu version
```bash
# Check Ubuntu version
lsb_release -a

# Expected output:
# Ubuntu 24.04.1 LTS (recommended)
# Ubuntu 22.04.3 LTS (supported)
```

**Solution**:
```bash
# For Ubuntu 22.04 (if you can't upgrade)
sudo add-apt-repository ppa:astros/ubuntu22-compat
sudo apt update

# For other distributions
# Use Docker installation instead
docker run -d --name astros astros/astros:latest
```

### Python Version Issues

**Problem**: Wrong Python version installed

```bash
# Check Python version
python3 --version
# Should be Python 3.12.x

# If wrong version:
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
```

### Package Installation Failures

**Problem**: `pip install` fails with compilation errors

```bash
# Install system dependencies first
sudo apt update && sudo apt install -y \
    build-essential \
    python3.12-dev \
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

# Clear pip cache and retry
pip cache purge
pip install --no-cache-dir astros
```

### Permission Issues

**Problem**: Permission denied during installation

```bash
# Don't use sudo with pip - use virtual environment instead
python3.12 -m venv astros-env
source astros-env/bin/activate
pip install astros

# Or install user-wide
pip install --user astros
```

---

## 🛠️ Development Environment

### Virtual Environment Problems

**Problem**: Virtual environment not working

```bash
# Remove old environment
rm -rf venv/

# Create fresh environment
python3.12 -m venv venv
source venv/bin/activate

# Verify activation
which python
# Should show: /path/to/your/project/venv/bin/python

# Install requirements
pip install --upgrade pip setuptools wheel
pip install -r requirements/dev.txt
pip install -e .
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'astros'`

```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Install in development mode
pip install -e .

# Verify installation
python -c "import astros; print(astros.__version__)"

# If still failing, check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Pre-commit Hook Failures

**Problem**: Pre-commit hooks fail or aren't running

```bash
# Reinstall pre-commit hooks
pre-commit uninstall
pre-commit install

# Update hooks
pre-commit autoupdate

# Run hooks manually to see errors
pre-commit run --all-files

# Common fixes:
black src/ tests/
ruff check src/ tests/ --fix
mypy src/
```

### Testing Issues

**Problem**: Tests fail or don't run

```bash
# Install test dependencies
pip install -r requirements/test.txt

# Run tests with verbose output
pytest tests/ -v -s

# Run specific test
pytest tests/test_specific.py -v

# Check test coverage
pytest tests/ --cov=src --cov-report=html
```

---

## ⚡ Runtime Problems

### Service Won't Start

**Problem**: AstrOS agent service fails to start

```bash
# Check detailed logs
sudo journalctl -u astros -n 50 --no-pager

# Common issues and fixes:

# 1. Configuration file not found
sudo mkdir -p /etc/astros
sudo cp config/production.yaml /etc/astros/astros.yaml

# 2. Permission issues
sudo chown astros:astros /etc/astros/astros.yaml
sudo chmod 644 /etc/astros/astros.yaml

# 3. Database connection
sudo -u astros astros-db init

# 4. Start manually for debugging
sudo -u astros /opt/astros/venv/bin/python -m astros.agent --debug
```

### High CPU Usage

**Problem**: AstrOS consuming too much CPU

```bash
# Check what's using CPU
top -p $(pgrep -f astros)

# Check for infinite loops in logs
tail -f /var/log/astros/astros.log | grep -E "(ERROR|WARNING)"

# Reduce AI processing load
# Edit /etc/astros/astros.yaml:
ai:
  batch_size: 1  # Reduce from default
  timeout: 30    # Add timeout
  
plugins:
  max_concurrent: 2  # Limit concurrent plugins
```

### Memory Issues

**Problem**: AstrOS using too much memory

```bash
# Check memory usage
ps aux | grep astros

# Monitor memory over time
watch 'ps -p $(pgrep -f astros) -o pid,ppid,cmd,%mem,%cpu'

# Optimize configuration
# Edit /etc/astros/astros.yaml:
database:
  pool_size: 5      # Reduce from default 10
  
cache:
  max_size: 100MB   # Limit cache size
  
ai:
  max_context_length: 2048  # Reduce context window
```

### Response Timeouts

**Problem**: Requests time out or are very slow

```bash
# Check response times in logs
grep "Response time" /var/log/astros/astros.log

# Increase timeouts in config
plugins:
  default_timeout: 60  # Increase from 30 seconds
  
ai:
  request_timeout: 45  # Increase AI timeout

# Check network connectivity to AI providers
curl -I https://api.openai.com
curl -I https://api.anthropic.com
```

---

## 🧩 Plugin Issues

### Plugin Won't Load

**Problem**: Plugin fails to load at startup

```bash
# Check plugin logs
python -m astros.plugins --validate my-plugin

# Common issues:

# 1. Missing dependencies
cd plugins/my-plugin
pip install -r requirements.txt

# 2. Syntax errors
python -m py_compile src/main.py

# 3. Plugin configuration
# Check plugin.yaml syntax:
python -c "import yaml; yaml.safe_load(open('plugin.yaml'))"

# 4. Permissions
sudo chown -R astros:astros /opt/astros/plugins/my-plugin
```

### Plugin Crashes

**Problem**: Plugin crashes during execution

```bash
# Enable plugin debugging
export ASTROS_PLUGIN_DEBUG=true
export ASTROS_LOG_LEVEL=DEBUG

# Run with stack traces
python -m astros.agent --debug --traceback

# Check plugin isolation
python -m astros.plugins --test my-plugin --isolated

# Validate plugin resources
python -m astros.plugins --check-resources my-plugin
```

### Plugin Communication Issues

**Problem**: Plugins can't communicate with each other

```bash
# Check plugin bus status
python -c "
from astros.plugins import PluginBus
bus = PluginBus()
print(bus.get_status())
"

# Test plugin messaging
python -m astros.plugins --test-communication

# Check permissions
# Ensure plugins have 'plugin_communication' permission
```

### Plugin Performance

**Problem**: Plugin is slow or unresponsive

```bash
# Profile plugin performance
python -m astros.plugins --profile my-plugin

# Check resource usage
python -m astros.plugins --monitor my-plugin

# Common optimizations:
# 1. Add caching to plugin
# 2. Use async/await properly
# 3. Optimize database queries
# 4. Reduce AI API calls
```

---

## 🚀 Performance Problems

### Slow Response Times

**Problem**: AstrOS takes too long to respond

**Diagnosis**:
```bash
# Enable performance monitoring
export ASTROS_PERF_MONITOR=true

# Check response time breakdown
grep "timing" /var/log/astros/astros.log | tail -20

# Profile the system
python -m astros.agent --profile
```

**Solutions**:
```yaml
# Optimize configuration (astros.yaml)
cache:
  enabled: true
  redis_url: "redis://localhost:6379"
  default_ttl: 3600

ai:
  provider_selection: "fast"  # Prefer faster models
  max_parallel_requests: 3
  
plugins:
  lazy_loading: true
  max_concurrent: 5
```

### Database Performance

**Problem**: Database queries are slow

```bash
# Check database performance
python -c "
from astros.storage import DatabaseManager
db = DatabaseManager()
db.analyze_performance()
"

# Optimize SQLite (if using SQLite)
sqlite3 /opt/astros/data/astros.db <<EOF
PRAGMA optimize;
PRAGMA analysis_limit=1000;
ANALYZE;
EOF

# For PostgreSQL
psql -d astros -c "ANALYZE;"
psql -d astros -c "REINDEX DATABASE astros;"
```

### Memory Leaks

**Problem**: Memory usage grows over time

```bash
# Monitor memory growth
python -m astros.debug --memory-monitor &

# Check for leaks in plugins
python -m astros.plugins --memory-check --all

# Common fixes:
# 1. Clear caches periodically
# 2. Close database connections
# 3. Clean up AI model contexts
# 4. Fix circular references in plugins
```

---

## 🤖 AI Integration Issues

### API Key Problems

**Problem**: AI provider authentication fails

```bash
# Check API key configuration
python -c "
import os
print('OpenAI key:', 'OPENAI_API_KEY' in os.environ)
print('Anthropic key:', 'ANTHROPIC_API_KEY' in os.environ)
"

# Test API connectivity
python -c "
from astros.ai import AIProvider
provider = AIProvider('openai')
result = provider.test_connection()
print(result)
"

# Common fixes:
export OPENAI_API_KEY="your-api-key-here"
export ANTHROPIC_API_KEY="your-api-key-here"

# Or set in config file:
# astros.yaml
ai:
  providers:
    openai:
      api_key: "your-key-here"
```

### Model Loading Issues

**Problem**: Local AI models won't load

```bash
# Check model file exists and permissions
ls -la /opt/astros/models/
file /opt/astros/models/llama-2-7b.gguf

# Test model loading
python -c "
from astros.ai.local import LocalAIProvider
provider = LocalAIProvider({
    'model_path': '/opt/astros/models/llama-2-7b.gguf'
})
print(provider.test_model())
"

# Common fixes:
# 1. Download correct model format
# 2. Check available disk space
# 3. Verify model file integrity
# 4. Install required dependencies (llama-cpp-python)
```

### Rate Limiting

**Problem**: AI API rate limits exceeded

```bash
# Check rate limit status
python -m astros.ai --check-limits

# Configure rate limiting
# astros.yaml
ai:
  rate_limiting:
    openai:
      requests_per_minute: 60
      tokens_per_minute: 10000
    anthropic:
      requests_per_minute: 20
      
  retry_policy:
    max_retries: 3
    backoff_factor: 2
```

---

## 🔗 System Integration

### D-Bus Connection Issues

**Problem**: Can't connect to system D-Bus

```bash
# Check D-Bus service status
systemctl status dbus

# Test D-Bus connection
python -c "
import dbus
bus = dbus.SystemBus()
print('D-Bus connection successful')
"

# Fix permissions
sudo usermod -a -G dbus astros

# Restart D-Bus (if necessary)
sudo systemctl restart dbus
```

### File System Permissions

**Problem**: Can't access user files

```bash
# Check AstrOS user permissions
id astros

# Add to necessary groups
sudo usermod -a -G users astros

# Fix file permissions
sudo chmod -R 755 /home/user/Documents
sudo chown -R user:astros /home/user/Documents

# Use ACLs for fine-grained control
sudo setfacl -R -m u:astros:rx /home/user/Documents
```

### Network Connectivity

**Problem**: Can't connect to external services

```bash
# Test network connectivity
curl -I https://api.openai.com
curl -I https://registry.astros.org

# Check firewall rules
sudo ufw status
sudo iptables -L

# Check DNS resolution
nslookup api.openai.com
dig api.openai.com

# Common fixes:
# 1. Configure proxy if needed
# 2. Open firewall ports
# 3. Check /etc/hosts
# 4. Verify network interfaces
```

---

## 💾 Database Issues

### Connection Problems

**Problem**: Can't connect to database

```bash
# Check database service
sudo systemctl status postgresql  # or mysql

# Test connection
python -c "
from astros.storage import DatabaseManager
db = DatabaseManager()
db.test_connection()
"

# Check configuration
cat /etc/astros/astros.yaml | grep -A 10 database:

# Common fixes:
# 1. Start database service
# 2. Create database and user
# 3. Update connection string
# 4. Check firewall/network
```

### Migration Issues

**Problem**: Database migrations fail

```bash
# Check migration status
python -m astros.db --migration-status

# Run migrations manually
python -m astros.db --migrate

# Reset migrations (CAUTION: DATA LOSS)
python -m astros.db --reset-migrations

# Check for conflicts
python -m astros.db --check-conflicts
```

### Performance Issues

**Problem**: Database queries are slow

```bash
# Analyze slow queries
python -m astros.db --analyze-slow-queries

# Optimize indexes
python -m astros.db --optimize-indexes

# For SQLite:
sqlite3 astros.db "PRAGMA optimize;"

# For PostgreSQL:
psql -d astros -c "VACUUM ANALYZE;"
```

---

## 🔍 Advanced Debugging

### Debug Mode

Enable comprehensive debugging:

```bash
# Environment variables
export ASTROS_DEBUG=true
export ASTROS_LOG_LEVEL=DEBUG
export ASTROS_TRACE=true

# Start with debugging
python -m astros.agent --debug --verbose --trace

# Debug specific components
python -m astros.plugins --debug my-plugin
python -m astros.ai --debug --test-providers
```

### Log Analysis

```bash
# Real-time log monitoring
tail -f /var/log/astros/astros.log | grep ERROR

# Search for specific issues
grep -n "PermissionError" /var/log/astros/astros.log
grep -A 5 -B 5 "timeout" /var/log/astros/astros.log

# Analyze log patterns
python -c "
import re
with open('/var/log/astros/astros.log') as f:
    errors = re.findall(r'ERROR.*', f.read())
    for error in set(errors):
        print(error)
"
```

### System State Inspection

```bash
# Check system state
python -c "
from astros.core import AstrOSAgent
agent = AstrOSAgent()
print(agent.get_debug_info())
"

# Inspect plugin states
python -m astros.plugins --inspect-all

# Check resource usage
python -m astros.debug --system-info
```

---

## 📞 Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Search existing issues**: [GitHub Issues](https://github.com/AstrOS-Project/astros-core/issues)
3. **Gather diagnostic information**:

```bash
# Run diagnostic script
python -m astros.debug --full-report > astros-debug.txt

# Include in your help request:
# - AstrOS version
# - Ubuntu version
# - Error messages
# - Steps to reproduce
# - Configuration (without API keys!)
```

### Community Support

- **💬 Discord**: [Join our server](https://discord.gg/astros) for real-time help
- **📋 GitHub Discussions**: [Ask questions](https://github.com/orgs/AstrOS-Project/discussions)
- **🌐 Matrix**: [Open protocol chat](https://matrix.to/#/#astros:matrix.org)

### Reporting Bugs

When reporting bugs, include:

1. **System Information**:
   ```bash
   astros --version
   lsb_release -a
   python3 --version
   ```

2. **Error Messages**: Full error messages and stack traces

3. **Reproduction Steps**: Exact steps to reproduce the issue

4. **Configuration**: Relevant config (remove API keys!)

5. **Logs**: Recent log entries showing the problem

### Getting Priority Support

- **Commercial Support**: Available for enterprise users
- **Consulting**: Architecture and deployment consulting
- **Training**: Custom training for teams

Contact: support@astros.org

---

## 🔧 Maintenance Tasks

### Regular Maintenance

```bash
# Weekly maintenance script
#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Restart AstrOS service
sudo systemctl restart astros

# Clean up logs older than 30 days
find /var/log/astros -name "*.log" -mtime +30 -delete

# Optimize database
python -m astros.db --optimize

# Clear old caches
python -m astros.cache --cleanup

# Check for plugin updates
python -m astros.plugins --check-updates
```

### Health Monitoring

```bash
# Set up monitoring (add to crontab)
*/5 * * * * /usr/local/bin/astros-health-check.sh
```

```bash
#!/bin/bash
# astros-health-check.sh

SERVICE_STATUS=$(systemctl is-active astros)
if [ "$SERVICE_STATUS" != "active" ]; then
    echo "$(date): AstrOS service is $SERVICE_STATUS" >> /var/log/astros-health.log
    systemctl restart astros
fi

# Check memory usage
MEMORY_USAGE=$(ps -p $(pgrep -f astros) -o %mem --no-headers | awk '{sum+=$1} END {print sum}')
if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "$(date): High memory usage: $MEMORY_USAGE%" >> /var/log/astros-health.log
fi
```

---

<div align="center">

### 🆘 Still Need Help?

**[💬 Join Discord](https://discord.gg/astros)** • **[📋 Create Issue](https://github.com/AstrOS-Project/astros-core/issues/new)** • **[📖 Read Docs](../README.md)**

*Don't give up! The community is here to help you succeed with AstrOS.*

</div>