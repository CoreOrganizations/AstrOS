#!/usr/bin/env python3
"""
AstrOS System Tray
System tray icon and menu for AstrOS
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio


class AstrosTray:
    """System tray icon for AstrOS"""
    
    def __init__(self, app):
        self.app = app
        
        # Note: GTK4 removed StatusIcon, using alternative approaches
        # For now, we'll focus on the application menu and window controls
        # Future: Implement using libappindicator or system-specific tray
        
        print("🔔 System tray integration (using app menu)")
        
    def show_window(self):
        """Show the main window"""
        if self.app.window:
            self.app.window.present()
