# Dragon Haven Cafe - Phase 4 Plan

## Overview

Phase 4 focuses on replayability, personalization, and player engagement features that extend the game's longevity. These features were deferred from Phase 3 due to scope considerations but are now ready for implementation.

## Current State Summary (Post-Phase 3)

| Area | Current | Status |
|------|---------|--------|
| Dragon Stages | 5 | Complete |
| Dragon Abilities | 10 | Complete |
| Zones | 9 | Complete |
| Recipes | 82 | Complete |
| Seasons | 4 | Complete |
| Weather States | 5 | Complete |
| Story Chapters | 8 | Complete |
| Reputation Tiers | 5 | Complete |
| Creatures | 8 types | Complete |
| Achievements | 24 | Complete |

**Estimated Total Playtime:** 15-30+ hours

---

## Phase 4 Features

### 4.1 New Game+ Mode
**Priority: HIGH | Effort: MEDIUM (6-8 hours) | Impact: HIGH**

Allows players to replay the game with carryover benefits and increased challenge.

**Carryover (Kept in NG+):**
- All unlocked recipes
- All achievements
- Dragon naming history
- Character affinity progress (50% retained)

**Reset (Fresh Start):**
- Dragon (new egg)
- Gold/currency (start with bonus 500g)
- Reputation (start at 50)
- Story progression (replay from beginning)
- Inventory (empty)

**NG+ Modifiers:**
| Modifier | Effect |
|----------|--------|
| Customer Expectations | +20% quality required |
| Time Pressure | Service periods 10% shorter |
| Resource Scarcity | 20% fewer spawns in zones |
| Bonus Gold | +25% from all sales |
| Reputation Decay | Slower decay rate |

**Implementation:**
- [ ] Add NG+ flag to save data
- [ ] Create NG+ unlock condition (complete Finale chapter)
- [ ] Implement carryover logic in save system
- [ ] Add difficulty modifiers to relevant systems
- [ ] Create NG+ indicator in HUD
- [ ] Add NG+ counter (NG+1, NG+2, etc.)

**Files to Modify:**
- `src/constants.py` - NG+ constants and modifiers
- `src/game_state.py` - Carryover logic
- `src/save_manager.py` - NG+ save handling
- `src/systems/cafe.py` - Customer expectations modifier
- `src/systems/time_system.py` - Time pressure modifier
- `src/systems/resources.py` - Scarcity modifier
- `src/ui/hud.py` - NG+ indicator

---

### 4.2 Dragon Customization System
**Priority: HIGH | Effort: MEDIUM (8-10 hours) | Impact: HIGH**

Adds cosmetic customization options for the dragon companion.

**Customization Categories:**

#### Accessories (Unlockable)
| Item | Unlock Condition | Visual |
|------|------------------|--------|
| Red Scarf | Reach 100 reputation | Neck wrap |
| Chef Hat | Master 10 recipes | Small toque |
| Flower Crown | Befriend all characters | Floral headpiece |
| Crystal Pendant | Complete Ancient Ruins | Glowing necklace |
| Cloud Wings | Visit Sky Islands 10x | Ethereal wing decorations |
| Golden Collar | Earn 10,000 total gold | Ornate collar |

#### Color Patterns (Earned)
| Pattern | Unlock Condition | Effect |
|---------|------------------|--------|
| Spots | Reach Juvenile stage | Spotted pattern overlay |
| Stripes | Reach Adolescent stage | Tiger stripe pattern |
| Gradient | Reach Adult stage | Color fade effect |
| Starlight | Collect 50 starlight crystals | Sparkle particles |
| Flame | Use Fire Stream 100x | Ember particle trail |

#### Special Effects (Achievement Rewards)
| Effect | Achievement | Visual |
|--------|-------------|--------|
| Sparkle Trail | "Best Friends" | Particles when moving |
| Glow Aura | "Legendary Status" | Soft glow around dragon |
| Mini Crown | "Recipe Master" | Tiny floating crown |

**Implementation:**
- [ ] Create DragonCustomization class
- [ ] Add customization slots (head, neck, back, effect)
- [ ] Implement unlock tracking
- [ ] Update sprite generation for accessories
- [ ] Create customization menu screen
- [ ] Add particle effects system for special effects
- [ ] Save/load customization choices

**Files to Create:**
- `src/systems/customization.py` (NEW)
- `src/states/customization_state.py` (NEW)

**Files to Modify:**
- `src/constants.py` - Customization definitions
- `src/entities/dragon.py` - Customization data
- `src/sprites.py` - Accessory/effect rendering
- `src/game_state.py` - Save customization
- `src/states/dragon_status_state.py` - Link to customization

---

### 4.3 Seasonal Events System
**Priority: MEDIUM | Effort: MEDIUM (6-8 hours) | Impact: MEDIUM**

Adds special events tied to in-game seasons with unique content.

**Event Calendar:**
| Season | Event | Duration | Features |
|--------|-------|----------|----------|
| Spring | Dragon Hatching Festival | Days 1-5 | +50% dragon bond gain, special hatchling decorations |
| Summer | Harvest Moon Feast | Days 15-20 | Double ingredient quality, fireworks at night |
| Autumn | Lantern Festival | Days 25-30 | Cafe decorations, exclusive recipes, +25% tips |
| Winter | Frost Dragon Celebration | Days 35-40 | Snow effects, warm drink bonuses, gift exchange |

