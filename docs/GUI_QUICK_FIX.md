# GUI Quick Fix Guide

## Issues Found

1. **PyGObject installation failed** - Missing `girepository-2.0` development files
2. **GUI using system Python** - Should use virtualenv Python
3. **Import errors** - Wrong path for astros module

## Quick Fix

Run this single command:
```bash
cd /mnt/d/AstrOS
./fix-gui.sh
```

This will:
- Install missing `libgirepository1.0-dev`
- Verify all GTK4 dependencies
- Setup proper launcher script
- Check DISPLAY variable

## Then Launch

```bash
# Option 1: Use launcher (recommended)
./astros-gui

# Option 2: Direct launch
~/.local/share/astros/venv/bin/python3 gui/app.py
```

## Understanding the Issue

### Problem
- PyGObject **cannot** be installed in virtualenv (requires system packages)
- GUI was trying to use system Python (externally-managed-environment error)
- System doesn't have `girepository-2.0` development files

### Solution
- Install PyGObject as **system package** (python3-gi)
- Use **virtualenv Python** to run GUI
- System PyGObject works with virtualenv Python
- Add missing development files

## After Running fix-gui.sh

Your setup will be:
```
System Python: Has PyGObject, GTK4, Adwaita
Virtualenv Python: Has httpx, openai, python-dotenv
GUI Launch: Virtualenv Python + System PyGObject ✅
```

## WSL2 Specific

Make sure:
1. **VcXsrv running on Windows**
2. **DISPLAY variable set**:
   ```bash
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
   ```
3. **X server allows connections** (disable access control in VcXsrv)

## Test After Fix

```bash
# 1. Check dependencies
./test-gui.sh

# 2. Launch GUI
./astros-gui
```

You should see the beautiful chat window! 🎨
