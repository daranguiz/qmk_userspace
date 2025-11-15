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
        layer_indices: Optional[Dict[str, int]] = None
    ):
        """
        Initialize translator with behavior aliases and special keycodes

        Args:
            aliases: Dictionary of BehaviorAlias objects
            special_keycodes: Dictionary of special keycode mappings
            layer_indices: Dictionary mapping layer names to indices (for &lt)
        """
        self.aliases = aliases or {}
        self.special_keycodes = special_keycodes or {}
        self.layer_indices = layer_indices or {}

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
            return self.special_keycodes[unified].get('zmk', '&none')

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

        # Simple keycode: A -> &kp A
        return f"&kp {unified}"

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

            # Special handling for layer-tap: convert layer name to index
            if alias_name == 'lt' and param_name == 'layer':
                if param_value in self.layer_indices:
                    param_value = str(self.layer_indices[param_value])
                # Otherwise use the raw value (might be a number already)

            params[param_name] = param_value

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
            valid_mods = ['LGUI', 'RGUI', 'LALT', 'RALT', 'LCTRL', 'RCTRL', 'LSHFT', 'RSHFT']
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
