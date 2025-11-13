# Feature Specification: Unified QMK/ZMK Keymap Configuration with Code Generation

**Feature Branch**: `003-unified-keymap-codegen`
**Created**: 2025-11-13
**Status**: Draft - In Review (reviewed through User Story 3)
**Input**: User description: "I have this repo, QMK userspace, as well as a separate ZMK repo. Right now, I have to maintain these two manually. If I make a change in one, I have to make a change in the other. It's a very manual process, very error prone, and usually just means my keymaps get out of date. I want to merge these into a single repo (or have a submodule or something, really whatever fits the model best), and I want to have a single common place where I can update my keymap. After I do so, it should auto-codegen for both QMK and ZMK."

---

## Review Notes

**Last Reviewed**: User Stories 1-3 (2025-11-13)

**Open Questions**:
1. **Configuration Format** [NEEDS RESEARCH]: Need to determine the format for the unified keymap configuration (JSON, YAML, TOML, custom DSL, etc.). This should be specified before proceeding to planning phase. Considerations:
   - Human readability and editability
   - Ability to represent complex keymap structures (layers, tap-hold, combos, etc.)
   - Validation and error reporting capabilities
   - Tooling support (syntax highlighting, LSP, etc.)
   - Extensibility for future firmware features

**Review Status**: User has reviewed and refined User Stories 1-3. User Stories 4-5 and remaining sections pending review.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Single-Source Keymap Updates (Priority: P1)

As a keyboard enthusiast maintaining multiple firmware configurations, I want to update my keymap definition in one place and have both QMK and ZMK keymaps automatically generated, so that I don't have to manually synchronize changes across two repositories.

**Why this priority**: This is the core value proposition - eliminating manual duplication is the primary goal. Without this, the feature provides no value.

**Independent Test**: Can be fully tested by modifying a single keymap source file (e.g., changing a key binding), running the code generation, and verifying that both QMK and ZMK keymaps reflect the change correctly.

**Acceptance Scenarios**:

1. **Given** I have a unified keymap configuration with a 3x5_3 layout, **When** I change a key binding in the source configuration, **Then** both QMK and ZMK generated keymaps reflect this change
2. **Given** I have multiple keyboards defined (different boards, same core layout), **When** I update a layer definition, **Then** all keyboards' keymaps are regenerated with the updated layer
3. **Given** I have made changes to the source keymap, **When** I run the code generation command, **Then** the generation completes without errors and produces valid QMK and ZMK keymap files

---

### User Story 2 - Firmware-Specific Feature Handling (Priority: P2)

As a user working with both QMK and ZMK firmwares, I want to define a superset keymap configuration that includes all possible keybindings (both QMK-specific and ZMK-specific features), with the system automatically filtering out unsupported keybindings for each firmware during generation, so that I can maintain one comprehensive source of truth that works for both firmwares.

**Why this priority**: This enables the unified keymap to handle real-world differences between firmwares bidirectionally. Without it, users would be forced to maintain separate configurations or sacrifice firmware-specific features. The superset approach future-proofs the system for any firmware-specific capabilities.

**Independent Test**: Can be tested by adding firmware-specific keybindings (e.g., ZMK Bluetooth keys, QMK-specific combo keys) to the unified keymap, generating both firmwares, and verifying that each firmware output only includes its supported features with unsupported features replaced by appropriate fallbacks.

**Acceptance Scenarios**:

1. **Given** I define a ZMK-specific keybinding (e.g., Bluetooth control) in my unified keymap, **When** I generate QMK configuration, **Then** the key is replaced with a no-op or alternative keybinding
2. **Given** I define a ZMK-specific keybinding in my unified keymap, **When** I generate ZMK configuration, **Then** the key appears with proper ZMK syntax
3. **Given** I define a QMK-specific keybinding (e.g., QMK combo) in my unified keymap, **When** I generate ZMK configuration, **Then** the key is replaced with a no-op or alternative keybinding
4. **Given** I define a QMK-specific keybinding in my unified keymap, **When** I generate QMK configuration, **Then** the key appears with proper QMK syntax
5. **Given** I add a bootloader key to my unified keymap, **When** I generate both QMK and ZMK configurations, **Then** both include the appropriate reset/bootloader key for their respective firmware

---

### User Story 3 - Board-Specific Layout Extensions (Priority: P2)

As a user with keyboards of different sizes (36-key, 58-key), I want to define board-specific additional keys in the unified configuration layer (not in the QMK/ZMK directories), and have the code generator compile these extensions down into the appropriate board's generated keymap, so that larger keyboards can utilize their extra keys while keeping all configuration centralized and preventing manual edits from being overwritten.

**Why this priority**: Enables the system to support multiple keyboard sizes while maintaining a consistent core layout and keeping all user configuration at the unified config level. Critical for users with diverse keyboard collections and essential to ensure generated QMK/ZMK files remain completely auto-generated.

