# Keycode Cleanup Plan: Refactor to Use keycodes.yaml as Source of Truth

**Status**: Planning Phase
**Date**: 2025-11-17
**Goal**: Remove all hardcoded keycode mappings and comparisons now that `config/keycodes.yaml` is the single source of truth

---

## Executive Summary

This document identifies ALL locations in the codebase where old keycode comparison code exists that should be cleaned up. Now that `config/keycodes.yaml` provides comprehensive keycode mappings between QMK and ZMK, hardcoded dictionaries and string comparisons should be eliminated.

**Files with changes needed**:
- `scripts/qmk_translator.py` - 6 locations
- `scripts/zmk_translator.py` - 5 locations
- `scripts/visualizer.py` - 2 locations
- `scripts/zmk_generator.py` - 1 location
- `scripts/migrate_layers.py` - 1 location (KEEP - one-time migration tool)

**Total refactoring locations**: 14 (excluding migration script)

---

## 1. qmk_translator.py - 6 Locations

### **Location 1.1: Hardcoded ZMK-specific alias list** ⚠️ **HIGH PRIORITY**
- **Lines**: 134-136
- **Code**:
```python
# Check if it's a ZMK-only feature (starts with known ZMK prefixes)
if alias_name in ['bt', 'out', 'ext_power']:
    return "KC_NO"  # Filter ZMK-specific
```
- **Category**: **REFACTOR**
- **Issue**: Hardcoded list of ZMK-only behavior aliases
- **Solution**: Check `alias.firmware_support` from `config/aliases.yaml` instead
- **Why**: If new ZMK-only aliases are added, they won't be filtered unless this list is manually updated
- **Change**:
```python
# NEW: Check firmware support from aliases.yaml
if 'qmk' not in alias.firmware_support:
    return "KC_NO"  # Filter unsupported
```

---

### **Location 1.2: Hardcoded ZMK-specific alias list (duplicate)** 🐛 **CRITICAL - BUG!**
- **Lines**: 186-189
- **Code**:
```python
# Check for known ZMK-only features
if alias_name in ['bt', 'out', 'ext_power', 'rgb_ug', 'bl']:
    # This is OK - will be filtered silently
    return
```
- **Category**: **REFACTOR**
- **Issue**: Duplicate hardcoded list with DIFFERENT values than Location 1.1!
  - Location 1.1: `['bt', 'out', 'ext_power']`
  - Location 1.2: `['bt', 'out', 'ext_power', 'rgb_ug', 'bl']`
- **Bug**: Inconsistency! `rgb_ug` and `bl` are missing from first list
- **Solution**: Same as 1.1 - use `alias.firmware_support`
- **Change**: Same pattern as 1.1

---

### **Location 1.3: Fallback for unknown KC_/QK_ keycodes** 🔸 **MEDIUM PRIORITY**
- **Lines**: 62-68
- **Code**:
```python
# Handle already-prefixed keycodes (e.g., KC_A, QK_BOOT)
if unified.startswith('KC_') or unified.startswith('QK_'):
    # Validate against keycodes.yaml if available
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('qmk', 'KC_NO')
        return value if value else "KC_NO"
    return unified  # ⚠️ FALLBACK - returns unvalidated keycode
```
- **Category**: **REFACTOR**
- **Issue**: Falls back to returning `unified` directly if keycode not in keycodes.yaml
- **Risk**: Silently accepts undefined keycodes
- **Solution**: Require keycode to exist in keycodes.yaml
- **Change**:
```python
if unified.startswith('KC_') or unified.startswith('QK_'):
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('qmk', 'KC_NO')
        return value if value else "KC_NO"
    # NEW: Return KC_NO instead of passing through unvalidated
    return "KC_NO"
```

---

### **Location 1.4: Fallback for unknown RGB_/RM_ keycodes** 🔸 **MEDIUM PRIORITY**
- **Lines**: 70-77
- **Code**:
```python
# Handle special QMK keycodes that don't use KC_ prefix
if unified.startswith('RGB_') or unified.startswith('RM_'):
    # Validate against keycodes.yaml if available
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('qmk', 'KC_NO')
        return value if value else "KC_NO"
    return unified  # ⚠️ FALLBACK - returns unvalidated keycode
```
- **Category**: **REFACTOR**
- **Issue**: Same as 1.3 - falls back to returning unvalidated keycode
- **Solution**: Same as 1.3 - require existence in keycodes.yaml
- **Change**: Same pattern as 1.3

