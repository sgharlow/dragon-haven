# Task 013: Cafe State and Operations

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 013 |
| **Status** | done |
| **Branch** | task/013 |
| **Assigned** | task/013 |
| **Depends** | 007, 012 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/time_system.py from 007
- src/systems/economy.py from 012

## Description
Create the cafe management system that handles cafe operations, service periods, and overall cafe state. The core framework for cafe gameplay.

## Acceptance Criteria
- [x] CafeManager class with singleton get_cafe_manager()
- [x] Cafe states: CLOSED, PREP, SERVICE, CLEANUP
- [x] Service period: 10:00-14:00 (single period for prototype)
- [x] start_service(), end_service() methods
- [x] Service automatically starts/ends based on time
- [x] Prep phase (30 min before service) for setup
- [x] Track customers served today
- [x] Track revenue today
- [x] Menu management (which recipes are available today)
- [x] set_menu(), get_menu()
- [x] Cafe can be skipped (with reputation penalty)
- [x] Callbacks for service events
- [x] Serialization for save/load

## Context Files
- src/systems/time_system.py
- src/systems/economy.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.1)

## Outputs
- Created: src/systems/cafe.py (CafeManager, get_cafe_manager)
- Modified: src/constants.py (cafe timing, service config)

---

## Work Log

### 2026-01-17
- Added cafe state constants to constants.py (CLOSED, PREP, SERVICE, CLEANUP)
- Added service timing configuration (10:00-14:00 service period)
- Created CafeManager class with singleton pattern
- Implemented state machine with automatic time-based transitions
- Created ServiceStats dataclass for tracking daily performance
- Implemented menu management (add/remove/set/get)
- Added service tracking (record_sale, record_customer_served)
- Implemented skip day functionality with reputation penalty
- Added callback system for state change events
- Implemented full serialization (get_save_state/load_state)
- Updated systems/__init__.py
- All tests pass

