# Dragon Haven Cafe - Expansion Plan

## Overview

This document outlines the top 10 gaps between the current prototype and the full specification, prioritized by impact and feasibility. These enhancements will bring the game closer to the original vision while building on the solid foundation already in place.

## Current State vs Full Spec Summary

| Area | Current | Spec | Gap |
|------|---------|------|-----|
| Dragon Stages | 3 | 5 | -2 (Adolescent, Adult) |
| Dragon Abilities | 3 | 8 | -5 |
| Zones | 3 | 7 | -4 |
| Recipes | 15 | 80+ | -65+ |
| Seasons | 2 | 4 | -2 (Autumn, Winter) |
| Weather States | 3 | 5 | -2 (Stormy, Special) |
| Story Chapters | 5 | 8 | -3 |
| Service Periods | 1 | 2 | -1 (Evening) |
| Reputation Tiers | 4 | 5 | -1 (Legendary) |
| Character Affinity | None | 0-100/character | Missing |

---

## Top 10 Gaps to Fix (Prioritized)

### Gap 1: Evening Service Period
**Priority: HIGH | Effort: LOW | Impact: HIGH**

**Current:** Single lunch service (10:00-14:00)
**Spec:** Two periods - Morning (10:00-14:00) and Evening (17:00-21:00)

**Why Fix:** Core gameplay loop change. Adds daily variety and time management decisions. Players must choose how to split time between exploration, dragon care, and two service windows.

**Implementation:**
- [ ] Add evening service window constants (17:00-21:00)
- [ ] Update CafeManager state transitions for second period
- [ ] Add evening prep/cleanup phases
- [ ] Update HUD to show next service time
- [ ] Balance customer volume between periods (lighter morning, busier evening)
- [ ] Add "skip evening service" option with reputation penalty

**Files to Modify:**
- `src/constants.py` - Add evening service constants
- `src/systems/cafe.py` - Dual service period logic
- `src/states/cafe_mode_state.py` - Handle both periods
- `src/ui/hud.py` - Service period display

---

### Gap 2: Adolescent & Adult Dragon Stages
**Priority: HIGH | Effort: MEDIUM | Impact: HIGH**

**Current:** Egg → Hatchling → Juvenile (3 stages)
**Spec:** Egg → Hatchling → Juvenile → Adolescent → Adult (5 stages)

**Why Fix:** Dragon progression is a core pillar. Two additional stages provide longer-term goals and unlock new abilities/zones.

**Implementation:**
- [ ] Add DRAGON_STAGE_ADOLESCENT and DRAGON_STAGE_ADULT constants
- [ ] Define stage durations (Adolescent: Days 6-12, Adult: Day 13+)
- [ ] Update Dragon entity stage progression logic
- [ ] Add adolescent/adult sprite generation
- [ ] Scale max stamina by stage
- [ ] Update dragon care screen for new stages

**Stage Progression (Adjusted for Prototype):**
| Stage | Days | Size Description |
|-------|------|------------------|
| Egg | Day 1 | 30cm diameter |
| Hatchling | Days 2-3 | Cat-sized |
| Juvenile | Days 4-5 | Large dog |
| Adolescent | Days 6-9 | Horse-sized |
| Adult | Day 10+ | Full dragon |

**Files to Modify:**
- `src/constants.py` - Stage constants and durations
- `src/entities/dragon.py` - Stage progression logic
- `src/sprites.py` - Adolescent/Adult sprite generation

**Dependencies:** None (foundational change)

---

### Gap 3: Missing Dragon Abilities
**Priority: HIGH | Effort: MEDIUM | Impact: HIGH**

**Current:** 3 abilities (burrow_fetch, sniff_track, rock_smash)
**Spec:** 8 abilities across all stages

**Missing Abilities:**
| Ability | Stage | Function | Stamina |
|---------|-------|----------|---------|
| Creature Scare | Juvenile | Frighten aggressive creatures | 20 |
| Glide | Adolescent | Descend safely, reach platforms | 3/sec |
| Ember Breath | Adolescent | Light torches, clear brambles | 25 |
| Full Flight | Adult | Free flight with player | 5/sec |
| Fire Stream | Adult | Powerful flame for obstacles | 40 |

