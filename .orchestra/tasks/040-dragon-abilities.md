# Task 040: Additional Dragon Abilities

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 040 |
| **Status** | done |
| **Branch** | task/040 |
| **Assigned** | task/040 |
| **Depends** | 039 |
| **Blocked-By** | |
| **Estimated** | 150 min |

## Inputs
- src/entities/dragon.py (with 5 stages from 039)
- src/states/exploration_mode_state.py (ability usage)

## Description
Add the 5 missing dragon abilities: Creature Scare (Juvenile), Glide (Adolescent), Ember Breath (Adolescent), Full Flight (Adult), Fire Stream (Adult). Each ability has unique effects in exploration.

## Acceptance Criteria
- [x] Add ability constants and stamina costs:
  - creature_scare: 20 stamina (Juvenile+)
  - glide: 3 stamina/sec (Adolescent+)
  - ember_breath: 25 stamina (Adolescent+)
  - full_flight: 5 stamina/sec (Adult)
  - fire_stream: 40 stamina (Adult)
- [x] Implement creature_scare:
  - Frightens hostile creatures temporarily
  - Visual scare effect
  - Useful for safe passage
- [x] Implement glide:
  - Descend from heights safely
  - Can reach elevated platforms
  - Continuous stamina drain while active
- [x] Implement ember_breath:
  - Lights torches in zones
  - Clears bramble obstacles
  - Visual fire effect
- [x] Implement full_flight:
  - Fast travel between zone exits
  - Access flight-only areas
  - Continuous stamina drain
- [x] Implement fire_stream:
  - Clears major obstacles
  - More powerful than ember_breath
  - Cool visual effect
- [x] Update DRAGON_STAGE_ABILITIES mapping
- [x] Add ability UI hotkeys (1-5 or Q-T)
- [x] Add ability visual effects in sprites.py

## Context Files
- src/entities/dragon.py
- src/constants.py
- src/states/exploration_mode_state.py
- src/sprites.py
- src/ui/hud.py

## Outputs
- Modified: src/constants.py (ability definitions, continuous ability support)
- Modified: src/entities/dragon.py (ability methods, continuous ability tracking)
- Modified: src/states/exploration_mode_state.py (ability usage, visual effects)
- Modified: src/states/dragon_status_state.py (expanded abilities panel)
- Modified: src/entities/player.py (ability hotkeys 1-0)

---

## Work Log

### Session 1
- Added 5 new abilities with stamina costs:
  - creature_scare (20), ember_breath (25), fire_stream (40) - instant
  - glide (3/sec), full_flight (5/sec) - continuous drain
- Created DRAGON_ABILITY_CONTINUOUS dict for continuous abilities
- Added DRAGON_ABILITY_DESCRIPTIONS for UI
- Updated DRAGON_STAGE_ABILITIES: 10 total abilities across all stages
- Added dragon.py methods for continuous abilities:
  - is_continuous_ability(), start_continuous_ability(), stop_continuous_ability()
  - is_ability_active(), get_active_ability()
  - _update_continuous_ability() for stamina drain
- Updated dragon status screen with expanded abilities panel (430px height)
- Added visual effects for all new abilities in exploration mode
- Added ability hotkeys 1-0 (10 abilities total)
- Added active ability indicator in controls hint
