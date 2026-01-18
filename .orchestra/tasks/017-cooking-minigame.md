# Task 017: Cooking Minigame

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 017 |
| **Status** | in_progress |
| **Branch** | task/017 |
| **Assigned** | task/017 |
| **Depends** | 005, 016 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/sound_manager.py from 005
- src/systems/recipes.py from 016

## Description
Create the rhythm-based cooking minigame. Players press buttons in time with a pattern to cook dishes. Performance affects final dish quality.

## Acceptance Criteria
- [x] CookingMinigame class
- [x] 4-lane rhythm game (mapped to keyboard: A, S, D, F or arrow keys)
- [x] Notes fall from top, hit line at bottom
- [x] Timing grades: PERFECT, GOOD, OK, MISS
  - PERFECT: ±50ms, +100 points
  - GOOD: ±100ms, +70 points
  - OK: ±150ms, +30 points
  - MISS: beyond ±150ms, 0 points, combo break
- [x] Combo system (consecutive non-miss increases multiplier)
- [x] Pattern generation based on recipe difficulty
- [x] Song duration: 15-30 seconds based on recipe
- [x] Visual feedback: note highlights, hit effects
- [x] Sound effects on hits (procedural)
- [x] Final score calculation
- [x] Quality output: score mapped to 1-5 star dish quality
- [x] Ingredient quality bonus to final score
- [x] Easy mode option (wider timing windows)
- [x] Results screen with breakdown

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

### 2026-01-17
- Added cooking minigame constants to constants.py (timing windows, scoring, combos, visual settings)
- Created CookingMinigame class with full rhythm game implementation:
  - 4-lane system with A/S/D/F and arrow key support
  - Note falling from top with configurable speed
  - Timing grades (PERFECT, GOOD, OK, MISS) with configurable windows
  - Combo system with multipliers at 5/10/20/30 thresholds
  - Pattern generation based on recipe difficulty
  - Variable duration (15-30s based on difficulty)
  - Visual feedback (lane colors, hit effects, grade popups)
  - Sound integration with SoundManager
  - Score calculation with quality mapping (1-5 stars)
  - Ingredient quality bonus system
  - Easy mode (slower notes, wider timing)
  - Results screen with full breakdown
- Created CookingResult dataclass for result data
- Created src/ui/__init__.py with exports
- All tests pass

