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

### Success Criteria (Phase 2 - COMPLETE ✓)
- [x] Dragon progresses through 5 life stages
- [x] 10 dragon abilities available across stages (exceeds spec)
- [x] 7 explorable zones (exceeds spec)
- [x] 76 recipes (exceeds spec)
- [x] 4 seasons with 5 weather types
- [x] 8 story chapters (exceeds spec)
- [x] Evening service period active
- [x] Character affinity tracking
- [x] Named dragon companion
- [x] All Phase 1 functionality preserved

---

## Phase 3: Polish & End-Game Content

See `.orchestra/PHASE3_PLAN.md` for detailed implementation plan.

**Included:**
- Legendary reputation tier (5th tier)
- Recipe completion (80+ total)
- Creature system for exploration
- Achievements system
- Ancient Ruins zone
- Sky Islands zone

**Deferred to Phase 4+:**
- Multiplayer/Sharing (requires networking infrastructure)
- New Game+ mode (nice-to-have, not core)
- Extensive dragon customization (cosmetic-only)
- Seasonal events system (live-service model)

### Success Criteria (Phase 3 - COMPLETE ✓)
- [x] 5 reputation tiers including Legendary
- [x] 82 recipes available
- [x] Creature system with 8 creature types
- [x] 24 achievements trackable
- [x] 9 explorable zones
- [x] All Phase 1 & 2 functionality preserved

---

## Phase 4: Replayability & Personalization

See `.orchestra/PHASE4_PLAN.md` for detailed implementation plan.

**Included:**
- New Game+ Mode (carryover, difficulty scaling)
- Dragon Customization System (accessories, patterns, effects)
- Seasonal Events System (4 events, limited recipes)
- Quality of Life Improvements

**Deferred to Phase 5+:**
- Multiplayer/Sharing System (requires networking infrastructure)

### Success Criteria (Phase 4 - COMPLETE ✓)
- [x] New Game+ mode unlockable after completing story
- [x] NG+ counter tracks multiple playthroughs
- [x] 6+ dragon accessories unlockable (6 implemented)
- [x] 5+ color patterns available (5 implemented)
- [x] Customization screen functional
- [x] 4 seasonal events active
- [x] 16 limited-time recipes available
- [x] QoL improvements implemented (favorites, auto-sort, stats)
- [x] All Phase 1-3 functionality preserved (237/237 tests pass)
