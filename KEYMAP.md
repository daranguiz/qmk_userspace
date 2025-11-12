# Keymap Documentation

Complete documentation of the dario keymap configuration used across all keyboards.

## Overview

This keymap uses a **36-key Colemak layout** with home row mods, optimized for Mac with Cmd-based clipboard shortcuts. The core 3x5+3 layout is shared across all keyboards via QMK External Userspace.

**Base Layout**: Colemak-DH
**Modifier Philosophy**: Home row mods (GACS pattern)
**Layer System**: 8 layers (BASE, NAV, MOUSE, MEDIA, NUM, SYM, FUN, BUTTON)
**Clipboard**: Mac-optimized (Cmd-based shortcuts)

## Keyboards Using This Keymap

| Keyboard | Physical Keys | Core Layout | Extra Features |
|----------|---------------|-------------|----------------|
| **Bastard Keyboards Skeletyl** | 36 (3x5+3) | Native 36-key | None |
| **Boardsource Lulu** | 58 (6x4+4 thumbs) | 36-key core via wrapper | OLED, RGB Matrix |
| **Lily58** | 58 (6x4+4 thumbs) | 36-key core via wrapper | OLED (Luna pet), WPM tracking |

**Visualization**: [Skeletyl Keymap SVG](docs/keymaps/bastardkb_skeletyl_promicro_dario.svg)

---

## Layer Definitions

### Layer 0: BASE (Colemak-DH)

Primary typing layer with home row modifiers.

```
┌─────┬─────┬─────┬─────┬─────┐       ┌─────┬─────┬─────┬─────┬─────┐
│  Q  │  W  │  F  │  P  │  G  │       │  J  │  L  │  U  │  Y  │  '  │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│GUI/A│ALT/R│CTL/S│SFT/T│  D  │       │  H  │SFT/N│CTL/E│ALT/I│GUI/O│
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│BTN/Z│FUN/X│  C  │  V  │  B  │       │  K  │  M  │  ,  │AGR/.│BTN//│
└─────┴─────┴─────┼─────┼─────┤       ├─────┼─────┼─────┴─────┴─────┘
                  │ ENT │NAV/ │       │SYM/ │LSFT │
                  │     │ SPC │       │ DEL │     │
                  └─────┴─────┘       ├─────┼─────┤
                         │MED/ │       │NUM/ │
                         │ TAB │       │BSPC │
                         └─────┘       └─────┘
```

**Home Row Mods**:
- Left hand: LGUI (A), LALT (R), LCTL (S), LSFT (T)
- Right hand: LSFT (N), LCTL (E), LALT (I), LGUI (O)

**Layer Access**:
- Thumb keys use Layer-Tap for layer activation when held
- BUTTON layer accessed via pinky (Z, /)

---

### Layer 1: NAV (Navigation)

Arrow keys, page navigation, and clipboard operations.

```
┌─────┬─────┬─────┬─────┬─────┐       ┌─────┬─────┬─────┬─────┬─────┐
│     │     │     │     │     │       │ RDO │ PST │ CPY │ CUT │ UND │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│ GUI │ ALT │ CTL │ SFT │     │       │CAPS │  ←  │  ↓  │  ↑  │  →  │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│ UND │ CUT │ CPY │ PST │     │       │ INS │HOME │PGDN │PGUP │ END │
└─────┴─────┴─────┼─────┼─────┤       ├─────┼─────┼─────┴─────┴─────┘
                  │     │     │       │ DEL │ ENT │
                  │     │ HLD │       │     │     │
                  └─────┴─────┘       ├─────┼─────┤
                         │     │       │BSPC │
                         │     │       │     │
                         └─────┘       └─────┘
```

**Clipboard Shortcuts** (Mac):
- UND: Cmd+Z (Undo)
- RDO: Cmd+Shift+Z (Redo)
- CUT: Cmd+X (Cut)
- CPY: Cmd+C (Copy)
- PST: Cmd+V (Paste)

---

### Layer 2: MOUSE

Mouse movement, scrolling, and button clicks.

