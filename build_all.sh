#!/bin/bash
set -e

echo "================================================"
echo "Building All Keyboard Firmware"
echo "================================================"
echo ""

# Get repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track build results
KEYGEN_SUCCESS=false
QMK_SUCCESS=false
ZMK_SUCCESS=false

# Generate keymaps first (runs once for both QMK and ZMK)
echo "================================================"
echo "Phase 0: Generating Keymaps"
echo "================================================"
echo ""

echo -e "${BLUE}Running keymap generator...${NC}"
if python3 "$REPO_ROOT/scripts/generate.py"; then
    echo -e "${GREEN}✓ Keymap generation successful${NC}"
    echo ""
    KEYGEN_SUCCESS=true
else
    echo -e "${YELLOW}✗ Keymap generation failed${NC}"
    echo "Cannot proceed with builds without generated keymaps"
    exit 1
fi

# Build QMK firmware
echo ""
echo "================================================"
echo "Phase 1: QMK Firmware"
echo "================================================"
echo ""

if bash "$REPO_ROOT/qmk/build_qmk.sh"; then
    QMK_SUCCESS=true
else
    echo -e "${YELLOW}⚠ QMK builds failed${NC}"
    echo ""
fi

# Build ZMK firmware
echo ""
echo "================================================"
echo "Phase 2: ZMK Firmware"
echo "================================================"
echo ""

if [ -f "$REPO_ROOT/zmk/build_zmk.sh" ]; then
    if bash "$REPO_ROOT/zmk/build_zmk.sh"; then
        ZMK_SUCCESS=true
    else
        echo -e "${YELLOW}⚠ ZMK builds failed${NC}"
        echo ""
    fi
else
    echo -e "${YELLOW}ZMK build script not found, skipping ZMK builds${NC}"
    echo ""
fi

# Summary
echo ""
echo "================================================"
echo "Build Summary"
echo "================================================"

if [ "$KEYGEN_SUCCESS" = true ]; then
    echo -e "${GREEN}✓ Keymap generation: SUCCESS${NC}"
else
    echo -e "${YELLOW}✗ Keymap generation: FAILED${NC}"
fi

if [ "$QMK_SUCCESS" = true ]; then
    echo -e "${GREEN}✓ QMK builds: SUCCESS${NC}"
else
    echo -e "${YELLOW}✗ QMK builds: FAILED${NC}"
fi

if [ "$ZMK_SUCCESS" = true ]; then
    echo -e "${GREEN}✓ ZMK builds: SUCCESS${NC}"
elif [ -f "$REPO_ROOT/zmk/build_zmk.sh" ]; then
    echo -e "${YELLOW}✗ ZMK builds: FAILED${NC}"
else
    echo -e "${BLUE}○ ZMK builds: SKIPPED${NC}"
fi

echo ""

# Show all firmware files
echo "All firmware files:"
ls -lh "$REPO_ROOT"/*.hex "$REPO_ROOT"/*.uf2 2>/dev/null || echo "  (no firmware files found)"
ls -lh "$REPO_ROOT/firmware"/*.uf2 2>/dev/null || echo "  (no ZMK firmware files found)"

echo ""
echo "All visualizations:"
ls -lh "$REPO_ROOT/docs/keymaps"/*.svg 2>/dev/null || echo "  (no visualizations found)"

echo ""

# Exit with appropriate code
if [ "$QMK_SUCCESS" = true ] || [ "$ZMK_SUCCESS" = true ]; then
    echo -e "${GREEN}✓ Build completed!${NC}"
    exit 0
else
    echo -e "${YELLOW}✗ All builds failed${NC}"
    exit 1
fi
