"""
Story Event System for Dragon Haven Cafe.
Manages narrative events, triggers, and story progression.
"""

import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from pathlib import Path
from systems.dialogue import get_dialogue_manager


@dataclass
class EventCondition:
    """
    A condition that must be met for an event to trigger.

    Condition types:
    - time_of_day: hour range (e.g., [6, 12] for morning)
    - day_range: day number range (e.g., [1, 3])
    - reputation_min: minimum reputation level
    - dragon_stage: required dragon stage
    - events_completed: list of event IDs that must be completed
    - location: current location ID
    - flag: dialogue flag that must be set
    """
    type: str
    value: Any

    def to_dict(self) -> Dict[str, Any]:
        return {'type': self.type, 'value': self.value}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventCondition':
        return cls(type=data['type'], value=data['value'])


@dataclass
class EventOutcome:
    """
    An outcome applied when an event completes.

    Outcome types:
    - reputation_change: int change to reputation
    - unlock_recipe: recipe ID to unlock
    - unlock_zone: zone ID to unlock
    - set_flag: flag name to set
    - next_event: event ID to queue
    - gold_reward: gold amount to give
    """
    type: str
    value: Any

    def to_dict(self) -> Dict[str, Any]:
        return {'type': self.type, 'value': self.value}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventOutcome':
        return cls(type=data['type'], value=data['value'])


@dataclass
class StoryEvent:
    """
    A story event that can be triggered under certain conditions.

    Attributes:
        id: Unique identifier
        chapter: Story chapter (prologue, chapter1, chapter2, etc.)
        sequence_order: Order within chapter (for sorting)
        name: Display name
        description: Brief description
        conditions: List of conditions that must ALL be met
        dialogue_id: ID of dialogue to play
        outcomes: List of outcomes to apply on completion
        repeatable: Whether event can trigger multiple times
    """
    id: str
    chapter: str
    sequence_order: int
    name: str
    description: str = ""
    conditions: List[EventCondition] = field(default_factory=list)
    dialogue_id: Optional[str] = None
    outcomes: List[EventOutcome] = field(default_factory=list)
    repeatable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'chapter': self.chapter,
            'sequence_order': self.sequence_order,
            'name': self.name,
            'description': self.description,
            'conditions': [c.to_dict() for c in self.conditions],
            'dialogue_id': self.dialogue_id,
            'outcomes': [o.to_dict() for o in self.outcomes],
            'repeatable': self.repeatable,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StoryEvent':
        return cls(
            id=data['id'],
            chapter=data.get('chapter', 'prologue'),
            sequence_order=data.get('sequence_order', 0),
            name=data.get('name', ''),
            description=data.get('description', ''),
            conditions=[EventCondition.from_dict(c) for c in data.get('conditions', [])],
            dialogue_id=data.get('dialogue_id'),
            outcomes=[EventOutcome.from_dict(o) for o in data.get('outcomes', [])],
            repeatable=data.get('repeatable', False),
        )