---

### **Location 1.5: String-based modifier derivation** 🔹 **LOW PRIORITY**
- **Lines**: 102-112
- **Code**:
```python
if self.special_keycodes:
    modifiers = []
    for keycode in self.special_keycodes.keys():
        # Look for KC_Lxxx and KC_Rxxx modifiers
        if keycode.startswith('KC_L') or keycode.startswith('KC_R'):
            key_part = keycode[3:]  # Remove KC_ prefix
            # Check if it ends with GUI, ALT, CTL/CTRL, SFT/SHFT
            if any(key_part.endswith(mod) for mod in ['GUI', 'ALT', 'CTL', 'CTRL', 'SFT', 'SHFT']):
                modifiers.append(key_part)
    return modifiers
```
- **Category**: **REFACTOR** (future enhancement)
- **Issue**: Uses string pattern matching instead of metadata
- **Risk**: Brittle - what about future modifiers like `HYPER` or `MEH`?
- **Solution**: Add `category: modifier` field to keycodes.yaml entries
- **Change**: Filter on `category` field instead of string patterns
- **Note**: This is a nice-to-have enhancement, not critical for current cleanup

---

### **Location 1.6: Hardcoded modifier fallback list** ⚠️ **HIGH PRIORITY - REMOVE**
- **Lines**: 111-112
- **Code**:
```python
# Fallback: hardcoded list if keycodes.yaml not available
return ['LGUI', 'RGUI', 'LALT', 'RALT', 'LCTL', 'RCTL', 'LSFT', 'RSFT']
```
- **Category**: **REMOVE**
- **Issue**: Hardcoded fallback list - no longer needed
- **Why**: keycodes.yaml is now mandatory and always present
- **Change**: Delete this fallback entirely

---

## 2. zmk_translator.py - 5 Locations

### **Location 2.1: Hardcoded QMK-specific alias list** ⚠️ **HIGH PRIORITY**
- **Lines**: 136-137
- **Code**:
```python
if alias_name in ['rgb', 'bl']:  # QMK-specific
    return "&none"  # Filter QMK-specific
```
- **Category**: **REFACTOR**
- **Issue**: Hardcoded list of QMK-only behavior aliases
- **Solution**: Check `alias.firmware_support` from `config/aliases.yaml`
- **Change**:
```python
# NEW: Check firmware support from aliases.yaml
if 'zmk' not in alias.firmware_support:
    return "&none"  # Filter unsupported
```

---

### **Location 2.2: Hardcoded QMK-specific alias list (duplicate)** ⚠️ **HIGH PRIORITY**
- **Lines**: 203
- **Code**:
```python
if alias_name in ['rgb', 'bl']:
    # This is OK - will be filtered silently
    return
```
- **Category**: **REFACTOR**
- **Issue**: Duplicate hardcoded list in validation function
- **Solution**: Same as 2.1 - use `alias.firmware_support`

---

### **Location 2.3: Prefix-based keycode filtering** 🔹 **LOW PRIORITY**
- **Lines**: 76-81
- **Code**:
```python
if not unified.startswith('KC_') and not unified.startswith('QK_') and not unified.startswith('BT_'):
    # Try looking up with KC_ prefix (e.g., "A" -> "KC_A")
    prefixed_key = f"KC_{unified}"
    if prefixed_key in self.special_keycodes:
        value = self.special_keycodes[prefixed_key].get('zmk', '&none')
        return value if value else "&none"
```
- **Category**: **REFACTOR** (minor improvement)
- **Issue**: Hardcoded prefix check logic
- **Solution**: Simplify by trying lookup with/without prefix in cleaner way
- **Note**: This code is mostly correct, just could be cleaner

---

### **Location 2.4: Hardcoded RGB/RM prefix filtering** 🔸 **MEDIUM PRIORITY**
- **Lines**: 84-86
- **Code**:
```python
# If keycode doesn't exist in keycodes.yaml, check for known unsupported keycodes
if unified.startswith('RM_') or unified.startswith('RGB_'):
    # RGB keycodes are QMK-only, not in ZMK
    return '&none'
```
- **Category**: **REFACTOR**
- **Issue**: Hardcoded prefix check instead of using keycodes.yaml
- **Solution**: RGB/RM keycodes should be in keycodes.yaml with `zmk: ""` (empty string)
- **Change**: Check keycodes.yaml for empty zmk value instead of prefix

---

