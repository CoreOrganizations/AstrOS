"""
System integration for AstrOS
"""
import os
import subprocess
import logging
import platform
from typing import Dict, Any, List


class SystemIntegration:
    """Handles system-level operations and integration"""
    
    def __init__(self):
        self.logger = logging.getLogger("astros.system")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        try:
            info = {
                'platform': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
            }
            
            # Add OS-specific information
            if platform.system() == 'Linux':
                info.update(self._get_linux_info())
            elif platform.system() == 'Windows':
                info.update(self._get_windows_info())
            
            return info
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}
    
    def _get_linux_info(self) -> Dict[str, str]:
        """Get Linux-specific information"""
        info = {}
        
        try:
            # Try to read /etc/os-release
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            info[key.lower()] = value.strip('"')
        except:
            pass
        
        try:
            # Get memory info
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        info['memory_total'] = line.split()[1] + ' kB'
                        break
        except:
            pass
        
        return info
    
    def _get_windows_info(self) -> Dict[str, str]:
        """Get Windows-specific information"""
        info = {}
        
        try:
            # Get Windows version info
            info['windows_edition'] = platform.win32_edition()
            info['windows_version'] = platform.win32_ver()[1]
        except:
            pass
        
        return info
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a system command safely"""
        try:
            # For security, only allow specific safe commands
            safe_commands = {
                'date': ['date'],
                'time': ['date'],
                'whoami': ['whoami'],
                'pwd': ['pwd'],
                'ls': ['ls', '-la'],
                'dir': ['dir'] if platform.system() == 'Windows' else ['ls', '-la'],
                'uptime': ['uptime'] if platform.system() != 'Windows' else ['systeminfo'],
            }
            
            cmd_parts = command.strip().lower().split()
            if not cmd_parts or cmd_parts[0] not in safe_commands:
                return {
                    'success': False,
                    'error': f'Command not allowed or not recognized: {command}',
                    'output': '',
                    'available_commands': list(safe_commands.keys())
                }
            
            actual_command = safe_commands[cmd_parts[0]]
            
            result = subprocess.run(
                actual_command,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out',
                'output': ''
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': ''
            }