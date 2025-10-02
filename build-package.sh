#!/bin/bash
# Build AstrOS Debian Package

set -e

echo "📦 Building AstrOS Core Debian Package"
echo "========================================"

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_BUILD="/tmp/astros-build-$$"
PACKAGE_NAME="astros-core"

# Create clean temp directory
rm -rf "$TEMP_BUILD"
mkdir -p "$TEMP_BUILD/$PACKAGE_NAME"

echo ""
echo "📁 Creating package structure in: $TEMP_BUILD"
echo ""

# Create directory structure
mkdir -p "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN"
mkdir -p "$TEMP_BUILD/$PACKAGE_NAME/usr/lib/astros/agent"
mkdir -p "$TEMP_BUILD/$PACKAGE_NAME/usr/bin"
mkdir -p "$TEMP_BUILD/$PACKAGE_NAME/etc/systemd/system"

# Copy files from source
echo "📋 Copying files..."
cp "$SOURCE_DIR/astros.py" "$TEMP_BUILD/$PACKAGE_NAME/usr/lib/astros/agent/"
cp "$SOURCE_DIR/astros_daemon.py" "$TEMP_BUILD/$PACKAGE_NAME/usr/lib/astros/agent/"
cp "$SOURCE_DIR/packages/astros-core/usr/lib/astros/agent/astros_cli.py" "$TEMP_BUILD/$PACKAGE_NAME/usr/lib/astros/agent/"
cp "$SOURCE_DIR/packages/astros-core/usr/lib/astros/agent/start_daemon.sh" "$TEMP_BUILD/$PACKAGE_NAME/usr/lib/astros/agent/"
cp "$SOURCE_DIR/configs/astros-agent.service" "$TEMP_BUILD/$PACKAGE_NAME/etc/systemd/system/astros-agent@.service"
cp "$SOURCE_DIR/packages/astros-core/DEBIAN/control" "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/"
cp "$SOURCE_DIR/packages/astros-core/DEBIAN/postinst" "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/"
cp "$SOURCE_DIR/packages/astros-core/DEBIAN/prerm" "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/"
cp "$SOURCE_DIR/packages/astros-core/usr/bin/astros-cli" "$TEMP_BUILD/$PACKAGE_NAME/usr/bin/"

# Fix Windows line endings (convert CRLF to LF)
echo "🔧 Converting line endings..."
dos2unix "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/postinst" 2>/dev/null || sed -i 's/\r$//' "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/postinst"
dos2unix "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/prerm" 2>/dev/null || sed -i 's/\r$//' "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/prerm"
dos2unix "$TEMP_BUILD/$PACKAGE_NAME/usr/bin/astros-cli" 2>/dev/null || sed -i 's/\r$//' "$TEMP_BUILD/$PACKAGE_NAME/usr/bin/astros-cli"

# Set proper permissions (in Linux temp filesystem)
echo "🔐 Setting permissions..."
chmod 755 "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN"
chmod 644 "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/control"
chmod 755 "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/postinst"
chmod 755 "$TEMP_BUILD/$PACKAGE_NAME/DEBIAN/prerm"
chmod 755 "$TEMP_BUILD/$PACKAGE_NAME/usr/bin/astros-cli"
chmod 644 "$TEMP_BUILD/$PACKAGE_NAME/usr/lib/astros/agent/"*.py
chmod 644 "$TEMP_BUILD/$PACKAGE_NAME/etc/systemd/system/astros-agent@.service"

# Show structure
echo ""
echo "📋 Package contents:"
find "$TEMP_BUILD/$PACKAGE_NAME" -type f | sed "s|$TEMP_BUILD/$PACKAGE_NAME|astros-core|" | sort
echo ""

# Build package
echo "🔨 Building .deb package..."
cd "$TEMP_BUILD"
dpkg-deb --build "$PACKAGE_NAME"

# Copy to source directory
cp "$PACKAGE_NAME.deb" "$SOURCE_DIR/packages/"

# Get package info
if [ -f "$SOURCE_DIR/packages/astros-core.deb" ]; then
    cd "$SOURCE_DIR"
    echo ""
    echo "========================================"
    echo "✅ Package built successfully!"
    echo "========================================"
    echo ""
    
    # Show package info
    echo "📦 Package Information:"
    dpkg-deb --info packages/astros-core.deb | grep -E "Package:|Version:|Architecture:|Depends:"
    echo ""
    
    # Show package size
    SIZE=$(du -h packages/astros-core.deb | cut -f1)
    echo "📏 Package Size: $SIZE"
    echo ""
    
    # Show contents
    echo "📋 Package Contents (first 20):"
    dpkg-deb --contents packages/astros-core.deb | head -20
    echo ""
    
    echo "========================================"
    echo "🎉 Ready to install!"
    echo "========================================"
    echo ""
    echo "Install with:"
    echo "  sudo dpkg -i packages/astros-core.deb"
    echo ""
    echo "Or test in a clean Ubuntu VM"
    echo ""
    
    # Cleanup
    rm -rf "$TEMP_BUILD"
else
    echo "❌ Package build failed!"
    rm -rf "$TEMP_BUILD"
    exit 1
fi