**Independent Test**: Can be tested by defining a board-specific extension (e.g., number row for a 58-key board) in the unified configuration layer, running code generation, and verifying that: (1) only that board's generated keymap includes the extra keys, (2) the core layout remains identical across all boards, and (3) the board-specific configuration does NOT exist within the QMK/ZMK directories.

**Acceptance Scenarios**:

1. **Given** I have a 36-key board and a 58-key board configured, **When** I define extra keys for the 58-key board in the unified configuration layer, **Then** only the 58-key board's generated keymap includes these keys
2. **Given** I update the core 3x5_3 layout in the unified configuration, **When** I regenerate keymaps for all boards, **Then** all boards reflect the core layout change while preserving their board-specific extensions
3. **Given** I add a gaming layer with number row for a specific larger board in the unified configuration, **When** I generate its keymap, **Then** the gaming layer appears only in that board's generated QMK/ZMK files
4. **Given** I have defined board-specific extensions in the unified configuration, **When** I examine the generated QMK/ZMK directories, **Then** those directories contain ONLY generated code with no user-editable board-specific configuration files
5. **Given** I regenerate keymaps after modifying board-specific extensions, **When** the generation completes, **Then** my board-specific changes are preserved because they live in the unified config layer, not in generated files

---

### User Story 4 - Repository Initialization and Migration (Priority: P1)

As a user with existing QMK and ZMK repositories, I want to initialize a new unified configuration repository and migrate my current keymaps, so that I can start using the single-source system without losing my existing configurations.

**Why this priority**: This is a prerequisite for adopting the system. Without a clear migration path, users cannot begin using the feature.

**Independent Test**: Can be tested by running an initialization command with paths to existing QMK and ZMK repositories, and verifying that a new unified repository is created with the current keymaps converted to the unified format.

**Acceptance Scenarios**:

1. **Given** I have existing QMK userspace and ZMK repositories, **When** I run the initialization command, **Then** a new unified repository is created with proper structure
2. **Given** initialization is complete, **When** I generate keymaps, **Then** the output matches my original QMK and ZMK configurations functionally
3. **Given** I need to continue syncing with upstream QMK/ZMK changes, **When** the repository is structured with submodules or separate directories, **Then** I can independently update each firmware's upstream without affecting the unified keymap configuration

---

### User Story 5 - Easy Board Addition (Priority: P3)

As a user acquiring new keyboards, I want to easily add a new board to my unified configuration by providing minimal information (board identifier, size, firmware type), so that I can quickly get a working keymap without manual file creation.

**Why this priority**: Improves long-term maintainability and user experience. Less critical for initial adoption but important for sustained use.

**Independent Test**: Can be tested by running an "add board" command with board details, and verifying that the necessary configuration structure is created and keymap generation works for the new board.

**Acceptance Scenarios**:

1. **Given** I acquire a new QMK-compatible 36-key keyboard, **When** I run the add-board command with the board identifier, **Then** a board-specific configuration is created using the default 3x5_3 layout
2. **Given** I acquire a new ZMK-compatible keyboard with a different size, **When** I specify the layout size during board addition, **Then** the system creates appropriate configuration with the specified layout
3. **Given** a new board has been added, **When** I run keymap generation, **Then** the new board is included in the build process alongside existing boards

---

### Edge Cases

- What happens when the user defines a keycode that exists in one firmware but not the other (e.g., QMK-specific combo keys, ZMK-specific sticky keys)?
- How does the system determine which features are QMK-specific vs ZMK-specific (feature registry, manual tagging)?
- What fallback behavior is used when a firmware-specific key is filtered out (no-op, transparent, user-defined alternative)?
- How does the system handle layout size changes in the core configuration (migrating from 3x5_3 to 3x6_3)?
- How does the system prevent users from accidentally editing generated QMK/ZMK files (warnings, documentation, file markers)?
- How are firmware-specific behaviors like tap-hold timing configurations handled when they need different values per firmware?
- What happens when upstream QMK or ZMK introduce breaking changes to their keymap syntax?
- How does the system validate that board-specific extensions don't overlap with core layout positions?
- What happens when a new firmware-specific feature is introduced - does the user need to update a feature registry?
- If a user has existing custom code in their QMK/ZMK directories (e.g., OLED implementations), how does this integrate with fully generated keymaps?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST maintain a single source of truth for core keymap layout that generates both QMK and ZMK keymaps
- **FR-002**: System MUST support a core 3x5_3 (36-key) layout definition that is consistent across all keyboards
- **FR-003**: System MUST allow the core layout size to be configurable (not hardcoded to 3x5_3)
- **FR-004**: System MUST generate valid QMK C/header files from the unified keymap configuration
- **FR-005**: System MUST generate valid ZMK keymap files from the unified keymap configuration
- **FR-006**: System MUST support a superset keymap configuration that includes both QMK-specific and ZMK-specific keybindings
- **FR-007**: System MUST bidirectionally filter firmware-incompatible keybindings during generation (strip ZMK-only features from QMK output and QMK-only features from ZMK output)
- **FR-008**: System MUST support board-specific layout extensions (additional keys beyond the core layout)
- **FR-009**: Board-specific layout extensions MUST be defined in the unified configuration layer and compiled down during generation; they MUST NOT exist in the QMK/ZMK directories
- **FR-010**: Generated QMK and ZMK keymap files MUST be completely auto-generated with no user-editable configuration (all user configuration lives in the unified config layer)
- **FR-011**: System MUST keep firmware-specific settings (homerow mod timings, tap-hold parameters, OLED, encoders) separate from keymap configuration
- **FR-012**: System MUST support multiple keyboards of different sizes using the same core layout
- **FR-013**: System MUST provide a command or script to generate all configured keymaps (QMK and ZMK) in a single operation
- **FR-014**: System MUST validate keymap configuration before generation and report errors clearly
- **FR-015**: System MUST preserve bootloader key bindings across both firmwares with firmware-appropriate syntax
- **FR-016**: System MUST provide an initialization process to set up the unified repository structure
- **FR-017**: System MUST support easy addition of new keyboards with minimal configuration
- **FR-018**: System MUST support layer definitions including modifiers, layer-tap keys, and custom keycodes
- **FR-019**: System MUST maintain consistency of modifier keys (Cmd, Alt, Ctrl, Shift) and layer-tap behaviors across firmwares
- **FR-020**: Generated keymaps MUST be completely reproducible (re-running generation produces identical output)