### **Location 2.5: Hardcoded modifier validation list** 🔹 **LOW PRIORITY**
- **Lines**: 231-236
- **Code**:
```python
# Accept both QMK and ZMK modifier names
valid_mods = ['LGUI', 'RGUI', 'LALT', 'RALT', 'LCTRL', 'RCTRL', 'LSHFT', 'RSHFT',
             'LCTL', 'RCTL', 'LSFT', 'RSFT']  # Also accept QMK shorthand
if mod not in valid_mods:
    raise ValidationError(...)
```
- **Category**: **REFACTOR** (future enhancement)
- **Issue**: Hardcoded list of valid modifiers
- **Solution**: Derive from keycodes.yaml using metadata (same as qmk_translator.py Location 1.5)
- **Note**: Nice-to-have, not critical

---

## 3. visualizer.py - 2 Locations

### **Location 3.1: Hardcoded special keycode list** 🔹 **LOW PRIORITY**
- **Lines**: 41-42
- **Code**:
```python
if keycode in ["NONE", "U_NA", "U_NU", "U_NP"]:
    return "KC_NO"  # keymap-drawer will render as blank with raw_binding_map
```
- **Category**: **REFACTOR** (cosmetic)
- **Issue**: Hardcoded list of "empty" keycodes
- **Solution**: Define in keycodes.yaml with metadata like `category: "placeholder"`
- **Note**: Mostly cosmetic, low priority

---

### **Location 3.2: Duplicate translation logic** 🔸 **MEDIUM PRIORITY**
- **Lines**: 44-61
- **Code**:
```python
# Handle home row mods: hrm:MOD:KEY -> MOD_T(KC_KEY)
if keycode.startswith("hrm:"):
    parts = keycode.split(":")
    if len(parts) == 3:
        mod = parts[1]
        key = parts[2]
        return f"{mod}_T(KC_{key})"

# Handle layer taps: lt:LAYER:KEY -> LT(LAYER, KC_KEY)
if keycode.startswith("lt:"):
    parts = keycode.split(":")
    if len(parts) == 3:
        layer = parts[1]
        key = parts[2]
        return f"LT({layer}, KC_{key})"

# Standard keycodes - add KC_ prefix
return f"KC_{keycode}"
```
- **Category**: **REFACTOR**
- **Issue**: Duplicates translation logic that exists in QMKTranslator
- **Solution**: Use `QMKTranslator.translate()` instead
- **Benefits**: DRY principle, consistent translation, easier maintenance
- **Change**:
```python
# NEW: Reuse QMKTranslator instead of duplicating logic
def _translate_keycode_for_display(self, keycode: str) -> str:
    # Initialize translator with config (passed from generate.py)
    return self.qmk_translator.translate(keycode)
```

---

## 4. zmk_generator.py - 1 Location

### **Location 4.1: Hardcoded BT visualization map** 🔹 **LOW PRIORITY**
- **Lines**: 215-221
- **Code**:
```python
elif behavior == 'bt':
    # bt BT_NXT -> BT→
    action_map = {
        'BT_NXT': 'BT→',
        'BT_PRV': 'BT←',
        'BT_CLR': 'BT×'
    }
    return action_map.get(params[0], 'BT')
```
- **Category**: **REFACTOR** (cosmetic)
- **Issue**: Hardcoded visualization symbols for Bluetooth keycodes
- **Solution**: Add `display: "BT→"` field to keycodes.yaml
- **Note**: Cosmetic only, low priority

---

## 5. migrate_layers.py - 1 Location (KEEP)

### **Location 5.1: Migration script special cases** ✅ **NO CHANGE NEEDED**
- **Lines**: 75-77
- **Code**:
```python
# Handle special unavailable/unused markers
if qmk_keycode in ('KC_NO', 'U_NA', 'U_NU', 'U_NP'):
    return 'NONE'
```
- **Category**: **KEEP**
- **Reason**: One-time migration script, not part of regular build process
- **Action**: No changes needed

---

## Summary Table

