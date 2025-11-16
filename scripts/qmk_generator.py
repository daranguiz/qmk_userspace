"""
QMK keymap generator

Generates QMK C code files from compiled layers
"""

from pathlib import Path
from typing import List, Dict
from data_model import Board, CompiledLayer


class QMKGenerator:
    """Generate QMK C keymap files"""

    def generate_keymap(
        self,
        board: Board,
        compiled_layers: List[CompiledLayer],
        output_dir: Path
    ) -> Dict[str, str]:
        """
        Generate all QMK files for a board

        Args:
            board: Target board
            compiled_layers: List of compiled layers
            output_dir: Output directory path

        Returns:
            Dictionary of {filename: content} for all generated files
        """
        files = {}

        # Generate keymap.c
        files['keymap.c'] = self.generate_keymap_c(board, compiled_layers)

        # Generate config.h
        files['config.h'] = self.generate_config_h(board, compiled_layers)

        # Generate rules.mk
        files['rules.mk'] = self.generate_rules_mk(board)

        # Generate README.md with ASCII art visualization
        files['README.md'] = self.generate_visualization(board, compiled_layers)

        return files

    def generate_keymap_c(
        self,
        board: Board,
        compiled_layers: List[CompiledLayer]
    ) -> str:
        """
        Generate keymap.c file

        Args:
            board: Target board
            compiled_layers: List of compiled layers

        Returns:
            Complete keymap.c file content
        """
        # Generate layer definitions
        layer_defs = []
        layer_names = [layer.name for layer in compiled_layers]

        for layer in compiled_layers:
            formatted = self.format_layer_definition(board, layer)
            layer_defs.append(f"    [{layer.name}] = {formatted},")

        layers_code = "\n".join(layer_defs)

        # Check if we need additional layer definitions (for board-specific layers like GAME)
        has_extra_layers = len(board.extra_layers) > 0
        extra_layers_code = ""
        if has_extra_layers:
            # Define extra layer enum values after the standard layers
            extra_layers_list = ", ".join(board.extra_layers)
            extra_layers_code = f"""
// Board-specific layers (extend standard enum from dario.h)
enum {{
    {extra_layers_list} = FUN + 1  // Continue from last standard layer
}};
"""

        return f"""// AUTO-GENERATED - DO NOT EDIT
// Generated from config/keymap.yaml by scripts/generate.py
// Board: {board.name}
// Firmware: QMK

#include "dario.h"
{extra_layers_code}
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {{
{layers_code}
}};
"""

    def format_layer_definition(
        self,
        board: Board,
        layer: CompiledLayer
    ) -> str:
        """
        Format a layer definition using the appropriate LAYOUT macro

        Args:
            board: Target board
            layer: Compiled layer

        Returns:
            Formatted LAYOUT_* macro call
        """
        keycodes = layer.keycodes
        num_keys = len(keycodes)

        # Determine which LAYOUT macro to use
        if board.layout_size == "3x5_3":
            # 36-key split 3x5_3
            return self._format_split_3x5_3(keycodes)
        elif board.layout_size == "3x6_3":
            # 42-key split 3x6_3
            return self._format_split_3x6_3(keycodes)
        elif board.layout_size.startswith("custom_"):
            # Custom layout - use board-specific wrapper
            return self._format_custom_layout(board, keycodes)
        else:
            # Default: split 3x5_3
            return self._format_split_3x5_3(keycodes)

    def _format_split_3x5_3(self, keycodes: List[str]) -> str:
        """Format 36-key split 3x5_3 layout"""
        if len(keycodes) != 36:
            raise ValueError(f"Expected 36 keys for 3x5_3 layout, got {len(keycodes)}")

        # Group into rows for readability
        # Left hand: rows 0-2 (5 keys each)
        # Right hand: rows 3-5 (5 keys each)
        # Left thumbs: row 6 (3 keys)
        # Right thumbs: row 7 (3 keys)

        rows = [
            keycodes[0:5],   # Left hand row 1
            keycodes[5:10],  # Left hand row 2
            keycodes[10:15], # Left hand row 3
            keycodes[15:20], # Right hand row 1
            keycodes[20:25], # Right hand row 2
            keycodes[25:30], # Right hand row 3
            keycodes[30:33], # Left thumbs
            keycodes[33:36], # Right thumbs
        ]

        formatted_rows = []
        for i, row in enumerate(rows):
            if i < 6:  # Finger rows
                formatted_rows.append("        " + ", ".join(f"{k:20}" for k in row) + ",")
            elif i == 6:  # Left thumb row (needs comma)
                formatted_rows.append("                              " + ", ".join(f"{k:20}" for k in row) + ",")
            else:  # Right thumb row (last row, no comma)
                formatted_rows.append("                              " + ", ".join(f"{k:20}" for k in row))

        return f"LAYOUT_split_3x5_3(\n" + "\n".join(formatted_rows) + "\n    )"

    def _format_split_3x6_3(self, keycodes: List[str]) -> str:
        """Format 42-key split 3x6_3 layout"""
        if len(keycodes) != 42:
            raise ValueError(f"Expected 42 keys for 3x6_3 layout, got {len(keycodes)}")

        # Group into rows (6 keys per finger row)
        rows = [
            keycodes[0:6],   # Left hand row 1
            keycodes[6:12],  # Left hand row 2
            keycodes[12:18], # Left hand row 3
            keycodes[18:24], # Right hand row 1
            keycodes[24:30], # Right hand row 2
            keycodes[30:36], # Right hand row 3
            keycodes[36:39], # Left thumbs
            keycodes[39:42], # Right thumbs
        ]

        formatted_rows = []
        for i, row in enumerate(rows):
            if i < 6:  # Finger rows
                formatted_rows.append("        " + ", ".join(f"{k:20}" for k in row) + ",")
            elif i == 6:  # Left thumb row (needs comma)
                formatted_rows.append("                                    " + ", ".join(f"{k:20}" for k in row) + ",")
            else:  # Right thumb row (last row, no comma)
                formatted_rows.append("                                    " + ", ".join(f"{k:20}" for k in row))

        return f"LAYOUT_split_3x6_3(\n" + "\n".join(formatted_rows) + "\n    )"

    def _format_custom_layout(self, board: Board, keycodes: List[str]) -> str:
        """
        Format custom layout (e.g., Lulu, Lily58)

        For custom_58 layouts, we expect 58 keys total.
        Just format them in rows for readability.
        """
        num_keys = len(keycodes)

        # Format in rows of 6 for readability
        rows = []
        for i in range(0, num_keys, 6):
            row = keycodes[i:i+6]
            rows.append("        " + ", ".join(f"{k:20}" for k in row) + ("," if i + 6 < num_keys else ""))

        return f"LAYOUT(\n" + "\n".join(rows) + "\n    )"


    def generate_config_h(
        self,
        board: Board,
        compiled_layers: List[CompiledLayer]
    ) -> str:
        """Generate config.h file"""
        return f"""// AUTO-GENERATED - DO NOT EDIT
// Generated from config/keymap.yaml by scripts/generate.py
// Board: {board.name}

#pragma once

// Include global QMK config if it exists
#ifdef __has_include
#  if __has_include("../../../../../../config/global/config.h")
#    include "../../../../../../config/global/config.h"
#  endif
#endif
"""

    def generate_rules_mk(self, board: Board) -> str:
        """Generate rules.mk file"""
        return f"""# AUTO-GENERATED - DO NOT EDIT
# Generated from config/boards.yaml by scripts/generate.py
# Board: {board.name}

# User name for userspace integration
USER_NAME := dario

# Include board-specific features if they exist
-include $(USER_PATH)/../../config/boards/{board.id}.mk

# Include global QMK rules if they exist
-include $(USER_PATH)/../../config/global/rules.mk
"""

    def generate_visualization(
        self,
        board: Board,
        compiled_layers: List[CompiledLayer]
    ) -> str:
        """
        Generate README.md with ASCII art visualization

        Args:
            board: Target board
            compiled_layers: List of compiled layers

        Returns:
            README.md content with ASCII art layer diagrams
        """
        # Generate basic ASCII art for each layer
        visualizations = []

        for layer in compiled_layers:
            viz = self._generate_layer_ascii(layer, board)
            visualizations.append(f"## {layer.name} Layer\n\n```\n{viz}\n```\n")

        viz_content = "\n".join(visualizations)

        return f"""# Keymap for {board.name}

**Auto-generated from config/keymap.yaml**

Do not edit this file directly. Edit config/keymap.yaml instead and regenerate.

## Build

```bash
qmk compile -kb {board.qmk_keyboard} -km dario
```

## Layers

{viz_content}

---

*Generated by scripts/generate.py*
"""

    def _generate_layer_ascii(self, layer: CompiledLayer, board: Board) -> str:
        """
        Generate ASCII art for a single layer

        This is a simple visualization. For production, consider integrating
        with keymap-drawer or a similar tool.
        """
        keycodes = layer.keycodes

        if board.layout_size == "3x5_3" and len(keycodes) == 36:
            # 36-key layout
            return f"""
╭─────────┬─────────┬─────────┬─────────┬─────────╮   ╭─────────┬─────────┬─────────┬─────────┬─────────╮
│ {keycodes[0]:7} │ {keycodes[1]:7} │ {keycodes[2]:7} │ {keycodes[3]:7} │ {keycodes[4]:7} │   │ {keycodes[15]:7} │ {keycodes[16]:7} │ {keycodes[17]:7} │ {keycodes[18]:7} │ {keycodes[19]:7} │
├─────────┼─────────┼─────────┼─────────┼─────────┤   ├─────────┼─────────┼─────────┼─────────┼─────────┤
│ {keycodes[5]:7} │ {keycodes[6]:7} │ {keycodes[7]:7} │ {keycodes[8]:7} │ {keycodes[9]:7} │   │ {keycodes[20]:7} │ {keycodes[21]:7} │ {keycodes[22]:7} │ {keycodes[23]:7} │ {keycodes[24]:7} │
├─────────┼─────────┼─────────┼─────────┼─────────┤   ├─────────┼─────────┼─────────┼─────────┼─────────┤
│ {keycodes[10]:7} │ {keycodes[11]:7} │ {keycodes[12]:7} │ {keycodes[13]:7} │ {keycodes[14]:7} │   │ {keycodes[25]:7} │ {keycodes[26]:7} │ {keycodes[27]:7} │ {keycodes[28]:7} │ {keycodes[29]:7} │
╰─────────┴─────────┴─────────┼─────────┼─────────┤   ├─────────┼─────────┼─────────┴─────────┴─────────╯
                              │ {keycodes[30]:7} │ {keycodes[31]:7} │   │ {keycodes[34]:7} │ {keycodes[35]:7} │
                              │ {keycodes[32]:7} │         │   │         │         │
                              ╰─────────┴─────────╯   ╰─────────┴─────────╯
"""
        else:
            # Fallback: just list the keycodes
            return "\n".join([f"{i:2d}: {kc}" for i, kc in enumerate(keycodes)])