**Implementation:**
- [ ] Add ability constants and stamina costs
- [ ] Implement creature_scare (zone creature interaction)
- [ ] Implement glide (vertical traversal in zones)
- [ ] Implement ember_breath (interact with bramble/torch objects)
- [ ] Implement full_flight (zone fast-travel or special areas)
- [ ] Implement fire_stream (powerful obstacle clearing)
- [ ] Update DRAGON_STAGE_ABILITIES mapping
- [ ] Add ability UI buttons/hotkeys

**Files to Modify:**
- `src/constants.py` - Ability definitions
- `src/entities/dragon.py` - Ability methods
- `src/states/exploration_mode_state.py` - Ability usage
- `src/sprites.py` - Ability visual effects

**Dependencies:** Gap 2 (new stages needed for Adolescent/Adult abilities)

---

### Gap 4: Additional World Zones
**Priority: HIGH | Effort: HIGH | Impact: HIGH**

**Current:** 3 zones (Cafe Grounds, Meadow Fields, Forest Depths)
**Spec:** 7 zones

**Missing Zones:**
| Zone | Stage Required | Primary Resources |
|------|----------------|-------------------|
| Coastal Shore | Juvenile | Seafood, salt, seaweed |
| Mountain Pass | Adolescent | Rare herbs, minerals, honey |
| Ancient Ruins | Adolescent | Special ingredients, recipes |
| Sky Islands | Adult | Legendary ingredients |

**Recommended for This Phase:** Add Coastal Shore and Mountain Pass (2 zones)
- Coastal Shore provides seafood ingredients for new recipes
- Mountain Pass unlocks with Adolescent stage

**Implementation:**
- [ ] Define zone constants and connections
- [ ] Create tile maps for new zones
- [ ] Define spawn points and ingredients
- [ ] Add zone unlock requirements
- [ ] Create zone-specific visuals in sprites.py
- [ ] Add new ingredients for zones

**New Ingredients:**
- Coastal: Sea Salt, Fresh Seaweed, Coastal Crab, Pearl Oyster
- Mountain: Mountain Herb, Rock Honey, Mineral Crystal, Alpine Flower

**Files to Modify:**
- `src/constants.py` - Zone and ingredient definitions
- `src/systems/world.py` - Zone data and connections
- `src/sprites.py` - Zone tile generation
- `src/systems/resources.py` - New spawn points

**Dependencies:** Gap 2 (Adolescent stage for Mountain Pass unlock)

---

### Gap 5: Autumn & Winter Seasons
**Priority: MEDIUM | Effort: LOW | Impact: MEDIUM**

**Current:** 2 seasons (Spring, Summer)
**Spec:** 4 seasons (Spring, Summer, Autumn, Winter)

**Why Fix:** Seasonal variety affects resource availability, customer preferences, and visual atmosphere.

**Implementation:**
- [ ] Add 'autumn' and 'winter' to SEASONS list
- [ ] Define weather probabilities for new seasons
- [ ] Add seasonal quality bonuses for ingredients
- [ ] Update time system season cycling
- [ ] Add autumn/winter color palettes
- [ ] Seasonal customer preference modifiers

**Season Effects:**
| Season | Weather Bias | Bonus Ingredients |
|--------|--------------|-------------------|
| Autumn | More cloudy/rainy | Mushrooms, nuts, root vegetables |
| Winter | More cloudy, rare snow | Preserved foods, warm dishes popular |

**Files to Modify:**
- `src/constants.py` - Season definitions and probabilities
- `src/systems/time_system.py` - Season cycling
- `src/sprites.py` - Seasonal color palettes

**Dependencies:** None

---

### Gap 6: Stormy & Special Weather
**Priority: MEDIUM | Effort: LOW | Impact: MEDIUM**

**Current:** 3 weather states (Sunny, Cloudy, Rainy)
**Spec:** 5 weather states (+ Stormy, Special)

**Why Fix:** Stormy weather creates risk/reward decisions. Special weather enables unique events.