```
┌─────┬─────┬─────┬─────┬─────┐       ┌─────┬─────┬─────┬─────┬─────┐
│     │     │     │     │     │       │ RDO │ PST │ CPY │ CUT │ UND │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│ GUI │ ALT │ CTL │ SFT │     │       │     │  ←  │  ↓  │  ↑  │  →  │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│     │ AGR │     │     │     │       │     │ W← │ W↓ │ W↑ │ W→ │
└─────┴─────┴─────┼─────┼─────┤       ├─────┼─────┼─────┴─────┴─────┘
                  │     │     │       │LCLK │MCLK │
                  │     │     │       │     │     │
                  └─────┴─────┘       ├─────┼─────┤
                         │     │       │RCLK │
                         │ HLD │       │     │
                         └─────┘       └─────┘
```

**Mouse Controls**:
- Arrows: Mouse cursor movement
- W←↓↑→: Mouse wheel scrolling
- LCLK/RCLK/MCLK: Left/Right/Middle click

---

### Layer 3: MEDIA

Media controls, RGB lighting, and volume.

```
┌─────┬─────┬─────┬─────┬─────┐       ┌─────┬─────┬─────┬─────┬─────┐
│     │     │     │     │     │       │ RGB │MODE │ HUE+│ SAT+│ VAL+│
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│ GUI │ ALT │ CTL │ SFT │     │       │     │ ⏮  │ VOL-│ VOL+│  ⏭  │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│     │ AGR │     │     │     │       │     │     │     │     │     │
└─────┴─────┴─────┼─────┼─────┤       ├─────┼─────┼─────┴─────┴─────┘
                  │     │     │       │ ⏹  │  ⏯  │
                  │     │     │       │     │     │
                  └─────┴─────┘       ├─────┼─────┤
                         │ HLD │       │ 🔇 │
                         │     │       │     │
                         └─────┘       └─────┘
```

**Media Keys**:
- ⏮/⏭: Previous/Next track
- ⏯: Play/Pause
- ⏹: Stop
- VOL-/VOL+: Volume down/up
- 🔇: Mute

**RGB Controls** (if hardware supports):
- RGB: Toggle RGB lighting
- MODE: Cycle RGB modes
- HUE+: Increase hue
- SAT+: Increase saturation
- VAL+: Increase brightness

---

### Layer 4: NUM (Numbers & Numpad)

Number row and numpad-style layout on the left hand.

```
┌─────┬─────┬─────┬─────┬─────┐       ┌─────┬─────┬─────┬─────┬─────┐
│  [  │  4  │  5  │  6  │  ]  │       │     │     │     │     │     │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│  ;  │  1  │  2  │  3  │  =  │       │     │ SFT │ CTL │ ALT │ GUI │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│  `  │  7  │  8  │  9  │  \  │       │     │     │     │ AGR │     │
└─────┴─────┴─────┼─────┼─────┤       ├─────┼─────┼─────┴─────┴─────┘
                  │  .  │  0  │       │     │     │
                  │     │     │       │     │     │
                  └─────┴─────┘       ├─────┼─────┤
                         │  -  │       │     │
                         │     │       │ HLD │
                         └─────┘       └─────┘
```

**Layout**: Numpad-style on left hand, modifiers on right.

---

### Layer 5: SYM (Symbols)

Shifted number row symbols and special characters.

```
┌─────┬─────┬─────┬─────┬─────┐       ┌─────┬─────┬─────┬─────┬─────┐
│  {  │  $  │  %  │  ^  │  }  │       │     │     │     │     │     │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│  :  │  !  │  @  │  #  │  +  │       │     │ SFT │ CTL │ ALT │ GUI │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│  ~  │  &  │  *  │  (  │  |  │       │     │     │     │ AGR │     │
└─────┴─────┴─────┼─────┼─────┤       ├─────┼─────┼─────┴─────┴─────┘
                  │  (  │  )  │       │     │     │
                  │     │     │       │ HLD │     │
                  └─────┴─────┘       ├─────┼─────┤
                         │  _  │       │     │
                         │     │       │     │
                         └─────┘       └─────┘
```

**Common Symbols**: All shifted number row characters plus brackets and operators.

---

### Layer 6: FUN (Function Keys)

Function keys F1-F12 plus system keys.

```
┌─────┬─────┬─────┬─────┬─────┐       ┌─────┬─────┬─────┬─────┬─────┐
│ F12 │ F7  │ F8  │ F9  │PSCR │       │     │     │     │     │     │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│ F11 │ F4  │ F5  │ F6  │SCRL │       │     │ SFT │ CTL │ ALT │ GUI │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│ F10 │ F1  │ F2  │ F3  │PAUS │       │     │     │     │ AGR │     │
└─────┴─────┴─────┼─────┼─────┤       ├─────┼─────┼─────┴─────┴─────┘
                  │ APP │ SPC │       │     │     │
                  │     │     │       │     │     │
                  └─────┴─────┘       ├─────┼─────┤
                         │ TAB │       │     │
                         │     │       │     │
                         └─────┘       └─────┘
