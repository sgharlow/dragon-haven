# Task 020: Settings Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 020 |
| **Status** | done |
| **Branch** | task/020 |
| **Assigned** | task/020 |
| **Depends** | 003, 005 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/state_manager.py from 003
- src/sound_manager.py from 005

## Description
Create the settings screen for adjusting game options. Accessible from main menu and pause menu.

## Acceptance Criteria
- [x] SettingsState extending BaseScreen
- [x] Settings categories:
  - Audio: Master volume, SFX volume, Music volume (sliders 0-100)
  - Gameplay: Game speed (0.75x, 1x, 1.25x), Cooking difficulty (Easy/Normal)
  - Display: Fullscreen toggle
- [x] Slider UI component for volume
- [x] Toggle UI component for on/off settings
- [x] Dropdown/selector for multiple choice
- [x] Changes apply immediately (preview)
- [x] Save settings to config file
- [x] Load settings on game start
- [x] Back button returns to previous screen
- [x] Reset to defaults option

## Context Files
- src/states/base_state.py
- src/sound_manager.py
- src/constants.py

## Outputs
- Created: src/states/settings_state.py (SettingsState class)
- Created: src/ui/components.py (Slider, Toggle, Selector, Button classes)
- Modified: src/ui/__init__.py (export new components)
- Modified: src/constants.py (settings constants and defaults)
- Modified: src/main.py (register SettingsState)

---

## Work Log

### 2026-01-17
- Added settings constants to constants.py (DEFAULT_SETTINGS, SETTINGS_FILE, etc.)
- Created ui/components.py with Slider, Toggle, Selector, and Button classes
- Created states/settings_state.py with full SettingsState implementation
- Settings categories: Audio (3 sliders), Gameplay (2 selectors), Display (1 toggle)
- Implemented immediate preview of changes via _apply_preview()
- Added JSON save/load for settings persistence
- Updated ui/__init__.py to export new components
- Updated main.py to register SettingsState
- All tests pass: components work, state works, imports work