**Implementation:**
- [ ] Add WEATHER_STORMY and WEATHER_SPECIAL constants
- [ ] Stormy: Cafe closed, exploration dangerous, rare resources
- [ ] Special: Unique events (meteor shower, etc.), legendary items
- [ ] Add weather probability per season
- [ ] Storm warning notification system
- [ ] Special weather event triggers

**Weather Effects:**
| Weather | Probability | Cafe | Exploration | Special Resources |
|---------|-------------|------|-------------|-------------------|
| Stormy | 10% | Closed | Dangerous | Storm flowers, lightning crystals |
| Special | 5% | Open | Safe | Event-specific legendary items |

**Files to Modify:**
- `src/constants.py` - Weather constants
- `src/systems/world.py` - Weather effects
- `src/systems/cafe.py` - Storm closure logic
- `src/states/exploration_mode_state.py` - Storm danger

**Dependencies:** None

---

### Gap 7: Additional Recipes (15-20 more)
**Priority: MEDIUM | Effort: MEDIUM | Impact: MEDIUM**

**Current:** 15 recipes
**Spec:** 80+ recipes

**Why Fix:** More recipes = more variety, longer engagement, better use of ingredients.

**Target:** Add 15-20 recipes to reach ~30-35 total (manageable scope increase)

**New Recipe Categories:**
- Seafood dishes (requires Coastal Shore zone)
- Warm/comfort dishes (popular in Autumn/Winter)
- Special/Legendary dishes (endgame content)

**Proposed New Recipes:**
| Recipe | Category | Difficulty | Key Ingredients |
|--------|----------|------------|-----------------|
| Coastal Chowder | Main | 3 | Coastal Crab, Sea Salt |
| Seaweed Salad | Appetizer | 1 | Fresh Seaweed, Wild Herb |
| Grilled Oysters | Appetizer | 2 | Pearl Oyster, Butter |
| Mountain Stew | Main | 3 | Alpine Flower, Game Meat |
| Honey Glazed Fish | Main | 3 | Forest Fish, Rock Honey |
| Autumn Harvest Soup | Main | 2 | Root vegetables, Mushroom |
| Winter Warmer | Beverage | 2 | Honey, Spiced Herbs |
| Dragon's Delight | Special | 5 | Crystal Shard, Rare Mushroom, Truffle |
| (+ 7-12 more) | Various | 1-5 | Various |

**Files to Modify:**
- `src/constants.py` - Recipe definitions
- `src/systems/recipes.py` - Recipe manager updates

**Dependencies:** Gap 4 (new zones for new ingredients)

---

### Gap 8: Additional Story Chapters
**Priority: MEDIUM | Effort: MEDIUM-HIGH | Impact: MEDIUM**

**Current:** 5 chapters (Prologue, Ch1-3, Epilogue)
**Spec:** 8 chapters (Prologue, Ch1-6, Finale)

**Why Fix:** Story is a core pillar. More chapters = more narrative engagement.

**Target:** Add 2 chapters (bringing total to 7)

**Proposed Chapters:**
| Chapter | Character | Theme | Unlock |
|---------|-----------|-------|--------|
| Chapter 4 | Captain Vera | Courage vs. recklessness | Dragon: Adolescent |
| Chapter 5 | The Masked Noble | Identity and authenticity | Reputation 200+ |

**Implementation:**
- [ ] Define chapter unlock conditions
- [ ] Create story events for each chapter
- [ ] Write dialogue trees
- [ ] Add character sprites
- [ ] Create chapter-specific recipes as rewards

**Files to Modify:**
- `src/constants.py` - Chapter definitions
- `src/systems/story.py` - Chapter progression
- `data/events/` - Story event JSON files
- `data/dialogues/` - Dialogue JSON files
- `data/characters/` - Character definitions
- `src/sprites.py` - New character sprites

**Dependencies:** Gap 2 (Adolescent stage for Chapter 4 unlock)

---

### Gap 9: Character Affinity System
**Priority: MEDIUM | Effort: MEDIUM-HIGH | Impact: MEDIUM**

**Current:** Event/flag-based story progression only
**Spec:** Per-character affinity 0-100 with thresholds

**Why Fix:** Adds depth to character relationships, encourages repeat interactions.

