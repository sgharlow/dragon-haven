# Project Goal: Dragon Haven Cafe

## Vision
Build a playable prototype of Dragon Haven Cafe - a dragon-raising cafe management simulation game using Python and Pygame.

## Scope (Prototype Version)
This is a **focused prototype** demonstrating core mechanics, not a full production game. We're building a complete, polished vertical slice.

### Core Features (Must Have)
1. **Dragon System**
   - 3 life stages: Egg → Hatchling → Juvenile (simplified from 5)
   - Core stats: Hunger, Happiness, Bond Level
   - Color system based on food consumed
   - 2-3 abilities that unlock with growth

2. **Cafe System**
   - Single service period per day (simplified)
   - 3 staff members with morale system
   - 10-15 recipes with cooking minigame (rhythm-based)
   - Customer satisfaction and reputation (0-100)

3. **World & Exploration**
   - 3 zones: Cafe Grounds, Meadow Fields, Forest Depths
   - Resource gathering with respawn system
   - Day/night cycle (simplified - morning/afternoon/evening)
   - 2 seasons (Spring/Summer)

4. **Story System**
   - Prologue + 2 story chapters
   - 3 story characters with relationship system
   - Basic dialogue system with choices

5. **UI/Screens**
   - Main Menu, Settings, Save/Load
   - Gameplay HUD (time, dragon status, gold)
   - Cafe Mode (kitchen, serving area)
   - Exploration Mode (zone navigation)
   - Inventory and Recipe Book
   - Dragon Status screen

### Tech Stack
- Python 3.8+
- Pygame 2.0+
- JSON for save data
- Procedural sprite generation (like Space Station Defense)

### Quality Targets
- 60 FPS gameplay
- All screens functional and polished
- 15-30 minutes of gameplay loop
- Save/Load working
- No crashes during normal play

## Success Criteria (Phase 1 - COMPLETE ✓)
- [x] Can hatch and raise a dragon through 3 stages
- [x] Dragon color changes based on food
- [x] Can run cafe service with customers
- [x] Cooking minigame is fun and functional
- [x] Can explore 3 zones and gather ingredients
- [x] Day/night cycle affects gameplay
- [x] Story events trigger and progress
- [x] Save/Load preserves all game state
- [x] Polished UI with consistent visual style

---

## Phase 2: Expansion (Closing Spec Gaps)

Building on the successful prototype, this phase brings the game closer to the full specification.

### Expansion Scope
See `.orchestra/EXPANSION_PLAN.md` for detailed implementation plan.

**Priority 1 - Foundation:**
- Dragon naming system
- Autumn & Winter seasons (4 total)
- Stormy & Special weather (5 total)

**Priority 2 - Dragon Expansion:**
- Adolescent & Adult stages (5 total)
- 5 additional abilities (8 total)

**Priority 3 - World Expansion:**
- Coastal Shore & Mountain Pass zones (5 total)
- 15-20 additional recipes (30-35 total)

**Priority 4 - Story & Depth:**
- Evening service period (2 periods/day)
- 2 additional story chapters (7 total)
- Character affinity system (0-100 per character)

### Success Criteria (Phase 2)
- [ ] Dragon progresses through 5 life stages
- [ ] 8 dragon abilities available across stages
- [ ] 5 explorable zones
- [ ] 30+ recipes
- [ ] 4 seasons with 5 weather types
- [ ] 7 story chapters
- [ ] Evening service period active
- [ ] Character affinity tracking
- [ ] Named dragon companion
- [ ] All Phase 1 functionality preserved
