#!/bin/bash
set -e

echo "================================================"
echo "Building QMK Firmware"
echo "================================================"
echo ""

# Get the directory where this script lives (qmk/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Set QMK_USERSPACE to this directory (qmk/)
export QMK_USERSPACE="$SCRIPT_DIR"
echo "QMK_USERSPACE set to: $QMK_USERSPACE"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Build all keyboards defined in qmk.json
echo -e "${BLUE}Building keyboards from qmk.json...${NC}"
echo "Command: qmk userspace-compile"
echo ""

if qmk userspace-compile; then
    echo ""
    echo -e "${GREEN}✓ QMK builds successful${NC}"
    echo ""

    # Show firmware files
    echo "Firmware files created:"
    ls -lh "$REPO_ROOT"/*.hex "$REPO_ROOT"/*.uf2 2>/dev/null || echo "  (no firmware files found in repo root)"

    exit 0
else
    echo ""
    echo -e "${YELLOW}✗ QMK builds failed${NC}"
    exit 1
fi
