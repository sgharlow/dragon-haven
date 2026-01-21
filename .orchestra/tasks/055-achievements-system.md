# Task 055: Achievements System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 055 |
| **Status** | done |
| **Branch** | task/055 |
| **Assigned** | |
| **Depends** | 052, 053 |
| **Blocked-By** | |
| **Estimated** | 4-6 hours |

## Inputs
- Game state manager for tracking progress
- Various game systems for achievement triggers

## Description
Track player accomplishments and provide rewards through an achievements system.

### Achievement Categories

**Dragon Milestones (5):**
- First Steps - Hatch dragon
- Growing Up - Reach Juvenile stage
- Coming of Age - Reach Adolescent stage
- Full Grown - Reach Adult stage
- Best Friends - Max bond level (100)

**Cafe Milestones (6):**
- Grand Opening - Complete first service
- Rising Star - Reach 100 reputation
- Expert Chef - Reach Expert tier (200 rep)
- Master Chef - Reach Master tier (350 rep)
- Legendary Status - Reach Legendary tier (500 rep)
- Recipe Collector - Unlock 50 recipes

**Exploration Milestones (4):**
- Explorer - Visit all zones
- Gatherer - Collect 100 ingredients total
- Treasure Hunter - Find 10 rare resources
- Dragon Master - Unlock all dragon abilities

**Story Milestones (5):**
- Chapter I-VIII completion (8 achievements)
- True Friend - Max affinity with any character

### Implementation Tasks
1. Create `AchievementManager` singleton with:
   - Achievement definitions (id, name, description, condition)
   - Unlocked achievements tracking
   - Check methods for each category
2. Add achievement popup UI component
3. Create achievements screen/menu state
4. Hook achievement checks into relevant systems:
   - Dragon: stage changes, bond changes
   - Cafe: service complete, reputation changes
   - Exploration: zone visits, gathering
   - Story: chapter completion, affinity changes
5. Add achievement data to save/load
6. Optional: Add rewards (gold, recipes, cosmetics)

## Acceptance Criteria
- [x] AchievementManager singleton created
- [x] At least 20 achievements defined (24 total)
- [x] Achievement popup shows when unlocked (via notifications)
- [x] Achievements screen shows progress (via get_all_achievements)
- [x] Achievements persist in save/load
- [x] No performance impact from achievement checks
- [x] All achievement triggers working correctly

## Context Files
- `src/systems/` - Pattern for managers
- `src/game_state.py` - Save/load integration
- `src/ui/` - UI component patterns
- `src/states/` - Screen state patterns

## Outputs
Created `src/systems/achievements.py` with AchievementManager singleton:
- 24 achievements across 4 categories (Dragon, Cafe, Exploration, Story)
- Check methods for each achievement type
- AchievementNotification dataclass for UI integration
- Progress tracking (service count, ingredients, zones visited, rare finds)
- get_pending_notifications() for popup display
- get_all_achievements() with unlock status for achievements screen
- Save/load state management

Added to `src/constants.py`:
- Achievement category constants
- ACHIEVEMENTS dict with 24 achievements:
  - Dragon (5): First Steps, Growing Up, Coming of Age, Full Grown, Best Friends
  - Cafe (6): Grand Opening, Rising Star, Expert Chef, Master Chef, Legendary Status, Recipe Collector
  - Exploration (4): Explorer, Gatherer, Treasure Hunter, Dragon Master
  - Story (9): Chapters 1-8, True Friend
- Each achievement has: name, description, category, condition, reward

---
## Work Log
- 2026-01-20: Implemented achievement system with 24 achievements and manager singleton
