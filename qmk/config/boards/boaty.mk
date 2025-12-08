# Board-specific QMK features for Jels Boaty
# This file is manually maintained

# Boaty is NOT a split keyboard
SPLIT_KEYBOARD = no

# Basic features
MOUSEKEY_ENABLE = yes       # Mouse keys

# V-USB limitation: console shares endpoint with mouse/extra keys
override CONSOLE_ENABLE = no

# Features not used on Boaty
OLED_ENABLE = no
RGB_MATRIX_ENABLE = no
ENCODER_ENABLE = no
