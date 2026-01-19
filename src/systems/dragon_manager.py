"""
Dragon Manager for Dragon Haven Cafe.
Provides centralized access to the player's dragon across all game states.
"""

from typing import Optional, Callable, List
from entities.dragon import Dragon
from constants import DRAGON_NAME_DEFAULT


class DragonManager:
    """
    Singleton manager for the player's dragon.

    Provides centralized dragon access for states and systems.
    Supports callbacks for name changes and other dragon events.
    """

    def __init__(self):
        """Initialize the dragon manager."""
        self._dragon: Optional[Dragon] = None
        self._name_change_callbacks: List[Callable[[str], None]] = []
        self._naming_pending = False
        self._naming_callback: Optional[Callable[[], None]] = None

    def create_dragon(self, name: str = DRAGON_NAME_DEFAULT) -> Dragon:
        """
        Create a new dragon.

        Args:
            name: Initial name for the dragon

        Returns:
            The newly created Dragon instance
        """
        self._dragon = Dragon(name)
        return self._dragon

    def get_dragon(self) -> Optional[Dragon]:
        """Get the current dragon instance."""
        return self._dragon

    def set_dragon(self, dragon: Dragon):
        """
        Set the dragon instance.

        Args:
            dragon: Dragon instance to manage
        """
        self._dragon = dragon

    def has_dragon(self) -> bool:
        """Check if a dragon exists."""
        return self._dragon is not None

    def get_dragon_name(self) -> str:
        """Get the dragon's name, or default if no dragon."""
        if self._dragon:
            return self._dragon.get_name()
        return DRAGON_NAME_DEFAULT

    def set_dragon_name(self, name: str) -> bool:
        """
        Set the dragon's name.

        Args:
            name: New name for the dragon

        Returns:
            True if name was valid and set
        """
        if not self._dragon:
            return False

        if self._dragon.set_name(name):
            # Notify callbacks
            for callback in self._name_change_callbacks:
                try:
                    callback(name)
                except Exception as e:
                    print(f"Error in name change callback: {e}")
            return True
        return False

    def on_name_change(self, callback: Callable[[str], None]):
        """
        Register a callback for name changes.

        Args:
            callback: Function to call with the new name
        """
        self._name_change_callbacks.append(callback)

    def request_naming(self, callback: Optional[Callable[[], None]] = None):
        """
        Request the naming popup to be shown.

        Args:
            callback: Optional callback when naming is complete
        """
        self._naming_pending = True
        self._naming_callback = callback

    def is_naming_pending(self) -> bool:
        """Check if naming has been requested."""
        return self._naming_pending

    def complete_naming(self):
        """Mark naming as complete and trigger callback."""
        self._naming_pending = False
        if self._naming_callback:
            try:
                self._naming_callback()
            except Exception as e:
                print(f"Error in naming complete callback: {e}")
            self._naming_callback = None

    def cancel_naming(self):
        """Cancel pending naming request."""
        self._naming_pending = False
        self._naming_callback = None

    def get_state(self) -> dict:
        """Get state for saving."""
        if not self._dragon:
            return {}
        return self._dragon.get_state()

    def load_state(self, state: dict):
        """Load dragon state."""
        if not state:
            return

        if not self._dragon:
            self._dragon = Dragon()
        self._dragon.load_state(state)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_dragon_manager: Optional[DragonManager] = None


def get_dragon_manager() -> DragonManager:
    """Get the global dragon manager instance."""
    global _dragon_manager
    if _dragon_manager is None:
        _dragon_manager = DragonManager()
    return _dragon_manager


def reset_dragon_manager():
    """Reset the dragon manager (for testing)."""
    global _dragon_manager
    _dragon_manager = None
