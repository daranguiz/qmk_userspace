"""
ZMK keycode translator

Translates unified keymap syntax to ZMK devicetree syntax
"""

import re
from typing import Dict, Optional
from data_model import BehaviorAlias, ValidationError


class ZMKTranslator:
    """Translate unified syntax to ZMK devicetree syntax"""

    def __init__(
        self,
        aliases: Optional[Dict[str, BehaviorAlias]] = None,
        special_keycodes: Optional[Dict[str, Dict[str, str]]] = None,
        layer_indices: Optional[Dict[str, int]] = None,
        layout_size: Optional[str] = None
    ):
        """
        Initialize translator with behavior aliases and special keycodes

        Args:
            aliases: Dictionary of BehaviorAlias objects
            special_keycodes: Dictionary of special keycode mappings
            layer_indices: Dictionary mapping layer names to indices (for &lt)
            layout_size: Board layout size (e.g., "3x5_3", "3x6_3") for position-aware translation
        """
        self.aliases = aliases or {}
        self.special_keycodes = special_keycodes or {}
        self.layer_indices = layer_indices or {}
        self.layout_size = layout_size
        self.current_key_index = 0  # Track current key position for context-aware translation

    def translate(self, unified) -> str:
        """
        Translate unified keycode to ZMK devicetree syntax

        Examples:
        - "A" -> "&kp A"
        - "hrm:LGUI:A" -> "&hrm LGUI A"
        - "lt:NAV:SPC" -> "&lt NAV SPC"
        - "NONE" -> "&none"
        - "bt:next" -> "&bt BT_NXT"

        Args:
            unified: Unified keycode (string or int)

        Returns:
            ZMK devicetree string

        Raises:
            ValidationError: If keycode is invalid or unsupported
        """
        # Convert to string if needed
        unified = str(unified)

        # Handle special keycodes
        if unified in self.special_keycodes:
            value = self.special_keycodes[unified].get('zmk', '&none')
            return value if value else "&none"  # Treat empty string as unsupported

        # Handle aliased behaviors (e.g., hrm:LGUI:A, lt:NAV:SPC)
        if ':' in unified:
            return self._translate_alias(unified)

        # Handle KC_ prefixed keycodes: KC_A -> &kp A
        if unified.startswith('KC_'):
            key = unified[3:]  # Remove KC_ prefix
            return f"&kp {key}"

        # Handle QK_ prefixed keycodes (QMK-specific)
        if unified.startswith('QK_'):
            # Map QMK-specific codes to ZMK equivalents
            qk_map = {
                'QK_BOOT': '&bootloader',
                'QK_RBT': '&sys_reset',
            }
            return qk_map.get(unified, '&none')

        # Handle Bluetooth keycodes (ZMK-specific)
        if unified.startswith('BT_'):
            bt_map = {
                'BT_SEL_0': '&bt BT_SEL 0',
                'BT_SEL_1': '&bt BT_SEL 1',
                'BT_SEL_2': '&bt BT_SEL 2',
                'BT_SEL_3': '&bt BT_SEL 3',
                'BT_SEL_4': '&bt BT_SEL 4',
                'BT_CLR': '&bt BT_CLR',
                'BT_NXT': '&bt BT_NXT',
                'BT_PRV': '&bt BT_PRV',
            }
            return bt_map.get(unified, '&none')

        # Handle RGB keycodes (QMK-specific, filter out for ZMK)
        if unified.startswith('RM_') or unified.startswith('RGB_'):
            # RGB keycodes don't exist in ZMK, return none
            return '&none'

        # Map QMK keycodes to ZMK equivalents
        zmk_key = self._map_qmk_key_to_zmk(unified)

        # Simple keycode: A -> &kp A
        return f"&kp {zmk_key}"

    def _map_qmk_key_to_zmk(self, key: str) -> str:
        """Map QMK-style key tokens to ZMK equivalents (including nums/symbols)."""
        qmk_to_zmk = {
            'SLSH': 'FSLH',  # Forward slash
            'QUOT': 'SQT',   # Single quote (apostrophe)
            'COMM': 'COMMA',
            'RGHT': 'RIGHT',
            'ALGR': 'RALT',
            'BSLS': 'BSLH',  # Backslash
            'GRV': 'GRAVE',
            'DLR': 'DOLLAR',
            'PERC': 'PERCENT',
            'CIRC': 'CARET',
            'AMPR': 'AMPERSAND',
            'ASTR': 'ASTERISK',
            'EXLM': 'EXCL',
            'LCBR': 'LBRC',
            'RCBR': 'RBRC',
            'MINS': 'MINUS',
            'UNDS': 'UNDERSCORE',
            'MNXT': 'C_NEXT',
            'MPRV': 'C_PREV',
            'MSTP': 'C_STOP',
            'MPLY': 'C_PLAY_PAUSE',
            'MUTE': 'C_MUTE',
            'PSCR': 'PRINTSCREEN',
            'SCRL': 'SCROLLLOCK',
            'ENT': 'ENTER',
            'APP': 'K_APP',
            # Explicit number mappings to avoid bare numeric tokens in DT
            '0': 'N0',
            '1': 'N1',
            '2': 'N2',
            '3': 'N3',
            '4': 'N4',
            '5': 'N5',
            '6': 'N6',
            '7': 'N7',
            '8': 'N8',
            '9': 'N9',
        }
        return qmk_to_zmk.get(key, key)

    def _translate_alias(self, unified: str) -> str:
        """
        Translate aliased behavior to ZMK syntax

        Args:
            unified: Aliased keycode (e.g., "hrm:LGUI:A")

        Returns:
            ZMK devicetree string

        Raises:
            ValidationError: If alias is unknown or firmware incompatible
        """
        parts = unified.split(':')
        alias_name = parts[0]

        # Check if alias exists
        if alias_name not in self.aliases:
            # Unknown alias - might be a QMK-specific feature
            if alias_name in ['rgb', 'bl']:  # QMK-specific
                return "&none"  # Filter QMK-specific
            raise ValidationError(f"Unknown behavior alias: {alias_name}")

        alias = self.aliases[alias_name]

        # Check if alias is supported in ZMK
        if 'zmk' not in alias.firmware_support:
            return "&none"  # Filter unsupported

        # Validate parameter count
        if len(parts) - 1 != len(alias.params):
            raise ValidationError(
                f"Alias {alias_name} expects {len(alias.params)} parameters, "
                f"got {len(parts) - 1}"
            )

        # Build parameter dict
        params = {}
        for i, param_name in enumerate(alias.params):
            param_value = parts[i + 1]
            # ZMK uses layer name #defines (e.g., &lt FUN X), not numeric indices
            # The #defines are generated in the keymap file header
            if param_name == 'key':
                params[param_name] = self._map_qmk_key_to_zmk(param_value)
            else:
                params[param_name] = param_value

        # Special handling for hrm: use position-aware behavior (hml vs hmr)
        if alias_name == 'hrm':
            is_left_hand = self._is_left_hand_key(self.current_key_index)
            behavior = 'hml' if is_left_hand else 'hmr'
            # Return position-specific behavior instead of generic hrm
            return f"&{behavior} {params['mod']} {params['key']}"

        # Translate using alias pattern
        return alias.translate_zmk(**params)

    def validate_keybinding(self, unified, layer_name: str) -> None:
        """
        Validate complex keybinding for ZMK compatibility (FR-007)

        This performs strict validation to ensure complex keybindings
        (homerow mods, layer-taps, etc.) are compatible with ZMK.

        Args:
            unified: Unified keycode (string or int)
            layer_name: Layer name (for error context)

        Raises:
            ValidationError: If keybinding is incompatible with ZMK
        """
        # Convert to string if needed
        unified = str(unified)

        # If it's a simple keycode, no validation needed
        if ':' not in unified:
            return

        # Parse alias
        parts = unified.split(':')
        alias_name = parts[0]

        # Check if alias exists
        if alias_name not in self.aliases:
            # Check for known QMK-only features
            if alias_name in ['rgb', 'bl']:
                # This is OK - will be filtered silently
                return
            raise ValidationError(
                f"Layer {layer_name}: Unknown behavior alias '{alias_name}' "
                f"in keycode '{unified}'"
            )

        alias = self.aliases[alias_name]

        # Check firmware support
        if 'zmk' not in alias.firmware_support:
            # This is a QMK-only feature - OK, will be filtered
            return

        # Validate parameter count
        if len(parts) - 1 != len(alias.params):
            raise ValidationError(
                f"Layer {layer_name}: Alias '{alias_name}' expects "
                f"{len(alias.params)} parameters, got {len(parts) - 1} "
                f"in keycode '{unified}'"
            )

        # Additional ZMK-specific validation
        # For example, validate modifier names for homerow mods
        if alias_name == 'hrm':
            mod = parts[1]
            # Accept both QMK and ZMK modifier names
            valid_mods = ['LGUI', 'RGUI', 'LALT', 'RALT', 'LCTRL', 'RCTRL', 'LSHFT', 'RSHFT',
                         'LCTL', 'RCTL', 'LSFT', 'RSFT']  # Also accept QMK shorthand
            if mod not in valid_mods:
                raise ValidationError(
                    f"Layer {layer_name}: Invalid modifier '{mod}' in '{unified}'. "
                    f"Valid modifiers: {', '.join(valid_mods)}"
                )

    def set_layer_indices(self, layer_names: list):
        """
        Set layer name to index mapping for &lt translation

        Args:
            layer_names: Ordered list of layer names
        """
        self.layer_indices = {name: idx for idx, name in enumerate(layer_names)}

    def set_key_index(self, index: int):
        """
        Set current key index for position-aware translation

        Args:
            index: Current key position in the layout (0-based)
        """
        self.current_key_index = index

    def _is_left_hand_key(self, key_index: int) -> bool:
        """
        Determine if a key position is on the left hand

        Args:
            key_index: Key position (0-based)

        Returns:
            True if key is on left hand, False if on right hand
        """
        if self.layout_size == "3x5_3":
            # 36 keys: 0-14 left hand (3x5), 15-29 right hand (3x5), 30-32 left thumbs, 33-35 right thumbs
            return key_index < 15 or (30 <= key_index < 33)
        elif self.layout_size == "3x6_3":
            # 42 keys: 0-17 left hand (3x6), 18-35 right hand (3x6), 36-38 left thumbs, 39-41 right thumbs
            return key_index < 18 or (36 <= key_index < 39)
        else:
            # Default: assume first half is left hand
            return key_index < 21  # Default to 42-key layout
