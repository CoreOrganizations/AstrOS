#!/bin/bash
# AstrOS Plugin Generator Script
# Creates a new plugin with proper structure and boilerplate code

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse command line arguments
PLUGIN_NAME=""
AUTHOR_NAME=""
AUTHOR_EMAIL=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --name)
            PLUGIN_NAME="$2"
            shift 2
            ;;
        --author)
            AUTHOR_NAME="$2"
            shift 2
            ;;
        --email)
            AUTHOR_EMAIL="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --name PLUGIN_NAME --author AUTHOR_NAME [--email AUTHOR_EMAIL]"
            echo ""
            echo "Creates a new AstrOS plugin with proper structure"
            echo ""
            echo "Options:"
            echo "  --name     Plugin name (required)"
            echo "  --author   Author name (required)"
            echo "  --email    Author email (optional)"
            echo "  -h, --help Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$PLUGIN_NAME" ]]; then
    print_error "Plugin name is required. Use --name PLUGIN_NAME"
    exit 1
fi

if [[ -z "$AUTHOR_NAME" ]]; then
    print_error "Author name is required. Use --author AUTHOR_NAME"
    exit 1
fi

# Sanitize plugin name
PLUGIN_NAME=$(echo "$PLUGIN_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
PLUGIN_CLASS=$(echo "$PLUGIN_NAME" | sed 's/-/ /g' | sed 's/\b\w/\U&/g' | sed 's/ //g')Plugin

print_status "Creating plugin: $PLUGIN_NAME"
print_status "Plugin class: $PLUGIN_CLASS"
print_status "Author: $AUTHOR_NAME"

# Create plugin directory structure
PLUGIN_DIR="plugins/$PLUGIN_NAME"

if [[ -d "$PLUGIN_DIR" ]]; then
    print_error "Plugin directory already exists: $PLUGIN_DIR"
    exit 1
fi

mkdir -p "$PLUGIN_DIR/src"
mkdir -p "$PLUGIN_DIR/tests"

# Create plugin.yaml
cat > "$PLUGIN_DIR/plugin.yaml" << EOF
# AstrOS Plugin Metadata
name: $PLUGIN_NAME
version: "1.0.0"
description: "A description of what this plugin does"
author: "$AUTHOR_NAME"
$(if [[ -n "$AUTHOR_EMAIL" ]]; then echo "email: \"$AUTHOR_EMAIL\""; fi)
homepage: "https://github.com/AstrOS-Project/astros-plugins/tree/main/$PLUGIN_NAME"

# Plugin Configuration
astros_version: ">=0.1.0"
python_version: ">=3.12"

# Plugin Capabilities
capabilities:
  - natural_language_processing
  - file_system_access
  # Add more capabilities as needed

# Plugin Dependencies
dependencies:
  - pydantic>=2.5.0
  
# Development Dependencies (for testing)
dev_dependencies:
  - pytest>=7.4.0
  - pytest-asyncio>=0.21.0

# Plugin Settings
settings:
  # Define configurable settings here
  enabled: true
  debug: false

# Plugin Permissions
permissions:
  filesystem:
    read: true
    write: false
  network:
    enabled: false
  system:
    commands: false
EOF

# Create main plugin file
cat > "$PLUGIN_DIR/src/__init__.py" << 'EOF'
"""
Plugin package initialization
"""

from .main import plugin

__all__ = ["plugin"]
EOF

cat > "$PLUGIN_DIR/src/main.py" << EOF
"""
$PLUGIN_CLASS - AstrOS Plugin

Description: A description of what this plugin does
Author: $AUTHOR_NAME
$(if [[ -n "$AUTHOR_EMAIL" ]]; then echo "Email: $AUTHOR_EMAIL"; fi)
"""

import logging
from typing import Any, Dict, List, Optional

from astros.plugin import BasePlugin, plugin_handler
from astros.types import Intent, Response


class $PLUGIN_CLASS(BasePlugin):
    """
    Example AstrOS plugin that demonstrates the plugin architecture.
    
    This plugin shows how to:
    - Handle natural language intents
    - Process user requests
    - Return structured responses
    - Use configuration settings
    - Log plugin activities
    """
    
    # Plugin metadata
    name = "$PLUGIN_NAME"
    version = "1.0.0"
    description = "A description of what this plugin does"
    author = "$AUTHOR_NAME"
    $(if [[ -n "$AUTHOR_EMAIL" ]]; then echo "    email = \"$AUTHOR_EMAIL\""; fi)
    
    # Plugin capabilities
    handles = [
        "example_action",
        "another_action",
    ]
    
    # Plugin requirements
    requires_ai = True
    requires_permissions = ["file_system"]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the plugin with configuration."""
        super().__init__(config)
        self.logger = logging.getLogger(f"astros.plugin.{self.name}")
        
        # Plugin-specific initialization
        self.enabled = self.config.get("enabled", True)
        self.debug = self.config.get("debug", False)
        
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
    
    async def initialize(self) -> None:
        """
        Initialize the plugin when it's loaded.
        
        This method is called when the plugin is first loaded.
        Use it to set up any resources, connections, or state needed.
        """
        self.logger.info(f"Initializing {self.name} plugin")
        
        if not self.enabled:
            self.logger.warning("Plugin is disabled in configuration")
            return
        
        # Perform any setup tasks here
        # Examples:
        # - Initialize database connections
        # - Set up file watchers
        # - Load configuration files
        # - Initialize AI models
        
        self.logger.info(f"{self.name} plugin initialized successfully")
    
    async def shutdown(self) -> None:
        """
        Clean up when the plugin is unloaded.
        
        This method is called when the plugin is being unloaded.
        Use it to clean up resources, save state, or close connections.
        """
        self.logger.info(f"Shutting down {self.name} plugin")
        
        # Perform cleanup tasks here
        # Examples:
        # - Close database connections
        # - Save configuration changes
        # - Stop background tasks
        # - Release file locks
        
        self.logger.info(f"{self.name} plugin shutdown complete")
    
    @plugin_handler("example_action")
    async def handle_example_action(self, intent: Intent) -> Response:
        """
        Handle an example action request.
        
        This is an example of how to handle specific user intents.
        The intent contains the user's natural language request and
        any extracted parameters.
        
        Args:
            intent: The user's intent with request text and parameters
            
        Returns:
            Response with success status, message, and optional data
        """
        self.logger.debug(f"Handling example action: {intent.text}")
        
        try:
            # Extract parameters from the intent
            user_input = intent.text
            parameters = intent.parameters or {}
            
            # Process the request
            result = await self._process_example_action(user_input, parameters)
            
            # Return successful response
            return Response(
                success=True,
                message=f"Example action completed successfully",
                data={
                    "result": result,
                    "processed_input": user_input,
                    "parameters": parameters
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error handling example action: {e}")
            return Response(
                success=False,
                message=f"Failed to process example action: {str(e)}",
                error=str(e)
            )
    
    @plugin_handler("another_action")
    async def handle_another_action(self, intent: Intent) -> Response:
        """Handle another type of action."""
        self.logger.debug(f"Handling another action: {intent.text}")
        
        # Implementation for another action type
        return Response(
            success=True,
            message="Another action completed",
            data={"action": "another_action"}
        )
    
    async def _process_example_action(
        self, 
        user_input: str, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Private method to process the example action.
        
        Args:
            user_input: The original user input text
            parameters: Extracted parameters from the intent
            
        Returns:
            Dictionary with processing results
        """
        # Example processing logic
        result = {
            "processed": True,
            "input_length": len(user_input),
            "parameter_count": len(parameters),
            "timestamp": self._get_current_timestamp()
        }
        
        # Add any processing logic here
        # Examples:
        # - File operations
        # - API calls
        # - Data transformations
        # - AI model inference
        
        return result
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get plugin status information.
        
        Returns:
            Dictionary with plugin status details
        """
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "debug": self.debug,
            "initialized": hasattr(self, '_initialized'),
        }


# Plugin instance - this is what gets loaded by the plugin manager
plugin = $PLUGIN_CLASS()
EOF

# Create tests
cat > "$PLUGIN_DIR/tests/__init__.py" << 'EOF'
"""
Tests package initialization
"""
EOF

cat > "$PLUGIN_DIR/tests/test_plugin.py" << EOF
"""
Tests for $PLUGIN_CLASS
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from astros.types import Intent, Response
from src.main import $PLUGIN_CLASS


class Test$PLUGIN_CLASS:
    """Test cases for $PLUGIN_CLASS plugin."""
    
    @pytest.fixture
    def plugin(self):
        """Create a plugin instance for testing."""
        config = {
            "enabled": True,
            "debug": True
        }
        return $PLUGIN_CLASS(config)
    
    @pytest.mark.asyncio
    async def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        await plugin.initialize()
        
        assert plugin.name == "$PLUGIN_NAME"
        assert plugin.version == "1.0.0"
        assert plugin.enabled is True
        assert plugin.debug is True
    
    @pytest.mark.asyncio
    async def test_handle_example_action(self, plugin):
        """Test handling example action."""
        await plugin.initialize()
        
        intent = Intent(
            text="Test example action",
            parameters={"test": "value"}
        )
        
        response = await plugin.handle_example_action(intent)
        
        assert response.success is True
        assert "Example action completed successfully" in response.message
        assert response.data is not None
        assert response.data["processed_input"] == "Test example action"
        assert response.data["parameters"]["test"] == "value"
    
    @pytest.mark.asyncio
    async def test_handle_another_action(self, plugin):
        """Test handling another action."""
        await plugin.initialize()
        
        intent = Intent(text="Test another action")
        response = await plugin.handle_another_action(intent)
        
        assert response.success is True
        assert response.message == "Another action completed"
        assert response.data["action"] == "another_action"
    
    @pytest.mark.asyncio
    async def test_get_status(self, plugin):
        """Test getting plugin status."""
        await plugin.initialize()
        
        status = await plugin.get_status()
        
        assert status["name"] == "$PLUGIN_NAME"
        assert status["version"] == "1.0.0"
        assert status["enabled"] is True
        assert status["debug"] is True
    
    @pytest.mark.asyncio
    async def test_plugin_shutdown(self, plugin):
        """Test plugin shutdown."""
        await plugin.initialize()
        await plugin.shutdown()
        
        # Plugin should handle shutdown gracefully
        # Add specific assertions based on your shutdown logic
        assert True  # Placeholder assertion
EOF

# Create requirements.txt
cat > "$PLUGIN_DIR/requirements.txt" << 'EOF'
# Plugin-specific requirements
# These are installed when the plugin is loaded

pydantic>=2.5.0
EOF

# Create README.md
cat > "$PLUGIN_DIR/README.md" << EOF
# $PLUGIN_NAME Plugin

A description of what this plugin does for AstrOS.

## Features

- Feature 1: Description
- Feature 2: Description  
- Feature 3: Description

## Installation

This plugin is part of the official AstrOS plugin collection. It's automatically available when you install AstrOS.

## Configuration

Add configuration to your \`config.yaml\`:

\`\`\`yaml
plugins:
  $PLUGIN_NAME:
    enabled: true
    debug: false
    # Add plugin-specific settings here
\`\`\`

## Usage

### Voice Commands

\`\`\`
"Hey AstrOS, [example command]"
"[Another example command]"
\`\`\`

### Text Commands

\`\`\`bash
astros plugin $PLUGIN_NAME [action]
\`\`\`

## Examples

### Example 1: Basic Usage

\`\`\`
User: "Example command"
AstrOS: "Action completed successfully"
\`\`\`

### Example 2: Advanced Usage

\`\`\`
User: "More complex example command with parameters"
AstrOS: "Advanced action completed with specific results"
\`\`\`

## Development

### Running Tests

\`\`\`bash
cd plugins/$PLUGIN_NAME
pytest tests/
\`\`\`

### Plugin Structure

\`\`\`
$PLUGIN_NAME/
├── plugin.yaml          # Plugin metadata
├── src/
│   ├── __init__.py
│   └── main.py          # Main plugin implementation
├── tests/
│   ├── __init__.py
│   └── test_plugin.py   # Plugin tests
├── requirements.txt     # Plugin dependencies
└── README.md           # This file
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests: \`pytest tests/\`
6. Submit a pull request

## License

This plugin is part of the AstrOS project and is licensed under the Apache License 2.0.

## Author

**$AUTHOR_NAME**$(if [[ -n "$AUTHOR_EMAIL" ]]; then echo "  "; echo "Email: $AUTHOR_EMAIL"; fi)

## Support

- 🐛 [Report Issues](https://github.com/AstrOS-Project/astros-plugins/issues)
- 💬 [Community Discord](https://discord.gg/astros)
- 📖 [Documentation](https://docs.astros.org/plugins/$PLUGIN_NAME)
EOF

print_success "Plugin created successfully: $PLUGIN_DIR"
echo
print_status "Plugin structure:"
echo "  plugins/$PLUGIN_NAME/"
echo "  ├── plugin.yaml          # Plugin metadata"
echo "  ├── src/"
echo "  │   ├── __init__.py"
echo "  │   └── main.py          # Main plugin implementation"
echo "  ├── tests/"
echo "  │   ├── __init__.py"
echo "  │   └── test_plugin.py   # Plugin tests"
echo "  ├── requirements.txt     # Plugin dependencies"
echo "  └── README.md           # Plugin documentation"
echo
print_status "Next steps:"
echo "  1. Edit plugin.yaml to customize metadata"
echo "  2. Implement your plugin logic in src/main.py"
echo "  3. Add tests in tests/test_plugin.py"
echo "  4. Update README.md with usage examples"
echo "  5. Test your plugin: cd plugins/$PLUGIN_NAME && pytest tests/"
echo
print_success "Happy plugin development! 🔌"