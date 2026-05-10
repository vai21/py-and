#!/usr/bin/env bash
# Build .app with PyInstaller, then wrap it in a .pkg for drag-free install to /Applications.
# Must run on macOS. Use Python from python.org (with tkinter) or another Tk-enabled build.
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

VERSION="${VERSION:-1.0.0}"
BUNDLE_ID="${BUNDLE_ID:-com.pyand.serialbpmonitor}"

python3 -m pip install -r requirements.txt -r requirements-packaging.txt
python3 -m PyInstaller --noconfirm serial_bp_monitor.spec

APP_PATH="$APP_DIR/dist/BPSerialMonitor.app"
PKG_PATH="$APP_DIR/dist/BPSerialMonitor-${VERSION}-macos.pkg"

if [[ ! -d "$APP_PATH" ]]; then
  echo "Expected app bundle not found: $APP_PATH" >&2
  exit 1
fi

pkgbuild \
  --component "$APP_PATH" \
  --identifier "$BUNDLE_ID" \
  --version "$VERSION" \
  --install-location /Applications \
  "$PKG_PATH"

echo ""
echo "Application bundle: $APP_PATH"
echo "Installer package:   $PKG_PATH"
