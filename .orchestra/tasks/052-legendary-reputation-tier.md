# Task 052: Legendary Reputation Tier

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 052 |
| **Status** | done |
| **Branch** | task/052 |
| **Assigned** | |
| **Depends** | none |
| **Blocked-By** | |
| **Estimated** | 1-2 hours |

## Inputs
- Current reputation system in `src/systems/cafe.py`
- Reputation constants in `src/constants.py`

## Description
Add the 5th and final reputation tier "Legendary" for end-game players who achieve 500+ reputation.

### Implementation Tasks
1. Add `REPUTATION_LEGENDARY` constant (threshold: 500+)
2. Update `REPUTATION_TIERS` list to include Legendary
3. Add Legendary tier benefits:
   - 25% tip bonus (highest tier)
   - Access to VIP customers (flag for future use)
   - Unlock legendary recipes
4. Update HUD to display Legendary status with special styling
5. Add Legendary achievement trigger

## Acceptance Criteria
- [x] REPUTATION_LEGENDARY constant defined at 500
- [x] CafeManager.get_reputation_tier() returns 'Legendary' for 500+ rep
- [x] Legendary tier provides 25% tip bonus
- [x] HUD displays "Legendary" with distinct styling (gold color)
- [x] Game runs without errors
- [x] Save/load preserves reputation correctly

## Context Files
- `src/constants.py` - Reputation tier definitions
- `src/systems/cafe.py` - CafeManager tier calculation
- `src/ui/hud.py` - Reputation display

## Outputs
- Added `REPUTATION_LEVEL_LEGENDARY` constant (min: 500, max: 1000)
- Extended `REPUTATION_MAX` from 500 to 1000
- Added legendary tier to `REPUTATION_LEVELS` dict with name "Legendary"
- Added `REPUTATION_CUSTOMER_RANGE` for legendary: (7, 10) VIP volume
- Added `LEGENDARY_TIP_BONUS = 0.25` constant
- Updated `customer.py` `_calculate_tip()` to apply 25% bonus at legendary tier
- Updated `cafe.py` to import `REPUTATION_LEVEL_LEGENDARY`
- Updated `cafe_mode_state.py` to display gold color (255, 215, 0) for Legendary tier
- Added legendary recipe unlocks: `legendary_dragon_feast`, `mythic_tea_ceremony`

---
## Work Log
- 2026-01-20: Implemented Legendary reputation tier with all features complete
