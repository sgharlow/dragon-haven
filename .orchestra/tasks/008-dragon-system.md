# Task 008: Dragon Entity System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 008 |
| **Status** | ready |
| **Branch** | task/008 |
| **Assigned** | |
| **Depends** | 004, 007 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/sprites.py from 004
- src/systems/time_system.py from 007

## Description
Create the dragon entity system - the heart of the game. Handles dragon stats, life stages, abilities, color changes from food, and bonding mechanics.

## Acceptance Criteria
- [ ] Dragon class with all stats:
  - Hunger (0-100, decreases over time)
  - Happiness (0-100, affects abilities)
  - Bond Level (0-1000, lifetime accumulation)
  - Stamina (0-100, used by abilities)
- [ ] 3 life stages: EGG, HATCHLING, JUVENILE
  - EGG: Days 1-3, no abilities
  - HATCHLING: Days 4-10, small size, basic abilities
  - JUVENILE: Days 11+, medium size, more abilities
- [ ] Stage progression based on days alive
- [ ] Color RGB system (0.0-1.0 each channel)
- [ ] Color changes gradually based on food consumed
- [ ] feed(recipe) method that affects stats and color
- [ ] pet() method that increases happiness and bond
- [ ] update(dt) for stat decay and stage checks
- [ ] Dragon abilities: burrow_fetch (hatchling), sniff_track (hatchling), rock_smash (juvenile)
- [ ] Ability stamina costs
- [ ] Serialization for save/load

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

