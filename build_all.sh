#!/bin/bash
set -e

echo "================================================"
echo "Building all QMK keyboards"
echo "================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Build counters
SUCCESS_COUNT=0
FAIL_COUNT=0
KEYBOARDS=()

# Function to build a keyboard
build_keyboard() {
    local keyboard=$1
    local keymap=$2
    local name=$3

    echo -e "${BLUE}Building ${name}...${NC}"
    echo "Command: qmk compile -kb ${keyboard} -km ${keymap}"

    if qmk compile -kb "${keyboard}" -km "${keymap}" 2>&1 | grep -E "(OK|firmware size)"; then
        echo -e "${GREEN}✓ ${name} build successful${NC}"
        echo ""
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        KEYBOARDS+=("${keyboard}")
        return 0
    else
        echo -e "${YELLOW}✗ ${name} build failed${NC}"
        echo ""
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi
}

# Build all keyboards
echo "------------------------------------------------"
echo "Phase 1: Building firmware"
echo "------------------------------------------------"
echo ""

build_keyboard "bastardkb/skeletyl/promicro" "dario" "Skeletyl"
build_keyboard "boardsource/lulu/rp2040" "dario" "Lulu"
build_keyboard "lily58/rev1" "dario" "Lily58"

echo ""
echo "------------------------------------------------"
echo "Phase 2: Generating keymap visualizations"
echo "------------------------------------------------"
echo ""

# Generate visualizations for successfully built keyboards
VIZ_SUCCESS=0
VIZ_FAIL=0

for keyboard in "${KEYBOARDS[@]}"; do
    keyboard_name=$(basename "$keyboard")
    echo -e "${BLUE}Generating visualization for ${keyboard_name}...${NC}"

    if bash tools/gen-keymap-visual.sh "${keyboard}" dario 2>&1 | grep -E "Wrote SVG|Generated JSON"; then
        echo -e "${GREEN}✓ ${keyboard_name} visualization generated${NC}"
        VIZ_SUCCESS=$((VIZ_SUCCESS + 1))
    else
        echo -e "${YELLOW}✗ ${keyboard_name} visualization failed${NC}"
        VIZ_FAIL=$((VIZ_FAIL + 1))
    fi
    echo ""
done

# Summary
echo "================================================"
echo "Build Summary"
echo "================================================"
echo -e "Firmware builds: ${GREEN}${SUCCESS_COUNT} successful${NC}, ${YELLOW}${FAIL_COUNT} failed${NC}"
echo -e "Visualizations:  ${GREEN}${VIZ_SUCCESS} successful${NC}, ${YELLOW}${VIZ_FAIL} failed${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All keyboard builds completed successfully!${NC}"
    echo ""
    echo "Firmware files:"
    ls -lh *.hex *.uf2 2>/dev/null || echo "  (check build output above)"
    echo ""
    echo "Visualizations:"
    ls -lh docs/keymaps/*.svg 2>/dev/null || echo "  (no visualizations generated)"
    exit 0
else
    echo -e "${YELLOW}Some builds failed. Check output above for details.${NC}"
    exit 1
fi
