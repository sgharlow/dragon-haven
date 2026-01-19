# Task 040: Additional Dragon Abilities

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 040 |
| **Status** | blocked |
| **Branch** | |
| **Assigned** | |
| **Depends** | 039 |
| **Blocked-By** | Requires new dragon stages |
| **Estimated** | 150 min |

## Inputs
- src/entities/dragon.py (with 5 stages from 039)
- src/states/exploration_mode_state.py (ability usage)

## Description
Add the 5 missing dragon abilities: Creature Scare (Juvenile), Glide (Adolescent), Ember Breath (Adolescent), Full Flight (Adult), Fire Stream (Adult). Each ability has unique effects in exploration.

## Acceptance Criteria
- [ ] Add ability constants and stamina costs:
  - creature_scare: 20 stamina (Juvenile+)
  - glide: 3 stamina/sec (Adolescent+)
  - ember_breath: 25 stamina (Adolescent+)
  - full_flight: 5 stamina/sec (Adult)
  - fire_stream: 40 stamina (Adult)
- [ ] Implement creature_scare:
  - Frightens hostile creatures temporarily
  - Visual scare effect
  - Useful for safe passage
- [ ] Implement glide:
  - Descend from heights safely
  - Can reach elevated platforms
  - Continuous stamina drain while active
- [ ] Implement ember_breath:
  - Lights torches in zones
  - Clears bramble obstacles
  - Visual fire effect
- [ ] Implement full_flight:
  - Fast travel between zone exits
  - Access flight-only areas
  - Continuous stamina drain
- [ ] Implement fire_stream:
  - Clears major obstacles
  - More powerful than ember_breath
  - Cool visual effect
- [ ] Update DRAGON_STAGE_ABILITIES mapping
- [ ] Add ability UI hotkeys (1-5 or Q-T)
- [ ] Add ability visual effects in sprites.py

## Context Files
- src/entities/dragon.py
- src/constants.py
- src/states/exploration_mode_state.py
- src/sprites.py
- src/ui/hud.py

## Outputs
- Modified: src/constants.py (ability definitions)
- Modified: src/entities/dragon.py (ability methods)
- Modified: src/states/exploration_mode_state.py (ability usage)
- Modified: src/sprites.py (ability effects)
- Modified: src/ui/hud.py (ability UI)

---

## Work Log
