# Dragon Haven Cafe - Phase 3 Plan

## Overview

Phase 3 focuses on polish, end-game content, and player engagement features. This phase builds on the complete Phase 1 (prototype) and Phase 2 (expansion) foundations.

## Current State Summary

| Area | Current | Original Spec | Status |
|------|---------|---------------|--------|
| Dragon Stages | 5 | 5 | ✅ Complete |
| Dragon Abilities | 10 | 8 | ✅ Exceeds Spec |
| Zones | 7 | 7 | ✅ Complete |
| Recipes | 76 | 80+ | 🔶 4 short |
| Seasons | 4 | 4 | ✅ Complete |
| Weather States | 5 | 5 | ✅ Complete |
| Story Chapters | 8 | 8 | ✅ Complete |
| Service Periods | 2 | 2 | ✅ Complete |
| Reputation Tiers | 4 | 5 | 🔶 Missing Legendary |
| Character Affinity | ✅ | ✅ | ✅ Complete |

---

## Phase 3 Features (Prioritized)

### Priority 1: Quick Wins (Low Effort, High Impact)

#### 3.1 Legendary Reputation Tier
**Effort: LOW (1-2 hours) | Impact: MEDIUM**

Add the 5th and final reputation tier for end-game players.

**Implementation:**
- Add `REPUTATION_LEGENDARY` constant (threshold: 500+)
- Update reputation tier calculation in CafeManager
- Add legendary tier benefits:
  - 25% tip bonus
  - Access to VIP customers
  - Unlock legendary recipes
- Update HUD to display legendary status

**Files to Modify:**
- `src/constants.py` - Add tier constant
- `src/systems/cafe.py` - Tier calculation
- `src/ui/hud.py` - Display updates

---

#### 3.2 Recipe Completion (80+ Recipes)
**Effort: LOW (2-3 hours) | Impact: MEDIUM**

Add 4-6 more recipes to exceed the 80 recipe target.

**Proposed Recipes:**
| Recipe | Category | Difficulty | Key Ingredients |
|--------|----------|------------|-----------------|
| Legendary Dragon Feast | Special | 5 | Dragon scale herb, premium meat, exotic spice |
| Mythic Tea Ceremony | Beverage | 4 | Premium tea, rare flower, honey |
| Ancient Ruins Relic Cake | Dessert | 4 | Flour, exotic spice, crystal honey |
| Sky Island Cloud Puffs | Dessert | 3 | Cream, egg, alpine ingredients |
| Storm Brew | Beverage | 3 | Storm flowers, honey, herb |
| Founders' Original Recipe | Main | 5 | Secret combination (unlocks with story) |

**Files to Modify:**
- `src/constants.py` - Recipe definitions

---

### Priority 2: Content Expansion (Medium Effort)

#### 3.3 Creature System
**Effort: MEDIUM (6-8 hours) | Impact: HIGH**

Add wildlife creatures to exploration zones that interact with dragon abilities.

**Creature Types:**
| Creature | Zones | Behavior | Dragon Interaction |
|----------|-------|----------|-------------------|
| Forest Sprites | Forest, Meadow | Friendly, give hints | Feed for bonus items |
| Wild Boars | Forest, Mountain | Aggressive, block paths | Creature Scare to clear |
| Cliff Birds | Mountain, Coastal | Neutral, carry items | Flight to reach nests |
| Shore Crabs | Coastal | Defensive, guard resources | Rock Smash to reveal |
| Cave Bats | Crystal Cave | Skittish, flee from light | Ember Breath reveals hidden areas |

**Implementation:**
- Create `Creature` entity class
- Add creature spawn points to zones
- Implement creature AI behaviors (patrol, flee, guard)
- Connect creature interactions to dragon abilities
- Add creature sprites to procedural generation

**Files to Create/Modify:**
- `src/entities/creature.py` (NEW)
- `src/systems/creature_manager.py` (NEW)
- `src/constants.py` - Creature definitions
- `src/systems/world.py` - Creature spawning
- `src/states/exploration_mode_state.py` - Creature interactions
- `src/sprites.py` - Creature sprite generation

---

#### 3.4 Achievements System
**Effort: MEDIUM (4-6 hours) | Impact: HIGH**

Track player accomplishments and provide rewards.

**Achievement Categories:**

**Dragon Milestones:**
- First Steps (Hatch dragon)
- Growing Up (Reach Juvenile)
- Coming of Age (Reach Adolescent)
- Full Grown (Reach Adult)
- Best Friends (Max bond level)

**Cafe Milestones:**
- Grand Opening (Complete first service)
- Rising Star (Reach 100 reputation)
- Master Chef (Reach Master tier)
- Legendary Status (Reach Legendary tier)
- Recipe Collector (Unlock 50 recipes)
- Recipe Master (Master 25 recipes)

**Exploration Milestones:**
- Explorer (Visit all zones)
- Gatherer (Collect 100 ingredients)
- Treasure Hunter (Find all rare resources)

**Story Milestones:**
- Chapter completion achievements
- Character affinity achievements

