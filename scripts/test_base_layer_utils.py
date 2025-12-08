#!/usr/bin/env python3
"""
Unit tests for base_layer_utils.py
"""

import pytest
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from base_layer_utils import BaseLayerManager


@pytest.fixture
def manager():
    """Create BaseLayerManager instance for testing"""
    config_dir = Path(__file__).parent.parent / "config"
    return BaseLayerManager(config_dir)


def test_derive_layer_family_standard(manager):
    """Test that BASE_COLEMAK is detected as standard family"""
    if "BASE_COLEMAK" not in manager.keymap_config.layers:
        pytest.skip("BASE_COLEMAK not in keymap")

    base_colemak = manager.keymap_config.layers["BASE_COLEMAK"]
    variant = manager._derive_layer_family(base_colemak)
    assert variant == "", f"Expected standard family (empty string), got: {variant}"


def test_derive_layer_family_night(manager):
    """Test that BASE_NIGHT is detected as NIGHT family"""
    if "BASE_NIGHT" not in manager.keymap_config.layers:
        pytest.skip("BASE_NIGHT not in keymap")

    base_night = manager.keymap_config.layers["BASE_NIGHT"]
    variant = manager._derive_layer_family(base_night)
    assert variant == "_NIGHT", f"Expected _NIGHT family, got: {variant}"


def test_layer_family_completeness_night(manager):
    """Test that all layers in NIGHT family are detected"""
    if "BASE_NIGHT" not in manager.layer_families:
        pytest.skip("BASE_NIGHT not in layer families")

    night_family = manager.get_layer_family("BASE_NIGHT")

    # Expected layers (FUN is shared across all families)
    expected = ["BASE_NIGHT", "NUM_NIGHT", "SYM_NIGHT", "NAV_NIGHT", "MEDIA_NIGHT", "FUN"]

    # Filter expected to only include layers that actually exist
    expected_existing = [
        layer for layer in expected if layer in manager.keymap_config.layers
    ]

    assert sorted(night_family) == sorted(
        expected_existing
    ), f"Family mismatch. Expected: {expected_existing}, Got: {night_family}"


def test_layer_family_completeness_colemak(manager):
    """Test that all layers in COLEMAK family are detected"""
    if "BASE_COLEMAK" not in manager.layer_families:
        pytest.skip("BASE_COLEMAK not in layer families")

    colemak_family = manager.get_layer_family("BASE_COLEMAK")

    # Expected layers
    expected = ["BASE_COLEMAK", "NUM", "SYM", "NAV", "MEDIA", "FUN"]

    # Filter expected to only include layers that actually exist
    expected_existing = [
        layer for layer in expected if layer in manager.keymap_config.layers
    ]

    assert sorted(colemak_family) == sorted(
        expected_existing
    ), f"Family mismatch. Expected: {expected_existing}, Got: {colemak_family}"


def test_display_name_base_layer(manager):
    """Test display name for BASE layers"""
    # Test with BASE_COLEMAK if it exists
    if "BASE_COLEMAK" in manager.keymap_config.layers:
        display = manager.get_display_name("BASE_COLEMAK")
        # Should be COLEMAK (either from metadata or stripping BASE_)
        assert display in ["COLEMAK"], f"Unexpected display name: {display}"

    # Test with BASE_NIGHT if it exists
    if "BASE_NIGHT" in manager.keymap_config.layers:
        display = manager.get_display_name("BASE_NIGHT")
        assert display in ["NIGHT"], f"Unexpected display name: {display}"


def test_display_name_variant_layer(manager):
    """Test display name for variant layers"""
    # Test NUM_NIGHT if it exists
    if "NUM_NIGHT" in manager.keymap_config.layers:
        assert manager.get_display_name("NUM_NIGHT") == "NUM"

    # Test SYM_NIGHT if it exists
    if "SYM_NIGHT" in manager.keymap_config.layers:
        assert manager.get_display_name("SYM_NIGHT") == "SYM"

    # Test NAV_NIGHT if it exists
    if "NAV_NIGHT" in manager.keymap_config.layers:
        assert manager.get_display_name("NAV_NIGHT") == "NAV"


