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

Training is on: typing a mapped bigram directly emits `#`; disable with `python3.11 scripts/generate.py --no-magic-training`.

Gallium (default: repeat):

| First key | Magic output |
| --------- | ------------ |
| .         | /            |
| A         | Y            |
| B         | R            |
| C         | S            |
| D         | --           |
| E         | Y            |
| F         | --           |
| G         | S            |
| H         | --           |
| I         | --           |
| J         | --           |
| K         | --           |
| L         | --           |
| M         | B            |
| N         | --           |
| O         | K            |
| P         | H            |
| Q         | --           |
| R         | L            |
| S         | C            |
| T         | --           |
| U         | E            |
| V         | --           |
| W         | --           |
| X         | --           |
| Y         | E            |
| Z         | --           |

Night (default: repeat):

| First key | Magic output |
| --------- | ------------ |
| (space)   | THE          |
| ,         |  BUT         |
| -         | >            |
| .         | /            |
| A         | O            |
| B         | --           |
| C         | Y            |
| D         | --           |
| E         | --           |
| F         | --           |
| G         | Y            |
| H         | L            |
| I         | ON           |
| J         | UST          |
| K         | --           |
| L         | --           |
| M         | ENT          |
| N         | --           |
| O         | A            |
| P         | Y            |
| Q         | UE           |
| R         | --           |
| S         | --           |
| T         | ION          |
| U         | E            |
| V         | S            |
| W         | HAT          |
| X         | --           |
| Y         | '            |
| Z         | --           |

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
