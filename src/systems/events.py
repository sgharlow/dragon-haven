"""
Seasonal Events System for Dragon Haven Cafe.
Manages special events tied to in-game seasons with unique content.
Phase 4 Feature.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum


# =============================================================================
# EVENT TYPES
# =============================================================================

class EventType(Enum):
    """Types of seasonal events."""
    SPRING_FESTIVAL = "spring_festival"
    SUMMER_FEAST = "summer_feast"
    AUTUMN_LANTERN = "autumn_lantern"
    WINTER_CELEBRATION = "winter_celebration"


# =============================================================================
# EVENT DEFINITIONS
# =============================================================================

@dataclass
class SeasonalEvent:
    """Definition of a seasonal event."""
    event_id: str
    name: str
    description: str
    season: str  # 'spring', 'summer', 'autumn', 'winter'
    start_day: int  # Day within season (1-10 for 10-day seasons)
    duration: int  # Number of days
    bonuses: Dict[str, float]  # Modifier bonuses
    special_recipes: List[str]  # Recipe IDs available during event
    decorations: List[str]  # Decoration IDs to apply
    special_customers: List[str]  # Customer type IDs

    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_id': self.event_id,
            'name': self.name,
            'description': self.description,
            'season': self.season,
            'start_day': self.start_day,
            'duration': self.duration,
            'bonuses': self.bonuses,
            'special_recipes': self.special_recipes,
            'decorations': self.decorations,
            'special_customers': self.special_customers,
        }


# Event definitions
SEASONAL_EVENTS: Dict[str, SeasonalEvent] = {
    'spring_festival': SeasonalEvent(
        event_id='spring_festival',
        name='Dragon Hatching Festival',
        description='Celebrate new beginnings! Dragon bonds grow faster during this festive time.',
        season='spring',
        start_day=1,
        duration=5,
        bonuses={
            'dragon_bond_gain': 1.5,  # +50% bond gain
            'egg_hatch_speed': 1.25,  # +25% faster hatching
        },
        special_recipes=['blossom_tea', 'spring_roll', 'honey_cake', 'flower_salad'],
        decorations=['cherry_blossoms', 'egg_banners', 'spring_flowers'],
        special_customers=['festival_goer', 'dragon_enthusiast'],
    ),
    'summer_feast': SeasonalEvent(
        event_id='summer_feast',
        name='Harvest Moon Feast',
        description='The summer harvest brings abundance! Ingredients are of exceptional quality.',
        season='summer',
        start_day=5,
        duration=6,
        bonuses={
            'ingredient_quality': 2.0,  # Double quality
            'gathering_yield': 1.5,  # +50% gathering
        },
        special_recipes=['starlight_sorbet', 'grilled_feast', 'summer_punch', 'moonberry_pie'],
        decorations=['harvest_wreaths', 'lanterns', 'fruit_displays'],
        special_customers=['merchant', 'traveling_chef'],
    ),
    'autumn_lantern': SeasonalEvent(
        event_id='autumn_lantern',
        name='Lantern Festival',
        description='Light up the night! Customers are generous during this magical celebration.',
        season='autumn',
        start_day=5,
        duration=6,
        bonuses={
            'tip_multiplier': 1.25,  # +25% tips
            'customer_patience': 1.2,  # +20% patience
        },
        special_recipes=['lantern_cake', 'spiced_cider', 'autumn_stew', 'candied_nuts'],
        decorations=['paper_lanterns', 'autumn_leaves', 'candle_arrangements'],
        special_customers=['lantern_maker', 'night_owl'],
    ),
    'winter_celebration': SeasonalEvent(
        event_id='winter_celebration',
        name='Frost Dragon Celebration',
        description='Warm hearts in cold weather! Cozy drinks and treats bring extra joy.',
        season='winter',
        start_day=5,
        duration=6,
        bonuses={
            'warm_drink_bonus': 1.5,  # +50% for warm drinks
            'reputation_gain': 1.25,  # +25% reputation
            'customer_satisfaction': 1.1,  # +10% base satisfaction
        },
        special_recipes=['frost_cocoa', 'winter_stew', 'gingerbread', 'mulled_wine'],
        decorations=['snowflakes', 'warm_lights', 'frost_crystals', 'gift_boxes'],
        special_customers=['gift_giver', 'caroler'],
    ),
}


# =============================================================================
# EVENT STATE
# =============================================================================

@dataclass
class EventState:
    """Tracks the current state of seasonal events."""
    active_event: Optional[str] = None
    event_day: int = 0  # Day within the event (1-based)
    events_participated: Dict[str, int] = field(default_factory=dict)  # event_id -> times participated
    special_recipes_unlocked: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'active_event': self.active_event,
            'event_day': self.event_day,
            'events_participated': self.events_participated.copy(),
            'special_recipes_unlocked': self.special_recipes_unlocked.copy(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventState':
        state = cls()
        state.active_event = data.get('active_event')
        state.event_day = data.get('event_day', 0)
        state.events_participated = data.get('events_participated', {})
        state.special_recipes_unlocked = data.get('special_recipes_unlocked', [])
        return state


# =============================================================================
# EVENT MANAGER
# =============================================================================

class EventManager:
    """
    Manages seasonal events and their effects on gameplay.

    Usage:
        events = get_event_manager()
        events.update(current_season, day_in_season)

        if events.is_event_active():
            bonus = events.get_bonus('tip_multiplier')
    """

    def __init__(self):
        self._state = EventState()
        self._callbacks_on_event_start: List[Callable[[SeasonalEvent], None]] = []
        self._callbacks_on_event_end: List[Callable[[SeasonalEvent], None]] = []

    def update(self, current_season: str, day_in_season: int) -> Optional[str]:
        """
        Update event state based on current time.

        Args:
            current_season: Current season ('spring', 'summer', 'autumn', 'winter')
            day_in_season: Day number within the season (1-10)

        Returns:
            Event ID if an event just started, None otherwise
        """
        # Find if any event should be active
        new_event = None
        for event_id, event in SEASONAL_EVENTS.items():
            if event.season == current_season:
                event_start = event.start_day
                event_end = event.start_day + event.duration - 1

                if event_start <= day_in_season <= event_end:
                    new_event = event_id
                    break

        # Handle event transitions
        if new_event != self._state.active_event:
            # End previous event
            if self._state.active_event:
                old_event = SEASONAL_EVENTS.get(self._state.active_event)
                if old_event:
                    self._on_event_end(old_event)

            # Start new event
            if new_event:
                event = SEASONAL_EVENTS[new_event]
                self._state.active_event = new_event
                self._state.event_day = day_in_season - event.start_day + 1
                self._on_event_start(event)

                # Track participation
                self._state.events_participated[new_event] = \
                    self._state.events_participated.get(new_event, 0) + 1

                # Unlock special recipes
                for recipe_id in event.special_recipes:
                    if recipe_id not in self._state.special_recipes_unlocked:
                        self._state.special_recipes_unlocked.append(recipe_id)

                return new_event
            else:
                self._state.active_event = None
                self._state.event_day = 0

        elif new_event:
            # Update day within event
            event = SEASONAL_EVENTS[new_event]
            self._state.event_day = day_in_season - event.start_day + 1

        return None

    def _on_event_start(self, event: SeasonalEvent):
        """Called when an event starts."""
        for callback in self._callbacks_on_event_start:
            callback(event)

    def _on_event_end(self, event: SeasonalEvent):
        """Called when an event ends."""
        for callback in self._callbacks_on_event_end:
            callback(event)

    def on_event_start(self, callback: Callable[[SeasonalEvent], None]):
        """Register a callback for event start."""
        self._callbacks_on_event_start.append(callback)

    def on_event_end(self, callback: Callable[[SeasonalEvent], None]):
        """Register a callback for event end."""
        self._callbacks_on_event_end.append(callback)

    def is_event_active(self) -> bool:
        """Check if any event is currently active."""
        return self._state.active_event is not None

    def get_active_event(self) -> Optional[SeasonalEvent]:
        """Get the currently active event."""
        if self._state.active_event:
            return SEASONAL_EVENTS.get(self._state.active_event)
        return None

    def get_event_day(self) -> int:
        """Get the current day within the active event."""
        return self._state.event_day

    def get_event_progress(self) -> float:
        """Get event progress as a percentage (0.0-1.0)."""
        event = self.get_active_event()
        if event and event.duration > 0:
            return self._state.event_day / event.duration
        return 0.0

    def get_bonus(self, bonus_name: str, default: float = 1.0) -> float:
        """
        Get a bonus modifier from the active event.

        Args:
            bonus_name: Name of the bonus (e.g., 'tip_multiplier')
            default: Default value if no event or bonus not found

        Returns:
            Bonus multiplier value
        """
        event = self.get_active_event()
        if event:
            return event.bonuses.get(bonus_name, default)
        return default

    def get_active_decorations(self) -> List[str]:
        """Get decoration IDs for the active event."""
        event = self.get_active_event()
        if event:
            return event.decorations
        return []

    def get_special_customers(self) -> List[str]:
        """Get special customer types for the active event."""
        event = self.get_active_event()
        if event:
            return event.special_customers
        return []

    def get_event_recipes(self) -> List[str]:
        """Get recipe IDs available during the active event."""
        event = self.get_active_event()
        if event:
            return event.special_recipes
        return []

    def is_recipe_available(self, recipe_id: str) -> bool:
        """Check if a seasonal recipe is currently available."""
        event = self.get_active_event()
        if event and recipe_id in event.special_recipes:
            return True
        return False

    def get_times_participated(self, event_id: str) -> int:
        """Get number of times player has participated in an event."""
        return self._state.events_participated.get(event_id, 0)

    def get_all_unlocked_recipes(self) -> List[str]:
        """Get all special recipes ever unlocked through events."""
        return self._state.special_recipes_unlocked.copy()

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return self._state.to_dict()

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._state = EventState.from_dict(state)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_event_manager: Optional[EventManager] = None


def get_event_manager() -> EventManager:
    """Get the global event manager instance."""
    global _event_manager
    if _event_manager is None:
        _event_manager = EventManager()
    return _event_manager