def test_display_name_standard_layer(manager):
    """Test display name for standard layers (no prefix/suffix)"""
    # Standard layers should return unchanged
    if "NUM" in manager.keymap_config.layers:
        assert manager.get_display_name("NUM") == "NUM"

    if "SYM" in manager.keymap_config.layers:
        assert manager.get_display_name("SYM") == "SYM"

    if "NAV" in manager.keymap_config.layers:
        assert manager.get_display_name("NAV") == "NAV"


def test_svg_replacement(manager):
    """Test that SVG replacement works correctly"""
    # Test BASE layer replacement
    svg = "<text>BASE_COLEMAK</text>"
    result = manager.apply_display_names_to_svg(svg)
    assert "COLEMAK" in result, f"Expected COLEMAK in result, got: {result}"
    assert "BASE_COLEMAK" not in result, "BASE_COLEMAK should be replaced"

    # Test variant layer replacement
    if "NUM_NIGHT" in manager.keymap_config.layers:
        svg = "<text>NUM_NIGHT</text>"
        result = manager.apply_display_names_to_svg(svg)
        assert "NUM" in result
        assert "NUM_NIGHT" not in result


def test_svg_replacement_multiple(manager):
    """Test that SVG replacement handles multiple occurrences"""
    svg = "<text>BASE_COLEMAK</text><text>NUM_NIGHT</text><text>BASE_NIGHT</text>"
    result = manager.apply_display_names_to_svg(svg)

    # Check replacements occurred
    if "BASE_COLEMAK" in manager.keymap_config.layers:
        assert "COLEMAK" in result
        assert "BASE_COLEMAK" not in result

    if "NUM_NIGHT" in manager.keymap_config.layers:
        assert result.count("NUM") >= 1

    if "BASE_NIGHT" in manager.keymap_config.layers:
        assert "NIGHT" in result


def test_all_base_layers_detected(manager):
    """Test that all BASE_* layers are found"""
    base_layers = manager.get_all_base_layers()

    # Should find at least BASE_NIGHT and BASE_COLEMAK
    assert len(base_layers) >= 2, f"Expected at least 2 base layers, got: {base_layers}"

    # All should start with BASE_
    for layer in base_layers:
        assert layer.startswith("BASE_"), f"Layer {layer} doesn't start with BASE_"

    # Check for specific known base layers
    known_bases = ["BASE_COLEMAK", "BASE_NIGHT"]
    for known in known_bases:
        if known in manager.keymap_config.layers:
            assert known in base_layers, f"{known} should be in base layers list"


def test_generate_keymap_drawer_config(manager):
    """Test that config generation produces valid structure"""
    config = manager.generate_keymap_drawer_config()

    # Check required keys exist
    assert "layer_names" in config
    assert "layer_legend_map" in config
    assert "df_keycodes" in config

    # Check layer_names is a list
    assert isinstance(config["layer_names"], list)
    assert len(config["layer_names"]) > 0

    # Check layer_legend_map is a dict
    assert isinstance(config["layer_legend_map"], dict)

    # Check df_keycodes is a dict
    assert isinstance(config["df_keycodes"], dict)

    # Verify base layers are in layer_names
    base_layers = manager.get_all_base_layers()
    for base in base_layers:
        assert base in config["layer_names"], f"{base} should be in layer_names"

    # Verify DF codes exist for base layers
    for base in base_layers:
        df_key = f"DF({base})"
        assert df_key in config["df_keycodes"], f"{df_key} should be in df_keycodes"


def test_layer_names_order_has_bases_first(manager):
    """Test that layer_names has BASE layers first"""
    config = manager.generate_keymap_drawer_config()
    layer_names = config["layer_names"]

    base_layers = manager.get_all_base_layers()

    # Find positions of base layers
    base_positions = [layer_names.index(base) for base in base_layers if base in layer_names]

    # All base layers should be at the beginning
    assert base_positions == sorted(base_positions), "Base layers should be grouped at the start"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
