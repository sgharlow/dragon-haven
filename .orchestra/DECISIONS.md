# Architectural Decisions

This document records all significant technical decisions made during development.

---

## DEC-001: Pygame with Procedural Assets

**Date:** 2026-01-17
**Status:** Accepted
**Context:** Need to choose game engine/framework for Dragon Haven Cafe prototype.

**Decision:** Use Python + Pygame with procedurally generated sprites and audio, matching the approach used in Space Station Defense.

**Rationale:**
- Proven approach from previous project
- No external asset dependencies
- Fast iteration on visual style
- Consistent aesthetic guaranteed
- Single-file distribution possible

**Consequences:**
- All sprites drawn with pygame.draw functions
- Sound effects synthesized at runtime
- May need optimization for complex scenes
- Art style will be geometric/retro

---

## DEC-002: Simplified Scope for Prototype

**Date:** 2026-01-17
**Status:** Accepted
**Context:** Full spec describes a 25-40 hour game with 5 dragon stages, 7 zones, 80+ recipes.

**Decision:** Build a focused vertical slice with:
- 3 dragon stages (Egg, Hatchling, Juvenile)
- 3 zones (Cafe Grounds, Meadow, Forest)
- 10-15 recipes
- 2 story chapters
- 15-30 minute gameplay loop

**Rationale:**
- Complete, polished experience better than incomplete ambitious one
- Core mechanics can be demonstrated in smaller scope
- Easier to expand later if desired
- Realistic for single-developer timeline

**Consequences:**
- Some spec features deferred (Adult dragon, Sky Islands, etc.)
- Focus on core loop quality
- Clear expansion path documented

---

## DEC-003: Balance Tuning for 15-30 Minute Sessions

**Date:** 2026-01-18
**Status:** Accepted
**Context:** Need to tune all gameplay values for satisfying progression within target 15-30 minute play sessions.

**Decision:** Adjusted the following balance parameters:

**Time System:**
- 30 real seconds = 1 game hour (was 60s)
- Full day = 12 real minutes
- Service period (4 hours) = 2 real minutes
- 7 days per season (was 10)

**Dragon Progression:**
- Egg hatches on Day 2 (was Day 4)
- Hatchling to Juvenile at Day 5 (was Day 11)
- Players see meaningful growth within one session

**Dragon Stats:**
- Hunger decay: 3/hour (depletes in ~16 min real)
- Happiness decay: 1/hour (depletes in ~50 min real)
- Generous feeding/petting rewards
- Earlier warning thresholds (40% vs 30%)

**Cooking Minigame:**
- Wider timing windows: PERFECT ±75ms, GOOD ±125ms, OK ±180ms
- Lower combo thresholds for multipliers
- Slower note speed (250 px/s normal, 180 px/s easy)
- Easy mode: 75% wider windows
- Shorter durations (12-20 seconds based on difficulty)

**Economy:**
- Starting gold: 150 (was 100)
- Quality thresholds more forgiving (3-star at 50%)
- Ingredient quality has smaller impact (±15% at extremes)

**Customer System:**
- Base patience: 2 game hours (60 real seconds)
- Urgent enough to feel exciting, not frustrating

**Rationale:**
- Casual players should feel rewarded, not punished
- Core loop (gather → cook → serve → grow dragon) must be achievable in one session
- Skill should be rewarded, but baseline competence should feel good
- Dragon companion must feel like companion, not obligation

**Consequences:**
- Very short sessions (5 min) may feel rushed
- Experienced players may find early game too easy
- Progression visible within first 15 minutes
- Players can complete prologue + start Chapter 1 in 30 minutes

---

## DEC-004: Additional Balance & Scope Adjustments

**Date:** 2026-01-18
**Status:** Accepted
**Context:** Several balance adjustments from the full spec were made for the prototype but not formally documented.

**Decisions:**

### Single Cafe Service Period
- **Spec:** Two service periods (Morning 10:00-14:00, Evening 17:00-21:00)
- **Prototype:** Single lunch service (10:00-14:00 only)
- **Rationale:** Simpler loop for 15-30 min sessions; evening service adds complexity without core value

### Dragon Bond Range
- **Spec:** 0-1000 lifetime bond
- **Prototype:** 0-500 bond
- **Rationale:** Lower max makes bond progression achievable in shorter play sessions

### Reputation Range & Tiers
- **Spec:** 0-1000 with 5 tiers (Unknown, Local Favorite, Town Attraction, Regional Fame, Legendary)
- **Prototype:** 0-500 with 4 tiers (no Legendary tier)
- **Rationale:** Proportionally scaled to match reduced content scope; Legendary tier requires endgame content not present in prototype

### Reputation Gain Values
- **Spec:** Character affinity gains specified (+5/+10 for dishes), cafe reputation gains not specified
- **Prototype:** +3 (happy customer), +5 (delighted customer)
- **Rationale:** Conservative gains ensure reputation feels earned; faster gains would trivialize progression

### Character Relationship System
- **Spec:** Per-character affinity 0-100 with thresholds and gifts
- **Prototype:** Event/flag-based story progression only
- **Rationale:** Simplified for prototype scope; affinity system requires more story characters than implemented

**Consequences:**
- Single service period means less daily variety but faster core loop
- Players can max bond/reputation within reasonable playtime
- Story progression is linear rather than relationship-driven

---

*Add new decisions above this line*
