#!/usr/bin/env python3
"""
AstrOS Chat Window
Main chat interface for interacting with the AI
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Pango, Gio
import asyncio
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '/usr/lib/astros/agent')

# Try to import AstrOS agent
AstrOSAgent = None
try:
    from astros import AstrOSAgent
    print("✅ AstrOS agent module loaded")
except ImportError as e:
    print(f"⚠️  astros module not found: {e}")
    print("   GUI will run in demo mode")
    print("   Install astros-core package for full functionality")


class MessageBubble(Gtk.Box):
    """A chat message bubble widget"""
    
    def __init__(self, text, is_user=False):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        
        # Message label
        label = Gtk.Label()
        label.set_text(text)
        label.set_wrap(True)
        label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        label.set_xalign(0)
        label.set_selectable(True)
        label.set_margin_start(12)
        label.set_margin_end(12)
        label.set_margin_top(8)
        label.set_margin_bottom(8)
        
        # Bubble container
        bubble = Gtk.Frame()
        bubble.set_child(label)
        
        # Style based on sender
        if is_user:
            bubble.add_css_class("user-bubble")
            self.set_halign(Gtk.Align.END)
        else:
            bubble.add_css_class("ai-bubble")
            self.set_halign(Gtk.Align.START)
            
        self.append(bubble)


class ChatWindow(Adw.ApplicationWindow):
    """Main chat window"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.agent = None
        self.is_processing = False
        
        # Setup UI
        self.setup_window()
        self.setup_ui()
        self.apply_css()
        
        # Initialize agent
        self.init_agent()
        
    def setup_window(self):
        """Configure window properties"""
        self.set_title("AstrOS - AI Assistant")
        self.set_default_size(800, 600)
        
    def setup_ui(self):
        """Create the user interface"""
        # Main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Header bar
        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="AstrOS"))
        
        # Header buttons
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()
        menu.append("Settings", "app.settings")
        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")
        menu_button.set_menu_model(menu)
        header.pack_end(menu_button)
        
        # Clear chat button
        clear_button = Gtk.Button()
        clear_button.set_icon_name("edit-clear-all-symbolic")
        clear_button.set_tooltip_text("Clear chat history")
        clear_button.connect("clicked", self.on_clear_chat)
        header.pack_start(clear_button)
        
        main_box.append(header)
        
        # Chat area (scrolled window)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        
        # Chat container
        self.chat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.chat_box.set_margin_start(12)
        self.chat_box.set_margin_end(12)
        self.chat_box.set_margin_top(12)
        self.chat_box.set_margin_bottom(12)
        
        scrolled.set_child(self.chat_box)
        main_box.append(scrolled)
        
        # Store scrolled window for auto-scrolling
        self.scrolled_window = scrolled
        
        # Input area
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        input_box.set_margin_start(12)
        input_box.set_margin_end(12)
        input_box.set_margin_top(8)
        input_box.set_margin_bottom(12)
        
        # Text entry
        self.text_entry = Gtk.Entry()
        self.text_entry.set_placeholder_text("Type your message...")
        self.text_entry.set_hexpand(True)
        self.text_entry.connect("activate", self.on_send_message)
        
        # Send button
        send_button = Gtk.Button()
        send_button.set_icon_name("mail-send-symbolic")
        send_button.add_css_class("suggested-action")
        send_button.connect("clicked", self.on_send_message)
        
        input_box.append(self.text_entry)
        input_box.append(send_button)
        
        main_box.append(input_box)
        
        # Set main content
        self.set_content(main_box)
        
        # Welcome message
        self.add_ai_message("👋 Hello! I'm AstrOS, your AI assistant. How can I help you today?")
        
    def apply_css(self):
        """Apply custom CSS styling"""
        css_provider = Gtk.CssProvider()
        css = b"""
        .user-bubble frame {
            background-color: #3584e4;
            border-radius: 12px;
            color: white;
        }
        
        .user-bubble frame label {
            color: white;
        }
        
        .ai-bubble frame {
            background-color: #f6f5f4;
            border-radius: 12px;
        }
        
        .ai-bubble frame label {
            color: #1e1e1e;
        }
        """
        css_provider.load_from_data(css)
        
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
    def init_agent(self):
        """Initialize the AstrOS agent"""
        try:
            if AstrOSAgent:
                self.agent = AstrOSAgent()
                print("✅ Agent initialized")
            else:
                print("⚠️  Running in demo mode (no agent)")
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            self.add_ai_message(f"⚠️ Warning: Could not connect to AstrOS backend.\n{e}")
            
    def add_user_message(self, text):
        """Add a user message to the chat"""
        bubble = MessageBubble(text, is_user=True)
        self.chat_box.append(bubble)
        self.scroll_to_bottom()
        
    def add_ai_message(self, text):
        """Add an AI message to the chat"""
        bubble = MessageBubble(text, is_user=False)
        self.chat_box.append(bubble)
        self.scroll_to_bottom()
        
    def scroll_to_bottom(self):
        """Scroll chat to the bottom"""
        def do_scroll():
            adj = self.scrolled_window.get_vadjustment()
            adj.set_value(adj.get_upper())
            return False
            
        GLib.timeout_add(100, do_scroll)
        
    def on_clear_chat(self, button):
        """Clear chat history"""
        # Remove all children except first (welcome message)
        child = self.chat_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            if child != self.chat_box.get_first_child():
                self.chat_box.remove(child)
            child = next_child
            
    def on_send_message(self, widget):
        """Handle send button click"""
        if self.is_processing:
            return
            
        text = self.text_entry.get_text().strip()
        if not text:
            return
            
        # Clear input
        self.text_entry.set_text("")
        
        # Add user message
        self.add_user_message(text)
        
        # Process in background
        self.is_processing = True
        self.text_entry.set_sensitive(False)
        
        # Show thinking indicator
        thinking_bubble = MessageBubble("💭 Thinking...", is_user=False)
        self.chat_box.append(thinking_bubble)
        self.scroll_to_bottom()
        
        # Get response asynchronously
        GLib.timeout_add(100, lambda: self.get_response_async(text, thinking_bubble))
        
    def get_response_async(self, question, thinking_bubble):
        """Get response from agent asynchronously"""
        async def get_response():
            try:
                if self.agent:
                    response = await self.agent.get_response(question)
                else:
                    # Demo mode response
                    await asyncio.sleep(1)
                    response = f"Demo response to: {question}\n\n(Install AstrOS agent for real responses)"
                    
                # Update UI in main thread
                GLib.idle_add(self.show_response, response, thinking_bubble)
            except Exception as e:
                error_msg = f"❌ Error: {e}"
                GLib.idle_add(self.show_response, error_msg, thinking_bubble)
                
        # Run async task
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(get_response())
        loop.close()
        
        return False
        
    def show_response(self, response, thinking_bubble):
        """Show the AI response"""
        # Remove thinking indicator
        self.chat_box.remove(thinking_bubble)
        
        # Add response
        self.add_ai_message(response)
        
        # Re-enable input
        self.is_processing = False
        self.text_entry.set_sensitive(True)
        self.text_entry.grab_focus()
        
        return False
