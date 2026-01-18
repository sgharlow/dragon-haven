# Task 014: Staff System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 014 |
| **Status** | ready |
| **Branch** | task/014 |
| **Assigned** | |
| **Depends** | 013 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/cafe.py from 013

## Description
Create the staff system with NPC workers who help run the cafe. Each staff member has unique traits, morale that affects performance, and can be directed by the player.

## Acceptance Criteria
- [ ] Staff class: name, role, trait, morale (0-100), efficiency
- [ ] 3 staff members:
  - Melody (Server): Enthusiastic but clumsy, needs pep talks
  - Bruno (Chef): Skilled but prideful, needs recipe guidance
  - Sage (Busser): Lazy but perceptive, needs frequent motivation
- [ ] Morale affects work efficiency (50% morale = 50% efficiency)
- [ ] Morale decays slowly over time
- [ ] talk_to(staff) increases morale (+10-20)
- [ ] assign_task(staff, task) for specific orders
- [ ] Autonomous behavior when not directed (with trait quirks)
- [ ] Staff can make mistakes based on trait (Melody drops things, etc.)
- [ ] Visual feedback for staff morale (happy/neutral/unhappy)
- [ ] Serialization for save/load

## Context Files
- src/systems/cafe.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.2)

## Outputs
- Created: src/entities/staff.py (Staff class, staff definitions)
- Modified: src/systems/cafe.py (integrate staff)
- Modified: src/constants.py (staff configs)

---

## Work Log

