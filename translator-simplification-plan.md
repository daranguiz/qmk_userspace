# Translator Simplification Plan: Remove Dead Prefix-Checking Code

**Status**: Planning Phase
**Date**: 2025-11-17
**Goal**: Simplify QMK and ZMK translators by removing ~30 lines of dead code that checks for prefixes that never exist in actual inputs

---

## Executive Summary

The QMK and ZMK translators contain extensive prefix-checking code (KC_, QK_, RGB_, RM_, BT_) that is **never executed** because all input comes from keymap.yaml which uses **common names** (e.g., `A`, `SLSH`, `LGUI`, `QK_BOOT`), not prefixed formats.

This plan removes the dead code and enforces a strict error on unknown keycodes instead of silently falling back.

---

## Investigation Results

### Input Format Analysis

**keymap.yaml format** (the ONLY source of keycodes):
- Uses **common names** exclusively: `A`, `W`, `F`, `P`, `G`, `SLSH`, `COMM`, `DOT`
- Modifiers: `LGUI`, `LALT`, `LCTL`, `LSFT`, `RSFT`, `RCTL`, `RALT`, `RGUI`
- Special codes with underscores are still common names: `QK_BOOT`, `RM_TOGG`, `BT_SEL_0`
- Behaviors use colons: `hrm:LGUI:A`, `lt:NAV:SPC`, `lt:FUN:SLSH`

**Data flow:**
```
keymap.yaml (common names)
    ↓
layer_compiler (NO transformation)
    ↓
translator.translate(common_name)
    ↓
keycodes.yaml lookup (common name → firmware value)
```

**keycodes.yaml structure:**
```yaml
# Common name as key
A:
  qmk: "KC_A"
  zmk: "&kp A"

SLSH:
  qmk: "KC_SLSH"
  zmk: "&kp FSLH"

QK_BOOT:
  qmk: "QK_BOOT"
  zmk: "&bootloader"
```

---

## Current Code Problems

### QMK Translator (`scripts/qmk_translator.py` lines 62-93)

**Dead code to remove:**

```python
# Lines 62-69: NEVER EXECUTES - input never has KC_ or QK_ prefix
if unified.startswith('KC_') or unified.startswith('QK_'):
    # Validate against keycodes.yaml (required)
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('qmk', 'KC_NO')
        return value if value else "KC_NO"
    # Unknown keycode - return KC_NO instead of passing through
    return "KC_NO"

# Lines 71-79: PARTIALLY DEAD - only needed for RM_/RGB_ common names
if unified.startswith('RGB_') or unified.startswith('RM_'):
    # Validate against keycodes.yaml (required)
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('qmk', 'KC_NO')
        return value if value else "KC_NO"
    # Unknown keycode - return KC_NO instead of passing through
    return "KC_NO"

# Lines 81-83: NEVER EXECUTES - input never contains parentheses
if '(' in unified:
    return unified
```

**The only code that actually runs:**

```python
# Lines 85-93: This handles EVERYTHING
if unified in self.special_keycodes:
    value = self.special_keycodes[unified].get('qmk', 'KC_NO')
    return value if value else "KC_NO"

# Fallback for keys not in keycodes.yaml
return f"KC_{unified}"  # ← SHOULD BE AN ERROR INSTEAD
```

### ZMK Translator (`scripts/zmk_translator.py` lines 69-93)

**Dead code to remove:**

```python
# Lines 69-72: NEVER EXECUTES - input never has KC_ prefix
if unified.startswith('KC_'):
    key = unified[3:]  # Remove KC_ prefix
    return f"&kp {key}"

# Lines 74-79: REDUNDANT - just duplicates the main lookup
if not unified.startswith('KC_') and not unified.startswith('QK_') and not unified.startswith('BT_'):
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('zmk', '&none')
        return value if value else "&none"

# Lines 81-89: PARTIALLY DEAD - only needed for RM_/RGB_ common names
if unified.startswith('RM_') or unified.startswith('RGB_'):
    # Look up in keycodes.yaml to confirm
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('zmk', '&none')
        return value if value else "&none"
    # Not in keycodes.yaml - assume QMK-only
    return '&none'
```

**The only code that actually runs:**

```python
# Lines 91-93: Fallback
return f"&kp {unified}"  # ← SHOULD BE AN ERROR INSTEAD
```

---

## Proposed Changes

### 1. QMK Translator Simplification

**File:** `scripts/qmk_translator.py`

**Remove:** Lines 62-83 (all prefix checking, function macro checking)

**Replace lines 85-93 with:**

```python
# Look up common name in keycodes.yaml
if unified in self.special_keycodes:
    value = self.special_keycodes[unified].get('qmk', 'KC_NO')
    return value if value else "KC_NO"

# Unknown keycode - raise error instead of silent fallback
raise ValidationError(
    f"Unknown keycode '{unified}' not found in keycodes.yaml. "
    f"All keycodes must be defined in config/keycodes.yaml"
)
```

**Final simplified translate() method:**

```python
def translate(self, unified) -> str:
    """
    Translate unified keycode to QMK C syntax

    Args:
        unified: Unified keycode in common name format (e.g., "A", "SLSH", "LGUI")

    Returns:
        QMK C code string

    Raises:
        ValidationError: If keycode is unknown or unsupported
    """
    # Convert to string if needed
    unified = str(unified)

    # Handle special keycodes from aliases.yaml
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('qmk', 'KC_NO')
        return value if value else "KC_NO"

    # Handle aliased behaviors (hrm:LGUI:A, lt:NAV:SPC, etc.)
    if ':' in unified:
        return self._translate_alias(unified)

    # Look up common name in keycodes.yaml
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('qmk', 'KC_NO')
        return value if value else "KC_NO"

    # Unknown keycode - raise error
    raise ValidationError(
        f"Unknown keycode '{unified}' not found in keycodes.yaml. "
        f"All keycodes must be defined in config/keycodes.yaml"
    )
```

