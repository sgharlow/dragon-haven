"""
Time System for Dragon Haven Cafe.
Manages day/night cycle, seasons, and time-based events.
"""

from typing import Callable, List, Dict, Any
from constants import (
    TIME_MORNING_START, TIME_AFTERNOON_START, TIME_EVENING_START,
    REAL_SECONDS_PER_GAME_HOUR, GAME_HOURS_PER_DAY,
    DAYS_PER_SEASON, SEASONS,
    CAFE_OPEN_HOUR, CAFE_CLOSE_HOUR
)


class TimeManager:
    """
    Manages the in-game time, day/night cycle, and seasons.

    Usage:
        time_mgr = get_time_manager()
        time_mgr.update(dt)
        period = time_mgr.get_time_of_day()
    """

    # Time periods
    MORNING = 'morning'
    AFTERNOON = 'afternoon'
    EVENING = 'evening'
    NIGHT = 'night'

    def __init__(self):
        """Initialize the time manager."""
        self._current_hour = 8.0  # Start at 8:00 AM
        self._current_day = 1
        self._current_season_index = 0
        self._paused = False
        self._time_scale = 1.0  # Can speed up or slow down time

        # Track previous period for change detection
        self._previous_period = self.get_time_of_day()

        # Callbacks for time events
        self._period_change_callbacks: List[Callable[[str, str], None]] = []
        self._new_day_callbacks: List[Callable[[int], None]] = []
        self._new_season_callbacks: List[Callable[[str], None]] = []

        # Event scheduling
        self._scheduled_events: List[Dict[str, Any]] = []

    def update(self, dt: float):
        """
        Update the time system.

        Args:
            dt: Delta time in seconds
        """
        if self._paused:
            return

        # Calculate how many game hours pass
        game_hours_passed = (dt / REAL_SECONDS_PER_GAME_HOUR) * self._time_scale

        previous_hour = self._current_hour
        self._current_hour += game_hours_passed

        # Check for day rollover
        while self._current_hour >= GAME_HOURS_PER_DAY:
            self._current_hour -= GAME_HOURS_PER_DAY
            self._advance_day()

        # Check for period change
        current_period = self.get_time_of_day()
        if current_period != self._previous_period:
            self._on_period_change(self._previous_period, current_period)
            self._previous_period = current_period

        # Process scheduled events
        self._process_scheduled_events()

    def _advance_day(self):
        """Advance to the next day."""
        self._current_day += 1

        # Check for season change
        day_in_season = (self._current_day - 1) % DAYS_PER_SEASON
        if day_in_season == 0 and self._current_day > 1:
            self._current_season_index = (self._current_season_index + 1) % len(SEASONS)
            self._on_new_season()

        # Trigger new day callbacks
        for callback in self._new_day_callbacks:
            try:
                callback(self._current_day)
            except Exception as e:
                print(f"Error in new day callback: {e}")

    def _on_period_change(self, old_period: str, new_period: str):
        """Handle time period change."""
        for callback in self._period_change_callbacks:
            try:
                callback(old_period, new_period)
            except Exception as e:
                print(f"Error in period change callback: {e}")

    def _on_new_season(self):
        """Handle season change."""
        new_season = self.get_current_season()
        for callback in self._new_season_callbacks:
            try:
                callback(new_season)
            except Exception as e:
                print(f"Error in new season callback: {e}")

    def _process_scheduled_events(self):
        """Process any scheduled time-based events."""
        current_time = self._current_hour
        events_to_remove = []

        for event in self._scheduled_events:
            if current_time >= event['hour']:
                try:
                    event['callback']()
                except Exception as e:
                    print(f"Error in scheduled event: {e}")
                events_to_remove.append(event)

        for event in events_to_remove:
            self._scheduled_events.remove(event)

    # =========================================================================
    # TIME QUERIES
    # =========================================================================

    def get_time_of_day(self) -> str:
        """
        Get the current time period.

        Returns:
            'morning', 'afternoon', 'evening', or 'night'
        """
        hour = self._current_hour

        if TIME_MORNING_START <= hour < TIME_AFTERNOON_START:
            return self.MORNING
        elif TIME_AFTERNOON_START <= hour < TIME_EVENING_START:
            return self.AFTERNOON
        elif TIME_EVENING_START <= hour < 24:
            return self.EVENING
        else:
            return self.NIGHT

    def get_current_hour(self) -> float:
        """Get the current hour (0.0-23.999...)."""
        return self._current_hour

    def get_current_time(self) -> tuple:
        """
        Get current time as hours and minutes.

        Returns:
            Tuple of (hours, minutes) as integers
        """
        hours = int(self._current_hour)
        minutes = int((self._current_hour - hours) * 60)
        return (hours, minutes)

    def get_formatted_time(self) -> str:
        """
        Get current time as formatted string.

        Returns:
            Time string like "8:00 AM" or "2:30 PM"
        """
        hours, minutes = self.get_current_time()
        period = "AM" if hours < 12 else "PM"
        display_hours = hours if hours <= 12 else hours - 12
        if display_hours == 0:
            display_hours = 12
        return f"{display_hours}:{minutes:02d} {period}"

    def get_current_day(self) -> int:
        """Get the current day number."""
        return self._current_day

    def get_current_season(self) -> str:
        """Get the current season name."""
        return SEASONS[self._current_season_index]

    def get_day_in_season(self) -> int:
        """Get the day number within the current season (1-based)."""
        return ((self._current_day - 1) % DAYS_PER_SEASON) + 1

    def is_cafe_open(self) -> bool:
        """Check if the cafe is currently open for business."""
        return CAFE_OPEN_HOUR <= self._current_hour < CAFE_CLOSE_HOUR

    def is_daytime(self) -> bool:
        """Check if it's currently daytime (morning or afternoon)."""
        period = self.get_time_of_day()
        return period in (self.MORNING, self.AFTERNOON)

    def is_nighttime(self) -> bool:
        """Check if it's currently nighttime."""
        return self.get_time_of_day() == self.NIGHT

    def get_light_level(self) -> float:
        """
        Get the current ambient light level.

        Returns:
            Float from 0.0 (darkest) to 1.0 (brightest)
        """
        hour = self._current_hour

        if 6 <= hour < 8:
            # Dawn transition
            return 0.3 + 0.7 * ((hour - 6) / 2)
        elif 8 <= hour < 18:
            # Full daylight
            return 1.0
        elif 18 <= hour < 20:
            # Dusk transition
            return 1.0 - 0.5 * ((hour - 18) / 2)
        elif 20 <= hour < 22:
            # Evening
            return 0.5 - 0.2 * ((hour - 20) / 2)
        else:
            # Night
            return 0.3

    # =========================================================================
    # TIME CONTROL
    # =========================================================================

    def pause(self):
        """Pause time progression."""
        self._paused = True

    def resume(self):
        """Resume time progression."""
        self._paused = False

    def is_paused(self) -> bool:
        """Check if time is paused."""
        return self._paused

    def set_time_scale(self, scale: float):
        """
        Set the time progression speed multiplier.

        Args:
            scale: Multiplier (1.0 = normal, 2.0 = double speed, etc.)
        """
        self._time_scale = max(0.1, min(10.0, scale))

    def get_time_scale(self) -> float:
        """Get the current time scale."""
        return self._time_scale

    def advance_to_morning(self):
        """
        Skip time to the next morning (used for sleeping).
        Advances to 6:00 AM of the next day.
        """
        self._current_hour = TIME_MORNING_START
        self._advance_day()
        self._previous_period = self.get_time_of_day()

    def set_time(self, hour: float):
        """
        Set the current time (for debugging/testing).

        Args:
            hour: Hour to set (0.0-23.999...)
        """
        self._current_hour = max(0.0, min(23.999, hour))
        self._previous_period = self.get_time_of_day()

    def set_day(self, day: int):
        """
        Set the current day number (for debugging/testing).

        Args:
            day: Day number to set (1+)
        """
        self._current_day = max(1, day)

    # =========================================================================
    # CALLBACKS
    # =========================================================================

    def on_period_change(self, callback: Callable[[str, str], None]):
        """
        Register a callback for when time period changes.

        Args:
            callback: Function(old_period, new_period)
        """
        self._period_change_callbacks.append(callback)

    def on_new_day(self, callback: Callable[[int], None]):
        """
        Register a callback for when a new day starts.

        Args:
            callback: Function(day_number)
        """
        self._new_day_callbacks.append(callback)

    def on_new_season(self, callback: Callable[[str], None]):
        """
        Register a callback for when a new season starts.

        Args:
            callback: Function(season_name)
        """
        self._new_season_callbacks.append(callback)

    def schedule_event(self, hour: float, callback: Callable):
        """
        Schedule an event to trigger at a specific hour today.

        Args:
            hour: Hour to trigger (0.0-23.999...)
            callback: Function to call
        """
        self._scheduled_events.append({
            'hour': hour,
            'callback': callback
        })

    def clear_scheduled_events(self):
        """Clear all scheduled events."""
        self._scheduled_events.clear()

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> dict:
        """Get current state for saving."""
        return {
            'current_hour': self._current_hour,
            'current_day': self._current_day,
            'current_season_index': self._current_season_index,
            'time_scale': self._time_scale
        }

    def load_state(self, state: dict):
        """Load state from save data."""
        self._current_hour = state.get('current_hour', 8.0)
        self._current_day = state.get('current_day', 1)
        self._current_season_index = state.get('current_season_index', 0)
        self._time_scale = state.get('time_scale', 1.0)
        self._previous_period = self.get_time_of_day()


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_time_manager = None


def get_time_manager() -> TimeManager:
    """Get the global time manager instance."""
    global _time_manager
    if _time_manager is None:
        _time_manager = TimeManager()
    return _time_manager