### Key Entities

- **Unified Keymap Configuration**: The single-source-of-truth definition of the keyboard layout, including layers, key positions, and bindings. Contains the core layout (e.g., 3x5_3) that applies to all keyboards.

- **Board Configuration**: Per-keyboard settings defined in the unified configuration layer (not in QMK/ZMK directories) that specify the physical characteristics (keyboard identifier, firmware type, layout size) and board-specific key extensions beyond the core layout. These are compiled down into generated keymaps during code generation.

- **Firmware Profile**: Defines firmware-specific capabilities and limitations (QMK vs ZMK feature sets) to enable proper keycode translation and filtering during generation.

- **Layer Definition**: A named collection of key bindings (e.g., BASE, NAV, NUM, SYM) that applies across all keyboards. Includes modifiers, tap-hold keys, and layer activation keys.

- **Keycode Mapping**: Translation rules between unified keymap representation and firmware-specific keycode syntax (e.g., how a "Bluetooth Next Profile" key maps to ZMK syntax and is stripped from QMK).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can update a key binding in the unified configuration and successfully generate both QMK and ZMK keymaps in under 1 minute
- **SC-002**: Generated keymaps are functionally identical to hand-written configurations (verified through compilation and flashing to physical keyboards)
- **SC-003**: User can add a new keyboard to the system in under 5 minutes with a single command
- **SC-004**: Firmware-specific features (both QMK-specific and ZMK-specific) are correctly filtered and appear only in their supported firmware outputs 100% of the time
- **SC-005**: Board-specific customizations persist across regeneration without manual file edits being overwritten
- **SC-006**: System successfully handles at least 5 different keyboard configurations with varying sizes (36-key to 58-key) from a single source
- **SC-007**: User reports 90% reduction in time spent synchronizing keymap changes across firmwares
- **SC-008**: Generated keymaps compile without errors for both QMK and ZMK 100% of the time (assuming valid input configuration)

## Assumptions *(optional - include if making significant assumptions)*

- The user has basic familiarity with their existing QMK and ZMK repository structures
- The user is comfortable running command-line tools for keymap generation
- The unified keymap format will use a declarative configuration format (e.g., YAML, JSON, or a custom DSL) rather than code
- Board-specific configurations will be stored in separate files or directories to avoid merge conflicts
- Generated files will include clear warnings/markers indicating they are auto-generated and should not be manually edited
- The system will use a monorepo structure with separate directories for QMK and ZMK, or a configuration repo with git submodules pointing to QMK and ZMK repos
- Firmware-specific settings (tap-hold timings, OLED configuration) will remain in their respective firmware configuration files and are out of scope for unified management
- The user's ZMK repository URL will need to be provided as it's a separate repository from the current QMK userspace

## Out of Scope *(optional - include if needed to clarify boundaries)*

- Unifying firmware-specific behavior settings (homerow mod timings, debounce, polling rates) - these remain firmware-specific
- Visual keymap generation (keymap diagrams/ASCII art) - this is handled separately by existing tools
- Automatic upstream synchronization with QMK/ZMK repositories - user manually manages upstream updates
- Migration of git history from existing repositories - only current configuration state is migrated
- Support for firmwares other than QMK and ZMK
- Complex macro definitions or behavior scripts that differ significantly between firmwares - simple macros supported, complex ones remain firmware-specific
- Automated testing of generated keymaps on actual hardware - user responsible for flashing and testing
