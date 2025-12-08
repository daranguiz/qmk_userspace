#!/usr/bin/env python3
"""
Update .keymap-drawer-config.yaml with auto-generated layer metadata

This script regenerates the dynamic sections of .keymap-drawer-config.yaml:
- layer_names: Ordered list for QMK enum mapping
- layer_legend_map: Display name mappings
- raw_binding_map DF() codes: Default layer switching keycodes
"""

from pathlib import Path
import yaml
import sys

# Add scripts directory to path to import base_layer_utils
sys.path.insert(0, str(Path(__file__).parent))

from base_layer_utils import BaseLayerManager


def update_config():
    """Update .keymap-drawer-config.yaml with auto-generated sections"""
    repo_root = Path(__file__).parent.parent
    config_file = repo_root / ".keymap-drawer-config.yaml"
    config_dir = repo_root / "config"

    print("📝 Updating .keymap-drawer-config.yaml...")

    # Load existing config
    with open(config_file) as f:
        config = yaml.safe_load(f)

    # Generate new sections
    manager = BaseLayerManager(config_dir)
    generated = manager.generate_keymap_drawer_config()

    # Update config sections
    if "parse_config" not in config:
        config["parse_config"] = {}

    config["parse_config"]["layer_names"] = generated["layer_names"]
    config["parse_config"]["layer_legend_map"] = generated["layer_legend_map"]

    # Update raw_binding_map with DF() codes
    if "raw_binding_map" not in config["parse_config"]:
        config["parse_config"]["raw_binding_map"] = {}

    for df_code, display in generated["df_keycodes"].items():
        config["parse_config"]["raw_binding_map"][df_code] = display

    # Write back (preserve formatting as much as possible)
    with open(config_file, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"✅ Updated {config_file.name}")
    print(f"   - {len(generated['layer_names'])} layer names")
    print(f"   - {len(generated['layer_legend_map'])} legend mappings")
    print(f"   - {len(generated['df_keycodes'])} DF() keycodes")

    # Print layer order for verification
    print("\n📋 Layer order (matches QMK enum):")
    for i, layer_name in enumerate(generated["layer_names"]):
        display_name = manager.get_display_name(layer_name)
        print(f"   L{i}: {layer_name:20} → {display_name}")


if __name__ == "__main__":
    try:
        update_config()
    except Exception as e:
        print(f"❌ Error updating config: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