**Implementation:**
- [ ] Add affinity tracking to CharacterManager
- [ ] Define affinity gains: cooking dishes (+5/+10), gifts (+3-8), dialogue (+5-10)
- [ ] Add affinity thresholds for bonus content
- [ ] Display affinity on character interactions
- [ ] Unlock bonus dialogue/backstory at thresholds

**Affinity Thresholds:**
| Level | Points | Unlocks |
|-------|--------|---------|
| Acquaintance | 0-24 | Basic dialogue |
| Friendly | 25-49 | Personal stories |
| Close | 50-74 | Secret recipes |
| Best Friend | 75-100 | Special events |

**Files to Modify:**
- `src/entities/story_character.py` - Affinity tracking
- `src/systems/story.py` - Affinity-based event conditions
- `src/constants.py` - Affinity constants
- `src/ui/dialogue_box.py` - Affinity display

**Dependencies:** None (enhances existing system)

---

### Gap 10: Dragon Naming
**Priority: LOW | Effort: LOW | Impact: MEDIUM**

**Current:** Dragon referred to generically
**Spec:** Player-assigned name (max 20 chars)

**Why Fix:** Personal connection to dragon companion. Simple quality-of-life feature.

**Implementation:**
- [ ] Add name field to Dragon entity
- [ ] Create naming prompt during egg hatch event
- [ ] Update all dragon references to use name
- [ ] Add rename option in dragon status screen
- [ ] Validate name length (max 20 chars)

**Files to Modify:**
- `src/entities/dragon.py` - Name field
- `src/systems/story.py` - Hatch naming event
- `src/states/dragon_status_state.py` - Display/rename
- `src/ui/hud.py` - Dragon name in HUD

**Dependencies:** None

---

## Implementation Order

Based on dependencies and logical progression:

### Phase 1: Foundation (Gaps 10, 5, 6)
1. **Dragon Naming** - Quick win, no dependencies
2. **Autumn & Winter Seasons** - No dependencies, enables seasonal content
3. **Stormy & Special Weather** - No dependencies, adds variety

### Phase 2: Dragon Expansion (Gaps 2, 3)
4. **Adolescent & Adult Stages** - Foundation for abilities and zones
5. **Missing Dragon Abilities** - Requires new stages

### Phase 3: World Expansion (Gaps 4, 7)
6. **Additional Zones** - Requires Adolescent stage, enables new ingredients
7. **Additional Recipes** - Uses new ingredients from zones

### Phase 4: Story & Depth (Gaps 1, 8, 9)
8. **Evening Service Period** - Core gameplay enhancement
9. **Additional Story Chapters** - Narrative content
10. **Character Affinity System** - Relationship depth

---

## Estimated Effort

| Gap | Effort | Est. Time |
|-----|--------|-----------|
| Gap 10: Dragon Naming | Low | 1-2 hours |
| Gap 5: Seasons | Low | 2-3 hours |
| Gap 6: Weather | Low | 2-3 hours |
| Gap 2: Dragon Stages | Medium | 4-6 hours |
| Gap 3: Abilities | Medium | 4-6 hours |
| Gap 4: Zones (2) | High | 6-8 hours |
| Gap 7: Recipes | Medium | 3-4 hours |
| Gap 1: Evening Service | Low | 2-3 hours |
| Gap 8: Story Chapters | Medium-High | 6-8 hours |
| Gap 9: Affinity System | Medium-High | 4-6 hours |

**Total Estimated: 35-50 hours**

---

## Success Criteria

After completing all 10 gaps:
- [ ] Dragon progresses through 5 life stages
- [ ] 8 dragon abilities available across stages
- [ ] 5 explorable zones
- [ ] 30+ recipes
- [ ] 4 seasons with 5 weather types
- [ ] 7 story chapters
- [ ] Evening service period active
- [ ] Character affinity tracking
- [ ] Named dragon companion
- [ ] All existing functionality preserved

---

## Notes

- Each gap should be implemented on a feature branch
- Run full game test after each gap completion
- Update DECISIONS.md if any spec deviations are made
- Commit messages: `[EXP-N] Description` where N is gap number
