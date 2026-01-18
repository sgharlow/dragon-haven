# Task 008: Dragon Entity System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 008 |
| **Status** | done |
| **Branch** | task/008 |
| **Assigned** | task/008 |
| **Depends** | 004, 007 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/sprites.py from 004
- src/systems/time_system.py from 007

## Description
Create the dragon entity system - the heart of the game. Handles dragon stats, life stages, abilities, color changes from food, and bonding mechanics.

## Acceptance Criteria
- [x] Dragon class with all stats:
  - Hunger (0-100, decreases over time)
  - Happiness (0-100, affects abilities)
  - Bond Level (0-1000, lifetime accumulation)
  - Stamina (0-100, used by abilities)
- [x] 3 life stages: EGG, HATCHLING, JUVENILE
  - EGG: Days 1-3, no abilities
  - HATCHLING: Days 4-10, small size, basic abilities
  - JUVENILE: Days 11+, medium size, more abilities
- [x] Stage progression based on days alive
- [x] Color RGB system (0.0-1.0 each channel)
- [x] Color changes gradually based on food consumed
- [x] feed(recipe) method that affects stats and color
- [x] pet() method that increases happiness and bond
- [x] update(dt) for stat decay and stage checks
- [x] Dragon abilities: burrow_fetch (hatchling), sniff_track (hatchling), rock_smash (juvenile)
- [x] Ability stamina costs
- [x] Serialization for save/load

## Context Files
- src/sprites.py
- src/systems/time_system.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 3)

## Outputs
- Created: src/entities/dragon.py (Dragon class)
- Created: src/entities/__init__.py
- Modified: src/constants.py (dragon stats, stage configs)

---

## Work Log

### 2026-01-17
- Added dragon constants to constants.py (stages, stat ranges, decay rates, abilities)
- Created DragonColor class for RGB color shift system
- Created Dragon class with full stat management (hunger, happiness, stamina, bond)
- Implemented 3 life stages with automatic progression based on age
- Added stat decay over time (hunger decreases, happiness affected by hunger)
- Implemented feed() method with color influence and quality multiplier
- Implemented pet() method for happiness and bond bonus
- Added ability system with stage-unlocked abilities and stamina costs
- Implemented serialization (get_state/load_state/from_state)
- Added helper methods: get_mood(), get_stage_progress(), stat queries
- Updated entities/__init__.py
- All tests pass
