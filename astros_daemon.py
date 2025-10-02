#!/usr/bin/env python3
"""
AstrOS Agent Daemon
Runs the AI agent as a systemd service
"""

import asyncio
import logging
import signal
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('astros-daemon')

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class AstrOSDaemon:
    def __init__(self):
        self.running = False
        self.agent = None
        
    async def start(self):
        """Start the daemon"""
        logger.info("🚀 Starting AstrOS Agent Daemon...")
        
        # Import agent (after logging setup)
        try:
            from astros import AstrOSAgent
            self.agent = AstrOSAgent()
            logger.info("✅ Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize agent: {e}")
            return False
            
        self.running = True
        logger.info("✅ Daemon running")
        
        # Keep running
        while self.running:
            await asyncio.sleep(1)
            
        return True
    
    def stop(self):
        """Stop the daemon gracefully"""
        logger.info("🛑 Stopping AstrOS Agent Daemon...")
        self.running = False

# Signal handlers
daemon = AstrOSDaemon()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}")
    daemon.stop()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Main entry point
if __name__ == "__main__":
    try:
        asyncio.run(daemon.start())
    except KeyboardInterrupt:
        logger.info("Daemon interrupted by user")
    except Exception as e:
        logger.error(f"Daemon crashed: {e}")
        sys.exit(1)
        