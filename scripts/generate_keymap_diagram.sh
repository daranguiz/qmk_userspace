#!/bin/bash
set -e

# Usage: bash scripts/generate_keymap_diagram.sh <keyboard> <keymap>
# Example: bash scripts/generate_keymap_diagram.sh boardsource/lulu/rp2040 dario

KEYBOARD="${1:-boardsource/lulu/rp2040}"
KEYMAP="${2:-dario}"
OUTPUT_DIR="docs/keymaps"
CONFIG=".keymap-drawer-config.yaml"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Convert keyboard path to safe filename (replace / with _)
KEYBOARD_SAFE="${KEYBOARD//\//_}"
OUTPUT_FILE="$OUTPUT_DIR/${KEYBOARD_SAFE}_${KEYMAP}.svg"

echo "Generating keymap visualization for $KEYBOARD:$KEYMAP"
echo "Config: $CONFIG"
echo "Output: $OUTPUT_FILE"

# Convert keymap to JSON, parse with config, and generate SVG
# Layer names: BASE NAV MEDIA NUM SYM FUN
# NOTE: Using --no-cpp because WITH preprocessing fails on userspace includes
# This means LAYOUT_wrapper won't be expanded, which is OK for visualization
qmk c2json -kb "$KEYBOARD" -km "$KEYMAP" --no-cpp 2>/dev/null | \
  keymap -c "$CONFIG" parse --layer-names BASE NAV MEDIA NUM SYM FUN -q - | \
  keymap -c "$CONFIG" draw - > "$OUTPUT_FILE"

echo "✓ Generated: $OUTPUT_FILE"