```

**System Keys**:
- PSCR: Print Screen
- SCRL: Scroll Lock
- PAUS: Pause/Break
- APP: Application/Menu key

---

### Layer 7: BUTTON

Clipboard shortcuts and mouse buttons mirrored on both hands for easy access.

```
┌─────┬─────┬─────┬─────┬─────┐       ┌─────┬─────┬─────┬─────┬─────┐
│ UND │ CUT │ CPY │ PST │ RDO │       │ RDO │ PST │ CPY │ CUT │ UND │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│ GUI │ ALT │ CTL │ SFT │ TRN │       │ TRN │ SFT │ CTL │ ALT │ GUI │
├─────┼─────┼─────┼─────┼─────┤       ├─────┼─────┼─────┼─────┼─────┤
│ UND │ CUT │ CPY │ PST │ RDO │       │ RDO │ PST │ CPY │ CUT │ UND │
└─────┴─────┴─────┼─────┼─────┤       ├─────┼─────┼─────┴─────┴─────┘
                  │RCLK │MCLK │       │LCLK │LCLK │
                  │     │     │       │     │     │
                  └─────┴─────┘       ├─────┼─────┤
                         │LCLK │       │MCLK │
                         │     │       │     │
                         └─────┘       └─────┘
```

**Purpose**: Quick access to clipboard operations and mouse buttons without layer switching.

---

## Configuration Details

### Tapping Terms

| Setting | Value | Description |
|---------|-------|-------------|
| Base Tapping Term | 200ms | Default for all tap-hold keys |
| Home Row Mods Term | 300ms | `TAPPING_TERM_HRM` for A/R/S/T/N/E/I/O |
| Permissive Hold | Enabled | With `TAPPING_TERM_PER_KEY` |

### QMK Features

| Feature | Status | Description |
|---------|--------|-------------|
| `CHORDAL_HOLD` | Enabled | Opposite hand rule for mod-tap keys |
| `TAPPING_FORCE_HOLD` | Enabled | Rapid tap-to-hold transitions |
| `LTO_ENABLE` | Enabled | Link-time optimization |
| `QMK_KEYS_PER_SCAN` | 4 | Optimized for heavy chording |
| `BOOTMAGIC_ENABLE` | Yes | Bootmagic lite |
| `MOUSEKEY_ENABLE` | Yes | Mouse keys support |
| `NKRO_ENABLE` | Yes | N-Key Rollover |

### Custom Keycodes

| Keycode | Expansion | Description |
|---------|-----------|-------------|
| `U_UND` | Cmd+Z | Undo (Mac) |
| `U_RDO` | Cmd+Shift+Z | Redo (Mac) |
| `U_CUT` | Cmd+X | Cut (Mac) |
| `U_CPY` | Cmd+C | Copy (Mac) |
| `U_PST` | Cmd+V | Paste (Mac) |
| `U_NA` | KC_NO | Not available |
| `U_NU` | KC_NO | Not used |
| `U_NP` | KC_NO | Non-present |

### Mouse Controls

| Keycode | Description |
|---------|-------------|
| `MS_LEFT` | Move cursor left |
| `MS_DOWN` | Move cursor down |
| `MS_UP` | Move cursor up |
| `MS_RGHT` | Move cursor right |
| `MS_BTN1` | Left click |
| `MS_BTN2` | Right click |
| `MS_BTN3` | Middle click |
| `MS_WHLL` | Wheel left |
| `MS_WHLD` | Wheel down |
| `MS_WHLU` | Wheel up |
| `MS_WHLR` | Wheel right |

### RGB Controls (Hardware Dependent)

| Keycode | Description |
|---------|-------------|
| `RM_TOGG` | Toggle RGB |
| `RM_NEXT` | Next RGB mode |
| `RM_HUEU` | Increase hue |
| `RM_SATU` | Increase saturation |
| `RM_VALU` | Increase brightness |

---

## Build Information

### Compilation

```bash
# Build all keyboards
./build_all.sh

