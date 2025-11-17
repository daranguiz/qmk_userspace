#!/bin/bash
set -e

echo "================================================"
echo "Building QMK Firmware"
echo "================================================"
echo ""

# Get the directory where this script lives (qmk/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$REPO_ROOT/out/qmk"

# Set QMK_USERSPACE to this directory (qmk/)
export QMK_USERSPACE="$SCRIPT_DIR"
echo "QMK_USERSPACE set to: $QMK_USERSPACE"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Build all keyboards defined in qmk.json
echo -e "${BLUE}Building keyboards from qmk.json...${NC}"
echo "Command: qmk userspace-compile"
echo ""

if qmk userspace-compile; then
    echo ""
    echo -e "${GREEN}✓ QMK builds successful${NC}"
    echo ""

    # Move firmware files to output directory
    echo "Moving firmware files to $OUTPUT_DIR..."

    # QMK outputs to both ~/qmk_firmware/ and qmk/ directory
    # Collect all firmware files and move to output
    find "$SCRIPT_DIR" -maxdepth 1 -type f \( -name "*.hex" -o -name "*.uf2" \) -exec mv {} "$OUTPUT_DIR/" \; 2>/dev/null || true
    find ~/qmk_firmware -maxdepth 1 -type f \( -name "*.hex" -o -name "*.uf2" \) -exec cp {} "$OUTPUT_DIR/" \; 2>/dev/null || true

    # Show firmware files
    echo ""
    echo "Firmware files in $OUTPUT_DIR:"
    ls -lh "$OUTPUT_DIR"/*.hex "$OUTPUT_DIR"/*.uf2 2>/dev/null || echo "  (no firmware files found)"

    exit 0
else
    echo ""
    echo -e "${YELLOW}✗ QMK builds failed${NC}"
    exit 1
fi
