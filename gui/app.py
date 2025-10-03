#!/usr/bin/env python3
"""
AstrOS Desktop Application
Main GTK4 application entry point
"""

import sys
import os
import signal
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.chat_window import ChatWindow
from gui.tray import AstrosTray


class AstrOSApplication(Adw.Application):
    """Main AstrOS GTK Application"""
    
    def __init__(self):
        super().__init__(
            application_id='org.astros.desktop',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        
        self.window = None
        self.tray = None
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
    def do_activate(self):
        """Called when the application is activated"""
        if not self.window:
            self.window = ChatWindow(application=self)
            self.setup_actions()
            
        self.window.present()
        
    def do_startup(self):
        """Called when the application starts"""
        Adw.Application.do_startup(self)
        
        # Create system tray
        self.tray = AstrosTray(self)
        
    def setup_actions(self):
        """Setup application actions"""
        # Show window action
        action = Gio.SimpleAction.new("show-window", None)
        action.connect("activate", self.on_show_window)
        self.add_action(action)
        
        # Settings action
        action = Gio.SimpleAction.new("settings", None)
        action.connect("activate", self.on_settings)
        self.add_action(action)
        
        # About action
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        
        # Quit action
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        
        # Keyboard shortcuts
        self.set_accels_for_action("app.quit", ["<Ctrl>Q"])
        self.set_accels_for_action("app.settings", ["<Ctrl>comma"])
        
    def on_show_window(self, action, param):
        """Show the main window"""
        if self.window:
            self.window.present()
            
    def on_settings(self, action, param):
        """Show settings dialog"""
        # TODO: Implement settings window
        print("Settings clicked")
        
    def on_about(self, action, param):
        """Show about dialog"""
        about = Adw.AboutWindow(
            transient_for=self.window,
            application_name="AstrOS",
            application_icon="org.astros.desktop",
            developer_name="CoreOrganizations",
            version="0.1.0",
            website="https://github.com/CoreOrganizations/AstrOS",
            issue_url="https://github.com/CoreOrganizations/AstrOS/issues",
            license_type=Gtk.License.MIT_X11,
            comments="AI-powered desktop assistant",
        )
        about.present()
        
    def on_quit(self, action, param):
        """Quit the application"""
        self.quit()


def main():
    """Main entry point"""
    app = AstrOSApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