# Or individually
qmk compile -kb bastardkb/skeletyl/promicro -km dario
qmk compile -kb boardsource/lulu/rp2040 -km dario
qmk compile -kb lily58/rev1 -km dario
```

### Firmware Sizes

| Keyboard | Flash Used | Total | Percentage | Free |
|----------|-----------|-------|------------|------|
| Skeletyl | 17,038 bytes | 28,672 bytes | 59% | 11,634 bytes |
| Lulu | N/A | RP2040 | - | No limit |
| Lily58 | 22,882 bytes | 28,672 bytes | 79% | 5,790 bytes |

---

## Hardware-Specific Features

### Lulu

- **OLED Display**: Shows current layer name and active modifiers
- **RGB Matrix**: Full per-key RGB lighting support
- **Display Orientation**: 270° rotation
- **Master/Slave**: Different display content per half

### Lily58

- **OLED Display**: Luna pet animation with WPM tracking
- **Animation States**: Sit, walk, run based on typing speed
- **WPM Thresholds**: Walk >10 WPM, Run >40 WPM
- **Display Features**: Layer name, Luna animation, WPM counter

### Skeletyl

- **Pure 36-key**: No extra features, minimal firmware
- **Native 3x5+3**: No layout wrapper needed
- **Smallest Size**: 17KB firmware (59% of available space)

---

## Design Philosophy

### Home Row Mods

The GACS pattern (GUI, Alt, Ctrl, Shift) is used on the home row for ergonomic modifier access:

- **Left hand**: A=GUI, R=Alt, S=Ctrl, T=Shift
- **Right hand**: N=Shift, E=Ctrl, I=Alt, O=GUI

This allows modifiers to be pressed with minimal finger movement while maintaining comfortable typing.

### Chordal Hold

The `CHORDAL_HOLD` feature enables "opposite hand rule" - tap-hold keys only trigger the hold action when another key on the opposite hand is pressed. This prevents accidental modifier activation while typing normally.

### Layer-Tap Thumbs

All thumb keys use Layer-Tap functionality:
- **Tap**: Regular key (Enter, Space, Tab, Delete, Shift, Backspace)
- **Hold**: Activate layer (NAV, MEDIA, MOUSE, SYM, NUM, FUN)

### Mac Optimization

All clipboard shortcuts use Cmd key instead of Ctrl, optimized for macOS:
- Standard shortcuts: Cmd+Z/X/C/V
- Redo uses Cmd+Shift+Z (Mac convention)

---

## File Locations

### Shared Code (Single Source of Truth)
- **Layer definitions**: `users/dario/layers.h`
- **Custom keycodes**: `users/dario/dario.h`
- **Keycode handlers**: `users/dario/dario.c`
- **Shared config**: `users/dario/config.h`
- **Shared features**: `users/dario/rules.mk`

### Per-Keyboard Code
- **Skeletyl**: `keyboards/bastardkb/skeletyl/keymaps/dario/`
- **Lulu**: `keyboards/boardsource/lulu/keymaps/dario/`
- **Lily58**: `keyboards/lily58/keymaps/dario/`

### Build Configuration
- **Build targets**: `qmk.json`
- **Build script**: `build_all.sh`
- **Visualization config**: `.keymap-drawer-config.yaml`

---

## Modification Guide

### Changing a Key on All Keyboards

Edit `users/dario/layers.h` and rebuild:

```bash
# Edit the layer definition
vim users/dario/layers.h

# Rebuild all keyboards
./build_all.sh
```

The change will automatically apply to all three keyboards.

### Adding a Keyboard-Specific Feature

Example: Adding encoder support to a keyboard

```makefile
# In keyboards/<keyboard>/keymaps/dario/rules.mk
ENCODER_ENABLE = yes
```

```c
// In keyboards/<keyboard>/keymaps/dario/keymap.c
bool encoder_update_user(uint8_t index, bool clockwise) {
    // Your encoder logic
    return true;
}
```

### Customizing OLED Display

Each keyboard can have its own OLED implementation:
- Edit `keyboards/<keyboard>/keymaps/dario/oled.c`
- Modify `oled_task_user()` function
- Rebuild specific keyboard

---

## References

- **QMK Documentation**: https://docs.qmk.fm
- **Miryoku Layout**: Inspiration for layer design
- **External Userspace**: https://docs.qmk.fm/newbs_external_userspace
- **Project Constitution**: `.specify/memory/constitution.md`
- **Implementation Guide**: `CLAUDE.md`
