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

*Add new decisions above this line*