### 2. ZMK Translator Simplification

**File:** `scripts/zmk_translator.py`

**Remove:** Lines 69-89 (all prefix checking)

**Replace lines 91-93 with:**

```python
# Look up common name in keycodes.yaml
if unified in self.special_keycodes:
    value = self.special_keycodes[unified].get('zmk', '&none')
    return value if value else "&none"

# Unknown keycode - raise error instead of silent fallback
raise ValidationError(
    f"Unknown keycode '{unified}' not found in keycodes.yaml. "
    f"All keycodes must be defined in config/keycodes.yaml"
)
```

**Final simplified translate() method:**

```python
def translate(self, unified) -> str:
    """
    Translate unified keycode to ZMK devicetree syntax

    Args:
        unified: Unified keycode in common name format (e.g., "A", "SLSH", "LGUI")

    Returns:
        ZMK devicetree string

    Raises:
        ValidationError: If keycode is invalid or unsupported
    """
    # Convert to string if needed
    unified = str(unified)

    # Handle special keycodes from aliases.yaml
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('zmk', '&none')
        return value if value else "&none"

    # Handle aliased behaviors (hrm:LGUI:A, lt:NAV:SPC, etc.)
    if ':' in unified:
        return self._translate_alias(unified)

    # Look up common name in keycodes.yaml
    if unified in self.special_keycodes:
        value = self.special_keycodes[unified].get('zmk', '&none')
        return value if value else "&none"

    # Unknown keycode - raise error
    raise ValidationError(
        f"Unknown keycode '{unified}' not found in keycodes.yaml. "
        f"All keycodes must be defined in config/keycodes.yaml"
    )
```

### 3. Update Documentation Comments

**Search and replace throughout both files:**
- "bare name" → "common name"
- "bare key" → "common name"
- "bare format" → "common name format"

**Files to update:**
- `scripts/qmk_translator.py`
- `scripts/zmk_translator.py`
- Any comments/docstrings that reference "bare"

---

## Benefits

### Code Quality
- ✅ **~30 lines removed** from each translator
- ✅ **Crystal clear logic:** common names → keycodes.yaml lookup → done
- ✅ **No confusing edge cases** or redundant checks
- ✅ **Self-documenting:** obvious that keycodes.yaml is the source of truth

### Error Handling
- ✅ **Fail fast:** Unknown keycodes immediately raise clear errors
- ✅ **Developer feedback:** "Add X to keycodes.yaml" instead of silent fallback
- ✅ **No surprises:** Can't accidentally use undefined keycodes

### Maintainability
- ✅ **One place to add keycodes:** Just update keycodes.yaml
- ✅ **No sync issues:** Can't have keycode work in one place but not another
- ✅ **Easier to understand:** Simple lookup, no special cases

---

## Implementation Steps

### Step 1: Document Current Behavior
- ✅ **Already done:** This document

### Step 2: Simplify QMK Translator
1. Remove lines 62-83 from `scripts/qmk_translator.py`
2. Replace lines 85-93 with error-raising code
3. Update all "bare" terminology to "common name"
4. Update docstrings to reflect simplified logic

### Step 3: Simplify ZMK Translator
1. Remove lines 69-89 from `scripts/zmk_translator.py`
2. Replace lines 91-93 with error-raising code
3. Update all "bare" terminology to "common name"
4. Update docstrings to reflect simplified logic

### Step 4: Update `_translate_key_for_zmk()`
- Already uses common name format correctly
- Just update terminology in comments

### Step 5: Verification
1. Run `python3 scripts/generate.py` - should succeed
2. Run `./build_all.sh` - all builds should pass
3. Verify error handling: temporarily remove a keycode from keycodes.yaml and confirm it raises ValidationError

---

## Verification Checklist

- [ ] QMK translator simplified (lines removed, error added)
- [ ] ZMK translator simplified (lines removed, error added)
- [ ] All "bare" references changed to "common name"
- [ ] Docstrings updated
- [ ] `python3 scripts/generate.py` succeeds
- [ ] `./build_all.sh` succeeds (all QMK and ZMK builds pass)
- [ ] Error handling verified (unknown keycode raises ValidationError)

---

## Edge Cases Confirmed Working

The simplified code correctly handles:
- ✅ Common names with underscores: `QK_BOOT`, `RM_TOGG`, `BT_SEL_0`
- ✅ Numeric keys: `1`, `2`, `3`, etc. (converted to strings)
- ✅ Aliased behaviors: `hrm:LGUI:A`, `lt:NAV:SPC`
- ✅ Firmware-specific codes: Checked via empty string in keycodes.yaml

---

## Risk Assessment

**Risk Level:** **LOW**

**Why:**
- We're removing code that **never executes** (dead code)
- The final lookup that actually runs is unchanged
- All inputs are validated against keycodes.yaml (already required)
- Error on unknown keycode is **safer** than silent fallback

**Mitigation:**
- Comprehensive build verification (`./build_all.sh`)
- All existing keycodes are in keycodes.yaml (verified)
- Clear error messages guide fixing any issues

---

## Success Criteria

1. ✅ Code is simplified (fewer lines, clearer logic)
2. ✅ All builds pass (QMK and ZMK)
3. ✅ Unknown keycodes raise ValidationError with helpful message
4. ✅ Terminology is consistent (common names, not bare names)
5. ✅ Documentation reflects simplified behavior

---

**Next Step:** Review this plan, then execute the changes
