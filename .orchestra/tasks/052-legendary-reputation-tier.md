# Task 052: Legendary Reputation Tier

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 052 |
| **Status** | ready |
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
- [ ] REPUTATION_LEGENDARY constant defined at 500
- [ ] CafeManager.get_reputation_tier() returns 'Legendary' for 500+ rep
- [ ] Legendary tier provides 25% tip bonus
- [ ] HUD displays "Legendary" with distinct styling (gold color)
- [ ] Game runs without errors
- [ ] Save/load preserves reputation correctly

## Context Files
- `src/constants.py` - Reputation tier definitions
- `src/systems/cafe.py` - CafeManager tier calculation
- `src/ui/hud.py` - Reputation display

## Outputs
<!-- Filled when complete -->

---
## Work Log
<!-- Appended during work -->
