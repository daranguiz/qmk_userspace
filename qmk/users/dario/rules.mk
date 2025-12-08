# Shared feature flags for all keyboards
BOOTMAGIC_ENABLE = yes      # Enable Bootmagic Lite
EXTRAKEY_ENABLE = yes       # Audio control and System control
NKRO_ENABLE = yes           # N-Key Rollover
LTO_ENABLE = yes            # Link Time Optimization for smaller firmware

# User preference features
COMBO_ENABLE = yes          # Key combos
CONSOLE_ENABLE = no         # Console off by default (enable per-board if supported)
COMMAND_ENABLE = no         # Commands for debug and configuration

# Include shared source files
SRC += dario.c
