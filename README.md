[![Build All Firmwares (QMK + ZMK)](https://github.com/daranguiz/qmk_userspace/actions/workflows/build-all.yml/badge.svg)](https://github.com/daranguiz/qmk_userspace/actions/workflows/build-all.yml)

# Keyboard Configuration

Custom keyboard firmware for split ergonomic keyboards using a unified keymap code generation system.

## Combos

### Bootloader Entry (DFU)
- Left hand: `B` + `Q` + `Z`
- Right hand: `P` + `.` + `'`

### GitHub URL
- Keys: `G` + `O` + `U` + `.`
- Outputs: `https://github.com/daranguiz/keyboard-config?tab=readme-ov-file#readme`

## Magic Keys
- Adaptive key powered by `urob/zmk-adaptive-key`; each base layer has its own MAGIC behavior.
- Where to press: Gallium left thumb is `LT(SYM_NIGHT, MAGIC)`, Night left thumb is `MT(LSFT, MAGIC)`.
- Training mode is on by default: typing a mapped bigram directly emits `#` so you learn to use MAGIC. Disable with `python3.11 scripts/generate.py --no-magic-training`.
- Gallium mappings (tap MAGIC after the first key): `B→R`, `A→Y`, `E→Y`, `R→L`, `U→E`, `O→K`, `.`→`/`, `S→C`, `C→S`, `M→B`, `G→S`, `P→H`, `Y→E` (default: repeat).
- Night mappings: `U→E`, `P→Y`, `C→Y`, `Y→'`, `G→Y`, `H→L`, `V→S`, `A→O` (default: repeat).

## Keymap Visualizations

### Split Ergonomic Keyboards

#### NIGHT Layout
![NIGHT Layout](docs/night.svg)

#### Gallium Layout
![Gallium Layout](docs/gallium.svg)

### Row-Staggered Keyboards (macOS .keylayout)

#### Nightlight
![Nightlight Layout](docs/nightlight_rowstagger.svg)

#### Rain
![Rain Layout](docs/rain_rowstagger.svg)

#### Sturdy
![Sturdy Layout](docs/sturdy_rowstagger.svg)

## About

This repository uses a unified YAML configuration to generate keymaps for both QMK and ZMK firmware. All keymaps are defined in `config/keymap.yaml` and automatically generated for each keyboard.

See [CLAUDE.md](CLAUDE.md) for detailed documentation.
