# keymap-drawer Issue with QMK External Userspace and Macro-Based Keymaps

## Problem Summary

I'm unable to generate keymap visualizations using `keymap-drawer` for my QMK External Userspace setup because the tool cannot handle my modular, macro-based keymap system.

## Environment

- **QMK Version**: 0.30.10
- **keymap-drawer Version**: 0.21.0
- **Setup**: QMK External Userspace (qmk_userspace repo separate from qmk_firmware)
- **Keyboards**: bastardkb/skeletyl/promicro, boardsource/lulu/rp2040, lily58/rev1

## Architecture

My keymap uses a modular design with wrapper macros to maintain a single source of truth:

### File Structure
```
qmk_userspace/
├── users/dario/
│   ├── layers.h          # Single source of truth - LAYER_BASE, LAYER_NAV, etc.
│   └── dario.h           # Layer enum and shared constants
├── keyboards/*/keymaps/dario/
│   ├── keymap.c          # Uses LAYOUT_wrapper(LAYER_*)
│   └── keymap_config.h   # Defines LAYOUT_wrapper macro
```

### Code Example

**users/dario/layers.h:**
```c
#define LAYER_BASE \
    KC_Q, KC_W, KC_F, KC_P, KC_G, KC_J, KC_L, KC_U, KC_Y, KC_QUOT, \
    LGUI_T(KC_A), LALT_T(KC_R), LCTL_T(KC_S), LSFT_T(KC_T), KC_D, /* ... */
```

**keyboards/bastardkb/skeletyl/keymaps/dario/keymap_config.h:**
```c
#define LAYOUT_wrapper(...) LAYOUT_split_3x5_3(__VA_ARGS__)
```

**keyboards/bastardkb/skeletyl/keymaps/dario/keymap.c:**
```c
#include QMK_KEYBOARD_H
#include "keymap_config.h"

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [BASE]   = LAYOUT_wrapper(LAYER_BASE),
    [NAV]    = LAYOUT_wrapper(LAYER_NAV),
    [MEDIA]  = LAYOUT_wrapper(LAYER_MEDIA),
    [NUM]    = LAYOUT_wrapper(LAYER_NUM),
    [SYM]    = LAYOUT_wrapper(LAYER_SYM),
    [FUN]    = LAYOUT_wrapper(LAYER_FUN)
};
```

## The Issue

### Option 1: Using `qmk c2json` WITH preprocessing (default)

**Command:**
```bash
qmk c2json -kb bastardkb/skeletyl/promicro -km dario
```

**Error:**
```
☐ Running command: ['cpp', '/Users/dario/git/qmk_userspace/keyboards/bastardkb/skeletyl/keymaps/dario/keymap.c']
☐ The C pre-processor ran into a fatal error:
  /Users/dario/git/qmk_userspace/keyboards/bastardkb/skeletyl/keymaps/dario/keymap_config.h:3:10:
  fatal error: 'dario.h' file not found
☒ Something went wrong. Try to use --no-cpp.
```

**Problem**: The C preprocessor cannot find userspace headers (users/dario/dario.h, users/dario/layers.h) because they're in a different directory structure.

### Option 2: Using `qmk c2json --no-cpp`

**Command:**
```bash
qmk c2json -kb bastardkb/skeletyl/promicro -km dario --no-cpp
```

**Output:**
```json
{
  "keyboard": "bastardkb/skeletyl/promicro",
  "layout": "LAYOUT_wrapper",
  "layers": [
    ["LAYER_BASE"],
    ["LAYER_NAV"],
    ["LAYER_MEDIA"],
    ["LAYER_NUM"],
    ["LAYER_SYM"],
    ["LAYER_FUN"]
  ]
}
```

**Problem**: Without preprocessing, the macros aren't expanded:
- Each layer shows as a single element (the macro name) instead of 36 individual keycodes
- `LAYOUT_wrapper` is not recognized as a valid layout (keymap-drawer expects `LAYOUT_split_3x5_3`)
- keymap-drawer reports: `Could not find layout "LAYOUT_wrapper" in available physical layouts`

### What keymap-drawer Needs

keymap-drawer expects fully expanded keymaps like this:

```json
{
  "keyboard": "bastardkb/skeletyl/promicro",
  "layout": "LAYOUT_split_3x5_3",
  "layers": [
    [
      "KC_Q", "KC_W", "KC_F", "KC_P", "KC_G",
      "KC_J", "KC_L", "KC_U", "KC_Y", "KC_QUOT",
      "LGUI_T(KC_A)", "LALT_T(KC_R)", /* ... 36 keys total */
    ],
    /* ... more layers */
  ]
}
```

## What I've Tried

1. ✅ **Clean qmk_firmware**: Reset qmk_firmware to upstream/master to remove any stale keymaps
2. ❌ **Manual macro replacement**: Temporarily replacing `LAYOUT_wrapper` with `LAYOUT_split_3x5_3` fails because `LAYER_*` macros still aren't expanded
3. ❌ **Using compiled output**: Build artifacts don't contain the expanded JSON format needed
4. ✅ **Configuration**: Successfully configured keymap-drawer with custom layer names and highlighting styles

## Current Workaround Needs

I need ONE of the following solutions:

### Solution A: Make `qmk c2json` preprocessing work
- How can I make the C preprocessor find userspace headers during `qmk c2json`?
- Is there a flag to specify include paths?
- Can I temporarily modify the build environment?

### Solution B: Pre-process before c2json
- Can I manually run `cpp` with the correct include paths?
- What include paths does QMK use during compilation?
- How can I generate the preprocessed keymap.c file?

### Solution C: Alternative visualization tool
- Is there a different QMK keymap visualization tool that handles macros better?
- Can keymap-drawer be configured to expand macros?

### Solution D: Generate flat keymap just for visualization
- Script to automatically expand `LAYER_*` macros into a flat keymap.c
- This would be for visualization only, not actual firmware

## Desired Configuration

I have successfully configured (but cannot test due to preprocessing issue):

**.keymap-drawer-config.yaml:**
```yaml
parse_config:
  qmk_remove_keycode_prefix:
    - "KC_"
  mark_alternate_layer_activators: true
  layer_legend_map:
    "BASE": "BASE"
    "NAV": "NAV"
    "MEDIA": "MEDIA"
    "NUM": "NUM"
    "SYM": "SYM"
    "FUN": "FUN"

draw_config:
  ortho_layout:
    split: true
    rows: 3
    columns: 5
    thumbs: 3
  svg_extra_style: |
    rect.held {
      fill: #ffeb3b;
      stroke: #f57c00;
      stroke-width: 2;
    }
    rect.held.alternate {
      fill: #fff9c4;
      stroke: #f57c00;
      stroke-width: 1.5;
    }
```

**Generation script:**
```bash
qmk c2json -kb "$KEYBOARD" -km "$KEYMAP" --no-cpp 2>/dev/null | \
  keymap -c "$CONFIG" parse --layer-names BASE NAV MEDIA NUM SYM FUN -q - | \
  keymap -c "$CONFIG" draw - > "$OUTPUT_FILE"
```

## Question

**How can I generate keymap visualizations with keymap-drawer when using a modular, macro-based QMK External Userspace setup?**

Any guidance on making preprocessing work or alternative approaches would be greatly appreciated!