**Event Components:**

#### Decorations
- Seasonal cafe decorations (auto-applied during events)
- Zone visual changes (festival banners, lights)
- Special weather effects (confetti, snow, fireflies)

#### Limited-Time Recipes (4 per season)
| Season | Recipe | Special Ingredient |
|--------|--------|-------------------|
| Spring | Blossom Tea | Cherry blossom (Spring only) |
| Summer | Starlight Sorbet | Moonberries (Summer nights) |
| Autumn | Lantern Cake | Festival spice (Autumn only) |
| Winter | Frost Cocoa | Ice crystals (Winter only) |

#### Event Customers
- Festival-themed customers with higher tips
- Special requests related to seasonal recipes
- Event-exclusive character visits

**Implementation:**
- [ ] Create EventManager singleton
- [ ] Define event schedule based on game days
- [ ] Implement seasonal decorations system
- [ ] Add limited-time recipes with availability checks
- [ ] Create event customer types
- [ ] Add event notification system
- [ ] Event participation tracking for achievements

**Files to Create:**
- `src/systems/events.py` (NEW)
- `src/ui/event_banner.py` (NEW)

**Files to Modify:**
- `src/constants.py` - Event definitions
- `src/systems/time_system.py` - Event triggers
- `src/systems/recipes.py` - Seasonal availability
- `src/entities/customer.py` - Event customers
- `src/sprites.py` - Decorations and effects
- `src/ui/hud.py` - Event indicator

---

### 4.4 Quality of Life Improvements
**Priority: MEDIUM | Effort: LOW (3-4 hours) | Impact: MEDIUM**

Small but impactful improvements based on playtesting feedback.

**Features:**
- [ ] Quick-restart option (skip intro on subsequent plays)
- [ ] Recipe favorites system (pin frequently used recipes)
- [ ] Ingredient auto-sort in inventory
- [ ] Customer queue preview (see next 3 customers)
- [ ] Zone resource preview (see available resources before entering)
- [ ] Stats summary screen (total gold earned, dishes served, etc.)

**Files to Modify:**
- `src/states/recipe_book_state.py` - Favorites
- `src/systems/inventory.py` - Auto-sort
- `src/systems/cafe.py` - Queue preview
- `src/systems/world.py` - Resource preview
- `src/states/pause_menu_state.py` - Stats summary

---

## Deferred Features (Phase 5+)

### Multiplayer/Sharing System
**Reason:** Requires networking infrastructure (100+ hours estimated)
- Recipe sharing between players
- Cafe visits
- Cooperative events
- Leaderboards

Will be considered if Phase 4 is successful and player demand exists.

---

## Implementation Order

### Sprint 1: Foundation (6-8 hours)
1. **New Game+ Mode** - Core replayability feature

### Sprint 2: Personalization (8-10 hours)
2. **Dragon Customization** - Player attachment feature

### Sprint 3: Events & Polish (9-12 hours)
3. **Seasonal Events** - Content variety
4. **QoL Improvements** - Polish

---

## Task Breakdown

| Task ID | Feature | Description | Effort |
|---------|---------|-------------|--------|
| 058 | NG+ Foundation | NG+ save flag, unlock condition | 2 hrs |
| 059 | NG+ Carryover | Recipe/achievement retention | 2 hrs |
| 060 | NG+ Modifiers | Difficulty scaling system | 2-3 hrs |
| 061 | Customization System | Core customization manager | 3 hrs |
| 062 | Accessories | 6 unlockable accessories | 2-3 hrs |
| 063 | Color Patterns | 5 pattern types | 2 hrs |
| 064 | Special Effects | Particle effects system | 2-3 hrs |
| 065 | Customization Screen | UI for equipping items | 2 hrs |
| 066 | Event Manager | Core event system | 2-3 hrs |
| 067 | Seasonal Decorations | Cafe/zone visuals | 2 hrs |
| 068 | Limited Recipes | 16 seasonal recipes | 2 hrs |
| 069 | Event Customers | Festival customer types | 2 hrs |
| 070 | QoL Bundle | All QoL improvements | 3-4 hrs |

**Total Estimated: 26-35 hours**

---

## Success Criteria (Phase 4)

- [ ] New Game+ mode unlockable after completing story
- [ ] NG+ counter tracks multiple playthroughs
- [ ] 6+ dragon accessories unlockable
- [ ] 5+ color patterns available
- [ ] Particle effects system working
- [ ] Customization screen functional
- [ ] 4 seasonal events active
- [ ] 16 limited-time recipes available
- [ ] QoL improvements implemented
- [ ] All Phase 1-3 functionality preserved
- [ ] No performance degradation (maintain 60 FPS)

---

## Notes

- Each feature should be implemented on a feature branch
- Run full game test after each feature completion
- Update DECISIONS.md for any design choices
- Commit messages: `[P4-N] Description` where N is task number
- NG+ Mode is the foundation - implement first
- Customization requires sprite generation updates
- Events integrate with existing time/season systems

---

*Created: January 21, 2026*
*Review: After Sprint 1 completion*