**Implementation:**
- Create `AchievementManager` singleton
- Define achievement conditions and rewards
- Add achievement popup notifications
- Create achievements screen/menu
- Save/load achievement progress

**Files to Create/Modify:**
- `src/systems/achievements.py` (NEW)
- `src/constants.py` - Achievement definitions
- `src/ui/achievement_popup.py` (NEW)
- `src/states/achievements_state.py` (NEW)
- `src/game_state.py` - Save/load achievements

---

### Priority 3: End-Game Content (Higher Effort)

#### 3.5 Ancient Ruins Zone
**Effort: HIGH (4-6 hours) | Impact: MEDIUM**

Add the 8th explorable zone with unique mechanics.

**Zone Details:**
- **Unlock Requirement:** Adolescent dragon + Chapter 5 complete
- **Theme:** Mysterious ancient dragon civilization ruins
- **Primary Resources:** Ancient spices, relic fragments, crystal shards
- **Special Mechanic:** Puzzle elements (pressure plates, hidden doors)
- **Hazards:** Crumbling floors, ancient traps

**Unique Features:**
- Hidden recipe scrolls (unlock legendary recipes)
- Dragon lore tablets (backstory content)
- Relic collection quest

**Files to Modify:**
- `src/constants.py` - Zone and ingredient definitions
- `src/systems/world.py` - Zone data
- `src/sprites.py` - Ruins tile generation
- `src/systems/resources.py` - New spawn points

---

#### 3.6 Sky Islands Zone
**Effort: HIGH (4-6 hours) | Impact: MEDIUM**

Add the 9th and final explorable zone for end-game players.

**Zone Details:**
- **Unlock Requirement:** Adult dragon with Full Flight ability
- **Theme:** Floating islands above the clouds
- **Primary Resources:** Sky berries, cloud essence, starlight crystals
- **Special Mechanic:** Flight-based traversal between islands
- **Weather:** Always special (clear skies above storms)

**Unique Features:**
- Legendary ingredient farming
- Dragon racing mini-game (optional)
- Final story revelation location

**Files to Modify:**
- `src/constants.py` - Zone and ingredient definitions
- `src/systems/world.py` - Zone data with flight mechanics
- `src/sprites.py` - Sky island tile generation
- `src/systems/resources.py` - Legendary spawn points

---

## Deferred Features (Phase 4 or Beyond)

The following features are deferred due to scope, complexity, or diminishing returns:

### ❌ Multiplayer/Sharing System
**Reason:** Requires networking infrastructure, server backend, database, authentication. This is essentially building a second game on top of the existing one. Estimated effort: 100+ hours.

**If implemented later:**
- Share recipes with friends
- Visit other players' cafes
- Cooperative events
- Leaderboards

---

### ❌ New Game+ Mode
**Reason:** Nice-to-have but not core to the experience. Current content provides 15-30+ hours of gameplay. Can be added if player demand exists.

**If implemented later:**
- Keep recipes/achievements
- Harder difficulty scaling
- New story variations
- Exclusive NG+ content

---

### ❌ Extensive Dragon Customization
**Reason:** Would require significant sprite generation rework for accessories, markings, and cosmetics. Medium-high effort for cosmetic-only benefit.

**If implemented later:**
- Hats, scarves, accessories
- Color pattern variations
- Earned cosmetics from achievements

---

### ❌ Seasonal Events System
**Reason:** Requires ongoing content creation and calendar-based triggers. Better suited for a live-service model.

**If implemented later:**
- Holiday-themed decorations
- Limited-time recipes
- Special event customers

---

## Implementation Order

### Sprint 1: Quick Wins (3-5 hours)
1. ✅ Legendary Reputation Tier (1-2 hours)
2. ✅ Recipe Completion to 80+ (2-3 hours)

### Sprint 2: Core Systems (10-14 hours)
3. Creature System (6-8 hours)
4. Achievements System (4-6 hours)

### Sprint 3: End-Game Zones (8-12 hours)
5. Ancient Ruins Zone (4-6 hours)
6. Sky Islands Zone (4-6 hours)

---

## Success Criteria (Phase 3)

- [ ] 5 reputation tiers including Legendary
- [ ] 80+ recipes available
- [ ] Creature system with 5+ creature types
- [ ] 20+ achievements trackable
- [ ] 9 explorable zones (including Ancient Ruins & Sky Islands)
- [ ] All Phase 1 & 2 functionality preserved
- [ ] No performance degradation (maintain 60 FPS)

---

## Estimated Total Effort

| Priority | Features | Estimated Hours |
|----------|----------|-----------------|
| Priority 1 | Quick Wins | 3-5 hours |
| Priority 2 | Core Systems | 10-14 hours |
| Priority 3 | End-Game Zones | 8-12 hours |
| **Total** | | **21-31 hours** |

---

## Notes

- Each feature should be implemented on a feature branch
- Run full game test after each feature completion
- Update DECISIONS.md for any design choices
- Commit messages: `[P3-N] Description` where N is feature number
- Priority 1 items can be done independently
- Priority 2 & 3 items may have interdependencies (creatures in new zones)
