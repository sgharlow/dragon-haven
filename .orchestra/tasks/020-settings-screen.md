# Task 020: Settings Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 020 |
| **Status** | ready |
| **Branch** | task/020 |
| **Assigned** | |
| **Depends** | 003, 005 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/state_manager.py from 003
- src/sound_manager.py from 005

## Description
Create the settings screen for adjusting game options. Accessible from main menu and pause menu.

## Acceptance Criteria
- [ ] SettingsState extending BaseScreen
- [ ] Settings categories:
  - Audio: Master volume, SFX volume, Music volume (sliders 0-100)
  - Gameplay: Game speed (0.75x, 1x, 1.25x), Cooking difficulty (Easy/Normal)
  - Display: Fullscreen toggle
- [ ] Slider UI component for volume
- [ ] Toggle UI component for on/off settings
- [ ] Dropdown/selector for multiple choice
- [ ] Changes apply immediately (preview)
- [ ] Save settings to config file
- [ ] Load settings on game start
- [ ] Back button returns to previous screen
- [ ] Reset to defaults option

## Context Files
- src/states/base_state.py
- src/sound_manager.py
- src/constants.py

## Outputs
- Created: src/states/settings_state.py (SettingsState)
- Created: src/ui/slider.py (Slider component)
- Created: src/ui/toggle.py (Toggle component)
- Modified: src/constants.py (default settings)

---

## Work Log