class StoryManager:
    """
    Manages story events and progression.

    Usage:
        manager = get_story_manager()
        manager.load_events_from_directory('data/events/')

        # Each frame/tick:
        manager.check_triggers(game_state)

        # When dialogue ends:
        manager.complete_current_event()
    """

    # Chapter order
    CHAPTERS = ['prologue', 'chapter1', 'chapter2', 'chapter3', 'epilogue']

    def __init__(self):
        """Initialize the story manager."""
        # All events
        self._events: Dict[str, StoryEvent] = {}

        # Completed event IDs
        self._completed_events: List[str] = []

        # Event queue (pending events to trigger)
        self._event_queue: List[str] = []

        # Currently active event
        self._current_event: Optional[StoryEvent] = None

        # Current chapter
        self._current_chapter = 'prologue'

        # Story flags
        self._flags: Dict[str, bool] = {}

        # Callbacks for outcomes
        self._outcome_handlers: Dict[str, Callable[[Any], None]] = {}

        # Callback for event triggers
        self._on_event_start: Optional[Callable[[StoryEvent], None]] = None
        self._on_event_complete: Optional[Callable[[StoryEvent], None]] = None

        # Dialogue manager reference
        self._dialogue = get_dialogue_manager()

    # =========================================================================
    # EVENT LOADING
    # =========================================================================

    def load_event(self, event: StoryEvent):
        """Load an event into the manager."""
        self._events[event.id] = event

    def load_event_dict(self, data: Dict[str, Any]):
        """Load an event from dict data."""
        event = StoryEvent.from_dict(data)
        self.load_event(event)

    def load_events_file(self, filepath: str) -> int:
        """
        Load events from a JSON file.

        The file can contain either:
        - A single event object
        - An array of event objects

        Returns:
            Number of events loaded
        """
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Event file not found: {filepath}")
                return 0

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            count = 0
            if isinstance(data, list):
                for event_data in data:
                    self.load_event_dict(event_data)
                    count += 1
            else:
                self.load_event_dict(data)
                count = 1

            return count
        except Exception as e:
            print(f"Error loading events: {e}")
            return 0

    def load_events_from_directory(self, directory: str) -> int:
        """
        Load all event files from a directory.

        Returns:
            Total number of events loaded
        """
        count = 0
        path = Path(directory)
        if not path.exists():
            return 0

        for file in path.glob('*.json'):
            count += self.load_events_file(str(file))

        return count

    def get_event(self, event_id: str) -> Optional[StoryEvent]:
        """Get an event by ID."""
        return self._events.get(event_id)

    def get_events_by_chapter(self, chapter: str) -> List[StoryEvent]:
        """Get all events in a chapter, sorted by sequence order."""
        events = [e for e in self._events.values() if e.chapter == chapter]
        return sorted(events, key=lambda e: e.sequence_order)

    # =========================================================================
    # TRIGGER CHECKING
    # =========================================================================

    def check_triggers(self, game_state: Dict[str, Any]) -> Optional[str]:
        """
        Check all pending events for trigger conditions.

        Args:
            game_state: Dict containing:
                - hour: current hour (0-23)
                - day: current day number
                - reputation: reputation level
                - dragon_stage: dragon stage string
                - location: current location ID
                - gold: current gold amount

        Returns:
            Event ID if an event should trigger, None otherwise
        """
        if self._current_event:
            return None  # Already have an active event

        # Check events in order (by chapter, then sequence)
        for chapter in self.CHAPTERS:
            events = self.get_events_by_chapter(chapter)
            for event in events:
                # Skip completed non-repeatable events
                if event.id in self._completed_events and not event.repeatable:
                    continue

                # Skip events already in queue
                if event.id in self._event_queue:
                    continue

                # Check all conditions
                if self._check_event_conditions(event, game_state):
                    self._event_queue.append(event.id)

        # Trigger first queued event
        if self._event_queue:
            return self.trigger_event(self._event_queue[0])

        return None

    def _check_event_conditions(self, event: StoryEvent, game_state: Dict[str, Any]) -> bool:
        """Check if all conditions for an event are met."""
        for condition in event.conditions:
            if not self._check_condition(condition, game_state):
                return False
        return True

    def _check_condition(self, condition: EventCondition, game_state: Dict[str, Any]) -> bool:
        """Check a single condition."""
        ctype = condition.type
        value = condition.value

        if ctype == 'time_of_day':
            # Value is [start_hour, end_hour]
            hour = game_state.get('hour', 0)
            if isinstance(value, list) and len(value) == 2:
                return value[0] <= hour < value[1]
            return False

        elif ctype == 'day_range':
            # Value is [start_day, end_day]
            day = game_state.get('day', 1)
            if isinstance(value, list) and len(value) == 2:
                return value[0] <= day <= value[1]
            return False

        elif ctype == 'day_min':
            # Value is minimum day
            day = game_state.get('day', 1)
            return day >= value

        elif ctype == 'reputation_min':
            # Value is minimum reputation
            reputation = game_state.get('reputation', 0)
            return reputation >= value

        elif ctype == 'dragon_stage':
            # Value is required stage
            dragon_stage = game_state.get('dragon_stage', '')
            stages = ['egg', 'hatchling', 'juvenile']
            if dragon_stage in stages and value in stages:
                return stages.index(dragon_stage) >= stages.index(value)
            return dragon_stage == value

        elif ctype == 'events_completed':
            # Value is list of event IDs
            if isinstance(value, list):
                return all(eid in self._completed_events for eid in value)
            return value in self._completed_events

        elif ctype == 'location':
            # Value is location ID
            location = game_state.get('location', '')
            return location == value

        elif ctype == 'flag':
            # Value is flag name
            return self.has_flag(value)

        elif ctype == 'not_flag':
            # Value is flag name that must NOT be set
            return not self.has_flag(value)

        elif ctype == 'chapter':
            # Value is chapter that must be current
            return self._current_chapter == value

        return False

    # =========================================================================
    # EVENT EXECUTION
    # =========================================================================

    def trigger_event(self, event_id: str) -> Optional[str]:
        """
        Trigger an event and start its dialogue.

        Args:
            event_id: ID of event to trigger

        Returns:
            Dialogue ID if dialogue started, None otherwise
        """
        event = self._events.get(event_id)
        if not event:
            return None

        # Remove from queue if present
        if event_id in self._event_queue:
            self._event_queue.remove(event_id)

        self._current_event = event

        # Trigger callback
        if self._on_event_start:
            self._on_event_start(event)

        # Start dialogue if present
        if event.dialogue_id:
            self._dialogue.start_dialogue(event.dialogue_id)
            return event.dialogue_id

        # No dialogue - complete immediately
        self.complete_current_event()
        return None

    def complete_current_event(self):
        """Complete the current event and apply outcomes."""
        if not self._current_event:
            return

        event = self._current_event

        # Mark as completed
        if event.id not in self._completed_events:
            self._completed_events.append(event.id)

        # Apply outcomes
        for outcome in event.outcomes:
            self._apply_outcome(outcome)

        # Update chapter if needed
        self._check_chapter_progression()

        # Trigger callback
        if self._on_event_complete:
            self._on_event_complete(event)

        self._current_event = None

    def _apply_outcome(self, outcome: EventOutcome):
        """Apply an outcome."""
        otype = outcome.type
        value = outcome.value

        if otype == 'set_flag':
            self.set_flag(value)

        elif otype == 'clear_flag':
            self.clear_flag(value)

        elif otype == 'next_event':
            # Queue another event
            if value not in self._event_queue:
                self._event_queue.append(value)

        elif otype == 'set_chapter':
            self._current_chapter = value

        # Handle via registered handlers
        if otype in self._outcome_handlers:
            try:
                self._outcome_handlers[otype](value)
            except Exception as e:
                print(f"Error in outcome handler: {e}")

    def _check_chapter_progression(self):
        """Check if we should advance to the next chapter."""
        # Get all events in current chapter
        chapter_events = self.get_events_by_chapter(self._current_chapter)

        # Check if all non-repeatable events are completed
        all_complete = all(
            e.id in self._completed_events or e.repeatable
            for e in chapter_events
        )

        if all_complete and chapter_events:
            # Advance to next chapter
            current_idx = self.CHAPTERS.index(self._current_chapter)
            if current_idx < len(self.CHAPTERS) - 1:
                self._current_chapter = self.CHAPTERS[current_idx + 1]

    def queue_event(self, event_id: str):
        """Manually queue an event."""
        if event_id not in self._event_queue and event_id in self._events:
            self._event_queue.append(event_id)

    def get_current_event(self) -> Optional[StoryEvent]:
        """Get the currently active event."""
        return self._current_event

    def is_event_active(self) -> bool:
        """Check if an event is currently active."""
        return self._current_event is not None

    # =========================================================================
    # FLAGS
    # =========================================================================

    def set_flag(self, flag: str, value: bool = True):
        """Set a story flag."""
        self._flags[flag] = value
        # Also set in dialogue manager for cross-system consistency
        self._dialogue.set_flag(flag, value)

    def clear_flag(self, flag: str):
        """Clear a story flag."""
        self._flags.pop(flag, None)
        self._dialogue.clear_flag(flag)

    def has_flag(self, flag: str) -> bool:
        """Check if a flag is set."""
        return self._flags.get(flag, False)

    def get_all_flags(self) -> Dict[str, bool]:
        """Get all flags."""
        return self._flags.copy()

    # =========================================================================
    # CALLBACKS
    # =========================================================================

    def register_outcome_handler(self, outcome_type: str, handler: Callable[[Any], None]):
        """Register a handler for an outcome type."""
        self._outcome_handlers[outcome_type] = handler

    def on_event_start(self, callback: Callable[[StoryEvent], None]):
        """Set callback for event start."""
        self._on_event_start = callback

    def on_event_complete(self, callback: Callable[[StoryEvent], None]):
        """Set callback for event completion."""
        self._on_event_complete = callback

    # =========================================================================
    # STATE QUERIES
    # =========================================================================

    def get_current_chapter(self) -> str:
        """Get the current story chapter."""
        return self._current_chapter

    def is_event_completed(self, event_id: str) -> bool:
        """Check if an event has been completed."""
        return event_id in self._completed_events

    def get_completed_events(self) -> List[str]:
        """Get list of completed event IDs."""
        return self._completed_events.copy()

    def get_chapter_progress(self) -> Dict[str, Any]:
        """Get progress info for current chapter."""
        chapter_events = self.get_events_by_chapter(self._current_chapter)
        completed = sum(1 for e in chapter_events if e.id in self._completed_events)
        total = len([e for e in chapter_events if not e.repeatable])

        return {
            'chapter': self._current_chapter,
            'completed': completed,
            'total': total,
            'progress': completed / total if total > 0 else 1.0,
        }

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'completed_events': self._completed_events.copy(),
            'event_queue': self._event_queue.copy(),
            'current_chapter': self._current_chapter,
            'flags': self._flags.copy(),
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._completed_events = state.get('completed_events', [])
        self._event_queue = state.get('event_queue', [])
        self._current_chapter = state.get('current_chapter', 'prologue')
        self._flags = state.get('flags', {})

        # Sync flags to dialogue manager
        for flag, value in self._flags.items():
            self._dialogue.set_flag(flag, value)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_story_manager: Optional[StoryManager] = None


def get_story_manager() -> StoryManager:
    """Get the global story manager instance."""
    global _story_manager
    if _story_manager is None:
        _story_manager = StoryManager()
    return _story_manager


def reset_story_manager():
    """Reset the story manager (for new game)."""
    global _story_manager
    _story_manager = StoryManager()
