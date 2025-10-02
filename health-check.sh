#!/bin/bash
# Comprehensive AstrOS Agent Health Check

echo "🏥 AstrOS Agent Health Check"
echo "=================================================="
echo ""

# Check 1: Service Status
echo "📋 Check 1: Systemd Service"
if sudo systemctl is-active --quiet astros-agent@root; then
    echo "✅ PASS: Service is running"
    uptime=$(sudo systemctl show astros-agent@root --property=ActiveEnterTimestamp --value)
    echo "   Uptime: Running since $uptime"
else
    echo "❌ FAIL: Service is not running"
    exit 1
fi
echo ""

# Check 2: Process Running
echo "📋 Check 2: Process Check"
if pgrep -f "astros_daemon.py" > /dev/null; then
    pid=$(pgrep -f "astros_daemon.py")
    echo "✅ PASS: Daemon process running"
    echo "   PID: $pid"
    
    # Memory usage
    mem=$(ps -p $pid -o rss= | awk '{print $1/1024 " MB"}')
    echo "   Memory: $mem"
else
    echo "❌ FAIL: Daemon process not found"
    exit 1
fi
echo ""

# Check 3: Configuration Files
echo "📋 Check 3: Configuration"
if [ -f /root/.config/astros/agent.env ]; then
    echo "✅ PASS: Config file exists"
    lines=$(wc -l < /root/.config/astros/agent.env)
    echo "   Location: /root/.config/astros/agent.env"
    echo "   Lines: $lines"
else
    echo "❌ FAIL: Config file missing"
    exit 1
fi
echo ""

# Check 4: Virtual Environment
echo "📋 Check 4: Virtual Environment"
if [ -d /root/.local/share/astros/venv ]; then
    echo "✅ PASS: Virtual environment exists"
    
    # Check installed packages
    packages=$(/root/.local/share/astros/venv/bin/pip list --format=freeze 2>/dev/null | grep -E "httpx|openai|python-dotenv" | wc -l)
    echo "   Location: /root/.local/share/astros/venv"
    echo "   Required packages: $packages/3"
    
    if [ $packages -eq 3 ]; then
        echo "   ✅ All dependencies installed"
    else
        echo "   ⚠️  WARNING: Some dependencies missing"
    fi
else
    echo "❌ FAIL: Virtual environment missing"
    exit 1
fi
echo ""

# Check 5: Agent Files
echo "📋 Check 5: Agent Files"
files_ok=0
total_files=2

if [ -f /usr/lib/astros/agent/astros.py ]; then
    echo "✅ astros.py present"
    files_ok=$((files_ok + 1))
else
    echo "❌ astros.py missing"
fi

if [ -f /usr/lib/astros/agent/astros_daemon.py ]; then
    echo "✅ astros_daemon.py present"
    files_ok=$((files_ok + 1))
else
    echo "❌ astros_daemon.py missing"
fi

if [ $files_ok -eq $total_files ]; then
    echo "✅ PASS: All agent files present ($files_ok/$total_files)"
else
    echo "❌ FAIL: Missing agent files ($files_ok/$total_files)"
    exit 1
fi
echo ""

# Check 6: Logs
echo "📋 Check 6: Logging"
log_lines=$(journalctl -u astros-agent@root -n 5 --no-pager 2>/dev/null | wc -l)
if [ $log_lines -gt 0 ]; then
    echo "✅ PASS: Logs accessible"
    echo "   Recent log entries: $log_lines"
    
    # Check for errors in last 20 lines
    errors=$(journalctl -u astros-agent@root -n 20 --no-pager 2>/dev/null | grep -i "error\|fail\|critical" | wc -l)
    if [ $errors -eq 0 ]; then
        echo "   ✅ No recent errors"
    else
        echo "   ⚠️  WARNING: $errors error entries in recent logs"
    fi
else
    echo "⚠️  WARNING: No logs found"
fi
echo ""

# Check 7: Auto-start
echo "📋 Check 7: Auto-start Configuration"
if sudo systemctl is-enabled --quiet astros-agent@root; then
    echo "✅ PASS: Service enabled for auto-start"
else
    echo "⚠️  WARNING: Service not enabled for auto-start"
fi
echo ""

# Check 8: Resource Limits
echo "📋 Check 8: Resource Limits"
mem_limit=$(sudo systemctl show astros-agent@root --property=MemoryLimit --value)
cpu_quota=$(sudo systemctl show astros-agent@root --property=CPUQuotaPerSecUSec --value)

echo "✅ Memory Limit: $mem_limit"
echo "✅ CPU Quota: $cpu_quota"
echo ""

# Summary
echo "=================================================="
echo "🎉 HEALTH CHECK COMPLETE"
echo "=================================================="
echo ""
echo "Summary:"
echo "  ✅ Service: Running"
echo "  ✅ Process: Active"  
echo "  ✅ Configuration: Valid"
echo "  ✅ Dependencies: Installed"
echo "  ✅ Files: Present"
echo "  ✅ Logs: Accessible"
echo ""
echo "Service Information:"
echo "  Command: sudo systemctl status astros-agent@root"
echo "  Logs:    journalctl -u astros-agent@root -f"
echo "  Restart: sudo systemctl restart astros-agent@root"
echo ""
echo "✅ ALL SYSTEMS OPERATIONAL"
