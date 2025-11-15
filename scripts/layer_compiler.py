"""
Layer compiler

Compiles layers by applying extensions and translating keycodes
"""

from typing import List, Union
from data_model import Layer, Board, CompiledLayer, ValidationError
from qmk_translator import QMKTranslator
from zmk_translator import ZMKTranslator


class LayerCompiler:
    """Compiles layers for specific boards and firmwares"""

    def __init__(self, qmk_translator: QMKTranslator, zmk_translator: ZMKTranslator):
        """
        Initialize compiler with translators

        Args:
            qmk_translator: QMK keycode translator
            zmk_translator: ZMK keycode translator
        """
        self.qmk_translator = qmk_translator
        self.zmk_translator = zmk_translator

    def compile_layer(
        self,
        layer: Layer,
        board: Board,
        firmware: str
    ) -> CompiledLayer:
        """
        Compile a layer for a specific board and firmware

        This applies the following transformations:
        1. Start with the 36-key core layout
        2. Apply extensions based on board requirements
        3. Translate keycodes to firmware-specific syntax
        4. Validate complex keybindings

        Args:
            layer: Layer to compile
            board: Target board
            firmware: Target firmware ("qmk" or "zmk")

        Returns:
            CompiledLayer with translated keycodes

        Raises:
            ValidationError: If compilation fails
        """
        # 1. Start with core layout (36 keys)
        keycodes = layer.core.flatten()

        # 2. Apply extensions if board requires them
        extensions_to_apply = board.get_extensions()
        for ext_name in extensions_to_apply:
            if ext_name in layer.extensions:
                extension = layer.extensions[ext_name]
                ext_keys = self.get_extension_keys(extension)
                keycodes.extend(ext_keys)
            else:
                # Board requires extension but layer doesn't define it
                # Fill with NONE
                if ext_name == "3x5_3_pinky":
                    keycodes.extend(["NONE", "NONE"])  # 2 extra keys
                elif ext_name == "3x6_3":
                    keycodes.extend(["NONE"] * 6)  # 6 extra keys (3 per side)

        # 3. Select translator based on firmware
        translator = self.qmk_translator if firmware == "qmk" else self.zmk_translator

        # 4. Validate complex keybindings before translation
        for keycode in keycodes:
            translator.validate_keybinding(keycode, layer.name)

        # 5. Translate keycodes
        translated = [translator.translate(kc) for kc in keycodes]

        return CompiledLayer(
            name=layer.name,
            board=board,
            keycodes=translated,
            firmware=firmware
        )

    def get_extension_keys(self, extension) -> List[str]:
        """
        Flatten extension keys to a list

        Args:
            extension: LayerExtension object

        Returns:
            Flattened list of keycodes
        """
        result = []
        # Extensions define keys positionally
        # For 3x5_3_pinky: outer_pinky_left, outer_pinky_right
        # For 3x6_3: outer_pinky_left (list of 3), outer_pinky_right (list of 3)

        # Process in consistent order
        if 'outer_pinky_left' in extension.keys:
            left_keys = extension.keys['outer_pinky_left']
            if isinstance(left_keys, list):
                result.extend(left_keys)
            else:
                result.append(left_keys)

        if 'outer_pinky_right' in extension.keys:
            right_keys = extension.keys['outer_pinky_right']
            if isinstance(right_keys, list):
                result.extend(right_keys)
            else:
                result.append(right_keys)

        return result