| Priority | File | Lines | Type | Description |
|----------|------|-------|------|-------------|
| 🐛 **CRITICAL** | qmk_translator.py | 186-189 | BUG | Inconsistent alias list (has extra items) |
| ⚠️ **HIGH** | qmk_translator.py | 134-136 | REFACTOR | Hardcoded ZMK alias list |
| ⚠️ **HIGH** | qmk_translator.py | 111-112 | REMOVE | Hardcoded modifier fallback |
| ⚠️ **HIGH** | zmk_translator.py | 136-137 | REFACTOR | Hardcoded QMK alias list |
| ⚠️ **HIGH** | zmk_translator.py | 203 | REFACTOR | Duplicate QMK alias list |
| 🔸 **MEDIUM** | qmk_translator.py | 62-68 | REFACTOR | Fallback for unknown KC_/QK_ |
| 🔸 **MEDIUM** | qmk_translator.py | 70-77 | REFACTOR | Fallback for unknown RGB_/RM_ |
| 🔸 **MEDIUM** | zmk_translator.py | 84-86 | REFACTOR | RGB/RM prefix filtering |
| 🔸 **MEDIUM** | visualizer.py | 44-61 | REFACTOR | Duplicate translation logic |
| 🔹 **LOW** | qmk_translator.py | 102-112 | REFACTOR | String-based modifier derivation |
| 🔹 **LOW** | zmk_translator.py | 76-81 | REFACTOR | Prefix-based filtering |
| 🔹 **LOW** | zmk_translator.py | 231-236 | REFACTOR | Hardcoded modifier list |
| 🔹 **LOW** | visualizer.py | 41-42 | REFACTOR | Hardcoded empty keycode list |
| 🔹 **LOW** | zmk_generator.py | 215-221 | REFACTOR | Hardcoded BT visualization |

**Total**: 14 locations (5 high priority, 4 medium priority, 5 low priority)

---

## Recommended Cleanup Phases

### **Phase 1: Critical Fixes (Must Do)**
1. ✅ **ALREADY DONE**: Add missing QK_RBT to keycodes.yaml
2. **Fix alias list inconsistency bug** (qmk_translator.py lines 134-136, 186-189)
   - Replace both with `alias.firmware_support` checks
3. **Remove hardcoded modifier fallback** (qmk_translator.py lines 111-112)
4. **Fix ZMK alias filtering** (zmk_translator.py lines 136-137, 203)

### **Phase 2: Important Refactoring (Should Do)**
5. **Enforce keycodes.yaml validation** (qmk_translator.py lines 62-68, 70-77; zmk_translator.py lines 84-86)
   - Remove fallbacks that pass through unvalidated keycodes
6. **Eliminate duplicate translation** (visualizer.py lines 44-61)
   - Reuse QMKTranslator instead of manual string building

### **Phase 3: Nice-to-Have Enhancements (Could Do)**
7. **Add metadata to keycodes.yaml**:
   - `category: modifier` for modifier detection
   - `category: placeholder` for empty keycodes
   - `display: "..."` for visualization symbols
8. **Refactor modifier validation** to use metadata

---

## Dependencies & Prerequisites

### Required for Phase 1 & 2:
- ✅ keycodes.yaml must include all RGB_* and RM_* keycodes
- ✅ keycodes.yaml must include all QK_* keycodes (QK_BOOT, QK_RBT)
- ✅ keycodes.yaml must include all BT_* keycodes
- ✅ aliases.yaml must have `firmware_support` field for all aliases

### Required for Phase 3 (optional):
- Add `category` field to keycodes.yaml schema
- Add `display` field to keycodes.yaml schema for visualization

---

## Testing Plan

After each phase, verify:
1. ✅ Run `./build_all.sh` - all boards build successfully
2. ✅ Check generated QMK keymaps in `qmk/keyboards/*/keymaps/dario/keymap.c`
3. ✅ Check generated ZMK keymaps in `zmk/keymaps/*/keymap`
4. ✅ Verify visualizations still generate correctly in `docs/keymaps/`
5. ✅ Test with boards of different sizes (3x5_3, 3x6_3)

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking existing builds | Test with `./build_all.sh` after each change |
| Missing keycodes in keycodes.yaml | Audit keycodes.yaml completeness first |
| Behavior changes | Add unit tests for translators |
| Performance regression | keycodes.yaml loaded once at startup, dict lookups are O(1) |

---

## Notes

- ✅ All hardcoded keycode mappings verified to exist in keycodes.yaml
- ✅ Only missing keycode was QK_RBT (already added)
- ⚠️ Critical bug found: Inconsistent alias lists in qmk_translator.py
- 📊 Total hardcoded mappings to remove: 41 entries from zmk_translator.py `_map_qmk_key_to_zmk` (already removed)

---

**Status**: Ready for implementation
**Next Step**: Review this plan, then proceed with Phase 1 refactoring
