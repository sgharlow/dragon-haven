# Task 017: Cooking Minigame

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 017 |
| **Status** | ready |
| **Branch** | task/017 |
| **Assigned** | |
| **Depends** | 005, 016 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/sound_manager.py from 005
- src/systems/recipes.py from 016

## Description
Create the rhythm-based cooking minigame. Players press buttons in time with a pattern to cook dishes. Performance affects final dish quality.

## Acceptance Criteria
- [ ] CookingMinigame class
- [ ] 4-lane rhythm game (mapped to keyboard: A, S, D, F or arrow keys)
- [ ] Notes fall from top, hit line at bottom
- [ ] Timing grades: PERFECT, GOOD, OK, MISS
  - PERFECT: ±50ms, +100 points
  - GOOD: ±100ms, +70 points
  - OK: ±150ms, +30 points
  - MISS: beyond ±150ms, 0 points, combo break
- [ ] Combo system (consecutive non-miss increases multiplier)
- [ ] Pattern generation based on recipe difficulty
- [ ] Song duration: 15-30 seconds based on recipe
- [ ] Visual feedback: note highlights, hit effects
- [ ] Sound effects on hits (procedural)
- [ ] Final score calculation
- [ ] Quality output: score mapped to 1-5 star dish quality
- [ ] Ingredient quality bonus to final score
- [ ] Easy mode option (wider timing windows)
- [ ] Results screen with breakdown

## Context Files
- src/sound_manager.py
- src/systems/recipes.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.3.2)

## Outputs
- Created: src/ui/cooking_minigame.py (CookingMinigame class)
- Created: src/ui/__init__.py
- Modified: src/constants.py (timing windows, scoring)

---

## Work Log

